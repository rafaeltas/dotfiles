# SPDX-FileCopyrightText: 2016-2022 Blender Foundation
#
# SPDX-License-Identifier: GPL-2.0-or-later

import os
import bpy
from bpy.types import Menu
from pathlib import Path
from .hotkeys import register_hotkey


# Sculpt Pie Pie Menus - W
class PIE_MT_sculpt_brush_select(Menu):
    bl_idname = "PIE_MT_sculpt_brush_select"
    bl_label = "Sculpt Pie"

    def draw(self, context):
        global brush_icons
        layout = self.layout
        pie = layout.menu_pie()
        pie.scale_y = 1.2

        # 4 - LEFT
        draw_brush_operator(pie, 'Crease', 'crease')
        # 6 - RIGHT
        draw_brush_operator(pie, 'Blob', 'blob')
        # 2 - BOTTOM
        pie.menu(PIE_MT_sculpt_brush_select_misc.bl_idname, text="More Brushes")
        # 8 - TOP
        draw_brush_operator(pie, 'Draw', 'draw')
        # 7 - TOP - LEFT
        draw_brush_operator(pie, 'Clay', 'clay')
        # 9 - TOP - RIGHT
        draw_brush_operator(pie, 'Clay Strips', 'clay_strips')
        # 1 - BOTTOM - LEFT
        draw_brush_operator(pie, 'Inflate/Deflate', 'inflate')
        # 3 - BOTTOM - RIGHT
        pie.menu(
            PIE_MT_sculpt_brush_select_grab.bl_idname,
            text="    Grab Brushes",
            icon_value=brush_icons["grab"],
        )


# Sculpt Pie 2
class PIE_MT_sculpt_brush_select_misc(Menu):
    bl_idname = "PIE_MT_sculpt_brush_select_misc"
    bl_label = "More Brushes"

    def draw(self, context):
        global brush_icons
        layout = self.layout
        layout.scale_y = 1.5

        # 4 - LEFT
        draw_brush_operator(layout, 'Smooth', 'smooth')
        # 6 - RIGHT
        draw_brush_operator(layout, 'Flatten/Contrast', 'flatten')
        # 2 - BOTTOM
        draw_brush_operator(layout, 'Scrape/Fill', 'scrape')
        # 8 - TOP
        draw_brush_operator(layout, 'Fill/Deepen', 'fill')
        # 7 - TOP - LEFT
        draw_brush_operator(layout, 'Pinch/Magnify', 'pinch')
        # 9 - TOP - RIGHT
        draw_brush_operator(layout, 'Layer', 'layer')
        # 1 - BOTTOM - LEFT
        draw_brush_operator(layout, 'Mask', 'mask')
        # 3 - BOTTOM - RIGHT


# Sculpt Pie Three
class PIE_MT_sculpt_brush_select_grab(Menu):
    bl_idname = "PIE_MT_sculpt_brush_select_grab"
    bl_label = "Grab Brushes"

    def draw(self, context):
        global brush_icons
        layout = self.layout
        layout.scale_y = 1.5

        # 4 - LEFT
        draw_brush_operator(layout, 'Grab', 'grab')
        # 6 - RIGHT
        draw_brush_operator(layout, 'Nudge', 'nudge')
        # 2 - BOTTOM
        draw_brush_operator(layout, 'Thumb', 'thumb')
        # 8 - TOP
        draw_brush_operator(layout, 'Snake Hook', 'snake_hook')
        # 7 - TOP - LEFT
        draw_brush_operator(layout, 'Twist', 'rotate')


def draw_brush_operator(layout, brush_name: str, brush_icon: str):
    """Draw a brush select operator in the provided UI element with the pre-4.3 icons.
    brush_name must match the name of the Brush Asset.
    brush_icon must match the name of a file in this add-on's icons folder.
    """
    if 'asset_activate' in dir(bpy.ops.brush):
        # 4.3
        op = layout.operator(
            'brush.asset_activate',
            text="     " + brush_name,
            icon_value=brush_icons[brush_icon],
        )
        op.asset_library_type = 'ESSENTIALS'
        op.relative_asset_identifier = (
            os.path.join("brushes", "essentials_brushes.blend", "Brush", brush_name)
        )
    else:
        # Pre-4.3
        op = layout.operator(
            "paint.brush_select",
            text="     " + brush_name,
            icon_value=brush_icons[brush_icon],
        )
        op.sculpt_tool = brush_icon.upper()


brush_icons = {}


def create_icons():
    global brush_icons
    icons_directory = Path(__file__).parent / "icons"

    for icon_path in icons_directory.iterdir():
        icon_value = bpy.app.icons.new_triangles_from_file(icon_path.as_posix())
        brush_name = icon_path.stem.split(".")[-1]
        brush_icons[brush_name] = icon_value


def release_icons():
    global brush_icons
    for value in brush_icons.values():
        bpy.app.icons.release(value)


registry = (
    PIE_MT_sculpt_brush_select,
    PIE_MT_sculpt_brush_select_misc,
    PIE_MT_sculpt_brush_select_grab,
)


def register():
    create_icons()

    register_hotkey(
        'wm.call_menu_pie',
        op_kwargs={'name': 'PIE_MT_sculpt_brush_select'},
        hotkey_kwargs={'type': "W", 'value': "PRESS"},
        key_cat="Sculpt",
    )


def unregister():
    release_icons()
