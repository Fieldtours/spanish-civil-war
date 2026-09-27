# The Spanish Civil War 1936–1939 — design brief

**Family:** DZ Charlie field guides (same layout, screens and components as Easy Company).
**The object:** a *Parte de guerra*, the typed daily war dispatch both armies issued, pinned to a map board.
The cover and headers read **PARTE DE GUERRA · FIELD GUIDE · 1936–1939**.

## Palette (from the period, not from either side's flags)
| Token | Hex | Where it comes from |
|---|---|---|
| `--earth` (dark main) | `#3d2b1f` | burnt-umber earth of Aragon and the Ebro hills; the brown of both armies' field kit |
| `--earth2` | `#5a4030` | lighter umber for raised surfaces |
| `--paper` | `#efe6cf` | aged newsprint and ration-card stock of 1937 |
| `--ink` | `#1f1a14` | typewriter ribbon / printer's ink |
| `--red` (accent) | `#a8321f` | the faded vermilion used on posters of BOTH sides (never used as a flag) |
| `--ochre` | `#c28a2c` | ochre of Castilian fields and poster backgrounds |
| `--rep` (maps only) | `#b03a2e` | Republican forces on maps — the standard historical-map convention |
| `--nat` (maps only) | `#2d4d73` | Nationalist forces on maps — the standard historical-map convention |
| HIGH / MEDIUM / LOW | `#2e7d32` / `#f2c200` / `#c62828` | unchanged across all DZ Charlie guides |

All text/background pairs checked at 4.5:1 or better (ink on paper 14:1, paper on earth 11:1, white on red 6.4:1).

## Fonts (free, OFL, stored offline in fonts/)
- **Big Shoulders Stencil Display 800** — titles. A condensed stencil in the spirit of the lettering stencilled on 1930s crates, trucks and posters; keeps the Easy Company stencil family link.
- **Special Elite** — labels and dispatch headings (the typewriter of the *parte*).
- **Courier Prime** — dates, coordinates, small caps labels.
- System sans — stories and body text, for easy reading outdoors.

## Textures and motifs
- Ruled dispatch paper (faint horizontal lines), a typed header strip, carbon-copy grey rules.
- Rubber stamps: "PARTE DE GUERRA", "VISADO" (approved), region stamps.
- Map style: a 1930s staff map — buff land, blue rivers, dotted provinces, red main roads, stencil place names.
- Icons: simple stroke icons drawn fresh (no party badges, no flags).

## Respect and balance
- No Republican tricolour, no Nationalist red-gold flag, no party symbols (CNT-FAI, Falange yoke-and-arrows, hammer & sickle) as decoration.
- Period posters and photos appear only as captioned historical exhibits, from both sides.
- Memorials, mass-grave and repression sites use quiet styling: no stamps, no red accent, a plain grey rule.

## Cover
Typographic cover over a real photograph (ruins of Belchite), darkened, with the stencil title
**THE SPANISH CIVIL WAR · 1936–1939** and the stamp **PARTE DE GUERRA**. A painted-poster prompt is in `cover-prompt.txt`.
