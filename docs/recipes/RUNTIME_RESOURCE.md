# How to add runtime configuration Resources in Godot 4.7

**Use when:** your addon needs user-editable data consumed by gameplay logic, not editor UI.

## File to create

- `addons/pooling/src/pooling_config.gd`

```gdscript
extends Resource
class_name PoolingConfig

@export var enabled: bool = true
@export_range(0.0, 1.0, 0.05) var intensity: float = 0.5
```

This runtime script does **not** require modifying `plugin.gd`, adding a dock or calling editor APIs. A `Resource` can be saved to a `.tres` file and reused in scenes. Use a distinctive `class_name` to avoid namespace conflicts, especially if publishing multiple addons.

## Verify

1. Create a new Resource using **PoolingConfig** in the Inspector.
2. Save it as a `.tres`, reopen it and confirm the properties persist.
3. Copy only `addons/pooling/` into a clean project and repeat.

Reference: [Resources](https://docs.godotengine.org/en/4.7/tutorials/scripting/resources.html).
