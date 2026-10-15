# How to test and publish a Godot 4.7 addon

**Use when:** you are adding a feature or preparing a public plugin release.

## Add a smoke test: `tests/test_feature.gd`

```gdscript
extends SceneTree

func _initialize() -> void:
    var result := 2 + 2
    if result != 4:
        push_error("Unexpected result")
        quit(1)
        return
    print("PASS: test_feature")
    quit(0)
```

Replace the trivial assertion with a focused behavior from your module. Use an explicit nonzero exit on failure: CI can miss errors if a test only prints them.

## Run checks

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/ci/run_tests.py --godot godot
```

The runner imports using Godot headless editor mode and executes every `tests/test_*.gd`. It expects `PASS: <test_file_stem>` for each test and fails for errors.

## Package

Only publish:

```text
addons/my_plugin/
  plugin.cfg
  plugin.gd
  src/                # only if your addon needs runtime modules
  editor/             # only if you opted into editor integrations
```

Do **not** ship the template's host `project.godot`, test runner, CI setup or documentation recipes as an implicit dependency.

## Verify

1. Enable/disable the plugin multiple times and confirm no UI or hooks leak.
2. Install the release contents alone in a clean Godot project.
3. Run your target Godot versions and document the actual minimum supported version.
4. Review every exported resource and plugin setting for opt-in, predictable behavior.

Reference: [Making plugins](https://docs.godotengine.org/en/4.7/tutorials/plugins/editor/making_plugins.html).
