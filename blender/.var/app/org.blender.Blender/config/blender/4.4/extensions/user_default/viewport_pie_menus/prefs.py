
from bpy.types import AddonPreferences
from .hotkeys import draw_hotkey_list

class ExtraPies_AddonPrefs(AddonPreferences):
    bl_idname = __package__

    keymap_items = {}

    def draw(self, context):
        draw_hotkey_list(self.layout.column(), context)

registry = [
    ExtraPies_AddonPrefs,
]
