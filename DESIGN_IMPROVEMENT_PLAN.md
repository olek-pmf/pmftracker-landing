# PMFtracker — Design Improvement Plan

A prioritized menu of design improvements for the marketing site. Each item is framed as a **decision** — issue, evidence, options, a recommendation, and effort/impact — so you can pick what to action rather than receive a fixed to-do list.

**Method:** holistic review of the rendered site against `DESIGN.md` (the documented intent) and `design-preview.html` (the drift detector), plus measured contrast, motion/accessibility, and color-coherence checks.

**Scoring:** Effort = **S** (≤ a couple hours) · **M** (≈ half-day) · **L** (multi-day). Impact = ★ (polish) → ★★★ (moves brand/conversion/accessibility meaningfully).

---

## What's already working (don't break these)

- **A coherent two-register system** — bright editorial light surfaces punctuated by deliberate deep-indigo "moments." It reads as intentional, not accidental.
- **Disciplined accent** — one indigo does almost all the work; status colors are reserved for verdicts. Restraint is a strength here.
- **Contrast baseline is healthy** — body 10.4:1, muted text passes AA on both white and the soft background, on-dark text passes comfortably. Most of the site is already accessible.
- **A genuine signature component** — the score gauge (big number, 40% threshold marker, indigo→green bar) is distinctive and ownable.
- **Design governance exists** — `DESIGN.md` + the drift detector are ahead of most startups. Improvements should flow back into both.

---

## Priority summary

| # | Improvement | Theme | Effort | Impact | Quick win? |
|---|---|---|---|---|---|
| B1 | `prefers-reduced-motion` support | Accessibility | S | ★★ | ✅ |
| B2 | `:focus-visible` rings on all interactive elements | Accessibility | S–M | ★★ | ✅ |
| B3 | Fix low-contrast micro-copy (2.56:1) | Accessibility | S | ★ | ✅ |
| A1 | Unify the indigo accent (retire the near-duplicate) | Brand coherence | M | ★★ | |
| A2 | Consolidate the dark-surface "night" ramp | Brand coherence | S–M | ★ | |
| D1 | Lean into the measurement/data motif | Distinctiveness | M–L | ★★★ | |
| D2 | Per-post share (OG) images | Distinctiveness | M | ★★ | |
| C2 | "Numbers as heroes," applied consistently | Hierarchy | M | ★★ | |
| E1 | CTA density & hierarchy sweep | Components | M | ★★ | |
| H1 | Mobile pass on signature surfaces | Responsive | M | ★★ | |
| C1 | Stronger display-headline weight | Typography | S | ★ | ✅ |
| C3 | Light/dark section rhythm rule | Layout | S–M | ★ | |
| E2 | Reconcile the card system + update tokens | Components | M | ★ | |
| E3 | Empty / error / loading states audit | Components | S–M | ★ | |
| F1 | Tasteful scroll-in reveals | Motion | M | ★ | |
| G1 | Externalize the 108 KB inline logo banner | Perf-as-design | S–M | ★ | ✅ |
| G2 | Add image dimensions (kill CLS) | Perf-as-design | M | ★ | |
| D3 | Custom feature iconography | Distinctiveness | M | ★ | |

---

## A. Brand & accent coherence

### A1 — Unify the indigo accent
**Issue.** Two visually near-identical indigos coexist: `#4f46e5` (the content/UI accent, ~21 uses) and `#4d53c4` (the Webflow brand indigo + the in-product embed-widget default, ~9 uses), alongside the brighter `#6366f1` (~17). Vestigial Webflow brand **blue `#2d62ff`** and **pink `#dd23bb`** also linger (1–2 uses each) and belong to no current system.
**Evidence.** Drift detector already tracks both indigos separately; `DESIGN.md` documents the duality rather than resolving it.
**Options.**
- **(A)** Standardize on `#4f46e5` (primary) + `#6366f1` (bright) everywhere; map `#4d53c4` → `#4f46e5`; delete blue/pink. *(Recommended.)*
- **(B)** Keep `#4d53c4` as the "brand" indigo and align the content system to it instead.
**Recommendation.** Option A — `#4f46e5`/`#6366f1` is already dominant and is what the dark panels and gauge are tuned to. Also nudge the **app's embed-widget default color** to match, so the survey users see in-product is the same indigo as the marketing site. **Effort M · Impact ★★.**

### A2 — Consolidate the dark "night" ramp
**Issue.** Several near-blacks do similar jobs: `#0a0826` (button base), `#0f172a`→`#312e81` (panels/gauge), `#080331` (deepest hero). Subtle variety is fine, but it's currently incidental, not a defined ramp.
**Recommendation.** Define a 3-stop night ramp in `DESIGN.md` (e.g. `night-900 / night-700 / night-indigo`) and map each surface to one. Mostly a documentation + light cleanup task. **Effort S–M · Impact ★.**

---

## B. Accessibility (highest ROI — do these first)

### B1 — Respect `prefers-reduced-motion`
**Issue.** Zero reduced-motion rules. The logo marquee, modal pop, hover lifts, and bar fills all animate regardless of the user's OS setting.
**Recommendation.** Add one media block that pauses the marquee and reduces transitions/animations to near-instant. Standard, low-risk, and the right thing to do. **Effort S · Impact ★★.**

### B2 — Visible keyboard focus everywhere
**Issue.** No `:focus-visible` anywhere; styling relies on `:focus`. Webflow nav links, card-as-link blocks, and the gradient buttons likely have no clear keyboard focus ring.
**Recommendation.** Add a consistent `:focus-visible` ring (reuse the existing 3px soft-indigo `focus-ring` token) to links, buttons, cards-as-links, dropdown items, and form fields. Keyboard and screen-reader users currently can't reliably see where they are. **Effort S–M · Impact ★★.**

### B3 — Fix failing micro-copy contrast
**Issue.** Light-grey fine print (`#94a3b8` / `#8b8497`) on white measures **2.56:1** — below the 4.5:1 minimum. Affects modal "no spam" lines, some captions, and footer-adjacent small text.
**Recommendation.** Darken small/secondary text to ~`#64748b` (already AA on white at 4.76:1). Keep the lighter grey only for non-essential decoration. **Effort S · Impact ★.**

---

## C. Visual hierarchy & typography

### C1 — Give display headlines more punch
**Issue.** Hero/H1 display type renders at weight **600**. At very large sizes Manrope 600 can feel a touch soft for a "data-serious" product.
**Options.** Bump display to **700–800** with slightly tighter tracking *(recommended for impact)*, **or** keep 600 if you prefer the current elegant/understated tone. **Effort S · Impact ★.**

### C2 — "Numbers as heroes," applied consistently
**Issue.** `DESIGN.md` calls numbers the payoff, and the gauge nails it — but long-form pages rarely use big-stat callouts. The 42% / 40% / 51% / 22%→58% figures are buried in prose.
**Recommendation.** Introduce a reusable **stat block** (huge gradient number + caption) and seed it into articles, the homepage, and comparison/benchmark pages. Reinforces the brand's core idea on every page. **Effort M · Impact ★★.**

### C3 — A light/dark section-rhythm rule
**Issue.** The two-register system has no spacing/cadence rule, which is how the earlier "two stacked dark CTA panels" slipped through.
**Recommendation.** Codify in `DESIGN.md`: *max one dark "moment" per scroll region; never two dark panels adjacent.* Then a quick audit. **Effort S–M · Impact ★.**

---

## D. Distinctiveness (reduce the "polished Webflow template" feel)

### D1 — Lean into the measurement / data motif *(the big strategic lever)*
**Issue.** The site is well-executed but visually reads like a high-quality generic SaaS template. Its single most ownable asset — *measuring a score against a 40% line* — is only expressed in one component.
**Recommendation.** Make the score/threshold a recurring **brand device**: the 40% marker as a motif, gauge-style progress bars in feature sections, subtle gridline/plot textures on dark panels, "score card" stat blocks, a benchmark dial. This is what would make PMFtracker look unmistakably like *itself*. **Effort M–L · Impact ★★★.**

### D2 — Per-post share images
**Issue.** All 17 blog posts + pages share one generic `og-image`. Social/search thumbnails are identical and unbranded-per-topic.
**Recommendation.** Design one branded OG **template** (logo + title + category, on the night gradient) and generate one per post — ideally script-driven like the benchmark generator. Lifts social CTR and brand recall. **Effort M (template) + S/post · Impact ★★.**

### D3 — Custom feature iconography
**Issue.** Feature icons are minimal generic line glyphs.
**Recommendation.** A small bespoke icon set (collect, score, track, ICP, report) in the brand's thin-stroke style. Nice-to-have. **Effort M · Impact ★.**

---

## E. Component consistency & polish

### E1 — CTA density & hierarchy sweep
**Issue.** We already fixed the tool pages' competing dual CTAs, but the pattern of "two strong CTAs near each other" likely recurs (e.g. benchmark pages have mid + end CTAs plus the lead magnet).
**Recommendation.** One unambiguous primary action per section; demote the rest to text links or quieter styles. Audit every template. **Effort M · Impact ★★.**

### E2 — Reconcile the card system
**Issue.** `blog-card`, `mkt-card`, `cta-box`, and `lead-request-card` are separate treatments; the drift detector revealed `blog-card` actually uses the *heavier* `card-hover` shadow at rest (not the documented soft `card`).
**Recommendation.** Define one card scale (resting/hover/featured/dark) and update the `DESIGN.md` card token to match reality. **Effort M · Impact ★.**

### E3 — Empty / error / loading states
**Issue.** Unreviewed: the calculator at 0 responses, invalid/again-empty input, and the lead modal's error/success states.
**Recommendation.** Quick audit + tidy each state (helpful zero-state copy, clear inline errors). **Effort S–M · Impact ★.**

---

## F. Motion & micro-interaction

### F1 — Tasteful scroll-in reveals
Subtle fade/translate-up as sections and card grids enter the viewport (staggered), **guarded by `prefers-reduced-motion`** (depends on B1). Adds life without gimmickry. **Effort M · Impact ★.**

### F2 — Consistent hover/active states
Ensure every interactive surface has a deliberate hover (cards lift, buttons shift, links underline) and a pressed/active state. **Effort S · Impact ★.**

---

## G. Performance as design

### G1 — Externalize the inline logo banner
The audience pages embed ~108 KB of inline SVG for the social-proof marquee, bloating the HTML.
**Recommendation.** Move to a shared, lazy-loaded asset. Faster first paint + easier maintenance. **Effort S–M · Impact ★.**

### G2 — Add image dimensions (kill CLS)
~100 images lack explicit `width`/`height`, risking layout shift (a Core Web Vital and a *perceived-stability* design issue).
**Recommendation.** Add intrinsic dimensions to content/hero images. **Effort M · Impact ★.**

---

## H. Mobile

### H1 — Mobile pass on the signature surfaces
**Issue.** The score gauge, calculator inputs, dark CTA panels, comparison tables, and the nav dropdown haven't been deliberately reviewed at ≤390 px.
**Recommendation.** A focused mobile sweep of those specific surfaces (the gauge and tables are the riskiest). **Effort M · Impact ★★.**

---

## Recommended sequencing

**Wave 1 — Quick wins (a day or less, mostly accessibility).**
`B1` reduced-motion · `B2` focus-visible · `B3` contrast fix · `C1` headline weight · `G1` externalize banner. *High value, low risk, ship together.*

**Wave 2 — Coherence & conversion.**
`A1` unify indigo (+ align the app widget color) · `A2` night ramp · `E1` CTA sweep · `C2` stat blocks · `H1` mobile pass.

**Wave 3 — The strategic bet.**
`D1` measurement motif · `D2` per-post OG images. *This is where PMFtracker stops looking like a template and starts looking like itself.*

**Ongoing.** Every change above should be reflected back into `DESIGN.md` and verified green in the drift detector — that's the governance loop that keeps the system from fragmenting again.

---

### How to use this doc
Tell me which items (by number) you want to action and I'll implement them, updating `DESIGN.md` and the drift detector in lockstep. If you want a single recommendation: **do Wave 1 now** (it's almost all accessibility and ships in an afternoon), then commit to **D1** as the one bet that changes how the brand *feels*.
