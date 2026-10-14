#!/usr/bin/env python3
"""Strict, zero-dependency Godot 4.7 headless smoke test runner."""
from __future__ import annotations
import argparse
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
ERROR = re.compile(r"(?:SCRIPT ERROR:|Parse Error:|Failed to load script|^ERROR:)", re.MULTILINE)

def run(cmd: list[str], timeout: int, require_pass: bool = False) -> bool:
    print("$ " + " ".join(cmd), flush=True)
    try:
        proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True,
                              errors="replace", timeout=timeout, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return False
    output = proc.stdout + "\n" + proc.stderr
    print(output, flush=True)
    ok = proc.returncode == 0 and not ERROR.search(output)
    return bool(ok and (not require_pass or "PASS: plugin smoke" in output))

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--godot", default=os.environ.get("GODOT_BIN", "godot"))
    parser.add_argument("--timeout", type=int, default=90)
    args = parser.parse_args()
    prefix = [args.godot, "--headless", "--path", str(ROOT)]
    if not run(prefix + ["--editor", "--quit"], args.timeout):
        return 1
    tests = sorted((ROOT / "tests").glob("test_*.gd"))
    if not tests:
        print("FAIL: no Godot tests found", file=sys.stderr)
        return 1
    for test in tests:
        if not run(prefix + ["--script", f"res://tests/{test.name}"], args.timeout, True):
            return 1
    print(f"PASS: {len(tests)} Godot smoke test(s)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
