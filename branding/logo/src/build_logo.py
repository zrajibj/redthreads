"""Build the Red Threads logo set (SVG with outlined text, plus PNG).

Usage:
    python3 build_logo.py --font path/to/font.ttf [--out ../]

Swap the font by passing a different --font; every file is regenerated.
Needs: fonttools, cairosvg.
"""
import argparse
import os

import cairosvg
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

RED = "#C8102E"
CREAM = "#F2E8D5"
INK = "#1E1E24"

THEMES = {
    "light": {"bg": CREAM, "fg": INK, "accent": RED},
    "dark": {"bg": INK, "fg": CREAM, "accent": RED},
}


class Font:
    def __init__(self, path):
        self.tt = TTFont(path)
        self.gs = self.tt.getGlyphSet()
        self.cmap = self.tt.getBestCmap()
        self.upm = self.tt["head"].unitsPerEm
        os2 = self.tt["OS/2"]
        self.cap = getattr(os2, "sCapHeight", 0) or int(self.upm * 0.7)

    def glyph(self, ch, x, baseline, size):
        """Return (svg path d, advance, bbox x0, x1) for one character."""
        name = self.cmap[ord(ch)]
        s = size / self.upm
        pen = SVGPathPen(self.gs)
        # font units are y-up; flip into SVG space
        self.gs[name].draw(TransformPen(pen, (s, 0, 0, -s, x, baseline)))
        adv = self.gs[name].width * s
        return pen.getCommands(), adv

    def layout(self, text, x, baseline, size, tracking=0.0):
        """Lay out text; returns list of (char, d, x0, x1) and total width."""
        out, cx = [], x
        for ch in text:
            if ch == " ":
                cx += self.gs[self.cmap[32]].width * size / self.upm + tracking * size
                continue
            d, adv = self.glyph(ch, cx, baseline, size)
            out.append((ch, d, cx, cx + adv))
            cx += adv + tracking * size
        return out, cx - x - tracking * size

    def cap_height(self, size):
        return self.cap * size / self.upm


def svg_doc(w, h, body, bg=None):
    rect = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}">{rect}{body}</svg>'
    )


def knockout(rects, cid):
    """clipPath that keeps everything except the given (x0, y0, x1, y1) rects."""
    d = "M-10000,-10000H20000V20000H-10000Z" + "".join(
        f"M{x0:.1f},{y0:.1f}V{y1:.1f}H{x1:.1f}V{y0:.1f}Z" for x0, y0, x1, y1 in rects
    )
    return f'<clipPath id="{cid}"><path d="{d}" clip-rule="evenodd"/></clipPath>'


def woven(letters, fill, thread_y, thread_x0, thread_x1, thread_w, accent, over_every=2, cid="weave"):
    """Letters with a red thread woven through: under some letters, over others.

    The thread is drawn first (under everything), then the letters with a gap
    cut out where the thread passes in front, then the thread across those
    "over" letters. The gap is a real cut-out, so it works on any background.
    """
    gap = thread_w * 0.45
    half = thread_w / 2 + gap
    overs = [(x0, x1) for i, (_, _, x0, x1) in enumerate(letters) if i % over_every == 1]
    rects = [(x0 - gap, thread_y - half, x1 + gap, thread_y + half) for x0, x1 in overs]
    parts = [
        knockout(rects, cid),
        f'<line x1="{thread_x0:.1f}" y1="{thread_y:.1f}" x2="{thread_x1:.1f}" y2="{thread_y:.1f}" '
        f'stroke="{accent}" stroke-width="{thread_w:.1f}" stroke-linecap="round"/>',
        f'<g clip-path="url(#{cid})">',
    ]
    parts += [f'<path d="{d}" fill="{fill}"/>' for _, d, _, _ in letters]
    parts.append("</g>")
    for x0, x1 in overs:
        parts.append(
            f'<line x1="{x0 - gap:.1f}" y1="{thread_y:.1f}" x2="{x1 + gap:.1f}" y2="{thread_y:.1f}" '
            f'stroke="{accent}" stroke-width="{thread_w:.1f}"/>'
        )
    return "".join(parts)


def wordmark(font, theme, transparent=False):
    """Option A: one-line wordmark, RED in red, a thread woven through THREADS."""
    t = THEMES[theme]
    size, pad = 400, 120
    cap = font.cap_height(size)
    red, w_red = font.layout("RED", 0, 0, size, 0.02)
    gap = size * 0.16
    h = cap + 2 * pad
    baseline = pad + cap
    red, w_red = font.layout("RED", pad, baseline, size, 0.02)
    thr, w_thr = font.layout("THREADS", pad + w_red + gap, baseline, size, 0.02)
    w = pad * 2 + w_red + gap + w_thr
    ty = baseline - cap * 0.30
    tw = size * 0.05
    body = "".join(f'<path d="{d}" fill="{t["accent"]}"/>' for _, d, _, _ in red)
    body += woven(thr, t["fg"], ty, pad + w_red + gap * 0.25, w - pad * 0.35, tw, t["accent"])
    return svg_doc(round(w), round(h), body, None if transparent else t["bg"])


def stacked(font, theme, transparent=False):
    """Option B: stacked RED / THREADS, the thread runs between and off the edge."""
    t = THEMES[theme]
    size2 = 300
    cap2 = font.cap_height(size2)
    _, w_thr = font.layout("THREADS", 0, 0, size2, 0.03)
    # size RED so it spans the same width as THREADS
    _, w_red_unit = font.layout("RED", 0, 0, 100, 0.03)
    size1 = 100 * w_thr / w_red_unit
    cap1 = font.cap_height(size1)
    pad, lead = 110, size2 * 0.22
    w = w_thr + 2 * pad
    b1 = pad + cap1
    b2 = b1 + lead + cap2
    h = b2 + pad
    red, _ = font.layout("RED", pad, b1, size1, 0.03)
    thr, _ = font.layout("THREADS", pad, b2, size2, 0.03)
    tw = size2 * 0.04
    ty = b1 + lead / 2
    body = "".join(f'<path d="{d}" fill="{t["accent"]}"/>' for _, d, _, _ in red)
    body += "".join(f'<path d="{d}" fill="{t["fg"]}"/>' for _, d, _, _ in thr)
    # a single thread that drops from RED, runs between the lines and exits right
    body += (
        f'<path d="M{pad:.1f},{ty:.1f} H{w - pad * 0.3:.1f}" fill="none" '
        f'stroke="{t["accent"]}" stroke-width="{tw:.1f}" stroke-linecap="round"/>'
    )
    return svg_doc(round(w), round(h), body, None if transparent else t["bg"])


def icon(font, theme, variant="rt"):
    """Square profile icon, safe inside a circle crop (YouTube/IG/FB)."""
    t = THEMES[theme]
    S = 1080
    if variant == "rt":
        size = 760
        cap = font.cap_height(size)
        _, w_txt = font.layout("RT", 0, 0, size, 0.04)
        baseline = S / 2 + cap / 2
        letters, _ = font.layout("RT", (S - w_txt) / 2, baseline, size, 0.04)
        ty = baseline - cap * 0.27
        body = woven(letters, t["fg"], ty, -10, S + 10, 34, t["accent"])
    else:  # "r": single R with the thread, for the smallest sizes
        size = 860
        cap = font.cap_height(size)
        _, w_txt = font.layout("R", 0, 0, size, 0)
        baseline = S / 2 + cap / 2
        letters, _ = font.layout("R", (S - w_txt) / 2, baseline, size, 0)
        ty = baseline - cap * 0.27
        tw = 36
        x0, x1 = letters[0][2], letters[0][3]
        mid = x0 + (x1 - x0) * 0.5
        body = f'<line x1="-10" y1="{ty:.1f}" x2="{S + 10}" y2="{ty:.1f}" stroke="{t["accent"]}" stroke-width="{tw}"/>'
        body += f'<path d="{letters[0][1]}" fill="{t["fg"]}"/>'
        # thread runs behind the stem and in front of the leg
        g = tw * 0.45
        clip = knockout([(mid, ty - tw / 2 - g, x1 + g, ty + tw / 2 + g)], "weave-r")
        body = clip + body.replace(f'<path d="{letters[0][1]}"', f'<path clip-path="url(#weave-r)" d="{letters[0][1]}"')
        body += f'<line x1="{mid:.1f}" y1="{ty:.1f}" x2="{S + 10}" y2="{ty:.1f}" stroke="{t["accent"]}" stroke-width="{tw}"/>'
    return svg_doc(S, S, body, t["bg"])


def write(out, name, svg, png_width):
    os.makedirs(os.path.join(out, "svg"), exist_ok=True)
    os.makedirs(os.path.join(out, "png"), exist_ok=True)
    with open(os.path.join(out, "svg", name + ".svg"), "w") as f:
        f.write(svg)
    cairosvg.svg2png(bytestring=svg.encode(), write_to=os.path.join(out, "png", name + ".png"), output_width=png_width)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--font", required=True)
    ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), ".."))
    a = ap.parse_args()
    font = Font(a.font)
    for theme in THEMES:
        write(a.out, f"wordmark-{theme}", wordmark(font, theme), 2400)
        write(a.out, f"wordmark-{theme}-transparent", wordmark(font, theme, True), 2400)
        write(a.out, f"stacked-{theme}", stacked(font, theme), 1600)
        write(a.out, f"stacked-{theme}-transparent", stacked(font, theme, True), 1600)
        write(a.out, f"icon-rt-{theme}", icon(font, theme, "rt"), 1080)
        write(a.out, f"icon-r-{theme}", icon(font, theme, "r"), 1080)


if __name__ == "__main__":
    main()
