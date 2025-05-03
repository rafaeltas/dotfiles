# SPDX-FileCopyrightText: 2016-2022 Blender Foundation
#
# SPDX-License-Identifier: GPL-2.0-or-later


import bpy
from bpy.types import (
    Menu,
    Operator,
)
from bpy.props import (
    BoolProperty,
    EnumProperty,
)
from .hotkeys import register_hotkey


class PIE_OT_WManupulators(Operator):
    bl_idname = "w.manipulators"
    bl_label = "W Manupulators"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = " Show/Hide Manipulator"

    extend: BoolProperty(
        default=False,
    )
    type: EnumProperty(
        items=(
            ('TRANSLATE', "Move", ""),
            ('ROTATE', "Rotate", ""),
            ('SCALE', "Scale", ""),
        )
    )

    def execute(self, context):
        space_data = context.space_data
        space_data.show_gizmo_context = True

        attrs = (
            "show_gizmo_object_translate",
            "show_gizmo_object_rotate",
            "show_gizmo_object_scale",
        )
        attr_t, attr_r, attr_s = attrs
        attr_index = ('TRANSLATE', 'ROTATE', 'SCALE').index(self.type)
        attr_active = attrs[attr_index]

        if self.extend:
            setattr(space_data, attr_active, not getattr(space_data, attr_active))
        else:
            for attr in attrs:
                setattr(space_data, attr, attr == attr_active)
        return {'FINISHED'}

    def invoke(self, context, event):
        self.extend = event.shift
        return self.execute(context)


class PIE_MT_Manipulator(Menu):
    bl_idname = "PIE_MT_manipulator"
    bl_label = "Manipulator Pie"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        # 4 - LEFT
        pie.operator("w.manipulators", text="Rotate", icon='NONE').type = 'ROTATE'
        # 6 - RIGHT
        pie.operator("w.manipulators", text="Scale", icon='NONE').type = 'SCALE'
        # 2 - BOTTOM
        props = pie.operator("wm.context_toggle", text="Show/Hide Toggle", icon='NONE')
        props.data_path = "space_data.show_gizmo"
        # 8 - TOP
        pie.operator("w.manipulators", text="Translate", icon='NONE').type = 'TRANSLATE'


registry = (
    PIE_OT_WManupulators,
    PIE_MT_Manipulator,
)


def register():
    register_hotkey(
        'wm.call_menu_pie',
        op_kwargs={'name': 'PIE_MT_manipulator'},
        hotkey_kwargs={'type': "SPACE", 'value': "PRESS", 'alt': True},
        key_cat="3D View",
    )
