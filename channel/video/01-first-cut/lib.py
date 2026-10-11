import cairo, math, random
import numpy as np

W, H = 1920, 1080
FPS = 30


def hexc(h, a=1.0):
    return (int(h[1:3], 16) / 255, int(h[3:5], 16) / 255, int(h[5:7], 16) / 255, a)


RED = hexc('#C8102E'); PAPER = hexc('#F2E8D5'); INK = hexc('#1E1E24')
TEAL = hexc('#2F6F73'); GOLD = hexc('#D9A441'); GREY = hexc('#6B6B73')
PAPER2 = hexc('#E6D6B8'); EARTH = hexc('#CDB894'); WHITE = hexc('#FFFDF7')
SKY = hexc('#F6D9A8'); DUSK = hexc('#E9B872'); SHADOW = hexc('#3A3540')
SKINS = [hexc('#8D5524'), hexc('#C68642'), hexc('#E0AC69'), hexc('#6B3E1F'), hexc('#B5784A')]
SUITS = [TEAL, GREY, hexc('#5B4B8A'), hexc('#8A5A44'), hexc('#3F5E8C'), GOLD, hexc('#7A8450')]


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def seg(t, a, b):
    if b <= a:
        return 1.0 if t >= b else 0.0
    return clamp((t - a) / (b - a))


def ease(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def eo(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def lerp(a, b, x):
    return a + (b - a) * x


def mix(c1, c2, x):
    return tuple(lerp(a, b, x) for a, b in zip(c1, c2))


def setc(ctx, c, a=None):
    if a is None:
        ctx.set_source_rgba(*c)
    else:
        ctx.set_source_rgba(c[0], c[1], c[2], c[3] * a)


def rrect(ctx, x, y, w, h, r=0):
    if r <= 0:
        ctx.rectangle(x, y, w, h)
        return
    r = min(r, w / 2, h / 2)
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    ctx.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    ctx.close_path()


def box(ctx, x, y, w, h, fill=None, stroke=INK, lw=3, r=0, a=1.0):
    rrect(ctx, x, y, w, h, r)
    if fill is not None:
        setc(ctx, fill, a)
        if stroke is not None:
            ctx.fill_preserve()
        else:
            ctx.fill()
    if stroke is not None:
        setc(ctx, stroke, a)
        ctx.set_line_width(lw)
        ctx.stroke()


def circle(ctx, x, y, r, fill=None, stroke=INK, lw=3, a=1.0):
    ctx.new_sub_path()
    ctx.arc(x, y, r, 0, 2 * math.pi)
    if fill is not None:
        setc(ctx, fill, a)
        if stroke is not None:
            ctx.fill_preserve()
        else:
            ctx.fill()
    if stroke is not None:
        setc(ctx, stroke, a)
        ctx.set_line_width(lw)
        ctx.stroke()


def line(ctx, pts, col=INK, lw=3, a=1.0, dash=None):
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    setc(ctx, col, a)
    ctx.set_line_width(lw)
    if dash:
        ctx.set_dash(dash)
    ctx.stroke()
    ctx.set_dash([])


def font(ctx, size, face='Inter', bold=True, italic=False):
    ctx.select_font_face(face, cairo.FONT_SLANT_ITALIC if italic else cairo.FONT_SLANT_NORMAL,
                         cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size)


def text(ctx, s, x, y, size=32, col=INK, face='Inter', bold=True, italic=False, align='c', a=1.0, spacing=0):
    font(ctx, size, face, bold, italic)
    if spacing:
        s = (' ' * 0).join(s)
    ext = ctx.text_extents(s)
    if align == 'c':
        x0 = x - ext.x_advance / 2
    elif align == 'r':
        x0 = x - ext.x_advance
    else:
        x0 = x
    ctx.move_to(x0, y)
    setc(ctx, col, a)
    ctx.show_text(s)
    return ext.x_advance


def twidth(ctx, s, size, face='Inter', bold=True, italic=False):
    font(ctx, size, face, bold, italic)
    return ctx.text_extents(s).x_advance


def wrap(ctx, s, size, maxw, face='Inter', bold=True, italic=False):
    font(ctx, size, face, bold, italic)
    words = s.split()
    lines, cur = [], ''
    for w in words:
        trial = (cur + ' ' + w).strip()
        if ctx.text_extents(trial).x_advance > maxw and cur:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def para(ctx, s, x, y, size, maxw, col=INK, face='Inter', bold=True, italic=False, align='c', lh=1.25, a=1.0, reveal=1.0):
    ls = wrap(ctx, s, size, maxw, face, bold, italic)
    total = sum(len(l) for l in ls)
    shown = int(round(total * clamp(reveal)))
    for i, l in enumerate(ls):
        if shown <= 0:
            break
        part = l[:shown]
        shown -= len(l)
        text(ctx, part, x, y + i * size * lh, size, col, face, bold, italic, align, a)
    return len(ls) * size * lh


# ---------- paper texture ----------
_paper = None


def paper_surface():
    global _paper
    if _paper is None:
        rng = np.random.default_rng(7)
        n = rng.normal(0, 1, (H // 4, W // 4)).astype(np.float32)
        n = np.kron(n, np.ones((4, 4), np.float32))
        fine = rng.normal(0, 1, (H, W)).astype(np.float32)
        v = 0.6 * n + 0.4 * fine
        base = np.array([0xD5, 0xE8, 0xF2], np.float32)  # BGR
        img = np.clip(base[None, None, :] + v[..., None] * 4.0, 0, 255).astype(np.uint8)
        # vignette
        yy, xx = np.mgrid[0:H, 0:W]
        d = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
        vig = np.clip(1 - 0.10 * d ** 2, 0.85, 1)[..., None]
        img = (img * vig).astype(np.uint8)
        arr = np.zeros((H, W, 4), np.uint8)
        arr[..., :3] = img
        arr[..., 3] = 255
        surf = cairo.ImageSurface.create_for_data(arr, cairo.FORMAT_RGB24, W, H)
        _paper = (surf, arr)
    return _paper[0]


def bg(ctx):
    ctx.set_source_surface(paper_surface(), 0, 0)
    ctx.paint()


# ---------- smooth thread ----------
def catmull(pts, n=24):
    out = []
    P = [pts[0]] + list(pts) + [pts[-1]]
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            out.append((x, y))
    out.append(pts[-1])
    return out


def partial(pts, prog):
    if prog >= 1:
        return pts
    if prog <= 0:
        return pts[:1]
    L = [0.0]
    for a, b in zip(pts, pts[1:]):
        L.append(L[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    target = L[-1] * prog
    out = [pts[0]]
    for i in range(1, len(pts)):
        if L[i] >= target:
            a, b = pts[i - 1], pts[i]
            f = (target - L[i - 1]) / max(1e-6, L[i] - L[i - 1])
            out.append((lerp(a[0], b[0], f), lerp(a[1], b[1], f)))
            break
        out.append(pts[i])
    return out


def thread(ctx, pts, prog=1.0, lw=6, col=RED, a=1.0, smooth=True):
    p = catmull(pts) if smooth and len(pts) > 2 else pts
    p = partial(p, prog)
    if len(p) < 2:
        return p[-1]
    line(ctx, p, col, lw, a)
    return p[-1]


def knot(ctx, x, y, r=18, a=1.0, col=RED):
    ctx.set_line_width(5)
    setc(ctx, col, a)
    for k in range(3):
        ang = k * 2 * math.pi / 3
        ctx.new_sub_path()
        ctx.arc(x + math.cos(ang) * r * 0.45, y + math.sin(ang) * r * 0.45, r * 0.55, 0, 2 * math.pi)
        ctx.stroke()
    circle(ctx, x, y, r * 0.22, col, None, a=a)


# ---------- people ----------
def person(ctx, x, y, s=1.0, body=TEAL, skin=None, hair=INK, walk=None, arms='down', beard=False, a=1.0, carry=False, face=0):
    """y is the feet line."""
    if skin is None:
        skin = SKINS[face % len(SKINS)]
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    sw = 0 if walk is None else math.sin(walk) * 9
    bob = 0 if walk is None else abs(math.cos(walk)) * 2
    ctx.translate(0, -bob)
    # legs
    line(ctx, [(-8, -40), (-8 + sw, 0)], INK, 7, a)
    line(ctx, [(8, -40), (8 - sw, 0)], INK, 7, a)
    # body
    box(ctx, -22, -98, 44, 62, body, INK, 3, 14, a)
    # arms
    if arms == 'up':
        line(ctx, [(-20, -88), (-34, -122)], INK, 6, a)
        line(ctx, [(20, -88), (34, -122)], INK, 6, a)
    elif arms == 'carry' or carry:
        line(ctx, [(-20, -86), (-6, -112)], INK, 6, a)
        line(ctx, [(20, -86), (6, -112)], INK, 6, a)
    elif arms == 'point':
        line(ctx, [(-20, -86), (-26, -50)], INK, 6, a)
        line(ctx, [(20, -86), (48, -100)], INK, 6, a)
    else:
        line(ctx, [(-20, -86), (-26 - sw * 0.4, -50)], INK, 6, a)
        line(ctx, [(20, -86), (26 + sw * 0.4, -50)], INK, 6, a)
    # head
    circle(ctx, 0, -116, 17, skin, INK, 3, a)
    # hair
    ctx.new_sub_path()
    ctx.arc(0, -116, 17, math.pi * 1.12, math.pi * 1.88)
    ctx.close_path()
    setc(ctx, hair, a)
    ctx.fill()
    if beard:
        ctx.new_sub_path()
        ctx.arc(0, -112, 16, math.pi * 0.05, math.pi * 0.95)
        ctx.close_path()
        setc(ctx, hair, a)
        ctx.fill()
    ctx.restore()


def brick(ctx, x, y, s=1.0, a=1.0):
    box(ctx, x - 13 * s, y - 9 * s, 26 * s, 18 * s, GOLD, INK, 2.5, 3, a)


def padlock(ctx, x, y, s=1.0, a=1.0, col=INK):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.new_sub_path()
    ctx.arc(0, -10, 13, math.pi, 2 * math.pi)
    setc(ctx, col, a)
    ctx.set_line_width(6)
    ctx.stroke()
    box(ctx, -20, -10, 40, 32, col, None, 0, 5, a)
    circle(ctx, 0, 4, 4, GOLD, None, a=a)
    ctx.restore()


# ---------- camera ----------
def camera(ctx, cx=960, cy=540, z=1.0):
    ctx.translate(W / 2, H / 2)
    ctx.scale(z, z)
    ctx.translate(-cx, -cy)
