#!/usr/bin/env python3
"""Gera os SVGs de assets/ a partir de content.py.

    python3 scripts/build_assets.py

Todo texto dos SVGs mora em content.py; este arquivo só cuida do desenho.
Larguras: 1120 para peças de largura total, 560 para os cartões que andam
em pares — os dois somados ocupam a mesma largura de uma peça cheia.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import content as C  # noqa: E402
from svgkit import (BASE, INK, INK2, INK3, L_INK, L_INK3, REVEAL, SIG,  # noqa: E402
                    SIGD, SIGL, SURF, WELL, Svg, width)

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
W, CW = 1120, 560


def save(name, svg):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(svg.render())
    print(f"  assets/{name}  {os.path.getsize(os.path.join(OUT, name)) // 1024} KB")


def corners(s, x, y, w, h, k=12, color=INK, op=0.5):
    """Os marcadores de canto do portfólio: moldura técnica sem virar card."""
    for cx, cy, dx, dy in ((x, y, 1, 1), (x + w, y, -1, 1),
                           (x, y + h, 1, -1), (x + w, y + h, -1, -1)):
        s.add(f'<path d="M{cx + dx * k} {cy}H{cx}V{cy + dy * k}" fill="none" '
              f'stroke="{color}" stroke-opacity="{op}" stroke-width="1.5"/>')


# ---------------------------------------------------------------- hero

def hero():
    H = 548
    s = Svg(W, H, C.HERO["alt"], C.HERO["desc"])
    s.css.append(REVEAL)
    s.defs.append(
        f'<pattern id="dp" width="7" height="7" patternUnits="userSpaceOnUse">'
        f'<rect width="2" height="2" fill="{INK}"/></pattern>'
        f'<filter id="nz" filterUnits="userSpaceOnUse" x="0" y="0" width="{W}" '
        f'height="{H}"><feTurbulence type="fractalNoise" baseFrequency=".0042 .0088" '
        f'numOctaves="4" seed="29"/><feColorMatrix type="matrix" values="0 0 0 0 1 '
        f'0 0 0 0 1 0 0 0 0 1 3.4 0 0 0 -1.32"/></filter>'
        f'<mask id="mn" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" '
        f'height="{H}"><rect width="{W}" height="{H}" filter="url(#nz)"/></mask>'
        f'<linearGradient id="fx" x1="0" x2="1"><stop offset=".38" stop-color="#000"/>'
        f'<stop offset=".95" stop-color="#fff"/></linearGradient>'
        f'<linearGradient id="fy" x1="0" y1="0" x2="0" y2="1"><stop offset=".1" '
        f'stop-color="#000"/><stop offset=".4" stop-color="#fff"/><stop '
        f'offset=".8" stop-color="#fff"/><stop offset=".94" stop-color="#000"/>'
        f'</linearGradient>'
        f'<mask id="mx"><rect width="{W}" height="{H}" fill="url(#fx)"/></mask>'
        f'<mask id="my"><rect width="{W}" height="{H}" fill="url(#fy)"/></mask>'
        f'<radialGradient id="glow" cx="{W - 170}" cy="150" r="460" '
        f'gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{SIG}" '
        f'stop-opacity=".26"/><stop offset="1" stop-color="{SIG}" stop-opacity="0"/>'
        f'</radialGradient>'
    )
    s.rect(0, 0, W, H, fill=BASE)
    s.rect(0, 0, W, H, fill="url(#glow)", extra='class="f"')
    # A trama de pontos ecoa o poço ASCII do portfólio sem desenhar nada.
    s.add(f'<g class="f d2" mask="url(#mx)"><g mask="url(#my)"><rect width="{W}" '
          f'height="{H}" fill="url(#dp)" mask="url(#mn)" opacity=".55"/></g></g>')

    s.text(40, 35, "001", "mono", 13, INK3, cls="r")
    s.text(80, 36, "JPT", "title", 16, INK, cls="r")
    s.text(80 + width("title", "JPT", 16) + 12, 35, "/  " + C.HERO["role"],
           "mono", 13, INK3, cls="r")
    s.text(W - 40, 35, C.HERO["place"], "mono", 13, INK3, anchor="end", cls="r")
    s.hline(0, W, 58)

    s.rect(40, 218, 7, 7, fill=SIGL, extra='class="r d1"')
    s.text(58, 225, C.HERO["kicker"], "mono", 13, INK2, cls="r d1")
    s.text(40, 278, C.HERO["name"], "title", 26, INK, cls="r d2")
    l1, l2a, l2b = C.HERO["lines"]
    s.text(36, 380, l1, "disp", 104, INK, cls="r d3")
    s.runs(36, 476, [(l2a, INK), (l2b, SIGL)], "disp", 104, cls="r d4")

    s.hline(40, W - 40, H - 40, cls="r d5")
    s.text(40, H - 16, C.HERO["foot"], "mono", 12, INK3, cls="r d6")
    s.text(W - 40, H - 16, C.HERO["foot_r"], "mono", 12, INK3, anchor="end",
           cls="r d6")
    save("hero.svg", s)


# ------------------------------------------------------- section heads

HH = 178  # altura do bloco de cabeçalho no topo de cada placa


def head(s, slug, pad=40):
    """Índice, título e fio: o cabeçalho de seção do portfólio, embutido na
    placa. Fica igual no tema claro e no escuro do GitHub — o <picture> com
    prefers-color-scheme não sobrevive ao link que o GitHub põe no <img>."""
    idx, title, aside = C.HEADS[slug]
    size = 84
    while width("disp", title, size) > s.w - pad * 2:
        size -= 2
    s.text(pad, 50, idx, "mono", 13, SIGL)
    s.text(s.w - pad, 50, aside, "mono", 13, INK3, anchor="end")
    s.text(pad - 3, 142, title, "disp", size, INK)
    s.hline(pad, s.w - pad, HH - 1)


# ---------------------------------------------------------------- craft

def craft_cell(s, x, y, i, item):
    title, body, case = item
    pad = 40
    s.text(x + pad, y + 54, f"{i:02d}", "mono", 14, SIGL)
    yy = y + 104
    for line in C.wrap_title(title, 30, CW - pad * 2):
        s.text(x + pad, yy, line, "title", 30, INK)
        yy += 34
    yy = s.para(x + pad, yy + 14, body, "sans", 18, INK2, CW - pad * 2, 28)
    s.text(x + pad, yy + 22, case, "mono", 12, INK3)
    return yy + 22 + 42 - y


def craft():
    items = C.CRAFT
    rows = [items[i:i + 2] for i in range(0, len(items), 2)]
    heights = [max(craft_cell(Svg(1, 1, ""), 0, 0, 1, it) for it in row)
               for row in rows]
    H = HH + sum(heights)
    s = Svg(W, H, "The craft", C.alt_craft())
    s.rect(0, 0, W, H, fill=BASE)
    head(s, "craft")
    y, n = HH, 1
    for row, h in zip(rows, heights):
        for c, it in enumerate(row):
            craft_cell(s, c * CW, y, n, it)
            n += 1
        y += h
        if y < H:
            s.hline(0, W, y)
    s.vline(CW, HH, H)
    s.rect(.5, .5, W - 1, H - 1, stroke=INK, op=0.14)
    corners(s, 0, 0, W, H)
    save("craft.svg", s)


# ------------------------------------------------------------- projects

def bullets(s, x, y, items, size, lh, maxw, gap):
    for b in items:
        s.rect(x, round(y - size * 0.36), 14, 1.6, fill=SIGL)
        y = s.para(x + 28, y, b, "sans", size, INK2, maxw - 28, lh) + gap
    return y - gap


def link(s, x, y, label, size=14):
    s.text(x, y, label, "mono", size, INK)
    w = width("mono", label, size)
    s.arrow(x + w + 6, y - size * 0.72, size * 0.66, SIGL)
    s.hline(x, x + w + size + 2, y + 9, color=INK, op=0.35)


def featured():
    p = C.BIRDY
    pad, lw, rx, kw = 40, 640, 690, 88
    rw = W - rx - pad

    def draw(s):
        s.text(pad, 66, p["label"], "mono", 14, SIGL)
        s.text(pad - 3, 160, p["name"], "disp", 92, INK)
        y = s.para(pad, 214, p["summary"], "sans", 23, INK, lw - pad, 33)
        y = bullets(s, pad, y + 26, p["bullets"], 18, 28, lw - pad, 14)
        y = s.chips(pad, y + 30, p["chips"], lw - pad)
        link(s, pad, y + 56, p["link"])
        left = y + 56 + 52
        # A placa de especificação: chave e valor, como numa etiqueta de
        # equipamento — no lugar de uma imagem que eu não devo escolher.
        ry = 74
        s.text(rx, 66, p["spec_title"], "mono", 12, INK3)
        for k, v in p["spec"]:
            s.hline(rx, W - pad, ry + 18)
            s.text(rx, ry + 50, k, "mono", 11, INK3)
            vy = ry + 50
            for line in C.wrap_mono(v, 13, rw - kw):
                s.text(rx + kw, vy, line, "mono", 13, INK)
                vy += 20
            ry = vy - 20 + 14
        s.hline(rx, W - pad, ry + 18)
        return max(left, ry + 60)

    BH = draw(Svg(1, 1, ""))
    H = HH + BH
    s = Svg(W, H, f"Projects — {p['name']}, {p['label']}", C.alt_project(p))
    s.rect(0, 0, W, H, fill=BASE)
    head(s, "projects")
    s.rect(0, HH, W, BH, fill=SURF)
    s.add(f'<defs><radialGradient id="g" cx="{W - 120}" cy="{H}" r="520" '
          f'gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{SIG}" '
          f'stop-opacity=".16"/><stop offset="1" stop-color="{SIG}" '
          f'stop-opacity="0"/></radialGradient></defs>')
    s.rect(0, HH, W, BH, fill="url(#g)")
    s.rect(.5, .5, W - 1, H - 1, stroke=INK, op=0.14)
    s.hline(0, W, HH + .5)
    corners(s, 0, 0, W, H)
    s.add(f'<g transform="translate(0 {HH})">')
    draw(s)
    s.add("</g>")
    save("project-birdy.svg", s)


def card_draw(s, p, H=None):
    pad = 40
    s.text(pad, 60, p["label"], "mono", 13, SIGL)
    s.text(pad - 2, 132, p["name"], "disp", 60, INK)
    y = s.para(pad, 180, p["summary"], "sans", 20, INK, CW - pad * 2, 29)
    y = bullets(s, pad, y + 22, p["bullets"], 17, 26, CW - pad * 2, 12)
    y = s.chips(pad, y + 26, p["chips"], CW - pad * 2, size=13)
    if H is None:
        return y + 44 + 54
    link(s, pad, H - 42, p["link"], 13)
    return H


def cards():
    H = max(card_draw(Svg(1, 1, ""), p) for p in C.CARDS)
    for p in C.CARDS:
        s = Svg(CW, H, f"{p['name']} — {p['label']}", C.alt_project(p))
        s.rect(0, 0, CW, H, fill=SURF)
        s.rect(.5, .5, CW - 1, H - 1, stroke=INK, op=0.14)
        corners(s, 0, 0, CW, H)
        card_draw(s, p, H)
        save(f"project-{p['slug']}.svg", s)


# ------------------------------------------------------------- boundary

def boundary():
    b = C.BOUNDARY
    pad, gap = 40, 22
    nw = (W - pad * 2 - gap * 4) / 5
    top = 172

    def node_h(n):
        lines = len(C.wrap_sans(n[3], 16, nw - 36))
        return 112 + lines * 23 + 26

    nh = max(node_h(n) for n in b["nodes"])
    rail = top + nh + 44
    notes_y = rail + 74
    note_lines = max(len(C.wrap_sans(t, 17, (W - pad * 2 - 48) / 2)) for _, t in b["notes"])
    BH = notes_y + 64 + note_lines * 26 + 36
    H = HH + BH

    s = Svg(W, H, "Where automation stops", C.alt_boundary())
    gate_x = pad + 3 * (nw + gap)
    # O pacote atravessa o trilho e PARA no portão humano antes de seguir.
    stop = gate_x + nw / 2 - pad
    end = W - pad * 2 - nw / 2
    s.css.append(
        "@keyframes trip{0%{transform:translateX(0);opacity:0}4%{opacity:1}"
        f"34%{{transform:translateX({stop - 40:.0f}px)}}"
        f"40%,66%{{transform:translateX({stop:.0f}px)}}"
        f"88%{{transform:translateX({end:.0f}px);opacity:1}}"
        f"96%,100%{{transform:translateX({end:.0f}px);opacity:0}}}}"
        "@keyframes hold{0%,38%{stroke-opacity:0}44%,64%{stroke-opacity:1}"
        "70%,100%{stroke-opacity:0}}"
        f".pk{{animation:trip 7s {C.EASE_IO} infinite}}"
        ".gt{animation:hold 7s linear infinite}"
        "@media (prefers-reduced-motion:reduce){.pk{display:none}.gt{animation:none}}"
    )
    s.rect(0, 0, W, H, fill=WELL)
    s.rect(.5, .5, W - 1, H - 1, stroke=INK, op=0.14)
    corners(s, 0, 0, W, H)
    head(s, "boundary")
    s.add(f'<g transform="translate(0 {HH - 8})">')
    s.para(pad, 72, b["lead"], "title", 26, INK, 900, 32)

    for i, (idx, role, name, desc, gate) in enumerate(b["nodes"]):
        x = pad + i * (nw + gap)
        fill, ink, sub, red = (SIG, INK, INK, INK) if gate else \
            (SURF, INK, INK2, SIGL)
        s.rect(x, top, nw, nh, fill=fill, stroke=None if gate else INK, op=0.18)
        if gate:
            s.add(f'<rect x="{x - 6}" y="{top - 6}" width="{nw + 12}" '
                  f'height="{nh + 12}" fill="none" stroke="{SIGL}" '
                  f'stroke-width="1.5" class="gt"/>')
        s.text(x + 18, top + 32, idx, "mono", 12, red)
        s.text(x + 18, top + 56, role, "monom", 11, sub if gate else INK3)
        s.text(x + 18, top + 94, name, "title", 21, ink)
        y = top + 126
        for line in C.wrap_sans(desc, 16, nw - 36):
            s.text(x + 18, y, line, "sans", 16, sub)
            y += 23
        if i < 4:
            ax = x + nw + 4
            s.add(f'<path d="M{ax} {top + nh / 2}h{gap - 8}m-5 -4l5 4l-5 4" '
                  f'fill="none" stroke="{INK3}" stroke-width="1.4"/>')
        s.vline(x + nw / 2, top + nh, rail - 6, op=0.2)
        s.add(f'<rect x="{x + nw / 2 - 3}" y="{rail - 3}" width="6" height="6" '
              f'fill="{SIGL if gate else INK3}"/>')
    s.hline(pad, W - pad, rail, op=0.3)
    s.add(f'<rect class="pk" x="{pad + nw / 2 - 7}" y="{rail - 7}" width="14" '
          f'height="14" fill="{SIGL}"/>')

    s.hline(pad, W - pad, notes_y)
    colw = (W - pad * 2 - 48) / 2
    for i, (t, body) in enumerate(b["notes"]):
        x = pad + i * (colw + 48)
        s.text(x, notes_y + 40, f"{i + 1:02d}  {t}", "mono", 12, SIGL)
        s.para(x, notes_y + 74, body, "sans", 17, INK2, colw, 26)
    s.add("</g>")
    save("boundary.svg", s)


# -------------------------------------------------------------- contact

def contact():
    c = C.CONTACT
    pad = 40
    lines = C.wrap_title(c["lead"], 30, 860)
    H = HH + 52 + len(lines) * 36 + 64
    s = Svg(W, H, "Let's talk", c["lead"])
    s.rect(0, 0, W, H, fill=BASE)
    s.add(f'<defs><radialGradient id="g" cx="{W - 140}" cy="{H}" r="420" '
          f'gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{SIG}" '
          f'stop-opacity=".22"/><stop offset="1" stop-color="{SIG}" '
          f'stop-opacity="0"/></radialGradient></defs>')
    s.rect(0, 0, W, H, fill="url(#g)")
    s.rect(.5, .5, W - 1, H - 1, stroke=INK, op=0.14)
    corners(s, 0, 0, W, H)
    head(s, "contact")
    y = HH + 62
    for line in lines:
        s.text(pad, y, line, "title", 30, INK)
        y += 36
    s.rect(pad, y + 4, 7, 7, fill=SIGL)
    s.text(pad + 18, y + 11, c["line"], "mono", 13, INK2)
    save("contact.svg", s)


# ---------------------------------------------------------------- tools

def tools():
    cols, pad = 4, 26
    cw = W / cols
    groups = C.TOOLS
    rows = [groups[i:i + cols] for i in range(0, len(groups), cols)]

    def cell(s, x, y, g):
        label, items = g
        s.text(x + pad, y + 40, label, "mono", 12, SIGL)
        cx, cy, size = x + pad, y + 76, 16
        for it in items:
            w = width("sans", it, size)
            if cx + w > x + cw - pad:
                cx, cy = x + pad, cy + 25
            s.text(cx, cy, it, "sans", size, INK2)
            cx += w + 13
        return cy + 34 - y

    hs = [max(cell(Svg(1, 1, ""), 0, 0, g) for g in r) for r in rows]
    H = HH + sum(hs)
    s = Svg(W, H, "Tools", C.alt_tools())
    s.rect(0, 0, W, H, fill=BASE)
    head(s, "tools")
    y = HH
    for r, h in zip(rows, hs):
        for c, g in enumerate(r):
            cell(s, c * cw, y, g)
        y += h
        if y < H:
            s.hline(0, W, y)
    for c in range(1, cols):
        s.vline(c * cw, HH, H)
    s.rect(.5, .5, W - 1, H - 1, stroke=INK, op=0.14)
    corners(s, 0, 0, W, H)
    save("tools.svg", s)


# -------------------------------------------------------------- buttons

def button(slug, label, solid):
    size, padx, H = 15, 30, 60
    tw = width("monom", label, size)
    Wb = round(tw + padx * 2 + (22 if not solid else 0))
    s = Svg(Wb, H, label)
    if solid:
        s.rect(0, 0, Wb, H, fill=SIG)
        s.text(padx, 37, label, "monom", size, INK)
    else:
        s.rect(.75, .75, Wb - 1.5, H - 1.5, fill=BASE, stroke=INK, op=0.4,
               extra='stroke-width="1.5"')
        s.text(padx, 37, label, "monom", size, INK)
        s.arrow(padx + tw + 8, 24, 10, SIGL)
    save(f"btn-{slug}.svg", s)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    hero()
    craft()
    featured()
    cards()
    boundary()
    tools()
    contact()
    for b in C.BUTTONS:
        button(*b)
