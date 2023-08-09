from pathlib import Path
import sys

import bpy

RATIOS = {
    "2x3": (7275, 10875),
    "3x4": (5475, 7275),
    "4x5": (4875, 6075),
    "11x14": (3375, 4275),
    "Asizes": (7091, 10008),
}

percentage = int(sys.argv[6])


blend_path = Path(bpy.data.filepath)
blend_name = blend_path.stem

scene = bpy.context.scene

for ratio, dims in RATIOS.items():

    scene.render.resolution_x = dims[0]
    scene.render.resolution_y = dims[1]
    scene.render.resolution_percentage = percentage

    bpy.context.scene.render.image_settings.file_format = 'JPEG'
    bpy.context.scene.render.image_settings.quality = 80

    img_name = f"{blend_name}_{ratio}"
    scene.render.filepath = (blend_path.parent / blend_name / img_name).as_posix()

    bpy.ops.render.render(write_still=True)
