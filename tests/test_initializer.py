"""Pure-Python initializer regression tests (no Godot needed)."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("initializer", SOURCE / "scripts/init_plugin.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

@unittest.skipUnless((SOURCE / "addons/my_plugin/plugin.cfg").is_file(),
                     "Starter initializer tests only apply before setup")
class InitializeTests(unittest.TestCase):
    def prepare(self, root):
        for source in mod.FILES:
            target = root / source.relative_to(SOURCE)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(source.read_bytes())

    def test_initialize(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.prepare(root)
            mod.initialize("world_tools", "World Tools", "Dev", root)
            self.assertFalse((root / "addons/my_plugin").exists())
            self.assertTrue((root / "addons/world_tools/plugin.gd").exists())
            self.assertIn('name="World Tools"', (root / "addons/world_tools/plugin.cfg").read_text())
            self.assertIn('author="Dev"', (root / "addons/world_tools/plugin.cfg").read_text())
            self.assertIn("addons/world_tools", (root / "tests/test_plugin.gd").read_text())
            with self.assertRaises(ValueError):
                mod.initialize("world_tools", "World Tools", "Dev", root)

    def test_reject_invalid_without_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.prepare(root)
            original = (root / "addons/my_plugin/plugin.cfg").read_bytes()
            for invalid in ("../evil", "MyPlugin", "a--b", "my_plugin"):
                with self.assertRaises(ValueError):
                    mod.initialize(invalid, "Title", "Dev", root)
            self.assertEqual(original, (root / "addons/my_plugin/plugin.cfg").read_bytes())

if __name__ == "__main__":
    unittest.main()
