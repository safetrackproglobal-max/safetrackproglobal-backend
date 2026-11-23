"""
Environmental analytics over the company's own monitoring records (2026-11-22).

Replaces the "AI" endpoints that called a service which never existed (every request failed and the
screen silently showed invented demo results).  Every number here is derived from the company's
readings, samples, incidents, goals and compliance reports, with simple, explainable methods:
  - forecasts      : least-squares trend of daily averages
  - anomalies      : robust z-score (median / MAD) per parameter and location + regulatory limits
  - risk & ESG     : weighted indicators with the inputs shown
When there is not enough data the result says so instead of guessing.
Pure Python (no Flask / DB) so it can be unit-tested.

ctx = {
  'daily_air': [{'date','pm2_5','pm10','aqi','readings'}],
  'air_readings': [{'timestamp','location','pm2_5','pm10','aqi','temperature','humidity'}],
  'water_samples': [{'timestamp','location','ph','turbidity','dissolved_oxygen','compliant'}],
  'incidents': [{'date','severity','status','type','title'}],
  'safety_incidents': [{'date','severity','status'}],
  'goals': [{'goal','category','progress','deadline','started','status'}],
  'reports': [{'type','status','next_submission','findings'}],
  'sensors': {'total','active'},
  'now': datetime
}
"""
from datetime import datetime, timedelta
import math

WHO = {'pm2_5': 15.0, 'pm10': 45.0, 'aqi': 100.0}
WATER_LIMITS = {'ph': (6.5, 8.5), 'turbidity': (None, 5.0), 'dissolved_oxygen': (5.0, None)}
CLOSED = ('resolved', 'closed', 'completed')
SEVERE = ('high', 'critical', 'major', 'severe')


def _mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def _pct(part, whole):
    return round(part / whole * 100, 1) if whole else None


def linear_forecast(values, horizon):
    pts = [(i, v) for i, v in enumerate(values) if v is not None]
    if len(pts) < 3:
        return None, None, None
    n = len(pts)
    mx = sum(x for x, _ in pts) / n
    my = sum(y for _, y in pts) / n
    sxx = sum((x - mx) ** 2 for x, _ in pts) or 1
    slope = sum((x - mx) * (y - my) for x, y in pts) / sxx
    intercept = my - slope * mx
    resid = math.sqrt(sum((y - (intercept + slope * x)) ** 2 for x, y in pts) / max(n - 2, 1))
    last = len(values) - 1
    return [max(0.0, round(intercept + slope * (last + k), 2)) for k in range(1, horizon + 1)], slope, resid


def _trend_word(slope, level):
    if slope is None or not level:
        return 'unknown'
    rel = slope / level
    return 'increasing' if rel > 0.02 else 'decreasing' if rel < -0.02 else 'stable'


def _not_enough(msg, **extra):
    return {'insufficient_data': True, 'message': msg, **extra}


# ------------------------------------------------------------------ forecast
def predict_air_quality(ctx, horizon_days=3, confidence_threshold=0.0):
    horizon = max(1, min(int(horizon_days or 3), 30))
    daily = ctx.get('daily_air') or []
    if len([d for d in daily if d.get('pm2_5') is not None or d.get('aqi') is not None]) < 3:
        return _not_enough('At least 3 days of air-quality readings are needed for a forecast.',
                           predictions=[], trend='unknown', risk_alerts=[], recommendations=[
                               'Add air-quality sensors or enter readings so forecasts can be calculated.'],
                           data_points=len(daily))
    series = {k: [d.get(k) for d in daily] for k in ('pm2_5', 'pm10', 'aqi')}
    fc, slopes, resid = {}, {}, {}
    for k, vals in series.items():
        fc[k], slopes[k], resid[k] = linear_forecast(vals, horizon)
    now = ctx.get('now') or datetime.utcnow()
    level = _mean(series['pm2_5']) or _mean(series['aqi'])
    base_err = (resid.get('pm2_5') or resid.get('aqi') or 0) / (level or 1)
    preds = []
    for i in range(horizon):
        conf = max(0.3, min(0.95, 0.92 - 0.04 * i - base_err * 0.5 - (0.1 if len(daily) < 7 else 0)))
        preds.append({'timestamp': (now + timedelta(days=i + 1)).replace(hour=12, minute=0, second=0, microsecond=0).isoformat(),
                      'pm2_5': fc['pm2_5'][i] if fc['pm2_5'] else None, 'pm10': fc['pm10'][i] if fc['pm10'] else None,
                      'aqi': round(fc['aqi'][i]) if fc['aqi'] else None, 'confidence': round(conf, 2),
                      'below_confidence_threshold': conf < float(confidence_threshold or 0)})
    alerts = []
    for p in preds:
        day = p['timestamp'][:10]
        if p['pm2_5'] is not None and p['pm2_5'] > WHO['pm2_5']:
            alerts.append(f"{day}: PM2.5 forecast {p['pm2_5']} µg/m³ is above the WHO guideline ({WHO['pm2_5']:.0f})")
        if p['aqi'] is not None and p['aqi'] > 100:
            alerts.append(f"{day}: AQI forecast {p['aqi']} — unhealthy for sensitive groups")
    trend = _trend_word(slopes.get('pm2_5') if slopes.get('pm2_5') is not None else slopes.get('aqi'), level)
    recs = []
    if alerts:
        recs += ['Plan dusty or combustion work for days with lower forecasts', 'Issue respiratory protection where exposure is likely',
                 'Check dust suppression and extraction systems before the forecast peak']
    if trend == 'increasing':
        recs.append('Particulate levels are rising — investigate sources (traffic, construction, generators, open burning)')
    if not recs:
        recs.append('Forecast within guideline values — keep routine monitoring')
    return {'predictions': preds, 'trend': trend, 'risk_alerts': alerts, 'recommendations': recs,
            'method': 'Least-squares trend of daily averages', 'data_points': len(daily),
            'typical_error_pm2_5': round(resid['pm2_5'], 2) if resid.get('pm2_5') is not None else None}


# ------------------------------------------------------------------ anomalies
def _robust_stats(values):
    vals = sorted(v for v in values if v is not None)
    if len(vals) < 5:
        return None, None
    med = vals[len(vals) // 2]
    mad = sorted(abs(v - med) for v in vals)[len(vals) // 2]
    return med, (mad * 1.4826) or (abs(med) * 0.05) or 1.0


def detect_anomalies(ctx, sensitivity='medium', scope='all'):
    z_lim = {'high': 2.5, 'medium': 3.0, 'low': 3.5}.get(str(sensitivity).lower(), 3.0)
    details = []
    groups = {}
    if scope in ('all', 'air', 'air_quality', None, ''):
        for r in ctx.get('air_readings') or []:
            for k in ('pm2_5', 'pm10', 'aqi', 'temperature', 'humidity'):
                if r.get(k) is not None:
                    groups.setdefault(('air', k, r.get('location') or 'Unknown sensor'), []).append((r.get('timestamp'), r[k]))
    if scope in ('all', 'water', 'water_quality', None, ''):
        for r in ctx.get('water_samples') or []:
            for k in ('ph', 'turbidity', 'dissolved_oxygen'):
                if r.get(k) is not None:
                    groups.setdefault(('water', k, r.get('location') or 'Unknown site'), []).append((r.get('timestamp'), r[k]))
    labels = {'pm2_5': ('PM2.5', 'µg/m³'), 'pm10': ('PM10', 'µg/m³'), 'aqi': ('AQI', ''), 'temperature': ('Temperature', '°C'),
              'humidity': ('Humidity', '%'), 'ph': ('Water pH', ''), 'turbidity': ('Turbidity', 'NTU'),
              'dissolved_oxygen': ('Dissolved oxygen', 'mg/L')}
    checked = 0
    for (kind, k, loc), pts in groups.items():
        checked += len(pts)
        med, scale = _robust_stats([v for _, v in pts])
        name, unit = labels[k]
        for ts, v in pts:
            reasons, sev = [], None
            if med is not None:
                z = abs(v - med) / scale
                if z >= z_lim:
                    reasons.append(f'{z:.1f}× the usual variation for this location')
                    sev = 'HIGH' if z >= z_lim * 2 else 'MEDIUM'
            lim = WHO.get(k)
            if lim and v > lim * 2:
                reasons.append(f'more than twice the guideline ({lim:g})')
                sev = 'HIGH'
            wl = WATER_LIMITS.get(k)
            if wl and ((wl[0] is not None and v < wl[0]) or (wl[1] is not None and v > wl[1])):
                reasons.append('outside the regulatory range')
                sev = sev or 'MEDIUM'
            if reasons:
                expected = (f'{med - z_lim * scale:.1f}–{med + z_lim * scale:.1f} {unit}'.strip() if med is not None else
                            (f"{wl[0] if wl and wl[0] is not None else '…'}–{wl[1] if wl and wl[1] is not None else '…'} {unit}".strip() if wl else f'≤ {lim:g} {unit}'))
                details.append({'timestamp': ts, 'parameter': name, 'value': round(v, 2), 'expected_range': expected,
                                'severity': 'CRITICAL' if sev == 'HIGH' and (lim and v > lim * 3) else sev or 'LOW',
                                'location': loc, 'description': f'{name} {round(v, 2)} {unit} — ' + '; '.join(reasons)})
    details.sort(key=lambda d: ({'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}[d['severity']], str(d['timestamp'] or '')), reverse=False)
    if not checked:
        return _not_enough('No readings or samples in the selected window.', anomalies_detected=0, critical_anomalies=0,
                           anomaly_details=[], root_cause_analysis=[], automatic_actions=[])
    causes = []
    locs = {}
    for d in details:
        locs[d['location']] = locs.get(d['location'], 0) + 1
    if details:
        top_loc, top_n = max(locs.items(), key=lambda kv: kv[1])
        if top_n >= max(2, len(details) * 0.6):
            causes.append(f'Most anomalies ({top_n}) come from "{top_loc}" — check that sensor or process (calibration, local source, equipment fault)')
        elif len(locs) > 1:
            causes.append(f'Anomalies at {len(locs)} locations at once usually point to an external cause (weather, nearby activity)')
        if any(d['parameter'] in ('Water pH', 'Turbidity') for d in details):
            causes.append('Water anomalies: review treatment dosing, run-off after rain and discharge sources')
        if any(d['parameter'] in ('PM2.5', 'PM10') for d in details):
            causes.append('Particulate spikes: dust from earthworks/traffic, generator or combustion emissions')
    actions = (['Confirm the reading (re-sample / check sensor calibration)', 'Inspect the location and record the likely source',
                'Log an environmental incident if the exceedance is confirmed', 'Increase monitoring frequency until values normalise']
               if details else ['No action needed — all values within their usual range'])
    return {'anomalies_detected': len(details), 'critical_anomalies': sum(1 for d in details if d['severity'] in ('CRITICAL', 'HIGH')),
            'anomaly_details': details[:100], 'root_cause_analysis': causes, 'automatic_actions': actions,
            'values_checked': checked, 'method': f'Robust z-score (median/MAD), threshold {z_lim}, plus regulatory limits'}


# ------------------------------------------------------------------ indicators shared by risk / ESG / advanced
def indicators(ctx):
    air = ctx.get('air_readings') or []
    measured = [r for r in air if r.get('pm2_5') is not None or r.get('pm10') is not None]
    air_ok = [r for r in measured if (r.get('pm2_5') is None or r['pm2_5'] <= WHO['pm2_5']) and (r.get('pm10') is None or r['pm10'] <= WHO['pm10'])]
    water = [w for w in ctx.get('water_samples') or [] if w.get('compliant') is not None]
    inc = ctx.get('incidents') or []
    open_inc = [i for i in inc if (i.get('status') or '').lower() not in CLOSED]
    severe_open = [i for i in open_inc if (i.get('severity') or '').lower() in SEVERE]
    reports = ctx.get('reports') or []
    now = ctx.get('now') or datetime.utcnow()
    overdue = [r for r in reports if r.get('next_submission') and r['next_submission'] < now and (r.get('status') or '') not in ('submitted', 'approved')]
    goals = ctx.get('goals') or []
    behind = []
    for g in goals:
        if g.get('deadline') and g.get('started') and (g.get('status') or '') not in ('completed', 'achieved'):
            span = (g['deadline'] - g['started']).total_seconds()
            if span > 0:
                expected = min(100, max(0, (now - g['started']).total_seconds() / span * 100))
                if (g.get('progress') or 0) + 10 < expected:
                    behind.append(g)
    sensors = ctx.get('sensors') or {}
    safety = ctx.get('safety_incidents') or []
    return {
        'air_compliance': _pct(len(air_ok), len(measured)), 'air_readings': len(measured),
        'water_compliance': _pct(sum(1 for w in water if w['compliant']), len(water)), 'water_samples': len(water),
        'incidents': len(inc), 'open_incidents': len(open_inc), 'severe_open': len(severe_open),
        'reports': len(reports), 'overdue_reports': len(overdue),
        'goals': len(goals), 'goals_behind': len(behind), 'goal_progress': _mean([g.get('progress') for g in goals]),
        'sensors_total': sensors.get('total', 0), 'sensors_active': sensors.get('active', 0),
        'safety_incidents': len(safety), 'safety_open': sum(1 for s in safety if (s.get('status') or '').lower() not in CLOSED),
        'behind_list': [g.get('goal') for g in behind][:5],
    }


# ------------------------------------------------------------------ risk
def assess_risk(ctx, tolerance='medium', include_external=False):
    ind = indicators(ctx)
    strict = {'low': 0.8, 'medium': 1.0, 'high': 1.2}.get(str(tolerance).lower(), 1.0)
    high, medium, low, mitig = [], [], [], []
    score = 0.0

    def add(points, text, level, fix):
        nonlocal score
        score += points
        {'high': high, 'medium': medium, 'low': low}[level].append(text)
        if fix and level != 'low':
            mitig.append(fix)

    ac = ind['air_compliance']
    if ac is None:
        add(10, 'No air-quality data — air risks cannot be assessed', 'medium', 'Install or connect air-quality monitoring')
    elif ac < 75 * strict:
        add(25, f'Only {ac:.0f}% of air readings meet the WHO guideline ({ind["air_readings"]} readings)', 'high',
            'Reduce particulate sources and add dust suppression / extraction')
    elif ac < 90 * strict:
        add(12, f'{ac:.0f}% of air readings meet the WHO guideline', 'medium', 'Investigate the days with exceedances')
    else:
        low.append(f'Air quality: {ac:.0f}% of readings within guideline')
    wc = ind['water_compliance']
    if wc is None:
        add(8, 'No water-quality samples in the period', 'medium', 'Set up a regular water sampling schedule')
    elif wc < 90 * strict:
        add(22, f'{100 - wc:.0f}% of water samples were non-compliant ({ind["water_samples"]} samples)', 'high',
            'Review treatment and discharge controls; re-sample failing sites')
    elif wc < 100:
        add(8, f'{100 - wc:.0f}% of water samples were non-compliant', 'medium', 'Follow up the non-compliant samples')
    else:
        low.append(f'Water quality: all {ind["water_samples"]} samples compliant')
    if ind['severe_open']:
        add(min(25, 10 * ind['severe_open']), f'{ind["severe_open"]} high/critical environmental incident(s) still open', 'high',
            'Close out the open high-severity incidents with root-cause actions')
    elif ind['open_incidents']:
        add(6, f'{ind["open_incidents"]} environmental incident(s) still open', 'medium', 'Close out open incidents')
    else:
        low.append('No open environmental incidents')
    if ind['overdue_reports']:
        add(min(20, 8 * ind['overdue_reports']), f'{ind["overdue_reports"]} regulatory report(s) overdue', 'high',
            'Submit overdue regulatory reports and set reminders')
    elif ind['reports']:
        low.append('Regulatory reporting up to date')
    if ind['goals_behind']:
        add(5, f'{ind["goals_behind"]} sustainability goal(s) behind schedule: {", ".join(ind["behind_list"])}', 'medium',
            'Re-plan or resource the goals that are behind')
    if ind['sensors_total'] and ind['sensors_active'] < ind['sensors_total']:
        add(4, f'{ind["sensors_total"] - ind["sensors_active"]} of {ind["sensors_total"]} sensors inactive', 'medium',
            'Restore inactive sensors so monitoring has no gaps')
    if include_external:
        low.append('External factors (weather, neighbours) are not part of this assessment — review them manually')
    score = round(min(100, score / strict))
    level = 'CRITICAL' if score >= 75 else 'HIGH' if score >= 50 else 'MEDIUM' if score >= 25 else 'LOW'
    data_points = ind['air_readings'] + ind['water_samples'] + ind['incidents'] + ind['reports']
    inc = sorted(ctx.get('incidents') or [], key=lambda i: str(i.get('date') or ''))
    half = len(inc) // 2
    trend = 'STABLE'
    if len(inc) >= 4:
        trend = 'INCREASING' if len(inc) - half > half * 1.3 else 'DECREASING' if len(inc) - half < half * 0.7 else 'STABLE'
    return {'overall_risk': level, 'risk_score': score, 'high_risk_factors': high, 'medium_risk_factors': medium,
            'low_risk_factors': low, 'mitigation_strategies': mitig or ['Keep current controls and monitoring in place'],
            'predicted_risk_trend': trend, 'confidence_level': round(min(0.95, 0.45 + data_points / 300), 2),
            'data_points': data_points, 'method': 'Weighted indicators from your monitoring, incidents and reporting records'}


# ------------------------------------------------------------------ advanced analysis
def advanced_analysis(ctx, analysis_type='comprehensive'):
    ind = indicators(ctx)
    fc = predict_air_quality(ctx, 30)
    breach_day, violations = None, 0
    for p in fc.get('predictions') or []:
        if (p.get('pm2_5') or 0) > WHO['pm2_5'] or (p.get('aqi') or 0) > 100:
            violations += 1
            breach_day = breach_day or p['timestamp'][:10]
    parts = [v for v in (ind['air_compliance'], ind['water_compliance']) if v is not None]
    prob = round(_mean(parts) / 100, 2) if parts else None
    if prob is not None and ind['overdue_reports']:
        prob = round(max(0.0, prob - 0.1 * ind['overdue_reports']), 2)
    risks = []
    if ind['air_compliance'] is not None and ind['air_compliance'] < 90:
        risks.append(f"Air quality: {ind['air_compliance']:.0f}% of readings within guideline")
    if ind['water_compliance'] is not None and ind['water_compliance'] < 100:
        risks.append(f"Water: {100 - ind['water_compliance']:.0f}% of samples non-compliant")
    if ind['overdue_reports']:
        risks.append(f"{ind['overdue_reports']} overdue regulatory report(s)")
    goals = ctx.get('goals') or []

    def goal_progress(*words):
        vals = [g.get('progress') for g in goals if any(w in (str(g.get('category') or '') + ' ' + str(g.get('goal') or '')).lower() for w in words)]
        return round(_mean(vals)) if _mean(vals) is not None else None
    recs = []
    if ind['air_compliance'] is not None and ind['air_compliance'] < 90:
        recs.append('Add dust suppression / extraction on the sources behind particulate exceedances')
    if ind['water_compliance'] is not None and ind['water_compliance'] < 100:
        recs.append('Investigate failing water sampling sites and adjust treatment')
    if ind['goals_behind']:
        recs.append(f"Re-plan goals behind schedule: {', '.join(ind['behind_list'])}")
    if not goals:
        recs.append('Set measurable sustainability goals (energy, water, waste, emissions) to track improvement')
    if not recs:
        recs.append('Performance is on track — keep monitoring and review targets annually')
    rating = None
    if parts:
        avg = _mean(parts)
        rating = 'LOW' if avg >= 90 else 'MODERATE' if avg >= 70 else 'HIGH'
    return {
        'impact_assessment': {'carbon_footprint_kg_co2': None, 'water_impact_score': ind['water_compliance'],
                              'waste_management_score': goal_progress('waste', 'recycl'),
                              'energy_efficiency_score': goal_progress('energy', 'electric', 'fuel'),
                              'air_quality_score': ind['air_compliance'], 'overall_impact_rating': rating or 'NOT ENOUGH DATA',
                              'improvement_recommendations': recs},
        'compliance_prediction': {'compliance_probability': prob, 'identified_risks': risks, 'predicted_violations': violations,
                                  'time_to_compliance_breach': breach_day or ('No breach forecast in the next 30 days' if fc.get('predictions') else 'Not enough data'),
                                  'mitigation_actions': recs},
        'sustainability_metrics': {'renewable_energy_usage': goal_progress('renew', 'solar'),
                                   'water_recycling_rate': goal_progress('water'),
                                   'waste_diverted_from_landfill': goal_progress('waste', 'recycl'),
                                   'carbon_intensity': None, 'goals_tracked': len(goals)},
        'current': {'avg_aqi': round(_mean([d.get('aqi') for d in ctx.get('daily_air') or []])) if _mean([d.get('aqi') for d in ctx.get('daily_air') or []]) is not None else None,
                    'avg_pm2_5': round(_mean([d.get('pm2_5') for d in ctx.get('daily_air') or []]), 1) if _mean([d.get('pm2_5') for d in ctx.get('daily_air') or []]) is not None else None,
                    'air_readings': ind['air_readings'], 'water_samples': ind['water_samples']},
        'notes': 'Scores are percentages from your own records; empty values mean the data is not tracked yet. '
                 'Carbon footprint needs energy/fuel consumption data.',
    }


# ------------------------------------------------------------------ ESG
def _rating(score):
    if score is None:
        return 'NOT RATED'
    for lim, r in ((90, 'AAA'), (80, 'AA'), (70, 'A'), (60, 'BBB'), (50, 'BB'), (40, 'B')):
        if score >= lim:
            return r
    return 'CCC'


def esg_score(ctx, standards=None, benchmark=None):
    ind = indicators(ctx)
    env_parts = {'air_quality_management': ind['air_compliance'], 'water_management': ind['water_compliance'],
                 'environmental_incident_control': (max(0, 100 - ind['open_incidents'] * 10 - ind['severe_open'] * 15) if ind['incidents'] or ind['air_readings'] else None),
                 'sustainability_goals': round(ind['goal_progress']) if ind['goal_progress'] is not None else None}
    soc_parts = {'health_and_safety': (max(0, 100 - ind['safety_open'] * 8 - ind['safety_incidents'] * 2) if ctx.get('safety_incidents') is not None else None)}
    gov_parts = {'regulatory_reporting': (max(0, 100 - ind['overdue_reports'] * 20) if ind['reports'] else None),
                 'incident_close_out': (_pct(ind['incidents'] - ind['open_incidents'], ind['incidents']) if ind['incidents'] else None)}
    e, s_, g = (_mean(list(p.values())) for p in (env_parts, soc_parts, gov_parts))
    pillars = [(e, 0.5), (s_, 0.25), (g, 0.25)]
    avail = [(v, w) for v, w in pillars if v is not None]
    overall = round(sum(v * w for v, w in avail) / sum(w for _, w in avail), 1) if avail else None
    breakdown = {k: (round(v) if v is not None else None) for k, v in {**env_parts, **soc_parts, **gov_parts}.items()}
    weak = sorted([(v, k) for k, v in breakdown.items() if v is not None and v < 75])
    improve = [k.replace('_', ' ').capitalize() + f' ({v}%)' for v, k in weak]
    improve += [k.replace('_', ' ').capitalize() + ' — no data recorded' for k, v in breakdown.items() if v is None]
    return {'overall_esg_score': overall, 'environmental_score': round(e, 1) if e is not None else None,
            'social_score': round(s_, 1) if s_ is not None else None, 'governance_score': round(g, 1) if g is not None else None,
            'esg_rating': _rating(overall), 'improvement_areas': improve[:8],
            'benchmark_comparison': 'No external benchmark — scores are calculated from your own SafeTrack records'
                                    + (f' (requested: {benchmark})' if benchmark else ''),
            'reporting_standards': standards if isinstance(standards, list) and standards else ['GRI'],
            'performance_breakdown': {k: v for k, v in breakdown.items() if v is not None},
            'method': 'Environmental 50%, Social 25%, Governance 25%, from monitoring, incident and reporting records'}


# ------------------------------------------------------------------ pollution map / sustainability report
def pollution_map(sensor_points):
    pts = [p for p in sensor_points if p.get('lat') is not None and p.get('lng') is not None]
    if not pts:
        return _not_enough('No sensors with coordinates — add latitude/longitude to your sensors.', hotspots=[], points=[])
    out = []
    for p in pts:
        v = p.get('pm2_5')
        out.append({**p, 'level': 'unknown' if v is None else 'good' if v <= WHO['pm2_5'] else 'moderate' if v <= 35 else 'poor'})
    hot = sorted([p for p in out if p['level'] == 'poor'], key=lambda p: -(p.get('pm2_5') or 0))
    return {'points': out, 'hotspots': hot[:10], 'sensors_used': len(out), 'method': 'Latest average per sensor vs WHO guideline'}


def sustainability_summary(ctx):
    ind = indicators(ctx)
    return {'indicators': {k: v for k, v in ind.items() if k != 'behind_list'}, 'goals_behind': ind['behind_list'],
            'risk': assess_risk(ctx), 'esg': esg_score(ctx)}
