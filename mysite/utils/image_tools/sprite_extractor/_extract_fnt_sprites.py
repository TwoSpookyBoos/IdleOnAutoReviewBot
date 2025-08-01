import xml.etree.ElementTree as eT
import os
from PIL import Image

from utils.image_tools.sprite_extractor.sprite_extractor_dict import sprite_extractor_dict, FontDefinition


def extract_fnt_sprites(src_dir, target_dir, fnt_filename):
    tree = eT.parse(os.path.join(src_dir, fnt_filename))
    try:
        texture = Image.open(os.path.join(src_dir, fnt_filename.replace('fnt', 'png')))
    except FileNotFoundError:
        return

    font_definition: FontDefinition = sprite_extractor_dict[fnt_filename]
    root = tree.getroot()
    chars = root.find("chars")
    for char in chars.findall("char"):
        char_id = int(char.get("id"))
        try:
            sprite_filename = font_definition[char_id]
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

        sprite_img = texture.crop((x, y, x + width, y + height))

        filepath = os.path.join(target_dir, str(sprite_filename) + ".png")
        sprite_img.save(filepath)
