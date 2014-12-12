import bpy
from bpy_extras.io_utils import ExportHelper
import os
import json
from . import field_container

# TODO: 
# write parent

def avangoNodeTrees():
    return (x for x in bpy.data.node_groups if
        (x.bl_idname == 'AvangoCustomTreeType'))

def to_json(obj):
    if isinstance(obj, field_container.SceneGraph):
        name = obj.name
        root = 'null'
        i = bpy.data.objects.find(obj.root)
        if -1 != i :
            root = bpy.data.objects[obj.root].name
        return {
                'type' : 'SceneGraph',
                'name' : obj.name,
                'root' : root
        }
    if isinstance(obj, field_container.Window):
        modeSocket = bpy.data.node_groups["NodeTree"].nodes["Window"].inputs['StereoMode']
        if modeSocket.is_linked and modeSocket.links[0].is_valid:
          mode = modeSocket.links[0].from_socket.stereo_mode
        else:
          mode = modeSocket.stereo_mode
        return {
                'type' : 'Window',
                'name' : obj.name,
                'title' : obj.title_field,
                'display' : obj.display_field,
                'left_resolution' : [obj.left_size[0], obj.left_size[1]],
                'left_position' : [obj.left_pos[0], obj.left_pos[1]],
                'mode' : mode
        }
    if isinstance(obj, field_container.Viewer):

        windowSocket = bpy.data.node_groups["NodeTree"].nodes[obj.name].inputs['Window']
        if windowSocket.is_linked and windowSocket.links[0].is_valid:
          window = windowSocket.links[0].from_node.name
        else:
          window = 'null'

        cameraSocket = bpy.data.node_groups["NodeTree"].nodes[obj.name].inputs['SceneGraph']
        if cameraSocket.is_linked and cameraSocket.links[0].is_valid:
          camera = cameraSocket.links[0].from_node.name
        else:
          camera = 'null'

        sgSocket = bpy.data.node_groups["NodeTree"].nodes[obj.name].inputs['Camera']
        if sgSocket.is_linked and sgSocket.links[0].is_valid:
          scenegraph = sgSocket.links[0].from_node.name
        else:
          scenegraph = 'null'

        return {
                'name' : obj.name,
                'type' : 'Viewer',
                'window' : window,
                'scenegraph' : scenegraph,
                'camera' : camera
        }
    if isinstance(obj, field_container.Camera):
        parent = 'null'
        if obj.referenced_object in bpy.data.objects:
          parent = bpy.data.objects[obj.referenced_object].parent

        return {
                'type' : 'Camera',
                'name' : obj.name,
                'scenegraph' : obj.scenegraph,
                'output_window_name' : obj.output_window_name,
                'resolution' : [ obj.resolution[0], obj.resolution[1] ],
                'parent' : parent.name
        }
    if isinstance(obj, field_container.Light):
        name = obj.name
        i = bpy.data.objects.find(obj.referenced_object)
        lamp = None
        o = None
        if -1 != i :
            o = bpy.data.objects[obj.referenced_object]
            lamp = bpy.data.lamps[o.data.name]
        ty = 'null'
        if lamp.type == 'POINT':
            ty = 'PointLight'
#     print(" Location: ", o.location) # light radius
#     print(" Scale: ", o.scale) # light radius
#     print(" Rotation Quaternion: ", o.rotation_quaternion) # light radius

        parent = 'null'
        if obj.referenced_object in bpy.data.objects:
          parent = bpy.data.objects[obj.referenced_object].parent

        if lamp is not None:
            return  {
                      'name' : obj.name,
                      'type' : ty,
                      'color' : [ lamp.color.r, lamp.color.g, lamp.color.b],
                      'distance' : lamp.distance,
                      'parent' : parent.name,
                      'energy' : lamp.energy
                    }
        else:
            return  {
                      'name' : obj.name,
                      'type' : ty
                    }

    if isinstance(obj, field_container.Mesh):

        parent = 'null'
        if obj.referenced_object in bpy.data.objects:
          parent = bpy.data.objects[obj.referenced_object].parent
        return {
                'type' : 'Mesh',
                'parent' : parent.name,
                'name' : obj.name
        }
    if isinstance(obj, field_container.Screen):
        parent = 'null'
        if obj.referenced_object in bpy.data.objects:
          parent = bpy.data.objects[obj.referenced_object].parent
        return {
                'type' : 'Screen',
                'parent' : parent.name,
                'name' : obj.name
        }
    if isinstance(obj, field_container.Transform):
        parent = 'null'
        if obj.referenced_object in bpy.data.objects:
          parent = bpy.data.objects[obj.referenced_object].parent
        return {
                'type' : 'Transform',
                'parent' : parent.name,
                'name' : obj.name
        }

    raise TypeError(repr(obj) + ' is not JSON serializable')

def meshAsDict(mesh):
    i = bpy.data.objects.find(self.referenced_object)
    if -1 != i :
        obj = bpy.data.objects[self.referenced_object]
    #parent
    #children
    #transform
    #boundingbox
    #shadowmode # OFF, LOW_QUALITY, HIGH_QUALITY
    #material

    return {
            'type' : 'TriMeshNode',
            'name' : mesh.name
            # 'transform' : matrix
            }

printFieldContainer = {
    'Mesh' : meshAsDict,
    'Light' : meshAsDict,
    'Transform' : meshAsDict
}

#def save(operator, context, filepath = ""):
def save(operator, context):
    which = "NodeTree"
    ns = bpy.data.node_groups[which].nodes
    document = {
      #triMeshes  = (x for x in ns if (x.bl_label == 'Mesh'))
      #screens    = (x for x in ns if (x.bl_label == 'Screen'))
      #'transforms' : list(x for x in ns if (x.bl_label == 'Transform'))
      'viewer'      : dict((x.name,x) for x in ns if (x.bl_label == 'Viewer')),
      'scenegraphs' : dict((x.name,x) for x in ns if (x.bl_label == 'SceneGraph')),
      'windows'     : dict((x.name,x) for x in ns if (x.bl_label == 'Window')),
      'cameras'     : dict((x.name,x) for x in ns if (x.bl_label == 'Camera')),
      'lights'      : dict((x.name,x) for x in ns if (x.bl_label == 'Light')),
      'meshes'      : dict((x.name,x) for x in ns if (x.bl_label == 'Mesh')),
      'screens'  : dict((x.name,x) for x in ns if (x.bl_label == 'Screen')),
      'transforms'  : dict((x.name,x) for x in ns if (x.bl_label == 'Transform'))
      }

    with open('/tmp/blabla.json', 'w', encoding='utf-8') as f:
        json.dump(document, f, default=to_json, indent=4)
    return {'FINISHED'}

class ExportAvango(bpy.types.Operator, ExportHelper):
    '''Export selected object / scene for Avango (ASCII JSON format).'''

    bl_idname = "export.avango"
    bl_label = "Export Avango"

    filename_ext = ".json"

    def invoke(self, context, event):
        #restore_settings_export(self.properties)
        return ExportHelper.invoke(self, context, event)

    @classmethod
    def poll(cls, context):
        return context.active_object != None

    def execute(self, context):
        print("Selected: " + context.active_object.name)
        if not self.properties.filepath:
            raise Exception("filename not set")

        filepath = self.filepath

        return save(self, context)#, **self.properties)

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text="Geometry:")

def menu_func_export(self, context):
    default_path = bpy.data.filepath.replace(".blend", ".json")
    self.layout.operator(ExportAvango.bl_idname, \
        text="Avango (.json)").filepath = default_path

def register():
    bpy.utils.register_class(ExportAvango)
    bpy.types.INFO_MT_file_export.append(menu_func_export)

def unregister():
    bpy.utils.register_class(ExportAvango)
    bpy.types.INFO_MT_file_export.remove(menu_func_export)
