import bpy
import mathutils
import numpy as np

cam_pivot = bpy.data.objects.new("cam_pivot", None)
bpy.data.collections["Collection"].objects.link(cam_pivot)
cam_obj = bpy.data.objects["Camera"]
cam_obj.rotation_euler = mathutils.Euler((0, 0, 0), 'XYZ')
cam_obj.location = mathutils.Vector((0, 0, 0))
cam_obj.parent = cam_pivot

light = bpy.data.objects["Light"].data
light.type = 'SUN'
light.energy = 10

bpy.context.scene["city"] = "yoy"  # Example city name, adjust as needed
city = bpy.context.scene["city"]

bpy.context.scene.sun_pos_properties.sun_object = bpy.data.objects["Light"]
bpy.context.scene.sun_pos_properties.sun_distance = 60000

models = [obj for obj in bpy.context.scene.objects if obj.name.startswith(f"{city}")]
dupe_collection = bpy.data.collections.new("Dupes")
bpy.context.scene.collection.children.link(dupe_collection)

for mat in bpy.data.materials:
   if not mat.use_nodes:
       continue
   nodes = mat.node_tree.nodes
   for node in nodes:
       if node.type == "NORMAL_MAP":
           nodes.remove(node)
   nodes.get("Principled BSDF").inputs["Metallic"].default_value = 1

dupe_mat_names = ["BuildingDupe", "TerrainDupe"]
dupe_mat_emission_color = [
    (1.0, 1.0, 1.0, 1),
    (0, 0, 0, 1)
]

for name, color in zip(dupe_mat_names, dupe_mat_emission_color):
    dupe = bpy.data.materials.new(name)
    dupe.use_nodes = True
    nodes = dupe.node_tree.nodes
    emit = nodes.new("ShaderNodeEmission")
    emit.inputs["Color"].default_value = color
    emit.inputs["Strength"].default_value = 15
    new_link = dupe.node_tree.links.new(nodes['Material Output'].inputs['Surface'], nodes['Emission'].outputs['Emission'])

mat_dict = {mat.name: i for i, mat in enumerate(bpy.data.materials)}
   
dupes = []
for obj in models:
    mesh = obj.data.copy()
    name = obj.name.split('_')[1]
    copy = bpy.data.objects.new(name, mesh)
    if copy.name == "buildings":
        copy.data.materials.append(bpy.data.materials["BuildingDupe"])
        for polygon in copy.data.polygons:
            polygon.material_index = mat_dict["BuildingDupe"]
        copy.active_material = bpy.data.materials["BuildingDupe"]
    else:
        copy.data.materials.append(bpy.data.materials["TerrainDupe"])
        for polygon in copy.data.polygons:
            polygon.material_index = mat_dict["TerrainDupe"]
        copy.active_material = bpy.data.materials["TerrainDupe"]
    copy.rotation_euler.x = np.deg2rad(90)
    dupe_collection.objects.link(copy)
    dupes.append(copy)
    
