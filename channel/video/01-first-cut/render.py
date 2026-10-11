import json, sys, subprocess
from scenes import *

import os
TM = json.load(open('timing_bn.json' if os.environ.get('RT_LANG') == 'bn' else 'timing.json'))
VO_END = TM[-1]['end']
END_LEN = 20.0
TOTAL = VO_END + END_LEN
STARTS = [b['start'] for b in TM]


def caption_chunks():
    tmp = cairo.ImageSurface(cairo.FORMAT_RGB24, 10, 10)
    cx = cairo.Context(tmp)
    out = []
    for b in TM:
        for s, e, txt in b['caps']:
            ls = wrap(cx, txt, 42, 1500)
            # chunks of at most two lines
            groups = [ls[i:i + 2] for i in range(0, len(ls), 2)]
            tot = sum(len(' '.join(g)) for g in groups)
            t0 = s
            for g in groups:
                dur = (e - s) * len(' '.join(g)) / tot
                out.append((t0, t0 + dur + (0.25 if g is groups[-1] else 0), g))
                t0 += dur
    return out


CAPS = caption_chunks()


def draw_caption(ctx, T):
    for s, e, ls in CAPS:
        if s <= T < e:
            wmax = max(twidth(ctx, l, 42) for l in ls)
            h = len(ls) * 54 + 26
            y0 = H - 40 - h
            box(ctx, W / 2 - wmax / 2 - 28, y0, wmax + 56, h, hexc('#1E1E24', 0.78), None, r=14)
            for i, l in enumerate(ls):
                text(ctx, l, W / 2, y0 + 52 + i * 54, 42, WHITE)
            return


def watermark(ctx, T):
    a = 0.55
    knot(ctx, 1680, 58, 14, a)
    text(ctx, 'RED THREADS', 1706, 66, 22, INK, align='l', a=a)


def scene_at(ctx, T):
    if T >= VO_END:
        endscreen(ctx, T - VO_END, END_LEN, [0], T)
        return
    i = max(k for k in range(len(STARTS)) if STARTS[k] <= T)
    b = TM[i]
    d = b['end'] - b['start']
    c = [x[0] - b['start'] for x in b['caps']]
    SCENES[i](ctx, T - b['start'], d, c, T)


def frame(T):
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    ctx = cairo.Context(surf)
    scene_at(ctx, T)
    # short crossfade from the previous scene at each cut
    for k, st in enumerate(STARTS[1:] + [VO_END], 1):
        if st <= T < st + 0.35 and k not in (5, 6):  # building scenes 4->5->6 flow without a fade
            prev = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
            pc = cairo.Context(prev)
            scene_at(pc, st - 0.001)
            ctx.set_source_surface(prev, 0, 0)
            ctx.paint_with_alpha(1 - (T - st) / 0.35)
            break
    if T < VO_END:
        watermark(ctx, T)
        draw_caption(ctx, T)
    return surf


if __name__ == '__main__':
    part, nparts = int(sys.argv[1]), int(sys.argv[2])
    nf = int(TOTAL * FPS)
    lo, hi = nf * part // nparts, nf * (part + 1) // nparts
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr0', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', f'part{os.environ.get("RT_LANG", "en")}{part}.mp4'], stdin=subprocess.PIPE)
    for f in range(lo, hi):
        s = frame(f / FPS)
        s.flush()
        p.stdin.write(bytes(s.get_data()))
        if (f - lo) % 300 == 0:
            print(part, f - lo, hi - lo, flush=True)
    p.stdin.close()
    p.wait()
    print('done', part, flush=True)
