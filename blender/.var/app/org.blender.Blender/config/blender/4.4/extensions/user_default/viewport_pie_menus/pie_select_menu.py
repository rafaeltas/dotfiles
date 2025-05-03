# SPDX-FileCopyrightText: 2016-2022 Blender Foundation
#
# SPDX-License-Identifier: GPL-2.0-or-later

import bpy
from bpy.types import Menu, Operator
from .hotkeys import register_hotkey


# Pie Selection Object Mode - A
class PIE_MT_SelectionsMore(Menu):
    bl_idname = "PIE_MT_selectionsmore"
    bl_label = "Selection Pie"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        box = pie.split().column()
        box.operator("object.select_random", text="Select Random")
        box.operator("object.select_linked", text="Select Linked")
        box.separator()

        box.operator("object.select_more", text="More")
        box.operator("object.select_less", text="Less")
        box.separator()

        props = box.operator("object.select_hierarchy", text="Parent")
        props.extend = False
        props.direction = 'PARENT'

        props = box.operator("object.select_hierarchy", text="Child")
        props.extend = False
        props.direction = 'CHILD'
        box.separator()

        props = box.operator("object.select_hierarchy", text="Extend Parent")
        props.extend = True
        props.direction = 'PARENT'

        props = box.operator("object.select_hierarchy", text="Extend Child")
        props.extend = True
        props.direction = 'CHILD'


# Pie Selection Object Mode - A


class PIE_MT_SelectionsOM(Menu):
    bl_idname = "PIE_MT_selectionsom"
    bl_label = "Selection Pie"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        # 4 - LEFT
        pie.operator("object.select_grouped", text="Select Grouped")
        # 6 - RIGHT
        pie.operator("object.select_by_type", text="Select By Type")
        # 2 - BOTTOM
        pie.operator(
            "object.select_all", text="Invert Selection", icon='ZOOM_PREVIOUS'
        ).action = 'INVERT'
        # 8 - TOP
        pie.operator(
            "object.select_all", text="Select All Toggle", icon='NONE'
        ).action = 'TOGGLE'
        # 7 - TOP - LEFT
        pie.operator("view3d.select_circle", text="Circle Select")
        # 9 - TOP - RIGHT
        pie.operator("view3d.select_box", text="Box Select")
        # 1 - BOTTOM - LEFT
        pie.operator("object.select_camera", text="Select Camera")
        # 3 - BOTTOM - RIGHT
        pie.menu("PIE_MT_selectionsmore", text="Select Menu")


# Pie Selection Edit Mode
class PIE_MT_SelectionsEM(Menu):
    bl_idname = "PIE_MT_selectionsem"
    bl_label = "Pie Selections Edit Mode"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        # 4 - LEFT
        pie.operator("mesh.select_less", text="Select Less")
        # 6 - RIGHT
        pie.operator("mesh.select_more", text="Select More")
        # 2 - BOTTOM
        pie.menu("OBJECT_MT_selectloopselection", text="Select Loop Menu")
        # 8 - TOP
        pie.operator("mesh.select_all", text="Select All Toggle").action = 'TOGGLE'
        # 7 - TOP - LEFT
        pie.operator("view3d.select_circle", text="Circle Select")
        # 9 - TOP - RIGHT
        pie.operator("view3d.select_box", text="Box Select")
        # 1 - BOTTOM - LEFT
        pie.operator("mesh.select_all", text="Invert Selection").action = 'INVERT'
        # 3 - BOTTOM - RIGHT
        pie.menu("PIE_MT_selectallbyselection", text="Edit Modes", icon='VERTEXSEL')


# Select All By Selection
class PIE_MT_SelectAllBySelection(Menu):
    bl_idname = "PIE_MT_selectallbyselection"
    bl_label = "Verts Edges Faces"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        box = pie.split().column()

        box.operator("class.vertexop", text="Vertex", icon='VERTEXSEL')
        box.operator("class.edgeop", text="Edge", icon='EDGESEL')
        box.operator("class.faceop", text="Face", icon='FACESEL')
        box.operator(
            "verts.edgesfacesop", text="Vertex/Edges/Faces", icon='OBJECT_DATAMODE'
        )


# Edit Selection Modes
class PIE_OT_classvertexop(Operator):
    bl_idname = "class.vertexop"
    bl_label = "Class Vertex"
    bl_description = "Vert Select Mode"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
        if bpy.ops.mesh.select_mode != "EDGE, FACE":
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
            return {'FINISHED'}


class PIE_OT_classedgeop(Operator):
    bl_idname = "class.edgeop"
    bl_label = "Class Edge"
    bl_description = "Edge Select Mode"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE')
        if bpy.ops.mesh.select_mode != "VERT, FACE":
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE')
            return {'FINISHED'}


class PIE_OT_classfaceop(Operator):
    bl_idname = "class.faceop"
    bl_label = "Class Face"
    bl_description = "Face Select Mode"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
        if bpy.ops.mesh.select_mode != "VERT, EDGE":
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
            return {'FINISHED'}


# Combined Selection Mode
class PIE_OT_vertsedgesfacesop(Operator):
    bl_idname = "verts.edgesfacesop"
    bl_label = "Verts Edges Faces"
    bl_description = "Vert/Edge/Face Select Mode"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.object.mode != "EDIT":
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
        if bpy.ops.mesh.select_mode != "VERT, EDGE, FACE":
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
            bpy.ops.mesh.select_mode(use_extend=True, use_expand=False, type='EDGE')
            bpy.ops.mesh.select_mode(use_extend=True, use_expand=False, type='FACE')
            return {'FINISHED'}


class PIE_MT_SelectLoopSelection(Menu):
    bl_idname = "OBJECT_MT_selectloopselection"
    bl_label = "Verts Edges Faces"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'

        layout.operator(
            "mesh.loop_multi_select", text="Select Loop", icon='NONE'
        ).ring = False
        layout.operator(
            "mesh.loop_multi_select", text="Select Ring", icon='NONE'
        ).ring = True
        layout.operator(
            "mesh.loop_to_region", text="Select Loop Inner Region", icon='NONE'
        )


registry = (
    PIE_MT_SelectionsOM,
    PIE_MT_SelectionsEM,
    PIE_MT_SelectAllBySelection,
    PIE_MT_SelectionsMore,
    PIE_MT_SelectLoopSelection,
    PIE_OT_classvertexop,
    PIE_OT_classedgeop,
    PIE_OT_classfaceop,
    PIE_OT_vertsedgesfacesop,
)


def register():
    register_hotkey(
        'wm.call_menu_pie',
        op_kwargs={'name': 'PIE_MT_selectionsom'},
        hotkey_kwargs={'type': "A", 'value': "PRESS"},
        key_cat="Object Mode",
    )
    register_hotkey(
        'wm.call_menu_pie',
        op_kwargs={'name': 'PIE_MT_selectionsem'},
        hotkey_kwargs={'type': "A", 'value': "PRESS"},
        key_cat="Mesh",
    )
