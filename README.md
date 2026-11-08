# Notebook themes

Colour schemes for Notebook, a local-first Markdown notebook. Each theme is one TOML file in `themes/`.

## Install a theme

- **From the app:** Appearance, then Browse themes. The app downloads only when you open that screen.
- **From a file:** download a `.toml` file from `themes/`, then use Appearance, then Install theme from file. This works with no internet connection.

The app checks each download against the SHA-256 listed in `index.json` and refuses a mismatch.

Your own preferences always win over a theme. Every setting has "Reset to theme default".

## Themes here

| Theme | Base | Description |
| --- | --- | --- |
| Paper | light | A warm off-white page with ink-blue links. |
| Sepia | light | Aged paper tones for long reading. |
| Slate | dark | Cool blue-grey for evening work. |
| Night | dark | Near-black with warm amber accents. |

## Theme format

A theme is data only, never code. It may not reference URLs or remote resources, and fonts must be ones already installed or bundled with the app.

```toml
base = "light"                  # light or dark: built-in values for anything not set here

[meta]
id = "paper"                    # must match the file name
name = "Paper"
version = "1.0.0"
description = "A warm off-white page with ink-blue links."
author = "Your name"
licence = "MIT"                 # MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC or CC0-1.0
min-app-version = "0.1.0"

[colours]
background = "#fbfaf8"
text = "#24221f"
accent = "#3b6ea8"
```

Everything else is optional: fonts, editor layout, each heading level, text styles, lists, tags and tag colours, both sidebars, the calendar (marker shapes, sizes and colours per level, the selected day and today), the status bar, shadows and date formats.

## Contributing a theme

1. Add `themes/<id>.toml`.
2. Run `python3 scripts/build_index.py` to validate it and update `index.json`.
3. Open a pull request. CI runs `python3 scripts/build_index.py --check` and fails if a theme is invalid or `index.json` is out of date.

By contributing you agree your theme is released under the licence named in its `[meta]` table.

## Licence

MIT. See `LICENSE`.
