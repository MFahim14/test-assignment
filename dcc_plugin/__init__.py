bl_info = {
    "name": "DCC Plugin",
    "blender": (4, 3, 2),
    "category": "Object",
    "author": "Mohammed Fahim A",
    "version": (1, 0),
    "location": "View3D > Sidebar > DCC Plugin",
    "description": "Send object transformation data to a Flask server",
    "support": "COMMUNITY"
}

import bpy
from .operators import (
    TransformOperator, TranslationOperator, RotationOperator, ScaleOperator,
    AddItemOperator, RemoveItemOperator, UpdateItemOperator
)
from .ui import DCC_PT_Panel  # Import the UI panel

classes = [
    TransformOperator, TranslationOperator, RotationOperator, ScaleOperator,
    AddItemOperator, RemoveItemOperator, UpdateItemOperator,
    DCC_PT_Panel  # Register the UI panel
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
