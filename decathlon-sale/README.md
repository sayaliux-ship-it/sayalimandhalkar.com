# Decathlon — "Your Next Move, 25% Off" sale homepage

Local build of the design handoff in `~/Downloads/design_handoff_decathlon_sale_homepage`.
Plain HTML/CSS/JS, no build step.

## Run it

```bash
python3 /Users/sayalim/Documents/AI/decathlon-sale/serve.py 4321
```

Then open http://localhost:4321/

## Files

| File | What it is |
|---|---|
| `index.html` | Page markup — 13 sections in the handoff's DOM order |
| `styles.css` | All styling. Tokens in `:root`, sections in handoff order, responsive rules at the end |
| `script.js` | Countdown — one `campaignEndsAt` timestamp drives all three clocks |
| `serve.py` | Static file server for local preview |
| `assets/` | Imagery copied from the handoff |
| `campaign/` | Campaign extensions — email, social and display (below) |

## Campaign

Everything in `campaign/` is a standalone HTML artboard at its true pixel size, sharing the
homepage's tokens and graphic devices. Open any of them directly in the browser.

| File | Format |
|---|---|
| `email-01-launch.html` | Launch email, 600px, table-built with inline styles |
| `email-02-picks.html` | Product/budget email, 600px |
| `email-03-lastchance.html` | Urgency email, 600px |
| `ig-01-keyvisual.html` … `ig-04-type.html` | Feed posts, 1080 × 1080 |
| `carousel-1.html` … `carousel-3.html` | Carousel frames, 1080 × 1080 |
| `story-01-keyvisual.html`, `story-02-countdown.html` | Stories, 1080 × 1920 |
| `banner-300x250` / `728x90` / `160x600` / `970x250` | IAB display units |
| `_artboard.css` | Shared tokens and devices for the artboards (emails are self-contained) |
| `gif/` | Animated units + the script that renders them |

### Motion

`campaign/gif/build_gifs.py` renders six animated GIFs on three motion concepts — re-run
it after any change to the offer, the crops or the copy:

```bash
python3 decathlon-sale/campaign/gif/build_gifs.py
```

| Concept | What it does | Units |
|---|---|---|
| **Sweep** | A skewed yellow bar wipes across; the composition behind it has changed. Three states, two wipes. | `banner-300x250.gif`, `social-square-sweep.gif` |
| **Count** | Kinetic type on flat colour; the discount counts 0 → 25 as the slab grows. No photography, so it stays sharp and light. | `banner-728x90.gif`, `social-square-count.gif` |
| **Reveal** | Slow push-in on the photography, product rising, type settling. | `banner-160x600.gif`, `email-hero-600x300.gif` |

Display units run under 5s and loop three times — inside the IAB 15-second ceiling — and
hold their end card for 1.4s. Social cuts loop continuously. Feed platforms take MP4
rather than GIF; production display would ship as HTML5 under the exchange weight cap.

Each build writes two sets: the nominal-size files for production, and `@2x` files for
HiDPI display (what the case study page shows, at half size, so they land pixel-for-pixel
on a retina screen). `python3 build_gifs.py --1x-only` skips the retina set.

| File | 1× | @2x |
|---|---|---|
| `banner-728x90` | 45 KB | 73 KB |
| `banner-300x250` | 86 KB | 202 KB |
| `social-square-count` | 209 KB | 350 KB |
| `email-hero-600x300` | 260 KB | 613 KB |
| `social-square-sweep` | 266 KB | 656 KB |
| `banner-160x600` | 569 KB | 1.9 MB |

Three things decide whether a hand-rolled GIF looks sharp: draw at 2× and deliver at 2×
(never let the browser upscale), quantise the whole animation against one 256-colour
global palette with **dithering off** (dithering speckles flat brand colour and fuzzes
type edges), and write **delta frames** — `disposal=1`, so each frame stores only the
region that changed.

Type is set in Helvetica Neue Condensed Bold (sheared for the campaign italic) because
Roboto Condensed isn't installed system-wide; swap the font path in the script for
production renders.

The emails stack to one column below 600px and fall back to Arial where Roboto Condensed
isn't supported. The case study that presents all of this lives at `../decathlon.html`.

## What was implemented

- Exact colours, type sizes, letter-spacing, skews and clip-paths from the handoff at the
  1440px canvas; no border radius anywhere.
- Type and gutters interpolate down to a 375px floor (`clamp()` in `:root`), following the
  handoff's suggested steps: 122→56, 88→40, 58→34, gutters 72→20.
- Responsive: hero stacks type-over-photo below 900px, category strip becomes a horizontal
  snap scroller below 1180px, product row becomes feature-then-2×2 (then 1 column below
  760px), budget columns and the sale index stack.
- Countdown starts at 47:23:59, persists across reloads in `localStorage`, ticks per second,
  and hides the sale bar and urgency band when it hits zero.
- Hover states from the handoff (yellow CTAs → white, links → blue/yellow, tiles → grey,
  index rows → blue top border) with a 120ms ease-out transition.

## Not wired up

Links point at in-page anchors (`#products`, `#categories`) as in the prototype — swap for
real PLP/PDP routes. Product, category, budget and index content is hardcoded; source it
from the campaign feed. Cutouts are the handoff's 300×300 originals — get 2× exports before
production.
