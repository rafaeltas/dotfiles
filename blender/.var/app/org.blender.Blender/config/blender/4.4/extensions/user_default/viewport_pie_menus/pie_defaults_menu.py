# SPDX-FileCopyrightText: 2016-2022 Blender Foundation
#
# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from bpy.types import Menu
from .hotkeys import register_hotkey


# Save/Open Pie
class PIE_MT_Load_Defaults(Menu):
    bl_idname = "PIE_MT_loaddefaults"
    bl_label = "Defaults Pie"

    def draw(self, context):
        layout = self.layout
        prefs = context.preferences
        pie = layout.menu_pie()
        # 4 - LEFT
        pie.operator(
            "wm.read_factory_settings", text="Load Factory Settings", icon='IMPORT'
        )
        # 6 - RIGHT
        pie.operator(
            "wm.read_factory_userpref",
            text="Load Factory Preferences",
            icon='RECOVER_LAST',
        )
        # 2 - BOTTOM
        pie.operator("wm.read_userpref", text="Revert to Saved Prefs", icon='NONE')
        # 8 - TOP
        pie.operator("wm.save_homefile", text="Save StartUp File", icon='FILE_NEW')
        # 7 - TOP - LEFT
        pie.prop(
            prefs,
            "use_preferences_save",
            text="Auto-Save Preferences",
            icon='LINK_BLEND',
        )
        # 9 - TOP - RIGHT
        pie.operator("wm.save_userpref", text="Save User Preferences", icon='NONE')
        # 1 - BOTTOM - LEFT
        pie.separator()
        # 3 - BOTTOM - RIGHT
        pie.separator()


registry = (PIE_MT_Load_Defaults,)


def register():
    register_hotkey(
        'wm.call_menu_pie',
        op_kwargs={'name': 'PIE_MT_loaddefaults'},
        hotkey_kwargs={'type': "U", 'value': "PRESS", 'ctrl': True},
        key_cat="Window",
    )
