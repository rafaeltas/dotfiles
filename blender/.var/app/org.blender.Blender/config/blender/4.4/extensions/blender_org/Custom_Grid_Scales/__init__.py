bl_info = {
    "name": "Custom Grid Scales",
    "blender": (4, 2, 1),
    "category": "3D View",
}

import bpy
import rna_keymap_ui 

addon_keymaps = []

class AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        col = box.column()
        col.label(text="Keymap List:", icon="KEYINGSET")

        wm = bpy.context.window_manager
        kc = wm.keyconfigs.addon
        old_km_name = ""
        get_kmi_l = []
        for km_add, kmi_add in addon_keymaps:
            for km_con in kc.keymaps:
                if km_add.name == km_con.name:
                    km = km_con
                    break

            for kmi_con in km.keymap_items:
                if kmi_add.idname == kmi_con.idname:
                    if kmi_add.name == kmi_con.name:
                        get_kmi_l.append((km, kmi_con))

        get_kmi_l = sorted(set(get_kmi_l), key=get_kmi_l.index)

        for km, kmi in get_kmi_l:
            if not km.name == old_km_name:
                col.label(text=str(km.name), icon="DOT")
            col.context_pointer_set("keymap", km)
            rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
            col.separator()
            old_km_name = km.name


# Property to store grid scale as an item in a collection
class GridScaleItem(bpy.types.PropertyGroup):
    scale: bpy.props.FloatProperty(
        name="Scale",
        description="Grid scale value",
        default=1.0,
        min=0.001,
        max=100.0
    )

# Property to manage the collection of grid scales
class GridScaleProperties(bpy.types.PropertyGroup):
    current_scale_index: bpy.props.IntProperty(
        name="Current Grid Scale Index",
        default=0,
        min=0,
        max=100  # Arbitrary large number to allow more scales
    )
    
    grid_scales: bpy.props.CollectionProperty(type=GridScaleItem)
    custom_scale: bpy.props.FloatProperty(
        name="Custom Scale",
        description="Add a custom grid scale increment",
        default=1.0,
        min=0.001,
        max=100.0
    )

# Function to update the grid scale and show a message in the status bar
def update_grid_scale(self, context):
    props = context.scene.grid_scale_properties
    index = props.current_scale_index
    if index < len(props.grid_scales):
        scale_value = props.grid_scales[index].scale
        bpy.context.space_data.overlay.grid_scale = scale_value
        self.report({'INFO'}, f"Grid Scale set to {scale_value}")

# Operator to cycle through grid scales
class VIEW3D_OT_grid_scale_cycle(bpy.types.Operator):
    bl_idname = "view3d.grid_scale_cycle"
    bl_label = "Cycle Grid Scale"
    
    direction: bpy.props.EnumProperty(
        items=[
            ('UP', "Up", "Increase grid scale"),
            ('DOWN', "Down", "Decrease grid scale")
        ]
    )
    
    def execute(self, context):
        props = context.scene.grid_scale_properties
        if self.direction == 'UP':
            props.current_scale_index = min(props.current_scale_index + 1, len(props.grid_scales) - 1)
        else:
            props.current_scale_index = max(props.current_scale_index - 1, 0)
        update_grid_scale(self, context)
        return {'FINISHED'}

# Operator to add a custom scale to the list
class VIEW3D_OT_add_custom_grid_scale(bpy.types.Operator):
    bl_idname = "view3d.add_custom_grid_scale"
    bl_label = "Add Custom Grid Scale"
    
    def execute(self, context):
        props = context.scene.grid_scale_properties
        new_scale = props.grid_scales.add()
        new_scale.scale = props.custom_scale
        props.current_scale_index = len(props.grid_scales) - 1  # Set to newly added scale
        update_grid_scale(self, context)
        return {'FINISHED'}

# Operator to remove a selected scale from the list
class VIEW3D_OT_remove_grid_scale(bpy.types.Operator):
    bl_idname = "view3d.remove_grid_scale"
    bl_label = "Remove Grid Scale"
    
    index: bpy.props.IntProperty()
    
    def execute(self, context):
        props = context.scene.grid_scale_properties
        if 0 <= self.index < len(props.grid_scales):
            props.grid_scales.remove(self.index)
            props.current_scale_index = min(props.current_scale_index, len(props.grid_scales) - 1)
            if props.grid_scales:
                update_grid_scale(self, context)
        return {'FINISHED'}
        
# Extend the Viewport Overlays panel
class VIEW3D_PT_overlay_grid_scale(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'HEADER'
    bl_label = "Grid Scale List"
    bl_parent_id = 'VIEW3D_PT_overlay'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        props = context.scene.grid_scale_properties
        
        for i, scale_item in enumerate(props.grid_scales):
            row = layout.row(align=True)
            row.prop(scale_item, "scale", text="")
            op = row.operator("view3d.remove_grid_scale", text="", icon="REMOVE")
            op.index = i

#        # Add controls for custom scale
        row = layout.row(align=True)
        row.prop(props, "custom_scale", text="")
        row.operator("view3d.add_custom_grid_scale", text="Add")

# Register and Unregister classes
classes = [
    AddonPreferences,
    GridScaleItem,
    GridScaleProperties,
    VIEW3D_OT_grid_scale_cycle,
    VIEW3D_OT_add_custom_grid_scale,
    VIEW3D_OT_remove_grid_scale,
    VIEW3D_PT_overlay_grid_scale,
]



def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.grid_scale_properties = bpy.props.PointerProperty(type=GridScaleProperties)
    
    # Add keymap entries for the bracket keys
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
    
    kmi = km.keymap_items.new("view3d.grid_scale_cycle", 'LEFT_BRACKET', 'PRESS')
    kmi.properties.direction = 'DOWN'
    
    kmi = km.keymap_items.new("view3d.grid_scale_cycle", 'RIGHT_BRACKET', 'PRESS')
    kmi.properties.direction = 'UP'
    
    addon_keymaps.append((km, kmi))

def unregister():
    # Remove keymaps
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.grid_scale_properties

if __name__ == "__main__":
    register()