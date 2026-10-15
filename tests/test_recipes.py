"""Check that the default plugin is non-invasive and recipes stay navigable."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
RECIPES = ROOT / "docs" / "recipes"
FILES = [
    "EDITOR_DOCK.md",
    "CUSTOM_NODE.md",
    "INSPECTOR_PLUGIN.md",
    "TOOLS_MENU.md",
    "RUNTIME_RESOURCE.md",
    "TESTING_RELEASE.md",
]

class StarterIntegrityTests(unittest.TestCase):
    def test_no_editor_ui_in_base_plugin(self):
        manifests = sorted((ROOT / "addons").glob("*/plugin.cfg"))
        self.assertEqual(len(manifests), 1, "Template should have one starter plugin")
        plugin = (manifests[0].parent / "plugin.gd").read_text(encoding="utf-8")
        self.assertIn("extends EditorPlugin", plugin)
        self.assertIn("func _enter_tree()", plugin)
        self.assertIn("func _exit_tree()", plugin)
        for call in ("add_dock(", "add_control_to_bottom_panel(",
                     "add_control_to_dock(", "add_tool_menu_item(",
                     "add_inspector_plugin(", "add_custom_type("):
            self.assertNotIn(call, plugin)
        self.assertFalse((manifests[0].parent / "editor" / "example_dock.gd").exists())
        self.assertFalse((manifests[0].parent / "editor" / "guide_topics.gd").exists())

    def test_recipes_are_complete_and_linked(self):
        index = (RECIPES / "README.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for filename in FILES:
            file = RECIPES / filename
            self.assertTrue(file.is_file(), filename)
            self.assertIn(f"({filename})", index)
            self.assertIn(f"(docs/recipes/{filename})", readme)
            recipe = file.read_text(encoding="utf-8")
            self.assertIn("```gdscript", recipe)
            self.assertIn("## Verify", recipe)
            self.assertIn("addons/", recipe)

if __name__ == "__main__":
    unittest.main()
