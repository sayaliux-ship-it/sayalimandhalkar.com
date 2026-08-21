#!/usr/bin/env python3
"""
Animated campaign units for "Your Next Move".

    python3 build_gifs.py

Three motion concepts, not one applied five times:

  SWEEP   the −14° campaign line is the transition. A yellow bar wipes across the
          frame and the composition behind it has changed. Three states, two wipes.
          Athletic, and it earns the graphic device instead of decorating with it.

  COUNT   kinetic typography on flat colour. The discount counts up 0 → 25 while the
          slab grows to meet it. No photography, so it stays razor sharp at any size
          and compresses to a fraction of the others.

  REVEAL  a slow push-in on the photography with the product rising into frame and
          type settling on top. The quiet one — for the email hero and the skyscraper,
          where the reader is already stopped.

Quality notes: every frame is drawn at 2× and resampled down (supersampling), and the
whole animation is quantised against one global palette so colours don't shimmer
between frames — the two things that make hand-rolled GIFs look soft and dirty.

Type is Helvetica Neue Condensed Bold, sheared for the campaign italic; swap FONT_FILE
for Roboto Condensed when it is installed.
"""

import math, os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, "..", "..", "assets"))

BLUE, BLUE_D = (0, 130, 195), (0, 86, 127)
YELLOW, RED, INK, WHITE = (255, 234, 40), (227, 38, 47), (26, 42, 52), (255, 255, 255)

FONT_FILE = "/System/Library/Fonts/HelveticaNeue.ttc"
FACES = {"cond": 4, "bold": 1, "reg": 0}
SS = 2                      # supersample factor
SCALE = 1                   # 1 = deliver at nominal size, 2 = deliver the @2x retina cut

_fonts = {}
def font(px, face="cond"):
    key = (px, face)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(FONT_FILE, px, index=FACES[face])
    return _fonts[key]


# ── canvas ───────────────────────────────────────────────────────────────────

class Frame:
    """Drawn at 2×, delivered at 1×. All coordinates are in design units."""

    def __init__(self, w, h, vertical=False):
        self.w, self.h = w, h
        self.img = Image.new("RGBA", (w * SS, h * SS), BLUE + (255,))
        self.gradient(vertical)

    def gradient(self, vertical):
        w, h = self.img.size
        span = h if vertical else w
        strip = Image.new("RGB", (1, span) if vertical else (span, 1))
        px = strip.load()
        for i in range(span):
            f = min(1.0, i / max(1, span - 1) * 1.35)
            c = tuple(int(BLUE_D[j] + (BLUE[j] - BLUE_D[j]) * f) for j in range(3))
            px[0, i] if vertical else px[i, 0]
            strip.putpixel((0, i) if vertical else (i, 0), c)
        self.img.paste(strip.resize((w, h), Image.BILINEAR), (0, 0))

    def draw(self):
        return ImageDraw.Draw(self.img)

    def skew_box(self, x, y, w, h, fill, deg=10, alpha=255):
        if w <= 0 or h <= 0:
            return
        k = math.tan(math.radians(deg))
        x, y, w, h = x * SS, y * SS, w * SS, h * SS
        layer = Image.new("RGBA", self.img.size, (0, 0, 0, 0))
        ImageDraw.Draw(layer).polygon(
            [(x + k * h, y), (x + k * h + w, y), (x + w, y + h), (x, y + h)],
            fill=fill + (alpha,))
        self.img.alpha_composite(layer)

    def bar(self, x, w, deg=14, fill=YELLOW, alpha=255):
        """A full-height motion line."""
        self.skew_box(x, -20, w, self.h + 40, fill, deg, alpha)

    def text(self, x, y, s, size, fill, italic=False, face="cond", track=0, alpha=255, right=False):
        f = font(int(size * SS), face)
        tr = track * SS
        wpx = int(sum(f.getlength(c) for c in s) + tr * max(0, len(s) - 1))
        pad = int(size * SS * 0.6)
        layer = Image.new("RGBA", (wpx + pad * 2, int(size * SS * 1.7)), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        cx = pad
        for ch in s:
            d.text((cx, int(size * SS * 0.18)), ch, font=f, fill=fill + (alpha,))
            cx += f.getlength(ch) + tr
        if italic:
            k = math.tan(math.radians(12))
            lw, lh = layer.size
            layer = layer.transform((lw + int(k * lh), lh), Image.AFFINE,
                                    (1, k, -k * lh, 0, 1, 0), resample=Image.BICUBIC)
        px = x * SS - pad
        if right:
            px = x * SS - wpx - pad
        self.img.alpha_composite(layer, (int(px), int(y * SS - size * SS * 0.18)))

    def arrow(self, x, y, w, fill, alpha=255):
        x, y, w = x * SS, y * SS, w * SS
        layer = Image.new("RGBA", self.img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        d.line([(x, y), (x + w * 0.72, y)], fill=fill + (alpha,), width=max(2, int(w * 0.13)))
        d.polygon([(x + w * 0.62, y - w * 0.3), (x + w, y), (x + w * 0.62, y + w * 0.3)],
                  fill=fill + (alpha,))
        self.img.alpha_composite(layer)

    def paste(self, im, x, y, alpha=255):
        if alpha < 255:
            im = im.copy()
            im.putalpha(im.getchannel("A").point(lambda a: int(a * alpha / 255)))
        self.img.alpha_composite(im, (int(x * SS), int(y * SS)))

    def out(self):
        rgb = self.img.convert("RGB")
        if SCALE >= SS:
            return rgb                      # @2x: ship the supersampled buffer untouched
        return rgb.resize((self.w * SCALE, self.h * SCALE), Image.LANCZOS)


def text_w(s, size, track=0, face="cond"):
    f = font(int(size * SS), face)
    return (sum(f.getlength(c) for c in s) + track * SS * max(0, len(s) - 1)) / SS


# ── assets ───────────────────────────────────────────────────────────────────

_photo = None
def photo(box, focus=(0.58, 0.40), diagonal=0.16, zoom=1.0, scrim=0.82):
    """Hero photography, diagonal left edge, scrim so type stays legible on it."""
    global _photo
    if _photo is None:
        _photo = Image.open(os.path.join(ASSETS, "hero.png")).convert("RGB")
    x, y, w, h = [v * SS for v in box]
    w, h = int(w), int(h)
    src = _photo
    sw, sh = src.size
    scale = max(w / sw, h / sh) * zoom
    im = src.resize((int(sw * scale), int(sh * scale)), Image.LANCZOS)
    ox = int((im.size[0] - w) * focus[0])
    oy = int((im.size[1] - h) * focus[1])
    im = im.crop((ox, oy, ox + w, oy + h))

    panel = Image.new("RGBA", (w, h))
    panel.paste(im, (0, 0))
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).polygon([(w * diagonal, 0), (w, 0), (w, h), (0, h)], fill=255)

    ramp = Image.new("L", (w, 1))
    for i in range(w):
        ramp.putpixel((i, 0), int(255 * scrim * max(0.0, 1 - i / (w * 0.66))))
    tint = Image.new("RGBA", (w, h), BLUE + (255,))
    tint.putalpha(ramp.resize((w, h), Image.BILINEAR))
    panel.alpha_composite(tint)
    panel.putalpha(mask)
    return panel, (int(x), int(y))


_cuts = {}
def cutout(name, height):
    key = (name, height)
    if key not in _cuts:
        im = Image.open(os.path.join(ASSETS, name)).convert("RGBA")
        w, h = im.size
        _cuts[key] = im.resize((int(w * height * SS / h), int(height * SS)), Image.LANCZOS)
    return _cuts[key]


_logos = {}
def logo(width):
    if width not in _logos:
        im = Image.open(os.path.join(ASSETS, "decathlon-logo.png")).convert("RGBA")
        w, h = im.size
        _logos[width] = im.resize((int(width * SS), int(h * width * SS / w)), Image.LANCZOS)
    return _logos[width]


def ease(t, p=3):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** p


def overshoot(t):
    """Snap with a small bounce back — used on the kinetic type."""
    t = max(0.0, min(1.0, t))
    return 1 + 2.2 * (t - 1) ** 3 + 1.2 * (t - 1) ** 2


# ── writing the file ─────────────────────────────────────────────────────────

def save(path, frames, duration, loop, colors, hold_ms=1400, dither=True):
    """One global palette for the whole animation — no frame-to-frame colour shift."""
    sample = frames[:: max(1, len(frames) // 12)]
    strip = Image.new("RGB", (frames[0].width, frames[0].height * len(sample)))
    for i, f in enumerate(sample):
        strip.paste(f, (0, i * frames[0].height))
    pal = strip.quantize(colors=colors, method=Image.MEDIANCUT)
    d = Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE
    seq = [f.quantize(palette=pal, dither=d) for f in frames]
    durations = [duration] * len(seq)
    durations[-1] = hold_ms
    # disposal=1 keeps the previous frame on screen, so the encoder can write only the
    # region that actually changed — the difference between a 7 MB file and a 1 MB one
    # on animations that hold a static plate.
    seq[0].save(path, save_all=True, append_images=seq[1:], duration=durations,
                loop=loop, optimize=True, disposal=1)
    kb = os.path.getsize(path) / 1024
    total = (sum(durations)) / 1000
    print(f"  {os.path.basename(path):<26} {len(seq):>3}f  {total:4.1f}s  {kb:7.0f} KB")


# ── concept 1 · SWEEP ────────────────────────────────────────────────────────

def sweep_state(cfg, state, t):
    """Build one of the three compositions the wipes cut between."""
    f = Frame(*cfg["size"])
    p, at = photo(cfg["photo"], diagonal=cfg.get("diag", 0.16))
    f.paste(p, at[0] / SS, at[1] / SS)
    for x, w, col in cfg["lines"]:
        f.bar(x, w, fill=col)
    f.paste(logo(cfg["logo_w"]), *cfg["logo_at"])

    if state == 0:
        for i, line in enumerate(cfg["head"]):
            a = ease((t - 0.06 - i * 0.06) / 0.26)
            if a > 0:
                f.text(cfg["head_at"][0], cfg["head_at"][1] + i * cfg["head_lh"] + (1 - a) * cfg["head_lh"] * 0.5,
                       line, cfg["head_size"], WHITE, italic=True, alpha=int(255 * a))
    elif state == 1:
        sx, sy, sw, sh = cfg["slab"]
        f.skew_box(sx, sy, sw, sh, YELLOW)
        f.text(sx + cfg["slab_pad"], sy + cfg["slab_ty"], cfg["offer"], cfg["offer_size"], INK, italic=True)
        for i, line in enumerate(cfg["support"]):
            f.text(cfg["support_at"][0], cfg["support_at"][1] + i * cfg["support_lh"],
                   line, cfg["support_size"], WHITE, face="reg")
    else:
        f.paste(cutout(*cfg["product"][:2]), *cfg["product"][2])
        sx, sy, sw, sh = cfg["slab"]
        f.skew_box(sx, sy, sw, sh, YELLOW)
        f.text(sx + cfg["slab_pad"], sy + cfg["slab_ty"], cfg["offer"], cfg["offer_size"], INK, italic=True)
        cx, cy, cw, ch = cfg["cta"]
        f.skew_box(cx, cy, cw, ch, RED)
        f.text(cx + cfg["cta_pad"], cy + cfg["cta_ty"], cfg["cta"][4] if len(cfg["cta"]) > 4 else cfg["cta_label"],
               cfg["cta_size"], WHITE, track=1)
        f.arrow(cx + cfg["cta_pad"] + text_w(cfg["cta_label"], cfg["cta_size"], 1) + 6,
                cy + ch * 0.55, cfg["cta_size"] * 0.7, WHITE)
    return f.out()


def build_sweep(path, cfg, fps=11, colors=256):
    w, h = cfg["size"]
    beats = [(0.00, 0.34), (0.34, 0.64), (0.64, 1.00)]      # state windows
    wipes = [0.34, 0.64]                                     # wipe centres
    dur = cfg.get("seconds", 4.2)
    n = int(dur * fps)
    frames = []
    for i in range(n):
        t = i / (n - 1)
        state = 0 if t < wipes[0] else (1 if t < wipes[1] else 2)
        base = sweep_state(cfg, state, (t - beats[state][0]) / (beats[state][1] - beats[state][0]))

        # the wipe itself: a skewed yellow bar dragging the next state in behind it
        for wi, wc in enumerate(wipes):
            span = 0.16
            p = (t - (wc - span)) / span
            if 0 <= p <= 1:
                prev = sweep_state(cfg, wi, 1.0)
                ow, oh = base.size                          # frames may be the @2x cut
                k = math.tan(math.radians(14))
                edge = -oh * k + ease(p) * (ow + oh * k + 40)
                mask = Image.new("L", (ow, oh), 0)
                ImageDraw.Draw(mask).polygon(
                    [(edge, 0), (ow + 400, 0), (ow + 400, oh), (edge - oh * k, oh)], fill=255)
                base = Image.composite(prev, base, mask)     # ahead of the bar: old state
                bw = max(10, int(ow * 0.045))
                bar = Image.new("RGB", (ow, oh))
                ImageDraw.Draw(bar).polygon(
                    [(edge, 0), (edge + bw, 0), (edge + bw - oh * k, oh), (edge - oh * k, oh)], fill=YELLOW)
                bmask = Image.new("L", (ow, oh), 0)
                ImageDraw.Draw(bmask).polygon(
                    [(edge, 0), (edge + bw, 0), (edge + bw - oh * k, oh), (edge - oh * k, oh)], fill=255)
                base = Image.composite(bar, base, bmask)
        frames.append(base)
    save(path, frames, int(1000 / fps), cfg.get("loop", 3), colors, dither=False)


# ── concept 2 · COUNT ────────────────────────────────────────────────────────

def build_count(path, cfg, fps=12, colors=48):
    """Kinetic type on flat colour. No photography — so it stays perfectly crisp."""
    w, h = cfg["size"]
    dur = cfg.get("seconds", 3.6)
    n = int(dur * fps)
    frames = []
    for i in range(n):
        t = i / (n - 1)
        f = Frame(w, h, vertical=cfg.get("vertical", False))
        for x, bw, col in cfg["lines"]:
            travel = ease((t - 0.02) / 0.3)
            f.bar(x - (1 - travel) * w * 0.35, bw, fill=col, alpha=int(255 * min(1, travel * 1.6)))
        f.paste(logo(cfg["logo_w"]), *cfg["logo_at"])

        # headline words snap in with a small overshoot
        for i2, line in enumerate(cfg["head"]):
            a = overshoot((t - 0.05 - i2 * 0.07) / 0.24)
            if a > 0.01:
                x, y = cfg["head_at"]
                f.text(x + (1 - a) * cfg["head_size"] * 0.5,
                       y + i2 * cfg["head_lh"], line, cfg["head_size"], WHITE,
                       italic=True, alpha=int(255 * min(1, a * 1.6)))

        # the number counts up, the slab grows to meet it
        cp = ease((t - 0.34) / 0.30, p=2)
        if cp > 0:
            val = int(round(25 * cp))
            label = f"{val}% OFF"
            sx, sy = cfg["count_at"]
            size = cfg["count_size"]
            tw = text_w(label, size) + cfg["count_pad"] * 2
            f.skew_box(sx, sy, tw, cfg["count_h"], YELLOW)
            f.text(sx + cfg["count_pad"], sy + cfg["count_ty"], label, size, INK, italic=True)
            if cp > 0.98 and cfg.get("count_suffix"):
                f.text(sx + tw + 12, sy + cfg["count_ty"] + cfg.get("suffix_dy", 0),
                       cfg["count_suffix"], cfg["suffix_size"], WHITE, track=2)

        if t > 0.68 and cfg.get("support"):
            a = ease((t - 0.68) / 0.16)
            for i3, line in enumerate(cfg["support"]):
                f.text(cfg["support_at"][0], cfg["support_at"][1] + i3 * cfg["support_lh"],
                       line, cfg["support_size"], WHITE, face="reg", alpha=int(255 * a))

        ca = ease((t - 0.78) / 0.16)
        if ca > 0:
            cx, cy, cw, ch = cfg["cta"]
            f.skew_box(cx, cy, cw, ch, RED, alpha=int(255 * ca))
            f.text(cx + cfg["cta_pad"], cy + cfg["cta_ty"], cfg["cta_label"], cfg["cta_size"],
                   WHITE, track=1, alpha=int(255 * ca))
            f.arrow(cx + cfg["cta_pad"] + text_w(cfg["cta_label"], cfg["cta_size"], 1) + 6,
                    cy + ch * 0.55, cfg["cta_size"] * 0.7, WHITE, alpha=int(255 * ca))
        frames.append(f.out())
    save(path, frames, int(1000 / fps), cfg.get("loop", 3), colors, dither=False)


# ── concept 3 · REVEAL ───────────────────────────────────────────────────────

def build_reveal(path, cfg, fps=10, colors=256):
    """Slow push-in on the photography, product rising, type settling."""
    w, h = cfg["size"]
    dur = cfg.get("seconds", 5.0)
    n = int(dur * fps)
    frames = []
    for i in range(n):
        t = i / (n - 1)
        f = Frame(w, h, vertical=cfg.get("vertical", False))
        amt = cfg.get("push", 0.10) if cfg.get("push", 0.10) is not False else 0.0
        zoom = 1.0 + amt - amt * ease(t, p=1.6)
        p, at = photo(cfg["photo"], focus=cfg.get("focus", (0.58, 0.40)),
                      diagonal=cfg.get("diag", 0.16), zoom=zoom)
        f.paste(p, at[0] / SS, at[1] / SS, alpha=255 if not amt else int(255 * ease(t / 0.18)))
        for x, bw, col in cfg["lines"]:
            a = ease((t - 0.1) / 0.35)
            f.bar(x, bw, fill=col, alpha=int(255 * a))
        f.paste(logo(cfg["logo_w"]), *cfg["logo_at"])

        for i2, line in enumerate(cfg["head"]):
            a = ease((t - 0.14 - i2 * 0.08) / 0.3)
            if a > 0:
                x, y = cfg["head_at"]
                f.text(x, y + i2 * cfg["head_lh"] + (1 - a) * 10, line, cfg["head_size"],
                       WHITE, italic=True, alpha=int(255 * a))

        pa = ease((t - 0.30) / 0.34)
        if pa > 0 and cfg.get("product"):
            name, ph, (px, py) = cfg["product"]
            f.paste(cutout(name, ph), px, py + (1 - pa) * 26, alpha=int(255 * pa))

        sa = ease((t - 0.46) / 0.22)
        if sa > 0:
            sx, sy, sw, sh = cfg["slab"]
            f.skew_box(sx, sy, int(sw * sa), sh, YELLOW)
            if sa > 0.6:
                f.text(sx + cfg["slab_pad"], sy + cfg["slab_ty"], cfg["offer"], cfg["offer_size"], INK, italic=True)

        if cfg.get("support") and t > 0.62:
            a = ease((t - 0.62) / 0.2)
            for i3, line in enumerate(cfg["support"]):
                f.text(cfg["support_at"][0], cfg["support_at"][1] + i3 * cfg["support_lh"],
                       line, cfg["support_size"], WHITE, face="reg", alpha=int(255 * a))

        ca = ease((t - 0.74) / 0.18)
        if ca > 0 and cfg.get("cta"):
            cx, cy, cw, ch = cfg["cta"]
            f.skew_box(cx, cy, cw, ch, RED, alpha=int(255 * ca))
            f.text(cx + cfg["cta_pad"], cy + cfg["cta_ty"], cfg["cta_label"], cfg["cta_size"],
                   WHITE, track=1, alpha=int(255 * ca))
            f.arrow(cx + cfg["cta_pad"] + text_w(cfg["cta_label"], cfg["cta_size"], 1) + 6,
                    cy + ch * 0.55, cfg["cta_size"] * 0.7, WHITE, alpha=int(255 * ca))
        frames.append(f.out())
    save(path, frames, int(1000 / fps), cfg.get("loop", 0), colors, dither=False)


# ── the kit ──────────────────────────────────────────────────────────────────

SWEEP_300 = dict(
    size=(300, 250), photo=(120, 0, 180, 250), diag=0.18, seconds=3.5,
    lines=[(150, 8, YELLOW), (166, 3, WHITE)],
    logo_w=80, logo_at=(16, 14),
    head=["YOUR", "NEXT", "MOVE"], head_at=(16, 66), head_lh=40, head_size=38,
    slab=(16, 96, 150, 40), slab_pad=14, slab_ty=6, offer="25% OFF", offer_size=26,
    support=["No code needed.", "70 sports."], support_at=(16, 152), support_lh=22, support_size=15,
    product=("p-rockrider-cut.png", 128, (152, 112)),
    cta=(16, 200, 132, 32), cta_pad=14, cta_ty=8, cta_label="SHOP THE SALE", cta_size=12,
)

SWEEP_SQUARE = dict(
    size=(600, 600), photo=(234, 0, 366, 600), diag=0.22, seconds=4.0, loop=0,
    lines=[(316, 16, YELLOW), (346, 6, WHITE)],
    logo_w=124, logo_at=(40, 38),
    head=["YOUR", "NEXT", "MOVE"], head_at=(40, 142), head_lh=80, head_size=76,
    slab=(40, 214, 300, 74), slab_pad=20, slab_ty=11, offer="25% OFF", offer_size=50,
    support=["Every sport. Every product.", "No code needed."],
    support_at=(40, 322), support_lh=30, support_size=21,
    product=("p-rockrider-cut.png", 280, (282, 262)),
    cta=(40, 506, 218, 48), cta_pad=19, cta_ty=13, cta_label="SHOP THE SALE", cta_size=17,
)

COUNT_728 = dict(
    size=(728, 90), seconds=3.4,
    lines=[(268, 9, YELLOW), (286, 4, WHITE)],
    logo_w=98, logo_at=(20, 33),
    head=["YOUR NEXT MOVE"], head_at=(140, 28), head_lh=0, head_size=30,
    count_at=(412, 24), count_size=28, count_h=42, count_pad=15, count_ty=7,
    cta=(600, 28, 108, 34), cta_pad=13, cta_ty=9, cta_label="SHOP NOW", cta_size=13,
)

COUNT_SQUARE = dict(
    size=(600, 600), seconds=3.8, loop=0,
    lines=[(386, 17, YELLOW), (416, 6, WHITE)],
    logo_w=124, logo_at=(40, 40),
    head=["YOUR", "NEXT", "MOVE"], head_at=(40, 112), head_lh=74, head_size=70,
    count_at=(40, 364), count_size=56, count_h=84, count_pad=22, count_ty=12,
    count_suffix="SITEWIDE", suffix_size=21, suffix_dy=28,
    support=["Every sport. Every product.", "The discount is already on the price."],
    support_at=(40, 472), support_lh=28, support_size=19,
    cta=(40, 536, 214, 46), cta_pad=18, cta_ty=12, cta_label="SHOP THE SALE", cta_size=17,
)

REVEAL_160 = dict(
    size=(160, 600), vertical=True, photo=(0, 300, 160, 300), diag=0.0, seconds=3.6, push=0.05,
    focus=(0.52, 0.34),
    lines=[(96, 7, YELLOW), (112, 3, WHITE)],
    logo_w=88, logo_at=(14, 18),
    head=["YOUR", "NEXT", "MOVE"], head_at=(14, 70), head_lh=42, head_size=40,
    slab=(14, 202, 122, 36), slab_pad=13, slab_ty=6, offer="25% OFF", offer_size=23,
    support=["70 sports.", "10,000+ items.", "No code needed."],
    support_at=(14, 254), support_lh=21, support_size=14,
    product=("p-rockrider-cut.png", 170, (10, 330)),
    cta=(14, 546, 122, 32), cta_pad=14, cta_ty=8, cta_label="SHOP", cta_size=13,
)

REVEAL_EMAIL = dict(
    size=(600, 300), photo=(276, 0, 324, 300), diag=0.16, seconds=4.2, loop=0, push=False,
    lines=[(292, 12, YELLOW), (314, 5, WHITE)],
    logo_w=104, logo_at=(28, 26),
    head=["YOUR", "NEXT", "MOVE"], head_at=(28, 78), head_lh=54, head_size=50,
    slab=(28, 238, 250, 44), slab_pad=16, slab_ty=8, offer="25% OFF SITEWIDE", offer_size=26,
    product=("p-rockrider-cut.png", 200, (300, 96)),
    cta=None,
)

def build_all(scale):
    global SCALE
    SCALE = scale
    tag = "@2x" if scale > 1 else ""
    def out(name):
        stem, ext = os.path.splitext(name)
        return os.path.join(HERE, stem + tag + ext)
    print(f"— {scale}× —")
    build_sweep(out("banner-300x250.gif"), SWEEP_300, fps=10)
    build_sweep(out("social-square-sweep.gif"), SWEEP_SQUARE, fps=10)
    build_count(out("banner-728x90.gif"), COUNT_728)
    build_count(out("social-square-count.gif"), COUNT_SQUARE, colors=32)
    build_reveal(out("banner-160x600.gif"), REVEAL_160, fps=10)
    build_reveal(out("email-hero-600x300.gif"), REVEAL_EMAIL, fps=10)


if __name__ == "__main__":
    import sys
    if "--1x-only" not in sys.argv:
        build_all(2)          # what the case study displays, at half size
    build_all(1)              # the production weights
    raise SystemExit

    print("SWEEP")
    build_sweep(os.path.join(HERE, "banner-300x250.gif"), SWEEP_300, fps=10, colors=96)
    build_sweep(os.path.join(HERE, "social-square-sweep.gif"), SWEEP_SQUARE, fps=10, colors=128)
    print("COUNT")
    build_count(os.path.join(HERE, "banner-728x90.gif"), COUNT_728)
    build_count(os.path.join(HERE, "social-square-count.gif"), COUNT_SQUARE, colors=32)
    print("REVEAL")
    build_reveal(os.path.join(HERE, "banner-160x600.gif"), REVEAL_160, fps=10, colors=96)
    build_reveal(os.path.join(HERE, "email-hero-600x300.gif"), REVEAL_EMAIL, fps=10, colors=128)
    print("Done.")
