from lib import *

BX0, BX1 = 560, 1360
GY = 640
FH = 96
FLOORS = [160 + i * FH for i in range(5)]  # top y of each floor, top floor first
FX0, FX1, FY1 = 500, 1420, 940
APEX = (960, 92)
ROOMS = [(FX0, 760, 'LAND'), (760, 1060, 'FACTORIES'), (1060, 1240, 'MONEY'), (1240, FX1, 'SURPLUS')]
FLOOR_LABELS = ['GOVERNMENT', 'PARLIAMENT', 'COURTS', 'PARTIES', 'NEWS & TV']


def outline_path():
    """Points the red thread follows to draw the building."""
    return [(380, GY), (BX0, GY), (BX0, FLOORS[0]), (APEX[0], APEX[1]), (BX1, FLOORS[0]), (BX1, GY),
            (FX1, GY), (FX1, FY1), (FX0, FY1), (FX0, GY), (BX0, GY), (1540, GY)]


def ground(ctx, a=1.0):
    box(ctx, -2000, GY, 6000, 1400, EARTH, None, a=a)
    # soil specks
    rnd = random.Random(3)
    for i in range(160):
        x = rnd.uniform(-600, 2500); y = rnd.uniform(GY + 20, GY + 700)
        if FX0 - 10 < x < FX1 + 10 and y < FY1 + 10:
            continue
        circle(ctx, x, y, rnd.uniform(2, 5), hexc('#B49E77'), None, a=a)
    line(ctx, [(-2000, GY), (4000, GY)], INK, 5, a)


def leader_fig(ctx, x, y, idx, a=1.0, s=0.62):
    person(ctx, x, y, s, SUITS[idx % len(SUITS)], SKINS[(idx * 2 + 1) % len(SKINS)],
           [INK, GREY, hexc('#5A3A22'), WHITE, INK][idx % 5], a=a)


def nameplate(ctx, x, y, idx, a=1.0, tilt=0.0, s=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(tilt)
    ctx.scale(s, s)
    box(ctx, -46, -14, 92, 28, GOLD, INK, 2.5, 4, a)
    circle(ctx, -36, 0, 3, INK, None, a=a)
    circle(ctx, 36, 0, 3, INK, None, a=a)
    # abstract "name": two bars, width varies by idx
    w1 = 30 + (idx * 13) % 22
    box(ctx, -26, -6, w1, 4, INK, None, a=a)
    box(ctx, -26, 2, 52 - (idx * 7) % 18, 4, INK, None, a=a)
    ctx.restore()


def top_floor(ctx, T, st, a=1.0):
    y0 = FLOORS[0]
    # desk + leader
    swap = st.get('swap')  # (old, new, prog)
    lx = 1010
    if swap:
        old, new, p = swap
        p = ease(p)
        if p < 1:
            leader_fig(ctx, lx - 260 * p, y0 + 88, old, a * (1 - p))
        if p > 0:
            leader_fig(ctx, lx + 260 * (1 - p), y0 + 88, new, a * p)
    else:
        leader_fig(ctx, lx, y0 + 88, st.get('leader', 0), a)
    box(ctx, 940, y0 + 52, 150, 38, hexc('#8A5A44'), INK, 3, 3, a)
    # portrait on wall
    box(ctx, 860, y0 + 14, 46, 34, WHITE, INK, 2.5, 2, a)
    circle(ctx, 883, y0 + 30, 8, SUITS[(st.get('leader', 0)) % len(SUITS)], None, a=a)
    # door with nameplate
    box(ctx, 1180, y0 + 14, 62, 82, hexc('#A7744C'), INK, 3, 3, a)
    circle(ctx, 1232, y0 + 58, 3.5, GOLD, None, a=a)
    plate = st.get('plate')
    if plate is None:
        nameplate(ctx, 1211, y0 + 34, st.get('leader', 0), a, s=0.55)
    else:
        old, new, p = plate
        if p < 0.5:
            q = ease(p / 0.5)
            nameplate(ctx, 1211, y0 + 34 + 120 * q * q, old, a * (1 - q * 0.3), tilt=q * 0.8, s=0.55)
        else:
            q = eo((p - 0.5) / 0.5)
            nameplate(ctx, 1211 + 80 * (1 - q), y0 + 34, new, a * q, s=0.55)


def parliament(ctx, T, a=1.0):
    y0 = FLOORS[1]
    cx, cy = 1040, y0 + 90
    k = 0
    for r, n in ((52, 9), (76, 13)):
        for i in range(n):
            ang = math.pi + (i + 0.5) * math.pi / n
            x = cx + math.cos(ang) * r * 1.9; y = cy + math.sin(ang) * r * 0.95
            col = SUITS[(k * 3) % len(SUITS)]
            box(ctx, x - 9, y - 2, 18, 14, col, INK, 2, 4, a)
            circle(ctx, x, y - 8 + math.sin(T * 3 + k) * 1.2, 7, SKINS[k % 5], INK, 2, a)
            k += 1
    box(ctx, cx - 20, cy - 34, 40, 30, hexc('#8A5A44'), INK, 2.5, 3, a)


def courts(ctx, T, a=1.0):
    y0 = FLOORS[2]
    person(ctx, 1040, y0 + 66, 0.42, INK, SKINS[2], WHITE, a=a)
    box(ctx, 940, y0 + 46, 200, 44, hexc('#8A5A44'), INK, 3, 3, a)
    # scales
    sx, sy = 1220, y0 + 40
    tilt = math.sin(T * 1.5) * 0.12
    line(ctx, [(sx, sy - 18), (sx, sy + 40)], INK, 3, a)
    lx, ly = sx - 34 * math.cos(tilt), sy - 18 - 34 * math.sin(tilt)
    rx, ry = sx + 34 * math.cos(tilt), sy - 18 + 34 * math.sin(tilt)
    line(ctx, [(lx, ly), (rx, ry)], INK, 3, a)
    for (px, py) in ((lx, ly), (rx, ry)):
        line(ctx, [(px, py), (px, py + 18)], INK, 2, a)
        ctx.new_sub_path(); ctx.arc(px, py + 18, 12, 0, math.pi); setc(ctx, GOLD, a); ctx.fill()
    box(ctx, sx - 18, sy + 38, 36, 8, INK, None, a=a)


def parties(ctx, T, a=1.0):
    y0 = FLOORS[3]
    for i, (x, col) in enumerate(((800, TEAL), (980, GOLD), (1160, hexc('#5B4B8A')))):
        sway = math.sin(T * 2 + i) * 3
        ctx.move_to(x - 30, y0 + 10); ctx.line_to(x + 30, y0 + 10); ctx.line_to(x + 30 + sway, y0 + 52)
        ctx.line_to(x + sway, y0 + 40); ctx.line_to(x - 30 + sway, y0 + 52); ctx.close_path()
        setc(ctx, col, a); ctx.fill_preserve(); setc(ctx, INK, a); ctx.set_line_width(2.5); ctx.stroke()
        person(ctx, x + 50, y0 + 92, 0.36, col, SKINS[i + 1], INK, arms='up' if math.sin(T * 2.5 + i * 2) > 0.3 else 'down', a=a)
        # speech bubble
        if math.sin(T * 2.5 + i * 2) > 0.3:
            box(ctx, x + 64, y0 + 18, 36, 22, WHITE, INK, 2, 8, a)
            text(ctx, '!', x + 82, y0 + 36, 18, RED, a=a)


def news(ctx, T, a=1.0):
    y0 = FLOORS[4]
    for i, x in enumerate((820, 1080)):
        box(ctx, x, y0 + 12, 150, 74, SHADOW, INK, 3, 6, a)
        box(ctx, x + 8, y0 + 20, 134, 58, hexc('#9CC5C2'), None, a=a)
        circle(ctx, x + 75, y0 + 44, 13, SKINS[i * 2], INK, 2, a)
        box(ctx, x + 58, y0 + 57, 34, 21, TEAL if i == 0 else GREY, None, a=a)
        mo = abs(math.sin(T * 9 + i)) * 4
        box(ctx, x + 70, y0 + 47, 10, 1 + mo, INK, None, a=a)
        # ticker
        box(ctx, x + 8, y0 + 70, 134, 8, RED, None, a=a)


def foundation(ctx, T, st, a=1.0):
    box(ctx, FX0, GY, FX1 - FX0, FY1 - GY, PAPER2, None, a=a)
    # land
    for i in range(6):
        y = GY + 120 + i * 30
        line(ctx, [(FX0 + 20, y), (750, y - 14)], hexc('#9C7A45'), 4, a)
        for j in range(5):
            x = FX0 + 40 + j * 46
            line(ctx, [(x, y - 6 - j * 2.8), (x, y - 18 - j * 2.8)], TEAL, 3, a)
    # factory
    box(ctx, 790, GY + 120, 120, 90, GREY, INK, 3, 4, a)
    ctx.save(); ctx.translate(850, GY + 165); ctx.rotate(T * 1.2)
    for k in range(8):
        ctx.save(); ctx.rotate(k * math.pi / 4); box(ctx, -6, -34, 12, 12, GOLD, INK, 2, 2, a); ctx.restore()
    circle(ctx, 0, 0, 26, GOLD, INK, 2.5, a); circle(ctx, 0, 0, 8, INK, None, a=a)
    ctx.restore()
    box(ctx, 930, GY + 190, 110, 14, INK, None, a=a)
    for k in range(5):
        x = 935 + ((T * 30 + k * 22) % 110)
        brick(ctx, x, GY + 182, 0.5, a)
    # money vault
    vx, vy = 1150, GY + 160
    circle(ctx, vx, vy, 54, GREY, INK, 3, a)
    circle(ctx, vx, vy, 40, hexc('#8E8E96'), INK, 2.5, a)
    for k in range(6):
        ang = k * math.pi / 3 + T * 0.2
        line(ctx, [(vx, vy), (vx + math.cos(ang) * 34, vy + math.sin(ang) * 34)], INK, 4, a)
    circle(ctx, vx, vy, 8, GOLD, INK, 2, a)
    # surplus room
    glow = st.get('glow', 0)
    if glow > 0:
        box(ctx, 1240, GY, FX1 - 1240, FY1 - GY, GOLD, None, a=a * 0.45 * glow)
    n = st.get('stack', 12)
    k = 0
    for row in range(6):
        for col in range(4 - row % 2):
            if k >= n:
                break
            brick(ctx, 1272 + col * 30 + (row % 2) * 15, FY1 - 14 - row * 19, 1.0, a)
            k += 1
    padlock(ctx, 1330, GY + 70, 1.1, a)
    # workers carrying bricks to the surplus room
    if st.get('workers', True):
        for i in range(3):
            ph = ((T / 7.0) + i / 3) % 1
            x = lerp(790, 1215, ph)
            fade = seg(ph, 0, 0.06) * (1 - seg(ph, 0.94, 1))
            person(ctx, x, FY1 - 4, 0.5, TEAL if i != 1 else hexc('#7A8450'), SKINS[i + 2], INK, walk=T * 7 + i, arms='carry', a=a * fade)
            brick(ctx, x, FY1 - 4 - 76, 0.75, a * fade)
            # a tiny crumb stays with the worker: wage
    # dividers + outline
    for x0, x1, lab in ROOMS[1:]:
        line(ctx, [(x0, GY), (x0, FY1)], INK, 3, a)
    box(ctx, FX0, GY, FX1 - FX0, FY1 - GY, None, INK, 5, a=a)
    la = st.get('flabels', 1.0)
    for x0, x1, lab in ROOMS:
        text(ctx, lab, (x0 + x1) / 2, GY + 36, 22, INK if lab != 'SURPLUS' else RED, a=a * la)
    sh = st.get('shadow', 0)
    if sh > 0:
        box(ctx, FX0, GY, FX1 - FX0, FY1 - GY, SHADOW, None, a=a * 0.62 * sh)


def building(ctx, T, st):
    a = st.get('a', 1.0)
    ground(ctx, st.get('ground', 1.0) * a)
    foundation(ctx, T, st, a * st.get('found', 1.0))
    if st.get('found', 1.0) < 1:
        box(ctx, FX0, GY, FX1 - FX0, FY1 - GY, None, INK, 5, a=a)
    reveal = st.get('reveal', [1] * 5)
    # walls
    for i, y in enumerate(FLOORS):
        r = reveal[i]
        box(ctx, BX0, y, BX1 - BX0, FH, WHITE, None, a=a * r)
    lit = st.get('lit', 0)
    funcs = [lambda: top_floor(ctx, T, st, a * reveal[0]), lambda: parliament(ctx, T, a * reveal[1]),
             lambda: courts(ctx, T, a * reveal[2]), lambda: parties(ctx, T, a * reveal[3]),
             lambda: news(ctx, T, a * reveal[4])]
    for i, f in enumerate(funcs):
        if reveal[i] > 0:
            f()
    # windows on the outer walls (lit progressively)
    k = 0
    for i, y in enumerate(FLOORS):
        for x in (BX0 + 22, BX1 - 52):
            on = clamp(lit * 10 - k)
            box(ctx, x, y + 22, 30, 48, mix(hexc('#C9D6D5'), hexc('#FFD86B'), on), INK, 2.5, 2, a * max(reveal[i], 0.0))
            if on > 0:
                circle(ctx, x + 15, y + 46, 34, hexc('#FFD86B', 0.25 * on), None, a=a)
            k += 1
    # labels
    la = st.get('labels', 1.0)
    for i, y in enumerate(FLOORS):
        text(ctx, FLOOR_LABELS[i], BX0 + 72, y + 56, 20, GREY, align='l', a=a * la * reveal[i])
    # structure lines
    for y in FLOORS[1:]:
        line(ctx, [(BX0, y), (BX1, y)], INK, 4, a)
    box(ctx, BX0, FLOORS[0], BX1 - BX0, GY - FLOORS[0], None, INK, 5, a=a)
    ctx.move_to(BX0 - 20, FLOORS[0]); ctx.line_to(*APEX); ctx.line_to(BX1 + 20, FLOORS[0]); ctx.close_path()
    setc(ctx, hexc('#B9A27A'), a); ctx.fill_preserve(); setc(ctx, INK, a); ctx.set_line_width(5); ctx.stroke()
    # columns at entrance level hint
    if st.get('crack', 0) > 0:
        pass
