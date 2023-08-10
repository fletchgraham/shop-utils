from pathlib import Path
from PIL import Image

def resize(src: Path, dst: Path, new_width: int, new_height: int):

    print(f"resizing {src}")

    with Image.open(src) as img:

        cur_aspect = img.width / img.height
        new_aspect = new_width / new_height

        if new_aspect < cur_aspect:  # new image is skinnier
            left = (img.width - new_aspect * img.height) // 2
            right = int(left + new_aspect * img.height)
            upper = 0
            lower = img.height
        else:  # new image is wider
            left = 0
            right = img.width
            upper = (img.height - (img.width / new_aspect)) // 2
            lower = int(upper + img.width / new_aspect)

        cropped_img = img.crop((left, upper, right, lower))
        resized_img = cropped_img.resize((new_width, new_height))

        resized_img.save(dst)