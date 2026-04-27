#!/usr/bin/env python3
"""Resolve the project directory by searching for features.json or progress.md.

Walks up from the given start directory (or cwd) to find the directory containing
project tracking files. This ensures agents always write to the correct location
regardless of their current working directory.

Usage:
    python3 scripts/resolve_project_dir.py [--start-dir DIR]

Exit codes:
    0 - Project directory found, printed to stdout
    1 - No project directory found
"""

import argparse
import sys
from pathlib import Path

MARKER_FILES = ["features.json", "progress.md"]
WRONG_DIRS = [".agent-harness", "node_modules", ".git", "__pycache__"]


def find_project_dir(start_dir: Path) -> Path:
    """Walk up from start_dir to find the directory containing marker files.

    Skips known non-project directories like .agent-harness and node_modules.
    Returns the first non-skipped parent if no markers are found.
    """
    current = start_dir.resolve()
    last_valid = current

    while current != current.parent:
        if current.name not in WRONG_DIRS:
            last_valid = current

        for marker in MARKER_FILES:
            if (current / marker).exists():
                return current

        current = current.parent

    # Check root directory too
    if current.name not in WRONG_DIRS:
        last_valid = current
    for marker in MARKER_FILES:
        if (current / marker).exists():
            return current

    return last_valid


def main():
    parser = argparse.ArgumentParser(
        description="Resolve the agent-harness project directory"
    )
    parser.add_argument(
        "--start-dir",
        "-s",
        default=None,
        help="Directory to start searching from (default: current directory)",
    )
    args = parser.parse_args()

    start = Path(args.start_dir) if args.start_dir else Path.cwd()
    project_dir = find_project_dir(start)

    # Verify marker files exist (or this might be a new project)
    has_markers = any((project_dir / m).exists() for m in MARKER_FILES)

    print(str(project_dir))

    if not has_markers:
        print(
            f"Warning: No marker files found. Using {project_dir} as project directory.",
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
