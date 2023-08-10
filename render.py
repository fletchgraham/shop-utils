from pathlib import Path
import sys

import bpy


percentage = int(sys.argv[6])

blend_path = Path(bpy.data.filepath)
blend_name = blend_path.stem

scene = bpy.context.scene

scene.render.resolution_x = 7275
scene.render.resolution_y = 10875
scene.render.resolution_percentage = percentage

bpy.context.scene.render.image_settings.file_format = 'PNG'

img_name = f"{blend_name}_src"
scene.render.filepath = (blend_path.parent / blend_name / img_name).as_posix()

bpy.ops.render.render(write_still=True)
