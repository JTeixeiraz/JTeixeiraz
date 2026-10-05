"""Peças comuns aos SVGs do perfil: paleta bento, fontes embutidas e medição.

O GitHub serve cada SVG como <img>, e nesse contexto nenhuma fonte externa
carrega. Então cada arquivo leva só os glifos que usa, em woff2 base64.
As fontes ficam em scripts/fonts (Space Grotesk, Inter e JetBrains Mono,
todas sob a SIL Open Font License — as licenças estão ao lado).
"""

import base64
import io
import os
from collections import defaultdict
from xml.sax.saxutils import escape

from fontTools import subset
from fontTools.ttLib import TTFont

FONTS = os.path.join(os.path.dirname(__file__), "fonts")

# Os blocos ficam sobre fundo transparente: o vão entre eles é a própria
# página do GitHub, clara ou escura. Por isso só há cor dentro dos blocos.
TILE = "#1c1b29"   # bloco escuro
TILE2 = "#262438"  # bloco dentro de bloco
INK = "#f5f3ff"    # texto sobre bloco escuro
DIM = "#aba8c6"    # texto secundário sobre bloco escuro (7:1)
DARK = "#16131f"   # texto sobre bloco colorido
VIOLET = "#6e5cf6"
AMBER = "#ffb547"
MINT = "#3fd9a0"
PINK = "#ff8fb8"
SKY = "#5aaeff"

# Cor de texto que cada cor de bloco pede.
ON = {VIOLET: "#ffffff", AMBER: DARK, MINT: DARK, PINK: DARK, SKY: DARK,
      TILE: INK, TILE2: INK}

R = 22    # raio dos blocos
GAP = 14  # vão entre blocos


class Face:
    """Uma fonte estática com medição de largura e subconjunto em woff2."""

    def __init__(self, path):
        f = TTFont(path, recalcTimestamp=False)
        f.flavor = None
        buf = io.BytesIO()
        f.save(buf)
        self.blob = buf.getvalue()
        self.cmap = f.getBestCmap()
        self.hmtx = f["hmtx"]
        self.upm = f["head"].unitsPerEm
        self.name = os.path.basename(path)

    def width(self, text, size, ls=0.0):
        units = 0
        for ch in text:
            g = self.cmap.get(ord(ch))
            if g is None:
                raise SystemExit(f"glifo ausente em {self.name}: {ch!r}")
            units += self.hmtx[g][0]
        return units * size / self.upm + ls * len(text)

    def woff2(self, chars):
        # Sem recalcular o timestamp: regerar sem mudar texto não muda o SVG.
        f = TTFont(io.BytesIO(self.blob), recalcTimestamp=False)
        opts = subset.Options()
        opts.flavor = "woff2"
        opts.layout_features = ["kern", "liga", "tnum", "case"]
        opts.name_IDs = []
        sub = subset.Subsetter(opts)
        sub.populate(text="".join(sorted(chars)) + " ")
        sub.subset(f)
        buf = io.BytesIO()
        f.flavor = "woff2"
        f.save(buf)
        return base64.b64encode(buf.getvalue()).decode()


def _face(file):
    return Face(os.path.join(FONTS, file))


# nome: (fonte, tracking em em)
FACES = {
    "head": (_face("space-grotesk-700.woff2"), -0.02),
    "headm": (_face("space-grotesk-500.woff2"), -0.01),
    "body": (_face("inter-400.woff2"), 0.0),
    "bodym": (_face("inter-500.woff2"), 0.0),
    "label": (_face("jetbrains-mono-500.woff2"), 0.12),
}


def width(face, text, size):
    f, tr = FACES[face]
    return f.width(text, size, tr * size)


def wrap(text, face, size, maxw):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if cur and width(face, trial, size) > maxw:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


class Svg:
    def __init__(self, w, h, title, desc=""):
        self.w, self.h, self.title, self.desc = w, h, title, desc
        self.defs, self.els, self.css = [], [], []
        self.used = defaultdict(set)

    def add(self, s):
        self.els.append(s)

    def text(self, x, y, txt, face, size, fill, anchor=None, cls="",
             opacity=None):
        self.used[face].update(txt)
        ls = FACES[face][1] * size
        a = [f'x="{x:.1f}"', f'y="{y:.1f}"', f'class="{(face + " " + cls).strip()}"',
             f'font-size="{size}"', f'fill="{fill}"']
        if ls:
            a.append(f'letter-spacing="{ls:.2f}"')
        if anchor:
            a.append(f'text-anchor="{anchor}"')
        if opacity is not None:
            a.append(f'fill-opacity="{opacity}"')
        self.add(f"<text {' '.join(a)}>{escape(txt)}</text>")

    def para(self, x, y, txt, face, size, fill, maxw, lh, cls="", opacity=None):
        """Parágrafo quebrado por largura. Devolve o y da linha seguinte."""
        for line in wrap(txt, face, size, maxw):
            self.text(x, y, line, face, size, fill, cls=cls, opacity=opacity)
            y += lh
        return y

    def tile(self, x, y, w, h, fill, r=R, cls=""):
        self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
                 f'rx="{r}" fill="{fill}" class="{cls}"/>')

    def chip(self, x, y, label, fill, size=11, ink=None):
        """Etiqueta em pílula. Devolve a largura."""
        w = width("label", label, size) + 22
        self.tile(x, y, w, size * 2.3, fill, r=size * 1.15)
        self.text(x + 11 + FACES["label"][1] * size / 2, y + size * 1.55, label,
                  "label", size, ink or ON.get(fill, DARK))
        return w

    def icon(self, ic, x, y, size, color):
        self.add(f'<svg x="{x:.1f}" y="{y:.1f}" width="{size}" height="{size}" '
                 f'viewBox="{ic["viewBox"]}" fill="{color}">{ic["svg"]}</svg>')

    def arrow(self, x, y, s, color, sw=2):
        """↗ desenhado: nenhuma das fontes traz o glifo no subconjunto latino."""
        self.add(f'<path d="M{x} {y + s}L{x + s} {y}M{x + s * .3} {y}H{x + s}'
                 f'V{y + s * .7}" fill="none" stroke="{color}" stroke-width="{sw}" '
                 f'stroke-linecap="round" stroke-linejoin="round"/>')

    def render(self):
        fonts = "".join(
            f"@font-face{{font-family:'{f}';src:url(data:font/woff2;base64,"
            f"{FACES[f][0].woff2(chars)}) format('woff2')}}"
            f".{f}{{font-family:'{f}'}}"
            for f, chars in sorted(self.used.items())
        )
        css = fonts + "text{font-kerning:normal;text-rendering:geometricPrecision}" \
            + "".join(self.css)
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" '
            f'height="{self.h}" viewBox="0 0 {self.w} {self.h}" role="img" '
            f'aria-labelledby="t d">'
            f'<title id="t">{escape(self.title)}</title>'
            f'<desc id="d">{escape(self.desc)}</desc>'
            f"<style>{css}</style><defs>{''.join(self.defs)}</defs>"
            f"{''.join(self.els)}</svg>"
        )


EASE = "cubic-bezier(.16,1,.3,1)"
REVEAL = (
    "@keyframes rise{from{opacity:0;transform:translateY(16px)}"
    "to{opacity:1;transform:none}}"
    f".r{{animation:rise .9s {EASE} both}}"
    + "".join(f".d{i}{{animation-delay:{i * 0.08:.2f}s}}" for i in range(1, 10))
    + "@media (prefers-reduced-motion:reduce){.r{animation:none}}"
)
