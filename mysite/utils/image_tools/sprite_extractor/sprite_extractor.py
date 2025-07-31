from PIL import Image
import os
import xml.etree.ElementTree as eT

from utils.image_tools.sprite_extractor.sprite_extractor_dict import sprite_extractor_dict

src_dir = "../../../static/imgs/1x"
target_dir = "../../../static/imgs/extracted_sprites"


def find_fnt_files():
    return [f for f in os.listdir(src_dir) if f.endswith("fnt")]


for fnt in find_fnt_files():
    try:
        sprite_extractor_dict[fnt]
    except KeyError:
        print(f'Skipping {fnt}, no sprites defined')
        continue
    tree = eT.parse(os.path.join(src_dir, fnt))
    try:
        texture = Image.open(os.path.join(src_dir, fnt.replace('fnt', 'png')))
    except FileNotFoundError:
        continue

    root = tree.getroot()

    chars = root.find("chars")

    for char in chars.findall("char"):
        char_id = int(char.get("id"))
        sprite_filename = ''
        try:
            sprite_filename = sprite_extractor_dict[fnt][char_id]
        except KeyError:
            continue
        if sprite_filename == '':
            continue
        x = int(char.get("x"))
        y = int(char.get("y"))
        width = int(char.get("width"))
        height = int(char.get("height"))
        if width == 0 or height == 0:
            continue

        glyph_img = texture.crop((x, y, x + width, y + height))

        filepath = os.path.join(target_dir, str(sprite_filename) + ".png")
        glyph_img.save(filepath)
        print(f"Saved sprite for id {char_id} as '{sprite_filename}.png'")
