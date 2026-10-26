"""
Processes source artwork into optimised web images and regenerates the gallery
manifest (assets/js/works.json).

Run from the repo root:   python tools/build_assets.py
Then:                     python tools/make_manifest.py
"""

import os, json
from PIL import Image

DL  = r"C:\Users\Lenovo\Downloads"
FG  = r"C:\Users\Lenovo\OneDrive\Fish Game"
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CA = os.path.join(FG, "Character Art", "Main Characters")
OC = os.path.join(FG, "Original Concept")

# ---------------------------------------------------------------------------
# Albums: sets of near-identical pieces that collapse into one clickable card
# and open as a slideshow. Keyed by album id; `cover` is a slug from ITEMS.
# ---------------------------------------------------------------------------
ALBUMS = {
    "angri-expressions": {
        "section": "fish-game",
        "title": "Ang-ri - Expression Set",
        "cover": "angri-sprite-idle",
        "caption": "The full dialogue sprite set for the player character. Every expression is "
                   "keyed off one base pose so the set stays visually consistent and cheap to "
                   "extend when new story beats need new emotions.",
        "tags": ["sprite set", "expression", "production"],
    },
    "yuli-expressions": {
        "section": "fish-game",
        "title": "Yuli - Expression Set",
        "cover": "yuli-sprite-base",
        "caption": "Matching dialogue sprite set for Yuli. Built to the same base-pose rule as "
                   "Ang-ri's so the two characters sit together on screen without one reading "
                   "as drawn later or by someone else.",
        "tags": ["sprite set", "expression", "production"],
    },
}

# slug, source, section, title, caption, tags, album
ITEMS = [
 # ---------------- FISH GAME ----------------
 ("deep-dark-key-art", os.path.join(OC, "Ang-ri_V1_Poster_The_Deep_Dark.jpeg"),
  "fish-game", "The Deep Dark - Key Art",
  "Promotional key art for Chapter 1. Pure black-and-white rendering keeps the read legible at "
  "thumbnail size while establishing the chapter's claustrophobic, lightless tone.",
  ["key art", "marketing", "monochrome"], None),

 ("coelacanth-poster", os.path.join(DL, "Game concept art for indie horror.jpeg"),
  "fish-game", "Coelacanth - Title Treatment",
  "Early title card and logotype study. Hand-lettered type paired with anglerfish and skeletal "
  "motifs to set the indie-horror register before a single line of dialogue.",
  ["key art", "typography", "monochrome"], None),

 ("hud-health-bar", os.path.join(DL, "Personal Game Art 1.jpeg"),
  "fish-game", "Ang-ri - Portrait HUD & Health Bar",
  "In-game HUD mockup: character bust framed by a bone cartouche with heart-pip health. "
  "Designed so the frame art survives cropping to a 1:1 UI slot.",
  ["UI/UX", "HUD", "character"], None),

 ("angri-character-sheet", os.path.join(CA, "Ang-ri", "Ang-ri Sketches", "Ang-ri_V1_Character_Sheet_Scrapped.jpeg"),
  "fish-game", "Ang-ri - Character Sheet (V1, scrapped)",
  "A full-body pass that was ultimately cut. Kept in the portfolio deliberately: the "
  "bioluminescent lure, fin-ears and tail silhouette all survived into the final design.",
  ["character design", "process"], None),

 ("group-concept-sketch", os.path.join(CA, "Group Sketches", "Group_V1_Concept_Sketch.jpeg"),
  "fish-game", "Main Cast - Ensemble Sketches",
  "Exploratory pass on the core trio. Silhouette and proportion are varied first so each "
  "character reads distinctly before any rendering is committed.",
  ["character design", "sketch", "ensemble"], None),

 ("angri-sprite-original", os.path.join(OC, "Ang-ri_V1_Sprite_.jpeg"),
  "fish-game", "Ang-ri - First Sprite Pass",
  "The earliest rendered sprite, kept as a reference point for how far the design has moved.",
  ["sprite", "process"], None),

 ("kimono-concept-sketch", os.path.join(DL, "Concept sketch of game character.jpeg"),
  "fish-game", "Robed Figure - Concept Sketch",
  "Construction sketch for a court character. Drapery and ribbon flow are blocked in loosely "
  "to test how the silhouette moves underwater.",
  ["sketch", "costume", "process"], None),

 # --- Ang-ri expression album ---
 ("angri-sprite-idle", os.path.join(CA, "Ang-ri", "Ang_ri_V1_Sprites", "Ang-ri_V1_Idle.jpeg"),
  "fish-game", "Idle",
  "Neutral dialogue sprite. The base pose every other expression is keyed from.",
  ["sprite"], "angri-expressions"),
 ("angri-sprite-joy", os.path.join(CA, "Ang-ri", "Ang_ri_V1_Sprites", "Ang-ri_V1_Joy.jpeg"),
  "fish-game", "Joy",
  "Brow and lure position carry the emotion so the body art stays reusable.",
  ["sprite"], "angri-expressions"),
 ("angri-sprite-depressed", os.path.join(CA, "Ang-ri", "Ang_ri_V1_Sprites", "Ang-ri_V1_Depressed.jpeg"),
  "fish-game", "Downcast",
  "Written for the Chapter 1 loss beat.",
  ["sprite"], "angri-expressions"),
 ("angri-sprite-nooutline", os.path.join(CA, "Ang-ri", "Ang_ri_V1_Sprites", "Ang-ri_V1_noOutline.jpeg"),
  "fish-game", "Outline Test",
  "Outline-free variant, tested for readability against dark underwater backgrounds.",
  ["sprite", "process"], "angri-expressions"),

 # --- Yuli expression album ---
 ("yuli-sprite-base", os.path.join(CA, "Yuli", "Yuli_V1_Sprites", "Yuli_V1.jpeg"),
  "fish-game", "Idle",
  "Neutral dialogue sprite for Ang-ri's adopted sister.",
  ["sprite"], "yuli-expressions"),
 ("yuli-sprite-happy", os.path.join(CA, "Yuli", "Yuli_V1_Sprites", "Yuli_V1_Happy.jpeg"),
  "fish-game", "Happy",
  "Expression variant.",
  ["sprite"], "yuli-expressions"),
 ("yuli-sprite-sigh", os.path.join(CA, "Yuli", "Yuli_V1_Sprites", "Yuli_V1_Sigh.jpeg"),
  "fish-game", "Sigh",
  "Expression variant.",
  ["sprite"], "yuli-expressions"),
 ("yuli-sprite-nooutline", os.path.join(CA, "Yuli", "Yuli_V1_Sprites", "Yuli without outline.jpeg"),
  "fish-game", "Outline Test",
  "Outline-free variant for background-contrast testing.",
  ["sprite", "process"], "yuli-expressions"),

 # ---------------- FAN ART: MY SINGING MONSTERS ----------------
 ("msm-sky-guardian", os.path.join(DL, "Game Art 1.jpeg"),
  "fanart", "Sky Guardian",
  "Fan art rendered at full illustration scale. Layered feather, cloud and fur forms keep a "
  "very large silhouette readable against a bright, low-contrast sky - the hardest part of the "
  "piece was stopping the creature from dissolving into its background.",
  ["fan art", "rendering", "creature"], None),

 ("msm-lily-pond", os.path.join(DL, "Game Art 2.jpeg"),
  "fanart", "Lily Pond",
  "Two characters staged in a fully painted environment. Depth is carried by water clarity and "
  "cast shadow rather than atmospheric haze, so the foreground stays fully saturated.",
  ["fan art", "environment", "rendering"], None),

 ("msm-blossom-valley", os.path.join(DL, "Game Art 3.jpeg"),
  "fanart", "Blossom Valley",
  "Companion piece in a warmer key. A backlit cherry canopy and low horizon push both "
  "characters forward as the focal read.",
  ["fan art", "environment", "rendering"], None),

 # ---------------- ILLUSTRATION ----------------
 ("illus-crowned", os.path.join(DL, "Art concept 1.jpeg"),
  "illustration", "Crowned",
  "Painterly figure study. Scale is built entirely through relation - a small body cradled in "
  "oversized hands beneath a severed face.",
  ["illustration", "painting", "surreal"], None),

 ("illus-rabbit-room", os.path.join(DL, "Art concept 2.jpeg"),
  "illustration", "Rabbit Room",
  "Horror composition in a restricted red and black key. The duplicated figure and encroaching "
  "hands build the threat without an explicit subject.",
  ["illustration", "painting", "horror"], None),

 ("illus-reliquary", os.path.join(DL, "Art concept 3.jpeg"),
  "illustration", "Reliquary",
  "Flat primary blocking against painted stained glass. Pushes how far a palette can be reduced "
  "before form stops reading.",
  ["illustration", "painting", "graphic"], None),

 ("illus-vday", os.path.join(DL, "Art concept 4.jpeg"),
  "illustration", "Offering",
  "Seasonal illustration mixing a rendered portrait with an inset chibi - a deliberate test of "
  "two rendering registers inside one frame.",
  ["illustration", "painting", "character"], None),

 ("illus-ribcage", os.path.join(DL, "Art concept 5.jpeg"),
  "illustration", "Pixel Heart",
  "Anatomical framing with an intentionally low-resolution heart. The resolution clash is the "
  "subject rather than an artefact.",
  ["illustration", "painting", "graphic"], None),

 ("illus-hanfu", os.path.join(DL, "Art Concept 6.jpeg"),
  "illustration", "Still Season",
  "A quieter register: soft-edged rendering, patterned flats and a high-key palette, built to "
  "contrast the darker work in this section.",
  ["illustration", "painting", "portrait"], None),

 ("illus-oni-portrait", os.path.join(DL, "Character art 1.jpeg"),
  "illustration", "Grin",
  "Sticker-style character bust. A hard white keyline and torn red field make the piece work as "
  "a standalone cut-out asset.",
  ["character design", "illustration"], None),

 ("illus-oc-sheet", os.path.join(DL, "Character art 2.jpeg"),
  "illustration", "Original Character - Reference Sheet",
  "Working reference sheet: a rendered bust paired with a chibi full-body and margin notes, "
  "formatted the way a sheet gets handed to a collaborator.",
  ["character design", "reference sheet"], None),

 # ---------------- COMMISSIONED ----------------
 ("merch-keychains-pair", os.path.join(DL, "Chibi art for a school event (Merch).jpeg"),
  "commissions", "Qanata - Acrylic Keychain Pair",
  "Commissioned merchandise for a school event. Drawn to a keychain cut-line with a bleed "
  "outline, hole placement and a branded colourway per character.",
  ["commission", "merch", "product"], None),

 ("merch-keychain-tiwi", os.path.join(DL, "Chibi art for a school event (Merch) 2.jpeg"),
  "commissions", "Tiwi - Acrylic Keychain",
  "Second design in the same run. A softer palette and grass base vary the silhouette across "
  "the set.",
  ["commission", "merch", "product"], None),
]


# ---------------------------------------------------------------------------
# Profile picture. Cropped from the original "Crowned" artwork rather than
# downloaded from Instagram, so it stays sharp (the Instagram CDN only serves
# a 150x150 thumbnail, and its URLs expire).
# ---------------------------------------------------------------------------
PROFILE = {
    "source": "illus-crowned",          # slug from ITEMS, read back from images/full
    "box": (80, 360, 390, 670),         # left, top, right, bottom in source pixels
    "size": 400,                        # output square size
    "out": "images/profile.jpg",
}


def build_profile():
    src = os.path.join(OUT, "images", "full", PROFILE["source"] + ".jpg")
    if not os.path.exists(src):
        print("profile: source missing,", src)
        return
    im = Image.open(src).convert("RGB").crop(PROFILE["box"])
    im = im.resize((PROFILE["size"], PROFILE["size"]), Image.LANCZOS)
    im.save(os.path.join(OUT, PROFILE["out"]), "JPEG", quality=90, optimize=True)
    print("profile: %s -> %s (%dpx)" % (PROFILE["source"], PROFILE["out"], PROFILE["size"]))


def main():
    manifest = []
    for slug, src, section, title, caption, tags, album in ITEMS:
        if not os.path.exists(src):
            print("MISSING:", src)
            continue

        im = Image.open(src).convert("RGB")
        w, h = im.size

        im.save(os.path.join(OUT, "images", "full", slug + ".jpg"),
                "JPEG", quality=88, optimize=True, progressive=True)

        th = im.copy()
        th.thumbnail((800, 800), Image.LANCZOS)
        th.save(os.path.join(OUT, "images", "thumb", slug + ".jpg"),
                "JPEG", quality=82, optimize=True, progressive=True)

        entry = {
            "slug": slug, "section": section, "title": title,
            "caption": caption, "tags": tags, "w": w, "h": h,
            "full": "images/full/%s.jpg" % slug,
            "thumb": "images/thumb/%s.jpg" % slug,
        }
        if album:
            entry["album"] = album
        manifest.append(entry)
        print("%-24s %5dx%-5d %-13s %s" % (slug, w, h, section, album or ""))

    data = {"albums": ALBUMS, "works": manifest}
    with open(os.path.join(OUT, "assets", "js", "works.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    build_profile()

    loose = sum(1 for m in manifest if "album" not in m)
    print("\n%d images  (%d standalone + %d in %d albums)"
          % (len(manifest), loose, len(manifest) - loose, len(ALBUMS)))
    for s in ["fish-game", "fanart", "illustration", "commissions"]:
        n = sum(1 for m in manifest if m["section"] == s)
        print("  %-13s %d" % (s, n))


if __name__ == "__main__":
    main()
