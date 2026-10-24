#!/usr/bin/env python3
"""Dependency-free static sanity checks for the portfolio."""
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parents[1]
required = ("index.html", "styles.css", "script.js", "resume.html")
errors = []
for name in required:
    path = root / name
    if not path.is_file() or path.stat().st_size == 0:
        errors.append(f"Missing or empty required file: {name}")

if not errors:
    html = (root / "index.html").read_text(encoding="utf-8")
    ids = set(re.findall(r'\bid=["\']([^"\']+)["\']', html))
    for required_id in ("home", "about", "skills", "projects", "experience", "contact"):
        if required_id not in ids:
            errors.append(f"Missing required section id: {required_id}")
    for href in re.findall(r'\bhref=["\']#([^"\']+)["\']', html):
        if href not in ids:
            errors.append(f"Broken internal anchor: #{href}")
    for tag in re.findall(r'<img\b[^>]*>', html, flags=re.IGNORECASE):
        if not re.search(r'\balt=["\']', tag, flags=re.IGNORECASE):
            errors.append(f"Image is missing alt text: {tag[:100]}")
    if "<title>" not in html.lower():
        errors.append("Missing document title")
    if 'name="viewport"' not in html.lower():
        errors.append("Missing responsive viewport meta tag")

if errors:
    print("\n".join(f"FAIL: {e}" for e in errors))
    sys.exit(1)
print("PASS: required files, portfolio sections, internal anchors, image alt text, title and viewport checks")
print("NOTE: This is a static sanity check, not a full accessibility, browser or deployment test.")
