from pathlib import Path
from PIL import Image

MOCKUP_CROPS = {
    "black_frame_mat_next_to_olive_branch": (288, 0, 4608, 3456),
    "blond_haired_asian_woman_reading_magazine": (527, 0, 6154, 4615),
    "blonde_woman_hanging_black_frame": (64, 0, 3826, 2870),
    "young_man_hanging_frame_white_minimal_wall": (-1406, 402, 7481, 5611),
    "wood_frame_twig_close": (278, 0, 4444, 3333),
    "wood_frame_sheer_curtains_credenza_zoom": (0, 229, 3080, 2310),
    "wood_frame_close_with_grasses": (-450, 0, 4400, 3300),
    "wood_frame_behind_cream_armchairs": (0, 498, 4000, 3000),
    "warp_reflection_olive_paneled_door": (77, 158, 2952, 2214),
    "picture_frame_parquet_floor": (-766, 2345, 6206, 4654),
    "mint_plaster_wall_with_credenza": (68, 0, 2591, 1944),
    "leaning_wood_frame_wood_floor_still_life": (-743, 2124, 6159, 4619),
    "headon_wood_frame_grasses_in_vase": (90, 142, 2704, 2028),
    "green_office": (0, 227, 2700, 2025),
    "green_office_leaning_zoom": (0, 347, 2700, 2025),
    "boho_sofa_with_arches": (0, 245, 2645, 1984),
}


def expand_image(image, x, y, width, height):
    """Expand the canvas of the image based on negative x and y values."""
    img_width, img_height = image.size
    
    # Calculate new dimensions considering the negative values and desired dimensions
    new_width = width + abs(x) if x < 0 else img_width
    new_height = height + abs(y) if y < 0 else img_height

    # Create a new image with the calculated dimensions
    expanded_image = Image.new("RGB", (new_width, new_height), color=(230, 230, 230))
    
    # Determine where to paste the original image in the expanded image
    paste_x = abs(x) if x < 0 else 0
    paste_y = abs(y) if y < 0 else 0
    
    expanded_image.paste(image, (paste_x, paste_y))
    
    return expanded_image


def resize_for_web(image):
    """Resize the image for 4x3 aspect ratio with a short side of 2600 pixels."""
    return image.resize((3467, 2600))

def crop_or_expand_image(input_path, output_path, coords):
    """Crop or expand the image based on the coordinates, then resize for web."""
    with Image.open(input_path) as img:
        x, y, width, height = coords
        
        if x < 0 or y < 0:
            img = expand_image(img, x, y, width, height)
            left = max(0, x)
            upper = max(0, y)
        else:
            left, upper = x, y
        
        right = left + width
        lower = upper + height
        
        cropped_image = img.crop((left, upper, right, lower))
        web_optimized_image = resize_for_web(cropped_image)
        web_optimized_image.save(output_path, "JPEG", quality=85)  # You can adjust the quality for further optimization


def crop_mockup(mockup: Path):
    coords = _get_coords(mockup)
    output_path = mockup.with_name("cropped_" + mockup.name)
    crop_or_expand_image(mockup, output_path, coords)
    print(f"Processed {mockup} to {output_path}")


def _get_coords(mockup: Path):
    for k, v in MOCKUP_CROPS.items():
        if k in mockup.name:
            return v