# Testing

Install a compatible Godot 4.7 executable and run from the repository root:

```bash
python3 scripts/ci/run_tests.py --godot godot --timeout 90
python3 -m unittest discover -s tests -p 'test_*.py'
```

The runner imports the project in **editor headless mode**, rejects parser/runtime errors even when Godot exits with status 0, then runs `tests/test_plugin.gd`. Its smoke test verifies the manifest, script, optional dock implementation, and disabled-plugin-safe file layout. Test actual enable/disable UI manually, since headless script execution is not equivalent to an interactive editor lifecycle.

CI pins Godot **4.7.2-stable**. To test another release, change the download version in the workflow and test the actual executable, rather than merely changing the badge/documentation.

For feature modules, add `tests/test_*.gd` scripts that extend `SceneTree`, return nonzero on failure using `quit(1)`, and print `PASS` on success. Add an integration project/test when using actual editor interaction.
