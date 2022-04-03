# (GNU GPL) <2022> <Taiseibutsu>" Developed for Blender 3.2, Tested on 3.1
# This program is free software: you can redistribute it and/or modify it, WITHOUT ANY WARRANTY that wont wake up on the backrooms. --- Kreepyrights is just a joke, this is license under GNU General Public License (GPL, or “free software”), but just with a strange name to reference, or maybe not...

bl_info = {
    "name": "Collection_Manager(TB)",
    "author": "Taiseibutsu",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "3D View, N Panel",
    "description": "Custom panel for visualice collections",
    "warning": "",
    "wiki_url": "",
    "category": "TB",
}
import bpy, addon_utils, os, rna_keymap_ui
from bpy.types import AddonPreferences, Panel 
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )

class TB_E_Properties(bpy.types.PropertyGroup):
    temp_stored_collection : bpy.props.StringProperty()

def setrenamename(ob,renamename):
    tbtool = bpy.context.scene.tb_data_tool
    pass   

def tbchangeactivecollection(collection_name):
    ac_col = bpy.context.layer_collection
    for ac_col in ac_col.children:
#        add condition recursive:
        ac_col.exclude = True
        for ac_col in ac_col.children:
            ac_col.exclude = True
    bpy.context.layer_collection.children[collection_name].exclude = False
    
    
class TB_CHANGE_COLLECTION_MANAGER(bpy.types.Operator):
    ''''''
    bl_idname = "tb_opx.change_active_collection"
    bl_label = "Renames data"
    
    collection_name : bpy.props.StringProperty(default = "s")
    def execute(self, context):
        print(str(collection_name))
        tbchangeactivecollection(collection_name)
        return {"FINISHED"}

def tbcollectionmanager(self, context):
    tbtool = context.scene.tb_data_tool
    layout = self.layout
    row = layout.row()
    row.label(text=str(len(bpy.data.collections['Collection'].children)))
    for i in bpy.data.collections['Collection'].children:

        row = layout.row()
        bpy.ops.tb_ops.change_active_collection
        button = self.layout.operator('tb_ops.change_active_collection',text=i.name)
        row.label(text=str(i.name))
        pass
    
class TB_COLLECTION_MANAGER_PNL(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "TB"
    bl_label = ""
    bl_idname = "TB_PNL_Collection_Manager"

    def draw_header(self,context):
        tbtool = context.scene.tb_data_tool
        layout = self.layout
        layout.label(icon='FILE_TEXT')
        layout.label(text="Data_Tool_Renamer")
    def draw (self,context):
        tbcollectionmanager(self, context)

class TB_COLLECTION_MANAGER_PNL_POP(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "context.tbcollectionmanagerpopup"
    bl_label = "Data Renamer"
    @classmethod
    def poll(cls, context):
        return context.object is not None
    def invoke(self, context, event):
        widthsize = 500     
        return context.window_manager.invoke_props_dialog(self,width = widthsize)        
    def draw(self, context):
        tbdatarenamer(self, context)
    def execute(self, context):
        return {'FINISHED'}

classes = (
    TB_E_Properties,
    TB_CHANGE_COLLECTION_MANAGER,
    TB_COLLECTION_MANAGER_PNL,
    TB_COLLECTION_MANAGER_PNL_POP,
    )
addon_keymaps = []         



def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        bpy.types.Scene.tb_data_tool = bpy.props.PointerProperty(type= TB_E_Properties)
 #KEYMAP
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
     #VIEW3D        
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new("context.tbcollectionmanagerpopup", 'C', 'PRESS', alt=True, ctrl=False, shift=False)
        kmi.active = True
        addon_keymaps.append((km, kmi))


def unregister():
 #CLASSES
    for cls in classes:
        bpy.utils.unregister_class(cls)
        bpy.types.Scene.tb_data_tool
 #KEYMAP
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()        
if __name__ == "__main__":
    register()
