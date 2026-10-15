"""Guard against accidental initialization of the upstream GodoForge template."""
from pathlib import Path
import configparser
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
GIT_CONFLICT = re.compile(r"(?m)^(?:<{7}|={7}|>{7})(?:\s|$)")

class TemplateHealthTests(unittest.TestCase):
    def test_project_is_valid_host(self):
        config_path = ROOT / "project.godot"
        text = config_path.read_text(encoding="utf-8")
        self.assertNotRegex(text, GIT_CONFLICT)
        self.assertIn("config_version=5", text)
        self.assertIn("[application]", text)
        self.assertIn("config/name=", text)
        self.assertIn('"4.7"', text)

    def test_template_addon_placeholder(self):
        addons = sorted(p.name for p in (ROOT / "addons").iterdir() if p.is_dir())
        self.assertEqual(addons, ["my_plugin"], "Expected a clean placeholder, not an initialized plugin")
        manifest = (ROOT / "addons/my_plugin/plugin.cfg").read_text(encoding="utf-8")
        self.assertIn('name="My Plugin"', manifest)
        self.assertIn('script="plugin.gd"', manifest)

    def test_docs_keep_upstream_brand(self):
        self.assertIn("# GodoForge", (ROOT / "README.md").read_text(encoding="utf-8"))
        self.assertIn("# My Plugin", (ROOT / "docs/PLUGIN_README_TEMPLATE.md").read_text(encoding="utf-8"))
        self.assertIn("https://github.com/Dragonboon/GodoForge", (ROOT / "README.md").read_text(encoding="utf-8"))

    def test_no_stale_pooling_or_conflict_markers(self):
        for path in [ROOT / "project.godot", ROOT / "README.md", ROOT / "docs/DEVELOPMENT.md",
                     ROOT / "tests/test_plugin.gd", ROOT / "docs/PLUGIN_README_TEMPLATE.md"]:
            text = path.read_text(encoding="utf-8")
            self.assertNotRegex(text, GIT_CONFLICT, str(path))
            self.assertNotIn("addons/pooling", text, str(path))

if __name__ == "__main__":
    unittest.main()
