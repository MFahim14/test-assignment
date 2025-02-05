import bpy

class DCC_PT_Panel(bpy.types.Panel):
    """Creates a Panel in the 3D Viewport sidebar"""
    bl_label = "DCC Plugin"
    bl_idname = "DCC_PT_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "DCC Plugin"

    def draw(self, context):
        layout = self.layout
        layout.operator("object.apply_transform", text="Apply Transform")
        layout.operator("object.apply_translation", text="Apply Translation")
        layout.operator("object.apply_rotation", text="Apply Rotation")
        layout.operator("object.apply_scale", text="Apply Scale")
        # layout.separator()
        # layout.operator("object.add_item", text="Add Item")
        # layout.operator("object.remove_item", text="Remove Item")
        # layout.operator("object.update_item", text="Update Item")
        
# Blender Registration
def register():
    bpy.utils.register_class(DCC_PT_Panel)

def unregister():
    bpy.utils.unregister_class(DCC_PT_Panel)
