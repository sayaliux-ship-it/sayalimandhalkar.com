# Portfolio Design System
**Sayali Mandhalkar · sayalimandhalkar.com**

A reference document for the visual language, tokens, components, and patterns used across the portfolio. All pages share this system — `index.html`, `tenetic.html`, `pur.html`, `about.html`, and others.

---

## Fonts

Loaded from Google Fonts.

| Role | Family | CSS Variable |
|------|--------|--------------|
| Serif (headings, display, pull quotes) | Cormorant Garamond | `var(--serif)` |
| Sans-serif (UI, body, labels) | DM Sans | `var(--sans)` |

```css
--serif: 'Cormorant Garamond', Georgia, serif;
--sans:  'DM Sans', system-ui, sans-serif;
```

Base body: `font-family: var(--sans); font-size: 15px; line-height: 1.65;`

---

## Color Tokens

All defined in `:root` and shared across every page.

### Core Palette

| Token | Value | Use |
|-------|-------|-----|
| `--bg` | `#111111` | Main page background |
| `--bg2` | `#0e0e0e` | Slightly darker surfaces (part headers, alternate sections) |
| `--bg3` | `#1a1a1a` | Raised surfaces (cards, hover states) |
| `--sidebar` | `#000000` | Sidebar panel background |

### Border

| Token | Value | Use |
|-------|-------|-----|
| `--border` | `rgba(255,255,255,0.07)` | Dividers, card edges, sidebar rules |

### Gold (Accent)

The single accent color across the entire portfolio. Used for labels, eyebrows, pull-quote borders, active states, highlights, and shimmer animation.

| Token | Value | Use |
|-------|-------|-----|
| `--gold` | `#c9a96e` | Primary accent — labels, borders, active nav |
| `--gold-lt` | `#dfc08a` | Lighter gold — hover states, emphasis |
| `--gold-dim` | `rgba(201,169,110,0.1)` | Subtle gold fills — badge backgrounds, card hover tints |

### Text

| Token | Value | Use |
|-------|-------|-----|
| `--text` | `#e8e4dc` | Primary text (headings, values, names) |
| `--muted` | `rgba(232,228,220,0.72)` | Secondary text (body copy, descriptions) |
| `--faint` | `rgba(232,228,220,0.55)` | Tertiary text (captions, NDA disclaimers, metadata) |

---

## Typography Scale

### Display / Hero

Used for the main case study title on the hero.

```css
font-family: var(--serif);
font-size: clamp(42px, 6vw, 80px);
font-weight: 300;
line-height: 1.05;
letter-spacing: -0.02em;
color: var(--text);
```

Hero italic subtitle (gold):
```css
font-family: var(--serif);
font-size: clamp(18px, 2.2vw, 26px);
font-weight: 300;
font-style: italic;
color: var(--gold);
```

### Part Number (Shimmer)

The large decorative number on part-header sections (01, 02).

```css
font-family: var(--serif);
font-size: clamp(80px, 12vw, 180px);
font-weight: 300;
line-height: 1;
letter-spacing: -0.03em;
/* shimmer gradient applied via background-clip: text */
animation: shimmerText 3.6s ease-in-out infinite;
```

### Section Headings

Used on part headers (`.ph-title`) and within content sections (`.sec-heading`).

```css
/* Part title */
font-family: var(--serif);
font-size: clamp(36px, 4.5vw, 60px);
font-weight: 300;
line-height: 1.1;
letter-spacing: -0.02em;

/* Section heading */
font-family: var(--serif);
font-size: clamp(32px, 4vw, 52px);
font-weight: 300;
line-height: 1.1;
letter-spacing: -0.01em;
```

Italic emphasis inside headings: `color: var(--gold); font-style: italic;`

### Pull Quotes

```css
font-family: var(--serif);
font-size: clamp(17px, 1.5vw, 21px);
font-weight: 300;
font-style: italic;
line-height: 1.7;
border-left: 2px solid var(--gold);
padding-left: 24px;
max-width: 640px;
```

### Body Text

```css
font-size: 0.95rem;
line-height: 1.9;
color: var(--muted);
```

Stacked paragraphs: `margin-top: 18px` between adjacent `.body-text` elements.

### Labels / Eyebrows

Uppercase tracking labels used above headings and section titles.

```css
font-size: 0.6rem – 0.68rem;
font-weight: 500 – 600;
letter-spacing: 0.24em – 0.28em;
text-transform: uppercase;
color: var(--gold);
display: flex;
align-items: center;
gap: 10px – 14px;
```

Eyebrow line element (`.eline` / `::before`): `width: 22–28px; height: 1px; background: var(--gold);`

### Captions

```css
font-size: 0.8rem;
line-height: 1.6;
color: var(--faint);
font-style: italic;
margin-top: 14px;
```

### Sidebar

```css
/* Name */
font-size: 0.88rem; font-weight: 500; color: var(--text);

/* Role */
font-size: 0.74rem; font-weight: 400; color: var(--muted);

/* Nav item */
font-size: 0.84rem; font-weight: 400; color: var(--muted);

/* Nav section label */
font-size: 0.58rem; font-weight: 500; letter-spacing: 0.24em; text-transform: uppercase;
```

### Meta Grid (Hero)

```css
/* Label */
font-size: 0.6rem; font-weight: 500; letter-spacing: 0.2em; text-transform: uppercase;
color: var(--gold); opacity: 0.75;

/* Value */
font-size: 0.82rem; font-weight: 400; color: var(--text); line-height: 1.4;
```

---

## Spacing

### Page Structure

| Element | Padding |
|---------|---------|
| Sidebar width | `280px` (`var(--sw)`) |
| Main content area | `margin-left: var(--sw)` |
| Hero content | `0 100px 72px` |
| Section (`.cs-section`) | `72px 100px` |
| Part header (`.part-header`) | `80px 100px 64px` |
| Image group (`.img-group`) | `0 100px`, `margin-bottom: 56px` |
| NDA disclaimer | `margin: 48px 100px`, `padding: 24px 28px` |

### Component Spacing

| Element | Value |
|---------|-------|
| Section label → heading gap | `margin-bottom: 20px` on label |
| Heading → body gap | `margin-bottom: 24px` on heading |
| Pull quote margin | `20px 0 16px` |
| Card padding | `32px 28px` |
| Meta cell padding | `20px 22px` |
| Sidebar profile area | `padding: 28px 22px 24px` |

---

## Layout

### Global

```
Fixed sidebar (280px) + flex-grow main content area
```

The sidebar is `position: fixed`, and the main content uses `margin-left: var(--sw)` to avoid overlap.

### Part Header Grid

Part headers use a 2-column CSS Grid to place the content beside the large decorative number.

```css
.part-header {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 0 40px;
  align-items: start;
}
```

On mobile (`max-width: 960px`): collapses to single column, number hidden.

### Workflow / Journey Cards

```css
display: grid;
grid-template-columns: 1fr 1fr;
gap: 20px;
```

### Hero Meta Grid

```css
display: grid;
grid-template-columns: repeat(4, 1fr);
gap: 1px;
max-width: 780px;
```

---

## Components

### Sidebar

- Fixed, full-height, `280px` wide
- Top accent: `border-top: 2px solid var(--gold)`
- Navigation rows animated in with `rowIn` keyframe, staggered with `animation-delay`
- Collapse toggle persists collapsed state per user
- Active nav item: gold dot indicator + `color: var(--gold)`

### Hero Section

- Full-width `min-height: 80vh` with cover image
- Gradient overlay: transparent → `rgba(10,12,20,0.92)` bottom
- NDA badge: pill with gold border, `position: absolute; top: 40px; right: 100px`
- Hero meta: 4-column grid, frosted-glass cells

### Part Header (`.part-header`)

- Background: `var(--bg2)`
- `border-top: 1px solid var(--border)`
- Left column: label + title + pull quote + description
- Right column: large shimmer part number (`01`, `02`)
- Pull quote: `border-left: 2px solid var(--gold)`

### Content Section (`.cs-section`)

- Padding: `72px 100px`
- Divided by `border-top: 1px solid var(--border)`
- Contains: `.sec-label` → `.sec-heading` → `.body-text` paragraphs

### Image Group (`.img-group`)

- Individual full-width image blocks
- `padding: 0 100px; margin-bottom: 56px`
- Each image: `border-radius: 12px; border: 1px solid rgba(255,255,255,0.07)`
- Caption below: `.cs-img-caption` in faint italic

### Workflow Cards (`.workflow-card`)

- Background: `var(--bg3)`
- Border: `1px solid rgba(201,169,110,0.2)`
- Hover: border brightens to `rgba(201,169,110,0.45)` + soft gold box-shadow
- `border-radius: 8px; padding: 32px 28px`

### NDA Disclaimer

```css
border-left: 3px solid var(--gold);
background: rgba(201,169,110,0.04);
border-radius: 0 6px 6px 0;
padding: 24px 28px;
```

### NDA Badge

```css
background: rgba(201,169,110,0.12);
border: 1px solid rgba(201,169,110,0.4);
border-radius: 100px;
padding: 6px 14px;
```

### Blockquotes / Callout Quotes

```css
font-family: var(--serif);
font-size: 1.1rem;
font-style: italic;
color: var(--text);
border-left: 2px solid var(--gold);
padding-left: 24px;
```

---

## Animations

All defined as `@keyframes` and applied via `animation` property.

### `sidebarIn`

Sidebar entrance — fades in and slides from left.

```css
@keyframes sidebarIn {
  from { opacity: 0; transform: translateX(-20px); }
  to   { opacity: 1; transform: translateX(0); }
}
```

Duration: `0.6s cubic-bezier(0.16,1,0.3,1)`

### `rowIn`

Nav row entrance — staggered fade-up for sidebar items.

```css
@keyframes rowIn {
  from { opacity: 0; transform: translateY(6px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

Stagger: each row adds `0.05s` to `animation-delay`.

### `dotRipple`

Active nav dot pulse — rings expand and fade.

```css
@keyframes dotRipple {
  0%   { transform: scale(1); opacity: 0.8; }
  100% { transform: scale(2.8); opacity: 0; }
}
```

### `shimmerText`

Scrolling gold shimmer across large text (part numbers, display type).

```css
@keyframes shimmerText {
  0%   { background-position: 200% 0; }
  50%  { background-position: -50% 0; }
  100% { background-position: 200% 0; }
}
```

Duration: `3.6s ease-in-out infinite`

Gradient: `linear-gradient(105deg, rgba(201,169,110,0.22) 0%, rgba(201,169,110,0.22) 38%, rgba(245,230,192,0.55) 48%, rgba(255,253,247,0.65) 52%, rgba(201,169,110,0.22) 58%, rgba(201,169,110,0.22) 100%)`

Applied via: `background-clip: text; -webkit-text-fill-color: transparent;`

### `gateIn`

Password gate entrance — card slides up and fades in.

```css
@keyframes gateIn {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

### `shake`

Password input error — horizontal shake on wrong code.

```css
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  20%, 60% { transform: translateX(-8px); }
  40%, 80% { transform: translateX(8px); }
}
```

### `unlockPop`

Gate dismissal — scales up and fades out after correct password.

```css
@keyframes unlockPop {
  0%   { opacity: 1; transform: scale(1); }
  60%  { opacity: 1; transform: scale(1.04); }
  100% { opacity: 0; transform: scale(0.97); }
}
```

### Scroll Reveal (`.reveal` → `.visible`)

All major sections (`.cs-section`, `.part-header`, `.img-group`) start hidden and animate in as they enter the viewport.

```css
.reveal {
  opacity: 0;
  transform: translateY(22px);
  transition: opacity 0.7s ease, transform 0.7s ease;
}
.reveal.visible {
  opacity: 1;
  transform: none;
}
```

Powered by `IntersectionObserver` with `threshold: 0.08`.

---

## Breakpoints

Single breakpoint at `960px`. The portfolio is desktop-first.

```css
@media (max-width: 960px) {
  :root { --sw: 0px; }
  /* Sidebar becomes hidden / toggled */
  /* Part header collapses to single column, ph-number hidden */
  /* All paddings reduce to 28px horizontal */
  /* Hero meta collapses to 2 columns */
}
```

---

## Focus & Accessibility

```css
:focus-visible {
  outline: 2px solid var(--gold);
  outline-offset: 3px;
  border-radius: 2px;
}
:focus:not(:focus-visible) { outline: none; }
```

Decorative elements (large part numbers) carry `aria-hidden="true"`.

---

## Password Gate

Projects that require a password use a shared gate pattern.

- Gate `div` is `position: fixed; inset: 0; z-index: 9999`
- Background: `rgba(0,0,0,0.97)` with frosted glass card
- Input: custom styled, no browser outline, gold focus ring
- Correct code stored as `btoa('XXXX')` — compared against `btoa(input.value.trim())`
- On success: `unlockPop` animation → gate removed from DOM
- On failure: `shake` animation + error message

---

## Naming Conventions

| Prefix | Scope |
|--------|-------|
| `cs-` | Case study layout (hero, section, image) |
| `ph-` | Part header sub-elements (label, title, pull, number) |
| `sb-` | Sidebar sub-elements (profile, avatar, name, row) |
| `sec-` | Section-level utilities (label, heading) |
| `nda-` | NDA-related UI (badge, disclaimer) |
| `img-` | Image grouping utilities |
| `workflow-` | Workflow card component |
