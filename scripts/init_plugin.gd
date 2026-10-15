## Python-free GodoForge initializer for Godot 4.7.
## godot --headless --path . --script res://scripts/init_plugin.gd -- --help
extends SceneTree

const FILES = [
	"README.md",
	"docs/PLUGIN_README_TEMPLATE.md",
	"project.godot",
	"addons/my_plugin/plugin.cfg",
	"addons/my_plugin/plugin.gd",
	"tests/test_plugin.gd",
	"docs/DEVELOPMENT.md",
	"docs/TESTING.md",
	"docs/recipes/README.md",
	"docs/recipes/EDITOR_DOCK.md",
	"docs/recipes/CUSTOM_NODE.md",
	"docs/recipes/INSPECTOR_PLUGIN.md",
	"docs/recipes/TOOLS_MENU.md",
	"docs/recipes/RUNTIME_RESOURCE.md",
	"docs/recipes/TESTING_RELEASE.md",
]

var _id_pattern: RegEx


func _initialize() -> void:
	_id_pattern = RegEx.new()
	if _id_pattern.compile("^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$") != OK:
		_fail("Could not initialize identifier validation.")
		return
	var parsed := _parse_args(OS.get_cmdline_user_args())
	if not parsed["ok"]:
		_fail(parsed["error"], 2)
		return
	var options: Dictionary = parsed["options"]
	if options.has("help"):
		_usage()
		quit(0)
		return
	var result := _collect(options)
	if not result["ok"]:
		if result["error"] == "cancelled":
			print("Cancelled. No files changed.")
			quit(0)
		else:
			_fail(result["error"], 2)
		return
	var values: Dictionary = result["values"]
	var error := _initialize_plugin(values["id"], values["name"], values["author"])
	if error != "":
		_fail(error)
		return
	print("Initialized %s as addons/%s/" % [values["name"], values["id"]])
	print("Next: open project.godot, enable your plugin, and run the checks.")
	quit(0)


func _fail(message: String, code: int = 1) -> void:
	printerr("ERROR: " + message)
	quit(code)


func _usage() -> void:
	print("GodoForge setup (Godot 4.7; no Python required)")
	print("godot --headless --path . --script res://scripts/init_plugin.gd -- [options]")
	print("  --id IDENTIFIER   lowercase snake_case folder, e.g. world_tools")
	print("  --name NAME       display name, e.g. World Tools")
	print("  --author AUTHOR   author or organization")
	print("  --no-color        plain terminal output (default)")
	print("  --help            show help")
	print("All three parameters: unattended setup. Missing parameters: terminal wizard.")
	print("Interactive mode requires stdin; Windows users should run the console executable.")


func _parse_args(arguments: PackedStringArray) -> Dictionary:
	var options := {}
	var i := 0
	while i < arguments.size():
		var argument: String = arguments[i]
		if argument == "--help" or argument == "--no-color":
			options[argument.trim_prefix("--")] = true
			i += 1
			continue
		if argument not in ["--id", "--name", "--author"]:
			return {"ok": false, "error": "Unknown argument '%s'; see --help." % argument}
		var key := argument.trim_prefix("--")
		if options.has(key) or i + 1 >= arguments.size():
			return {"ok": false, "error": "Missing or repeated value for %s." % argument}
		options[key] = arguments[i + 1]
		i += 2
	return {"ok": true, "options": options}


func _collect(args: Dictionary) -> Dictionary:
	var name: String = args.get("name", "")
	var identifier: String = args.get("id", "")
	var author: String = args.get("author", "")
	var complete: bool = args.has("name") and args.has("id") and args.has("author")
	if not complete:
		print("")
		print("GodoForge Setup | 3 fields, Godot only")
		print("Enter accepts suggestions. Any answer other than 'y' cancels at confirmation.")
		if name.is_empty():
			name = _ask("1/3 Plugin name", "Human-readable name, e.g. World Tools", "", false)
		if identifier.is_empty():
			var suggestion := name.to_lower().strip_edges().replace(" ", "_").replace("-", "_")
			if not _valid_id(suggestion):
				suggestion = ""
			identifier = _ask("2/3 Plugin ID", "lowercase snake_case, e.g. world_tools", suggestion, true)
		if author.is_empty():
			author = _ask("3/3 Author", "Person or organization shown in plugin.cfg", "", false)
	if not _valid_id(identifier):
		return {"ok": false, "error": "Invalid plugin ID; choose lowercase snake_case, e.g. world_tools."}
	if not _valid_text(name) or not _valid_text(author):
		return {"ok": false, "error": "Name and author cannot be empty or contain quotes/control characters."}
	if not complete:
		print("")
		print("Review (no changes made):")
		print("  Name: " + name)
		print("  ID: " + identifier)
		print("  Author: " + author)
		print("  Destination: addons/%s/" % identifier)
		print("Create this plugin? [y/N] ")
		var answer := OS.read_string_from_stdin(4096).strip_edges().to_lower()
		if answer not in ["y", "yes", "s", "si", "sí"]:
			return {"ok": false, "error": "cancelled"}
	return {"ok": true, "values": {"id": identifier, "name": name, "author": author}}


func _ask(label: String, hint: String, default: String, is_id: bool) -> String:
	# Bounded retries also prevent endless loops when stdin is closed.
	for attempt in range(5):
		print("")
		print(label)
		print("  " + hint)
		var suffix := " [%s]" % default if not default.is_empty() else ""
		print("  Value%s: " % suffix)
		var value := OS.read_string_from_stdin(4096).strip_edges()
		if value.is_empty():
			value = default
		if (is_id and _valid_id(value)) or (not is_id and _valid_text(value)):
			return value
		print("  ERROR: Invalid value. Try again.")
	return ""


func _valid_id(value: String) -> bool:
	return value != "my_plugin" and _id_pattern.search(value) != null


func _valid_text(value: String) -> bool:
	if value.strip_edges().is_empty():
		return false
	for ch in value:
		if ch == '"' or ch.unicode_at(0) < 32 or ch.unicode_at(0) == 127:
			return false
	return true


func _initialize_plugin(identifier: String, display_name: String, author: String) -> String:
	var root := ProjectSettings.globalize_path("res://")
	var source := root.path_join("addons/my_plugin")
	var destination := root.path_join("addons/" + identifier)
	if not DirAccess.dir_exists_absolute(source) or DirAccess.dir_exists_absolute(destination):
		return "Template already initialized or destination exists."
	var addons := DirAccess.open(root.path_join("addons"))
	if addons == null or addons.get_directories() != PackedStringArray(["my_plugin"]):
		return "Expected only addons/my_plugin. Refusing to modify other addons."
	var contents := {}
	var original := {}
	var generated_class := ""
	for part: String in identifier.split("_"):
		generated_class += part.capitalize()
	for relative: String in FILES:
		var absolute := root.path_join(relative)
		if not FileAccess.file_exists(absolute):
			return "Incomplete template: missing %s. No changes made." % relative
		var handle := FileAccess.open(absolute, FileAccess.READ)
		if handle == null:
			return "Cannot read %s. No changes made." % relative
		var content := handle.get_as_text()
		handle.close()
		if _has_conflict_markers(content):
			return "Unresolved merge markers in %s. No changes made." % relative
		original[relative] = content
		content = content.replace("my_plugin", identifier).replace("MyPlugin", generated_class)
		content = content.replace("My Plugin", display_name)
		if relative == "addons/my_plugin/plugin.cfg":
			content = content.replace("Template Author", author)
		if relative == "project.godot":
			content = content.replace('config/name="GodoForge"', 'config/name="%s"' % display_name)
			content = content.replace(
				'config/description="Minimal, modular Godot 4.7 plugin starter and developer toolkit."',
				'config/description="%s plugin development project"' % display_name
			)
		contents[relative] = content
	contents["README.md"] = contents["docs/PLUGIN_README_TEMPLATE.md"]
	var written: Array[String] = []
	for relative: String in FILES:
		var handle := FileAccess.open(root.path_join(relative), FileAccess.WRITE)
		if handle == null:
			_restore(root, written, original)
			return "Cannot write %s; attempted to restore originals." % relative
		handle.store_string(contents[relative])
		handle.flush()
		if handle.get_error() != OK:
			handle.close()
			written.append(relative)
			_restore(root, written, original)
			return "Write failed for %s; attempted to restore originals." % relative
		handle.close()
		written.append(relative)
	var result := DirAccess.rename_absolute(source, destination)
	if result != OK:
		_restore(root, written, original)
		return "Cannot rename addon folder (%s); attempted to restore originals." % result
	return ""


func _restore(root: String, written: Array[String], original: Dictionary) -> void:
	for relative: String in written:
		var handle := FileAccess.open(root.path_join(relative), FileAccess.WRITE)
		if handle != null:
			handle.store_string(original[relative])
			handle.close()


func _has_conflict_markers(content: String) -> bool:
	for line: String in content.split("\n"):
		if line.begins_with("<<<<<<<") or line.begins_with("=======") or line.begins_with(">>>>>>>"):
			return true
	return false
