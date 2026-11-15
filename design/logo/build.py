# /// script
# dependencies = ["shapely", "fonttools", "uharfbuzz"]
# ///
"""Build the Infinipedia logo SVGs (and PNGs when rsvg-convert is installed).

Run with: uv run build.py

Symbol: an infinity sign left open at its right end, so it also reads as a
lowercase alpha and as the ichthys fish. It is written with a broad nib held
at 38 degrees: the outline is the centre line swept along the nib, then
rounded by half the nib's thickness.
Wordmark: lowercase "infinipedia" from EB Garamond Medium outlines.
"""
from io import BytesIO
from pathlib import Path
import math
import shutil
import subprocess

import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from shapely.geometry import Polygon
from shapely.ops import unary_union

ROOT = Path(__file__).resolve().parent

FONT = ROOT / 'fonts' / 'EBGaramond[wght].ttf'

LAPIS = '#1d3f9c'
IVORY = '#fbf6ea'
INK = '#141a26'       # wordmark on light backgrounds
FONT_WEIGHT = 500     # EB Garamond Medium
FONT_SIZE = 92        # wordmark size on the symbol's 100-unit grid
TEXT_GAP = 26         # visible gap between the symbol and the first letter
LOGO_MARGIN = 12      # clear space around the full logo

# Centre line: a closed infinity sign as eight cubic beziers, starting and ending at its far right point.
START = (90, 50)
SEGMENTS = [
    (90, 38, 82, 28, 70, 28), (62, 28, 57, 38, 50, 50), (43, 62, 38, 72, 30, 72), (18, 72, 10, 62, 10, 50),
    (10, 38, 18, 28, 30, 28), (38, 28, 43, 38, 50, 50), (57, 62, 62, 72, 70, 72), (82, 72, 90, 62, 90, 50),
]
OPENING = 10          # percent of the centre line removed, centred on the far right point
NIB_ANGLE = -38       # degrees; the nib's long axis
NIB_LENGTH = 10.08    # long axis of the nib
NIB_THICKNESS = 3.264  # short axis; also rounds every corner
TILE_SCALE = 0.9      # symbol size inside the 100-unit app tile
TILE_RADIUS = 23
MASKABLE_SCALE = 0.72  # keeps the symbol inside the 80% maskable safe zone
MARK_MARGIN = 6       # clear space around the symbol-only files


def centre_line(samples=96):
    pts, p0 = [START], START
    for x1, y1, x2, y2, x3, y3 in SEGMENTS:
        for i in range(1, samples + 1):
            t = i / samples
            u = 1 - t
            pts.append((
                u**3 * p0[0] + 3 * u * u * t * x1 + 3 * u * t * t * x2 + t**3 * x3,
                u**3 * p0[1] + 3 * u * u * t * y1 + 3 * u * t * t * y2 + t**3 * y3,
            ))
        p0 = (x3, y3)
    return pts


def trim(pts, percent):
    lengths = [0.0]
    for a, b in zip(pts, pts[1:]):
        lengths.append(lengths[-1] + math.dist(a, b))
    cut = lengths[-1] * percent / 200
    lo, hi = cut, lengths[-1] - cut

    def at(s):
        i = next(k for k in range(1, len(lengths)) if lengths[k] >= s)
        f = (s - lengths[i - 1]) / (lengths[i] - lengths[i - 1])
        return (pts[i - 1][0] + f * (pts[i][0] - pts[i - 1][0]), pts[i - 1][1] + f * (pts[i][1] - pts[i - 1][1]))

    return [at(lo)] + [p for p, s in zip(pts, lengths) if lo < s < hi] + [at(hi)]


def symbol():
    """The symbol's outline, centred on (50, 50) by its centre line."""
    pts = trim(centre_line(), OPENING)
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    dx, dy = 50 - (min(xs) + max(xs)) / 2, 50 - (min(ys) + max(ys)) / 2
    pts = [(x + dx, y + dy) for x, y in pts]
    a = math.radians(NIB_ANGLE)
    hx, hy = NIB_LENGTH / 2 * math.cos(a), NIB_LENGTH / 2 * math.sin(a)
    sweep = []
    for (px, py), (qx, qy) in zip(pts, pts[1:]):
        quad = Polygon([(px - hx, py - hy), (px + hx, py + hy), (qx + hx, qy + hy), (qx - hx, qy - hy)])
        sweep.append(quad.convex_hull)
    return unary_union(sweep).buffer(NIB_THICKNESS / 2, resolution=32).simplify(0.004)


def path_data(shape):
    polygons = [shape] if shape.geom_type == 'Polygon' else list(shape.geoms)
    parts = []
    for polygon in polygons:
        for ring in [polygon.exterior, *polygon.interiors]:
            coords = list(ring.coords)[:-1]
            parts.append('M' + 'L'.join(f'{x:.3f} {y:.3f}' for x, y in coords) + 'Z')
    return ''.join(parts)


def wordmark(left, centre_y):
    """Outlines of "infinipedia" starting at x = left, its x-height centred on centre_y."""
    medium = instancer.instantiateVariableFont(TTFont(FONT), {'wght': FONT_WEIGHT})
    data = BytesIO()
    medium.save(data)
    face = hb.Face(data.getvalue())
    buffer = hb.Buffer()
    buffer.add_str('infinipedia')
    buffer.guess_segment_properties()
    hb.shape(hb.Font(face), buffer)
    glyphs, order, k = medium.getGlyphSet(), medium.getGlyphOrder(), FONT_SIZE / face.upem
    baseline = centre_y + medium['OS/2'].sxHeight * k / 2

    def draw(pen, shift):
        x = 0
        for info, pos in zip(buffer.glyph_infos, buffer.glyph_positions):
            glyphs[order[info.codepoint]].draw(TransformPen(pen, (k, 0, 0, -k, shift + (x + pos.x_offset) * k, baseline - pos.y_offset * k)))
            x += pos.x_advance

    bounds = BoundsPen(glyphs)
    draw(bounds, 0)
    shift = left - bounds.bounds[0]
    pen = SVGPathPen(glyphs, ntos=lambda v: f'{v:.3f}'.rstrip('0').rstrip('.'))
    draw(pen, shift)
    x0, y0, x1, y1 = bounds.bounds
    return pen.getCommands(), (x0 + shift, y0, x1 + shift, y1)


def svg(view_box, body, label):
    x, y, w, h = view_box
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x:g} {y:g} {w:g} {h:g}" role="img" aria-label="{label}">\n'
            f'{body}\n</svg>\n')


def tile(d, scale, radius):
    k = f'translate(50 50) scale({scale}) translate(-50 -50)'
    return (f'  <rect width="100" height="100" rx="{radius}" fill="{IVORY}"/>\n'
            f'  <path transform="{k}" fill="{LAPIS}" fill-rule="evenodd" d="{d}"/>')


def main():
    shape = symbol()
    d = path_data(shape)
    x0, y0, x1, y1 = shape.bounds
    box = (round(x0 - MARK_MARGIN, 3), round(y0 - MARK_MARGIN, 3), round(x1 - x0 + 2 * MARK_MARGIN, 3), round(y1 - y0 + 2 * MARK_MARGIN, 3))
    files = {
        'infinipedia-mark-on-light.svg': svg(box, f'  <path fill="{LAPIS}" fill-rule="evenodd" d="{d}"/>', 'Infinipedia'),
        'infinipedia-mark-on-dark.svg': svg(box, f'  <path fill="{IVORY}" fill-rule="evenodd" d="{d}"/>', 'Infinipedia'),
        'infinipedia-app-icon.svg': svg((0, 0, 100, 100), tile(d, TILE_SCALE, TILE_RADIUS), 'Infinipedia'),
        'infinipedia-app-icon-square.svg': svg((0, 0, 100, 100), tile(d, MASKABLE_SCALE, 0), 'Infinipedia'),
        'infinipedia-favicon.svg': svg((0, 0, 100, 100), tile(d, TILE_SCALE, TILE_RADIUS), 'Infinipedia'),
    }
    text_d, (tx0, ty0, tx1, ty1) = wordmark(x1 + TEXT_GAP, (y0 + y1) / 2)
    top, bottom = min(y0, ty0) - LOGO_MARGIN, max(y1, ty1) + LOGO_MARGIN
    logo_box = (round(x0 - LOGO_MARGIN, 3), round(top, 3), round(tx1 - x0 + 2 * LOGO_MARGIN, 3), round(bottom - top, 3))
    for ground, mark_fill, text_fill in (('light', LAPIS, INK), ('dark', IVORY, IVORY)):
        files[f'infinipedia-logo-on-{ground}.svg'] = svg(
            logo_box, f'  <path fill="{mark_fill}" fill-rule="evenodd" d="{d}"/>\n  <path fill="{text_fill}" d="{text_d}"/>', 'Infinipedia')
    for name, text in files.items():
        (ROOT / name).write_text(text)
        print('wrote', name, f'({len(text)} bytes)')

    if not shutil.which('rsvg-convert'):
        print('rsvg-convert not found: skipped PNGs')
        return
    pngs = {
        'infinipedia-logo-on-light': ['-w', '2400'], 'infinipedia-logo-on-dark': ['-w', '2400'],
        'infinipedia-mark-on-light': ['-h', '1024'], 'infinipedia-mark-on-dark': ['-h', '1024'],
        'infinipedia-app-icon': ['-w', '1024'], 'infinipedia-app-icon-square': ['-w', '1024'], 'infinipedia-favicon': ['-w', '64'],
    }
    for stem, size in pngs.items():
        subprocess.run(['rsvg-convert', *size, str(ROOT / f'{stem}.svg'), '-o', str(ROOT / f'{stem}.png')], check=True)
        print('wrote', f'{stem}.png')


if __name__ == '__main__':
    main()
