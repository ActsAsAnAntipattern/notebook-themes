"""Validate every theme in themes/ and write index.json.

A theme is either a single file, themes/<id>.toml, or a package folder,
themes/<id>/theme.toml with its fonts in themes/<id>/fonts/.

Run with --check in CI: it fails if a theme is invalid or if the committed
index.json does not match what this script would write.
"""

import hashlib
import json
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
THEMES = ROOT / "themes"
INDEX = ROOT / "index.json"

REQUIRED_META = ["id", "name", "version", "description", "author", "licence", "min-app-version"]
VERSION = re.compile(r"^\d+\.\d+\.\d+$")
COLOUR = re.compile(r"^#[0-9a-fA-F]{6}$")
ALLOWED_LICENCES = {"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "CC0-1.0"}
# Fonts may also be OFL (owner decision, 2026-11-08). They ship unmodified.
FONT_LICENCES = {"OFL-1.1", "MIT", "Apache-2.0"}
FONT_SUFFIXES = {".ttf", ".otf"}
MAX_FONT_BYTES = 5 * 1024 * 1024
MAX_THEME_BYTES = 20 * 1024 * 1024
# Themes are data only: nothing may point at the network.
REMOTE = re.compile(r"(https?:|ftp:|url\()", re.IGNORECASE)


def walk(value, path=""):
    if isinstance(value, dict):
        for k, v in value.items():
            yield from walk(v, f"{path}.{k}" if path else k)
    elif isinstance(value, list):
        for i, v in enumerate(value):
            yield from walk(v, f"{path}[{i}]")
    else:
        yield path, value


def file_entry(path: Path, base: Path) -> dict:
    data = path.read_bytes()
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "name": path.relative_to(base).as_posix(),
        "size": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def font_parses(path: Path) -> bool:
    """The app checks fonts with ttf-parser; CI uses fontTools to the same end."""
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
        print("error: fontTools is required for font checks: pip install fonttools", file=sys.stderr)
        sys.exit(2)
    try:
        with TTFont(str(path), lazy=True) as font:
            return "name" in font and "cmap" in font
    except Exception:
        return False


def inside(base: Path, rel: str) -> Path | None:
    """Resolve rel under base; refuse anything that escapes the package."""
    target = (base / rel).resolve()
    return target if target.is_relative_to(base.resolve()) else None


def check_fonts(name: str, theme: dict, base: Path, errors: list[str]) -> list[Path]:
    used = []
    for i, spec in enumerate(theme.get("fonts", {}).get("files", [])):
        where = f"{name}: fonts.files[{i}]"
        for key in ("file", "family", "licence", "licence-file"):
            if not spec.get(key):
                errors.append(f"{where} is missing {key}")
        if spec.get("licence") and spec["licence"] not in FONT_LICENCES:
            errors.append(f"{where}: font licence must be one of {sorted(FONT_LICENCES)}")
        font = inside(base, spec["file"]) if spec.get("file") else None
        if spec.get("file") and font is None:
            errors.append(f"{where}: {spec['file']} points outside the theme folder")
        elif font is not None:
            if font.suffix.lower() not in FONT_SUFFIXES:
                errors.append(f"{where}: fonts must be .ttf or .otf")
            elif not font.is_file():
                errors.append(f"{where}: {spec['file']} does not exist")
            elif font.stat().st_size > MAX_FONT_BYTES:
                errors.append(f"{where}: {spec['file']} is over 5 MB")
            elif not font_parses(font):
                errors.append(f"{where}: {spec['file']} is not a readable font")
            else:
                used.append(font)
        lic = inside(base, spec["licence-file"]) if spec.get("licence-file") else None
        if spec.get("licence-file"):
            if lic is None or not lic.is_file():
                errors.append(f"{where}: licence file {spec['licence-file']} is missing")
            else:
                used.append(lic)
    return used


def validate(toml_path: Path, package: Path | None) -> tuple[dict, list[str]]:
    name = toml_path.relative_to(THEMES).as_posix()
    expected_id = package.name if package else toml_path.stem
    errors = []
    raw = toml_path.read_bytes()
    try:
        theme = tomllib.loads(raw.decode("utf-8"))
    except (tomllib.TOMLDecodeError, UnicodeDecodeError) as e:
        return {}, [f"{name}: not valid TOML ({e})"]
    meta = theme.get("meta", {})
    for key in REQUIRED_META:
        if not meta.get(key):
            errors.append(f"{name}: [meta] is missing {key}")
    if meta.get("id") and meta["id"] != expected_id:
        errors.append(f"{name}: [meta] id must match the {'folder' if package else 'file'} name ({expected_id})")
    for key in ("version", "min-app-version"):
        if meta.get(key) and not VERSION.match(str(meta[key])):
            errors.append(f"{name}: {key} must look like 1.2.3")
    if meta.get("licence") and meta["licence"] not in ALLOWED_LICENCES:
        errors.append(f"{name}: licence must be one of {sorted(ALLOWED_LICENCES)}")
    if theme.get("base") not in ("light", "dark"):
        errors.append(f"{name}: base must be light or dark")
    for key, value in theme.get("colours", {}).items():
        if not COLOUR.match(str(value)):
            errors.append(f"{name}: colours.{key} must be a colour like #1a2b3c")
    for path, value in walk(theme):
        if isinstance(value, str) and REMOTE.search(value):
            errors.append(f"{name}: {path} points at a remote resource, which themes may not do")

    files = [toml_path]
    if theme.get("fonts", {}).get("files"):
        if not package:
            errors.append(f"{name}: a theme with font files must be a folder: themes/{expected_id}/theme.toml")
        else:
            files += check_fonts(name, theme, package, errors)
    base = package or THEMES
    listed = [file_entry(f, base) for f in dict.fromkeys(files)]
    if sum(f["size"] for f in listed) > MAX_THEME_BYTES:
        errors.append(f"{name}: the theme is over 20 MB")

    entry = {
        "id": meta.get("id"),
        "name": meta.get("name"),
        "version": meta.get("version"),
        "description": meta.get("description"),
        "author": meta.get("author"),
        "licence": meta.get("licence"),
        "min-app-version": meta.get("min-app-version"),
        "base": theme.get("base"),
        "package": package is not None,
        "files": listed,
        # Kept for single-file readers: the theme's TOML and its hash.
        "file": listed[0]["path"],
        "sha256": listed[0]["sha256"],
    }
    return entry, errors


def themes():
    for item in sorted(THEMES.iterdir()):
        if item.is_file() and item.suffix == ".toml":
            yield item, None
        elif item.is_dir():
            yield item / "theme.toml", item


def build() -> tuple[str, list[str]]:
    entries, errors = [], []
    for toml_path, package in themes():
        if not toml_path.is_file():
            errors.append(f"{toml_path.parent.name}/: a theme folder needs theme.toml")
            continue
        entry, errs = validate(toml_path, package)
        errors += errs
        if entry:
            entries.append(entry)
    index = {"format": 2, "themes": entries}
    return json.dumps(index, indent=2, ensure_ascii=False) + "\n", errors


def main() -> int:
    text, errors = build()
    for e in errors:
        print(f"error: {e}", file=sys.stderr)
    if errors:
        return 1
    if "--check" in sys.argv:
        if not INDEX.exists() or INDEX.read_text(encoding="utf-8") != text:
            print("error: index.json is out of date. Run: python3 scripts/build_index.py", file=sys.stderr)
            return 1
        print(f"ok: {text.count('\"package\"')} themes, index.json up to date")
        return 0
    INDEX.write_text(text, encoding="utf-8")
    print("wrote index.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
