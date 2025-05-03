# SPDX-FileCopyrightText: 2016-2022 Blender Foundation
#
# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from bpy.types import (
    Menu,
    Operator,
)
from .hotkeys import register_hotkey

class PIE_MT_PieAnimation(Menu):
    bl_idname = "PIE_MT_animation"
    bl_label = "Animation Pie"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        # 4 - LEFT
        pie.operator("screen.frame_jump", text="Jump REW", icon='REW').end = False
        # 6 - RIGHT
        pie.operator("screen.frame_jump", text="Jump FF", icon='FF').end = True
        # 2 - BOTTOM
        pie.operator(
            "screen.animation_play", text="Reverse", icon='PLAY_REVERSE'
        ).reverse = True
        # 8 - TOP
        if not context.screen.is_animation_playing:  # Play / Pause
            pie.operator("screen.animation_play", text="Play", icon='PLAY')
        else:
            pie.operator("screen.animation_play", text="Stop", icon='PAUSE')
        # 7 - TOP - LEFT
        pie.operator(
            "screen.keyframe_jump", text="Previous FR", icon='PREV_KEYFRAME'
        ).next = False
        # 9 - TOP - RIGHT
        pie.operator(
            "screen.keyframe_jump", text="Next FR", icon='NEXT_KEYFRAME'
        ).next = True
        # 1 - BOTTOM - LEFT
        pie.operator("insert.autokeyframe", text="Auto Keyframe", icon='REC')
        # 3 - BOTTOM - RIGHT
        pie.menu("VIEW3D_MT_object_animation", text="Keyframe Menu", icon="KEYINGSET")


class PIE_OT_InsertAutoKeyframe(Operator):
    bl_idname = "insert.autokeyframe"
    bl_label = "Insert Auto Keyframe"
    bl_description = "Toggle Insert Auto Keyframe"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        ts = context.tool_settings

        ts.use_keyframe_insert_auto ^= 1

        for area in context.screen.areas:
            if area.type == 'TIMELINE':
                area.tag_redraw()

        return {'FINISHED'}


registry = (PIE_MT_PieAnimation, PIE_OT_InsertAutoKeyframe)


def register():
    register_hotkey(
        'wm.call_menu_pie',
        op_kwargs={'name': 'PIE_MT_animation'},
        hotkey_kwargs={'type': "SPACE", 'value': "PRESS", 'shift': True},
        key_cat="Object Mode",
    )
