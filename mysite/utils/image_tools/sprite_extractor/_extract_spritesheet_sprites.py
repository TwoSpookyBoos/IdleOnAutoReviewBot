import os

from PIL import Image

from utils.image_tools.sprite_extractor.sprite_extractor_dict import sprite_extractor_dict, SpritesheetDefinition


def extract_spritesheet_sprites(src_dir, target_dir, spritesheet_filename):
    spritesheet = Image.open(os.path.join(src_dir, spritesheet_filename))
    spritesheet_definition: SpritesheetDefinition = sprite_extractor_dict[spritesheet_filename]

    sprite_width = spritesheet.width / spritesheet_definition["columns"]
    sprite_height = spritesheet.height / spritesheet_definition["rows"]

    for row in range(spritesheet_definition["rows"]):
        for col in range(spritesheet_definition["columns"]):
            if row * spritesheet_definition["columns"] + col >= spritesheet_definition["num_sprites"]:
                break
            sprite = spritesheet.crop((col * sprite_width, row * sprite_height, (col + 1) * sprite_width, (row + 1) * sprite_height))
            sprite_filename = spritesheet_definition["base_file_name"] + str(row * spritesheet_definition["columns"] + col) + ".png"
            filepath = os.path.join(target_dir, sprite_filename)
            sprite.save(filepath)
