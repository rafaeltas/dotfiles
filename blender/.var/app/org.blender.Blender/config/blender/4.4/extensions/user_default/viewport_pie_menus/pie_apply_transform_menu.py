# SPDX-FileCopyrightText: 2016-2022 Blender Foundation
#
# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from bpy.types import (
    Menu,
    Operator,
)
from .hotkeys import register_hotkey


class PIE_MT_PieApplyTransforms(Menu):
    bl_idname = "PIE_MT_applytransforms"
    bl_label = "Apply Transforms Pie"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        # 4 - LEFT
        pie.operator("object.visual_transform_apply", text="Apply Visual")
        # 6 - RIGHT
        props = pie.operator("object.transform_apply", text="Apply All")
        props.location, props.rotation, props.scale = (True, True, True)
        # 2 - BOTTOM
        props = pie.operator("object.transform_apply", text="Rotation/Scale")
        props.location, props.rotation, props.scale = (False, True, True)
        # 8 - TOP
        props = pie.operator("object.transform_apply", text="Rotation")
        props.location, props.rotation, props.scale = (False, True, False)
        # 7 - TOP - LEFT
        props = pie.operator("object.transform_apply", text="Location")
        props.location, props.rotation, props.scale = (True, False, False)
        # 9 - TOP - RIGHT
        props = pie.operator("object.transform_apply", text="Scale")
        props.location, props.rotation, props.scale = (False, False, True)
        # 1 - BOTTOM - LEFT
        pie.operator("object.duplicates_make_real", text="Make Instances Real")
        # 3 - BOTTOM - RIGHT
        pie.menu("PIE_MT_clear_menu", text="Clear Transform Menu")


class PIE_MT_ClearMenu(Menu):
    bl_idname = "PIE_MT_clear_menu"
    bl_label = "Clear Transforms"

    def draw(self, context):
        layout = self.layout
        layout.operator("clear.all", text="Clear All", icon='NONE')
        layout.operator("object.location_clear", text="Clear Location", icon='NONE')
        layout.operator("object.rotation_clear", text="Clear Rotation", icon='NONE')
        layout.operator("object.scale_clear", text="Clear Scale", icon='NONE')
        layout.operator("object.origin_clear", text="Clear Origin", icon='NONE')


class PIE_OT_ClearAll(Operator):
    bl_idname = "clear.all"
    bl_label = "Clear All Transforms"
    bl_description = "Clear All Transforms"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.location_clear()
        bpy.ops.object.rotation_clear()
        bpy.ops.object.scale_clear()
        return {'FINISHED'}


registry = (
    PIE_MT_PieApplyTransforms,
    PIE_MT_ClearMenu,
    PIE_OT_ClearAll,
)


def register():
    register_hotkey(
        'wm.call_menu_pie',
        op_kwargs={'name': 'PIE_MT_applytransforms'},
        hotkey_kwargs={'type': "A", 'value': "PRESS", 'ctrl': True},
        key_cat="Object Mode",
    )
