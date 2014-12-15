import bpy
import mathutils
import math
import os
import cProfile
import bgl

# serialize data to json

_OBJECT_PT_constraints = None

class ScenePanel(bpy.types.Panel):
    bl_label = "Avango-Blender"
    bl_idname = "SCENE_PT_b4a"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        if scene:

            row = layout.row()
            row.prop(scene, "enable_ssao", text="Enable SSAO")

            row = layout.row()
            row.prop(scene, "enable_god_rays", text="Enable God Rays")

            row = layout.row()
            row.prop(scene, "enable_bloom", text="Enable Bloom")

            row = layout.row()
            row.prop(scene, "enable_fog", text="Enable Fog")

            row = layout.row()
            row.prop(scene, "enable_vignette", text="Enable Vignette")

            row = layout.row()
            row.prop(scene, "enable_hdr", text="Enable HDR")

            row = layout.row()
            row.prop(scene, "enable_preview_display", text="Enable Preview Display")

            row = layout.row()
            row.prop(scene, "enable_fps_display", text="Enable FPS Display")

            row = layout.row()
            row.prop(scene, "enable_ray_display", text="Enable Ray Display")

            row = layout.row()
            row.prop(scene, "enable_bbox_display", text="Enable bbox Display")

            row = layout.row()
            row.prop(scene, "enable_wire_frame", text="Enable Wire Frame")

            row = layout.row()
            row.prop(scene, "enable_FXAA", text="Enable FXAA")

            row = layout.row()
            row.prop(scene, "enable_frustum_culling", text="Enable Frustum Culling")

            row = layout.row()
            row.prop(scene, "enable_backface_culling", text="Enable Backface Culling")

            row = layout.row()
            row.prop(scene, "near_clip", text="Near Clip")

            row = layout.row()
            row.prop(scene, "far_clip", text="Far Clip")

            split = layout.split()
            col = split.column()

class WorldPanel(bpy.types.Panel):
    bl_label = "Avango-Blender"
    bl_idname = "WORLD_PT_b4a"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "world"

    def draw(self, context):
        layout = self.layout

        world = context.world
        if world:
            ssao = world.ssao_settings
            row = layout.row()
            box = row.box()
            col = box.column()
            col.label("SSAO Settings:")
            row = col.row()
            row.prop(ssao, "radius", text="Radius")
            row = col.row()
            row.prop(ssao, "intensity", text="Intensity")
            row = col.row()
            row.prop(ssao, "falloff", text="Falloff")

            bloom = world.bloom_settings
            row = layout.row()
            box = row.box()
            col = box.column()
            col.label("Bloom settings:")
            row = col.row()
            row.prop(bloom, "radius", text="Radius")
            row = col.row()
            row.prop(bloom, "threshold", text="Threshold")
            row = col.row()
            row.prop(bloom, "intensity", text="Intensity")

            fog = world.fog_settings
            row = layout.row()
            box = row.box()
            col = box.column()
            col.label("Fog settings:")
            row = col.row()
            row.prop(fog, "start", text="Start")
            row = col.row()
            row.prop(fog, "end", text="End")
            row = col.row()
            row.prop(fog, "texture", text="Texture")
            row = col.row()
            row.prop(fog, "color", text="Color")

            background = world.background_settings
            row = layout.row()
            box = row.box()
            col = box.column()
            col.label("Background settings:")
            row = col.row()
            row.prop(background, "mode", text="Mode")
            row = col.row()
            row.prop(background, "texture", text="Texture")
            row = col.row()
            row.prop(background, "color", text="Color")

            vignette = world.vignette_settings
            row = layout.row()
            box = row.box()
            col = box.column()
            col.label("Vignette settings:")
            row = col.row()
            row.prop(vignette, "color", text="Color")
            row = col.row()
            row.prop(vignette, "coverage", text="Coverage")
            row = col.row()
            row.prop(vignette, "softness", text="Softness")

            hdr = world.hdr_settings
            row = layout.row()
            box = row.box()
            col = box.column()
            col.label("HDR settings:")
            row = col.row()
            row.prop(hdr, "key", text="Key")

class DataPanel(bpy.types.Panel):
    bl_label = "Avango-Blender"
    bl_idname = "DATA_PT_b4a"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"

    def draw(self, context):
        layout = self.layout

        cam = context.camera
        if cam:
            row = layout.row(align=True)
            row.prop(cam, "ms_style", text="Mono/Sterio")
            
class CustomConstraintsPanel(bpy.types.OBJECT_PT_constraints):
    def draw_constraint(self, context, con):

        if con.type == "LOCKED_TRACK":

            layout = self.layout
            box = layout.box()

            box.label("LOCKED_TRACK constraint reserved for " + con.name)

        else:
            global _OBJECT_PT_constraints
            _OBJECT_PT_constraints.draw_constraint(self, context, con)

def add_remove_refl_plane(obj):

    if obj.reflective:
        #add reflection plane
        bpy.ops.object.constraint_add(type="LOCKED_TRACK")

        lods = obj.lods
        index = len(lods)
        obj.refl_plane_index = index

        cons = get_locked_track_constraint(obj, index)
        cons.name = "REFLECTION PLANE"
        # disable fake LOCKED_TRACK constraint
        cons.mute = True

    else:
        #remove reflection plane

        index = obj.refl_plane_index

        if index >= 0:
            cons = get_locked_track_constraint(obj, index)
            obj.constraints.remove(cons)

def register():
    global _OBJECT_PT_constraints

    bpy.utils.register_class(ScenePanel)
    bpy.utils.register_class(WorldPanel)
    bpy.utils.register_class(DataPanel)

    _OBJECT_PT_constraints = bpy.types.OBJECT_PT_constraints
    bpy.utils.unregister_class(bpy.types.OBJECT_PT_constraints)
    bpy.utils.register_class(CustomConstraintsPanel)

def unregister():
    global _OBJECT_PT_constraints

    bpy.utils.unregister_class(ScenePanel)
    bpy.utils.unregister_class(WorldPanel)
    bpy.utils.unregister_class(DataPanel)

    bpy.utils.unregister_class(CustomConstraintsPanel)
    bpy.utils.register_class(_OBJECT_PT_constraints)