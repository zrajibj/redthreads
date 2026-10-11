from building import *


def quote_card(ctx, q, src, x, y, w, prog, a=1.0, size=44):
    """Hand-lettered quote along the red thread."""
    if prog <= 0:
        return
    al = a * ease(prog * 4)
    ls = wrap(ctx, q, size, w, 'Caladea', True, True)
    hgt = len(ls) * size * 1.3 + 70
    box(ctx, x - 30, y - size - 20, w + 60, hgt, hexc('#FFFDF7', 0.92), None, a=al, r=10)
    thread(ctx, [(x - 30, y - size - 20), (x + w + 30, y - size - 20)], ease(prog * 2), 6, RED, al, False)
    para(ctx, q, x, y, size, w, INK, 'Caladea', True, True, 'l', 1.3, al, reveal=eo(prog * 1.6))
    text(ctx, src, x, y + len(ls) * size * 1.3 + 8, 24, GREY, 'Inter', True, False, 'l', al * seg(prog, 0.5, 0.7))


def label(ctx, s, x, y, size=34, col=RED, a=1.0, align='c'):
    text(ctx, s, x, y, size, col, 'Inter', True, False, align, a)


def city_back(ctx, a=1.0, sky=None):
    rnd = random.Random(11)
    x = -40
    while x < W + 40:
        w = rnd.randint(120, 220); h = rnd.randint(260, 520)
        col = [hexc('#C9BBA0'), hexc('#B7A98E'), hexc('#D4C6A9')][rnd.randint(0, 2)]
        box(ctx, x, 760 - h, w, h, col, None, a=a)
        for wy in range(760 - h + 30, 740, 56):
            for wx in range(x + 20, x + w - 30, 44):
                box(ctx, wx, wy, 20, 28, hexc('#E9DEC6'), None, a=a)
        x += w + rnd.randint(4, 30)
    box(ctx, 0, 760, W, 320, hexc('#A89A82'), None, a=a)
    line(ctx, [(0, 760), (W, 760)], INK, 4, a)


POSTER_COLS = [TEAL, GOLD, hexc('#5B4B8A'), hexc('#3F5E8C'), hexc('#7A8450'), hexc('#8A5A44')]
POSTER_WORDS = ['A NEW DAWN', 'HOPE', 'CHANGE NOW', 'A NEW DAWN', 'TOMORROW', 'HOPE']


def poster(ctx, x, y, k, a=1.0, drop=1.0):
    col = POSTER_COLS[k % len(POSTER_COLS)]
    hh = 230 * drop
    ctx.save()
    rrect(ctx, x, y, 170, hh, 0)
    ctx.clip()
    box(ctx, x, y, 170, 230, col, INK, 3, 0, a)
    circle(ctx, x + 85, y + 82, 40, SKINS[k % 5], INK, 3, a)
    ctx.new_sub_path(); ctx.arc(x + 85, y + 82, 40, math.pi * 1.05, math.pi * 1.95); ctx.close_path()
    setc(ctx, [INK, GREY, WHITE][k % 3], a); ctx.fill()
    box(ctx, x + 45, y + 124, 80, 30, WHITE, None, a=a * 0.9)
    text(ctx, POSTER_WORDS[k % len(POSTER_WORDS)], x + 85, y + 200, 22, WHITE, a=a)
    ctx.restore()


def poster_wall(ctx, t, x0, y0, n=3, start=0, rate=1.6, a=1.0):
    for i in range(n):
        x = x0 + i * 200
        layers = int(max(0, (t - i * 0.4) / rate)) + 1
        frac = ((t - i * 0.4) / rate) % 1 if t - i * 0.4 > 0 else 0
        base = start + i * 2 + layers - 1
        poster(ctx, x, y0, base, a)
        if t - i * 0.4 > 0:
            poster(ctx, x, y0, base + 1, a, drop=eo(frac * 2.5))


def tv(ctx, x, y, t, a=1.0, ticker='NEW PROMISES'):
    box(ctx, x, y, 300, 190, SHADOW, INK, 4, 12, a)
    box(ctx, x + 14, y + 14, 272, 146, hexc('#9CC5C2'), None, a=a)
    circle(ctx, x + 150, y + 70, 30, SKINS[1], INK, 3, a)
    box(ctx, x + 112, y + 100, 76, 60, TEAL, None, a=a)
    mo = abs(math.sin(t * 9)) * 9
    box(ctx, x + 140, y + 80, 20, 2 + mo, INK, None, a=a)
    ctx.save(); rrect(ctx, x + 14, y + 132, 272, 28); ctx.clip()
    box(ctx, x + 14, y + 132, 272, 28, RED, None, a=a)
    off = (t * 90) % 420
    text(ctx, ticker + '  •  ' + ticker, x + 290 - off, y + 154, 18, WHITE, align='l', a=a)
    ctx.restore()
    line(ctx, [(x + 150, y + 190), (x + 150, y + 240)], INK, 6, a)
    line(ctx, [(x + 100, y + 240), (x + 200, y + 240)], INK, 6, a)


def door_closeup(ctx, t, old, new, prog, a=1.0):
    box(ctx, 0, 0, W, H, hexc('#E9DEC6'), None, a=a)
    for i in range(0, W, 120):
        line(ctx, [(i, 0), (i, H)], hexc('#DCCFB3'), 3, a)
    box(ctx, 640, 120, 640, 960, hexc('#A7744C'), INK, 6, 6, a)
    box(ctx, 700, 180, 520, 360, None, hexc('#8A5A3A'), 5, 4, a)
    box(ctx, 700, 600, 520, 420, None, hexc('#8A5A3A'), 5, 4, a)
    circle(ctx, 1220, 640, 18, GOLD, INK, 3, a)
    if prog < 0.5:
        q = ease(prog / 0.5)
        # screwdriver turning the screw, then the plate swings off
        nameplate(ctx, 960, 300 + 700 * q * q, old, a, tilt=q * 1.1, s=4.0)
        if q < 0.3:
            ang = t * 8
            line(ctx, [(960 + 144, 300), (960 + 144 + 130 * math.cos(-0.6), 300 + 130 * math.sin(-0.6) - 40)], hexc('#7A8450'), 18, a)
            line(ctx, [(960 + 144, 300), (960 + 144 + 70 * math.cos(-0.6), 300 + 70 * math.sin(-0.6) - 20)], GREY, 8, a)
    else:
        q = eo((prog - 0.5) / 0.5)
        nameplate(ctx, 960 + 900 * (1 - q), 300, new, a, s=4.0)


def factory_dawn(ctx, t, a=1.0):
    # sky
    grad = cairo.LinearGradient(0, 0, 0, 760)
    grad.add_color_stop_rgba(0, 0.96, 0.82, 0.62, a)
    grad.add_color_stop_rgba(1, 0.98, 0.92, 0.80, a)
    ctx.rectangle(0, 0, W, 760); ctx.set_source(grad); ctx.fill()
    circle(ctx, 1500, 640, 110, hexc('#F3B85C'), None, a=a)
    box(ctx, 0, 760, W, 320, hexc('#A89A82'), None, a=a)
    # factory
    box(ctx, 260, 360, 900, 400, GREY, INK, 5, 0, a)
    for i in range(5):
        x = 260 + i * 180
        ctx.move_to(x, 360); ctx.line_to(x + 90, 290); ctx.line_to(x + 180, 360); ctx.close_path()
        setc(ctx, hexc('#8E8E96'), a); ctx.fill_preserve(); setc(ctx, INK, a); ctx.set_line_width(4); ctx.stroke()
    box(ctx, 1040, 160, 60, 200, hexc('#8E8E96'), INK, 4, 0, a)
    for k in range(4):
        sy = 140 - ((t * 25 + k * 40) % 160)
        circle(ctx, 1070 + k * 12 + math.sin(t + k) * 8, sy, 22 + k * 4, hexc('#D8D2C8'), None, a=a * 0.8 * (1 - (140 - sy) / 200))
    for i in range(6):
        box(ctx, 300 + i * 140, 430, 80, 60, hexc('#C9D6D5'), INK, 3, 2, a)
    # gate
    box(ctx, 600, 560, 260, 200, SHADOW, INK, 4, 0, a)
    for i in range(7):
        line(ctx, [(620 + i * 36, 570), (620 + i * 36, 760)], GREY, 4, a)
    # time clock with red thread
    box(ctx, 900, 600, 70, 100, hexc('#8A5A44'), INK, 3, 4, a)
    circle(ctx, 935, 630, 20, WHITE, INK, 2.5, a)
    line(ctx, [(935, 630), (935 + 14 * math.cos(t), 630 + 14 * math.sin(t))], INK, 3, a)
    box(ctx, 915, 662, 40, 26, WHITE, INK, 2, 2, a)
    thread(ctx, [(935, 690), (1000, 720), (1100, 700), (1300, 760), (1500, 740), (1700, 800), (1960, 790)], 1.0, 6, RED, a)
    # queue of workers
    for i in range(7):
        x = 1700 - ((t * 60 + i * 120) % 1000)
        fade = seg(x, 700, 800)
        person(ctx, x, 800, 0.95, [TEAL, hexc('#7A8450'), GREY, hexc('#5B4B8A')][i % 4], SKINS[i % 5], INK, walk=t * 6 + i, a=a * fade)


def sewing_floor(ctx, t, x0, y0, w, a=1.0):
    box(ctx, x0, y0, w, 760, hexc('#DCCFB3'), None, a=a)
    for r in range(2):
        for i in range(3):
            x = x0 + 120 + i * 260; y = y0 + 330 + r * 300
            person(ctx, x, y + 10, 0.9, [TEAL, hexc('#5B4B8A'), GOLD][(i + r) % 3], SKINS[(i + r * 2) % 5], INK, a=a)
            box(ctx, x - 70, y - 70, 170, 46, GREY, INK, 3, 4, a)
            ny = abs(math.sin(t * 12 + i + r)) * 10
            line(ctx, [(x + 60, y - 110), (x + 60, y - 70 - 4 + ny)], INK, 3, a)
            box(ctx, x - 20, y - 80, 60, 12, [RED, TEAL, GOLD][i], None, a=a)
            box(ctx, x - 110, y - 24, 260, 18, hexc('#8A5A44'), INK, 3, 2, a)


# ---------------- scenes ----------------
def s1(ctx, t, d, c, T):
    bg(ctx)
    cut = c[2]
    if t < cut + 0.5:
        a = 1 - seg(t, cut, cut + 0.5)
        if t < 3.4:
            door_closeup(ctx, t, 0, 1, seg(t, 0.2, 3.2), a)
        else:
            z = lerp(1.6, 1.0, ease(seg(t, 3.4, 5.0)))
            ctx.save(); camera(ctx, lerp(1450, 960, ease(seg(t, 3.4, 5.0))), 540, z)
            city_back(ctx, a)
            poster_wall(ctx, t - 3.6, 160, 430, 3, 0, 1.7, a)
            tv(ctx, 860, 470, t, a)
            # office door at street level
            box(ctx, 1320, 380, 170, 380, hexc('#A7744C'), INK, 4, 4, a)
            nameplate(ctx, 1405, 450, 1, a, s=1.2)
            box(ctx, 1290, 350, 230, 30, GREY, INK, 3, 0, a)
            for i in range(3):
                person(ctx, 520 + i * 360 + math.sin(t * 0.7 + i) * 30, 860, 1.0, SUITS[i + 1], SKINS[i], INK, walk=t * 5 + i, a=a)
            ctx.restore()
    if t > cut:
        a = seg(t, cut, cut + 0.5)
        factory_dawn(ctx, t, a)


def s2(ctx, t, d, c, T):
    bg(ctx)
    ctx.save(); rrect(ctx, 0, 0, W / 2, H); ctx.clip()
    city_back(ctx)
    poster_wall(ctx, t + 4, 120, 420, 3, 6, 0.9)
    ctx.restore()
    ctx.save(); rrect(ctx, W / 2, 0, W / 2, H); ctx.clip()
    sewing_floor(ctx, t, W / 2, 160, W / 2)
    box(ctx, W / 2, 0, W / 2, 160, hexc('#CDBF9F'), None)
    ctx.restore()
    thread(ctx, [(960, -10), (950, 300), (970, 700), (960, 1090)], ease(t / 0.8), 8)
    a1 = ease(seg(t, 0.3, 0.9)); a2 = ease(seg(t, c[1], c[1] + 0.6))
    box(ctx, 240, 70, 480, 80, WHITE, INK, 3, 12, a1)
    label(ctx, 'CHANGED', 480, 125, 44, TEAL, a1)
    box(ctx, 1200, 70, 480, 80, WHITE, INK, 3, 12, a2)
    label(ctx, 'NOT CHANGED', 1440, 125, 44, RED, a2)


def stall(ctx, x, y, price, a=1.0):
    box(ctx, x, y, 520, 40, RED, INK, 4, 0, a)
    for i in range(6):
        box(ctx, x + i * 86, y + 40, 86, 26, [RED, WHITE][i % 2], INK, 2, 0, a)
    box(ctx, x + 20, y + 200, 480, 120, hexc('#8A5A44'), INK, 4, 3, a)
    for i in range(5):
        circle(ctx, x + 80 + i * 90, y + 190, 34, [GOLD, hexc('#7A8450'), hexc('#C8102E'), GOLD, WHITE][i], INK, 3, a)
    box(ctx, x + 330, y + 80, 170, 90, SHADOW, INK, 3, 4, a)
    text(ctx, 'RICE', x + 415, y + 116, 26, WHITE, a=a)
    text(ctx, str(price), x + 415, y + 156, 32, GOLD, a=a)


def globe(ctx, x, y, r, t, a=1.0):
    circle(ctx, x, y, r, hexc('#9CC5C2'), INK, 5, a)
    ctx.save(); ctx.new_sub_path(); ctx.arc(x, y, r, 0, 2 * math.pi); ctx.clip()
    for k in range(-3, 4):
        off = ((t * 40 + k * 60) % 360) - 180
        ex = r * math.cos(math.radians(off * 0.5))
        ctx.save(); ctx.translate(x + r * math.sin(math.radians(off * 0.5)), y); ctx.scale(max(0.05, abs(math.cos(math.radians(off * 0.5)))), 1)
        ctx.new_sub_path(); ctx.arc(0, 0, r * 0.02 + 1, 0, 2 * math.pi); ctx.restore()
        line(ctx, [(x + r * math.sin(math.radians(off * 0.5)), y - r), (x + r * math.sin(math.radians(off * 0.5)), y + r)], TEAL, 2, a * 0.6)
    for k in (-2, -1, 0, 1, 2):
        yy = y + k * r * 0.38
        line(ctx, [(x - r, yy), (x + r, yy)], TEAL, 2, a * 0.6)
    rnd = random.Random(5)
    for k in range(7):
        bx = ((rnd.uniform(-1, 1) * r + t * 40 + k * 130) % (2.4 * r)) - 1.2 * r
        circle(ctx, x + bx, y + rnd.uniform(-0.6, 0.6) * r, rnd.uniform(0.18, 0.32) * r, hexc('#7A8450'), None, a=a * 0.85)
    ctx.restore()
    circle(ctx, x, y, r, None, INK, 5, a)


def s3(ctx, t, d, c, T):
    bg(ctx)
    q = c[2]
    if t < c[1] + 0.4:
        a = 1 - seg(t, c[1], c[1] + 0.4)
        globe(ctx, 960, 500, 300, t, a)
        for i, (px, py) in enumerate(((800, 380), (1080, 460), (900, 620), (1150, 330), (980, 520))):
            pa = a * ease(seg(t, 0.5 + i * 0.6, 0.9 + i * 0.6))
            circle(ctx, px, py - 30 * (1 - pa), 14, RED, INK, 3, pa)
    if c[1] < t < q + 0.4:
        a = seg(t, c[1], c[1] + 0.4) * (1 - seg(t, q, q + 0.4))
        lt = t - c[1]
        decade = int(lt / 2.0)
        years = ['1970s', '1980s', '1990s', '2000s', '2010s', '2020s']
        yi = min(decade, len(years) - 1)
        box(ctx, 160, 140, 300, 340, WHITE, INK, 5, 8, a)
        box(ctx, 160, 140, 300, 80, RED, INK, 5, 8, a)
        flip = (lt % 2.0)
        if flip < 0.3 and decade > 0 and yi == decade:
            ctx.save(); ctx.translate(310, 220); ctx.scale(1, 1 - flip / 0.3); text(ctx, years[yi - 1], 0, 150, 76, INK, a=a); ctx.restore()
        else:
            text(ctx, years[yi], 310, 370, 76, INK, a=a)
        stall(ctx, 700, 300, [30, 45, 60, 80, 110, 150][yi], a)
        for i in range(3):
            person(ctx, 1380 + i * 150, 820, 1.25, [TEAL, GOLD, hexc('#5B4B8A')][i], SKINS[i * 2 % 5], INK, a=a)
            # worried brows
            ctx.save(); ctx.translate(1380 + i * 150, 820); ctx.scale(1.25, 1.25)
            line(ctx, [(-9, -124), (-3, -121)], INK, 2.5, a); line(ctx, [(9, -124), (3, -121)], INK, 2.5, a)
            ctx.new_sub_path(); ctx.arc(0, -104, 5, math.pi * 1.15, math.pi * 1.85); setc(ctx, INK, a); ctx.set_line_width(2.5); ctx.stroke()
            ctx.restore()
        words = ['CORRUPTION', 'PRICES', 'WAGES']
        for i, w in enumerate(words):
            wa = a * ease(seg(lt, 3.0 + i * 1.2, 3.5 + i * 1.2))
            box(ctx, 700 + i * 180, 700, 170, 54, WHITE, RED, 3, 27, wa)
            text(ctx, w, 785 + i * 180, 736, 22, RED, a=wa)
    if t > q:
        a = seg(t, q, q + 0.5)
        para(ctx, 'Why does changing the government change so little?', 960, 430, 80, 1400, INK, 'Caladea', True, False, 'c', 1.15, a)
        thread(ctx, [(380, 560), (800, 575), (1200, 555), (1540, 570)], ease(seg(t, q + 0.3, q + 1.5)), 7, RED, a)
        u = ease(seg(t, c[3], c[3] + 0.8))
        if u > 0:
            text(ctx, '...and what would it take to change the thing underneath?', 960, 680, 40, GREY, 'Caladea', True, True, 'c', u)
            thread(ctx, [(960, 700), (960, 1100)], u, 6, RED, u)


def s4(ctx, t, d, c, T):
    bg(ctx)
    ctx.save(); camera(ctx, 960, 520, 1.0)
    p = ease(seg(t, 0.2, d - 0.3))
    pts = outline_path()
    # draw the outline in ink faintly behind the thread
    end = thread(ctx, pts, p, 8, RED, 1.0, smooth=False)
    circle(ctx, end[0], end[1], 9, RED, None)
    ctx.restore()


def s5(ctx, t, d, c, T):
    bg(ctx)
    ctx.save(); camera(ctx, 960, 520, 1.0)
    reveal = [ease(seg(t, 0.4 + i * 1.3, 1.0 + i * 1.3)) for i in range(5)]
    st = {'reveal': reveal, 'found': 0.0, 'labels': 1.0, 'workers': False, 'flabels': 0}
    sw = c[1]
    if t > sw:
        k = int((t - sw) / 1.4)
        p = ((t - sw) % 1.4) / 0.9
        st['swap'] = (k, k + 1, clamp(p))
        st['leader'] = k + (1 if p >= 1 else 0)
    building(ctx, T, st)
    thread(ctx, outline_path(), 1.0, 5, RED, 0.35, smooth=False)
    if t > sw:
        a = ease(seg(t, sw, sw + 0.5))
        box(ctx, 1400, 150, 440, 120, WHITE, INK, 3, 14, a)
        text(ctx, 'WHERE THE FACES', 1620, 200, 30, RED, a=a)
        text(ctx, 'CHANGE', 1620, 244, 30, RED, a=a)
        thread(ctx, [(1400, 210), (1300, 208)], a, 5, RED, a, False)
    ctx.restore()


def s6(ctx, t, d, c, T):
    bg(ctx)
    m = ease(seg(t, 0.5, 2.6))
    ctx.save(); camera(ctx, 960, lerp(520, 760, m), lerp(1.0, 1.55, m))
    fa = ease(seg(t, 2.0, 3.0))
    st = {'found': fa, 'flabels': 1.0, 'workers': t > 9.0, 'stack': 4 + int(max(0, t - 9) / 2.3)}
    building(ctx, T, st)
    ctx.restore()
    tags = [('WHO OWNS?', c[1] + 1.2, 330, 140), ('WHO WORKS?', c[1] + 5.5, 960, 140), ('WHO KEEPS THE SURPLUS?', c[1] + 8.0, 1560, 140)]
    for s, t0, x, y in tags:
        a = ease(seg(t, t0, t0 + 0.5))
        if a > 0:
            w = twidth(ctx, s, 40) + 60
            box(ctx, x - w / 2, y - 52, w, 72, WHITE, RED, 4, 36, a)
            label(ctx, s, x, y, 40, RED, a)


def two_men(ctx, t, a=1.0):
    # tavern table with two bearded figures sketching the building
    box(ctx, 120, 640, 760, 40, hexc('#8A5A44'), INK, 4, 4, a)
    line(ctx, [(200, 680), (200, 900)], INK, 10, a); line(ctx, [(800, 680), (800, 900)], INK, 10, a)
    person(ctx, 260, 760, 1.6, GREY, SKINS[2], INK, beard=True, a=a)
    person(ctx, 740, 760, 1.6, hexc('#3F5E8C'), SKINS[2], hexc('#8A5A44'), beard=True, a=a, arms='point')
    box(ctx, 380, 590, 240, 56, WHITE, INK, 3, 2, a)
    p = ease(seg(t, 0.4, 4.0))
    pts = [(420, 640), (420, 606), (500, 596), (580, 606), (580, 640)]
    thread(ctx, pts, p, 4, RED, a, False)
    line(ctx, [(400, 640), (600, 640)], INK, 3, a)
    # mugs
    box(ctx, 160, 600, 40, 44, GOLD, INK, 3, 4, a); box(ctx, 820, 600, 40, 44, GOLD, INK, 3, 4, a)


def base_diagram(ctx, x, y, a=1.0, prog=1.0):
    p1 = ease(seg(prog, 0, 0.4)); p2 = ease(seg(prog, 0.4, 0.9))
    box(ctx, x - 300, y, 600, 120, PAPER2, INK, 4, 4, a * p1)
    text(ctx, 'ECONOMIC BASE', x, y + 72, 40, INK, a=a * p1)
    ctx.move_to(x - 250, y); ctx.line_to(x - 250, y - 200 * p2); ctx.line_to(x, y - 280 * p2); ctx.line_to(x + 250, y - 200 * p2); ctx.line_to(x + 250, y); ctx.close_path()
    setc(ctx, WHITE, a * p2); ctx.fill_preserve(); setc(ctx, INK, a * p2); ctx.set_line_width(4); ctx.stroke()
    text(ctx, 'LAW & POLITICS', x, y - 100, 36, GREY, a=a * p2)
    thread(ctx, [(x - 330, y + 140), (x, y + 125), (x + 330, y + 140)], p1, 6, RED, a * p1)


def s7(ctx, t, d, c, T):
    bg(ctx)
    two_men(ctx, t)
    text(ctx, 'MARX', 260, 520, 30, GREY, a=ease(seg(t, 0.5, 1)))
    text(ctx, 'ENGELS', 740, 520, 30, GREY, a=ease(seg(t, c[1], c[1] + 0.6)))
    a1 = 1 - seg(t, c[2] - 0.6, c[2])
    base_diagram(ctx, 1380, 640, a1, seg(t, 1.5, 7.0))
    if t > c[2] - 0.6:
        quote_card(ctx, '"The ultimate causes of all social changes and political revolutions are to be sought, not in men\'s brains... but in changes in the modes of production and exchange."',
                   'Engels, Socialism: Utopian and Scientific, ch. 3', 1000, 300, 800, seg(t, c[2] - 0.4, d - 2), 1.0, 42)


def s8(ctx, t, d, c, T):
    bg(ctx)
    ctx.save(); camera(ctx, 960, 560, 0.9)
    p = ease(seg(t, 4.0, 6.5))
    st = {'glow': ease(seg(t, 6.3, 7.0)), 'stack': 10}
    building(ctx, T, st)
    # magnifying glass
    if t < 4.0:
        gx = lerp(620, 1300, (math.sin(t * 1.2 - 1.6) + 1) / 2); gy = lerp(210, 590, seg(t, 0, 4.0))
    else:
        gx = lerp(1300, 1330, p); gy = lerp(590, 790, p)
    circle(ctx, gx, gy, 90, hexc('#FFFFFF', 0.25), INK, 10)
    line(ctx, [(gx + 64, gy + 64), (gx + 150, gy + 150)], hexc('#8A5A44'), 22)
    if t < 4.0:
        text(ctx, '?', gx, gy + 24, 70, GREY, a=0.8)
    ctx.restore()


def s9(ctx, t, d, c, T):
    bg(ctx)
    pan = ease(seg(t, c[2], c[2] + 2.5))
    ctx.save(); camera(ctx, lerp(1000, 960, pan), lerp(230, 740, pan), lerp(2.1, 1.4, pan))
    st = {'stack': 9 + int(max(0, t - c[2]) / 2.0), 'glow': ease(seg(t, c[5], c[5] + 0.8))}
    if t < c[2] + 1:
        st['plate'] = (3, 4, seg(t, 0.6, 3.4))
        st['swap'] = (3, 4, seg(t, 2.6, 4.4))
        st['leader'] = 4 if t > 4.4 else 3
    else:
        st['leader'] = 4
    building(ctx, T, st)
    ctx.restore()
    tags = [('SAME OWNERS', c[3]), ('SAME WORKERS', c[4]), ('SAME LOCKED ROOM', c[5])]
    for i, (s, t0) in enumerate(tags):
        a = ease(seg(t, t0, t0 + 0.5))
        if a > 0:
            box(ctx, 80 + i * 600, 120, 560, 84, WHITE, RED, 4, 42, a)
            label(ctx, s, 360 + i * 600, 178, 40, RED, a)


def boardroom(ctx, t, rot, a=1.0):
    box(ctx, 0, 720, W, 360, hexc('#CDBF9F'), None, a=a)
    seats = [(560, 600), (760, 600), (960, 600), (1160, 600), (1360, 600)]
    for i, (x, y) in enumerate(seats):
        k = int(rot) + i
        box(ctx, x - 50, y - 160, 100, 170, hexc('#5A3A22'), INK, 3, 14, a)
        person(ctx, x, y + 40, 1.15, SUITS[k % len(SUITS)], SKINS[k % 5], [INK, GREY, hexc('#5A3A22'), WHITE][k % 4], a=a)
    ctx.save(); ctx.translate(960, 830); ctx.scale(1, 0.32)
    ctx.new_sub_path(); ctx.arc(0, 0, 640, 0, 2 * math.pi); setc(ctx, hexc('#8A5A44'), a); ctx.fill_preserve(); setc(ctx, INK, a); ctx.set_line_width(5); ctx.stroke()
    ctx.restore()
    # agenda
    ctx.save(); ctx.translate(960, 830); ctx.rotate(-0.05)
    box(ctx, -110, -60, 220, 120, WHITE, INK, 3, 3, a)
    text(ctx, 'AGENDA', 0, -24, 28, INK, a=a)
    for k in range(3):
        box(ctx, -80, -6 + k * 20, 160 - k * 30, 6, GREY, None, a=a)
    ctx.restore()


def s10(ctx, t, d, c, T):
    bg(ctx)
    rot = 0 if t < c[2] else (t - c[2]) / 1.0
    rot = rot + 0.0
    boardroom(ctx, t, int(rot) * 2 if t > c[2] else 0)
    if t < c[2]:
        quote_card(ctx, '"The executive of the modern State is but a committee for managing the common affairs of the whole bourgeoisie."',
                   'Marx & Engels, The Communist Manifesto, 1848', 360, 150, 1200, seg(t, c[1] - 0.3, c[2] - 1), 1 - seg(t, c[2] - 0.5, c[2]), 46)
    else:
        a = ease(seg(t, c[2] + 1.2, c[2] + 1.8))
        thread(ctx, [(1300, 200), (1150, 330), (1060, 640)], a, 6, RED, a)
        box(ctx, 1000, 120, 600, 90, WHITE, RED, 4, 45, a)
        label(ctx, 'SAME JOB DESCRIPTION', 1300, 180, 38, RED, a)


def s11(ctx, t, d, c, T):
    bg(ctx)
    # ballot box
    bx, by = 760, 560
    box(ctx, bx - 160, by, 320, 280, WHITE, INK, 5, 6)
    box(ctx, bx - 60, by - 6, 120, 14, INK, None)
    text(ctx, 'VOTE', bx, by + 160, 54, GREY)
    for i in range(4):
        x = 160 + i * 110
        person(ctx, x, 920, 1.2, SUITS[i + 1], SKINS[i], INK)
        ph = ((t + i * 0.9) % 3.6) / 3.6
        if ph < 0.5:
            px = lerp(x + 20, bx, ease(ph * 2)); py = lerp(760, by - 30, ease(ph * 2)) - math.sin(ph * 2 * math.pi) * 80
            box(ctx, px - 22, py - 14, 44, 28, WHITE, INK, 2.5, 2)
    # threads from the slot to purses
    p = ease(seg(t, 1.0, 4.0))
    purses = [(1500, 300), (1620, 520), (1480, 740)]
    for i, (x, y) in enumerate(purses):
        thread(ctx, [(bx, by), (bx + 220, by - 140 + i * 60), (1100, y + 40), (x - 60, y)], p, 5)
        a = ease(seg(t, 3.0 + i * 0.3, 3.6 + i * 0.3))
        # hand + purse
        circle(ctx, x - 40, y - 10, 30, SKINS[(i + 2) % 5], INK, 3, a)
        line(ctx, [(x - 10, y - 10), (x + 140, y - 10)], SUITS[i + 2], 40, a)
        ctx.new_sub_path(); ctx.arc(x - 40, y + 50, 46, 0, 2 * math.pi); setc(ctx, GOLD, a); ctx.fill_preserve(); setc(ctx, INK, a); ctx.set_line_width(3); ctx.stroke()
        text(ctx, '$', x - 40, y + 66, 44, INK, a=a)
    if c[1] - 0.3 < t < c[2]:
        quote_card(ctx, '"...an oligarchy of private capital the enormous power of which cannot be effectively checked even by a democratically organized political society."',
                   'Albert Einstein, "Why Socialism?", Monthly Review, 1949', 120, 140, 900, seg(t, c[1] - 0.3, c[2] - 2.5), 1 - seg(t, c[2] - 0.5, c[2]), 40)
    if t > c[2]:
        a = ease(seg(t, c[2], c[2] + 0.6))
        box(ctx, 200, 90, 1100, 100, WHITE, RED, 4, 50, a)
        label(ctx, 'THE MONEY HAS OFTEN CHOSEN FIRST', 750, 156, 44, RED, a)


def trophy(ctx, x, y, s, a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    box(ctx, -170, 60, 340, 220, hexc('#8E8E96'), INK, 5, 4, a)
    box(ctx, -210, 40, 420, 30, GREY, INK, 4, 3, a)
    box(ctx, -150, -150, 300, 190, GOLD, INK, 5, 4, a)
    ctx.move_to(-180, -150); ctx.line_to(0, -230); ctx.line_to(180, -150); ctx.close_path()
    setc(ctx, hexc('#E8BC5A'), a); ctx.fill_preserve(); setc(ctx, INK, a); ctx.set_line_width(5); ctx.stroke()
    box(ctx, -40, -80, 80, 120, hexc('#B8862E'), INK, 4, 3, a)
    nameplate(ctx, 0, -110, 2, a, s=0.9)
    for k in range(3):
        circle(ctx, -110 + k * 110, -200 + (k % 2) * 30, 6, WHITE, None, a=a * 0.8)
    ctx.restore()


def s12(ctx, t, d, c, T):
    bg(ctx)
    if t < c[3]:
        a = 1 - seg(t, c[3] - 0.4, c[3])
        da = ease(seg(t, c[1], c[1] + 0.5)); sa = ease(seg(t, c[2], c[2] + 0.5))
        box(ctx, 360, 380, 520, 160, WHITE, INK, 4, 20, a * da)
        text(ctx, 'DISEASE', 620, 486, 80, INK, a=a * da)
        if sa > 0:
            line(ctx, [(390, 470), (390 + 460 * sa, 450)], RED, 12, a)
        box(ctx, 1040, 380, 520, 160, WHITE, RED, 6, 20, a * sa)
        text(ctx, 'SYMPTOM', 1300, 486, 80, RED, a=a * sa)
        thread(ctx, [(600, 600), (960, 700), (1300, 600)], sa, 6, RED, a)
    else:
        lt = t - c[3]
        a = ease(seg(lt, 0, 0.5))
        box(ctx, 0, 790, W, 300, PAPER2, INK, 4, 0, a)
        text(ctx, 'THE BASE', 160, 860, 34, GREY, align='l', a=a)
        for k in range(6):
            brick(ctx, 1500 + (k % 3) * 34, 880 - (k // 3) * 22, 1.3, a)
        padlock(ctx, 1700, 870, 1.3, a)
        trophy(ctx, 960, 440, 0.95, a)
        k = int(lt / 2.4); ph = (lt % 2.4) / 2.4
        side = 1 if k % 2 == 0 else -1
        reach = math.sin(clamp(ph) * math.pi)
        hx = 960 + side * lerp(900, 230, ease(reach)); hy = 380
        sleeve = SUITS[(k + 1) % len(SUITS)]
        line(ctx, [(960 + side * 1100, hy + 40), (hx + side * 60, hy)], sleeve, 60, a)
        circle(ctx, hx, hy, 40, SKINS[k % 5], INK, 4, a)
        # strings from the basement to the reaching hand, like a puppet
        for j in range(3):
            thread(ctx, [(1540 + j * 40, 820), (hx + side * (40 + j * 20), 700), (hx + side * j * 20, hy - 10)], a, 4, RED, a)


def s13(ctx, t, d, c, T):
    bg(ctx)
    tilt = ease(seg(t, c[3] - 1.0, c[3] + 1.2))
    ctx.save(); camera(ctx, 960, lerp(420, 640, tilt), lerp(1.12, 1.0, tilt))
    st = {'lit': ease(seg(t, c[2], c[3])), 'shadow': lerp(0.4, 1.0, tilt), 'stack': 12}
    building(ctx, T, st)
    if t > c[3]:
        a = ease(seg(t, c[3] + 0.3, c[3] + 1.4))
        thread(ctx, [(1500, 160), (1520, 400), (1490, 630)], a, 7, RED)
        circle(ctx, 1490, 630, 10, RED, None, a=a)
        text(ctx, '?', 1500, 800, 120, RED, 'Caladea', True, False, 'c', a)
    ctx.restore()
    for i, s in enumerate(['RIGHTS', 'COURTS', 'FREE PRESS']):
        a = ease(seg(t, c[2] + 0.4 + i * 1.0, c[2] + 0.9 + i * 1.0)) * (1 - seg(t, c[3] - 0.5, c[3]))
        if a > 0:
            box(ctx, 80, 180 + i * 110, 340, 80, WHITE, TEAL, 4, 40, a)
            label(ctx, s, 250, 234 + i * 110, 36, TEAL, a)


def wall(ctx, t, paint, crack, a=1.0):
    box(ctx, 0, 0, W, H, hexc('#D8CCB2'), None, a=a)
    for r in range(0, H, 70):
        off = 0 if (r // 70) % 2 == 0 else 70
        for x in range(-70 + off, W, 140):
            box(ctx, x, r, 140, 70, None, hexc('#C4B597'), 3, 0, a)
    # paint stripes covering the wall
    cols = [hexc('#E9A8A0'), hexc('#9CC5C2'), hexc('#F2D27A'), hexc('#C7B6E0'), hexc('#B7D39C')]
    for i in range(5):
        p = ease(seg(paint, i * 0.15, i * 0.15 + 0.4))
        if p > 0:
            box(ctx, 200 + i * 300, 0, 300, H * p, cols[i], None, a=a)
    # crack
    pts = [(1010, H), (980, 900), (1040, 760), (990, 610), (1060, 470), (1020, 330), (1080, 180), (1050, 0)]
    if crack > 0:
        line(ctx, partial(pts, crack), INK, 8, a)
        sub = partial(pts, crack)
        for k in range(2, len(sub) - 1, 2):
            x, y = sub[k]
            line(ctx, [(x, y), (x + 60, y - 30)], INK, 4, a)


def s14(ctx, t, d, c, T):
    bg(ctx)
    paint = seg(t, c[1] + 2, c[2])
    crack = 1.0 if t < c[1] + 2 else seg(t, c[2] - 2, c[2] + 2.0)
    wall(ctx, t, paint, crack)
    if t > c[1]:
        for i in range(2):
            x = 400 + i * 900 + math.sin(t * 2 + i) * 30
            person(ctx, x, 1060, 2.2, WHITE, SKINS[i + 1], INK, arms='up')
            ry = 650 + math.sin(t * 4 + i) * 120
            line(ctx, [(x + 75, 790), (x + 120, ry)], INK, 8)
            box(ctx, x + 70, ry - 30, 110, 40, GOLD, INK, 4, 8)
    if t < c[2] - 0.3:
        quote_card(ctx, '"...the suppression of the abuses of capitalism instead of suppression of capitalism itself."',
                   'Rosa Luxemburg, Reform or Revolution?, ch. 8', 360, 200, 1200, seg(t, 0.8, c[2] - 3), 1 - seg(t, c[2] - 0.8, c[2] - 0.3), 52)
    # silent subscribe knot after the line
    sa = ease(seg(t, d - 3.6, d - 3.2)) * (1 - seg(t, d - 0.6, d - 0.2))
    if sa > 0:
        box(ctx, 1520, 870, 340, 120, WHITE, RED, 4, 60, sa)
        knot(ctx, 1590, 930, 34, sa)
        text(ctx, 'SUBSCRIBE', 1640, 944, 36, RED, align='l', a=sa)


def s15(ctx, t, d, c, T):
    bg(ctx)
    box(ctx, 0, 0, W, 560, WHITE, None, a=0.5)
    box(ctx, 0, 560, W, 520, PAPER2, None)
    line(ctx, [(0, 560), (W, 560)], INK, 5)
    text(ctx, 'THE TOP FLOOR', 120, 110, 30, GREY, align='l')
    text(ctx, 'THE FOUNDATION', 120, 640, 30, GREY, align='l')
    p = ease(seg(t, 0.2, 2.0))
    thread(ctx, [(960, -10), (940, 200), (980, 420), (950, 700), (970, 1090)], p, 8)
    knots = [('WHO SHOULD RULE?', 0.6, 300, GREY), ('WHO OWNS?', c[1] + 0.9, 640, RED), ('WHO WORKS?', c[2], 760, RED),
             ('WHO KEEPS THE SURPLUS?', c[3], 880, RED), ('WHO DECIDES?', c[4], 1000, RED)]
    for i, (s, t0, y, col) in enumerate(knots):
        a = ease(seg(t, t0, t0 + 0.4))
        if a > 0:
            x = 955 + (math.sin(y) * 12)
            knot(ctx, x, y - 12, 24, a, RED)
            side = -1 if i % 2 else 1
            text(ctx, s, x + side * 60, y, 48 if i else 44, col, align='l' if side > 0 else 'r', a=a)


def pin_card(ctx, x, y, kind, lab, a, t):
    ctx.save(); ctx.translate(x, y); ctx.rotate(math.sin(x) * 0.05)
    box(ctx, -150, 0, 300, 300, WHITE, INK, 4, 4, a)
    box(ctx, -130, 20, 260, 210, PAPER2, None, a=a)
    if kind == 0:  # co-operative: people in a circle
        for k in range(6):
            ang = k * math.pi / 3 + t * 0.3
            person(ctx, math.cos(ang) * 70, 150 + math.sin(ang) * 30, 0.55, [TEAL, GOLD, GREY][k % 3], SKINS[k % 5], INK, a=a)
    elif kind == 1:  # land reform: field plots
        for i in range(3):
            for j in range(2):
                box(ctx, -110 + i * 75, 50 + j * 85, 68, 76, [hexc('#B7D39C'), GOLD, hexc('#9CC5C2')][(i + j) % 3], INK, 3, 2, a)
    elif kind == 2:  # bureaucrat's stamp
        sy = 90 + abs(math.sin(t * 3)) * 40
        box(ctx, -50, 170, 100, 40, WHITE, INK, 3, 2, a)
        box(ctx, -30, sy - 60, 60, 50, hexc('#8A5A44'), INK, 3, 6, a)
        box(ctx, -50, sy - 10, 100, 24, INK, None, a=a)
    else:  # crowd
        for k in range(9):
            person(ctx, -100 + (k % 5) * 50 + (k // 5) * 25, 200 + (k // 5) * 20, 0.6, SUITS[k % 7], SKINS[k % 5], INK, a=a)
    text(ctx, lab, 0, 272, 26, INK, a=a)
    circle(ctx, 0, 0, 12, RED, INK, 2, a)
    ctx.restore()


def s16(ctx, t, d, c, T):
    bg(ctx)
    p = ease(seg(t, 0, 1.2))
    thread(ctx, [(-20, 300), (480, 330), (960, 300), (1440, 330), (1940, 300)], p, 7)
    labs = ['CO-OPERATIVES', 'LAND REFORM', 'BUREAUCRACY', 'MASS MOVEMENTS']
    for i, lab in enumerate(labs):
        a = ease(seg(t, c[1] + i * 0.9, c[1] + i * 0.9 + 0.4))
        if a > 0:
            pin_card(ctx, 300 + i * 440, 320 - 60 * (1 - a), i, lab, a, t)
    a = ease(seg(t, 1.0, 1.6)) * (1 - seg(t, c[1] - 0.3, c[1]))
    if a > 0:
        box(ctx, 560, 560, 800, 260, WHITE, INK, 4, 8, a)
        box(ctx, 900, 600, 120, 150, GOLD, INK, 4, 4, a)
        circle(ctx, 960, 650, 30, SKINS[1], INK, 3, a)
        text(ctx, 'HARDER THAN', 760, 720, 34, GREY, a=a)
        text(ctx, 'A PORTRAIT', 1160, 720, 34, GREY, a=a)


def s17(ctx, t, d, c, T):
    bg(ctx)
    m = ease(seg(t, 1.5, 5.0))
    ctx.save()
    camera(ctx, lerp(1210, 960, m), lerp(200, 560, m), lerp(3.0, 1.0, m))
    pull = ease(seg(t, c[1], d))
    shake = math.sin(t * 40) * 3 * pull
    ctx.translate(shake, 0)
    building(ctx, T, {'stack': 12, 'leader': 5})
    # thread from the nameplate through the floors into the foundation
    pts = [(1211, 194), (1250, 300), (1180, 450), (1240, 600), (1300, 700), (1330, 800 + 40 * pull)]
    thread(ctx, pts, ease(seg(t, 0.5, 6.0)), 6)
    if pull > 0:
        circle(ctx, 1330, 800 + 40 * pull, 10, RED, None)
    ctx.restore()


def s18(ctx, t, d, c, T):
    bg(ctx)
    a = ease(seg(t, 0, 0.5))
    text(ctx, 'NEXT THREAD', 960, 360, 40, RED, a=a)
    para(ctx, "Why couldn't the most famous scientist in the world trust elections to stop the rich?", 960, 480, 70, 1400, INK, 'Caladea', True, False, 'c', 1.2, a)
    thread(ctx, [(-20, 760), (600, 740), (1300, 780), (1940, 760)], ease(seg(t, 0.5, 4)), 7)


def endscreen(ctx, t, d, c, T):
    bg(ctx)
    a = ease(seg(t, 0, 0.6))
    thread(ctx, [(-20, 540), (200, 520), (380, 560), (560, 540)], ease(seg(t, 0, 1.5)), 8)
    # next-lesson tile
    box(ctx, 560, 300, 800, 450, SHADOW, INK, 5, 12, a)
    box(ctx, 580, 320, 760, 410, hexc('#F6E3C2'), None, a=a)
    # generic scientist silhouette with wild hair
    for k in range(14):
        ang = math.pi * (0.9 + k / 13 * 1.2)
        circle(ctx, 760 + math.cos(ang) * 58, 470 + math.sin(ang) * 50, 24, WHITE, INK, 2, a)
    person(ctx, 760, 690, 1.9, GREY, SKINS[2], WHITE, a=a)
    para(ctx, "Why can't elections stop the rich?", 1120, 470, 50, 360, INK, 'Caladea', True, False, 'c', 1.15, a)
    text(ctx, 'LESSON 2', 1120, 650, 28, RED, a=a)
    # subscribe knot
    circle(ctx, 1600, 520, 110, WHITE, RED, 6, a)
    knot(ctx, 1600, 520, 64, a)
    text(ctx, 'SUBSCRIBE', 1600, 700, 40, RED, a=a)
    text(ctx, 'RED THREADS', 960, 900, 34, INK, a=a * 0.8)
    text(ctx, 'Ideas, not parties.', 960, 950, 26, GREY, 'Inter', False, True, 'c', a * 0.8)


SCENES = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18]
