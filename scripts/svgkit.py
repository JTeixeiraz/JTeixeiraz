"""Peças comuns aos SVGs do perfil: paleta NOITE, fontes embutidas e medição.

As fontes vêm do build do portfólio (~/portfolio/out/_next/static/media),
que já baixou Bricolage Grotesque, Geist e Geist Mono. Cada SVG leva só o
subconjunto de glifos que usa, em woff2 base64 — o GitHub serve o SVG como
<img>, e nesse contexto nenhuma fonte externa carrega.
"""

import base64
import glob
import io
import math
import os
from collections import defaultdict
from xml.sax.saxutils import escape

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

MEDIA = os.environ.get(
    "PORTFOLIO_FONTS", "/home/teixas/portfolio/out/_next/static/media"
)


def oklch(L, C, h):
    """oklch → hex sRGB. A paleta do portfólio é declarada em oklch."""
    a, b = C * math.cos(math.radians(h)), C * math.sin(math.radians(h))
    l_ = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m_ = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s_ = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    rgb = (
        4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_,
        -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_,
        -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_,
    )

    def enc(c):
        c = max(0.0, min(1.0, c))
        c = 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055
        return round(c * 255)

    return "#%02x%02x%02x" % tuple(enc(c) for c in rgb)


# Mesmos tokens de src/app/globals.css do portfólio.
BASE = oklch(0.145, 0.012, 264)
SURF = oklch(0.2, 0.013, 264)
SURF2 = oklch(0.255, 0.014, 264)
WELL = oklch(0.105, 0.01, 264)
INK = oklch(0.975, 0.002, 264)
INK2 = oklch(0.76, 0.01, 264)
INK3 = oklch(0.6, 0.012, 264)
SIG = oklch(0.585, 0.218, 27)
SIGD = oklch(0.52, 0.205, 27)
SIGL = oklch(0.7, 0.19, 27)
# Variante para o tema claro do GitHub (só os cabeçalhos de seção usam).
L_INK = BASE
L_INK3 = oklch(0.47, 0.012, 264)

EASE = "cubic-bezier(.16,1,.3,1)"  # ease-out-expo, o mesmo do portfólio


def _pick(pred):
    best, size = None, -1
    for p in glob.glob(os.path.join(MEDIA, "*.woff2")):
        f = TTFont(p)
        if pred(f["name"].getDebugName(1)) and len(f.getBestCmap()) > size:
            best, size = p, len(f.getBestCmap())
    if not best:
        raise SystemExit(f"fonte não encontrada em {MEDIA}")
    return best


class Face:
    """Uma instância estática de uma fonte variável, com medição de largura."""

    def __init__(self, css, pred, axes):
        self.css = css
        var = TTFont(_pick(pred))
        var.flavor = None
        static = instancer.instantiateVariableFont(var, axes)
        buf = io.BytesIO()
        static.save(buf)
        self.blob = buf.getvalue()
        self.font = TTFont(io.BytesIO(self.blob))
        self.cmap = self.font.getBestCmap()
        self.hmtx = self.font["hmtx"]
        self.upm = self.font["head"].unitsPerEm

    def width(self, text, size, ls=0.0):
        units = 0
        for ch in text:
            g = self.cmap.get(ord(ch))
            if g is None:
                raise SystemExit(f"glifo ausente em {self.css}: {ch!r}")
            units += self.hmtx[g][0]
        return units * size / self.upm + ls * len(text)

    def woff2(self, chars):
        f = TTFont(io.BytesIO(self.blob))
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


def _is_geist(n):
    return n.startswith("Geist") and "Mono" not in n


FACES = {
    # .type-display do portfólio: Bricolage 800, wdth 92, opsz 40, caixa alta.
    "disp": Face("disp", lambda n: n.startswith("Bricolage"),
                 {"wght": 800, "wdth": 92, "opsz": 40}),
    # .type-title: Bricolage 700, wdth 100, opsz 24.
    "title": Face("title", lambda n: n.startswith("Bricolage"),
                  {"wght": 700, "wdth": 100, "opsz": 24}),
    "sans": Face("sans", _is_geist, {"wght": 400}),
    "sansm": Face("sansm", _is_geist, {"wght": 500}),
    "mono": Face("mono", lambda n: n.startswith("Geist Mono"), {"wght": 400}),
    "monom": Face("monom", lambda n: n.startswith("Geist Mono"), {"wght": 500}),
}

# Tracking de cada papel tipográfico, em em.
TRACK = {"disp": -0.028, "title": -0.018, "sans": 0.0, "sansm": 0.0,
         "mono": 0.15, "monom": 0.15}


def width(face, text, size):
    return FACES[face].width(text, size, TRACK[face] * size)


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
        ls = TRACK[face] * size
        attrs = [f'x="{x:.1f}"', f'y="{y:.1f}"',
                 f'class="{(face + " " + cls).strip()}"', f'font-size="{size}"']
        if ls:
            attrs.append(f'letter-spacing="{ls:.2f}"')
        attrs.append(f'fill="{fill}"')
        if anchor:
            attrs.append(f'text-anchor="{anchor}"')
        if opacity is not None:
            attrs.append(f'fill-opacity="{opacity}"')
        self.add(f"<text {' '.join(attrs)}>{escape(txt)}</text>")

    def runs(self, x, y, parts, face, size, cls=""):
        """Uma linha com trechos de cores diferentes: [(texto, cor), ...]."""
        ls = TRACK[face] * size
        spans = ""
        for txt, fill in parts:
            self.used[face].update(txt)
            spans += f'<tspan fill="{fill}">{escape(txt)}</tspan>'
        self.add(
            f'<text x="{x:.1f}" y="{y:.1f}" class="{(face + " " + cls).strip()}" '
            f'font-size="{size}" letter-spacing="{ls:.2f}" '
            f'xml:space="preserve">{spans}</text>'
        )

    def para(self, x, y, txt, face, size, fill, maxw, lh, cls=""):
        """Parágrafo quebrado por largura. Devolve o y depois da última linha."""
        for line in wrap(txt, face, size, maxw):
            self.text(x, y, line, face, size, fill, cls=cls)
            y += lh
        return y

    def hline(self, x1, x2, y, color=INK, op=0.14, cls=""):
        self.add(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{color}" '
                 f'stroke-opacity="{op}" stroke-width="1" class="{cls}"/>')

    def vline(self, x, y1, y2, color=INK, op=0.14):
        self.add(f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{color}" '
                 f'stroke-opacity="{op}" stroke-width="1"/>')

    def rect(self, x, y, w, h, fill="none", stroke=None, op=0.14, extra=""):
        s = f' stroke="{stroke}" stroke-opacity="{op}"' if stroke else ""
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" '
                 f'fill="{fill}"{s} {extra}/>')

    def arrow(self, x, y, s, color, cls=""):
        """↗ desenhado: as fontes do portfólio não trazem o glifo."""
        self.add(f'<path d="M{x} {y + s}L{x + s} {y}M{x + s * .3} {y}H{x + s}'
                 f'V{y + s * .7}" fill="none" stroke="{color}" stroke-width="1.6" '
                 f'class="{cls}"/>')

    def chips(self, x, y, items, maxw, size=14, gap=8, color=INK2):
        """Etiquetas mono com borda. Devolve o y da base da última fileira."""
        h, padx = size * 2.1, size * 0.85
        cx = x
        for it in items:
            w = width("mono", it, size) + padx * 2 - TRACK["mono"] * size
            if cx + w > x + maxw:
                cx, y = x, y + h + gap
            self.rect(cx + .5, y + .5, round(w), round(h), stroke=INK, op=0.22)
            self.text(cx + padx, y + h * 0.66, it, "mono", size, color)
            cx += w + gap
        return y + h

    def render(self):
        fonts = "".join(
            f"@font-face{{font-family:'{f}';src:url(data:font/woff2;base64,"
            f"{FACES[f].woff2(chars)}) format('woff2')}}"
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


REVEAL = (
    "@keyframes rise{from{opacity:0;transform:translateY(18px)}"
    "to{opacity:1;transform:none}}"
    "@keyframes fade{from{opacity:0}to{opacity:1}}"
    f".r{{animation:rise 1s {EASE} both}}"
    f".f{{animation:fade 2.4s {EASE} both}}"
    + "".join(f".d{i}{{animation-delay:{i * 0.09:.2f}s}}" for i in range(1, 10))
    + "@media (prefers-reduced-motion:reduce){.r,.f{animation:none}}"
)
