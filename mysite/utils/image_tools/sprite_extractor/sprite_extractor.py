import os

from utils.image_tools.sprite_extractor._extract_fnt_sprites import extract_fnt_sprites
from utils.image_tools.sprite_extractor._extract_spritesheet_sprites import extract_spritesheet_sprites
from utils.image_tools.sprite_extractor.sprite_extractor_dict import sprite_extractor_dict

src_dir = "../../../static/imgs/1x"
target_dir = "../../../static/imgs/extracted_sprites"

font_files = []
sprite_files = []
defined_files = set(sprite_extractor_dict.keys())
for f in os.listdir(src_dir):
    if f not in defined_files:
        continue
    if f.endswith(".fnt"):
        extract_fnt_sprites(src_dir, target_dir, f)
    if f.endswith(".png"):
        extract_spritesheet_sprites(src_dir, target_dir, f)
