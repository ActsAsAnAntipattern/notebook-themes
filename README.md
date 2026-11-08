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

## What can be customised

Everything a theme can set, and everything a person can change in Settings. Where both can set something, **the person's preference always wins**, and every preference has "Reset to theme default". Switching themes never clears preferences. Values not set by either fall back to the built-in default.

Status: this is the planned v1 list. The theme file format is still settling, so key names may change before the first release.

### Colours and surfaces

| Setting | Values | Theme | User |
| --- | --- | --- | --- |
| Colour scheme | System (follows light or dark), Paper, Sepia, Slate, Night, or any installed theme | Yes | Yes |
| Interface and editor themes | A different theme for the panels than for the page | Yes | Yes |
| Core colours | background, panel, text, muted, border, accent, link, missing link, quote | Yes | Yes |
| Page shadow | none, soft, medium, strong; or colour, opacity, blur, spread, and which side | Yes | Yes (preset) |

### Text

Four text roles: interface title, interface body, editor title, editor body. Interface titles are note titles, section labels and tabs; editor titles are headings. By default the editor matches the interface.

| Setting | Values | Theme | User |
| --- | --- | --- | --- |
| Font, per role | Any bundled or installed font; themes can bundle `.ttf` or `.otf` files | Yes | Yes |
| Colour, per role | Any colour | Yes | Yes |
| Weight, per role | 100 to 900 | Yes | No |
| Text size | Small, medium, large, extra large | Yes | Yes |
| Heading sizes | Each of h1 to h6 on its own: size, weight, colour, space above and below, colour of the `#` | Yes | Presets |
| Text elements | Bold, italic, inline code, quotes and links each on their own | Yes | No |
| Editor layout | Line height, text column width, page padding, paragraph spacing | Yes | No |
| Date formats | strftime strings for the daily heading, previous and next links, sidebar and calendar month | Yes | Yes |

### Editor

| Setting | Values | Theme | User |
| --- | --- | --- | --- |
| Bullet style | dot, circle, dash, arrow, or any single character | Yes | Yes |
| List indent and item spacing | Any length | Yes | No |
| Opening links and tags | Double-click (default), Ctrl+click, single click | No | Yes |

### Tags

| Setting | Values | Theme | User |
| --- | --- | --- | --- |
| Tag style | Pill or coloured text | Yes | Yes |
| Tag colour and background | Any colour | Yes | Yes |
| Per-tag colours | A colour for any tag, matched case-insensitively | Yes | Yes |
| Where tags show on a note | Below the title (default), above it, bottom of the page, not shown | Yes | Yes |
| Tag management | Rename, merge, delete, colour, across every note | No | Yes |

### Sidebar

| Setting | Values | Theme | User |
| --- | --- | --- | --- |
| Layout | Recents, folders, both stacked, both as tabs, two sidebars | No | Yes |
| Stacked order | Recents or folders on top; each section collapses to its header | No | Yes |
| List style | Quiet list or timeline | Yes | Yes |
| Density | Comfortable or compact | Yes | Yes |
| Width and minimum width | Any length | Yes | No |
| Colours | background, text, muted, border, card hover, card active | Yes | Yes |
| Group labels ("Today", "This week", "Earlier") | Simple (default) or with a separator line; colour, size, letter spacing | Yes | No |
| Timeline node shape | Bar (default), circle, half pill, diamond, square | Yes | Yes |
| Recents limit | Last 5, last 10, since yesterday, last 3 days, all | No | Yes |
| Note cards | Show tags, show folder, preview length 0 to 5 lines | Yes | Yes |
| Earlier daily pages in recents | Show or hide | No | Yes |
| Today | Pinned card, calendar button, or both; the card can hide its tags and preview | Yes | Yes |
| Today card style | Date block, week strip, plain card, single line, writing prompt | Yes | Yes |

### Folder column (two-sidebar layout)

| Setting | Values | Theme | User |
| --- | --- | --- | --- |
| Width | Any length | Yes | No |
| Order of entries | Drag Recents, All notes and folders into any order | No | Yes |
| Folder colours | A colour per folder | No | Yes |

### Collapsed sidebars and bars

| Setting | Values | Theme | User |
| --- | --- | --- | --- |
| How the left sidebar collapses | Hidden (focus mode) or an icon rail | No | Yes |
| Rail density | Same as sidebar, comfortable, compact | Yes | Yes |
| Rail labels | Shown or hidden (Today never has a label) | No | Yes |
| Rail Today button | Date in the accent colour, date blended in, or calendar icon | Yes | Yes |
| Top bar | Off (controls in the sidebar and page) or on | No | Yes |
| Panel openers without a top bar | Text buttons or icons | No | Yes |
| Bottom bar density | Same as sidebar, comfortable, compact | Yes | Yes |
| Info panel | Collapses into the bottom bar: word count, links in, reopen | No | Yes (open or closed) |

### Calendar and daily notes

| Setting | Values | Theme | User |
| --- | --- | --- | --- |
| Daily notes | On or off | No | Yes |
| Daily view | One day at a time or a continuous journal | No | Yes |
| Writing levels | Thresholds for levels 2 and 3 (default 50 and 250 words added) | Yes | Yes |
| Marker per level | Shape (dot, square, ring, bar, diamond, star, none, any character), count 1 to 3, size, colour | Yes | No |
| Marker position | Below, above, corner, or behind (fills the day) | Yes | No |
| Day cell per level | Background, number colour, border, roundness | Yes | No |
| Selected day and today | Their own styles, which can also vary by level | Yes | No |
| Dot style shortcut | One to three dots, growing dot, deepening colour | Yes | Yes |

### Behaviour (preferences only)

| Setting | Values |
| --- | --- |
| Keyboard shortcuts | Every app shortcut can be rebound, with clash warnings and reset; editor formatting keys are fixed in v1 |
| Theme browser | On or off (the only feature that uses the network, and only when opened) |
| Built-in modules | Code highlighting, Mermaid diagrams (vim mode later) |
