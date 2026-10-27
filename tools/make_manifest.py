"""
Regenerates assets/js/works.js from assets/js/works.json, then version-stamps
the CSS/JS references in index.html with a content hash.

The stamp matters: browsers cache by URL, so changing a Cache-Control header
does nothing for a copy already sitting in someone's cache. Only a new URL
forces a re-fetch. Without this, fresh HTML can pair with a stale script and
features silently do nothing.

Run from the repo root:  python tools/make_manifest.py
"""

import json, io, os, re, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(ROOT, "assets", "js", "works.json")
DST  = os.path.join(ROOT, "assets", "js", "works.js")
HTML = os.path.join(ROOT, "index.html")

# Files whose references in index.html get a ?v= stamp.
VERSIONED = [
    "assets/css/style.css",
    "assets/js/works.js",
    "assets/js/main.js",
]


def build_works_js():
    with io.open(SRC, encoding="utf-8") as f:
        data = json.load(f)

    with io.open(DST, "w", encoding="utf-8") as f:
        f.write("// Auto-generated gallery manifest.\n")
        f.write("// Edit tools/build_assets.py and re-run it, then run tools/make_manifest.py.\n")
        f.write("const ALBUMS = ")
        f.write(json.dumps(data["albums"], indent=2, ensure_ascii=False))
        f.write(";\n\nconst WORKS = ")
        f.write(json.dumps(data["works"], indent=2, ensure_ascii=False))
        f.write(";\n")

    print("works.js written: %d works, %d albums" % (len(data["works"]), len(data["albums"])))


def stamp_assets():
    digest = hashlib.sha256()
    for rel in VERSIONED:
        path = os.path.join(ROOT, *rel.split("/"))
        if not os.path.exists(path):
            print("stamp: missing", rel)
            continue
        with io.open(path, "rb") as f:
            digest.update(f.read())
    version = digest.hexdigest()[:8]

    with io.open(HTML, encoding="utf-8") as f:
        html = f.read()

    changed = 0
    for rel in VERSIONED:
        # Match the path with or without an existing ?v= stamp.
        pattern = re.compile(re.escape(rel) + r'(\?v=[0-9a-f]+)?')
        html, n = pattern.subn(rel + "?v=" + version, html)
        changed += n

    with io.open(HTML, "w", encoding="utf-8") as f:
        f.write(html)

    print("stamped %d references with ?v=%s" % (changed, version))


if __name__ == "__main__":
    build_works_js()
    stamp_assets()
