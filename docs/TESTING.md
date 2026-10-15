# Testing

From your repository root with Godot 4.7 installed:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/ci/run_tests.py --godot godot --timeout 90
```

Python tests cover the terminal wizard and its validation, noninteractive execution, cancellation and initializer file rename. They also assert that the default `plugin.gd` has **no UI registration** and that all cookbook entries exist.

The Godot runner imports the project headlessly, detects parser errors even if Godot exits with zero, then runs `tests/test_*.gd`. Each Godot test must print `PASS: <test_filename_stem>` only after its assertions succeed and use `quit(1)` on failures.

## Manual editor acceptance

1. Open the Godot 4.7.2 project and enable **My Plugin** in **Project > Project Settings > Plugins**.
2. Confirm there is **no additional tab, dock, panel or menu** and the bottom bar (Output/Debugger) is unchanged.
3. Disable and re-enable the plugin and restart the editor; confirm no layout changes and no errors.
4. Follow one [recipe](recipes/README.md) as needed, and test its registration/cleanup separately.
5. Install **only** the plugin's `addons/<id>/` folder into a clean project and repeat the relevant checks.

CI pins Godot 4.7.2-stable; visual editor-layout checks are manual because headless smoke tests do not prove pixel/layout behavior.
