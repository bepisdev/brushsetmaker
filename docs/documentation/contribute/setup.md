---
layout: page
title: Development Environment & Toolchain Setup
---

## Quick Start

For automated setup, run the setup script:

```bash
./scripts/setup_dev.sh
```

This will check for all required tools and automatically install dependencies. For manual setup or troubleshooting, see the detailed requirements below.

## Languages

The following tools are essential for development. Whilst we do not enforce version management for language interpreters / compilers
the following languages are used in this project and must have at least the standard toolchain available

- Python (>= 3.12)
- Ruby

## System

- `git` - Version control
- `make` - Task runner
- Xcode - macOS IDE for various edge case tasks
- `editorconfig` - Enforcing setups

## Python

- `uv` - Package and virtual environment management, Python version management
- `ruff` - Python linter
- `briefcase` - Compiler and packaging tool for the Toga framework

## Ruby

- `bundler` - Ruby gem
- `jekyll` - Static site engine

## Manual Setup

If you prefer manual setup or need to troubleshoot:

### Python Environment

```bash
# Install uv if not present
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv venv
uv sync

# Install ruff for linting
uv pip install ruff
```

### Ruby Environment (for documentation)

```bash
# Install bundler if not present
gem install bundler

# Install Jekyll and dependencies
cd docs
bundle install
```

### Verification

```bash
# Test the app runs
make dev

# Test the docs site
cd docs && bundle exec jekyll serve
```

For more automation scripts, see the [scripts directory](../../../scripts/README.md).
