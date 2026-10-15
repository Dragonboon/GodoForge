# Contributing

Please open an issue before large changes. Keep the base template **small and generic**, with no default dependencies. A feature should help developers build different Godot plugins, not solve a specific game's needs.

For pull requests, include the purpose, any compatibility risks, and the results of:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/ci/run_tests.py --godot godot
```

Use the supplied bug/feature issue templates. Report the exact Godot version and a minimal reproduction. Document editor lifecycle cleanup and test a fresh plugin install.
