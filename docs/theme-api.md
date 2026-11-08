# Theme API reference

How to build a theme for Notebook. A theme is data only: one TOML file, or a folder with that file and its fonts. It never contains code, and it may not point at anything on the network.

Status: planned v1 format. Key names may still change before the first release; this page will be updated when they do.

## Contents

1. [File layout](#file-layout)
2. [How values resolve](#how-values-resolve)
3. [Value types](#value-types)
4. [Top level and `[meta]`](#top-level-and-meta)
5. [`[colours]`](#colours)
6. [`[fonts]` and bundled font files](#fonts-and-bundled-font-files)
7. [`[text.*]`: the four text roles](#text-the-four-text-roles)
8. [`[editor]`](#editor)
9. [`[heading.h1]` to `[heading.h6]`](#headingh1-to-headingh6)
10. [`[style.*]`: inline text elements](#style-inline-text-elements)
11. [`[list]`](#list)
12. [`[tag]` and `[tag.colours]`](#tag-and-tagcolours)
13. [`[sidebar]`](#sidebar)
14. [`[folders]`](#folders)
15. [`[rail]`](#rail)
16. [`[info-panel]`](#info-panel)
17. [`[status-bar]`](#status-bar)
18. [`[shadow]`](#shadow)
19. [`[calendar]`](#calendar)
20. [`[daily]`](#daily)
21. [Validation rules](#validation-rules)
22. [A complete example](#a-complete-example)

## File layout

A theme without fonts is a single file:

```
themes/paper.toml
```

A theme with fonts is a folder:

```
themes/literary/
  theme.toml
  fonts/Literata-Regular.ttf
  fonts/OFL.txt
```

The folder name, or the file name without `.toml`, must equal `[meta] id`.

## How values resolve

For every setting the app uses the first of these that is set:

1. The person's preference.
2. The active theme.
3. The built-in values for the theme's `base` (light or dark).

Every key below is optional except `base` and `[meta]`. A theme can be three lines of colours; everything else comes from `base`. People can always override a theme in Settings and reset back to it; see "What can be customised" in the README for which settings people can change.

## Value types

| Type | Format | Examples |
| --- | --- | --- |
| colour | `#rrggbb` | `"#3b6ea8"` |
| length | A number with `px` or `em` | `"16px"`, `"1.4em"` |
| number | A plain number | `1.6`, `400` |
| font | A family name: bundled in this theme, bundled with the app, or installed | `"Literata"` |
| weight | 100 to 900 | `500` |
| boolean | `true` or `false` | `true` |
| enum | One of the listed words | `"pill"` |
| strftime | A date format string | `"%A, %B %-d"` |

Unknown keys are ignored and reported as warnings, so a theme written for a newer app still loads in an older one.

## Top level and `[meta]`

| Key | Type | Required | Description |
| --- | --- | --- | --- |
| `base` | `light` or `dark` | Yes | Built-in values to start from. Must come before any table. |
| `[meta] id` | text | Yes | Lower case, matches the file or folder name. |
| `[meta] name` | text | Yes | Shown in the theme picker. |
| `[meta] version` | `1.2.3` | Yes | Newer versions replace older ones on install. |
| `[meta] description` | text | Yes | One sentence for the picker. |
| `[meta] author` | text | Yes | Your name or handle. |
| `[meta] licence` | text | Yes | MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC or CC0-1.0. |
| `[meta] min-app-version` | `1.2.3` | Yes | Oldest app version the theme works with. |

## `[colours]`

The palette every other table falls back to.

| Key | Type | Used for |
| --- | --- | --- |
| `background` | colour | The page |
| `panel` | colour | Sidebars and bars |
| `text` | colour | Default text (use a soft near-black or near-white, not pure black or white) |
| `muted` | colour | Secondary text: times, counts, previews |
| `border` | colour | Lines and separators |
| `accent` | colour | Selection, active items, the Today tile |
| `link` | colour | Links to notes that exist |
| `link-missing` | colour | Links to notes not created yet |
| `quote` | colour | Block quotes |
| `hover` | colour | Hovered rows and buttons |
| `active` | colour | The selected row |

## `[fonts]` and bundled font files

| Key | Type | Description |
| --- | --- | --- |
| `interface` | font | Default for the two interface text roles |
| `note` | font | Default for the two editor text roles |
| `code` | font | Inline code and code blocks |

Bundled fonts are listed in `[[fonts.files]]`, one entry per file:

| Key | Type | Required | Description |
| --- | --- | --- | --- |
| `file` | path | Yes | Inside the theme folder, for example `fonts/Literata-Regular.ttf` |
| `family` | text | Yes | The name other keys use |
| `weight` | weight or range | No | `400`, or `"200 900"` for a variable font |
| `style` | `normal` or `italic` | No | Defaults to `normal` |
| `licence` | `OFL-1.1`, `MIT` or `Apache-2.0` | Yes | |
| `licence-file` | path | Yes | The licence text, inside the theme folder |

Fonts must be `.ttf` or `.otf`, at most 5 MB each, shipped exactly as published (never subset, converted or edited). A theme is at most 20 MB in total. The app registers the fonts for itself only; they are never installed on the system.

## `[text.*]`: the four text roles

`[text.interface-title]`, `[text.interface-body]`, `[text.editor-title]`, `[text.editor-body]`. Interface titles are note titles, section labels and tabs; editor titles are headings. By default the editor uses the interface's values.

| Key | Type | Description |
| --- | --- | --- |
| `font` | font | |
| `colour` | colour | |
| `weight` | weight | Themes only; people cannot change weight |

## `[editor]`

| Key | Type | Default | Description |
| --- | --- | --- | --- |
| `font-size` | length | `16px` | Body text size |
| `line-height` | number | `1.65` | |
| `max-width` | length | `760px` | Width of the text column |
| `padding` | length, one to four values | `28px 32px` | Space around the page |
| `paragraph-spacing` | length | `0.6em` | Space between paragraphs |

## `[heading.h1]` to `[heading.h6]`

Each level has its own table.

| Key | Type | Description |
| --- | --- | --- |
| `font-size` | length | |
| `font-weight` | weight | |
| `colour` | colour | |
| `margin-top` | length | Space above the heading |
| `margin-bottom` | length | Space between the heading and the text under it |
| `marker-colour` | colour | The visible `#` characters |

## `[style.*]`: inline text elements

`[style.bold]`, `[style.italic]`, `[style.code]`, `[style.quote]`, `[style.link]`.

| Key | Type | Applies to |
| --- | --- | --- |
| `font-weight` | weight | bold |
| `font-style` | `normal` or `italic` | italic |
| `font-family` | font | code |
| `background` | colour | code |
| `colour` | colour | all |
| `border-left` | length and colour, for example `"3px solid #e2ded7"` | quote |
| `missing-colour` | colour | link |

## `[list]`

| Key | Type | Description |
| --- | --- | --- |
| `bullet` | `dot`, `circle`, `dash`, `arrow`, or any single character | The `-` stays in the file; this is how it is drawn |
| `indent` | length | |
| `item-spacing` | length | |

## `[tag]` and `[tag.colours]`

| Key | Type | Description |
| --- | --- | --- |
| `style` | `pill` or `text` | |
| `colour` | colour | |
| `background` | colour | Used by `pill` |
| `placement` | `below-title`, `above-title`, `bottom`, `hidden` | Where a note's tags show |

`[tag.colours]` gives individual tags their own colour, matched case-insensitively:

```toml
[tag.colours]
ideas = "#c0392b"
"project/notebook" = "#2e7d5b"
```

## `[sidebar]`

| Key | Type | Description |
| --- | --- | --- |
| `width` | length | Comfortable width (default 340px) |
| `compact-width` | length | Compact width (default 290px) |
| `min-width` | length | Narrowest it shrinks to in small windows |
| `density` | `comfortable` or `compact` | |
| `list-style` | `quiet` or `timeline` | |
| `timeline-node` | `bar`, `circle`, `half-pill`, `diamond`, `square` | Compact timeline marker |
| `background`, `text`, `muted`, `border` | colour | |
| `card-hover`, `card-active` | colour | Note rows |
| `card-tags` | boolean | Show tags on note cards |
| `card-folder` | boolean | Show the folder on note cards |
| `card-preview-lines` | 0 to 5 | |
| `group-label` | colour | "Today", "This week", "Earlier" |
| `group-label-style` | `simple` or `ruled` | `ruled` adds a line on each side |
| `group-label-size` | length | |
| `group-label-spacing` | length | Letter spacing |
| `today-style` | `date`, `week`, `card`, `line`, `prompt` | The Today card |

## `[folders]`

| Key | Type | Description |
| --- | --- | --- |
| `width` | length | Folder column in the two-sidebar layout |
| `compact-width` | length | |
| `background` | colour | Usually a little darker than `panel`, so the note list reads as layered on top |

## `[rail]`

The collapsed left sidebar, when shown as an icon rail.

| Key | Type | Description |
| --- | --- | --- |
| `density` | `comfortable` or `compact` | Comfortable 52px, compact 30px |
| `today` | `date`, `date-blend`, `icon` | The Today button: date in the accent colour, date blended in, or a calendar icon |
| `background` | colour | |

## `[info-panel]`

| Key | Type | Description |
| --- | --- | --- |
| `width`, `min-width` | length | |
| `background`, `text`, `muted` | colour | |
| `heading` | colour | Section labels such as "Tags" |

## `[status-bar]`

| Key | Type | Description |
| --- | --- | --- |
| `density` | `comfortable` or `compact` | 30px or 22px tall |
| `background`, `text` | colour | |

## `[shadow]`

How far the page lifts off the side panels.

| Key | Type | Description |
| --- | --- | --- |
| `preset` | `none`, `soft`, `medium`, `strong` | The keys below override it |
| `colour` | colour | |
| `opacity` | number, 0 to 1 | |
| `blur` | length | |
| `spread` | length | |
| `left`, `right` | boolean | Which panels the shadow falls on |

## `[calendar]`

Days are grouped into four levels by the words added that day: level 0 is nothing, then one level below each threshold and one above the last.

| Key | Type | Description |
| --- | --- | --- |
| `thresholds` | two numbers | Words added that start levels 2 and 3. Default `[50, 250]` |
| `marker` | `dot`, `square`, `ring`, `bar`, `diamond`, `star`, `none`, or any single character | Default shape |
| `marker-position` | `below`, `above`, `corner`, `behind` | `behind` fills the whole day |
| `dot-style` | `count`, `size`, `shade` | A shortcut for common looks |

`[calendar.level.0]` to `[calendar.level.3]`, `[calendar.selected]`, `[calendar.selected.level.N]` and `[calendar.today]` each accept:

| Key | Type | Description |
| --- | --- | --- |
| `marker` | as above | Change the shape for this level |
| `marker-count` | 1 to 3 | Markers side by side |
| `marker-size` | length | |
| `marker-colour` | colour | |
| `cell-background` | colour | Colour the whole day |
| `cell-text` | colour | The day number |
| `cell-border` | length and colour | |
| `cell-radius` | length or `50%` | |

Examples:

| Look | Settings |
| --- | --- |
| One dot that grows with the day's writing | `marker-count = 1` on every level, `marker-size` rising from level 1 to 3 |
| Colours by amount | a different `marker-colour` per level |
| A heat map | `marker-position = "behind"`, then `cell-background` and `cell-text` per level |
| Stars on big days | `[calendar.level.3] marker = "star"` |
| Selected day styled by its level | `[calendar.selected.level.3] cell-background = "#2e7d5b"` |

## `[daily]`

Date formats are strftime strings. Supported codes: `%A` `%a` `%B` `%b` `%d` `%-d` `%e` `%m` `%-m` `%Y` `%y` `%j` `%%`.

| Key | Default | Example output |
| --- | --- | --- |
| `heading-format` | `%A, %B %-d, %Y` | Monday, November 9, 2026 |
| `nav-format` | `%A` | Sunday |
| `sidebar-format` | `%A, %B %-d` | Monday, November 9 |
| `calendar-month-format` | `%B %Y` | November 2026 |

## Validation rules

`scripts/build_index.py` checks every theme in a pull request. A theme fails if:

- `base` is missing or not `light` or `dark`.
- A required `[meta]` key is missing, the id does not match the file or folder name, or a version is not `1.2.3`.
- The licence is not one of the allowed licences.
- A key under `[colours]` is not `#rrggbb`.
- Any value points at the network (`http:`, `https:`, `ftp:` or `url(`).
- A font is not `.ttf` or `.otf`, is over 5 MB, does not open cleanly, has a licence other than OFL-1.1, MIT or Apache-2.0, or is missing its licence file.
- A path leaves the theme folder, or the theme is over 20 MB.
- `index.json` is out of date (run `python3 scripts/build_index.py` and commit the result).

## A complete example

```toml
base = "light"

[meta]
id = "literary"
name = "Literary"
version = "1.0.0"
description = "Warm paper, a bookish serif for titles and calm sans serif text."
author = "Your name"
licence = "MIT"
min-app-version = "0.1.0"

[colours]
background = "#fbfaf8"
panel = "#f2f0ec"
text = "#3b3733"
muted = "#8a857d"
border = "#e2ded7"
accent = "#3b6ea8"

[fonts]
interface = "Figtree"
note = "Figtree"

[[fonts.files]]
file = "fonts/Literata-Variable.ttf"
family = "Literata"
weight = "200 900"
licence = "OFL-1.1"
licence-file = "fonts/OFL.txt"

[text.interface-title]
font = "Literata"
weight = 500

[text.editor-title]
font = "Literata"
weight = 600

[heading.h1]
font-size = "1.75em"
margin-bottom = "0.4em"

[sidebar]
list-style = "timeline"
timeline-node = "bar"
group-label-style = "simple"

[calendar]
thresholds = [50, 250]

[calendar.level.3]
marker = "star"
marker-colour = "#6b4fa0"

[daily]
heading-format = "%A, %B %-d"
```
