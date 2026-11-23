"""
Standard permit-to-work catalogue and permit document renderer.

The catalogue follows widely used international practice for permit-to-work systems
(UK HSE HSG250, IOGP Report 423 / OGP, ISO 45001 clause 8.1, OSHA 29 CFR 1910/1926, NFPA).
Every type carries its own risk assessment starter, precautions, gas-test limits, required
supporting documents, PPE and signatories. Everything is editable per permit.
"""
import html as _h

RISK_LEVELS = [(1, 4, 'Low', '#52c41a'), (5, 9, 'Medium', '#faad14'), (10, 16, 'High', '#fa541c'), (17, 25, 'Extreme', '#cf1322')]

GAS_LIMITS = {
    'O2': {'label': 'Oxygen (O₂)', 'unit': '%', 'min': 19.5, 'max': 23.5},
    'LEL': {'label': 'Flammable gas', 'unit': '% LEL', 'max': 10},
    'H2S': {'label': 'Hydrogen sulphide (H₂S)', 'unit': 'ppm', 'max': 10},
    'CO': {'label': 'Carbon monoxide (CO)', 'unit': 'ppm', 'max': 25},
}

SIGNATORIES = {
    'applicant': 'Permit applicant / Performing authority',
    'issuer': 'Issuing / Area authority',
    'isolator': 'Isolating authority',
    'gas_tester': 'Authorised gas tester',
    'safety': 'HSE officer',
    'client': 'Client representative',
    'lifting': 'Appointed person (lifting)',
    'rpa': 'Radiation protection supervisor',
}


def _h_(hazard, consequence, likelihood, severity, controls):
    return {'hazard': hazard, 'consequence': consequence, 'likelihood': likelihood, 'severity': severity,
            'controls': controls, 'residual_likelihood': max(1, likelihood - 2), 'residual_severity': severity}


PERMIT_TYPES = [
    {
        'key': 'general', 'name': 'General / Cold Work Permit', 'color': '#1677ff', 'validity_hours': 12,
        'standards': ['UK HSE HSG250', 'IOGP Report 423', 'ISO 45001 8.1.2'],
        'description': 'Maintenance and construction work with no ignition source, energy isolation or other special hazard.',
        'gas_test': False,
        'ppe': ['Safety helmet', 'Safety glasses', 'Safety boots', 'High-visibility clothing', 'Gloves'],
        'precautions': ['Work area inspected and barricaded', 'Toolbox talk held with the work party',
                        'Tools and equipment inspected and fit for use', 'Housekeeping and access routes kept clear',
                        'Emergency arrangements and muster point explained'],
        'required_documents': ['Method statement', 'Job safety analysis (JSA)', 'Competency records of the work party'],
        'signatories': ['applicant', 'issuer'],
        'hazards': [_h_('Slips, trips and falls on the same level', 'Sprains, fractures', 3, 2, 'Good housekeeping, cable management, adequate lighting'),
                    _h_('Manual handling', 'Back and muscle injury', 3, 2, 'Mechanical aids, team lifts, manual handling training'),
                    _h_('Hand tools', 'Cuts and impact injuries', 2, 2, 'Inspected tools, gloves, correct tool for the task')],
    },
    {
        'key': 'hot_work', 'name': 'Hot Work Permit', 'color': '#fa541c', 'validity_hours': 12,
        'standards': ['OSHA 29 CFR 1910.252', 'NFPA 51B', 'UK HSE HSG250'],
        'description': 'Welding, cutting, grinding, brazing or any work that produces flame, sparks or heat able to ignite flammable material.',
        'gas_test': True, 'gas_parameters': ['O2', 'LEL', 'H2S', 'CO'],
        'ppe': ['Welding helmet / face shield', 'Fire-retardant coveralls', 'Leather gloves', 'Safety boots', 'Hearing protection'],
        'precautions': ['Combustibles removed or covered within 11 m (35 ft)', 'Gas test completed and recorded before start',
                        'Fire watch posted during work and for at least 30 minutes after', 'Fire extinguisher and fire blanket at the work point',
                        'Drains, openings and floor gaps covered', 'Fire and gas detection inhibits authorised (if any)',
                        'Hot work equipment (cylinders, hoses, flashback arrestors) inspected'],
        'required_documents': ['Gas test record', 'Fire watch log', 'Welder / operator qualification', 'Isolation certificate (if equipment isolated)'],
        'signatories': ['applicant', 'gas_tester', 'issuer', 'safety'],
        'hazards': [_h_('Fire / explosion from sparks or hot slag', 'Burns, fatalities, asset loss', 3, 5, 'Remove combustibles, gas testing, fire watch, extinguisher at hand'),
                    _h_('Welding fumes', 'Respiratory illness', 3, 3, 'Local exhaust ventilation, respiratory protection'),
                    _h_('Arc eye / UV radiation', 'Eye injury', 3, 2, 'Welding screens, correct shade filter'),
                    _h_('Electric shock from welding set', 'Electrocution', 2, 5, 'Inspected leads, earth clamp, dry conditions')],
    },
    {
        'key': 'confined_space', 'name': 'Confined Space Entry Permit', 'color': '#722ed1', 'validity_hours': 8,
        'standards': ['OSHA 29 CFR 1910.146', 'UK Confined Spaces Regulations 1997', 'IOGP Report 423'],
        'description': 'Entry into tanks, vessels, pits, sewers, silos or any enclosed space with limited access where a dangerous atmosphere may exist.',
        'gas_test': True, 'gas_parameters': ['O2', 'LEL', 'H2S', 'CO'],
        'ppe': ['Full-body harness with retrieval line', 'Personal gas monitor', 'Safety helmet', 'Coveralls', 'Respiratory protection as assessed'],
        'precautions': ['Space isolated (positive isolation / blinds) and drained, purged and ventilated',
                        'Continuous atmospheric monitoring while occupied', 'Attendant (standby person) stationed at the entrance at all times',
                        'Rescue plan and rescue equipment in place and tested', 'Entry log of all entrants maintained',
                        'Communication method between entrants and attendant agreed'],
        'required_documents': ['Gas test record', 'Rescue plan', 'Isolation certificate', 'Entrant and attendant training records'],
        'signatories': ['applicant', 'isolator', 'gas_tester', 'issuer', 'safety'],
        'hazards': [_h_('Oxygen deficiency or enrichment', 'Asphyxiation, fatality', 3, 5, 'Ventilation, continuous O₂ monitoring, breathing apparatus'),
                    _h_('Toxic gas (H₂S, CO)', 'Poisoning, fatality', 3, 5, 'Gas testing, isolation, ventilation, personal monitors'),
                    _h_('Engulfment / ingress of material', 'Fatality', 2, 5, 'Positive isolation, lock-out, drained and cleaned'),
                    _h_('Difficult rescue', 'Delayed treatment', 3, 4, 'Rescue plan, tripod and winch, trained rescue team')],
    },
    {
        'key': 'work_at_height', 'name': 'Working at Height Permit', 'color': '#13c2c2', 'validity_hours': 12,
        'standards': ['OSHA 29 CFR 1926.501-503', 'UK Work at Height Regulations 2005', 'EN 365 / EN 363'],
        'description': 'Work where a person could fall a distance liable to cause injury (typically 1.8 m / 6 ft or more), including roofs, structures and open edges.',
        'gas_test': False,
        'ppe': ['Full-body harness', 'Double lanyard with shock absorber', 'Safety helmet with chin strap', 'Safety boots'],
        'precautions': ['Collective protection (guardrails, nets) used where possible', 'Anchor points certified and identified',
                        'Scaffold / MEWP inspected and tagged', 'Area below barricaded and tools tethered',
                        'Rescue-at-height plan in place', 'Weather and wind speed checked'],
        'required_documents': ['Rescue plan', 'Scaffold inspection tag / MEWP inspection', 'Harness inspection record', 'Work-at-height training records'],
        'signatories': ['applicant', 'issuer', 'safety'],
        'hazards': [_h_('Fall of persons from height', 'Serious injury, fatality', 3, 5, 'Guardrails, harness with 100% tie-off, trained workers'),
                    _h_('Falling objects', 'Injury to people below', 3, 4, 'Toe boards, tool lanyards, exclusion zone'),
                    _h_('Suspension trauma after a fall', 'Serious injury', 2, 4, 'Rescue plan, rescue kit, rescue within 10 minutes')],
    },
    {
        'key': 'electrical', 'name': 'Electrical Work Permit', 'color': '#faad14', 'validity_hours': 8,
        'standards': ['NFPA 70E', 'OSHA 29 CFR 1910.333', 'UK Electricity at Work Regulations 1989'],
        'description': 'Work on or near electrical equipment and installations, including energised work where de-energising is not feasible.',
        'gas_test': False,
        'ppe': ['Arc-rated clothing (category per arc-flash study)', 'Insulated gloves', 'Arc-flash face shield', 'Insulated tools', 'Safety boots (EH rated)'],
        'precautions': ['Equipment de-energised, isolated, locked and tagged where possible', 'Absence of voltage verified with a tested instrument',
                        'Arc-flash and shock boundaries established', 'Energised work justified and authorised in writing',
                        'Competent / qualified electrical person assigned', 'Earthing / grounding applied where required'],
        'required_documents': ['Isolation certificate', 'Arc-flash risk assessment', 'Electrical competency records', 'Single-line diagram (marked up)'],
        'signatories': ['applicant', 'isolator', 'issuer', 'safety'],
        'hazards': [_h_('Electric shock', 'Electrocution', 3, 5, 'Isolation and LOTO, test before touch, insulated tools'),
                    _h_('Arc flash / arc blast', 'Severe burns', 2, 5, 'Arc-rated PPE, approach boundaries, remote racking'),
                    _h_('Unexpected re-energisation', 'Fatality', 2, 5, 'Personal locks, permit control of keys')],
    },
    {
        'key': 'isolation', 'name': 'Isolation & Lockout/Tagout Certificate', 'color': '#2f54eb', 'validity_hours': 24,
        'standards': ['OSHA 29 CFR 1910.147', 'UK HSE HSG253', 'IOGP Report 423'],
        'description': 'Control of hazardous energy (electrical, mechanical, hydraulic, pneumatic, process, thermal) before work on equipment.',
        'gas_test': False,
        'ppe': ['Safety glasses', 'Gloves', 'Safety boots'],
        'precautions': ['All energy sources identified on the isolation list', 'Isolation points locked and tagged with personal locks',
                        'Stored energy released (bleed, vent, drain, block)', 'Zero-energy state verified (try-out)',
                        'Lock box / key safe controlled by the isolating authority'],
        'required_documents': ['Isolation list / marked-up P&ID', 'LOTO register', 'Isolating authority competency'],
        'signatories': ['applicant', 'isolator', 'issuer'],
        'hazards': [_h_('Release of stored energy', 'Crushing, burns, injection injury', 3, 5, 'Bleed-down, blocking, verification of zero energy'),
                    _h_('Isolation removed by mistake', 'Unexpected start-up', 2, 5, 'Personal locks, tags, key control')],
    },
    {
        'key': 'excavation', 'name': 'Excavation & Ground Disturbance Permit', 'color': '#8c6d1f', 'validity_hours': 24,
        'standards': ['OSHA 29 CFR 1926 Subpart P', 'UK HSE HSG47', 'IOGP Report 423'],
        'description': 'Any digging, trenching, piling, drilling or ground breaking, including near buried services.',
        'gas_test': False,
        'ppe': ['Safety helmet', 'High-visibility clothing', 'Safety boots', 'Gloves'],
        'precautions': ['Underground services located (drawings + cable avoidance tool) and marked', 'Hand digging within 0.5 m of services',
                        'Shoring, sloping or benching for depths over 1.2 m (4 ft)', 'Spoil and plant kept back from the edge',
                        'Safe access/egress (ladder every 7.5 m)', 'Edge protection and barriers installed'],
        'required_documents': ['Underground services drawing', 'Cable avoidance survey', 'Temporary works / shoring design', 'Method statement'],
        'signatories': ['applicant', 'issuer', 'safety'],
        'hazards': [_h_('Collapse of excavation sides', 'Burial, fatality', 3, 5, 'Shoring/sloping, inspections, no work beneath unsupported faces'),
                    _h_('Striking buried services', 'Electrocution, gas release', 3, 5, 'Service drawings, CAT scan, hand digging'),
                    _h_('People or vehicles falling in', 'Serious injury', 2, 4, 'Edge protection, stop blocks, lighting')],
    },
    {
        'key': 'lifting', 'name': 'Lifting Operations Permit', 'color': '#d4380d', 'validity_hours': 12,
        'standards': ['UK LOLER 1998', 'ASME B30 series', 'OSHA 29 CFR 1926 Subpart CC'],
        'description': 'Crane and heavy lifting operations, critical lifts, tandem lifts and lifts over live plant or people.',
        'gas_test': False,
        'ppe': ['Safety helmet', 'High-visibility clothing', 'Safety boots', 'Gloves'],
        'precautions': ['Lift plan prepared by an appointed person', 'Crane and lifting accessories certified and inspected',
                        'Ground conditions and outrigger pads checked', 'Exclusion zone established below the load',
                        'Wind speed within the crane limit', 'Banksman / signaller assigned with agreed signals'],
        'required_documents': ['Lift plan', 'Crane certificate', 'Lifting accessories certificates', 'Operator and rigger certificates'],
        'signatories': ['applicant', 'lifting', 'issuer', 'safety'],
        'hazards': [_h_('Dropped load', 'Fatality, asset damage', 2, 5, 'Certified gear, exclusion zone, tag lines'),
                    _h_('Crane overturning', 'Fatality', 2, 5, 'Load charts, ground assessment, outrigger mats'),
                    _h_('Contact with overhead lines', 'Electrocution', 2, 5, 'Safe distances, goal posts, spotter')],
    },
    {
        'key': 'line_breaking', 'name': 'Line Breaking / Opening Process Equipment Permit', 'color': '#531dab', 'validity_hours': 12,
        'standards': ['OSHA 29 CFR 1910.119 (PSM)', 'API RP 2009', 'IOGP Report 423'],
        'description': 'Opening pipes, vessels or equipment that contain or have contained hazardous substances, pressure or temperature.',
        'gas_test': True, 'gas_parameters': ['LEL', 'H2S', 'CO', 'O2'],
        'ppe': ['Chemical-resistant gloves and suit as per SDS', 'Face shield', 'Respiratory protection as assessed', 'Safety boots'],
        'precautions': ['Line isolated, depressurised, drained and purged', 'Contents and SDS reviewed with the crew',
                        'First break made away from the face (bolts loosened opposite side first)', 'Spill containment and drain covers in place',
                        'Emergency shower / eyewash available'],
        'required_documents': ['Isolation certificate', 'Safety data sheet (SDS)', 'Gas test record', 'Marked-up P&ID'],
        'signatories': ['applicant', 'isolator', 'gas_tester', 'issuer'],
        'hazards': [_h_('Release of hazardous substance', 'Burns, poisoning', 3, 5, 'Isolation, depressurisation, PPE, first-break technique'),
                    _h_('Residual pressure', 'Injury from ejected parts', 2, 4, 'Verify zero pressure, bleed points'),
                    _h_('Fire from flammable residues', 'Burns', 2, 5, 'Purging, gas testing, no ignition sources')],
    },
    {
        'key': 'radiography', 'name': 'Radiography / Ionising Radiation Permit', 'color': '#a0d911', 'validity_hours': 12,
        'standards': ['IAEA SSR-3 / GSR Part 3', 'UK Ionising Radiations Regulations 2017', 'OSHA 29 CFR 1910.1096'],
        'description': 'Industrial radiography and any work with sealed radioactive sources or X-ray equipment.',
        'gas_test': False,
        'ppe': ['Personal dosimeter', 'Survey meter', 'Safety helmet', 'High-visibility clothing'],
        'precautions': ['Controlled area defined with barriers, signs and warning lights', 'Area announced and cleared of non-essential people',
                        'Survey meter calibrated and checked', 'Source container and transport documents verified',
                        'Emergency procedure for source retrieval available'],
        'required_documents': ['Radiation licence', 'Source certificate', 'Radiation protection supervisor appointment', 'Dose records of radiographers'],
        'signatories': ['applicant', 'rpa', 'issuer', 'safety'],
        'hazards': [_h_('Exposure to ionising radiation', 'Radiation injury, long-term illness', 2, 5, 'Distance, shielding, time limits, barriers'),
                    _h_('Lost or stuck source', 'High exposure', 1, 5, 'Trained crew, retrieval kit, emergency plan')],
    },
    {
        'key': 'scaffolding', 'name': 'Scaffolding Erection / Dismantling Permit', 'color': '#08979c', 'validity_hours': 24,
        'standards': ['OSHA 29 CFR 1926.451', 'BS EN 12811-1', 'NASC TG20'],
        'description': 'Erection, alteration and dismantling of scaffolds and temporary access structures.',
        'gas_test': False,
        'ppe': ['Full-body harness', 'Safety helmet with chin strap', 'Safety boots', 'Gloves'],
        'precautions': ['Scaffold design / drawing available for non-standard scaffolds', 'Competent scaffolders only', 'Base plates and sole boards on firm ground',
                        'Exclusion zone and tool tethering during erection', 'Scaffold tagged (green/red) and inspected before use'],
        'required_documents': ['Scaffold design / drawing', 'Scaffolder competency cards', 'Scaffold inspection register'],
        'signatories': ['applicant', 'issuer', 'safety'],
        'hazards': [_h_('Falls during erection', 'Fatality', 3, 5, 'Advance guardrail system, harness, competent scaffolders'),
                    _h_('Scaffold collapse', 'Multiple injuries', 2, 5, 'Design, ties, inspections, load limits'),
                    _h_('Falling materials', 'Injury to people below', 3, 4, 'Exclusion zone, netting, tethering')],
    },
    {
        'key': 'diving', 'name': 'Diving Operations Permit', 'color': '#0050b3', 'validity_hours': 12,
        'standards': ['IMCA D014', 'UK Diving at Work Regulations 1997', 'OSHA 29 CFR 1910 Subpart T'],
        'description': 'Commercial diving, including inshore and offshore diving and work near water intakes.',
        'gas_test': False,
        'ppe': ['Diving equipment as per diving project plan', 'Life jacket for topside crew'],
        'precautions': ['Diving project plan and dive plan approved', 'Intakes, propellers and pumps isolated', 'Standby diver dressed and ready',
                        'Weather, current and visibility within limits', 'Medical and emergency (recompression) arrangements confirmed'],
        'required_documents': ['Diving project plan', 'Diver medical and competency certificates', 'Isolation certificate', 'Emergency response plan'],
        'signatories': ['applicant', 'isolator', 'issuer', 'safety'],
        'hazards': [_h_('Differential pressure / suction at intakes', 'Fatality', 2, 5, 'Isolation and LOTO of intakes and pumps'),
                    _h_('Loss of breathing gas', 'Drowning', 2, 5, 'Bail-out cylinder, gas monitoring, standby diver'),
                    _h_('Decompression illness', 'Serious injury', 2, 4, 'Dive tables, ascent control, chamber available')],
    },
]
PERMIT_TYPE_BY_KEY = {t['key']: t for t in PERMIT_TYPES}

STYLES = {
    'classic': {'label': 'Classic (bordered form)', 'font': 'serif'},
    'modern': {'label': 'Modern (coloured headers)', 'font': 'sans-serif'},
    'compact': {'label': 'Compact (fits more on a page)', 'font': 'sans-serif'},
}


def risk_rating(likelihood, severity):
    score = int(likelihood or 0) * int(severity or 0)
    for lo, hi, label, color in RISK_LEVELS:
        if lo <= score <= hi:
            return score, label, color
    return score, 'Not rated', '#8c8c8c'


def public_catalog():
    """Catalogue for the frontend wizard."""
    return {'types': PERMIT_TYPES, 'gas_limits': GAS_LIMITS, 'signatories': SIGNATORIES,
            'styles': [{'key': k, **v} for k, v in STYLES.items()],
            'risk_levels': [{'min': lo, 'max': hi, 'label': lb, 'color': c} for lo, hi, lb, c in RISK_LEVELS]}


def _e(v):
    return _h.escape(str(v if v is not None else ''))


def render_permit_html(permit, company_name=''):
    """HTML for the permit document (used for the on-screen preview and the PDF)."""
    d = permit.get('data') or {}
    ptype = PERMIT_TYPE_BY_KEY.get(permit.get('permit_type')) or {}
    style = d.get('style') or {}
    style_key = style.get('template') if style.get('template') in STYLES else 'modern'
    accent = style.get('color') or ptype.get('color') or '#1677ff'
    if not (isinstance(accent, str) and accent.startswith('#') and len(accent) in (4, 7)):
        accent = '#1677ff'
    font = STYLES[style_key]['font']
    base = 8.6 if style_key == 'compact' else 9.6
    # the PDF engine ignores background colours, so headings use coloured text + an accent rule
    head_fg = accent if style_key == 'modern' else '#1f1f1f'
    head_rule = f'2px solid {accent}' if style_key != 'classic' else '1.4px solid #333'
    border = '1.4px solid #333' if style_key == 'classic' else '1px solid #d0d7e2'

    def section(title, body):
        return f'<h2>{_e(title)}</h2>{body}'

    def table(headers, rows, widths=None):
        th = ''.join(f'<th>{_e(x)}</th>' for x in headers)
        trs = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
        return f'<table class="grid"><tr>{th}</tr>{trs}</table>'

    details = [
        ('Permit number', permit.get('permit_number')), ('Permit type', ptype.get('name') or d.get('custom_type_name') or permit.get('permit_type')),
        ('Location / equipment', permit.get('location')), ('Contractor / work party', d.get('contractor')),
        ('Valid from', permit.get('start_at')), ('Valid until', permit.get('end_at')),
        ('Overall risk', permit.get('risk_level')), ('Status', (permit.get('status') or '').upper()),
    ]
    meta = '<table class="meta">' + ''.join(
        f'<tr><td class="k">{_e(a)}</td><td>{_e(b)}</td><td class="k">{_e(c)}</td><td>{_e(e)}</td></tr>'
        for (a, b), (c, e) in zip(details[0::2], details[1::2])) + '</table>'

    parts = [
        f'<div class="top"><div class="co">{_e(style.get("company_name") or company_name)}</div>'
        f'<h1>{_e(permit.get("title") or ptype.get("name") or "Permit to Work")}</h1>'
        f'<div class="std">{_e(", ".join(ptype.get("standards", [])))}</div></div>',
        meta,
        section('1. Description of work', f'<p>{_e(permit.get("work_description"))}</p>'),
    ]
    hazards = d.get('hazards') or []
    if hazards:
        rows = []
        for i, hz in enumerate(hazards, 1):
            s, lbl, col = risk_rating(hz.get('likelihood'), hz.get('severity'))
            rs, rlbl, rcol = risk_rating(hz.get('residual_likelihood'), hz.get('residual_severity'))
            rows.append([str(i), _e(hz.get('hazard')), _e(hz.get('consequence')),
                         f'<span class="rk" style="color:{col}">{s} {lbl}</span>', _e(hz.get('controls')),
                         f'<span class="rk" style="color:{rcol}">{rs} {rlbl}</span>'])
        parts.append(section('2. Risk assessment', table(['#', 'Hazard', 'Consequence', 'Risk', 'Control measures', 'Residual'], rows)
                             + '<p class="note">Risk = likelihood (1-5) × severity (1-5). Low 1-4 · Medium 5-9 · High 10-16 · Extreme 17-25.</p>'))
    prec = d.get('precautions') or []
    if prec:
        rows = [[('☑' if p.get('done') else '☐'), _e(p.get('text')), _e(p.get('note'))] for p in prec]
        parts.append(section('3. Precautions and controls', table(['', 'Precaution', 'Remarks'], rows)))
    gas = d.get('gas_tests') or []
    if gas:
        rows = []
        for g in gas:
            vals = []
            for k in ('O2', 'LEL', 'H2S', 'CO'):
                if g.get(k) not in (None, ''):
                    lim = GAS_LIMITS[k]
                    try:
                        v = float(g[k])
                        ok = (v >= lim.get('min', -1e9)) and (v <= lim.get('max', 1e9))
                    except (TypeError, ValueError):
                        ok = False
                    vals.append(f'<span class="{"ok" if ok else "bad"}">{k}: {_e(g[k])} {lim["unit"]}</span>')
            rows.append([_e(g.get('time')), ' '.join(vals), _e(g.get('tester')), _e(g.get('location'))])
        parts.append(section('4. Gas test record', table(['Time', 'Readings', 'Tested by', 'Test point'], rows)
                             + '<p class="note">Acceptable: O₂ 19.5-23.5 % · flammable &lt; 10 % LEL · H₂S &lt; 10 ppm · CO &lt; 25 ppm.</p>'))
    ppe = d.get('ppe') or []
    if ppe:
        parts.append(section('5. Personal protective equipment', '<p>' + ' · '.join(_e(x) for x in ppe) + '</p>'))
    docs = d.get('required_documents') or []
    if docs:
        rows = [[('☑' if x.get('attached') else '☐'), _e(x.get('name')), _e(x.get('reference') or ('Attached' if x.get('attached') else 'Outstanding'))] for x in docs]
        parts.append(section('6. Supporting documents', table(['', 'Document', 'Reference / status'], rows)))
    custom = d.get('custom_fields') or []
    if custom:
        parts.append(section('7. Additional information', '<table class="meta">' + ''.join(
            f'<tr><td class="k">{_e(c.get("label"))}</td><td colspan="3">{_e(c.get("value"))}</td></tr>' for c in custom) + '</table>'))
    sigs = d.get('signatories') or []
    if sigs:
        rows = [[_e(SIGNATORIES.get(s.get('role'), s.get('role'))), _e(s.get('name')), '', ''] for s in sigs]
        parts.append(section('Authorisation', table(['Role', 'Name', 'Signature', 'Date / time'], rows)
                             + '<p class="note">Electronic signatures and stamps are added when this permit is approved through SafeTrack Pro; the approval certificate is attached at the end.</p>'))
    parts.append(section('Close-out / hand-back', table(['Work completed and area left safe', 'Isolations removed', 'Permit closed by', 'Date / time'],
                                                         [['☐ Yes  ☐ No', '☐ Yes  ☐ N/A', '', '']])))
    css = f"""
    * {{ font-family: {font}; }}
    body {{ font-size: {base}pt; color: #1f1f1f; }}
    .top {{ border-bottom: 3px solid {accent}; padding-bottom: 4px; margin-bottom: 6px; }}
    .co {{ font-size: {base + 1}pt; color: #555; font-weight: bold; }}
    h1 {{ font-size: {base + 8}pt; color: {accent}; margin: 2px 0; }}
    .std {{ font-size: {base - 1.5}pt; color: #777; }}
    h2 {{ font-size: {base + 1.5}pt; color: {head_fg}; border-bottom: {head_rule}; padding: 2px 0; margin: 10px 0 4px 0; }}
    table {{ border-collapse: collapse; width: 100%; }}
    table.meta td {{ border: {border}; padding: 3px 5px; }}
    td.k {{ background: #f5f7fa; font-weight: bold; width: 20%; }}
    table.grid th {{ border: {border}; background: #f5f7fa; text-align: left; padding: 3px; font-size: {base - 0.6}pt; }}
    table.grid td {{ border: {border}; padding: 3px; vertical-align: top; }}
    .rk {{ font-weight: bold; }}
    .ok {{ color: #237804; font-weight: bold; }}
    .bad {{ color: #cf1322; font-weight: bold; }}
    .note {{ font-size: {base - 1.6}pt; color: #666; margin: 3px 0; }}
    p {{ margin: 3px 0; }}
    """
    return f'<style>{css}</style>' + ''.join(parts)
