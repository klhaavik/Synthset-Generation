import bpy
import mathutils
import numpy as np
import random
#import convert_materials

gsd = 3 # m/px
focal_len = 0.7 # m
sensor_width = 5.5 * 10 ** -6 * 8800 # m - width/pixel * num pixels
height = 525000 # m
clip_start = 10000 # m
clip_end = height + 1000000 # m


#cam_res_w = 3333 # px
#cam_res_h = 3333 # px
terrain_name = "london_terrain_0"
terrain = bpy.data.objects[terrain_name]
img_coverage_w = terrain.dimensions[0] # m
img_coverage_h = terrain.dimensions[2] # m

max_coverage = max(img_coverage_w, img_coverage_h)

fudge_factor = max_coverage / (height * sensor_width / focal_len)
focal_len /= fudge_factor

cam_res_w = max_coverage // gsd
cam_res_h = max_coverage // gsd

#cam_coverage_w = cam_res_w * gsd
#cam_coverage_h = cam_res_h * gsd

cam_pivot = bpy.data.objects["cam_pivot"]
cam_obj = bpy.data.objects["Camera"]
cam = cam_obj.data
cam.lens = focal_len * 10 ** 3 
cam.sensor_width = sensor_width * 10 ** 3
cam_obj.location.z = height
cam.clip_start = clip_start
cam.clip_end = clip_end

bpy.context.scene.render.resolution_x = int(cam_res_w)
bpy.context.scene.render.resolution_y = int(cam_res_h)

def collection_toggle_hide_render(collection, hide_render):
    for obj in collection.objects:
        obj.hide_render = hide_render

#def step_and_snap(overlap):
#    if overlap > 0.5:
#        print("Choose a smaller overlap ( < 0.5)"):
#        raise ValueError

#    num_vertical_iterations = img_coverage_w // (cam_coverage_w - overlap) + 1
#    num_horizontal_iterations = img_coverage_h // (cam_coverage_h - overlap) + 1
#    
#    for i in range(0, int(num_vertical_iterations):
#        for j in range(0, int(num_horizontal_iterations):

cam_standard_angle_deviation = 5 # degrees

min_day_of_year = 1
max_day_of_year = 365

min_time_of_day = 8.0
max_time_of_day = 16.0

city = "London"

color_path = f"C:\\Users\\bachc\\Documents\\GitHub\\Synthset-Generation\\Blender\\{city}\\Images\\Color\\"
sem_seg_path = f"C:\\Users\\bachc\\Documents\\GitHub\\Synthset-Generation\\Blender\\{city}\\Images\\Sem_seg\\"

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

links = bpy.data.worlds["World"].node_tree.nodes["Background"].inputs["Color"].links
if links[0] and bpy.data.worlds["World"].node_tree.nodes.find("Sky Texture") != -1:
    using_sky_tex = True
    using_bg = False
    sky_tex = bpy.data.worlds["World"].node_tree.nodes["Sky Texture"]
elif bpy.data.worlds["World"].node_tree.nodes.find("Background") != -1:
    using_bg = True
    using_sky_tex = False
    scene_brightness = bpy.data.worlds["World"].node_tree.nodes["Background"]
else:
    using_sky_tex = False
    using_bg = False
    
min_scene_brightness = 0.4
max_scene_brightness = 2

min_sun_elevation_angle = 23 # degrees
sun_rotation_deviation = 40 # degrees

for i in range(0, 5):
    if using_sky_tex:
        sky_tex.sun_rotation = random.uniform(180 - sun_rotation_deviation, 180 + sun_rotation_deviation)
        sky_tex.sun_elevation = random.uniform(min_sun_elevation_angle, 90)
    elif using_bg:
        scene_brightness.default_value = random.uniform(min_scene_brightness, max_scene_brightness)
    elif bpy.context.scene.sun_pos_properties.usage_mode == 'NORMAL':
        bpy.context.scene.sun_pos_properties.day_of_year = random.randrange(1, 365)
        bpy.context.scene.sun_pos_properties.time_of_day = random.uniform(8.0, 16.0)

    
#    cam_pivot.rotation_euler = mathutils.Euler((random.gauss(0, np.deg2rad(5)), random.gauss(0, np.deg2rad(5)), 0), 'XYZ')
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

