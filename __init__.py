bl_info = {
    "name": "Avango",
    "author": "Avango Development Team",
    "version": (14, 11, 0),
    "blender": (2, 72, 0),
    "b4w_format_version": "5.01",
    "location": "File > Import-Export",
    "description": "Avango is a Blender-friendly 3D web framework",
    "warning": "",
    "wiki_url": "http://www.blend4web.com/doc",
    "category": "Import-Export"
}

if "bpy" in locals():
    import imp
    imp.reload(properties)
    imp.reload(interface)
    imp.reload(node_tree)
    imp.reload(field_container)
    imp.reload(exporter)
else:
    from . import properties
    from . import interface
    from . import node_tree
    from . import field_container
    from . import exporter

import bpy
import nodeitems_utils
import nodeitems_utils as nu
from bpy.props import StringProperty

import os

node_categories = [
    node_tree.AvangoNodeCategory("SOMENODES", "avango.osg", items=[
      nu.NodeItem("SceneGraph"),
      nu.NodeItem("Viewer"),
      nu.NodeItem("Window"),
      nu.NodeItem("Camera"),
      nu.NodeItem("Light"),
      nu.NodeItem("Screen"),
      nu.NodeItem("Transform"),
      nu.NodeItem("Mesh"),
    ]),
    #node_tree.AvangoNodeCategory("SOMENODES", "Nodes", items=[
    #]
    #node_tree.AvangoNodeCategory("SOMENODES", "Texture", items=[
    #]
    #node_tree.AvangoNodeCategory("SOMENODES", "Loader", items=[
    #]
  ]

def register():
    properties.register()
    interface.register()
    node_tree.register()
    field_container.register()
    exporter.register()

    # Idee: root am SceneGraph
# 1.)
# alle objects haben CollectionProperty,
# sollte beim exportieren des scene graphs ein die CollectionProperty eines
# Hierarchieknotens leer sein, wird ein default FieldContainer des
# passenden typs erstellt
# 2.) wenn ein Node gelöscht wird, soll auf referenzierten blender objecten
#   vorher die Referenz auf diesen Node entfernt werden

    #bpy.types.Object.avango_nodes = bpy.props.CollectionProperty(type=bpy.types.PropertyGroup)

    if not 'AVANGO_NODES' in nu._node_categories:
        nu.register_node_categories('AVANGO_NODES', node_categories)

def unregister():
    properties.unregister() 
    interface.unregister() 
    node_tree.unregister()
    field_container.unregister()
    exporter.unregister()
    if 'AVANGO_NODES' in nu._node_categories:
        nu.unregister_node_categories('AVANGO_NODES')

if __name__ == "__main__":
    register()
