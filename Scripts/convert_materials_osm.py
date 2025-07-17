import bpy
import mathutils
import numpy as np

cam_pivot = bpy.data.objects.new("cam_pivot", None)
cam_obj = bpy.data.objects["Camera"]
cam_obj.rotation_euler = mathutils.Euler((0, 0, 0), 'XYZ')
cam_obj.location = mathutils.Vector((0, 0, 0))
cam_obj.parent = cam_pivot

light = bpy.data.objects["Light"].data
light.type = 'SUN'
light.energy = 10
#light.angle = np.deg2rad(0.526)

bpy.context.scene['City'] = 'London'
city = bpy.context.scene['City']

bpy.context.scene.sun_pos_properties.sun_object = bpy.data.objects["Light"]
bpy.context.scene.sun_pos_properties.sun_distance = 60000

models = [obj for obj in bpy.context.scene.objects if obj.name.startswith(city)]
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

def split_copy_mesh(obj):

    accumulator = {}

    for polygon in obj.data.polygons:
        
        mat = obj.data.materials[polygon.material_index]
        nodes = mat.node_tree.nodes
        if nodes.get("Image Texture") != None:
            img_name = nodes.get("Image Texture").image.name
            if 'Roof' in img_name or img_name.startswith('u_', 0) or img_name.startswith('g_', 0):
                tag = "buildings"
            else:
                tag = "terrain"
        else:
            tag = "terrain"


        acc = accumulator.get(tag)
        if acc is None:
            acc = {
                "tag":tag,
                "verts":[],
                "faces":[],
                "materials":[],
                "vertMap": {}
            }
            accumulator[tag] = acc

        face = []
        for vi in polygon.vertices:
            vi2 = acc["vertMap"].get(vi)
            if vi2 is None:
                verts = acc["verts"]
                vi2 = len( verts )
                acc["vertMap"][vi] = vi2
                verts.append(obj.data.vertices[vi].co)
            face.append(vi2)
        acc["faces"].append(face)
        acc["materials"].append(polygon.material_index)

    rval = []
    for tag,acc in accumulator.items():
        print(tag)

        mesh = bpy.data.meshes.new(tag)
        #print(acc)
        mesh.from_pydata(acc["verts"], [], acc["faces"])
        mesh.validate(verbose=True)

        for mat in obj.data.materials:
            mesh.materials.append(mat)

        for i in range(len(mesh.polygons)):
            mesh.polygons[i].material_index = acc["materials"][i]

        obj = bpy.data.objects.new(tag, mesh)
        dupe_collection.objects.link(obj)
        rval.append(obj)

    return rval
    
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
    dupes.append(copy)

for dupe in dupes:
    bpy.data.collections["Dupes"].objects.link(dupe)

