#!/usr/bin/env python3
"""End-to-end smoke check of a newly generated plugin repository."""
from __future__ import annotations
import argparse
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]

def run(cmd: list[str], cwd: Path) -> None:
    print("$ " + " ".join(map(str, cmd)), flush=True)
    subprocess.run(cmd, cwd=cwd, check=True, timeout=180)

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--godot", required=True, help="Godot executable (absolute path recommended)")
    parser.add_argument("--native", action="store_true", help="Use GDScript initializer instead of Python")
    args = parser.parse_args()
    godot = Path(args.godot).resolve()
    if not godot.is_file():
        print("ERROR: Provide a path to the Godot binary.", file=sys.stderr)
        return 2
    with tempfile.TemporaryDirectory(prefix="godoforge-check-") as folder:
        sample = Path(folder) / "sample"
        sample.mkdir()
        for name in ("addons", "docs", "scripts", "tests"):
            shutil.copytree(ROOT / name, sample / name,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".godot"))
        for name in ("README.md", "project.godot", "icon.svg", "LICENSE"):
            shutil.copy2(ROOT / name, sample / name)
        if args.native:
            command = [str(godot), "--headless", "--path", str(sample),
                       "--script", "res://scripts/init_plugin.gd", "--",
                       "--id", "my_sample_addon", "--name", "My Sample Addon", "--author", "CI"]
        else:
            command = [sys.executable, "scripts/init_plugin.py",
                       "--id", "my_sample_addon", "--name", "My Sample Addon", "--author", "CI"]
        run(command, sample)
        assert (sample / "addons/my_sample_addon/plugin.cfg").exists()
        assert not (sample / "addons/my_plugin").exists()
        assert 'config/name="My Sample Addon"' in (sample / "project.godot").read_text()
        assert "# My Sample Addon" in (sample / "README.md").read_text()
        if args.native:
            # Repeat setup must fail safely; do not mutate the existing addon.
            result = subprocess.run(command, cwd=sample, capture_output=True, text=True, timeout=30)
            assert result.returncode != 0, "Initializer unexpectedly ran twice"
        run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"], sample)
        run([sys.executable, "scripts/ci/run_tests.py", "--godot", str(godot)], sample)
    print("PASS: fresh generated plugin smoke")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
