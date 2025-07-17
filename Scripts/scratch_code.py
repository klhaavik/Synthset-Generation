import bpy
import numpy as np

mat_dict = {mat.name: i for i, mat in enumerate(bpy.data.materials)}

bldg = bpy.data.objects["buildings"]
for polygon in bldg.data.polygons:
    polygon.material_index = mat_dict["BuildingDupe.001"]
bldg.active_material = bpy.data.materials["BuildingDupe.001"]

terrain = bpy.data.objects["terrain"]
for polygon in terrain.data.polygons:
    polygon.material_index = mat_dict["TerrainDupe.001"]
terrain.active_material = bpy.data.materials["TerrainDupe.001"]

#bpy.ops.object.mode_set(mode='OBJECT')

#for obj in bpy.context.selected_objects:
#    for face in obj.data.polygons:
#        face.select = (bpy.data.materials[face.material_index].name == "CityEngineMaterial_7.005")

#bpy.ops.object.mode_set(mode='EDIT')
#bpy.ops.mesh.delete(type='FACE')

#for mat in bpy.data.materials:
#    if mat.use_nodes == False: continue
#    for node in mat.node_tree.nodes:
#        if node.type == "TEX_IMAGE":
#            img_name = mat.node_tree.nodes["Image Texture"].image.name
#            if (
#            img_name.startswith("asphalt") 
#            or img_name.startswith("lanes") 
#            or img_name.startswith("centerline") 
#            or img_name.startswith("crosswalk")
#            or img_name.startswith("curbs")
#            or img_name.startswith("pavement")
#            ):
##                mat.node_tree.nodes["Principled BSDF"].inputs["Metallic"].default_value = 0
#                new_node = mat.node_tree.nodes.new('ShaderNodeBrightContrast')
#                bsdf_node = mat.node_tree.nodes["Principled BSDF"]
#                links = mat.node_tree.links
#                for link in links:
#                    if link.from_node == node and link.to_node == bsdf_node:
#                        links.remove(link)
#                        break
#                links.new(node.outputs["Color"], new_node.inputs["Color"])
#                links.new(new_node.outputs["Color"], bsdf_node.inputs["Base Color"])
#            break
                    
#                    
#for mat in bpy.data.materials:
#    if mat.use_nodes == False: continue
#    for node in mat.node_tree.nodes:
#        if node.bl_idname == "ShaderNodeBrightContrast":
#            print("here")
#            node.inputs[1].default_value = 0.3
