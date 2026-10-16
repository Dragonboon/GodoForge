# Agent guide — GodoForge

Scope: this file applies to the entire repository. **GodoForge is a GitHub template for Godot addons**, not a reusable runtime framework or a finished game. Its untouched starter is deliberately inert. The supported baseline is **Godot 4.7** (CI pins **4.7.2-stable**); the optional Python wizard requires Python **3.10+** and uses the standard library.

## Read and navigate efficiently

1. Check the current `main` state and existing changes before editing. Read only the README section and files related to the task; use narrow searches before opening large directories.
2. Route by responsibility:
   - Python setup/rename: `scripts/init_plugin.py` and `tests/test_initializer.py`, `tests/test_template.py`.
   - Godot-native setup: `scripts/init_plugin.gd` and `scripts/ci/check_generated.py`.
   - Minimal editor lifecycle: `addons/my_plugin/plugin.gd`, `plugin.cfg`, `tests/test_plugin.gd`.
   - Documentation patterns: `docs/recipes/` and `tests/test_recipes.py`.
   - Headless validation/CI: `scripts/ci/run_tests.py`, `scripts/ci/check_generated.py`, `.github/workflows/godot-ci.yml`.
3. Inspect the direct caller, associated regression and public documentation before changing behavior. Avoid reading all recipes, generating all example projects, or executing costly test matrices for documentation-only edits.

## Non-negotiable contracts

- **Never run the initializer against the upstream working tree** as a demonstration: it is designed to initialize a newly created copy, and renames `addons/my_plugin/`. Test initialization in a temporary copy through the existing checks.
- Preserve both initialization paths (Python and Godot CLI), interactive confirmation, unattended arguments, lowercase `snake_case` plugin IDs, and refusal to overwrite an existing addon.
- A pristine template must register no dock, toolbar, autoload or custom editor type. Add capabilities through opt-in recipes; do not ship their example behavior by default.
- The only distributable unit is `addons/<plugin_id>/` in an initialized project. It must not depend on root tests, CI, template scripts or recipe files.
- For recipe composition, merge `EditorPlugin` registration and cleanup deliberately; do not replace an existing `plugin.gd` wholesale. Preserve enable/disable symmetry.
- Do not rewrite `project.godot`, regenerate UIDs/import files unnecessarily, add runtime dependencies, or claim support for untested engine versions.

## Validation with minimal work

Run the narrowest relevant check first, then the broader checks when changing initialization, packaging or lifecycle:

```sh
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/ci/run_tests.py --godot godot --timeout 90
```

For initializer/packaging changes, additionally use the existing `scripts/ci/check_generated.py` workflow for **both** Python and native Godot setup, matching `.github/workflows/godot-ci.yml`; execute these only in safe temporary workspaces. Verify `godot --version` before claiming engine compatibility. If Godot is unavailable, report Python/static checks separately and mark the headless import as unverified.

## Change and delivery discipline

Make the smallest compatible patch, with targeted regression coverage for behavior changes. Preserve template portability and public documentation. When explicitly authorized, commit only the requested changes to current `main` without force pushing or discarding concurrent edits. Summarize touched paths, commands actually run, results and remaining manual/editor verification. Never claim CI success without checking the commit's actual run.
