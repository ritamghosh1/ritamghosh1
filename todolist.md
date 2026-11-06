# Portfolio completion roadmap

Turn the scaffold into a personal portfolio that makes it easy to understand Ritam’s work, explore real projects, view a resume, and get in touch. Give it a distinct visual identity, real photography, and polished swipe and scroll interactions.

Updated: November 7, 2026.

## Release status

Implemented: responsive editorial layout, native swipe/keyboard project rail, filters and empty state, three direct-link case studies, architecture flows, portrait and resume, light/dark/system theme, one-time entrances, reduced-motion changes, copy-email fallback, social card, favicon/touch icon, sitemap, content generator, static/HTTP checks, behavior tests, and CI.

Publication: after the initial private-repository plan rejection, Ritam explicitly authorized making the repository public and publishing with GitHub Pages. The repository is public and GitHub Pages has deployed `main` / `/docs` successfully with HTTPS enforced. All 16 checked public paths matched the release bytes, including case studies, share images, scripts/styles, and resume. Live URL: https://ritamghosh1.github.io/ritamghosh1/. Browser host and native capture failed, so real-browser, device, screen-reader, and Lighthouse checks are not represented as passed. Real project screenshots, additional photos, the new project, and the Playground replacement await assets or a brief.

Optional choices closed for this release: no inline PDF preview, autoplay, analytics, contact-form service, empty writing section, photo lightbox, custom domain, or framework migration. Their prerequisites or a concrete need are absent. These are deliberate scope decisions, not implemented features.

## Status and scope

- [x] Inspect the existing static site in `docs/`.
- [x] Remove the Playground section, maze controls, maze JavaScript, and unused styles.
- [x] Remove Playground navigation and its hero link; the supplied portrait now replaces the artwork.
- [x] Keep competitive-programming profile links in About.
- [x] Replace `PORTFOLIO.md` with this roadmap.
- [x] Complete the available design and implementation work below.
- [ ] Finish the explicitly listed browser/content/hosting gates before claiming a verified public launch.

The supplied portrait, resume links, education, internship, skills, and selected achievements are now integrated. The website resume is a reformatted one-page copy with Sentiment Streamer removed; the source PDF is unchanged. The redesign, swipeable project rail, case studies, persistent light/dark/system theme, and reduced-motion-aware entrances are implemented. Automated checks pass; real-browser layout, performance, and assistive-technology verification remain open because browser access failed. The replacement for Playground is deliberately undecided: do not invent a section or publish a “coming soon” placeholder. Additional galleries and project screenshots still need source assets from Ritam.

Priority: **P0** = necessary inputs and decisions; **P1** = launch essentials; **P2** = polish after essentials; **P3** = optional future work. Complete P0, then P1, then P2. Choose P3 work only when it improves the actual portfolio.

## 1. Content and asset preparation — P0

- [x] Receive the resume and permission to create a website copy excluding Sentiment Streamer. Use the supplied email and professional details; retain contact details in the downloadable resume.
- [x] Receive `Profpic.png` and export optimized portrait assets for the website.
- Deferred — needs Ritam’s assets: choose 3–6 additional photos if a gallery is wanted: project building, campus, events, or personal interests. Confirm permission to publish photos containing other people.
- [ ] Collect real screenshots for Ask the Book, AlgoCoach, and Arrakis. Remove private data, credentials, and irrelevant browser chrome.
- [x] Match project names, stacks, roles, links, and status to the supplied resume and project READMEs. Omit unsupplied project dates; label Arrakis as a team concept.
- [ ] Recheck full demo behavior in a working browser; hosted APIs may sleep or require sign-in.
- [x] Write a short account of each project: problem, approach, difficult decision, result, and next improvement. Include numerical claims only when evidence exists.
- [x] Extract degree wording, 2024–2028 education dates, CGPA, Kolkata internship, and selected achievements from the supplied resume. Treat ratings as resume-reported figures, not live data.
- [x] Decide the primary audience: internship recruiters, collaborators, or both. Choose the main call to action accordingly.
- [x] Match contact/profile handles to the supplied resume and existing profile README. Live coding ratings are deliberately not fetched.
- [x] Choose 2–3 visual references and identify specific qualities to borrow: typography, density, photography, color, or motion.

**Done when:** approved copy and source assets are available; missing details are explicitly tracked, with no invented achievements, photos, or resume content.

## 2. Information architecture and design direction — P0 → P1

- [x] Set the launch section order: Hero → Selected work → About / skills / education → Contact. Integrate the resume entry points throughout this flow.
- [x] Replace the hero’s illustrated grid with the supplied portrait.
- [x] Develop one coherent direction around the personal content: expressive typography, a clear accent color, generous spacing, and strong project imagery.
- [x] Define reusable tokens for backgrounds, text, accent, borders, spacing, typography, radii, shadows, and motion.
- [x] Sketch mobile and desktop layouts before implementing the redesign.
- [x] Define reusable button, project card, tag, section heading, photo, and link treatments, including focus, hover, pressed, and disabled states where relevant.
- [x] Keep the GitHub profile `README.md` and its existing workflows independent from website changes.
- [x] Keep repository-relative asset paths so deployment under `/ritamghosh1/` works.

**Done when:** one visual direction and responsive layout are agreed, with a clear content hierarchy and consistent component styles.

## 3. Resume integration — P1

- [x] Store the approved PDF at a stable path such as `docs/assets/resume/ritam-ghosh-resume.pdf`.
- [x] Add clearly labeled “View resume” and “Download resume” links. Place a prominent entry in the hero or navigation and a secondary entry near About or Contact.
- [x] Open the view link as a normal PDF URL. If opening a new tab, indicate it accessibly and use appropriate link attributes.
- [x] Add the `Ritam_Ghosh_Resume.pdf` download filename and verify the live PDF URL returns the exact approved bytes with `application/pdf`. Browser-specific download behavior remains below.
- [x] Include a short HTML summary of education and relevant skills so key information is available without opening a PDF.
- [x] Omit a resume update-date claim because the original issue date was not supplied.
- [x] Verify the website PDF has selectable text, working embedded link targets, one page, and no excluded project text or links; visually inspect its rendered page.
- [ ] Verify PDF viewing and download behavior in desktop and mobile browsers.
- Deferred: inline PDF preview is not needed for this release; direct viewing/download links are implemented.

**Done when:** both resume actions work on desktop and mobile, the published PDF is current, and no resume link points to a placeholder.

## 4. Personal photos and project media — P1

- [x] Serve 480px/960px portrait sizes with responsive aspect ratios and tuned `object-position` for narrow/wide crops. Real-device visual confirmation remains in the browser gate.
- [x] Use optimized image formats with compatible fallbacks where needed; supply responsive `srcset` / `sizes`.
- [x] Set image dimensions or aspect ratios to reserve space and prevent layout shifts.
- [x] Load the primary visible portrait promptly; lazy-load images below the fold.
- [x] Write useful alt text for meaningful photos and screenshots; use empty alt text for purely decorative images.
- [ ] Replace illustrative project previews with real screenshots where available. Keep any remaining illustration clearly identified as an illustration.
- [ ] Use consistent screenshot framing without cropping out information needed to understand the project.
- [x] Remove unnecessary location metadata from public photo exports and keep original large files out of the shipped site.
- [x] Verify every published image path on GitHub Pages and compare its bytes to the release.

**Done when:** images look sharp at their intended display sizes, crops work across breakpoints, and loading media does not shift the layout.

## 5. Core portfolio UI — P1

- [x] Refine the hero around a concise introduction, portrait, primary project action, and visible resume action.
- [x] Implement wrapping native navigation and a labeled theme selector; no menu/dialog is needed. Real small-screen layout review remains in the browser gate.
- [x] Give each project a clear title, short problem statement, contribution, technology context, and source/demo actions.
- [x] Preserve and polish project filtering. Keep selected state visible, announce the result count, and provide a useful empty state if future categories can be empty.
- [x] Turn About into a personal narrative with concise education and grouped skills. Avoid oversized lists of technology badges.
- [x] Preserve all four coding-profile links and label figures as recorded in the supplied resume, not live data. Case-study provenance is dated November 7, 2026.
- [x] Improve contact layout, email-copy feedback, social labels, and footer spacing.
- [ ] Confirm hero actions, long email addresses, tags, and navigation fit at narrow widths without page-wide horizontal scrolling.
- [ ] Check light backgrounds, darker contact surfaces, readable body copy, line lengths, and consistent vertical rhythm.

**Done when:** a visitor can identify who Ritam is, understand the strongest work, reach the resume, and contact him without searching through decorative content.

## 6. Swipe and motion system — P2

### Motion foundations

- [x] Define a small shared set of durations, easing curves, offsets, and stagger values. Starting ranges: 120–200 ms feedback, 180–300 ms state transitions, 400–700 ms section reveals; tune after previewing.
- [x] Plan one distinctive hero entrance and quieter supporting motion so the resume and main actions remain immediately usable.
- [x] Add short, one-time section reveals with small translate and opacity changes. Avoid repeatedly replaying motion while scrolling back and forth.
- [x] Keep content visible by default; enable reveal states only after JavaScript initializes successfully.
- [x] Add restrained button/card-action feedback and visible keyboard focus; large artwork stays still.
- [x] Animate transforms and opacity where possible; avoid animating layout dimensions or large blur effects.
- [x] Keep normal document scrolling. Do not intercept the mouse wheel or force full-screen section snapping.

### Swipe experience

- [x] Use the selected-project cards as the swipe surface. Screenshot and personal-photo galleries remain deferred until real assets exist.
- [x] Prototype a horizontal track with native scrolling and CSS scroll snap before adding custom gesture code.
- [x] Implement native touch/trackpad scrolling, previous/next controls, and Arrow/Home/End navigation; test finite boundaries and links reachable without dragging.
- [ ] Verify actual touch/trackpad gesture behavior on real devices.
- [x] Define boundary behavior at the first and last item; avoid an infinite loop unless it has a clear benefit.
- [x] Show the current position or slide count and disable unavailable navigation actions.
- [x] Preserve native gesture handling and vertical document scrolling; do not intercept wheel or pointer gestures.
- [ ] Confirm mostly vertical swipes and accidental-link prevention on an actual touch device.
- [x] Implement and test horizontal focus navigation so focusing a project link selects its card without programmatic vertical scrolling.
- [ ] Verify rendered focus visibility and browser scrolling by keyboard on devices.
- [x] Avoid autoplay. If later introduced for a specific reason, provide pause controls and stop it on interaction.

### Accessibility and performance

- [x] Honor `prefers-reduced-motion`: show content immediately, remove decorative movement, and use instant transitions or minimal fades.
- [x] Handle preference changes without requiring a reload if animation behavior is controlled in JavaScript.
- [x] Disconnect completed/reduced-motion reveal observers and cancel active animations on pagehide. Views are static documents, so there is no dynamic view-removal lifecycle.
- [ ] Profile on a representative phone and desktop; remove effects that cause stutter or delay input.
- [x] Evaluate any animation dependency against the actual interaction needs before adding it; record why it is necessary.

**Done when:** swipes feel predictable, controls work with keyboard and touch, page scrolling remains natural, reduced-motion mode is complete, and there is no hidden content when scripts fail.

## 7. Richer project storytelling — P2

- [x] Give each featured project a case-study section or detail page once there is enough approved content.
- [x] Give each case study an overview, role, key decision, architecture/product flow, source/demo actions, result, lesson, and proposed improvement. Use labeled illustrations while screenshots are unavailable.
- [x] Distinguish implemented work from planned features and personal contributions from team contributions.
- [x] Add readable architecture diagrams only where they explain a meaningful design decision.
- [x] Show real outcomes, limitations, and tradeoffs; avoid unsupported performance figures.
- [x] Add documented source/demo URLs and label Streamlit sign-in/wake-up, AlgoCoach cold starts, and Arrakis concept status. Full external-app behavior remains a manual check.
- [x] If detail pages are added, support direct links, browser back, consistent navigation, and unique page metadata.

**Done when:** the strongest projects explain engineering judgment as well as technologies used.

## 8. Playground replacement — deferred, awaiting Ritam’s idea

- [ ] Capture the new section concept when Ritam is ready.
- [ ] Define its visitor benefit, content requirements, interaction, and placement.
- [ ] Sketch it in context with the rest of the portfolio.
- [ ] Define accessibility, mobile, and performance requirements before implementation.
- [ ] Implement and verify it as a separate milestone.

**Constraint:** leave the removed section absent until the replacement is defined. This does not block the initial portfolio launch.

## 9. Accessibility and resilience — P1, repeated after P2

- [x] Keep semantic landmarks, one primary heading, logical heading order, and the working skip link.
- [ ] Test all links, filters, galleries, menus, and dialogs with keyboard only; keep focus visible and predictable.
- [x] Check nine primary light/dark text/accent contrast pairs against 4.5:1.
- [ ] Complete rendered contrast, focus-state, and image-overlay verification in real browsers.
- [x] Give controls accessible names; keep decorative icons out of the accessibility tree.
- [ ] Make touch targets comfortably usable and verify the layout at 200% zoom and narrow reflow widths.
- [ ] Test with a screen reader: navigation, project filtering announcements, gallery position, resume links, and copy-email status.
- [x] Confirm core content, contact links, and resume access work with JavaScript disabled.
- [ ] Verify blocked fonts and unavailable images still leave a usable layout.
- [x] Preserve the email fallback when clipboard permission is denied or unavailable.

**Done when:** core tasks remain possible by keyboard, screen reader, touch, reduced-motion settings, and without JavaScript.

## 10. Metadata, sharing, and performance — P1

- [x] Generate unique titles, descriptions, matching canonical/OG URLs, image alt text, and Twitter cards for the intended GitHub Pages URL.
- [x] Fetch the absolute Open Graph/social image URL over HTTPS and match it to the release. Actual social-network card rendering remains a manual check.
- [x] Create a branded social preview image using approved assets, and add absolute Open Graph / social image URLs with descriptive alt text.
- [x] Add SVG favicon/touch icon and update browser theme-color with the selected theme.
- [ ] Visually verify icon and browser chrome rendering on devices.
- [x] Add structured person/profile data only if its fields accurately match public content.
- [x] Review font loading, weights, fallbacks, and caching; avoid shipping unused font variants.
- [x] Set practical image budgets: aim for a portrait around 250 KB or less and optimized screenshot derivatives, while preserving quality.
- [ ] Measure the finished page with Lighthouse and browser performance tools on mobile settings; investigate slow rendering, layout shifts, and delayed input.
- [x] Use Core Web Vitals targets as a quality goal: LCP ≤ 2.5 s, CLS ≤ 0.1, INP ≤ 200 ms. Distinguish lab checks from real visitor measurements.
- [x] Keep analytics optional. Add a service only after deciding what question the data should answer and documenting its privacy implications.

**Done when:** the deployed URL shares correctly, loads quickly on mobile, and contains no broken local assets or misleading metadata.

## 11. Verification and launch — P1

- [x] Serve the static site locally and verify successful HTTP responses.
- [ ] Complete visual browser preview; browser host/native capture errors prevented it in this session.
- [x] Check JavaScript syntax, HTML structure, duplicate IDs, missing local assets, and broken section anchors.
- [x] Test filtering, copy success/failure, no-JavaScript links, and carousel keyboard/focus flows; validate local navigation anchors and published resume responses.
- [ ] Finish interactive browser checks for navigation, PDF viewing, and downloads.
- [ ] Test phone, tablet, and desktop layouts, including 320 px width, landscape, zoom, and long text.
- [ ] Test current Chrome, Firefox, Safari, and at least one actual touch device when available.
- [x] Test empty filters, reduced-motion initialization/live changes, no-JavaScript content, repeated navigation/filtering, storage denial, and clipboard denial.
- [ ] Check slow/unavailable media loading in rendered browsers.
- [ ] Inspect browser console and network requests for runtime errors and 404s.
- [x] Document the `main` + `/docs` setup, initial plan rejection, explicit public-visibility authorization, and successful public publication in `DEPLOYMENT.md`.
- [x] Receive explicit authorization, make the repository public, and select GitHub Pages from `main` / `/docs`.
- [x] Confirm GitHub accepts and deploys `main` / `/docs`: Pages build/deploy succeeded; site status is `built`; HTTPS is enforced.
- [x] Verify 13 local HTTP paths under `/ritamghosh1/`, including nested case studies, assets, and exact resume bytes/PDF content type.
- [x] Verify 16 published HTTPS paths with exact release-content matches, including the resume PDF content type and bytes.
- [x] Keep the GitHub Pages canonical origin (no custom domain), fetch canonical/share paths over HTTPS, and confirm HTTPS enforcement. Recheck redirects if a custom domain is introduced later.
- [x] Recheck that existing profile workflows still operate and no large original assets or private data were added.
- [x] Record implementation completion and verification limits on November 7, 2026.
- [x] Public launch: November 7, 2026 — https://ritamghosh1.github.io/ritamghosh1/.

**Launch gate:** approved real content, functioning resume, responsive layout, accessible navigation, working project/contact links, no Playground remnants, and no blocking console or asset errors.

## 12. Optional enhancements — P3

- [x] Theme switching, with complete contrast checks and a persistent preference, if both themes can be maintained well.
- [x] Add an internship summary and selected resume achievements.
- Deferred: a longer timeline needs more verified experience material.
- Deferred: a writing section needs actual articles; no empty section is published.
- Deferred: a photo lightbox needs a real gallery; if added, require Escape, focus containment/return, and descriptive captions.
- Not selected: direct email plus clipboard feedback covers contact. A future form would need an approved service, labeled errors, and server-side secrets.
- Deferred: custom domain needs a chosen/owned domain. The HTTPS GitHub Pages address is live.
- [x] Add `content/projects.json` with a small Python static generator. No runtime framework or CMS is needed.

## Supplied content and current follow-up

- Source resume: `/Users/ritamghosh/Downloads/Ritam_Ghosh_Resume.pdf`; source portrait: `/Users/ritamghosh/Downloads/Profpic.png`.
- Keep Sentiment Streamer out of the site and downloadable PDF. Await the better project’s name, description, stack, media, and URLs; do not invent a replacement.
- The original resume remains unchanged. The shipped copy contains the other resume content, including technical skills, consolidated onto one page.
- Existing Arrakis content remains from the scaffold; the supplied resume adds detail for Ask the Book and AlgoCoach.
- PDF layout was rendered and inspected. Local HTML structure, anchors, asset paths, responsive image dimensions, PDF text/links, HTTP asset responses, and JavaScript syntax were checked.
- Browser preview failed: browser access host unavailable; native capture returned a ScreenCaptureKit audio/video capture failure. Actual desktop/mobile visual review, real browser interactions, screen-reader/device checks, and deployed-origin downloads remain open.
- Automated verification: `npm run check`, all 11 `npm test` cases, `python3 scripts/check_site.py --http`, and `python3 scripts/check_deployment.py`. GitHub’s Portfolio checks workflow passed. Tests use jsdom/axe for behavior and semantics; they do not measure browser layout or Core Web Vitals.
- Community research tools required an unconnected account; no community-source claims or invented citations are included. Project READMEs and official MDN scroll-snap documentation informed the implementation.

## Maintenance and working notes

- `docs/index.html`: page structure, content, links, metadata.
- `docs/style.css`: design tokens, components, breakpoints, motion styles.
- `docs/script.js`: carousel/filtering, copy-email feedback, footer year, entrances, and reduced-motion handling.
- `docs/theme.js`: early theme selection, persistence, system preference changes, and cross-tab sync.
- `content/projects.json` / `scripts/build_site.py`: maintainable project copy and generated static pages.
- `DESIGN.md` / `DEPLOYMENT.md`: visual decisions, checks, preview steps, and publication constraints.
- `docs/favicon.svg`: site icon.
- `docs/assets/`: optimized portrait images and website resume; add approved screenshots and sharing assets later.
- `README.md`: existing GitHub profile; preserve its content and automation.

After each milestone, check only tasks that were actually implemented and verified. Record unresolved content dependencies here. Review resume freshness, project links, screenshots, social profiles, and time-sensitive claims before every release and periodically after launch.
