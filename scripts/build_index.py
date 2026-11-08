"""Validate every theme in themes/ and write index.json.

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


def validate(file: Path) -> tuple[dict, list[str]]:
    errors = []
    raw = file.read_bytes()
    try:
        theme = tomllib.loads(raw.decode("utf-8"))
    except (tomllib.TOMLDecodeError, UnicodeDecodeError) as e:
        return {}, [f"{file.name}: not valid TOML ({e})"]
    meta = theme.get("meta", {})
    for key in REQUIRED_META:
        if not meta.get(key):
            errors.append(f"{file.name}: [meta] is missing {key}")
    if meta.get("id") and meta["id"] != file.stem:
        errors.append(f"{file.name}: [meta] id must match the file name ({file.stem})")
    for key in ("version", "min-app-version"):
        if meta.get(key) and not VERSION.match(str(meta[key])):
            errors.append(f"{file.name}: {key} must look like 1.2.3")
    if meta.get("licence") and meta["licence"] not in ALLOWED_LICENCES:
        errors.append(f"{file.name}: licence must be one of {sorted(ALLOWED_LICENCES)}")
    if theme.get("base") not in ("light", "dark"):
        errors.append(f"{file.name}: base must be light or dark")
    for key, value in theme.get("colours", {}).items():
        if not COLOUR.match(str(value)):
            errors.append(f"{file.name}: colours.{key} must be a colour like #1a2b3c")
    for path, value in walk(theme):
        if isinstance(value, str) and REMOTE.search(value):
            errors.append(f"{file.name}: {path} points at a remote resource, which themes may not do")
    entry = {
        "id": meta.get("id"),
        "name": meta.get("name"),
        "version": meta.get("version"),
        "description": meta.get("description"),
        "author": meta.get("author"),
        "licence": meta.get("licence"),
        "min-app-version": meta.get("min-app-version"),
        "base": theme.get("base"),
        "file": f"themes/{file.name}",
        "sha256": hashlib.sha256(raw).hexdigest(),
    }
    return entry, errors


def build() -> tuple[str, list[str]]:
    entries, errors = [], []
    for file in sorted(THEMES.glob("*.toml")):
        entry, errs = validate(file)
        errors += errs
        if entry:
            entries.append(entry)
    index = {"format": 1, "themes": entries}
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
        print(f"ok: {text.count('\"id\"')} themes, index.json up to date")
        return 0
    INDEX.write_text(text, encoding="utf-8")
    print("wrote index.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
