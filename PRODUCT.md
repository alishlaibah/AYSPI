# Product

<!-- impeccable:product-schema 1 -->

Source: written from the owner's brief of 2026-11-16 (the owner asked not to be interviewed). Facts below are the owner's own words or read directly from the code; anything inferred is marked *(inferred)*.

## Platform

web

## Users

Recruiters and engineers clicking in from LinkedIn or GitHub. They usually spend under a minute on the page. In that time they should try the live demo and understand the work behind it.

## Product Purpose

AYSPI is a browser-based ASL fingerspelling recognizer. It is a proof of concept and portfolio piece, not a product. Success means a visitor runs the demo (or understands why it is waiting) and leaves knowing how the pipeline works and that the author built it end to end.

## Positioning

The whole loop is the author's own work: a self-recorded, self-labeled dataset, a trained Conv1D + bidirectional GRU sequence classifier, and a deployed real-time inference path. No video leaves the browser; only landmark sequences are sent.

## Operating Context

- MediaPipe Hands extracts 21 hand landmarks per frame in the browser.
- A 30-frame window is sent to a FastAPI backend (`/predict`), which returns a letter (A–Z) and a confidence. Below 0.20 confidence the page shows "Unknown".
- The backend is on Render's free tier and cold-starts: the first prediction can take 60–120 seconds. Many visitors first see a waiting, no-hand, camera-unavailable, or backend-waking state.
- Frontend: React 19 + Vite, plain CSS with custom-property tokens, hosted on Cloudflare Pages.

## Capabilities and Constraints

- All copy is frozen word-for-word, including the headings, the pipeline steps, the build text, the stack names, the notes, the footer, the status and error messages, alt text, and aria-labels.
- The images, the links (GitHub, LinkedIn, and the stack documentation URLs), and the section order are frozen: header, demo + intro, How It Works, Building the System, Tech Stack, footer.
- Demo behavior is frozen: MediaPipe setup, sequence buffering, the fetches, the timing, and the Unknown threshold.
- No new dependencies. No CSS frameworks, component libraries, or animation libraries.

## Brand Commitments

- Name: AYSPI, shown as "ayspi.com" with the subtitle "ASL Letter Recognizer".
- Personality: precise, calm, technical, confident, like a well-made research lab project page or an instrument spec sheet. Not a SaaS landing page, not playful.

## Evidence on Hand

- Live demo (webcam + backend).
- `frontend/public/images/all_signs.jpg`: an ASL fingerspelling chart from A to Z.
- No metrics, accuracy figures, or testimonials are published on the page. Don't invent any.

## Product Principles

1. The demo is the proof. Everything else explains it.
2. Be honest about state. Waiting, cold-start, and failure states are first-class, because many visitors see them first.
3. Show the mechanism, not adjectives.
4. Respect a visitor's minute: the work should be legible at a glance and rewarding on a closer read.

## Accessibility & Inclusion

The subject is ASL. Keep the reference chart and the demo accessible: keyboard focus on every control, WCAG AA contrast, and reduced-motion support *(inferred standard)*.
