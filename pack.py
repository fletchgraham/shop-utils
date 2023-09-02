import bpy

try:
    bpy.ops.file.pack_all()
except RuntimeError:
    print('error on packing')


bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
