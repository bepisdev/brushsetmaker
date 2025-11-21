# GitHub Copilot Instructions for BrushsetMaker

## Project Overview

BrushsetMaker is a macOS-native GUI application that packages Procreate brushes into `.brushset` files. Built with **Python 3.12+**, **Toga** (cross-platform GUI framework), and **Briefcase** (native app packager).

**Key Architecture Pattern**: Separation of concerns across three layers:
- `app.py`: Main Toga app class, window setup, async handler wrappers
- `ui/builder.py`: UI construction with static methods returning Toga widgets
- `core/handlers.py`: Business logic as static methods, accepts app instance

## Critical Development Workflows

### Environment Setup
```bash
./scripts/setup_dev.sh        # Automated full setup
uv sync                        # Install/update dependencies
make dev                       # Run in development mode
```

### Building & Packaging
```bash
make build                     # Build macOS .app
make package                   # Create .dmg (runs build first)
make clean                     # Remove all build artifacts
```

### Version Management
Use `scripts/bump_version.py` to update versions across ALL files simultaneously:
```bash
python scripts/bump_version.py --patch   # 0.2.2 -> 0.2.3
python scripts/bump_version.py --minor   # 0.2.2 -> 0.3.0
python scripts/bump_version.py --major   # 0.2.2 -> 1.0.0
```
Version MUST match in: `pyproject.toml` (lines 3, 17), `src/brushsetmaker/__init__.py`, `src/brushsetmaker.dist-info/METADATA`

### Release Process (Git Flow)
```bash
git flow release start 0.3.0
python scripts/bump_version.py --minor
git add . && git commit -m "Bump version to 0.3.0"
git flow release finish 0.3.0
git push origin main develop --tags
```

## Code Style Conventions

### Imports (strictly enforced by ruff)
```python
"""Module docstring required."""

import zipfile              # stdlib first
from pathlib import Path

import toga                 # third-party second
from toga.style import Pack

from .handlers import X     # local last, use relative imports within package
```

### Naming & Structure
- **snake_case**: functions, variables, module names
- **PascalCase**: classes only
- **UPPER_SNAKE_CASE**: constants
- **_prefix**: private methods (e.g., `_build_single_section`, `_handle_create_single`)
- **Double quotes** for strings (enforced by ruff)
- **100 char line limit** (soft, formatter handles)

### Async Patterns (Toga-specific)
UI event handlers MUST be async. Pattern: app class has async wrappers that call static handler methods:
```python
# In app.py (wrapper)
async def _handle_create_single(self, widget):
    await BrushsetHandlers.create_single_brushset(self, widget)

# In core/handlers.py (logic)
@staticmethod
async def create_single_brushset(app, widget):
    folder_path = await app.main_window.select_folder_dialog(...)
    if not folder_path:
        return  # Early return pattern
```

### UI Construction Pattern
Static methods in `UIBuilder` class build and return Box widgets. Attach widgets to app instance when they need later access:
```python
app.folder_label = toga.Label("No folder selected")  # Store on app
app.process_button = toga.Button("Process", enabled=False)

# Padding convention: (top, right, bottom, left)
style=Pack(padding=(0, 0, 15, 0))
```

## Package Management & Dependencies

- **uv** (not pip): `uv sync`, `uv run`, `uv pip install`
- **Briefcase**: Manages macOS bundle, icons, metadata (see `pyproject.toml` `[tool.briefcase]`)
- **Toga**: GUI framework, version pinning critical (`toga>=0.5.2`, `toga-cocoa>=0.4.0`)

## Testing & Linting

```bash
ruff check .                   # Lint with auto-configured rules
ruff check --fix .             # Auto-fix issues
ruff format .                  # Format code (respects 100 char limit)
```

Ruff config in `pyproject.toml` enforces: import sorting, pathlib over os.path, modern Python 3.12 syntax, no wildcard imports.

## Documentation Site

Jekyll-based site in `docs/`. Ruby/bundler required:
```bash
cd docs && bundle install
bundle exec jekyll serve      # Local preview at localhost:4000
```

## Common Pitfalls

1. **Version mismatch**: Always use `bump_version.py` script, never manually edit versions
2. **Missing await**: Toga dialogs (`select_folder_dialog`, `error_dialog`) return awaitables
3. **State management**: App state lives on `self` (app instance), not in static handlers
4. **Import order**: Ruff will fail CI if imports aren't sorted correctly (stdlib → third-party → local)
5. **Python version**: Code must work on 3.12+, use modern syntax (match statements, type hints)

## File Locations

- **Main app**: `src/brushsetmaker/app.py`
- **UI builders**: `src/brushsetmaker/ui/builder.py`
- **Business logic**: `src/brushsetmaker/core/handlers.py`
- **Version**: `src/brushsetmaker/__init__.py` (`__version__`)
- **Dependencies**: `pyproject.toml`
- **Style guide**: `docs/documentation/contribute/style-guide.md`
- **Automation**: `scripts/` (setup_dev.sh, bump_version.py)
