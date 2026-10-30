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

## Feature contract and evidence

Before changing behavior, record a short contract in the task or review:

- Observable problem and acceptance example.
- Existing state owner, direct consumers and reusable native/addon mechanism.
- Smallest missing behavior; defaults, serialized fields, signals and compatibility affected.
- Focused reproduction, failure/cancel case and integration evidence.

Template-specific acceptance includes refusal to overwrite, temporary-copy initialization
and complete editor registration cleanup. Keep one writable owner for each state. Prefer an existing extension point to a
second manager; keep host-game policy outside the addon. A new shared abstraction
needs two concrete independent consumer scenarios, not two copies of one demo.
Trace actual instantiation, signal connections and teardown: a class name found
by search does not prove that the scene uses it.

Read branch/HEAD, source signatures and the nearest caller/test before trusting
old chat, roadmap or generated summaries. Use narrow searches and expand context
only when dependencies require it. Preserve tracked UIDs; generate new ones with
Godot. Review exported names, enums, defaults and save formats against the base
revision; document migration/version decisions for incompatible changes.

Validate progressively: documentation paths/links for docs-only work; import and
focused regression for logic; full existing suite for shared contracts; graphical
input/editor and clean addon-only installation for affected surfaces. Tests must
assert observable behavior, not repeat implementation details. Include invalid
input, repeated invocation, cancellation, freed references or tree reentry when
the changed lifetime permits them. Do not turn this list into speculative scope.

Report the owner, real wiring, changed contract, exact checks/results and skipped
checks. Separate static review, engine execution, graphical/device observation
and benchmarks. No invented quality, performance or agent-productivity gains;
compare baseline/final on the same scenario and hardware before quantifying.
