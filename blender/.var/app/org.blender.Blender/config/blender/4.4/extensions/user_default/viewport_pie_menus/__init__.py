# SPDX-FileCopyrightText: 2016-2022 Blender Foundation
#
# SPDX-License-Identifier: GPL-2.0-or-later

bl_info = {
    "name":"3D Viewport Pie Menus",
    "description": "A set of handy pie menus to enhance various workflows",
    "author": "pitiwazou, meta-androcto, Demeter Dzadik",
    "version": (1, 3, 2),
    "blender": (3, 0, 0),
    "location": "See Add-on Preferences for shortcut list",
    "warning": "",
    "doc_url": "",
    'tracker_url': "https://projects.blender.org/extensions/space_view3d_pie_menus",
    'support': 'COMMUNITY',
    "category": "Modeling",
}

from bpy.utils import register_class, unregister_class
import importlib

module_names = (
    "prefs",
    "hotkeys",
    "pie_modes_menu",
    "pie_views_numpad_menu",
    "pie_sculpt_menu",
    "pie_origin",
    "pie_manipulator_menu",
    "pie_shading_menu",
    "pie_align_menu",
    "pie_delete_menu",
    "pie_apply_transform_menu",
    "pie_select_menu",
    "pie_animation_menu",
    "pie_save_open_menu",
    "pie_editor_switch_menu",
    "pie_defaults_menu",
    "pie_proportional_menu",
)


modules = [
    __import__(__package__ + "." + submod, {}, {}, submod)
    for submod in module_names
]


def register_unregister_modules(modules: list, register: bool):
    """Recursively register or unregister modules by looking for either
    un/register() functions or lists named `registry` which should be a list of
    registerable classes.
    """
    register_func = register_class if register else unregister_class
    un = 'un' if not register else ''

    for m in modules:
        if register:
            importlib.reload(m)
        if hasattr(m, 'registry'):
            for c in m.registry:
                try:
                    register_func(c)
                except Exception as e:
                    print(
                        f"Warning: Pie Menus failed to {un}register class: {c.__name__}"
                    )
                    print(e)

        if hasattr(m, 'modules'):
            register_unregister_modules(m.modules, register)

        if register and hasattr(m, 'register'):
            m.register()
        elif hasattr(m, 'unregister'):
            m.unregister()


def register():
    register_unregister_modules(modules, True)


def unregister():
    register_unregister_modules(reversed(modules), False)
