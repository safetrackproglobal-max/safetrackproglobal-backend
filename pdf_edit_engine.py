"""
PDF editing engine (PyMuPDF) used by the Document Control PDF editor.

Coordinates exchanged with the frontend are *visible page points*: origin at the top-left of the
page as the user sees it (rotation applied), 1 unit = 1 PDF point. This is exactly what PDF.js
uses for a viewport at scale 1, so the browser preview and the saved file line up.

Two entry points:
    extract_text_lines(pdf_bytes, page_number)  -> editable text lines with font/size/colour
    apply_edits(pdf_bytes, objects)             -> new PDF bytes with all edits applied

"Edit text" really removes the original characters (redaction with no fill, so the page
background and graphics stay) and writes the new text at the same baseline. "White-out" removes
text underneath and paints a solid colour.
"""
import re

import pymupdf as fitz

# Line height and first-baseline ratios used by the browser preview (CSS line-height 1.2),
# so text drawn here sits where the user saw it while editing.
LINE_HEIGHT = 1.2
BASELINE_RATIO = {'Helvetica': 0.947, 'Times': 0.938, 'Courier': 0.867}

# PyMuPDF base-14 font codes: (family, bold, italic) -> fontname
BASE14 = {
    ('Helvetica', False, False): 'helv', ('Helvetica', True, False): 'hebo',
    ('Helvetica', False, True): 'heit', ('Helvetica', True, True): 'hebi',
    ('Times', False, False): 'tiro', ('Times', True, False): 'tibo',
    ('Times', False, True): 'tiit', ('Times', True, True): 'tibi',
    ('Courier', False, False): 'cour', ('Courier', True, False): 'cobo',
    ('Courier', False, True): 'coit', ('Courier', True, True): 'cobi',
}

MAX_OBJECTS = 2000
MAX_TEXT = 5000


class PdfEditError(ValueError):
    """A problem the user can fix (bad input, unsupported characters...)."""


# ---------------------------------------------------------------- helpers
def _hex(color_int):
    return '#{:06x}'.format(int(color_int) & 0xFFFFFF)


def _rgb(hex_color, default=(0, 0, 0)):
    try:
        h = str(hex_color).lstrip('#')
        if len(h) == 3:
            h = ''.join(c * 2 for c in h)
        return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
    except Exception:
        return default


def guess_family(font_name):
    n = (font_name or '').lower()
    if re.search(r'courier|mono|consol|menlo', n):
        return 'Courier'
    if re.search(r'times|serif|georgia|garamond|roman|cambria|book|minion|palatino', n) and 'sans' not in n:
        return 'Times'
    return 'Helvetica'


def _fontname(obj):
    family = obj.get('font') if obj.get('font') in BASELINE_RATIO else 'Helvetica'
    return BASE14[(family, bool(obj.get('bold')), bool(obj.get('italic')))], family


def _check_encodable(text):
    """Base-14 fonts only cover Latin-1 (WinAnsi). Refuse instead of silently printing '?'."""
    bad = sorted({ch for ch in text if ord(ch) > 255 and ch not in '–—‘’“”•€…'})
    if bad:
        raise PdfEditError('These characters cannot be written with the built-in PDF fonts: ' + ' '.join(bad[:10]))


def _num(v, name):
    try:
        f = float(v)
    except (TypeError, ValueError):
        raise PdfEditError(f'{name} must be a number')
    if f != f or abs(f) > 100000:
        raise PdfEditError(f'{name} is out of range')
    return f


def _to_unrot(page, x, y):
    """visible point -> PyMuPDF (unrotated) page point"""
    return fitz.Point(x, y) * page.derotation_matrix


def _rect_to_unrot(page, x0, y0, x1, y1):
    r = fitz.Rect(_to_unrot(page, x0, y0), _to_unrot(page, x1, y1))
    r.normalize()
    return r


# ---------------------------------------------------------------- text detection
def extract_text_lines(pdf_bytes, page_number):
    """Editable text lines on one page, in visible coordinates."""
    doc = fitz.open(stream=pdf_bytes, filetype='pdf')
    try:
        if page_number < 1 or page_number > doc.page_count:
            raise PdfEditError('Page out of range')
        page = doc[page_number - 1]
        rot = page.rotation_matrix
        data = page.get_text('dict', flags=fitz.TEXTFLAGS_TEXT)
        lines = []
        for b_i, block in enumerate(data.get('blocks', [])):
            for l_i, line in enumerate(block.get('lines', [])):
                spans = [s for s in line.get('spans', []) if s.get('text', '').strip()]
                if not spans:
                    continue
                # visible direction must be horizontal (left-to-right)
                dx, dy = line.get('dir', (1, 0))
                vdir = fitz.Point(dx, dy) * fitz.Matrix(rot.a, rot.b, rot.c, rot.d, 0, 0)
                if abs(vdir.y) > 0.01 or vdir.x <= 0:
                    continue
                text = ''.join(s['text'] for s in line['spans']).rstrip()
                main = max(spans, key=lambda s: len(s['text'].strip()))
                bbox = fitz.Rect(line['bbox']) * rot
                bbox.normalize()
                origin = fitz.Point(spans[0]['origin']) * rot
                styles = {(s['font'], round(s['size'], 1), s['color']) for s in spans}
                flags = main.get('flags', 0)
                font_name = main.get('font', '')
                lines.append({
                    'id': f'p{page_number}_b{b_i}_l{l_i}',
                    'text': text,
                    'x0': round(bbox.x0, 2), 'y0': round(bbox.y0, 2),
                    'x1': round(bbox.x1, 2), 'y1': round(bbox.y1, 2),
                    'origin_x': round(origin.x, 2), 'baseline': round(origin.y, 2),
                    'size': round(main['size'], 2),
                    'font_name': font_name,
                    'font': guess_family(font_name),
                    'bold': bool(flags & 16) or bool(re.search(r'bold|black|heavy|semibold|demi', font_name, re.I)),
                    'italic': bool(flags & 2) or bool(re.search(r'italic|oblique', font_name, re.I)),
                    'color': _hex(main.get('color', 0)),
                    'mixed_styles': len(styles) > 1,
                })
        has_images = bool(page.get_images(full=False))
        return {
            'page': page_number,
            'width': round(page.rect.width, 2),
            'height': round(page.rect.height, 2),
            'rotation': page.rotation,
            'lines': lines,
            'likely_scanned': not lines and has_images,
        }
    finally:
        doc.close()


# ---------------------------------------------------------------- writing
def _insert_lines(page, x, top, text, size, color, fontname, family, align='left', box_width=None,
                  baseline=None):
    """Draw (multi-line) text. `baseline` (first line) wins over `top` when given."""
    lines = text.split('\n')
    first_baseline = baseline if baseline is not None else top + BASELINE_RATIO[family] * size
    widths = [fitz.get_text_length(l, fontname=fontname, fontsize=size) for l in lines]
    width = box_width or (max(widths) if widths else 0)
    for i, line in enumerate(lines):
        if not line:
            continue
        lx = x
        if align == 'center':
            lx = x + (width - widths[i]) / 2
        elif align == 'right':
            lx = x + width - widths[i]
        p = _to_unrot(page, lx, first_baseline + i * LINE_HEIGHT * size)
        page.insert_text(p, line, fontsize=size, fontname=fontname, color=color, rotate=page.rotation)


def _validate(objects):
    if not isinstance(objects, list) or not objects:
        raise PdfEditError('Nothing to save')
    if len(objects) > MAX_OBJECTS:
        raise PdfEditError('Too many changes in one save')
    for o in objects:
        if not isinstance(o, dict) or not isinstance(o.get('page'), int):
            raise PdfEditError('Every change needs a page number')
        text = o.get('text')
        if text is not None:
            if not isinstance(text, str) or len(text) > MAX_TEXT:
                raise PdfEditError('Text is too long')
            _check_encodable(text)


def apply_edits(pdf_bytes, objects):
    """Apply editor objects (visible coordinates) and return the new PDF bytes."""
    _validate(objects)
    doc = fitz.open(stream=pdf_bytes, filetype='pdf')
    try:
        if doc.needs_pass:
            raise PdfEditError('This PDF is password protected and cannot be edited')
        by_page = {}
        for o in objects:
            if o['page'] < 1 or o['page'] > doc.page_count:
                raise PdfEditError(f"Page {o['page']} does not exist")
            by_page.setdefault(o['page'], []).append(o)

        for page_no, objs in by_page.items():
            page = doc[page_no - 1]

            # 1) removal pass: edited text is removed (background kept); white-out erases + paints
            redactions = 0
            for o in objs:
                t = o.get('type')
                if t == 'textedit':
                    x0, y0, x1, y1 = (_num(v, 'cover') for v in o['cover'])
                    r = _rect_to_unrot(page, x0, y0, x1, y1)
                    page.add_redact_annot(r, fill=False, cross_out=False)
                    redactions += 1
                elif t == 'whiteout':
                    x, y, w, h = (_num(o[k], k) for k in ('x', 'y', 'w', 'h'))
                    r = _rect_to_unrot(page, x, y, x + w, y + h)
                    page.add_redact_annot(r, fill=_rgb(o.get('color', '#ffffff'), (1, 1, 1)), cross_out=False)
                    redactions += 1
            if redactions:
                page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE,
                                      graphics=fitz.PDF_REDACT_LINE_ART_NONE,
                                      text=fitz.PDF_REDACT_TEXT_REMOVE)

            # 2) drawing pass (in the order the user created them)
            for o in objs:
                t = o.get('type')
                color = _rgb(o.get('color', '#000000'))
                if t in ('textedit', 'textbox'):
                    text = o.get('text') or ''
                    if not text.strip():
                        continue
                    size = max(4.0, min(144.0, _num(o.get('size', 12), 'size')))
                    fontname, family = _fontname(o)
                    if t == 'textbox' and o.get('bg'):
                        x, y = _num(o['x'], 'x'), _num(o['y'], 'y')
                        widths = [fitz.get_text_length(l, fontname=fontname, fontsize=size) for l in text.split('\n')]
                        bw = max(widths) + 4
                        bh = LINE_HEIGHT * size * len(text.split('\n')) + 2
                        page.draw_rect(_rect_to_unrot(page, x - 2, y - 1, x + bw, y + bh),
                                       color=None, fill=_rgb(o['bg'], (1, 1, 1)), overlay=True)
                    if t == 'textedit':
                        _insert_lines(page, _num(o['x'], 'x'), None, text, size, color, fontname, family,
                                      baseline=_num(o['baseline'], 'baseline'))
                    else:
                        _insert_lines(page, _num(o['x'], 'x'), _num(o['y'], 'y'), text, size, color,
                                      fontname, family, align=o.get('align', 'left'))
                elif t in ('highlight', 'rect', 'ellipse', 'stamp', 'note'):
                    x, y, w, h = (_num(o[k], k) for k in ('x', 'y', 'w', 'h'))
                    r = _rect_to_unrot(page, x, y, x + w, y + h)
                    width = max(0.5, min(20.0, _num(o.get('width', 2), 'width')))
                    if t == 'highlight':
                        # A real highlight annotation: viewers blend it (multiply), so text stays crisp
                        annot = page.add_highlight_annot(r)
                        annot.set_colors(stroke=color)
                        annot.update()
                    elif t == 'rect':
                        page.draw_rect(r, color=color, width=width, overlay=True)
                    elif t == 'ellipse':
                        page.draw_oval(r, color=color, width=width, overlay=True)
                    elif t == 'stamp':
                        page.draw_rect(r, color=color, width=2.5, overlay=True)
                        text = (o.get('text') or 'APPROVED').upper()
                        size = max(8.0, min(h * 0.55, 48.0))
                        tw = fitz.get_text_length(text, fontname='hebo', fontsize=size)
                        if tw > w - 8:
                            size = size * (w - 8) / tw
                            tw = fitz.get_text_length(text, fontname='hebo', fontsize=size)
                        _insert_lines(page, x + (w - tw) / 2, None, text, size, color, 'hebo', 'Helvetica',
                                      baseline=y + h / 2 + size * 0.35)
                    elif t == 'note':
                        page.draw_rect(r, color=_rgb('#d4b106'), fill=_rgb(o.get('color', '#fff566')), width=1, overlay=True)
                        text = o.get('text') or ''
                        size = max(6.0, min(14.0, _num(o.get('size', 10), 'size')))
                        _insert_lines(page, x + 4, y + 3, text, size, (0.15, 0.15, 0.15), 'helv', 'Helvetica')
                elif t == 'line':
                    p1 = _to_unrot(page, _num(o['x1'], 'x1'), _num(o['y1'], 'y1'))
                    p2 = _to_unrot(page, _num(o['x2'], 'x2'), _num(o['y2'], 'y2'))
                    page.draw_line(p1, p2, color=color, width=max(0.5, min(20.0, _num(o.get('width', 2), 'width'))), overlay=True)
                elif t == 'ink':
                    pts = o.get('points') or []
                    if len(pts) >= 2:
                        poly = [_to_unrot(page, _num(p[0], 'point'), _num(p[1], 'point')) for p in pts[:5000]]
                        page.draw_polyline(poly, color=color, width=max(0.5, min(20.0, _num(o.get('width', 2), 'width'))),
                                           overlay=True, lineCap=1, lineJoin=1)
                elif t == 'whiteout':
                    pass  # done in the removal pass
                else:
                    raise PdfEditError(f"Unknown change type: {t}")

        return doc.tobytes(garbage=3, deflate=True)
    finally:
        doc.close()


# ================================================================ signing / conversion
SLOT_W, SLOT_H, SLOT_GAP, SLOT_MARGIN = 160.0, 64.0, 12.0, 40.0


def default_slots(pdf_bytes, count):
    """Signature boxes along the bottom of the last page (visible coords), filling rows upwards."""
    doc = fitz.open(stream=pdf_bytes, filetype='pdf')
    try:
        page = doc[-1]
        w, h = page.rect.width, page.rect.height
        per_row = max(1, int((w - 2 * SLOT_MARGIN + SLOT_GAP) // (SLOT_W + SLOT_GAP)))
        slots = []
        for i in range(count):
            row, col = divmod(i, per_row)
            x = SLOT_MARGIN + col * (SLOT_W + SLOT_GAP)
            y = h - SLOT_MARGIN - SLOT_H - row * (SLOT_H + 26)
            slots.append({'page': doc.page_count, 'x': x, 'y': y, 'w': SLOT_W, 'h': SLOT_H})
        return slots
    finally:
        doc.close()


def place_images(pdf_bytes, placements):
    """placements: [{page, x, y, w, h, image: bytes, caption?: str}] in visible coordinates.
    Images keep their aspect ratio inside the box and appear upright on rotated pages."""
    doc = fitz.open(stream=pdf_bytes, filetype='pdf')
    try:
        for p in placements:
            n = int(p['page'])
            if n < 1 or n > doc.page_count:
                raise PdfEditError(f'Page {n} does not exist')
            page = doc[n - 1]
            x, y, w, h = (_num(p[k], k) for k in ('x', 'y', 'w', 'h'))
            if w < 8 or h < 8:
                raise PdfEditError('Signature box is too small')
            rect = _rect_to_unrot(page, x, y, x + w, y + h)
            page.insert_image(rect, stream=p['image'], keep_proportion=True, rotate=page.rotation, overlay=True)
            if p.get('caption'):
                cap = str(p['caption'])[:120]
                _check_encodable(cap)
                size = 6.5
                _insert_lines(page, x, None, cap, size, (0.25, 0.25, 0.25), 'helv', 'Helvetica',
                              baseline=y + h + size + 1.5)
        return doc.tobytes(garbage=3, deflate=True)
    finally:
        doc.close()


def append_certificate(pdf_bytes, info):
    """Add an approval certificate page (audit trail) at the end of the PDF.
    info: {title, reference, company, submitted_by, submitted_at, completed_at, status,
           content_hash, signers: [{order, name, organization, action, decision, at, ip, comment}]}"""
    import html as _h
    doc = fitz.open(stream=pdf_bytes, filetype='pdf')
    try:
        last = doc[-1].rect
        width, height = (last.width, last.height) if last.width < last.height else (595, 842)
        page = doc.new_page(width=width, height=height)
        rows = ''.join(
            '<tr>' + ''.join(f'<td>{_h.escape(str(c or ""))}</td>' for c in (
                s.get('order'), s.get('name'), s.get('organization'), s.get('action'),
                s.get('decision'), s.get('at'), s.get('ip'))) + '</tr>'
            + (f'<tr><td></td><td colspan="6" class="c">Comment: {_h.escape(s["comment"])}</td></tr>' if s.get('comment') else '')
            for s in info.get('signers', []))
        status = _h.escape(str(info.get('status', '')).upper())
        html = f"""
        <h1>Approval Certificate</h1>
        <p class="st">Status: <b>{status}</b></p>
        <table class="meta">
          <tr><td class="k">Document</td><td>{_h.escape(str(info.get('title', '')))}</td></tr>
          <tr><td class="k">Submission reference</td><td>{_h.escape(str(info.get('reference', '')))}</td></tr>
          <tr><td class="k">Issued by</td><td>{_h.escape(str(info.get('company', '')))}</td></tr>
          <tr><td class="k">Submitted by</td><td>{_h.escape(str(info.get('submitted_by', '')))} on {_h.escape(str(info.get('submitted_at', '')))}</td></tr>
          <tr><td class="k">Completed</td><td>{_h.escape(str(info.get('completed_at', '')))}</td></tr>
        </table>
        <h2>Signatures and decisions</h2>
        <table class="sig">
          <tr><th>#</th><th>Name</th><th>Organisation</th><th>Action</th><th>Decision</th><th>Date (UTC)</th><th>IP</th></tr>
          {rows}
        </table>
        <p class="hash">SHA-256 of the signed document pages: {_h.escape(str(info.get('content_hash', '')))}</p>
        <p class="foot">This certificate was generated automatically by SafeTrack Pro Global. Every signature above was applied by the named, logged-in user; the record is kept in the document's audit trail.</p>
        """
        css = """
        * { font-family: sans-serif; }
        h1 { font-size: 20px; color: #0b3d91; margin: 0 0 4px 0; }
        h2 { font-size: 13px; margin: 14px 0 6px 0; color: #222; }
        p.st { font-size: 11px; margin: 0 0 10px 0; }
        table { border-collapse: collapse; width: 100%; }
        table.meta td { font-size: 9.5px; padding: 3px 5px; border-bottom: 1px solid #ddd; }
        td.k { color: #555; width: 30%; }
        table.sig th { font-size: 8.5px; text-align: left; background: #eef3fb; padding: 4px; border: 1px solid #c9d6ea; }
        table.sig td { font-size: 8.5px; padding: 4px; border: 1px solid #dde3ec; }
        td.c { color: #444; font-style: italic; }
        p.hash { font-size: 7.5px; color: #555; margin-top: 12px; }
        p.foot { font-size: 7.5px; color: #777; }
        """
        page.insert_htmlbox(fitz.Rect(40, 40, width - 40, height - 40), html, css=css)
        return doc.tobytes(garbage=3, deflate=True)
    finally:
        doc.close()


def pages_hash(pdf_bytes):
    import hashlib
    return hashlib.sha256(pdf_bytes).hexdigest()


def html_to_pdf(html, title=None):
    """Render editor HTML (documents created in the rich-text editor) to an A4 PDF."""
    import io
    story_html = (f'<h1>{title}</h1>' if title else '') + (html or '')
    story = fitz.Story(html=story_html, user_css='body { font-family: sans-serif; font-size: 11pt; } '
                                                 'table { border-collapse: collapse; } td, th { border: 1px solid #999; padding: 3px; }')
    buf = io.BytesIO()
    writer = fitz.DocumentWriter(buf)
    mediabox = fitz.paper_rect('a4')
    where = mediabox + (50, 50, -50, -50)
    more = True
    while more:
        dev = writer.begin_page(mediabox)
        more, _ = story.place(where)
        story.draw(dev)
        writer.end_page()
    writer.close()
    return buf.getvalue()


def image_to_pdf(image_bytes):
    """Wrap a PNG/JPEG (e.g. a scanned drawing) in a one-page PDF."""
    img = fitz.open(stream=image_bytes)
    try:
        return fitz.open('pdf', img.convert_to_pdf()).tobytes()
    finally:
        img.close()
