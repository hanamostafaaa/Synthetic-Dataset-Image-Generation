import bpy
import os
import random
import math
from bpy_extras.object_utils import world_to_camera_view

OUTPUT_DIR = r"C:\Users\hanam\OneDrive\Desktop\randomimages"
IMAGES_DIR = os.path.join(OUTPUT_DIR, "images")
LABELS_DIR = os.path.join(OUTPUT_DIR, "labels")
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(LABELS_DIR, exist_ok=True)

scene = bpy.context.scene
obj = bpy.data.objects["TargetObject"]
camera = bpy.data.objects["Camera"]
ground_z = obj.location.z

meshes = [o for o in [obj] + list(obj.children_recursive) if o.type == 'MESH']

obj.rotation_mode = 'XYZ'

for i in range(50):
    obj.location = (random.uniform(-7.0, 7.0), random.uniform(-7.0, 7.0), ground_z)
    obj.rotation_euler.z = random.uniform(0, 2 * math.pi)
    bpy.context.view_layer.update()

    coords = [
        world_to_camera_view(scene, camera, m.matrix_world @ v.co)
        for m in meshes
        for v in m.data.vertices
    ]
    xs = [c.x for c in coords]
    ys = [1.0 - c.y for c in coords]
    min_x, max_x = max(0.0, min(xs)), min(1.0, max(xs))
    min_y, max_y = max(0.0, min(ys)), min(1.0, max(ys))
    w = max_x - min_x
    h = max_y - min_y
    x_c = min_x + (w / 2.0)
    y_c = min_y + (h / 2.0)

    scene.render.filepath = os.path.join(IMAGES_DIR, f"img_{i:03d}.png")
    bpy.ops.render.render(write_still=True)

    with open(os.path.join(LABELS_DIR, f"img_{i:03d}.txt"), "w") as f:
        f.write(f"0 {x_c:.6f} {y_c:.6f} {w:.6f} {h:.6f}\n")
print("Done!")