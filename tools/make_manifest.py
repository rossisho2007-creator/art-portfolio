"""Regenerate assets/js/works.js from assets/js/works.json."""
import json, io, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(ROOT, "assets", "js", "works.json")
DST  = os.path.join(ROOT, "assets", "js", "works.js")

with io.open(SRC, encoding="utf-8") as f:
    data = json.load(f)

with io.open(DST, "w", encoding="utf-8") as f:
    f.write("// Auto-generated gallery manifest. Edit tools/build_assets.py and re-run to regenerate.\n")
    f.write("const WORKS = ")
    f.write(json.dumps(data, indent=2, ensure_ascii=False))
    f.write(";\n")

print("works.js written, %d entries" % len(data))
