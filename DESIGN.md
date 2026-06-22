---
name: PMFtracker
description: >-
  A confident, data-serious SaaS identity for a product that measures
  product-market fit. The system pairs bright, editorial light surfaces
  (white canvases, crisp slate text, generous whitespace) with dramatic
  deep-indigo-to-near-black gradient "moments" — hero bands, call-to-action
  panels, and the score gauge. One disciplined indigo accent carries every
  link, tag, and button. Numbers are treated as heroes. Optimistic, modern,
  trustworthy — never playful or noisy.

colors:
  # Light canvas & ink
  background: '#ffffff'
  background-soft: '#f8fafc'
  background-tint: '#eef2ff'
  ink: '#0f172a'            # primary headings, strong text
  body: '#334155'           # default body copy
  muted: '#64748b'          # secondary text, captions, meta
  line: '#e2e8f0'           # hairline borders & dividers
  on-dark: '#ffffff'        # text on dark / gradient surfaces
  on-dark-muted: '#cbd5e1'  # secondary text on dark surfaces
  text-purple: '#443a59'    # muted purple-grey (secondary button labels, footers)

  # Primary indigo (the single accent / action color)
  primary: '#4f46e5'
  primary-hover: '#4338ca'
  primary-bright: '#6366f1'
  primary-300: '#818cf8'
  primary-soft: '#eef2ff'   # tinted fills, hover states
  primary-border: '#c7d2fe' # dashed/outline accents

  # Extended brand indigo scale (marketing surfaces)
  brand-25: '#f6f6fc'
  brand-50: '#edeef9'
  brand-100: '#dbddf3'
  brand-200: '#b8bae7'
  brand-300: '#9498dc'
  brand-400: '#7175d0'
  brand-500: '#4d53c4'   # legacy — Webflow + in-product widget indigo; converge on primary #4f46e5
  brand-600: '#3e429d'
  brand-700: '#2e3276'
  brand-800: '#1f214e'
  brand-900: '#0f1127'

  # Dark surfaces (hero bands, CTA panels, primary buttons, overlays)
  surface-dark: '#0f172a'         # slate-black base for gradient panels
  surface-dark-indigo: '#312e81'  # indigo terminus of the panel gradient
  surface-night: '#0a0826'        # near-black base of the pill button
  hero-night: '#080331'           # deepest brand night

  # Legacy Webflow defaults — NOT part of the active system; do not use
  accent-blue: '#2d62ff'
  accent-pink: '#dd23bb'

  # Status & feedback
  success: '#34d399'
  success-soft: '#6ee7b7'
  warning: '#fcd34d'
  danger: '#dc2626'
  danger-soft: '#fca5a5'

typography:
  font-primary: '"Manrope", system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif'
  font-secondary: '"Open Sauce Two", "Manrope", Arial, sans-serif'
  font-mono: '"SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace'

  display:
    fontFamily: Manrope
    fontSize: 'clamp(2.6rem, 6vw, 4.5rem)'
    fontWeight: 700
    lineHeight: 1.04
    letterSpacing: '-0.02em'
  h1:
    fontFamily: Manrope
    fontSize: 'clamp(2rem, 4.5vw, 2.6rem)'
    fontWeight: 700
    lineHeight: 1.12
    letterSpacing: '-0.02em'
  h2:
    fontFamily: Manrope
    fontSize: 'clamp(1.6rem, 3.4vw, 2.1rem)'
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: '-0.015em'
  h3:
    fontFamily: Manrope
    fontSize: '1.25rem'
    fontWeight: 700
    lineHeight: 1.3
  body-lg:
    fontFamily: Manrope
    fontSize: '1.12rem'
    fontWeight: 400
    lineHeight: 1.7
  body:
    fontFamily: Manrope
    fontSize: '1rem'
    fontWeight: 400
    lineHeight: 1.6
  small:
    fontFamily: Manrope
    fontSize: '0.85rem'
    fontWeight: 400
    lineHeight: 1.5
  eyebrow:
    fontFamily: Manrope
    fontSize: '0.78rem'
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: '0.08em'
    textTransform: uppercase
  metric:
    fontFamily: Manrope
    fontSize: 'clamp(3rem, 9vw, 4.25rem)'
    fontWeight: 800
    lineHeight: 1
    letterSpacing: '-0.03em'

spacing:
  unit: '4px'
  xs: '0.5rem'
  sm: '0.75rem'
  md: '1rem'
  lg: '1.5rem'
  xl: '2.5rem'
  2xl: '3.25rem'
  3xl: '5rem'
  content-max: '720px'      # ideal reading measure for articles/body
  content-wide: '980px'     # wider content (tables, feature grids)
  container-max: '80rem'    # outer page container
  section-padding-y: '5rem' # vertical rhythm between major sections

radii:
  sm: '6px'
  DEFAULT: '10px'
  md: '12px'
  lg: '16px'
  xl: '18px'
  2xl: '28px'
  pill: '6.25rem'   # buttons — fully rounded "lozenge"
  full: '9999px'    # bars, chips, avatars

shadows:
  card: '0 6px 28px rgba(29, 27, 46, 0.05)'
  card-hover: '0 18px 40px -24px rgba(15, 23, 42, 0.35)'
  raised: '0 24px 60px -36px rgba(15, 23, 42, 0.4)'
  dropdown: '0 20px 50px -24px rgba(15, 23, 42, 0.4)'
  modal: '0 40px 90px -30px rgba(15, 23, 42, 0.55)'
  glow-indigo: '0 16px 36px -18px #4f46e5'
  focus-ring: '0 0 0 3px rgba(99, 102, 241, 0.15)'

motion:
  duration-fast: '150ms'   # hovers, color/border transitions
  duration-base: '220ms'   # modal/overlay entrances
  duration-slow: '350ms'   # bar fills, button morphs
  easing-standard: 'cubic-bezier(0.2, 0.8, 0.25, 1)'  # gentle, slightly springy
  easing-brand: 'cubic-bezier(0.596, 0.007, 0.25, 1)' # decisive button easing
  easing-ease: 'ease'
  modal-enter: 'opacity 220ms ease, transform 220ms cubic-bezier(0.2, 0.8, 0.25, 1)'
  hover-lift: 'transform 150ms ease, box-shadow 150ms ease'
  focus-visible: '3px solid #6366f1, 2px offset'
  reduced-motion: 'honored — animations and transitions collapse to ~0ms'

gradients:
  # Signature pill button: near-black base with a soft inner top-glow (not flat).
  primary-button: 'radial-gradient(84.92% 150% at 50% 138.75%, rgba(255,255,255,0.24) 0%, rgba(255,255,255,0) 100%), #0a0826'
  # Bright accent fill for chips, secondary buttons, icon badges.
  accent: 'linear-gradient(135deg, #6366f1, #4f46e5)'
  # Dramatic dark panel for CTA bands, featured cards, the score gauge.
  surface-night: 'linear-gradient(135deg, #0f172a 0%, #312e81 100%)'
  # Progress / score bar: indigo travelling into success-green.
  score-bar: 'linear-gradient(90deg, #818cf8, #34d399)'
  # Gradient text used on hero headline accents.
  text-accent: 'linear-gradient(90deg, #818cf8, #c7d2fe)'

components:
  button-primary:
    background: '{gradients.primary-button}'
    textColor: '{colors.on-dark}'
    rounded: '{radii.pill}'
    padding: '1rem 2rem'
    fontWeight: 500
    iconStroke: '#cdc9d5'
    transition: 'all 350ms {motion.easing-brand}'
  button-secondary:
    background: 'transparent'
    textColor: '{colors.text-purple}'
    rounded: '{radii.pill}'
    padding: '0.75rem 1rem'
    fontWeight: 500
  button-accent:
    background: '{gradients.accent}'
    textColor: '#ffffff'
    rounded: '{radii.DEFAULT}'
    padding: '0.65rem 1.1rem'
    fontWeight: 600
  link:
    textColor: '{colors.primary}'
    textDecoration: none
    hoverTextDecoration: underline
  eyebrow-tag:
    background: '{colors.primary-soft}'
    textColor: '{colors.primary}'
    rounded: '{radii.full}'
    typography: '{typography.eyebrow}'
    padding: '0.35rem 0.85rem'
  card-light:
    background: '{colors.background}'
    border: '1px solid {colors.line}'
    rounded: '{radii.lg}'
    shadow: '{shadows.card}'
    hoverShadow: '{shadows.card-hover}'
    padding: '1.5rem'
  card-dark:
    background: '{gradients.surface-night}'
    textColor: '{colors.on-dark}'
    rounded: '{radii.lg}'
    padding: '2.5rem'
  input:
    background: '{colors.background}'
    border: '1px solid #d8dee9'
    rounded: '{radii.DEFAULT}'
    padding: '0.8rem 0.9rem'
    focusBorder: '{colors.primary-bright}'
    focusRing: '{shadows.focus-ring}'
  modal:
    background: '{colors.background}'
    rounded: '{radii.xl}'
    shadow: '{shadows.modal}'
    maxWidth: '440px'
    overlayColor: 'rgba(10, 8, 38, 0.55)'
    overlayBlur: '4px'
    enter: '{motion.modal-enter}'
  metric-gauge:
    background: '{gradients.surface-night}'
    textColor: '{colors.on-dark}'
    metricColor: '{colors.on-dark}'
    barTrack: 'rgba(255, 255, 255, 0.14)'
    barFill: '{gradients.score-bar}'
    rounded: '{radii.md}'
  stat-band:
    number: '{typography.metric}'
    numberFill: '{gradients.accent}'   # gradient-clipped text
    labelColor: '{colors.muted}'
---

# PMFtracker — Visual Identity

PMFtracker helps founders turn a fuzzy question — *do people actually need this?* — into a number they can trust. The visual language has to earn that trust: it should feel **measured, modern, and quietly confident**, like a well-built analytics product, while staying warm and human enough for an early-stage founder. The system does this by living in two registers and switching between them with intent.

## Brand personality

- **Data-serious, not corporate.** Clean geometry, restraint, and one accent color. Nothing decorative for its own sake.
- **Optimistic and forward-leaning.** Indigo, soft gradients, and big celebratory numbers keep it from feeling clinical.
- **Editorial clarity.** Long-form content (guides, comparisons, benchmarks) reads like a good publication — generous measure, strong hierarchy, calm typography.
- **Moments of drama.** Where it matters — the hero, a primary CTA, the score result — the UI drops into deep indigo-black gradients that make those moments feel important.

## The two registers

**1. Light editorial surfaces (the default).**
Pure white and near-white (`background-soft`) canvases, slate ink (`ink` / `body` / `muted`), and hairline borders (`line`). Content sits in a comfortable reading measure (`content-max` ≈ 720px). Cards are white with a very soft, low-contrast shadow and a 1px border — they feel light, almost flat, lifting only slightly on hover. This is where 90% of the product lives.

**2. Dark gradient "moments" (the punctuation).**
Heroes, closing CTA panels, featured cards, and the score gauge use the `surface-night` gradient (slate-black → indigo) or the deeper near-black of the primary button. White text, generous padding, deep soft shadows. These bands break up the white and signal "this is the important part." Used sparingly — usually one per screen — they carry most of the brand's emotional weight.

## Color

Indigo is the entire identity. There is effectively **one accent** (`primary` `#4f46e5`, brightening to `#6366f1` for fills and gradients), and it does all the work: links, tags, focus rings, primary actions, the score bar's origin. Everything else is a neutral — white, the slate ink ramp, and the dark indigo-black surface family.

- **Tints over new hues.** When indigo needs to soften, it goes to `primary-soft` (`#eef2ff`) fills or `primary-border` (`#c7d2fe`) outlines — never a different color.
- **Status colors are reserved for verdicts.** Green (`success`) signals "good / above the 40% benchmark," amber (`warning`) signals "close," red (`danger`) signals "below." They appear almost exclusively in result/score contexts, not as general UI chrome.
- **The dark surfaces are a family, not one black.** `surface-dark` → `surface-dark-indigo` for panels, `surface-night`/`hero-night` for the near-black button base. The subtle differences keep the dark moments from feeling like flat black rectangles.

**Accent policy — one indigo.** The active accent is a single indigo: `primary #4f46e5`, brightening to `#6366f1`. Two near-duplicates are *legacy* and should converge on it — `#4d53c4` (the Webflow brand indigo and the in-product survey-widget default; visually all but identical — set the widget's default color to `#4f46e5` so in-product and marketing match), and the unused Webflow-default blue (`#2d62ff`) and pink (`#dd23bb`), which belong to no current system. Do not introduce them.

**The night ramp.** The dark surfaces are one family, not one black: `surface-dark #0f172a` → `surface-dark-indigo #312e81` for gradient panels and the gauge; `surface-night #0a0826` for the near-black pill button; `hero-night #080331` for the deepest band. Every dark surface maps to one of these four — never an ad-hoc black.

## Typography

**Manrope** is the voice — a modern geometric sans that reads as precise and trustworthy. It sets everything: display headlines, UI labels, and body. **Open Sauce Two** is a softer secondary used on a few labels/buttons to add warmth. Monospace appears only for code and formula snippets (e.g. the score formula).

- **Tight, confident headings.** Large sizes, negative letter-spacing, weight 600–800. Display headlines use fluid `clamp()` sizing and often a gradient-filled accent word.
- **Comfortable body.** ~1.12rem at 1.7 line-height for article body; never cramped.
- **Uppercase letterspaced eyebrows.** Small (`0.78rem`), bold, `0.08em` tracking — used as section kickers and pill tags. They organize the page without shouting.
- **Numbers are heroes.** Scores and benchmarks use the `metric` scale: huge (up to ~4.25rem), weight 800, tight tracking, often white-on-dark. A PMF score is the product's payoff, so it's typeset like one.

## Layout & spacing

Spacing follows a soft 4px-rooted rhythm expressed in rems, with deliberate breathing room. Sections stack with generous vertical padding (`section-padding-y` ≈ 5rem). Hero and CTA compositions are **center-aligned**; long-form content is left-aligned within the reading measure. The grid is calm and predictable — feature cards in 2- and 3-up grids, comparison tables full-width within `content-wide`. Whitespace is a feature, not an afterthought; the design trusts emptiness.

## Shape & radius

Rounded, but never bubbly. The signature shape is the **pill button** (`radii.pill`, ~100px) — a fully-rounded lozenge that reads as friendly and clickable. Cards and panels use medium radii (`lg`–`xl`, 16–18px). Small chips, inputs, and code blocks use 6–12px. Bars, avatars, and number badges go fully round (`full`). The radius language is consistent enough that everything feels part of one kit.

## Elevation & depth

Two distinct shadow vocabularies:

- **Light cards barely float.** A wide, very low-opacity shadow (`shadows.card`) plus a hairline border. On hover they lift gently (`card-hover`) with a quick 150ms transform. The effect is "paper on paper," not heavy material.
- **Overlays go deep.** Dropdowns, and especially modals, use large, soft, high-blur shadows (`dropdown`, `modal`) to sit convincingly above the page. Modal overlays use a translucent indigo-black scrim (`rgba(10,8,38,0.55)`) with a 4px backdrop blur, which ties the dimming back to the brand night palette.

Focus states are a 3px soft-indigo ring (`focus-ring`) plus a brighter border — visible, on-brand, never a default browser outline.

## Motion

Quick and quietly springy. Hovers and color/border changes resolve in **150ms**; modals and overlays enter in **~220ms** with a slight ease-out spring (`easing-standard`) and a small translate-and-fade pop. Slower **350ms** is reserved for satisfying state changes — the score bar filling, the primary button morphing on hover (which uses the more decisive `easing-brand`). A continuous marquee carries the social-proof logo strip. Motion is always in service of feedback or delight, never ambient animation for its own sake.

## Gradients & surfaces

Gradients are core, but disciplined:

- **The primary button is never a flat fill.** It's a near-black base with a soft radial top-glow, giving it a subtle dimensional sheen and a faintly nocturnal feel.
- **Dark panels run slate-black into indigo** (`surface-night`), used for heroes, closing CTAs, and the featured content card.
- **The accent gradient** (`#6366f1` → `#4f46e5`) fills small elements — icon badges, secondary buttons, number chips.
- **The score bar** travels from indigo into success-green, visually encoding "progress toward fit."
- **Gradient text** highlights a single word in hero headlines.

## Components

- **Buttons.** Primary = the dark gradient pill with white label and a light-grey arrow icon. Secondary = a quiet text link in muted purple-grey. Accent = the bright indigo-gradient pill for compact, in-content actions.
- **Tags / eyebrows.** Pill-shaped, soft-indigo fill, uppercase letterspaced indigo text. They label sections and card categories.
- **Cards.** Light by default (white, hairline border, soft shadow, hover lift). One "featured" card per surface flips to the dark gradient treatment to stand out.
- **Inputs.** White field, soft grey border, 10px radius, indigo focus border + soft focus ring. Calm and legible.
- **Modals.** Centered white card (~440px), 18px radius, deep soft shadow, indigo-black blurred scrim. Spring-in entrance. Used for lead capture and quick prompts.
- **The score gauge.** The product's signature component: a dark gradient panel housing a giant white percentage (the `metric` scale), a thin translucent track with the indigo→green fill, a 40% threshold marker, and a colored verdict line (green/amber/red). It is the visual climax of the entire system — everything else exists to lead the eye here.

## Imagery & iconography

Product imagery is clean dashboard UI shown in soft-cornered frames, often over the dark hero band so the white interface pops. Icons are simple, thin-stroke line glyphs (the arrow in the primary button, check marks in feature cards), never filled or skeuomorphic. The logo is a geometric three-block mark — structured, precise, on-brand with the "measurement" theme.

## In one line

**White, slate, and a single disciplined indigo — calm and editorial — broken by deep indigo-black gradient moments and big celebratory numbers that make measuring product-market fit feel both rigorous and exciting.**
