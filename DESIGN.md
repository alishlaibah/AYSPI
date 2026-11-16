# AYSPI Design System

An instrument and its spec sheet. The live demo is the one framed object on the page, and everything else is set like a lab's technical note: a strict grid, typographic hierarchy, whitespace, and thin rules. Tokens live in `frontend/src/styles/tokens.css`.

## Principles

1. **One container.** Only the camera is boxed, because it really is a device. Structure everywhere else comes from the grid, rules, and type.
2. **The accent is signal.** Emerald appears only where the system is live: the landmark overlay, the hand-detected dot, and the confidence bar. Never on links, buttons, headings, hover states, or focus rings.
3. **Mono is for data.** Martian Mono sets the prediction letter, the confidence, the model name, the status readout, and the pipeline step numbers. Prose and headings are Archivo.
4. **States are first-class.** Waiting, no hand, camera unavailable, and backend waking each read clearly in the viewfinder and the readout.
5. **Motion confirms change.** Only hover and focus feedback, the letter settling when it updates, and the confidence bar gliding. No entrance or scroll motion.

## Color (OKLCH, light only)

| Token | Value | Hex ≈ | Use | Contrast vs `--bg` |
|---|---|---|---|---|
| `--bg` | `oklch(0.985 0.002 250)` | #f9fafb | Page ground (cool white) | — |
| `--ink` | `oklch(0.20 0.010 255)` | #13161b | Headings, body, links, strong rules | 17.3:1 |
| `--ink-2` | `oklch(0.43 0.012 255)` | #4b5056 | Secondary prose, labels | 7.8:1 |
| `--ink-3` | `oklch(0.52 0.012 255)` | #646970 | Meta (footer date, model key) | 5.3:1 |
| `--rule` | `oklch(0.89 0.004 255)` | #d9dbdd | Hairline dividers, bar track | — |
| `--rule-strong` | `oklch(0.76 0.006 255)` | #aeb1b5 | Control borders, ticks | 2.1:1 |
| `--stage` | `oklch(0.19 0.008 255)` | #111417 | Viewfinder ground | — |
| `--on-stage` | `oklch(0.93 0.004 255)` | #e6e8ea | Text on the viewfinder | 15.0:1 on stage |
| `--on-stage-2` | `oklch(0.72 0.006 255)` | #a2a5a8 | Secondary text and marks on the viewfinder | 7.5:1 on stage |
| `--signal` | `oklch(0.56 0.15 155)` | #008d4b | Confidence bar fill | 4.1:1 |
| `--signal-bright` | `oklch(0.80 0.19 152)` | #3ddf7d | Landmark overlay and status dot on the viewfinder | 10.6:1 on stage |
| `--error` | `oklch(0.72 0.16 25)` | #f97770 | Error marker on the viewfinder only | 6.9:1 on stage |

The canvas overlay uses the hex equivalents: bones `#3ddf7d` at 2px, and joints filled `#3ddf7d` (r = 3.5) with a 1.5px `#111417` ring.

## Typography

- **Sans:** Archivo (Google Fonts, 400/500/600), used for all prose and headings.
- **Mono:** Martian Mono (Google Fonts, 400/500), used for data only. Numerals are tabular.

| Token | Size | Line height | Use |
|---|---|---|---|
| `--text-sm` | 0.875rem / 14px | 1.5 | Labels, notes, footer, stack links |
| `--text-base` | 1rem / 16px | 1.6 | Body, pipeline descriptions |
| `--text-md` | 1.0625rem / 17px | 1.6 | Lead paragraphs, build prose |
| `--text-lg` | 1.25rem / 20px | 1.3 | h3, demo title |
| `--text-xl` | clamp(1.5rem, 1.2rem + 1vw, 2rem) | 1.15 | Section h2 |
| `--text-2xl` | clamp(2rem, 1.4rem + 2vw, 2.75rem) | 1.05 | h1 |
| `--text-readout` | clamp(3rem, 2.25rem + 2.25vw, 4.5rem) | 1 | Prediction letter (the row height is reserved so it never jumps) |
| `--text-mono-sm` | 0.8125rem / 13px | 1.4 | Mono readouts: status, model ID, step numbers (Martian Mono runs wide; 13px mono optically matches 14px Archivo) |

The floor is 14px for sans and 13px for mono. Labels are sentence case, not tracked uppercase. Headings use -0.02em tracking, h1 -0.025em. Body measure is at most 68ch.

## Spacing

The base unit is 4px. Tokens: `--sp-1` 4, `--sp-2` 8, `--sp-3` 12, `--sp-4` 16, `--sp-5` 24, `--sp-6` 32, `--sp-7` 48, `--sp-8` 64, `--sp-9` 96. Sections get `--sp-9` of block padding on desktop and `--sp-8` at 768px and below. There is always more space above a heading than below it.

## Grid

- The container is 1280px max, with 32px inline padding (20px at 390px).
- 12 columns with a 32px gap (24px at 1024px and below).
- **Hero:** demo in columns 1–7, intro in columns 8–12. At 900px and below it becomes a single column with the demo first.
- **Sections:** a 1px `--ink` rule on top, drawn as a `::before` across the content width only (not the gutters). The heading block takes columns 1–4 and the content columns 5–12. How It Works runs its pipeline across all 12 columns. At 900px and below the heading stacks above the content.

## Components

- **Viewfinder** (`.webcam-stage`): `--stage` ground, 2px radius, and four corner marks and a centre crosshair in `--on-stage-2`. Inside it are the status readout (top-left, mono, solid stage-colored plate; hollow dot when idle, filled `--signal-bright` when a hand is detected) and the error strip (bottom edge, with a square `--error` marker). The video covers the marks when live. The video and landmark canvas are mirrored together (`scaleX(-1)`, selfie view); the landmark data sent to the backend is not.
- **Readout:** a ruled row under the viewfinder. The prediction letter is in mono at `--text-readout`; "Unknown" steps down to `--text-lg` in `--ink-2`. Confidence shows an exact mono percentage over a 2px bar, with quarter ticks and a `--signal` fill. The backend-waking message sits on its own ruled line under the readout, marked with a hollow neutral dot.
- **Toggle:** a 32×18 switch. Off is a `--rule-strong` outline; on is filled `--ink`. Neutral, never accent.
- **Pipeline:** an ordered list. Each step has a mono number on a rule that ends in an arrowhead pointing to the next step. It runs horizontal on desktop and vertical (rule down the left) at 900px and below.
- **Build notes:** three ruled rows with the h3 in a narrow left column and the prose on the right.
- **Stack:** three columns of plain links, underlined with a 0.18em offset. On hover the underline thickens to 2px.
- **Links and buttons:** ink text. Focus is a 2px `--ink` outline with a 3px offset.

## Motion

- `--ease-out: cubic-bezier(0.16, 1, 0.3, 1)`, durations 120ms (hover) and 200ms (bar).
- The prediction letter settles from 0.4 opacity and a 3px offset over 160ms when it changes.
- `prefers-reduced-motion: reduce` turns off the letter settle and the bar transition.
