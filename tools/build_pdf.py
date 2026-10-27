"""
Renders index.html to Rossi-Sho-Portfolio.pdf using headless Chrome.

Why a pre-built file rather than letting the browser print on demand:
a visitor's print dialog defaults to their paper size (A4 vs Letter) and
leaves "Background graphics" switched off, so the document they'd get is
not the document we designed. Shipping a rendered file means every
recruiter downloads exactly the same thing, in one click, with no dialog.

Run from the repo root:  python tools/build_pdf.py
Re-run whenever the artwork or page copy changes.
"""

import os, sys, subprocess, tempfile, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT  = os.path.join(ROOT, "Rossi-Sho-Portfolio.pdf")
PAGE = os.path.join(ROOT, "index.html")

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe"),
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]


def find_chrome():
    for p in CHROME_CANDIDATES:
        if os.path.exists(p):
            return p
    found = shutil.which("chrome") or shutil.which("google-chrome") or shutil.which("chromium")
    if found:
        return found
    sys.exit("Chrome not found. Install Chrome or add its path to CHROME_CANDIDATES.")


def main():
    chrome = find_chrome()
    url = "file:///" + PAGE.replace("\\", "/")
    profile = tempfile.mkdtemp(prefix="pdfbuild-")

    cmd = [
        chrome,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",          # no browser URL/date furniture
        "--virtual-time-budget=30000",     # let lazy images and fonts settle
        "--user-data-dir=" + profile,
        "--print-to-pdf=" + OUT,
        url,
    ]

    subprocess.run(cmd, capture_output=True, timeout=180)
    shutil.rmtree(profile, ignore_errors=True)

    if not os.path.exists(OUT):
        sys.exit("Chrome did not write a PDF.")

    size = os.path.getsize(OUT)
    pages = "?"
    try:
        import pymupdf
        pages = len(pymupdf.open(OUT))
    except Exception:
        pass

    print("%s  (%.1f MB, %s pages)" % (os.path.basename(OUT), size / 1048576.0, pages))


if __name__ == "__main__":
    main()
