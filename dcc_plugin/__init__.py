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
    TransformOperator, TranslationOperator, RotationOperator, ScaleOperator
)
from .ui import DCC_PT_Panel  # Import the UI panel

classes = [
    TransformOperator, TranslationOperator, RotationOperator, ScaleOperator,
    DCC_PT_Panel  # Add UI panel here
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
