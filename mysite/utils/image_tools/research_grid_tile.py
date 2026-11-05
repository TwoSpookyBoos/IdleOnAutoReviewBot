"""usage: python research_grid_tile.py <IdleOnAssets/1x/font-746.fnt> <dir> <Label>...

Builds Research Grid square images for two-character labels (e.g. "E4") from font 746:
the tile glyph "[" with the letter and digit glyphs drawn on top. Writes
`<dir>/ResearchGrid<Label>.png`; the squares live in `static/imgs/w7/research/`.

Placement reproduces all existing two-character squares pixel for pixel: glyphs sit 6px
from the top; the letter at x=10 (x=8 for the wide M/O), the digit at x=30 (x=32 after a
wide letter, and for "3"). Three-character labels (H10...) were laid out by hand
differently and aren't supported.
"""

import re
import sys
from pathlib import Path

from PIL import Image

TILE_CHAR = "["
GLYPH_Y = 6
WIDE_LETTER_WIDTH = 26


def load_glyphs(fnt_path: Path) -> dict[str, Image.Image]:
    fnt = fnt_path.read_text(encoding="utf-8")
    atlas = Image.open(fnt_path.with_suffix(".png")).convert("RGBA")
    glyphs = {}
    for match in re.finditer(r"<char [^>]*>", fnt):
        attrs = dict(re.findall(r'(\w+)="([^"]*)"', match.group(0)))
        x, y, w, h = (int(attrs[key]) for key in ("x", "y", "width", "height"))
        glyphs[chr(int(attrs["id"]))] = atlas.crop((x, y, x + w, y + h))
    return glyphs


def build(glyphs: dict[str, Image.Image], label: str) -> Image.Image:
    if len(label) != 2:
        raise ValueError(f"only two-character labels are supported: {label!r}")
    letter, digit = glyphs[label[0]], glyphs[label[1]]
    wide = letter.width >= WIDE_LETTER_WIDTH
    tile = glyphs[TILE_CHAR].copy()
    tile.alpha_composite(letter, (8 if wide else 10, GLYPH_Y))
    tile.alpha_composite(digit, (32 if wide or label[1] == "3" else 30, GLYPH_Y))
    return tile


def main():
    fnt_path, out_dir, *labels = sys.argv[1:]
    glyphs = load_glyphs(Path(fnt_path))
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for label in labels:
        path = out_dir / f"ResearchGrid{label}.png"
        build(glyphs, label).save(path)
        print(f"{label} -> {path}")


if __name__ == "__main__":
    main()
