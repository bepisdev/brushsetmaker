# Scripts

This directory contains utility scripts for development and release automation.

## setup_dev.sh

Automated development environment setup script that verifies system requirements and installs all necessary dependencies.

### Usage

```bash
# Full setup (Python + Ruby)
./scripts/setup_dev.sh

# Skip Ruby/Jekyll setup
./scripts/setup_dev.sh --skip-ruby

# Skip Python setup
./scripts/setup_dev.sh --skip-python

# Force reinstall even if tools exist
./scripts/setup_dev.sh --force

# Show help
./scripts/setup_dev.sh --help
```

### What It Does

The script will:

1. **Check system requirements**: git, make, Xcode tools, Python 3.12+, Ruby
2. **Install missing tools**: uv (Python package manager), ruff (Python linter), bundler (Ruby gem manager)
3. **Setup Python environment**: Create virtual environment and install dependencies with `uv sync`
4. **Setup Ruby environment**: Install Jekyll and documentation dependencies
5. **Verify installation**: Test that packages are correctly installed

### First Time Setup

For a fresh clone of the repository:

```bash
# Clone the repository
git clone https://github.com/bepisdev/brushsetmaker.git
cd brushsetmaker

# Run the setup script
./scripts/setup_dev.sh
```

## bump_version.py

Automatically increments the version number across all project files that contain version references.

### Basic Usage

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
