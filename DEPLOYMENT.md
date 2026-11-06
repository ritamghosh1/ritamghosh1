# Portfolio preview and release

The website is static HTML in `docs/`. Python and Node are development tools; neither is needed on the web host. The existing GitHub profile README, snake workflow, and WakaTime workflow remain unchanged.

## Preview

```sh
python3 -m http.server 8000 --directory docs
```

Open http://localhost:8000. All content, case studies, email, and resume links work without JavaScript. JavaScript enables the carousel, filtering, theme preference, copy-email feedback, and entrances.

## Edit and verify

Edit `content/projects.json` for project copy and links; run `npm run build` to regenerate the index, case studies, and sitemap. Edit `scripts/build_site.py` for shared markup and other personal content. Edit `docs/style.css`, `docs/theme.js`, and `docs/script.js` for presentation and enhancements. The design is documented in `DESIGN.md`.

```sh
npm ci --ignore-scripts
npm run build
npm run check
npm test
```

`npm run check` validates JavaScript syntax, HTML nesting and headings, local URLs and anchors, metadata, image budgets, content exclusions, and core color contrast pairs. Tests exercise filtering, carousel boundaries and keyboard behavior, focus navigation, theme persistence and denied storage, clipboard success/failure, reduced-motion updates, no-JavaScript content, and automated semantic accessibility on every page. DOM tests do not validate real browser layout or prove screen-reader usability.

`python3 scripts/check_site.py --http` also serves the site under `/ritamghosh1/` on an ephemeral local port and verifies all local HTTP paths and the PDF response. The server shuts down after the check.

To regenerate share artwork and touch icons, install Pillow in a local virtual environment and run `python3 scripts/build_assets.py`. The already-generated images are committed; CI does not need Pillow or source assets from Downloads. The website PDF is the approved reformatted copy with the excluded project removed; it is committed as a static asset.

## GitHub Pages

Intended address: https://ritamghosh1.github.io/ritamghosh1/.

The first release attempt on November 7, 2026 returned HTTP 422 because the account plan did not support Pages for this private repository. Ritam then explicitly authorized changing this repository to public and publishing with GitHub Pages. The repository is now public.

Publishing configuration: `main` branch, `/docs` directory. Static output includes `.nojekyll`; the profile README and its existing workflows are preserved. No paid service, custom domain, or external account is needed. Live deployment status and origin checks are recorded in `todolist.md` after GitHub completes the build.

Future changes: edit source, run the checks above, commit generated files, and push to `main`. Pages publishes the committed `docs/` files. The separate Portfolio checks workflow verifies output consistency, structure, and behavior.

## Manual release checks

Browser access host and native capture both failed during implementation, so these remain required before a verified launch:

- Inspect 320px, phone, tablet, desktop, landscape, and 200% zoom layouts in Chrome, Firefox, and Safari.
- Swipe on an actual touch device, navigate by keyboard, and test with a screen reader.
- Test light/dark/system modes, reduced motion, JavaScript disabled, blocked media, and clipboard denial.
- Verify PDF viewing and downloading, direct case-study links, browser back, and link targets on the deployed origin.
- Review the browser console/network and run mobile Lighthouse. Target LCP ≤2.5s, CLS ≤0.1, and INP ≤200ms; local DOM tests cannot establish these metrics.
- Check the actual social preview at the deployed URL. Absolute share-image URLs cannot be verified while the host returns 404.

Analytics, autoplay, a contact form service, extra personal photos, a writing section, a lightbox, and a custom domain were not added because their prerequisites or a concrete need are absent. Contact uses direct email and clipboard feedback. The Playground replacement and the better new project await Ritam’s content.
