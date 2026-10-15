"""Pure-Python initializer and wizard regression tests, without Godot."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest import mock

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
            self.assertIn("addons/world_tools", (root / "tests/test_guides.gd").read_text())
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

    @mock.patch.object(mod, "initialize")
    @mock.patch.object(mod, "_interactive_terminal", return_value=True)
    def test_no_flags_runs_wizard(self, terminal, initialize):
        with mock.patch("builtins.input", side_effect=["World Tools", "", "Dev", "y"]):
            self.assertEqual(mod.main(["--no-color"]), 0)
        initialize.assert_called_once_with("world_tools", "World Tools", "Dev")

    @mock.patch.object(mod, "initialize")
    @mock.patch.object(mod, "_interactive_terminal", return_value=True)
    def test_validation_retry_and_partial_flags(self, terminal, initialize):
        with mock.patch("builtins.input", side_effect=["BAD-ID", "world_tools", "Dev", "yes"]):
            self.assertEqual(mod.main(["--name", "World Tools", "--no-color"]), 0)
        initialize.assert_called_once_with("world_tools", "World Tools", "Dev")

    @mock.patch.object(mod, "initialize")
    @mock.patch.object(mod, "_interactive_terminal", return_value=True)
    def test_confirmation_defaults_to_cancel(self, terminal, initialize):
        with mock.patch("builtins.input", side_effect=["World Tools", "", "Dev", ""]):
            self.assertEqual(mod.main([]), 0)
        initialize.assert_not_called()

    @mock.patch.object(mod, "initialize")
    @mock.patch.object(mod, "_interactive_terminal", return_value=False)
    def test_non_tty_requires_flags(self, terminal, initialize):
        self.assertEqual(mod.main([]), 2)
        initialize.assert_not_called()

    @mock.patch.object(mod, "initialize")
    def test_flags_still_work_untouched(self, initialize):
        self.assertEqual(mod.main(["--id", "tools", "--name", "Tools", "--author", "Dev"]), 0)
        initialize.assert_called_once_with("tools", "Tools", "Dev")

    def test_no_color_env(self):
        with mock.patch.dict(mod.os.environ, {"NO_COLOR": ""}):
            self.assertFalse(mod._supports_color())

if __name__ == "__main__":
    unittest.main()
