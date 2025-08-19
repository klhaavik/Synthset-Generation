import bpy
import mathutils
import numpy as np
import random

gsd = 3 # m/px
focal_len = 0.7 # m
sensor_width = 5.5 * 10 ** -6 * 8800 # m - width/pixel * num pixels
height = 525000 # m
clip_start = 10000 # m
clip_end = height + 1000000 # m

city = bpy.context.scene["city"]

terrain = bpy.data.objects[f"{city}_terrain_0"]
img_coverage_w = terrain.dimensions[0] # m
img_coverage_h = terrain.dimensions[2] # m

max_coverage = max(img_coverage_w, img_coverage_h)

fudge_factor = max_coverage / (height * sensor_width / focal_len)
focal_len /= fudge_factor

cam_res_w = max_coverage // gsd
cam_res_h = max_coverage // gsd

cam_pivot = bpy.data.objects["cam_pivot"]
cam_obj = bpy.data.objects["Camera"]
cam = cam_obj.data
cam.lens = focal_len * 10 ** 3 
cam.sensor_width = sensor_width * 10 ** 3
cam_obj.location.z = height
cam_obj.rotation_euler = mathutils.Euler((0, 0, 0), 'XYZ')
cam.clip_start = clip_start
cam.clip_end = clip_end

sun = bpy.data.objects["Light"].data
sun.angle = np.deg2rad(0.526)

bpy.context.scene.render.resolution_x = int(cam_res_w)
bpy.context.scene.render.resolution_y = int(cam_res_h)

def collection_toggle_hide_render(collection, hide_render):
    for obj in collection.objects:
        obj.hide_render = hide_render

cam_standard_angle_deviation = 5 # degrees

min_day_of_year = 1
max_day_of_year = 365

min_time_of_day = 8.0
max_time_of_day = 16.0

render_engine = "Eevee" if bpy.context.scene.render.engine == 'BLENDER_EEVEE_NEXT' else "CYCLES"

#Example paths, adjust as needed
color_path = f"C:\\Users\\bachc\\Documents\\GitHub\\Synthset-Generation\\Blender\\{city}\\Images\\{render_engine}\\Color\\"
sem_seg_path = f"C:\\Users\\bachc\\Documents\\GitHub\\Synthset-Generation\\Blender\\{city}\\Images\\{render_engine}\\Sem_seg\\"

ogs = bpy.data.collections["Collection"]
dupes = bpy.data.collections["Dupes"]

if bpy.data.objects.find("Clouds") != -1:
    cloud_mat = bpy.data.materials["Clouds.002"]
    cloud_opacity = cloud_mat.node_tree.nodes["Mix Shader.001"].inputs[0]
    cloud_size = cloud_mat.node_tree.nodes["Noise Texture"].inputs[2]
    using_clouds = True
else:
    using_clouds = False

min_cloud_size = 4
max_cloud_size = 14
max_cloud_opacity = 0.4

if bpy.data.worlds["World"].node_tree.nodes.find("Sky Texture") != -1:
    sky_tex = bpy.data.worlds["World"].node_tree.nodes["Sky Texture"]

if sky_tex and sky_tex.outputs[0].is_linked:
    using_sky_tex = True
    using_bg = False
elif bpy.context.scene.sun_pos_properties.sun_object != None:
    using_bg = False
    using_sky_tex = False
else:
    using_bg = True
    using_sky_tex = False
    bg = bpy.data.worlds["World"].node_tree.nodes["Background"]
    scene_brightness = bg.inputs[1]
    
min_scene_brightness = 0.2
max_scene_brightness = 1

min_sun_elevation_angle = 23 # degrees
sun_rotation_deviation = 40 # degrees

for i in range(0, 20):
    cam_pivot.rotation_euler = mathutils.Euler((0, 0, 0), 'XYZ')
    cam_pivot.scale = mathutils.Vector((1, 1, 1))
    
    if using_bg:
        scene_brightness.default_value = random.uniform(min_scene_brightness, max_scene_brightness)
    elif using_sky_tex:
        sky_tex.sun_intensity = random.uniform(0.2, 0.8)
    else:
        sun.energy = random.uniform(2.0, 10.0)
    
    bpy.context.scene.sun_pos_properties.day_of_year = random.randrange(50, 300)
    bpy.context.scene.sun_pos_properties.time_of_day = random.uniform(8.0, 16.0)
    
    angle_x = random.gauss(0, np.deg2rad(cam_standard_angle_deviation))
    angle_y = random.gauss(0, np.deg2rad(cam_standard_angle_deviation))
    cam_pivot.rotation_euler = mathutils.Euler((angle_x, angle_y, 0), 'XYZ')
    size_factor = angle_x**2 + angle_y**2
    cam_pivot.scale = mathutils.Vector((1 - size_factor, 1 - size_factor, 1 - size_factor))

    if using_clouds:
        cloud_opacity.default_value = 1 - random.uniform(0, max_cloud_opacity)
        cloud_size.default_value = random.uniform(min_cloud_size, max_cloud_size)
    
    collection_toggle_hide_render(ogs, False)
    collection_toggle_hide_render(dupes, True)
    bpy.context.scene.render.filepath = color_path + f"render{i}.png"
    bpy.ops.render.render(write_still=True)
    
    collection_toggle_hide_render(ogs, True)
    collection_toggle_hide_render(dupes, False)
    bpy.context.scene.render.filepath = sem_seg_path + f"render{i}.png"
    bpy.ops.render.render(write_still=True)
