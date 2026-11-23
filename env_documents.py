"""
Environmental document generators (2026-11-22).

Builds real reports from what the user entered plus the company's own monitoring data:
  - iso14001  : ISO 14001 environmental performance & compliance report
  - safety    : workplace safety inspection report (OSHA / ISO 45001 / local regulation)
  - eia       : environmental impact assessment

Nothing is invented: values the user did not provide are shown as "Not provided", statuses are
calculated from the numbers (value vs target, impact significance matrix), and conclusions follow
from the findings.  One structured report renders to HTML (-> PDF), Word (.docx) and Excel (.xlsx).
Pure Python: no Flask / database imports, so it can be tested on its own.
"""
from datetime import datetime
import html as _html
import re

NP = 'Not provided'

ISO_CLAUSES = [
    ('4', 'Context of the organization (issues, interested parties, EMS scope)'),
    ('5', 'Leadership (environmental policy, roles and responsibilities)'),
    ('6', 'Planning (aspects & impacts, compliance obligations, objectives)'),
    ('7', 'Support (resources, competence, awareness, communication, documented information)'),
    ('8', 'Operation (operational control, emergency preparedness and response)'),
    ('9', 'Performance evaluation (monitoring, compliance evaluation, internal audit, management review)'),
    ('10', 'Improvement (nonconformity, corrective action, continual improvement)'),
]
CLAUSE_STATUS = {'implemented': 'Implemented', 'partial': 'Partially implemented',
                 'not_implemented': 'Not implemented', 'not_assessed': 'Not assessed'}

PERFORMANCE_PARAMS = [
    ('carbon_emissions', 'Carbon emissions', 'tCO2e'),
    ('energy_consumption', 'Energy consumption', 'kWh'),
    ('water_usage', 'Water usage', 'm³'),
    ('waste_generated', 'Waste generated', 'kg'),
    ('waste_recycled', 'Waste recycled / diverted', '%'),
]

SAFETY_AREAS = [
    'Personal protective equipment (PPE)', 'Emergency exits, routes and signage', 'Fire protection & extinguishers',
    'Chemical storage, labelling and SDS', 'Machine guarding & lockout/tagout', 'Electrical safety',
    'Working at height (ladders, scaffolds, edges)', 'Housekeeping, walkways and slips/trips',
    'First aid & welfare facilities', 'Training records and toolbox talks',
]
SAFETY_STATUS = {'compliant': 'Compliant', 'minor': 'Minor issue', 'major': 'Major issue',
                 'critical': 'Critical — stop work', 'na': 'Not applicable', 'not_inspected': 'Not inspected'}

EIA_AREAS = ['Air quality', 'Noise & vibration', 'Surface & ground water', 'Soil & land',
             'Biodiversity & habitats', 'Waste generation', 'Traffic & transport', 'Community & socio-economic',
             'Cultural heritage', 'Climate (greenhouse gases)']
MAGNITUDE = {'negligible': 0, 'low': 1, 'medium': 2, 'high': 3}
DURATION = {'short': 0, 'medium': 1, 'long': 2, 'permanent': 3}
EXTENT = {'site': 0, 'local': 1, 'regional': 2, 'national': 3}
LIKELIHOOD = {'unlikely': 0, 'possible': 1, 'likely': 2, 'certain': 3}


# ---------------------------------------------------------------- helpers
def _s(v, limit=2000):
    if v is None:
        return ''
    return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', str(v)).strip()[:limit]


def _num(v):
    if v is None or v == '':
        return None
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    if f != f or f in (float('inf'), float('-inf')):
        return None
    return f


def _fmt(v, unit=''):
    if v is None:
        return NP
    txt = f'{v:,.0f}' if abs(v) >= 100 or float(v).is_integer() else f'{v:,.2f}'
    return f'{txt} {unit}'.strip()


def _date(v):
    if not v:
        return None
    if isinstance(v, datetime):
        return v
    try:
        return datetime.fromisoformat(str(v).replace('Z', '+00:00')).replace(tzinfo=None)
    except ValueError:
        return None


def _dstr(v):
    d = _date(v)
    return d.strftime('%d %b %Y') if d else NP


def _pick(value, allowed, default):
    v = _s(value, 40).lower().replace(' ', '_').replace('-', '_')
    return v if v in allowed else default


def performance_status(value, target, lower_is_better=True):
    """Status of a performance figure against its target."""
    if value is None:
        return 'No data'
    if target is None:
        return 'No target set'
    if lower_is_better:
        if value <= target:
            return 'Within target'
        over = (value - target) / target * 100 if target else 100
        return f'Above target by {over:.0f}%'
    if value >= target:
        return 'Target met'
    short = (target - value) / target * 100 if target else 100
    return f'Below target by {short:.0f}%'


def eia_significance(magnitude, duration, extent, likelihood='likely'):
    """Classic significance matrix: (magnitude + duration + extent) scaled by likelihood."""
    m = MAGNITUDE.get(magnitude, 1)
    if m == 0:
        return 'Negligible', 0
    score = (m * 2 + DURATION.get(duration, 1) + EXTENT.get(extent, 0)) * (1 + LIKELIHOOD.get(likelihood, 2)) / 3
    if score >= 9:
        return 'Major', round(score, 1)
    if score >= 5:
        return 'Moderate', round(score, 1)
    return 'Minor', round(score, 1)


# ---------------------------------------------------------------- live data sections
def _live_sections(live):
    """Sections built from the company's monitoring data (air, water, incidents, goals)."""
    if not live:
        return []
    out = []
    air = live.get('air') or {}
    rows = [
        ['Active air-quality sensors', str(air.get('sensors', 0))],
        ['Readings in the period', str(air.get('readings', 0))],
        ['Average PM2.5', _fmt(air.get('avg_pm25'), 'µg/m³')],
        ['Average PM10', _fmt(air.get('avg_pm10'), 'µg/m³')],
        ['Highest AQI recorded', _fmt(air.get('max_aqi'))],
        ['Readings within WHO 2021 guideline (PM2.5 ≤ 15, PM10 ≤ 45 µg/m³)',
         f"{air['compliance_pct']:.0f}%" if air.get('compliance_pct') is not None else 'No readings'],
    ]
    out.append({'heading': 'Air quality monitoring', 'table': {'headers': ['Indicator', 'Result'], 'rows': rows}})

    water = live.get('water') or {}
    wrows = [['Samples analysed', str(water.get('samples', 0))],
             ['Compliant samples', f"{water['compliance_pct']:.0f}%" if water.get('compliance_pct') is not None else 'No samples']]
    sec = {'heading': 'Water quality monitoring', 'table': {'headers': ['Indicator', 'Result'], 'rows': wrows}}
    bad = water.get('non_compliant') or []
    if bad:
        sec['table2'] = {'headers': ['Date', 'Site', 'pH', 'Turbidity', 'Issue'],
                         'rows': [[_dstr(b.get('date')), _s(b.get('site'), 80) or NP, _fmt(_num(b.get('ph'))),
                                   _fmt(_num(b.get('turbidity')), 'NTU'), _s(b.get('violations'), 200) or 'Outside limits']
                                  for b in bad[:25]]}
    out.append(sec)

    inc = live.get('incidents') or {}
    irows = [[k.title(), str(v)] for k, v in sorted((inc.get('by_severity') or {}).items())]
    irows.append(['Still open at end of period', str(inc.get('open', 0))])
    sec = {'heading': 'Environmental incidents', 'paragraphs': [f"{inc.get('total', 0)} environmental incident(s) were reported in the period."],
           'table': {'headers': ['Severity', 'Count'], 'rows': irows}}
    if inc.get('open_list'):
        sec['table2'] = {'headers': ['Date', 'Title', 'Severity', 'Status', 'Location'],
                         'rows': [[_dstr(i.get('date')), _s(i.get('title'), 120), _s(i.get('severity'), 20),
                                   _s(i.get('status'), 20), _s(i.get('location'), 80)] for i in inc['open_list'][:25]]}
    out.append(sec)

    goals = live.get('goals') or []
    if goals:
        out.append({'heading': 'Sustainability objectives and targets', 'table': {
            'headers': ['Objective', 'Category', 'Current', 'Target', 'Progress', 'Deadline', 'Status'],
            'rows': [[_s(g.get('goal'), 120), _s(g.get('category'), 40) or '—', _s(g.get('current'), 40) or '—',
                      _s(g.get('target'), 40) or '—', f"{_num(g.get('progress')) or 0:.0f}%", _dstr(g.get('deadline')),
                      _s(g.get('status'), 30) or '—'] for g in goals[:40]]}})
    return out


# ---------------------------------------------------------------- builders
def _meta_common(inputs, live):
    company = _s(inputs.get('company_name'), 200) or _s((live or {}).get('company_name'), 200) or NP
    return company


def build_iso14001(inputs, live=None):
    company = _meta_common(inputs, live)
    period = _s(inputs.get('report_period'), 80) or _s((live or {}).get('period_label'), 80) or NP
    perf_in = inputs.get('environmental_performance') or {}
    targets = inputs.get('targets') or {}
    rows, problems, missing = [], [], 0
    for key, label, unit in PERFORMANCE_PARAMS:
        v = _num(perf_in.get(key))
        t = _num(targets.get(key))
        status = performance_status(v, t, lower_is_better=(key != 'waste_recycled'))
        if v is None:
            missing += 1
        if status.startswith(('Above', 'Below')):
            problems.append(f'{label}: {status.lower()}')
        rows.append([label, _fmt(v, unit), _fmt(t, unit) if t is not None else 'Not set', status])

    clauses_in = inputs.get('clauses') or {}
    crows, gaps = [], []
    for num, title in ISO_CLAUSES:
        c = clauses_in.get(num) or {}
        st = _pick(c.get('status'), CLAUSE_STATUS, 'not_assessed')
        if st in ('partial', 'not_implemented'):
            gaps.append(f'Clause {num}')
        crows.append([f'{num}. {title}', CLAUSE_STATUS[st], _s(c.get('evidence'), 300) or '—'])

    live_secs = _live_sections(live)
    air = (live or {}).get('air') or {}
    water = (live or {}).get('water') or {}
    inc = (live or {}).get('incidents') or {}
    if air.get('compliance_pct') is not None and air['compliance_pct'] < 90:
        problems.append(f"only {air['compliance_pct']:.0f}% of air readings met the WHO guideline")
    if water.get('compliance_pct') is not None and water['compliance_pct'] < 100:
        problems.append(f"{100 - water['compliance_pct']:.0f}% of water samples were non-compliant")
    if inc.get('open'):
        problems.append(f"{inc['open']} environmental incident(s) still open")

    if problems or gaps:
        conclusion = 'ACTION REQUIRED'
        summary = 'The review found the following issues: ' + '; '.join(problems + [f'gaps in {", ".join(gaps)}'] if gaps else problems) + '.'
    elif missing == len(PERFORMANCE_PARAMS) and not air.get('readings') and not water.get('samples'):
        conclusion = 'INSUFFICIENT DATA'
        summary = 'No performance figures or monitoring data were available for this period, so compliance could not be evaluated.'
    else:
        conclusion = 'MEETING OBJECTIVES'
        summary = 'All figures provided are within their targets and no open issues were found in the monitoring data.'

    sections = [
        {'heading': '1. Executive summary', 'paragraphs': [summary] + ([_s(inputs.get('summary_notes'), 3000)] if inputs.get('summary_notes') else [])},
        {'heading': '2. Environmental performance', 'table': {'headers': ['Parameter', 'Value', 'Target', 'Status'], 'rows': rows, 'status_col': 3},
         'paragraphs': ['Status compares each reported value with the target set for the period. "No data" means no value was entered.']},
        {'heading': '3. ISO 14001:2015 clause review', 'table': {'headers': ['Clause', 'Status', 'Evidence'], 'rows': crows, 'status_col': 1}},
    ]
    for i, sec in enumerate(live_secs, start=4):
        sec = dict(sec); sec['heading'] = f'{i}. {sec["heading"]}'
        sections.append(sec)
    actions = [a for a in (inputs.get('actions') or []) if isinstance(a, dict) and _s(a.get('action'))]
    if actions:
        sections.append({'heading': f'{len(sections) + 1}. Corrective actions', 'table': {
            'headers': ['Action', 'Owner', 'Due date'],
            'rows': [[_s(a.get('action'), 300), _s(a.get('owner'), 80) or '—', _dstr(a.get('due_date'))] for a in actions[:40]]}})
    return {
        'kind': 'iso14001', 'title': 'Environmental Performance & ISO 14001 Compliance Report',
        'company': company, 'conclusion': conclusion, 'accent': '#237804',
        'meta': [('Organisation', company), ('Reporting period', period), ('Site / scope', _s(inputs.get('site'), 200) or 'All sites'),
                 ('Prepared by', _s(inputs.get('prepared_by'), 120) or NP), ('Overall conclusion', conclusion)],
        'sections': sections,
        'signoff': ['Prepared by', 'Reviewed by (EHS Manager)', 'Approved by (Management representative)'],
    }


def build_safety(inputs, live=None):
    company = _meta_common(inputs, live)
    items_in = inputs.get('items') or []
    if not items_in:
        items_in = [{'area': a, 'status': 'not_inspected'} for a in SAFETY_AREAS]
    rows, counts = [], {}
    for it in items_in[:60]:
        if not isinstance(it, dict) or not _s(it.get('area')):
            continue
        st = _pick(it.get('status'), SAFETY_STATUS, 'not_inspected')
        counts[st] = counts.get(st, 0) + 1
        rows.append([_s(it.get('area'), 120), SAFETY_STATUS[st], _s(it.get('finding'), 400) or '—',
                     _s(it.get('action'), 300) or ('—' if st in ('compliant', 'na', 'not_inspected') else 'Action to be defined'),
                     _s(it.get('responsible'), 80) or '—', _dstr(it.get('due_date')) if it.get('due_date') else '—'])
    inspected = sum(v for k, v in counts.items() if k not in ('na', 'not_inspected'))
    ok = counts.get('compliant', 0)
    score = round(ok / inspected * 100) if inspected else None
    if counts.get('critical'):
        conclusion = 'CRITICAL — IMMEDIATE ACTION'
    elif counts.get('major'):
        conclusion = 'MAJOR ISSUES FOUND'
    elif counts.get('minor'):
        conclusion = 'MINOR ISSUES FOUND'
    elif inspected:
        conclusion = 'SATISFACTORY'
    else:
        conclusion = 'NOT INSPECTED'

    m = inputs.get('safety_metrics') or {}
    mrows = [['Recordable incidents in the period', _fmt(_num(m.get('incidents')))],
             ['Near misses reported', _fmt(_num(m.get('near_misses')))],
             ['Workers with up-to-date safety training', _fmt(_num(m.get('safety_training')), '%')],
             ['PPE compliance observed', _fmt(_num(m.get('ppe_compliance')), '%')],
             ['Hours worked', _fmt(_num(m.get('hours_worked')))]]
    inc_n, hours = _num(m.get('incidents')), _num(m.get('hours_worked'))
    if inc_n is not None and hours:
        mrows.append(['Incident rate (per 200,000 hours, OSHA TRIR)', f'{inc_n * 200000 / hours:.2f}'])
    li = (live or {}).get('safety_incidents')
    if li:
        mrows.append(['Incidents recorded in SafeTrack for the period', str(li.get('total', 0))])
        mrows.append(['…of which still open', str(li.get('open', 0))])

    summary = (f'{inspected} area(s) inspected, {ok} compliant'
               + (f' (score {score}%)' if score is not None else '')
               + ''.join(f', {counts[k]} {SAFETY_STATUS[k].lower()}' for k in ('minor', 'major', 'critical') if counts.get(k)) + '.')
    return {
        'kind': 'safety', 'title': 'Workplace Safety Inspection Report', 'company': company, 'conclusion': conclusion,
        'accent': '#a8071a',
        'meta': [('Organisation', company), ('Facility / site', _s(inputs.get('facility'), 200) or NP),
                 ('Inspection date', _dstr(inputs.get('inspection_date'))), ('Inspector', _s(inputs.get('inspector'), 120) or NP),
                 ('Standard / regulation', _s(inputs.get('standard'), 160) or 'OSHA 29 CFR 1910 / ISO 45001'),
                 ('Result', conclusion)],
        'sections': [
            {'heading': '1. Summary', 'paragraphs': [summary] + ([_s(inputs.get('notes'), 3000)] if inputs.get('notes') else [])},
            {'heading': '2. Inspection findings', 'table': {'headers': ['Area', 'Status', 'Finding', 'Corrective action', 'Responsible', 'Due'],
                                                            'rows': rows, 'status_col': 1}},
            {'heading': '3. Safety performance indicators', 'table': {'headers': ['Indicator', 'Value'], 'rows': mrows}},
        ],
        'signoff': ['Inspector', 'Area supervisor', 'HSE Manager'],
    }


def build_eia(inputs, live=None):
    company = _meta_common(inputs, live)
    impacts_in = inputs.get('impacts')
    if not impacts_in:
        legacy = inputs.get('impact_areas') or {}
        key_map = {'air_quality': 'Air quality', 'water_resources': 'Surface & ground water',
                   'biodiversity': 'Biodiversity & habitats', 'noise_pollution': 'Noise & vibration'}
        impacts_in = [{'area': key_map[k], 'magnitude': str(v).lower()} for k, v in legacy.items() if k in key_map]
    rows, majors, mitigation_rows = [], [], []
    for it in (impacts_in or [])[:40]:
        if not isinstance(it, dict) or not _s(it.get('area')):
            continue
        mag = _pick(it.get('magnitude'), MAGNITUDE, 'low')
        dur = _pick(it.get('duration'), DURATION, 'medium')
        ext = _pick(it.get('extent'), EXTENT, 'local')
        lik = _pick(it.get('likelihood'), LIKELIHOOD, 'likely')
        sig, score = eia_significance(mag, dur, ext, lik)
        if sig == 'Major':
            majors.append(_s(it.get('area'), 80))
        nature = 'Positive' if str(it.get('nature', '')).lower() == 'positive' else 'Negative'
        rows.append([_s(it.get('area'), 80), nature, mag.title(), dur.title(), ext.title(), lik.title(), f'{sig} ({score})'])
        mitigation_rows.append([_s(it.get('area'), 80), _s(it.get('mitigation'), 500) or 'To be defined',
                                sig if not it.get('mitigation') else _residual(sig),
                                _s(it.get('monitoring'), 300) or '—'])
    if not rows:
        conclusion = 'IMPACTS NOT ASSESSED'
    elif majors:
        conclusion = 'SIGNIFICANT IMPACTS — MITIGATION REQUIRED'
    elif any(r[6].startswith('Moderate') for r in rows):
        conclusion = 'MODERATE IMPACTS — MANAGEABLE WITH MITIGATION'
    else:
        conclusion = 'MINOR IMPACTS'

    lat, lng = _num(inputs.get('latitude')), _num(inputs.get('longitude'))
    meta = [('Project', _s(inputs.get('project_name'), 200) or NP), ('Proponent', company),
            ('Location', _s(inputs.get('location'), 300) or NP)]
    if lat is not None and lng is not None:
        meta.append(('Coordinates', f'{lat:.5f}, {lng:.5f}'))
    meta += [('Assessment date', _dstr(inputs.get('assessment_date'))), ('Assessor', _s(inputs.get('assessor'), 120) or NP),
             ('Framework', _s(inputs.get('framework'), 160) or 'ISO 14001 / IFC Performance Standards / national EIA regulations'),
             ('Overall finding', conclusion)]
    baseline = [s for s in _live_sections(live) if s['heading'] in ('Air quality monitoring', 'Water quality monitoring')]
    sections = [
        {'heading': '1. Project description', 'paragraphs': [_s(inputs.get('description'), 5000) or 'Project description not provided.']},
        {'heading': '2. Impact assessment', 'table': {'headers': ['Receptor / aspect', 'Nature', 'Magnitude', 'Duration', 'Extent', 'Likelihood', 'Significance'],
                                                      'rows': rows or [['No impacts assessed', '', '', '', '', '', '']], 'status_col': 6},
         'paragraphs': ['Significance = (2 × magnitude + duration + extent) weighted by likelihood. '
                        'Minor < 5 ≤ Moderate < 9 ≤ Major.']},
        {'heading': '3. Mitigation and monitoring plan', 'table': {'headers': ['Receptor / aspect', 'Mitigation measure', 'Residual significance', 'Monitoring'],
                                                                   'rows': mitigation_rows or [['—', '—', '—', '—']]}},
    ]
    for i, sec in enumerate(baseline, start=4):
        sec = dict(sec); sec['heading'] = f'{i}. Baseline — {sec["heading"].lower()}'
        sections.append(sec)
    if majors:
        sections.append({'heading': f'{len(sections) + 1}. Conclusion', 'paragraphs': [
            f'Major impacts were identified for: {", ".join(majors)}. These require mitigation and regulator approval before the project proceeds.']})
    return {
        'kind': 'eia', 'title': 'Environmental Impact Assessment', 'company': company, 'conclusion': conclusion,
        'accent': '#08979c', 'meta': meta, 'sections': sections,
        'signoff': ['Lead assessor', 'Project proponent', 'Environmental authority (review)'],
    }


def _residual(sig):
    return {'Major': 'Moderate', 'Moderate': 'Minor', 'Minor': 'Minor', 'Negligible': 'Negligible'}.get(sig, sig)


BUILDERS = {'iso14001': build_iso14001, 'safety': build_safety, 'eia': build_eia}
FILE_STEM = {'iso14001': 'ISO14001_Environmental_Report', 'safety': 'Safety_Inspection_Report', 'eia': 'Environmental_Impact_Assessment'}


def build_report(kind, inputs, live=None):
    if kind not in BUILDERS:
        raise ValueError('unknown report type')
    rep = BUILDERS[kind](inputs if isinstance(inputs, dict) else {}, live)
    rep['generated_at'] = datetime.utcnow().strftime('%d %b %Y %H:%M UTC')
    return rep


# ---------------------------------------------------------------- renderers
STATUS_COLORS = [
    (('Within target', 'Target met', 'Implemented', 'Compliant', 'Minor (', 'Negligible', 'MEETING', 'SATISFACTORY', 'MINOR IMPACTS'), '#237804'),
    (('Above', 'Below', 'Partially', 'Minor issue', 'Moderate', 'ACTION', 'MINOR ISSUES'), '#ad6800'),
    (('Not implemented', 'Major', 'Critical', 'CRITICAL', 'SIGNIFICANT', 'MAJOR'), '#a8071a'),
]


def _status_color(text):
    for keys, color in STATUS_COLORS:
        if any(str(text).startswith(k) for k in keys):
            return color
    return '#595959'


def render_html(rep):
    e = lambda v: _html.escape(str(v if v is not None else ''))  # noqa: E731
    a = rep.get('accent', '#237804')
    parts = [f"""<style>
      * {{ font-family: sans-serif; }} body {{ font-size: 9.5pt; color: #222; }}
      .top {{ border-bottom: 3px solid {a}; margin-bottom: 8px; }} .co {{ color: #555; font-weight: bold; }}
      h1 {{ color: {a}; font-size: 17pt; margin: 2px 0 4px 0; }}
      h2 {{ color: {a}; font-size: 11.5pt; border-bottom: 1.5px solid {a}; margin: 14px 0 4px 0; }}
      table {{ border-collapse: collapse; width: 100%; margin: 4px 0; }}
      td, th {{ border: 1px solid #c9d1dc; padding: 3px 4px; vertical-align: top; }}
      th {{ color: {a}; text-align: left; }} td.k {{ font-weight: bold; width: 30%; }}
      .small {{ color: #666; font-size: 8pt; }} .sig td {{ height: 34px; }}
    </style>
    <div class="top"><div class="co">{e(rep.get('company'))}</div><h1>{e(rep['title'])}</h1>
    <div class="small">Generated {e(rep.get('generated_at'))} with SafeTrack Pro Global</div></div>"""]
    parts.append('<table>' + ''.join(
        f'<tr><td class="k">{e(k)}</td><td' + (f' style="color:{_status_color(v)};font-weight:bold"' if k in ('Overall conclusion', 'Result', 'Overall finding') else '')
        + f'>{e(v)}</td></tr>' for k, v in rep['meta']) + '</table>')

    def table(t):
        sc = t.get('status_col')
        out = '<table><tr>' + ''.join(f'<th>{e(h)}</th>' for h in t['headers']) + '</tr>'
        for r in t['rows']:
            out += '<tr>' + ''.join(
                (f'<td style="color:{_status_color(c)};font-weight:bold">{e(c)}</td>' if i == sc else f'<td>{e(c)}</td>')
                for i, c in enumerate(r)) + '</tr>'
        return out + '</table>'

    for sec in rep['sections']:
        parts.append(f'<h2>{e(sec["heading"])}</h2>')
        for p in sec.get('paragraphs') or []:
            if p:
                parts.append(f'<p>{e(p).replace(chr(10), "<br/>")}</p>')
        if sec.get('table'):
            parts.append(table(sec['table']))
        if sec.get('table2'):
            parts.append(table(sec['table2']))
    parts.append('<h2>Sign-off</h2><table class="sig"><tr><th>Role</th><th>Name</th><th>Signature</th><th>Date</th></tr>'
                 + ''.join(f'<tr><td>{e(r)}</td><td></td><td></td><td></td></tr>' for r in rep.get('signoff') or []) + '</table>')
    parts.append('<p class="small">Values marked "Not provided" were not entered when the report was generated. '
                 'Monitoring figures come from the organisation\'s SafeTrack records for the reporting period.</p>')
    return '\n'.join(parts)


def render_docx(rep, path):
    from docx import Document as _Docx
    from docx.shared import Pt, RGBColor

    def rgb(hexcol):
        h = hexcol.lstrip('#')
        return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

    doc = _Docx()
    doc.styles['Normal'].font.size = Pt(10)
    p = doc.add_paragraph(); r = p.add_run(rep.get('company') or ''); r.bold = True
    h = doc.add_heading(rep['title'], 0)
    for run in h.runs:
        run.font.color.rgb = rgb(rep.get('accent', '#237804'))
    doc.add_paragraph(f"Generated {rep.get('generated_at')} with SafeTrack Pro Global").runs[0].font.size = Pt(8)

    t = doc.add_table(rows=0, cols=2); t.style = 'Table Grid'
    for k, v in rep['meta']:
        cells = t.add_row().cells
        cells[0].text = k; cells[0].paragraphs[0].runs[0].bold = True
        cells[1].text = str(v)
        if k in ('Overall conclusion', 'Result', 'Overall finding'):
            cells[1].paragraphs[0].runs[0].bold = True
            cells[1].paragraphs[0].runs[0].font.color.rgb = rgb(_status_color(v))

    def add_table(tb):
        tt = doc.add_table(rows=1, cols=len(tb['headers'])); tt.style = 'Table Grid'
        for i, hd in enumerate(tb['headers']):
            tt.rows[0].cells[i].text = hd
            tt.rows[0].cells[i].paragraphs[0].runs[0].bold = True
        for row in tb['rows']:
            cells = tt.add_row().cells
            for i, c in enumerate(row):
                cells[i].text = str(c)
                if i == tb.get('status_col') and cells[i].paragraphs[0].runs:
                    cells[i].paragraphs[0].runs[0].font.color.rgb = rgb(_status_color(c))
                    cells[i].paragraphs[0].runs[0].bold = True

    for sec in rep['sections']:
        doc.add_heading(sec['heading'], level=1)
        for para in sec.get('paragraphs') or []:
            if para:
                doc.add_paragraph(para)
        if sec.get('table'):
            add_table(sec['table'])
        if sec.get('table2'):
            doc.add_paragraph()
            add_table(sec['table2'])
    doc.add_heading('Sign-off', level=1)
    add_table({'headers': ['Role', 'Name', 'Signature', 'Date'], 'rows': [[r, '', '', ''] for r in rep.get('signoff') or []]})
    doc.save(path)


def render_xlsx(rep, path):
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment

    def safe(v):
        v = '' if v is None else str(v)
        return "'" + v if v[:1] in ('=', '+', '-', '@') else v      # no formula injection

    wb = Workbook()
    ws = wb.active; ws.title = 'Summary'
    ws.append([safe(rep['title'])]); ws['A1'].font = Font(bold=True, size=14)
    ws.append([safe(rep.get('company'))]); ws.append([f"Generated {rep.get('generated_at')}"]); ws.append([])
    for k, v in rep['meta']:
        ws.append([safe(k), safe(v)]); ws.cell(ws.max_row, 1).font = Font(bold=True)
    ws.column_dimensions['A'].width = 34; ws.column_dimensions['B'].width = 60
    head_fill = PatternFill('solid', start_color=rep.get('accent', '#237804').lstrip('#'))
    used = set()
    for sec in rep['sections']:
        tables = [x for x in (sec.get('table'), sec.get('table2')) if x]
        if not tables and not sec.get('paragraphs'):
            continue
        name = re.sub(r'[^A-Za-z0-9 ]', '', re.sub(r'^\d+\.\s*', '', sec['heading']))[:28] or 'Section'
        while name in used:
            name = name[:26] + str(len(used))
        used.add(name)
        s = wb.create_sheet(name)
        s.append([safe(sec['heading'])]); s['A1'].font = Font(bold=True, size=12)
        for para in sec.get('paragraphs') or []:
            if para:
                s.append([safe(para)])
        for tb in tables:
            s.append([])
            s.append([safe(h) for h in tb['headers']])
            for c in s[s.max_row]:
                c.font = Font(bold=True, color='FFFFFF'); c.fill = head_fill
            for row in tb['rows']:
                s.append([safe(c) for c in row])
        for col in s.columns:
            width = max((len(str(c.value or '')) for c in col), default=10)
            s.column_dimensions[col[0].column_letter].width = min(max(12, width + 2), 60)
            for c in col:
                c.alignment = Alignment(wrap_text=True, vertical='top')
    wb.save(path)
