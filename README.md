# Rossi Sho — Art Portfolio

Character design, concept art and game art. Built as a static site so it can be hosted
free on GitHub Pages and linked directly from internship applications.

**Live site:** https://rossisho2007-creator.github.io/art-portfolio/

---

## What's in it

| Section | Pieces | What it shows |
|---|---|---|
| **Fish Game** | 15 | Ongoing original narrative game — cast design, two expression sprite sets (shown as albums), key art, HUD mockup, title treatment |
| **Fan Art — My Singing Monsters** | 3 | Rendered fan art; three pieces officially reposted by Big Blue Bubble |
| **Illustration & Character Concepts** | 8 | Personal narrative illustration and original character work |
| **Commissioned & Product** | 2 | Paid merch design drawn to a client brief and real print constraints |

Published as **Sottonos** — [instagram.com/sottonos](https://www.instagram.com/sottonos).

Fan art pieces were originally posted under an older handle (`@Fishettoob`) which is no
longer in active use; the signature is still visible in those images.

### A note on Fish Game

Fish Game is in active development. This portfolio shows **artwork only** — the story,
script and design documents are deliberately not published here while the project is
unreleased.

---

## Features

- Filterable gallery by discipline
- Album tiles: near-identical sets (sprite expression sheets) collapse into one card and
  open as a slideshow with dot navigation
- Lightbox viewer with keyboard (`←` `→` `Esc`), swipe and focus trapping
- Lazy-loaded thumbnails with full-resolution images on open
- Responsive down to small phones
- No build step, no dependencies, no tracking

---

## Running it locally

It's plain HTML/CSS/JS — open `index.html` in a browser and it works.

For a local server instead:

```bash
python -m http.server 8000
# → http://localhost:8000
```

---

## Adding or changing artwork

Artwork is driven by a single generated manifest, so you never hand-edit the gallery HTML.

1. Open `tools/build_assets.py` and add an entry to the `ITEMS` list:

   ```python
   ("my-new-piece",                       # url-safe slug, becomes the filename
    r"C:\path\to\the\original.png",       # source file anywhere on disk
    "illustration",                       # fish-game | creatures | illustration | commissions
    "Piece Title",                        # shown on the tile and in the lightbox
    "One or two sentences on what the piece solves.",
    ["illustration", "painting"],         # filter tags
    None),                                # album id, or None for a standalone piece
   ```

   To add a piece to an **album** (a set that collapses into one clickable slideshow card),
   pass an album id as the last field and make sure that id exists in the `ALBUMS` dict at
   the top of the same file.

2. Run it:

   ```bash
   python tools/build_assets.py
   ```

   This writes an optimised full-size JPEG to `images/full/`, an 800px thumbnail to
   `images/thumb/`, and regenerates `assets/js/works.json`.

3. Regenerate the JS manifest the page actually loads:

   ```bash
   python tools/make_manifest.py
   ```

4. Commit and push — GitHub Pages redeploys automatically.

To **reorder** pieces, move them within `ITEMS`. To **remove** one, delete its entry and
the matching files in `images/full/` and `images/thumb/`.

### Section ordering

Sections render in the order set by `SECTIONS` at the top of `assets/js/main.js`, which
must match the group `data-group` attributes in `index.html`.

---

## Structure

```
.
├── index.html              page content and section copy
├── assets/
│   ├── css/style.css       all styling
│   └── js/
│       ├── works.js        generated manifest the page loads
│       ├── works.json      generated manifest (source of truth)
│       └── main.js         gallery, filtering, lightbox
├── images/
│   ├── full/               full-resolution, lightbox
│   └── thumb/              800px, grid
└── tools/
    ├── build_assets.py     processes source art → images/ + works.json
    └── make_manifest.py    works.json → works.js
```

---

## Copyright

All artwork in this repository is © Rossi Sho and is **not** licensed for reuse,
redistribution, training or derivative work. The site code may be reused freely.
