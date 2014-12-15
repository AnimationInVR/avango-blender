import bpy
import mathutils
import math
import os
import cProfile
from .interface import *

class SSAOSettings(bpy.types.PropertyGroup):

    radius = bpy.props.FloatProperty(
        name = "radius",
        description = "radius",
        default = 0.0,
        min = 0.0,
        max = 20.0,
        step = 0.01,
        precision = 2
    )

    intensity = bpy.props.FloatProperty(
        name = "intensity",
        description = "intensity",
        default = 0.0,
        min = 0.0,
        max = 20.0,
        step = 0.01,
        precision = 2
    )

    falloff = bpy.props.FloatProperty(
        name = "falloff",
        description = "falloff",
        default = 0.0,
        min = 0.0,
        max = 20.0,
        step = 0.01,
        precision = 2
    )

class BloomSettings(bpy.types.PropertyGroup):

    radius = bpy.props.FloatProperty(
        name = "radius",
        description = "radius",
        default = 0.0,
        min = 0.0,
        max = 20.0,
        step = 0.01,
        precision = 2
    )

    threshold = bpy.props.FloatProperty(
        name = "threshold",
        description = "threshold",
        default = 0.0,
        min = 0.0,
        max = 20.0,
        step = 0.01,
        precision = 2
    )

    intensity = bpy.props.FloatProperty(
        name = "intensity",
        description = "intensity",
        default = 0.0,
        min = 0.0,
        max = 20.0,
        step = 0.01,
        precision = 2
    )

class FogSettings(bpy.types.PropertyGroup):

    start = bpy.props.FloatProperty(
        name = "start",
        description = "start",
        default = 1.0,
        min = 0.0,
        max = 5.0,
        step = 0.01,
        precision = 2
    )

    end = bpy.props.FloatProperty(
        name = "end",
        description = "end",
        default = 4.0,
        min = 0.0,
        max = 20.0,
        step = 0.01,
        precision = 2
    )

    texture = bpy.props.StringProperty(
        name = "texture",
        description = "texture",
        default = ""
    )

    color = bpy.props.FloatVectorProperty(
        name = "Avango-Blender: fog color",
        description = "Fog color",
        default = (0.5, 0.5, 0.5),
        min = 0.0,
        soft_min = 0.0,
        max = 1.0,
        soft_max = 1.0,
        precision = 3,
        subtype = 'COLOR',
        size = 3
    )

class BackgroundSettings(bpy.types.PropertyGroup):
   
    mode = bpy.props.FloatProperty(
        name = "mode",
        description = "mode",
        default = 0,
        min = 0,
        max = 5,
        step = 1
    )

    texture = bpy.props.StringProperty(
        name = "texture",
        description = "texture",
        default = ""
    )

    color = bpy.props.FloatVectorProperty(
        name = "Avango-Blender: Background color",
        description = "Background color",
        default = (0.5, 0.5, 0.5),
        min = 0.0,
        soft_min = 0.0,
        max = 1.0,
        soft_max = 1.0,
        precision = 3,
        subtype = 'COLOR',
        size = 3
    )

class VignetteSettings(bpy.types.PropertyGroup):

    color = bpy.props.FloatVectorProperty(
        name = "Avango-Blender: coverage color",
        description = "coverage color",
        default = (0.5, 0.5, 0.5),
        min = 0.0,
        soft_min = 0.0,
        max = 1.0,
        soft_max = 1.0,
        precision = 3,
        subtype = 'COLOR',
        size = 3
    )

    coverage = bpy.props.FloatProperty(
        name = "coverage",
        description = "coverage",
        default = 1.0,
        min = 0.0,
        max = 5.0,
        step = 0.01,
        precision = 2
    )

    softness = bpy.props.FloatProperty(
        name = "softness",
        description = "softness",
        default = 4.0,
        min = 0.0,
        max = 20.0,
        step = 0.01,
        precision = 2
    )

class HdrSettings(bpy.types.PropertyGroup):

    key = bpy.props.FloatProperty(
        name = "key",
        description = "key",
        default = 1.0,
        min = 0.0,
        max = 5.0,
        step = 0.01,
        precision = 2
    )


def add_props():

    do_not_export = bpy.props.BoolProperty(
        name = "Avango-Blender: do not export",
        description = "Check if you do NOT wish to export this component",
        default = False
    )

    # deprecated
    export_path = bpy.props.StringProperty(
        name = "Avango-Blender: component export path",
        description = "Exported file path relative to the blend file",
        default = ""
    )

    class_names = [
        'Action',
        'Armature',
        'Camera',
        'Curve',
        'Group',
        'Image',
        'Lamp',
        'Material',
        'Mesh',
        'Object',
        'ParticleSettings',
        'Texture',
        'Scene',
        'Speaker',
        'Sound',
        'World'
    ]

    class_names_for_export = [
        'Action',
        'Image',
        'Material',
        'Object',
        'ParticleSettings',
        'Scene',
        'Texture',
        'World'
    ]

    for class_name in class_names_for_export:
        cl = getattr(bpy.types, class_name)
        cl.do_not_export = do_not_export

    for class_name in class_names:
        cl = getattr(bpy.types, class_name)
        # deprecated
        cl.export_path   = export_path

    export_path_json = bpy.props.StringProperty(
        name = "Avango-Blender: export path json",
        description = "Exported json file path relative to the blend file",
        default = ""
    )
    export_path_html = bpy.props.StringProperty(
        name = "Avango-Blender: export path html",
        description = "Exported html file path relative to the blend file",
        default = ""
    )
    bpy.types.Scene.export_path_json = export_path_json
    bpy.types.Scene.export_path_html = export_path_html

    add_scene_properties()

    add_world_properties()
     
def add_scene_properties():

    scene_type = bpy.types.Scene

    enable_ssao = bpy.props.BoolProperty(
        name = "Avango-Blender: enable SSAO",
        description = "Enable screen space ambient occlusion",
        default = False
    )
    scene_type.enable_ssao = enable_ssao

    enable_preview_display = bpy.props.BoolProperty(
        name = "Avango-Blender: enable preview display",
        description = "enable preview display",
        default = False
    )
    scene_type.enable_preview_display = enable_preview_display

    enable_fps_display = bpy.props.BoolProperty(
        name = "Avango-Blender: enable fps display",
        description = "enable fps display",
        default = False
    )
    scene_type.enable_fps_display = enable_fps_display

    enable_ray_display = bpy.props.BoolProperty(
        name = "Avango-Blender: enable ray display",
        description = "enable ray display",
        default = False
    )
    scene_type.enable_ray_display = enable_ray_display

    enable_bbox_display = bpy.props.BoolProperty(
        name = "Avango-Blender: enable bbox display",
        description = "enable bbox display",
        default = False
    )
    scene_type.enable_bbox_display = enable_bbox_display

    enable_fxaa = bpy.props.BoolProperty(
        name = "Avango-Blender: enable FXAA",
        description = "Enable FXAA",
        default = False
    )
    scene_type.enable_fxaa = enable_fxaa

    enable_frustum_culling = bpy.props.BoolProperty(
        name = "Avango-Blender: enable_frustum_culling",
        description = "enable_frustum_culling",
        default = False
    )
    scene_type.enable_frustum_culling = enable_frustum_culling

    enable_backface_culling = bpy.props.BoolProperty(
        name = "Avango-Blender: enable_backface_culling",
        description = "enable_backface_culling",
        default = False
    )
    scene_type.enable_backface_culling = enable_backface_culling

    near_clip = bpy.props.FloatProperty(
        name = "Avango-Blender: near clip",
        description = "near clip",
        default = 0.1,
        min = 0.0000001,
        soft_min = 0.01,
        max = 1000.0,
        soft_max = 100.0,
        step = 0.1,
        precision = 4
    )

    scene_type.near_clip = near_clip

    far_clip = bpy.props.FloatProperty(
        name = "Avango-Blender: far clip",
        description = "far clip",
        default = 1000.0,
        min = 0.0,
        soft_min = 0.0,
        max = 1000000000.0,
        soft_max = 0.1,
        step = 0.1,
        precision = 4
    )

    scene_type.far_clip = far_clip

    enable_bloom = bpy.props.BoolProperty(
        name = "Avango-Blender: enable bloom",
        description = "Enable bloom",
        default = False
    )
    scene_type.enable_bloom = enable_bloom

    enable_fog = bpy.props.BoolProperty(
        name = "Avango-Blender: enable fog",
        description = "Enable fog",
        default = False
    )
    scene_type.enable_fog = enable_fog

    enable_vignette = bpy.props.BoolProperty(
        name = "Avango-Blender: enable vignette",
        description = "Enable vignette",
        default = False
    )
    scene_type.enable_vignette = enable_vignette

    enable_fog = bpy.props.BoolProperty(
        name = "Avango-Blender: enable fog",
        description = "Enable fog",
        default = False
    )
    scene_type.enable_fog = enable_fog

    enable_FXAA = bpy.props.BoolProperty(
        name = "Avango-Blender: enable fxaa",
        description = "Enable fxaa",
        default = False
    )
    scene_type.enable_FXAA = enable_FXAA

    enable_hdr = bpy.props.BoolProperty(
        name = "Avango-Blender: enable hdr",
        description = "Enable hdr",
        default = False
    )
    scene_type.enable_hdr = enable_hdr

def add_world_properties():

    # for world panel
    
    fog_color = bpy.props.FloatVectorProperty(
        name = "Avango-Blender: fog color",
        description = "Fog color",
        default = (0.5, 0.5, 0.5),
        min = 0.0,
        soft_min = 0.0,
        max = 1.0,
        soft_max = 1.0,
        precision = 3,
        subtype = 'COLOR',
        size = 3
    )
    bpy.types.World.fog_color = fog_color

    fog_density = bpy.props.FloatProperty(
        name = "Avango-Blender: fog density",
        description = "Fog density",
        default = 0.0,
        min = 0.0,
        soft_min = 0.0,
        max = 1.0,
        soft_max = 0.1,
        step = 0.1,
        precision = 4
    )

    bpy.types.World.fog_density = fog_density

    bpy.types.World.ssao_settings = bpy.props.PointerProperty(
        name = "Avango-Blender: SSAO settings",
        type = SSAOSettings
    )

    bpy.types.World.bloom_settings = bpy.props.PointerProperty(
        name = "Avango-Blender: bloom settings",
        type = BloomSettings
    )

    bpy.types.World.fog_settings = bpy.props.PointerProperty(
        name = "Avango-Blender: fog settings",
        type = FogSettings
    )

    bpy.types.World.background_settings = bpy.props.PointerProperty(
        name = "Avango-Blender: background settings",
        type = BackgroundSettings
    )

    bpy.types.World.vignette_settings = bpy.props.PointerProperty(
        name = "Avango-Blender: vignette settings",
        type = VignetteSettings
    )

    bpy.types.World.hdr_settings = bpy.props.PointerProperty(
        name = "Avango-Blender: hdr settings",
        type = HdrSettings
    )

def register():
    bpy.utils.register_class(SSAOSettings)
    bpy.utils.register_class(BloomSettings)
    bpy.utils.register_class(FogSettings)
    bpy.utils.register_class(BackgroundSettings)
    bpy.utils.register_class(VignetteSettings)
    bpy.utils.register_class(HdrSettings)
    add_props()

def unregister():
    bpy.utils.unregister_class(SSAOSettings)
    bpy.utils.unregister_class(BloomSettings)
    bpy.utils.unregister_class(FogSettings)
    bpy.utils.unregister_class(BackgroundSettings)
    bpy.utils.unregister_class(VignetteSettings)
    bpy.utils.unregister_class(HdrSettings)

