# Portfolio design and implementation

Audience: internship recruiters and engineering collaborators. First tasks: understand Ritam's work, inspect a project, open the resume, get in touch.

## Direction

Preserve the scaffold's warm paper, ink, and cobalt identity. Use a quiet editorial layout, oversized but responsive headings, small monospace section labels, generous spacing, and the approved portrait as the only personal photograph. Project artwork is illustrative and labeled; do not fabricate screenshots or a new personal project.

Design references are the existing scaffold (color and typography hierarchy), the supplied professional portrait (human focal point), and the project READMEs (technical storytelling). This is a deliberate evolution of the existing identity, not an imitation of a different portfolio.

Desktop sketch: restrained navigation → two-column introduction/portrait → wide swipeable project cards → paired biography/experience → achievement grid → dark contact panel. Mobile sketch: compact wrapping navigation → introduction → portrait → single-card project viewport with controls → stacked biography → two-column stats → contact. Case studies use a readable single-column story with a wrapping flow diagram.

## Tokens

All colors, spacing, radii, typography, and motion durations live in `docs/style.css`. The default is warm light; dark mode remaps surface, ink, line, and accent tokens. Artwork has its own readable palette in both themes. System fonts avoid a font-service dependency. Content max width is 1180px; text width is capped independently.

## Motion and navigation

CSS transitions handle feedback. Native Web Animations run brief hero and section entrances only after initialization. IntersectionObserver reveals once; content is visible without JavaScript. Reduced-motion changes cancel current animations, reveal all content, and make programmatic scrolling instant. There are no continuous loops, cursor effects, or scroll hijacking.

The project rail uses native horizontal scrolling with CSS scroll snap, arrows, keyboard navigation, and current-position feedback. It has finite boundaries and no autoplay. Filtering removes nonmatching projects and resets position. The no-JavaScript fallback is a vertical list, including every case-study link. No gesture library is needed.

## Maintenance

Edit `content/projects.json` and run `python3 scripts/build_site.py` to regenerate the index and case studies. Static HTML is committed for build-free hosting. CSS and JavaScript are hand-authored. `scripts/check_site.py` validates all generated pages and local links. Product behavior tests run with `npm test`; development dependencies never ship in `docs/`.

New content must preserve the explicit exclusion of Sentiment Streamer and the deferred Playground replacement. No analytics, form service, blog placeholder, stock personal photos, or invented performance claims are included. Contact uses working email and copy-email actions. Public ratings remain attributed to the supplied resume.
