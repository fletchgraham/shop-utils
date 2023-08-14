import sys
from pathlib import Path
import bpy

tree = bpy.context.scene.node_tree
art_file = Path(sys.argv[6])
img = bpy.data.images.load(art_file.as_posix())
art_node = tree.nodes["ART_FILE"]
art_node.image = img

# Set the render settings
bpy.context.scene.render.image_settings.file_format = 'JPEG'

art_name = art_file.stem
mockup_name = Path(bpy.data.filepath).stem
out_name = f"{'_'.join(art_name.split('_')[:-1])}_{mockup_name.replace('mockup_', '')}"
bpy.context.scene.render.filepath = (art_file.parent / "mockups" / out_name).as_posix()

# Render the scene
bpy.ops.render.render(write_still=True)

