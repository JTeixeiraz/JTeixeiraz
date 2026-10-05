#!/usr/bin/env python3
"""Gera os SVGs de assets/ a partir de content.py.

    python3 scripts/build_assets.py

Linguagem bento: blocos arredondados sobre fundo transparente, um fato por
bloco. Larguras: 1120 para peças cheias, 553 para os cartões em par e 364
para os de contato em trio — somados com o vão, ocupam a mesma largura.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import content as C  # noqa: E402
from svgkit import (DARK, DIM, GAP, INK, MINT, ON, REVEAL, TILE,  # noqa: E402
                    Svg, width, wrap)

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
W = 1120
HALF = (W - GAP) / 2
THIRD = (W - GAP * 2) / 3
ARROW = "#8a87a6"  # cinza que lê tanto na página clara quanto na escura


def save(name, s):
    path = os.path.join(OUT, name)
    with open(path, "w") as f:
        f.write(s.render())
    print(f"  assets/{name}  {os.path.getsize(path) // 1024} KB")


def fit(face, text, size, maxw, floor=12):
    while size > floor and width(face, text, size) > maxw:
        size -= 1
    return size


def dot(s, x, y, color, r=4):
    s.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{color}"/>')


def link(s, x, y, label, color, anchor_end=False):
    w = width("label", label, 12)
    x0 = x - w - 22 if anchor_end else x
    s.text(x0, y, label, "label", 12, color)
    s.arrow(x0 + w + 6, y - 11, 11, color)


def built_with(s, x, y, names, color, size=20, gap=18):
    for n in names:
        s.icon(C.ICONS[n], x, y - size + 4, size, color)
        s.text(x + size + 7, y, n, "bodym", 14, color)
        x += size + 7 + width("bodym", n, 14) + gap
    return x


# ----------------------------------------------------------------- hero

def hero():
    h = C.HERO
    cw, rh = (W - GAP * 3) / 4, 172
    H = rh * 2 + 150 + GAP * 2
    s = Svg(W, H, f"{' '.join(h['name'])} — {h['line']}",
            "Working at XP Educação as a Full Stack Developer. Birdy is live "
            "on Google Play and the App Store. Based in Belo Horizonte, "
            "Brazil. Focus: AI agents with a human in the loop.")
    s.css.append(REVEAL)

    s.tile(0, 0, cw * 2 + GAP, rh * 2 + GAP, C.VIOLET, cls="r")
    s.text(32, 48, h["handle"], "label", 12, "#ffffff", cls="r", opacity=.72)
    first, last = h["name"]
    s.text(30, 152, first, "head", 70, "#ffffff", cls="r d1")
    s.text(30, 228, last, "head", 70, "#ffffff", cls="r d1")
    s.para(32, 282, h["line"], "body", 20, "#ffffff", cw * 2 - 60, 29,
           cls="r d2", opacity=.92)

    spots = [(cw * 2 + GAP * 2, 0), (cw * 3 + GAP * 3, 0),
             (cw * 2 + GAP * 2, rh + GAP), (cw * 3 + GAP * 3, rh + GAP)]
    for i, ((label, big, small, col), (x, y)) in enumerate(zip(h["tiles"], spots)):
        cls, ink = f"r d{i + 2}", ON[col]
        s.tile(x, y, cw, rh, col, cls=cls)
        s.text(x + 24, y + 40, label, "label", 11, ink, cls=cls, opacity=.75)
        s.text(x + 22, y + 106, big, "head", fit("head", big, 30, cw - 46), ink,
               cls=cls)
        s.text(x + 24, y + 138, small, "bodym", 15, ink, cls=cls, opacity=.8)

    y0 = rh * 2 + GAP * 2
    s.tile(0, y0, W, 150, TILE, cls="r d6")
    s.text(32, y0 + 40, h["stack_label"], "label", 11, DIM, cls="r d6")
    names = h["stack"]
    step = (W - 64) / len(names)
    s.add('<g class="r d7">')
    for i, n in enumerate(names):
        cx = 32 + step * i + step / 2
        s.icon(C.ICONS[n], cx - 17, y0 + 58, 34, INK)
        s.text(cx, y0 + 124, n, "body", 12, DIM, anchor="middle")
    s.add("</g>")
    save("hero.svg", s)


# ------------------------------------------------------------ what I do

def doing():
    pad, cols = 28, 3
    rows = [C.DOING[i:i + cols] for i in range(0, len(C.DOING), cols)]
    heights = [max(150 + len(wrap(b, "body", 16, THIRD - pad * 2)) * 24 + 8
                   for _, b, _ in r) for r in rows]
    H = sum(heights) + GAP * (len(rows) - 1)
    alt = " ".join(f"{t}: {b}" for t, b, _ in C.DOING)
    s = Svg(W, H, "What I do", alt)
    y, n = 0, 1
    for r, rh in zip(rows, heights):
        for c, (title, body, col) in enumerate(r):
            x = c * (THIRD + GAP)
            s.tile(x, y, THIRD, rh, TILE)
            s.tile(x + pad, y + pad, 44, 44, col, r=12)
            s.text(x + pad + 22, y + pad + 27, f"{n:02d}", "label", 13, ON[col],
                   anchor="middle")
            s.text(x + pad, y + 114, title, "head", 24, INK)
            s.para(x + pad, y + 148, body, "body", 16, DIM, THIRD - pad * 2, 24)
            n += 1
        y += rh + GAP
    save("doing.svg", s)


# ------------------------------------------------------------- projects

def featured():
    p = C.BIRDY
    pad, lw, rx = 40, 580, 652
    rw = W - rx - 28

    def left(s):
        s.chip(pad, 36, p["status"], DARK, ink=MINT)
        s.text(pad - 2, 156, p["name"], "head", 76, DARK)
        y = s.para(pad, 206, p["what"], "body", 21, DARK, lw, 30)
        y += 14
        for pt in p["points"]:
            lines = wrap(pt, "bodym", 17, lw - 22)
            dot(s, pad + 4, y - 6, DARK)
            for line in lines:
                s.text(pad + 20, y, line, "bodym", 17, DARK)
                y += 25
            y += 9
        return y + 58

    probe = Svg(1, 1, "")
    H = max(left(probe), 470)
    s = Svg(W, H, f"Birdy — {p['status']}",
            f"{p['what']} " + " ".join(p["points"]))
    s.tile(0, 0, W, H, MINT)
    left(s)
    link(s, pad, H - 40, p["link"], DARK)

    # O painel "de relance": as respostas que o recrutador procura.
    s.tile(rx, 28, rw, H - 56, TILE)
    s.text(rx + 28, 70, "AT A GLANCE", "label", 11, DIM)
    y = 112
    for k, v in p["glance"]:
        s.text(rx + 28, y, k, "label", 10, DIM)
        s.text(rx + 150, y, v, "bodym", 17, INK)
        s.add(f'<line x1="{rx + 28}" y1="{y + 18}" x2="{rx + rw - 28}" '
              f'y2="{y + 18}" stroke="{INK}" stroke-opacity=".1"/>')
        y += 46
    s.text(rx + 28, y + 14, "BUILT WITH", "label", 11, DIM)
    names = p["stack"]
    step = (rw - 56) / len(names)
    for i, n in enumerate(names):
        cx = rx + 28 + step * i + step / 2
        s.icon(C.ICONS[n], cx - 15, y + 34, 30, INK)
        s.text(cx, y + 92, n, "body", 12, DIM, anchor="middle")
    save("project-birdy.svg", s)


def card(s, p, H=None):
    pad, w = 32, HALF
    col = p["color"]
    s.chip(pad, 32, p["status"], col)
    s.text(pad - 1, 128, p["name"], "head", 42, INK)
    y = s.para(pad, 170, p["what"], "body", 17, DIM, w - pad * 2, 25) + 10
    for pt in p["points"]:
        dot(s, pad + 4, y - 5, col, 3.5)
        for line in wrap(pt, "bodym", 15.5, w - pad * 2 - 20):
            s.text(pad + 18, y, line, "bodym", 15.5, INK)
            y += 23
        y += 8
    if H is None:
        return y + 64
    built_with(s, pad, H - 34, p["stack"], INK)
    link(s, w - pad, H - 34, p["link"], col, anchor_end=True)
    return H


def cards():
    H = max(card(Svg(1, 1, ""), p) for p in C.CARDS)
    for p in C.CARDS:
        s = Svg(HALF, H, f"{p['name']} — {p['status']}",
                f"{p['what']} " + " ".join(p["points"]))
        s.tile(0, 0, HALF, H, TILE)
        card(s, p, H)
        save(f"project-{p['slug']}.svg", s)


# ---------------------------------------------------------- how I use AI

def ai():
    a = C.AI
    gap, pad = 46, 28
    tw = (W - gap * 2) / 3
    th = max(150 + len(wrap(t, "body", 16, tw - pad * 2)) * 24 + 40
             for _, _, t, _ in a["steps"])
    ex = wrap(a["example"], "headm", 22, W - 64)
    note = wrap(a["note"], "body", 16, W - 64)
    eh = 96 + len(ex) * 30 + 14 + len(note) * 24 + 20
    H = th + GAP + eh
    s = Svg(W, H, "How I use AI",
            " ".join(f"{n}: {t}" for _, n, t, _ in a["steps"])
            + f" {a['example']} {a['note']}")
    # A barra de cada passo enche em sequência: o pedido anda da IA para o
    # código e só termina quando a pessoa aprova.
    for i in range(3):
        a0, a1 = 22 * i, 22 * i + 22
        s.css.append(f"@keyframes b{i}{{0%,{a0}%{{transform:scaleX(0)}}"
                     f"{a1}%,88%{{transform:scaleX(1)}}100%{{transform:scaleX(0)}}}}"
                     f".b{i}{{animation:b{i} 6s cubic-bezier(.65,0,.35,1) infinite}}")
    s.css.append(".bar{transform-box:fill-box;transform-origin:left center}"
                 "@media (prefers-reduced-motion:reduce){.bar{animation:none}}")
    for i, (step, name, text, col) in enumerate(a["steps"]):
        x, ink = i * (tw + gap), ON[col]
        s.tile(x, 0, tw, th, col)
        s.text(x + pad, 44, step, "label", 11, ink, opacity=.75)
        s.text(x + pad, 96, name, "head", 28, ink)
        s.para(x + pad, 132, text, "body", 16, ink, tw - pad * 2, 24, opacity=.88)
        bar = (f'x="{x + pad}" y="{th - 34}" width="{tw - pad * 2:.1f}" '
               f'height="6" rx="3" fill="{ink}"')
        s.add(f'<rect {bar} fill-opacity=".22"/>')
        s.add(f'<rect {bar} class="bar b{i}"/>')
        if i < 2:
            ax, ay = x + tw + 10, th / 2
            s.add(f'<path d="M{ax} {ay}h{gap - 20}m-8 -7l8 7l-8 7" fill="none" '
                  f'stroke="{ARROW}" stroke-width="2.5" stroke-linecap="round" '
                  f'stroke-linejoin="round"/>')
    y = th + GAP
    s.tile(0, y, W, eh, TILE)
    s.chip(32, y + 30, a["label"], MINT)
    yy = y + 100
    for line in ex:
        s.text(32, yy, line, "headm", 22, INK)
        yy += 30
    yy += 10
    for line in note:
        s.text(32, yy, line, "body", 16, DIM)
        yy += 24
    save("ai.svg", s)


# ---------------------------------------------------------------- stack

def stack():
    pad, cols = 28, 3
    colw = (THIRD - pad * 2) / 2

    def tile_h(items, extra):
        rows = (len(items) + 1) // 2
        return 92 + rows * 40 + (34 if extra else 0) + 14

    rows = [C.STACK[i:i + cols] for i in range(0, len(C.STACK), cols)]
    hs = [max(tile_h(it, ex) for _, _, it, ex in r) for r in rows]
    label, practices = C.PRACTICES
    plines = wrap(practices, "body", 17, W - 64)
    ph = 84 + len(plines) * 26 + 12
    H = sum(hs) + GAP * len(rows) + ph
    alt = "; ".join(f"{g.title()}: {', '.join(it)}{(' — ' + ex) if ex else ''}"
                    for g, _, it, ex in C.STACK) + f"; Practices: {practices}"
    s = Svg(W, H, "Stack", alt)
    y = 0
    for r, rh in zip(rows, hs):
        for c, (group, col, items, extra) in enumerate(r):
            x = c * (THIRD + GAP)
            s.tile(x, y, THIRD, rh, TILE)
            s.chip(x + pad, y + pad, group, col)
            for k, n in enumerate(items):
                ix = x + pad + (k % 2) * colw
                iy = y + 104 + (k // 2) * 40
                s.icon(C.ICONS[n], ix, iy - 19, 24, INK)
                s.text(ix + 34, iy, n, "bodym", fit("bodym", n, 15, colw - 40),
                       INK)
            if extra:
                s.text(x + pad, y + 104 + ((len(items) + 1) // 2) * 40, extra,
                       "body", 14, DIM)
        y += rh + GAP
    s.tile(0, y, W, ph, TILE)
    s.chip(32, y + 28, label, MINT)
    s.para(32, y + 92, practices, "body", 17, INK, W - 64, 26)
    save("stack.svg", s)


# -------------------------------------------------------------- contact

def contact():
    H = 150
    for slug, label, value, col in C.CONTACT:
        ink = ON[col]
        s = Svg(THIRD, H, f"{label.title()}: {value}")
        s.tile(0, 0, THIRD, H, col)
        s.text(26, 42, label, "label", 11, ink, opacity=.75)
        s.arrow(THIRD - 46, 26, 18, ink, sw=2.4)
        s.text(26, 112, value, "bodym", fit("bodym", value, 21, THIRD - 52), ink)
        save(f"contact-{slug}.svg", s)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for old in os.listdir(OUT):
        if old.endswith(".svg"):
            os.remove(os.path.join(OUT, old))
    hero()
    doing()
    featured()
    cards()
    ai()
    stack()
    contact()
