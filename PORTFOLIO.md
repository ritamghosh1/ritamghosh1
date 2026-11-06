# Portfolio website

The website is in `docs/`. The root profile README and its existing automation are preserved.

## Preview locally

```sh
cd ~/Desktop/ritamghosh1
python3 -m http.server 8000 --directory docs
```

Open http://localhost:8000. No build step or package installation is required.

## Publish in this repository

1. Commit and push the website files to `main`.
2. In GitHub **Settings → Pages**, choose **Deploy from a branch**.
3. Select **main** and **/docs**, then save.
4. The expected address is https://ritamghosh1.github.io/ritamghosh1/.

All local assets use relative paths so they work under the repository subpath.

## Edit

- `docs/index.html`: biography, projects, social links, metadata.
- `docs/style.css`: design tokens, layout, mobile styles.
- `docs/script.js`: project filters, copy-email feedback, breadth-first search demo.
- `docs/favicon.svg`: site icon.

Google Fonts is the only third-party resource loaded by the page; system sans-serif fonts are the fallback. No analytics, tracking, remote profile API calls, or secrets are needed. Core content and navigation work without JavaScript; enhanced controls appear only when JavaScript runs. Reduced-motion preferences skip the maze animation.

## Content provenance

Reviewed November 7, 2026:

- Profile and contact links: https://github.com/ritamghosh1/ritamghosh1/blob/main/README.md
- Ask the Book: https://github.com/ritamghosh1/ask_the_book/blob/main/README.md
- AlgoCoach: https://github.com/ritamghosh1/Algo_Coach/blob/main/README.md
- Arrakis: https://github.com/ritamghosh1/Arrakis/blob/main/README.md

The Arrakis description identifies it as a team project and describes the assigned role in its README. Project graphics are illustrative, not application screenshots. No live ratings, placement claims, or unverified employment history are included. The LeetCode link uses AlgoRithmic91 from the profile URL rather than the mismatched badge label. LinkedIn and some competitive-programming pages could not be read through the research tool, so they are included as profile links without additional claims.
