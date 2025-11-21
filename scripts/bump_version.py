#!/usr/bin/env python3
"""
Version bump script for BrushsetMaker.

This script increments the version number across all project files
that contain version references, ensuring consistency.

Usage:
    python scripts/bump_version.py [--major|--minor|--patch]
    python scripts/bump_version.py --set X.Y.Z

Examples:
    python scripts/bump_version.py --patch  # 0.2.2 -> 0.2.3
    python scripts/bump_version.py --minor  # 0.2.2 -> 0.3.0
    python scripts/bump_version.py --major  # 0.2.2 -> 1.0.0
    python scripts/bump_version.py --set 1.5.0
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Tuple


def parse_version(version: str) -> Tuple[int, int, int]:
    """Parse a semantic version string into major, minor, patch components."""
    match = re.match(r'^(\d+)\.(\d+)\.(\d+)$', version)
    if not match:
        raise ValueError(f"Invalid version format: {version}")
    return tuple(map(int, match.groups())) # type: ignore


def format_version(major: int, minor: int, patch: int) -> str:
    """Format version components into a semantic version string."""
    return f"{major}.{minor}.{patch}"


def bump_version(current_version: str, bump_type: str) -> str:
    """Bump the version based on the specified type (major, minor, or patch)."""
    major, minor, patch = parse_version(current_version)

    if bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "patch":
        patch += 1
    else:
        raise ValueError(f"Invalid bump type: {bump_type}")

    return format_version(major, minor, patch)


def get_current_version(project_root: Path) -> str:
    """Extract current version from __init__.py."""
    init_file = project_root / "src" / "brushsetmaker" / "__init__.py"

    if not init_file.exists():
        raise FileNotFoundError(f"Cannot find {init_file}")

    content = init_file.read_text()
    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)

    if not match:
        raise ValueError("Cannot find __version__ in __init__.py")

    return match.group(1)


def update_file(file_path: Path, old_version: str, new_version: str) -> bool:
    """Update version in a file. Returns True if changes were made."""
    if not file_path.exists():
        print(f"Warning: {file_path} does not exist, skipping...")
        return False

    content = file_path.read_text()
    original_content = content

    # Replace all occurrences of the old version with the new version
    content = content.replace(old_version, new_version)

    if content != original_content:
        file_path.write_text(content)
        return True

    return False


def update_all_files(project_root: Path, old_version: str, new_version: str) -> None:
    """Update version in all relevant project files."""
    files_to_update = [
        project_root / "pyproject.toml",
        project_root / "src" / "brushsetmaker" / "__init__.py",
        project_root / "src" / "brushsetmaker.dist-info" / "METADATA",
    ]

    print(f"Bumping version from {old_version} to {new_version}\n")

    updated_files = []
    skipped_files = []

    for file_path in files_to_update:
        relative_path = file_path.relative_to(project_root)
        if update_file(file_path, old_version, new_version):
            updated_files.append(relative_path)
            print(f"✓ Updated {relative_path}")
        else:
            skipped_files.append(relative_path)
            print(f"⊘ No changes in {relative_path}")

    print(f"\n{'='*60}")
    print("Summary:")
    print(f"  Version: {old_version} → {new_version}")
    print(f"  Updated: {len(updated_files)} file(s)")
    print(f"  Skipped: {len(skipped_files)} file(s)")
    print(f"{'='*60}\n")

    if updated_files:
        print("Next steps:")
        print("  1. Review changes: git diff")
        print(f"  2. Commit changes: git add . && git commit -m 'Bump version to {new_version}'")
        print(f"  3. Finish release: git flow release finish {new_version}")


def main():
    """Main entry point for the version bump script."""
    parser = argparse.ArgumentParser(
        description="Bump version across all BrushsetMaker project files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--major",
        action="store_const",
        const="major",
        dest="bump_type",
        help="Bump major version (X.0.0)"
    )
    group.add_argument(
        "--minor",
        action="store_const",
        const="minor",
        dest="bump_type",
        help="Bump minor version (x.Y.0)"
    )
    group.add_argument(
        "--patch",
        action="store_const",
        const="patch",
        dest="bump_type",
        help="Bump patch version (x.y.Z)"
    )
    group.add_argument(
        "--set",
        type=str,
        metavar="VERSION",
        help="Set specific version (e.g., 1.2.3)"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without making changes"
    )

    args = parser.parse_args()

    # Determine project root (script is in scripts/ directory)
    project_root = Path(__file__).parent.parent

    try:
        # Get current version
        current_version = get_current_version(project_root)

        # Calculate new version
        if args.set:
            # Validate the provided version format
            parse_version(args.set)
            new_version = args.set
        else:
            new_version = bump_version(current_version, args.bump_type)

        # Show what will happen
        if args.dry_run:
            print(f"[DRY RUN] Would bump version from {current_version} to {new_version}")
            return 0

        # Confirm if major version bump
        if args.bump_type == "major" or (args.set and parse_version(args.set)[0] > parse_version(current_version)[0]):
            response = input(f"⚠️  Major version bump detected ({current_version} → {new_version}). Continue? [y/N] ")
            if response.lower() != 'y':
                print("Aborted.")
                return 1

        # Update all files
        update_all_files(project_root, current_version, new_version)

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
