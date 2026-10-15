@tool
extends RefCounted

## Optional offline recipes, intentionally separate from editor UI and runtime code.
const TOPICS = [
	{
		"title": "01 · Editor dock",
		"goal": "Build an optional panel without taking over the editor.",
		"steps": "1. Create an EditorPlugin script with @tool.\n2. Create an EditorDock and add a Control as its content.\n3. Use a side slot; avoid large minimum heights.\n4. Remove the dock in _exit_tree().",
		"code": "@tool\nextends EditorPlugin\n\nvar _dock: EditorDock\n\nfunc _enter_tree() -> void:\n    _dock = EditorDock.new()\n    _dock.title = \"My Tool\"\n    _dock.default_slot = EditorDock.DOCK_SLOT_RIGHT_BR\n    _dock.available_layouts = EditorDock.DOCK_LAYOUT_VERTICAL\n    _dock.add_child(Label.new())\n    add_dock(_dock)\n\nfunc _exit_tree() -> void:\n    remove_dock(_dock)\n    _dock.queue_free()\n",
		"verify": "Disable/re-enable the plugin and confirm no duplicate tabs or hidden Output panel.",
	},
	{
		"title": "02 · Custom node",
		"goal": "Expose a reusable Node2D type in the Create Node dialog.",
		"steps": "1. Add a Node2D script under src/.\n2. Register it in plugin.gd using add_custom_type().\n3. Unregister the exact type name on plugin shutdown.\n4. Prefer unique names to avoid collisions.",
		"code": "# addons/my_plugin/src/my_gizmo.gd:\n@tool\nextends Node2D\n\n# In plugin.gd:\nfunc _enter_tree() -> void:\n    add_custom_type(\n        \"MyGizmo\", \"Node2D\",\n        preload(\"src/my_gizmo.gd\"), null\n    )\n\nfunc _exit_tree() -> void:\n    remove_custom_type(\"MyGizmo\")\n",
		"verify": "Create the node, save a scene, disable the plugin and inspect errors.",
	},
	{
		"title": "03 · Inspector extension",
		"goal": "Add contextual controls to the Inspector for a supported object.",
		"steps": "1. Implement EditorInspectorPlugin in editor/.\n2. Restrict _can_handle() to your objects.\n3. Register/unregister its instance from plugin.gd.\n4. Free references when disabling.",
		"code": "# editor/my_inspector.gd:\n@tool\nextends EditorInspectorPlugin\n\nfunc _can_handle(object: Object) -> bool:\n    return object is Node2D\n\nfunc _parse_begin(object: Object) -> void:\n    var label := Label.new()\n    label.text = \"Inspector extension\"\n    add_custom_control(label)\n\n# plugin.gd: register in _enter_tree():\n# _inspector = preload(\"editor/my_inspector.gd\").new()\n# add_inspector_plugin(_inspector)\n# Then remove_inspector_plugin(_inspector) in _exit_tree().\n",
		"verify": "Select a supported node and confirm inspector controls disappear when disabled.",
	},
	{
		"title": "04 · Tools menu action",
		"goal": "Add a reversible one-click editor command.",
		"steps": "1. Register a named item via add_tool_menu_item().\n2. Connect a Callable to a method.\n3. Keep the callback safe if no scene is open.\n4. Remove the item in _exit_tree().",
		"code": "@tool\nextends EditorPlugin\n\nfunc _enter_tree() -> void:\n    add_tool_menu_item(\"Run My Tool\", _run_tool)\n\nfunc _exit_tree() -> void:\n    remove_tool_menu_item(\"Run My Tool\")\n\nfunc _run_tool() -> void:\n    print(\"Tool selected\")\n",
		"verify": "Confirm the command appears once in Project > Tools, then disappears on disable.",
	},
	{
		"title": "05 · Runtime resources",
		"goal": "Keep game-facing data independent from editor APIs.",
		"steps": "1. Put your runtime Resource class under src/.\n2. Use a unique class_name prefix for reusable public APIs.\n3. Expose validated @export properties.\n4. Never reference EditorPlugin in runtime scripts.",
		"code": "# addons/my_plugin/src/my_tool_config.gd\nextends Resource\nclass_name MyToolConfig\n\n@export var enabled: bool = true\n@export_range(0.0, 1.0) var strength: float = 0.5\n",
		"verify": "Create a .tres resource in a clean Godot project containing only the addon.",
	},
	{
		"title": "06 · Tests and release",
		"goal": "Catch import failures and package only distributable files.",
		"steps": "1. Add a SceneTree smoke script under tests/.\n2. Print PASS only after assertions succeed.\n3. Run scripts/ci/run_tests.py locally.\n4. Install only addons/<plugin_id>/ in a clean project.",
		"code": "# tests/test_feature.gd\nextends SceneTree\n\nfunc _initialize() -> void:\n    if 2 + 2 != 4:\n        push_error(\"Feature regression\")\n        quit(1)\n        return\n    print(\"PASS: test_feature\")\n    quit(0)\n\n# Run:\n# python3 scripts/ci/run_tests.py --godot godot\n",
		"verify": "CI must pass the same tests and a clean install without the template's project.godot.",
	},
]
