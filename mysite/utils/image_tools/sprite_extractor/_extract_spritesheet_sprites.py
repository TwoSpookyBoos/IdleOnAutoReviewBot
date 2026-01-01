import os

from PIL import Image

from utils.image_tools.sprite_extractor.sprite_extractor_dict import sprite_extractor_dict, SpritesheetDefinition


def extract_spritesheet_sprites(src_dir, target_dir, spritesheet_filename):
    spritesheet = Image.open(os.path.join(src_dir, spritesheet_filename))
    spritesheet_definition: SpritesheetDefinition = sprite_extractor_dict[spritesheet_filename]

    images = get_images(spritesheet, spritesheet_definition)
    if spritesheet_definition.get("as_gif", False):
        save_as_gif(images, spritesheet_definition, target_dir)
        return

    for index, image in enumerate(images):
        sprite_filename = spritesheet_definition["base_file_name"] + str(index) + ".png"
        filepath = os.path.join(target_dir, sprite_filename)
        image.save(filepath)


def get_images(spritesheet, spritesheet_definition):
    sprite_width = spritesheet.width / spritesheet_definition["columns"]
    sprite_height = spritesheet.height / spritesheet_definition["rows"]

    images = []
    for row in range(spritesheet_definition["rows"]):
        for col in range(spritesheet_definition["columns"]):
            if row * spritesheet_definition["columns"] + col >= spritesheet_definition["num_sprites"]:
                break
            sprite = spritesheet.crop((col * sprite_width, row * sprite_height, (col + 1) * sprite_width, (row + 1) * sprite_height))
            images.append(sprite)
    return images


def save_as_gif(frames, spritesheet_definition, target_dir):
    gif_filename = spritesheet_definition["base_file_name"] + '.gif'
    frames[0].save(
        os.path.join(target_dir, gif_filename),
        save_all=True,
        append_images=frames[1:],
        disposal=2,
        duration=100,
        loop=0
    )
