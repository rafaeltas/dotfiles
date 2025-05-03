# SPDX-FileCopyrightText: 2016-2022 Blender Foundation
#
# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from bpy.types import Menu
from .hotkeys import register_hotkey


# Shading Pie - Z
class PIE_MT_ShadingView(Menu):
    bl_idname = "PIE_MT_shadingview"
    bl_label = "Shading Pie"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()
        pie.prop(context.space_data.shading, "type", expand=True)

        if context.active_object:
            if context.mode == 'EDIT_MESH':
                pie.operator("MESH_OT_faces_shade_smooth")
                pie.operator("MESH_OT_faces_shade_flat")
            else:
                pie.operator("OBJECT_OT_shade_smooth")
                pie.operator("OBJECT_OT_shade_flat")


registry = (
    PIE_MT_ShadingView,
)


def register():
    register_hotkey(
        'wm.call_menu_pie',
        op_kwargs={'name': 'PIE_MT_shadingview'},
        hotkey_kwargs={'type': "Z", 'value': "PRESS"},
        key_cat="3D View",
    )
