---
version: 1
slug: "frontend-src-app-jsx"
primary_target: "frontend/src/App.jsx"
related_targets: ["frontend/src/components/webcamfeed.jsx"]
---

# Surface: AYSPI project page (frontend/src/App.jsx)

Mode: Experience (portfolio piece; the demo leads). Audience: recruiters and engineers, under a minute. Task: try the demo, understand the pipeline. Constraints: copy, links, images, section order, and demo behavior are frozen (see PRODUCT.md).

## Direction contract

THESIS: The page is an instrument with its spec sheet. The live demo is a framed device with a readout, and everything else is set like a lab's technical note. It refuses the dark-SaaS template of gradient, glass, cards, pills, and staggered fades.

OWN-WORLD: A cool white ground, near-black ink, and 1px graphite rules on a 12-column grid. The only container is the camera, a near-black viewfinder with corner marks. One accent, emerald (oklch hue 155), is reserved for live signal only: the landmark overlay, the hand-detected dot, and the confidence bar. Type is Archivo for text and headings, with Martian Mono for data (the letter, confidence, model name, and step numbers).

STORY: Visitors see the instrument first and read its state (waiting, no hand, camera unavailable, backend waking), then the method as a directed pipeline, then the build notes, then the stack.

FIRST VIEWPORT: At 1440, the demo takes 7 of 12 columns: title row, 4:3 viewfinder, and a ruled readout below it (an 88px mono letter, the exact confidence, and a 2px ticked bar). The intro takes columns 8–12: a 44px h1, its paragraphs, and the reference chart. The status readout sits inside the viewfinder.

FORM: A pinned instrument and spec sheet. Signature interaction: the prediction letter updates with a 160ms settle while the bar glides. No entrance motion.

seed: none (pinned) — "Think of a well-made research lab project page or an instrument spec sheet." / "The demo is the hero and should feel like an instrument."

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
