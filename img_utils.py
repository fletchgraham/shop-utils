from pathlib import Path
from PIL import Image

def crop_resize(src: Path, dst: Path, new_width: int, new_height: int, quality=95):

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

        converted = resized_img.convert("RGB")

        converted.save(dst, quality=quality, optimize=True)


def resize_image(input_path, output_path, quality=85, base_width=800):
    """
    Resize the image, maintaining its aspect ratio.
    :param input_path: Path to the input image.
    :param output_path: Path to save the output image.
    :param base_width: Desired width of the output image.
    """
    # Open an image file
    with Image.open(input_path) as img:
        img = img.convert("RGB")
        # Calculate aspect ratio
        w_percent = base_width / img.size[0]
        h_size = int(img.size[1] * w_percent)
        
        # Resize image
        img = img.resize((base_width, h_size))
        
        # Save image with optimization
        img.save(output_path, "JPEG", quality=quality, optimize=True, progressive=True)


def optimize_images_in_directory(directory: Path, base_width=800):
    """
    Optimize all images in a directory.
    :param directory: Directory containing the images to be optimized.
    :param base_width: Desired width of the output images.
    """
    directory = Path(directory)
    for filename in directory.iterdir():
        if filename.suffix in [".jpg", ".png"]:
            output_path = directory / f"lo_{filename.name}"
            print(f"resizing to {base_width}")
            resize_image(filename, output_path, quality=80, base_width=base_width)