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

art_name = art_file.stem.replace("_", "-")
mockup_name = Path(bpy.data.filepath).stem
bpy.context.scene.render.filepath = (art_file.parent / "mockups" / f"{mockup_name}-{art_name}").as_posix()

# Render the scene
bpy.ops.render.render(write_still=True)

