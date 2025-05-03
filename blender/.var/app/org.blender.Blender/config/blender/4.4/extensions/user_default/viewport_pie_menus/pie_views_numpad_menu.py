# SPDX-FileCopyrightText: 2016-2022 Blender Foundation
#
# SPDX-License-Identifier: GPL-2.0-or-later


import bpy
from bpy.types import (
    Menu,
    Operator,
)
from .hotkeys import register_hotkey


# Lock Camera Transforms
class PIE_OT_LockTransforms(Operator):
    bl_idname = "object.locktransforms"
    bl_label = "Lock Object Transforms"
    bl_description = (
        "Enable or disable the editing of objects transforms in the 3D View\n"
        "Needs an existing Active Object"
    )
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        obj = context.active_object
        if obj.lock_rotation[0] is False:
            obj.lock_rotation[0] = True
            obj.lock_rotation[1] = True
            obj.lock_rotation[2] = True
            obj.lock_scale[0] = True
            obj.lock_scale[1] = True
            obj.lock_scale[2] = True

        elif context.object.lock_rotation[0] is True:
            obj.lock_rotation[0] = False
            obj.lock_rotation[1] = False
            obj.lock_rotation[2] = False
            obj.lock_scale[0] = False
            obj.lock_scale[1] = False
            obj.lock_scale[2] = False

        return {'FINISHED'}


# Pie views numpad - Q
class PIE_MT_ViewNumpad(Menu):
    bl_idname = "PIE_MT_viewnumpad"
    bl_label = "Views Pie"

    def draw(self, context):
        layout = self.layout
        ob = context.active_object
        pie = layout.menu_pie()
        scene = context.scene
        rd = scene.render

        # 4 - LEFT
        pie.operator("view3d.view_axis", text="Left", icon='TRIA_LEFT').type = 'LEFT'
        # 6 - RIGHT
        pie.operator("view3d.view_axis", text="Right", icon='TRIA_RIGHT').type = 'RIGHT'
        # 2 - BOTTOM
        pie.operator("view3d.view_axis", text="Bottom", icon='TRIA_DOWN').type = (
            'BOTTOM'
        )
        # 8 - TOP
        pie.operator("view3d.view_axis", text="Top", icon='TRIA_UP').type = 'TOP'
        # 7 - TOP - LEFT
        pie.operator("view3d.view_axis", text="Back").type = 'BACK'
        # 9 - TOP - RIGHT
        pie.operator("view3d.view_axis", text="Front").type = 'FRONT'
        # 1 - BOTTOM - LEFT
        box = pie.split().column()

        row = box.row(align=True)
        row.operator("view3d.view_camera", text="View Cam", icon='HIDE_OFF')
        row.operator("view3d.camera_to_view", text="Cam To View", icon='NONE')

        row = box.row(align=True)
        if context.space_data.lock_camera is False:
            row.operator(
                "wm.context_toggle", text="Lock Cam To View", icon='UNLOCKED'
            ).data_path = "space_data.lock_camera"
        elif context.space_data.lock_camera is True:
            row.operator(
                "wm.context_toggle", text="Lock Cam to View", icon='LOCKED'
            ).data_path = "space_data.lock_camera"

        icon_locked = (
            'LOCKED'
            if ob and ob.lock_rotation[0] is False
            else 'UNLOCKED' if ob and ob.lock_rotation[0] is True else 'LOCKED'
        )

        row = box.row(align=True)
        row.operator("object.locktransforms", text="Lock Transforms", icon=icon_locked)

        row = box.row(align=True)
        row.prop(rd, "use_border", text="Border")
        # 3 - BOTTOM - RIGHT
        box = pie.split().column()

        row = box.row(align=True)
        row.operator("view3d.view_all").center = True
        row.operator("view3d.view_selected", text="Selected")

        row = box.row(align=True)
        row.operator("view3d.view_persportho", text="Persp/Ortho")
        row.operator("view3d.localview", text="Local/Global")

        row = box.row(align=True)
        row.operator("screen.region_quadview", text="Toggle Quad")
        row.operator("screen.screen_full_area", text="Toggle Full")


registry = (
    PIE_MT_ViewNumpad,
    PIE_OT_LockTransforms,
)


def register():
    register_hotkey(
        'wm.call_menu_pie',
        op_kwargs={'name': 'PIE_MT_viewnumpad'},
        hotkey_kwargs={'type': "Q", 'value': "PRESS", 'alt': True},
        key_cat="3D View",
    )
