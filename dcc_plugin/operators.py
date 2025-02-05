import bpy
import requests

FLASK_SERVER_URL = "http://127.0.0.1:5000"  # Update if hosted elsewhere

def send_request(endpoint, data):
    """Sends a request to the Flask server."""
    url = f"{FLASK_SERVER_URL}/{endpoint}"
    try:
        response = requests.post(url, json=data)
        print(f"Response from {endpoint}: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send request: {e}")

def get_active_object():
    """Returns the active Blender object."""
    obj = bpy.context.active_object
    if obj is None:
        print("No active object selected.")
    return obj

def refresh_ui():
    """Forces Blender's UI to update."""
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

# ===========================
#   Transformation Operators
# ===========================
class TransformOperator(bpy.types.Operator):
    """Send Transform Data"""
    bl_idname = "object.apply_transform"
    bl_label = "Apply Transform"

    def execute(self, context):
        obj = get_active_object()
        if not obj:
            return {'CANCELLED'}
        
        transform_data = {
            "position": list(obj.location),
            "rotation": list(obj.rotation_euler),
            "scale": list(obj.scale)
        }
        
        send_request("transform", transform_data)
        refresh_ui()
        return {'FINISHED'}

class TranslationOperator(bpy.types.Operator):
    """Send Position Data"""
    bl_idname = "object.apply_translation"
    bl_label = "Apply Translation"

    def execute(self, context):
        obj = get_active_object()
        if not obj:
            return {'CANCELLED'}
        
        send_request("translation", {"translation": list(obj.location)})
        refresh_ui()
        return {'FINISHED'}

class RotationOperator(bpy.types.Operator):
    """Send Rotation Data"""
    bl_idname = "object.apply_rotation"
    bl_label = "Apply Rotation"

    def execute(self, context):
        obj = get_active_object()
        if not obj:
            return {'CANCELLED'}
        
        send_request("rotation", {"rotation": list(obj.rotation_euler)})
        refresh_ui()
        return {'FINISHED'}

class ScaleOperator(bpy.types.Operator):
    """Send Scale Data"""
    bl_idname = "object.apply_scale"
    bl_label = "Apply Scale"

    def execute(self, context):
        obj = get_active_object()
        if not obj:
            return {'CANCELLED'}
        
        send_request("scale", {"scale": list(obj.scale)})
        refresh_ui()
        return {'FINISHED'}

# ===========================
#   Inventory Management Operators
# ===========================
class AddItemOperator(bpy.types.Operator):
    """Send Add Item Request"""
    bl_idname = "object.add_item"
    bl_label = "Add Item"

    def execute(self, context):
        obj = get_active_object()
        if not obj:
            return {'CANCELLED'}

        send_request("add_item", {"name": obj.name, "position": list(obj.location)})
        refresh_ui()
        return {'FINISHED'}

class RemoveItemOperator(bpy.types.Operator):
    """Send Remove Item Request"""
    bl_idname = "object.remove_item"
    bl_label = "Remove Item"

    def execute(self, context):
        obj = get_active_object()
        if not obj:
            return {'CANCELLED'}
        
        send_request("remove_item", {"name": obj.name})
        refresh_ui()
        return {'FINISHED'}

class UpdateItemOperator(bpy.types.Operator):
    """Send Update Item Request"""
    bl_idname = "object.update_item"
    bl_label = "Update Item"

    def execute(self, context):
        obj = get_active_object()
        if not obj:
            return {'CANCELLED'}
        
        send_request("update_item", {"name": obj.name, "position": list(obj.location)})
        refresh_ui()
        return {'FINISHED'}

# ===========================
#   Blender Registration
# ===========================
def register():
    bpy.utils.register_class(TransformOperator)
    bpy.utils.register_class(TranslationOperator)
    bpy.utils.register_class(RotationOperator)
    bpy.utils.register_class(ScaleOperator)
    bpy.utils.register_class(AddItemOperator)
    bpy.utils.register_class(RemoveItemOperator)
    bpy.utils.register_class(UpdateItemOperator)

def unregister():
    bpy.utils.unregister_class(TransformOperator)
    bpy.utils.unregister_class(TranslationOperator)
    bpy.utils.unregister_class(RotationOperator)
    bpy.utils.unregister_class(ScaleOperator)
    bpy.utils.unregister_class(AddItemOperator)
    bpy.utils.unregister_class(RemoveItemOperator)
    bpy.utils.unregister_class(UpdateItemOperator)

if __name__ == "__main__":
    register()
