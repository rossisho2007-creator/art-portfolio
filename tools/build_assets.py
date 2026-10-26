import os, json
from PIL import Image

DL  = r"C:\Users\Lenovo\Downloads"
FG  = r"C:\Users\Lenovo\OneDrive\Fish Game"
OUT = r"C:\Users\Lenovo\art-portfolio"

CA = os.path.join(FG, "Character Art", "Main Characters")
OC = os.path.join(FG, "Original Concept")

# slug, source, section, title, caption, tags
ITEMS = [
 # ---------- FISH GAME ----------
 ("deep-dark-key-art", os.path.join(OC, "Ang-ri_V1_Poster_The_Deep_Dark.jpeg"),
  "fish-game", "The Deep Dark - Key Art",
  "Promotional key art for Chapter 1. Pure black-and-white rendering keeps the read legible at thumbnail size while establishing the chapter's claustrophobic, lightless tone.",
  ["key art", "marketing", "monochrome"]),

 ("coelacanth-poster", os.path.join(DL, "Game concept art for indie horror.jpeg"),
  "fish-game", "Coelacanth - Title Treatment",
  "Early title card and logotype study. Hand-lettered type paired with anglerfish and skeletal motifs to set the indie-horror register before a single line of dialogue.",
  ["key art", "typography", "monochrome"]),

 ("hud-health-bar", os.path.join(DL, "Personal Game Art 1.jpeg"),
  "fish-game", "Ang-ri - Portrait HUD & Health Bar",
  "In-game HUD mockup: character bust framed by a bone cartouche with heart-pip health. Designed so the frame art survives cropping to a 1:1 UI slot.",
  ["UI/UX", "HUD", "character"]),

 ("angri-character-sheet", os.path.join(CA, "Ang-ri", "Ang-ri Sketches", "Ang-ri_V1_Character_Sheet_Scrapped.jpeg"),
  "fish-game", "Ang-ri - Character Sheet (V1, scrapped)",
  "A full-body pass that was ultimately cut. Kept in the portfolio deliberately: the bioluminescent lure, fin-ears and tail silhouette all survived into the final design.",
  ["character design", "process"]),

 ("group-concept-sketch", os.path.join(CA, "Group Sketches", "Group_V1_Concept_Sketch.jpeg"),
  "fish-game", "Main Cast - Ensemble Sketches",
  "Exploratory pass on the core trio. Silhouette and proportion are varied first so each character reads distinctly before any rendering is committed.",
  ["character design", "sketch", "ensemble"]),

 ("angri-sprite-idle", os.path.join(CA, "Ang-ri", "Ang_ri_V1_Sprites", "Ang-ri_V1_Idle.jpeg"),
  "fish-game", "Ang-ri - Idle",
  "Neutral dialogue sprite. The base pose every other expression is keyed from.",
  ["sprite", "expression"]),

 ("angri-sprite-joy", os.path.join(CA, "Ang-ri", "Ang_ri_V1_Sprites", "Ang-ri_V1_Joy.jpeg"),
  "fish-game", "Ang-ri - Joy",
  "Expression variant. Brow and lure position carry the emotion so the body art can be reused.",
  ["sprite", "expression"]),

 ("angri-sprite-depressed", os.path.join(CA, "Ang-ri", "Ang_ri_V1_Sprites", "Ang-ri_V1_Depressed.jpeg"),
  "fish-game", "Ang-ri - Downcast",
  "Expression variant written for the Chapter 1 loss beat.",
  ["sprite", "expression"]),

 ("angri-sprite-nooutline", os.path.join(CA, "Ang-ri", "Ang_ri_V1_Sprites", "Ang-ri_V1_noOutline.jpeg"),
  "fish-game", "Ang-ri - Outline Test",
  "Outline-free variant, tested for readability against dark underwater backgrounds.",
  ["sprite", "process"]),

 ("yuli-sprite-base", os.path.join(CA, "Yuli", "Yuli_V1_Sprites", "Yuli_V1.jpeg"),
  "fish-game", "Yuli - Idle",
  "Neutral dialogue sprite for Ang-ri's adopted sister.",
  ["sprite", "expression"]),

 ("yuli-sprite-happy", os.path.join(CA, "Yuli", "Yuli_V1_Sprites", "Yuli_V1_Happy.jpeg"),
  "fish-game", "Yuli - Happy",
  "Expression variant.",
  ["sprite", "expression"]),

 ("yuli-sprite-sigh", os.path.join(CA, "Yuli", "Yuli_V1_Sprites", "Yuli_V1_Sigh.jpeg"),
  "fish-game", "Yuli - Sigh",
  "Expression variant.",
  ["sprite", "expression"]),

 ("yuli-sprite-nooutline", os.path.join(CA, "Yuli", "Yuli_V1_Sprites", "Yuli without outline.jpeg"),
  "fish-game", "Yuli - Outline Test",
  "Outline-free variant for background-contrast testing.",
  ["sprite", "process"]),

 ("angri-sprite-original", os.path.join(OC, "Ang-ri_V1_Sprite_.jpeg"),
  "fish-game", "Ang-ri - First Sprite Pass",
  "The earliest rendered sprite, kept as a reference point for how far the design has moved.",
  ["sprite", "process"]),

 ("kimono-concept-sketch", os.path.join(DL, "Concept sketch of game character.jpeg"),
  "fish-game", "Robed Figure - Concept Sketch",
  "Construction sketch for a court character. Drapery and ribbon flow are blocked in loosely to test how the silhouette moves underwater.",
  ["sketch", "costume", "process"]),

 # ---------- CREATURE & ENVIRONMENT ----------
 ("creature-cloud-beast", os.path.join(DL, "Game Art 1.jpeg"),
  "creatures", "Sun-Eye Guardian",
  "Boss-tier creature design. The floating solar sigil doubles as a readable tell for attack timing; layered feather and cloud forms keep the mass legible against a bright sky.",
  ["creature design", "boss", "rendering"]),

 ("creature-pond", os.path.join(DL, "Game Art 2.jpeg"),
  "creatures", "Lily Pond - Encounter",
  "Two-creature staging in a fully painted environment. Depth is carried by water clarity and cast shadow rather than atmospheric haze.",
  ["creature design", "environment", "rendering"]),

 ("creature-blossom", os.path.join(DL, "Game Art 3.jpeg"),
  "creatures", "Blossom Valley - Encounter",
  "Companion piece in a warmer key. A backlit cherry canopy and low horizon push the two creatures forward as the focal read.",
  ["creature design", "environment", "rendering"]),

 # ---------- ILLUSTRATION ----------
 ("illus-crowned", os.path.join(DL, "Art concept 1.jpeg"),
  "illustration", "Crowned",
  "Painterly figure study. Scale is built entirely through relation - a small body cradled in oversized hands beneath a severed face.",
  ["illustration", "painting", "surreal"]),

 ("illus-rabbit-room", os.path.join(DL, "Art concept 2.jpeg"),
  "illustration", "Rabbit Room",
  "Horror composition in a restricted red and black key. The duplicated figure and encroaching hands build the threat without an explicit subject.",
  ["illustration", "painting", "horror"]),

 ("illus-reliquary", os.path.join(DL, "Art concept 3.jpeg"),
  "illustration", "Reliquary",
  "Flat primary blocking against painted stained glass. Pushes how far a palette can be reduced before form stops reading.",
  ["illustration", "painting", "graphic"]),

 ("illus-vday", os.path.join(DL, "Art concept 4.jpeg"),
  "illustration", "Offering",
  "Seasonal illustration mixing a rendered portrait with an inset chibi - a deliberate test of two rendering registers inside one frame.",
  ["illustration", "painting", "character"]),

 ("illus-ribcage", os.path.join(DL, "Art concept 5.jpeg"),
  "illustration", "Pixel Heart",
  "Anatomical framing with an intentionally low-resolution heart. The resolution clash is the subject rather than an artefact.",
  ["illustration", "painting", "graphic"]),

 ("illus-hanfu", os.path.join(DL, "Art Concept 6.jpeg"),
  "illustration", "Still Season",
  "A quieter register: soft-edged rendering, patterned flats and a high-key palette, built to contrast the darker work in this section.",
  ["illustration", "painting", "portrait"]),

 ("illus-oni-portrait", os.path.join(DL, "Character art 1.jpeg"),
  "illustration", "Grin",
  "Sticker-style character bust. A hard white keyline and torn red field make the piece work as a standalone cut-out asset.",
  ["character design", "illustration"]),

 ("illus-oc-sheet", os.path.join(DL, "Character art 2.jpeg"),
  "illustration", "Original Character - Reference Sheet",
  "Working reference sheet: a rendered bust paired with a chibi full-body and margin notes, formatted the way a sheet gets handed to a collaborator.",
  ["character design", "reference sheet"]),

 # ---------- COMMISSIONED ----------
 ("merch-keychains-pair", os.path.join(DL, "Chibi art for a school event (Merch).jpeg"),
  "commissions", "Qanata - Acrylic Keychain Pair",
  "Commissioned merchandise for a school event. Drawn to a keychain cut-line with a bleed outline, hole placement and a branded colourway per character.",
  ["commission", "merch", "product"]),

 ("merch-keychain-tiwi", os.path.join(DL, "Chibi art for a school event (Merch) 2.jpeg"),
  "commissions", "Tiwi - Acrylic Keychain",
  "Second design in the same run. A softer palette and grass base vary the silhouette across the set.",
  ["commission", "merch", "product"]),
]

manifest = []
for slug, src, section, title, caption, tags in ITEMS:
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

    manifest.append({
        "slug": slug, "section": section, "title": title,
        "caption": caption, "tags": tags, "w": w, "h": h,
        "full": "images/full/%s.jpg" % slug,
        "thumb": "images/thumb/%s.jpg" % slug,
    })
    print("%-26s %5dx%-5d %s" % (slug, w, h, section))

with open(os.path.join(OUT, "assets", "js", "works.json"), "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

print("\nTOTAL: %d pieces" % len(manifest))
for s in ["fish-game", "creatures", "illustration", "commissions"]:
    print("  %-14s %d" % (s, sum(1 for m in manifest if m["section"] == s)))
