import bpy
from bpy.types import NodeTree, Node, NodeSocket
from bpy.props import StringProperty, IntProperty, FloatProperty, IntVectorProperty, FloatVectorProperty, BoolProperty
from . import node_tree
from bpy.app.handlers import persistent

# field connection socket color
# TODO: 

class Camera(Node, node_tree.AvangoCustomTreeNode):
    bl_idname = 'Camera'
    bl_label = 'Camera'

    def update_name(self, context):
        lamp = None
        if self.referenced_object in bpy.data.objects:
            bpy.data.objects[self.referenced_object].name = self.name
            self.referenced_object = self.name
        else:
            print("Error: failed referenced_object")

    name = StringProperty(description='name', update=update_name)

    scenegraph = StringProperty(
            default='SceneGraph',
            description='name of scenegraph'
            )

    output_window_name = StringProperty(
            default='Window',
            description=''
            )

    referenced_object = StringProperty(
            description='name of referenced blender object'
            )

    resolution = IntVectorProperty(
            name="Resolution",
            description="resolution",
            default=(1024,768),
            min=1,
            size=2
            )

    def init(self, context):

        bpy.ops.object.camera_add()
        obj = bpy.context.object
        self.referenced_object = obj.name
        self.name = obj.name
        obj["avango_nodes"] = self.name

        self.outputs.new('CameraSocketType', 'Camera')

    def draw_buttons(self, context, layout):
        scene = context.scene
        col = layout.column()
        col.prop(self, 'name', text='Name')
        col.prop(self, 'scenegraph', text='SceneGraph')
        col.prop(self, 'output_window_name', text='OutputWindowName')
        col.prop(self, 'resolution', text='Resolution')
        col.label(text='Camera: '+self.referenced_object, icon='CAMERA_DATA')
        # browse cameras
        #col.prop_search(self, 'referenced_object', bpy.data, 'cameras',
        #        text='', icon='CAMERA_DATA')

    def process(self):
        pass

    def get_args(self):
        pass

class Screen(Node, node_tree.AvangoCustomTreeNode):
    bl_idname = 'Screen'
    bl_label = 'Screen'

    width = FloatProperty(default=2, step=0.001, min=0.01)
    height = FloatProperty(default=1.5, step=0.001, min=0.01)

    def init(self, context):
        pass

    def draw_buttons(self, context, layout):
        scene = context.scene
        col = layout.column()
        col.prop(self, 'name', text='Name')
        col.prop(self, 'width', text='Width')
        col.prop(self, 'height', text='Heigth')

    def process(self):
        pass

    def get_args(self):
        pass

class Light(Node, node_tree.AvangoCustomTreeNode):
    bl_idname = 'Light'
    bl_label = 'Light'

    def update_name(self, context):
        lamp = None
        if self.referenced_object in bpy.data.objects:
            bpy.data.objects[self.referenced_object].name = self.name
            self.referenced_object = self.name
        else:
            print("Error: failed update_linked_lamp_name")

    name = StringProperty(description='name', update=update_name)

    referenced_object = StringProperty(
            default='',
            description='name of referenced blender object'
            #update=update_node
            )
            #update= todo when update , add my name to blender object

    def init(self, context):
        bpy.ops.object.lamp_add(type='POINT')
        obj = bpy.context.object
        self.referenced_object = obj.name
        self.name = obj.name
        obj["avango_nodes"] = self.name

    def draw_buttons(self, context, layout):
        scene = context.scene
        col = layout.column()
        col.prop(self, 'name', text='Name')
        #if referenced_object == '':
        #    col.prop(self, ...oplus, button new light
        # browse lights
        #col.prop_search(self, 'referenced_object', bpy.data, 'lamps',
        #        text='', icon='LAMP_DATA')
        col.label(text='Light: '+self.referenced_object, icon='LAMP_DATA')

    def free(self):
        print("Light unregister shit")
        i = bpy.data.objects.find(self.referenced_object)
        if -1 != i :
            print("Remove link to me")

            obj = bpy.data.objects[self.referenced_object]
            if obj.get("avango_nodes"):
                obj["avango_nodes"] = list(filter((obj["avango_nodes"]).__ne__, self.name))

    def process(self):
        pass

    def get_args(self):
        pass

class Mesh(Node, node_tree.AvangoCustomTreeNode):
    bl_idname = 'Mesh'
    bl_label = 'Mesh'

    referenced_object = StringProperty(description='linked mesh',
            #update= todo when update , add my name to blender object
            )

    def init(self, context):
        pass

    def draw_buttons(self, context, layout):
        scene = context.scene
        col = layout.column()
        col.prop(self, 'name', text='Name')
        col.prop_search(self, 'referenced_object', bpy.data, 'meshes',
                text='', icon='MESH_DATA')

    # a blender mesh is telling us, that it will no longer link to this mesh
    def unregister(blender_mesh):
      if blender_mesh.name == self.referenced_object:
          self.referenced_object = ""
      # else:
      #   ignore event

    def process(self):
        pass

    def get_args(self):
        pass

    def free(self):
        print("Mesh unregister shit")
        i = bpy.data.objects.find(self.referenced_object)
        if -1 != i :
            print("Remove link to me")

            obj = bpy.data.objects[self.referenced_object]
            if obj.get("avango_nodes"):
                obj["avango_nodes"] = list(filter((obj["avango_nodes"]).__ne__, self.name))

class SceneGraph(Node, node_tree.AvangoCustomTreeNode):
    bl_idname = 'SceneGraph'
    bl_label = 'SceneGraph'

    root = StringProperty(description='root node', default='Av_root')

    def init(self, context):
        self.outputs.new('SceneGraphSocketType', 'SceneGraph')
        bpy.ops.object.empty_add(type='PLAIN_AXES')
        bpy.context.object.name = 'Av_root'

    def draw_buttons(self, context, layout):
        col = layout.column()
        col.prop(self, 'name', text='Name')
        col.label(text='Root: '+self.root, icon='OBJECT_DATA')

#        col.prop_search(self, 'root', bpy.data, 'objects',
#                text='', icon='OBJECT_DATA')

    def process(self):
        pass

    def get_args(self):
        pass

'''
class MatrixSocket(NodeSocket):
    # 4x4 matrix Socket_type
    # ref: http://urchn.org/post/nodal-transform-experiment
    bl_idname = "MatrixSocket"
    bl_label = "Matrix Socket"
    prop_name = StringProperty(default='')
    def sv_get(self, default=sentinel, deepcopy=True):
        if self.is_linked and not self.is_output:
            return SvGetSocket(self, deepcopy)
        elif default is sentinel:
            raise SvNoDataError
        else:
            return default
    def sv_set(self, data):
        SvSetSocket(self, data)
    def draw(self, context, layout, node, text):
        if self.is_linked:
            layout.label(text + '. ' + SvGetSocketInfo(self))
        else:
            layout.label(text)
    def draw_color(self, context, node):
        #if self.is_linked:
        #    return(.8,.3,.75,1.0)
        #else:
        return(.2, .8, .8, 1.0)
'''

class Transform(Node, node_tree.AvangoCustomTreeNode):
    bl_idname = 'Transform'
    bl_label = 'Transform'

    referenced_object = StringProperty(default='transform',
            description='identifies this FieldContainer')

    def init(self, context):
        bpy.ops.object.empty_add(type='PLAIN_AXES')
#        bpy.context.object.name = 'transform'
        # self.inputs.new('MatrixSocketType', 'Transform')

    def draw_buttons(self, context, layout):
        col = layout.column()
        col.prop(self, 'name', text='Name')
        col.prop_search(self, 'referenced_object', bpy.data, 'objects',
                text='', icon='OBJECT_DATA')

    def process(self):
        pass

    def get_args(self):
        pass

class Viewer(Node, node_tree.AvangoCustomTreeNode):
    bl_idname = 'Viewer'
    bl_label = 'Viewer'

    def init(self, context):
        self.color = (0.4022911489, 0.6329187, 0.841202378)
        self.inputs.new('WindowSocketType', 'Window')
        self.inputs.new('SceneGraphSocketType', 'SceneGraph')
        self.inputs.new('CameraSocketType', 'Camera')

    def draw_buttons(self, context, layout):
        col = layout.column()
        col.prop(self, 'name', text='Name')
        #col.operator("node.sp_serialize_synthdef", text='make synthdef')

    def process(self):
        pass

    def get_args(self):
        pass

class Window(Node, node_tree.AvangoCustomTreeNode):
    bl_idname = 'Window'
    bl_label = 'Window'

    display_field = StringProperty(description='display number', default=':0.0')
    title_field   = StringProperty(description='window title', default='beautiful')

    left_size = IntVectorProperty(
            name="Resolution",
            description="size",
            default=(1024,768),
            min=1,
            size=2
            )

    left_pos = IntVectorProperty(
            name="Position",
            description="size",
            default=(0,0),
            min=0,
            size=2
            )

    enabled = BoolProperty(
            name = "enabled",
            description="enabled",
            default=True
            )

    def init(self, context):
        self.inputs.new('StereoModeSocketType', "StereoMode")
        self.outputs.new('WindowSocketType', 'Window')

    def draw_buttons(self, context, layout):
        col = layout.column()
        col.prop(self, 'name', text='Name')
        col.prop(self, 'title_field', text='Title')
        col.prop(self, 'display_field', text='Display')
        col.prop(self, 'left_size', text='LeftSize')
        col.prop(self, 'left_pos', text='LeftPosition')

    def process(self):
        pass

    def get_args(self):
        pass

# Sockets - theses Correspond to the various field types

class CameraSocket(NodeSocket):
    '''Camera node socket type'''
    bl_idname = 'CameraSocketType'
    bl_label = 'Camera Socket'

#    def camera_select(self, context):
#        cams = bpy.data.cameras
#        return [(c.name,c.name,"") for c in cams]
#
#    cameraProperty = bpy.props.EnumProperty(items=camera_select)

    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
#        if self.is_output or self.is_linked:
            layout.label(text)
#        else:
#            layout.prop(self, "cameraProperty", text=text)

    # Socket color
    def draw_color(self, context, node):
        return (0.216, 0.4, 1.0, 0.5)

class WindowSocket(NodeSocket):
    '''Custom node socket type'''
    bl_idname = 'WindowSocketType'
    bl_label = 'Window Socket'

    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
#        if self.is_output or self.is_linked:
            layout.label(text)
#        else:
#            layout.prop(self, "stereo_mode", text=text)

    # Socket color
    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 0.5)

class SceneGraphSocket(NodeSocket):
    '''SceneGraph node socket type'''
    bl_idname = 'SceneGraphSocketType'
    bl_label = 'SceneGraph Socket'

    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
#        if self.is_output or self.is_linked:
            layout.label(text)
#        else:
#            layout.prop(self, "stereo_mode", text=text)

    # Socket color
    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 0.5)

# Custom socket type
class StereoModeSocket(NodeSocket):
    # Description string
    '''Custom node socket type'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'StereoModeSocketType'
    bl_label = 'Stereo Mode Socket'

    # Enum items list
    modes = [
        ("MONO", "Mono", "mono"),
        ("SIDE_BY_SIDE", "SideBySide", "side by side stereo"),
        ("ANAGLYPH_RED_GREEN", "Anaglyph", "anaglyph stereo"),
        ("ANAGLYPH_RED_CYAN", "Anaglyph", "anaglyph stereo"),
        ("CHECKERBOARD", "Checkerboard", "checkerboard for 3D-TVs")
    ]

    stereo_mode = bpy.props.EnumProperty(name="StereoMode",
        description="stereo modes", items=modes, default='MONO')

    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text)
        else:
            layout.prop(self, "stereo_mode", text=text)

    # Socket color
    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 0.5)

# bpy.app.handlers.scene_update_pre
# bpy.app.handlers.scene_update_post
#@persistent
#def scene_update_pre(dummy):
#    print("scene_update_pre:")

@persistent
def scene_update_post(dummy):
    #print("scene_update_post:")
    objects = bpy.data.objects
#    if objects.is_updated:
#      print("one or more objects were updated")
    for object in objects:
        if object.is_updated_data:
          print("updateddata => {0}".format(object.name)) 
        if object.is_updated:
          print("updated => {0}".format(object.name)) 

def register():
    print("field_container.register()")
    bpy.utils.register_class(StereoModeSocket)
    bpy.utils.register_class(WindowSocket)
    bpy.utils.register_class(CameraSocket)
    bpy.utils.register_class(SceneGraphSocket)
    bpy.utils.register_class(SceneGraph)
    bpy.utils.register_class(Viewer)
    bpy.utils.register_class(Window)
    bpy.utils.register_class(Camera)
    bpy.utils.register_class(Light)
    bpy.utils.register_class(Mesh)
    bpy.utils.register_class(Screen)
    bpy.utils.register_class(Transform)

#    bpy.app.handlers.scene_update_pre.append(scene_update_pre)
#    bpy.app.handlers.scene_update_post.append(scene_update_post)

def unregister():
    print("field_container.unregister()")
    bpy.utils.unregister_class(StereoModeSocket)
    bpy.utils.unregister_class(WindowSocket)
    bpy.utils.unregister_class(CameraSocket)
    bpy.utils.unregister_class(SceneGraphSocket)
    bpy.utils.unregister_class(SceneGraph)
    bpy.utils.unregister_class(Viewer)
    bpy.utils.unregister_class(Window)
    bpy.utils.unregister_class(Camera)
    bpy.utils.unregister_class(Light)
    bpy.utils.unregister_class(Mesh)
    bpy.utils.unregister_class(Screen)
    bpy.utils.unregister_class(Transform)
