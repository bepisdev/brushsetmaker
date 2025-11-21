# Scripts

This directory contains utility scripts for development and release automation.

## bump_version.py

Automatically increments the version number across all project files that contain version references.

### Usage

```bash
# Bump patch version (0.2.2 -> 0.2.3)
python scripts/bump_version.py --patch

# Bump minor version (0.2.2 -> 0.3.0)
python scripts/bump_version.py --minor

# Bump major version (0.2.2 -> 1.0.0)
python scripts/bump_version.py --major

# Set a specific version
python scripts/bump_version.py --set 1.5.0

# Preview changes without modifying files
python scripts/bump_version.py --dry-run --patch
```

### Files Updated

The script automatically updates version numbers in:

- `pyproject.toml` (lines 3 and 17)
- `src/brushsetmaker/__init__.py` (line 3)
- `src/brushsetmaker.dist-info/METADATA` (line 6)

### Integration with Git Flow

Use this script when preparing a release:

```bash
# Start a release branch
git flow release start 0.3.0

# Bump the version
python scripts/bump_version.py --minor

# Review the changes
git diff

# Commit the version bump
git add .
git commit -m "Bump version to 0.3.0"

# Finish the release
git flow release finish 0.3.0
```

See [Preparing a Release](../docs/documentation/contribute/prepare-a-release.md) for the complete release workflow.
