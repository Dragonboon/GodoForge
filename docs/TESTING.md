# Testing

Run from the template root with Godot 4.7:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/ci/run_tests.py --godot godot --timeout 90
```

Python tests verify CLI flags, the new interactive wizard (including cancellation, TTY handling, suggested identifier, invalid input and no color), and the one-time rename without modifying your source checkout.

The Godot runner imports headlessly and then runs every `tests/test_*.gd`. Each must print `PASS: <test_filename_stem>` only on success, and call `quit(1)` on failure. The suite verifies plugin load and offline tutorial data; it does **not** prove that GUI sizing and docking behave correctly on all display sizes.

## Manual editor checks

1. Open Godot 4.7.2 and enable **My Plugin** in Project Settings.
2. Verify the right-side **Plugin Guide** opens, and Output, Debugger and the bottom status bar remain accessible.
3. Shrink the editor window, switch all six tutorials, scroll, select and copy sample code.
4. Move the dock to another side slot or float it; disable/re-enable the plugin.
5. Check no duplicate tabs, editor errors or changes to user project settings.
6. Install only `addons/<plugin_id>/` into a clean project.

CI pins Godot **4.7.2-stable** for import and scripting regression; interactive layout checks remain manual.
