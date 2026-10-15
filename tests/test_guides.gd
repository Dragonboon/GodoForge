extends SceneTree

const Topics = preload("res://addons/my_plugin/editor/guide_topics.gd")
const GuidePanel = preload("res://addons/my_plugin/editor/example_dock.gd")


func _initialize() -> void:
	if Topics.TOPICS.size() < 5:
		fail("expected at least five offline tutorials")
		return
	for topic: Dictionary in Topics.TOPICS:
		for key: String in ["title", "goal", "steps", "code", "verify"]:
			if not topic.has(key) or String(topic[key]).strip_edges().is_empty():
				fail("incomplete tutorial: " + key)
				return
	var panel := GuidePanel.new()
	if not panel is ScrollContainer:
		fail("learning panel must be scrollable")
		return
	if panel.custom_minimum_size.y > 0.0:
		fail("learning panel must not force editor height")
		return
	panel.free()
	print("PASS: test_guides")
	quit(0)


func fail(message: String) -> void:
	push_error(message)
	quit(1)
