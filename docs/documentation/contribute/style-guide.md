---
layout: page
title: Code Style Guide
---

This document outlines the coding standards and conventions used in the BrushsetMaker project. Following these guidelines ensures consistency and maintainability across the codebase.

## Table of Contents

- [Python Version](#python-version)
- [Code Formatting](#code-formatting)
- [Naming Conventions](#naming-conventions)
- [Documentation](#documentation)
- [Import Organization](#import-organization)
- [Type Hints](#type-hints)
- [Error Handling](#error-handling)
- [Async/Await Patterns](#asyncawait-patterns)
- [UI Components](#ui-components)
- [Project Structure](#project-structure)

## Python Version

- **Target Python Version**: 3.12+
- All code must be compatible with Python 3.12 or higher
- Use modern Python features when appropriate

## Code Formatting

### Indentation and Spacing

- Use **4 spaces** for indentation (never tabs)
- Maximum line length: **100 characters** (soft limit)
- Use blank lines to separate logical sections within functions
- Add two blank lines between top-level classes and functions

### String Formatting

- Use **double quotes** (`"`) for strings by default
- Use **single quotes** (`'`) for string keys in dictionaries when appropriate
- Prefer f-strings for string interpolation:

```python
# Good
message = f"Processing {idx} of {total} folders..."

# Avoid
message = "Processing %d of %d folders..." % (idx, total)
message = "Processing {} of {} folders...".format(idx, total)
```

### Whitespace

- One space around operators: `x = y + 5`
- No spaces inside parentheses: `function(arg1, arg2)`
- No trailing whitespace at end of lines

## Naming Conventions

### Variables and Functions

- Use **snake_case** for variables and functions:

```python
selected_folder = None
progress_window = None

def create_progress_window(app, total):
    pass
```

### Classes

- Use **PascalCase** for class names:

```python
class BrushsetMaker(toga.App):
    pass

class UIBuilder:
    pass

class BrushsetHandlers:
    pass
```

### Constants

- Use **UPPER_SNAKE_CASE** for constants:

```python
MAX_ERRORS_TO_DISPLAY = 5
DEFAULT_PADDING = 30
```

### Private Methods

- Prefix private methods with a single underscore:

```python
def _build_single_section(app):
    """Build the single brushset section."""
    pass

async def _handle_create_single(self, widget):
    """Wrapper for create single brushset handler."""
    pass
```

### Module Names

- Use lowercase with underscores: `handlers.py`, `builder.py`
- Keep module names short and descriptive

## Documentation

### Module Docstrings

- Every module must have a docstring at the top:

```python
"""BrushsetMaker - macOS utility to compile brushsets for Procreate."""
```

### Class Docstrings

- Use simple, descriptive docstrings for classes:

```python
class BrushsetMaker(toga.App):
    """Main application class for BrushsetMaker."""
```

### Function Docstrings

- Use descriptive docstrings for all functions and methods
- Keep docstrings concise and action-oriented:

```python
def startup(self):
    """Construct and show the Toga application."""
    # implementation

@staticmethod
async def create_single_brushset(app, widget):
    """Create a single brushset from a selected folder."""
    # implementation
```

- For complex functions, add parameter descriptions if needed:

```python
def create_progress_window(app, total):
    """
    Create a progress window.
    
    Args:
        app: The application instance
        total: Total number of items to process
    """
```

### Comments

- Use inline comments sparingly and only when necessary
- Comments should explain *why*, not *what*
- Keep comments up-to-date with code changes
- Use descriptive variable names instead of comments when possible

## Import Organization

Organize imports in the following order, with a blank line between each group:

1. **Standard library imports**
2. **Third-party library imports**
3. **Local application imports**

Example:

```python
"""Event handlers for BrushsetMaker application."""

import zipfile
from pathlib import Path

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from .handlers import BrushsetHandlers
```

### Import Guidelines

- Use absolute imports for packages
- Use relative imports within the same package
- Avoid wildcard imports (`from module import *`)
- Import only what you need

### `__all__` Declarations

- Use `__all__` in `__init__.py` files to define public API:

```python
"""Core application logic."""

from .handlers import BrushsetHandlers

__all__ = ['BrushsetHandlers']
```

## Type Hints

While the current codebase does not use type hints extensively, contributors are encouraged to add them when appropriate, especially for:

- Function parameters and return values
- Public API methods
- Complex data structures

Example:

```python
from pathlib import Path
from typing import Optional, List

def get_subdirectories(root_path: Path) -> List[Path]:
    """Get all subdirectories in the given path."""
    return [d for d in root_path.iterdir() if d.is_dir()]

async def create_single_brushset(
    app: toga.App, 
    widget: toga.Widget
) -> None:
    """Create a single brushset from a selected folder."""
    pass
```

## Error Handling

### Exception Handling

- Always handle exceptions gracefully in user-facing code
- Use specific exception types when possible
- Show user-friendly error messages through dialogs:

```python
try:
    # Operation that might fail
    result = perform_operation()
except SpecificException as e:
    await app.main_window.error_dialog("Error", f"Operation failed: {e}")
except Exception as e:
    await app.main_window.error_dialog("Error", f"Unexpected error: {e}")
```

### Error Messages

- Error messages should be clear and actionable
- Include relevant context (file names, paths, etc.)
- Use proper punctuation and capitalization
- Example: `"Error creating brushset: {e}"`

### Early Returns

- Use early returns to avoid deep nesting:

```python
async def create_single_brushset(app, widget):
    """Create a single brushset from a selected folder."""
    folder_path = await app.main_window.select_folder_dialog(
        title="Select Folder to Package"
    )
    
    if not folder_path:
        return  # Early return for cancellation
    
    # Continue with main logic
```

## Async/Await Patterns

### When to Use Async

- Use `async`/`await` for all UI event handlers
- Use `async` for file dialogs and I/O operations
- Mark handler wrappers as async:

```python
async def _handle_create_single(self, widget):
    """Wrapper for create single brushset handler."""
    await BrushsetHandlers.create_single_brushset(self, widget)
```

### Static Methods as Handlers

- Handler logic is implemented as static methods in handler classes
- Wrapper methods in the app class bridge UI callbacks to handlers:

```python
# In app.py
async def _handle_select_bulk(self, widget):
    """Wrapper for select bulk folder handler."""
    await BrushsetHandlers.select_bulk_folder(self, widget)

# In handlers.py
@staticmethod
async def select_bulk_folder(app, widget):
    """Handle bulk folder selection."""
    # Implementation
```

## UI Components

### Toga Style Conventions

- Use `Pack` for all styling
- Define styles inline when creating widgets:

```python
label = toga.Label(
    "BrushsetMaker",
    style=Pack(padding=(0, 0, 5, 0), font_size=24, font_weight="bold")
)
```

### Layout Structure

- Use `Box` containers for layout organization
- Separate major UI sections into builder methods:

```python
@staticmethod
def build_main_window(app):
    """Build and return the main window content."""
    main_box = toga.Box(style=Pack(direction=COLUMN, padding=30))
    
    # Build sub-sections
    single_box = UIBuilder._build_single_section(app)
    bulk_box = UIBuilder._build_bulk_section(app)
    
    main_box.add(single_box)
    main_box.add(bulk_box)
    
    return main_box
```

### UI Naming

- Store UI elements as app instance attributes when they need to be accessed later:

```python
app.folder_label = toga.Label("No folder selected")
app.process_button = toga.Button("Process All Subfolders", enabled=False)
```

### Padding and Spacing

- Use consistent padding values throughout the UI
- Main containers: `padding=30`
- Section boxes: `padding=20`
- Widget spacing: `padding=(0, 0, 10, 0)` (top, right, bottom, left)
- Add visual separators using `toga.Divider()`

### Emoji Usage

- Use emojis sparingly for visual enhancement in UI labels:

```python
single_label = toga.Label(
    "📦 Package Single Brushset",
    style=Pack(padding=(0, 0, 10, 0), font_size=16, font_weight="bold")
)
```

## Project Structure

### Package Organization

```text
src/
  brushsetmaker/
    __init__.py          # Package version and metadata
    __main__.py          # Entry point for module execution
    app.py               # Main application class
    core/                # Business logic
      __init__.py
      handlers.py        # Event handlers
    ui/                  # User interface
      __init__.py
      builder.py         # UI component builders
```

### Module Responsibilities

- **`app.py`**: Main application class, window setup, handler wrappers
- **`core/handlers.py`**: All business logic and event handling
- **`ui/builder.py`**: UI construction and layout
- **`__init__.py`**: Package initialization and public API definition

### Separation of Concerns

- Keep UI building separate from business logic
- Handler classes should be stateless static method containers
- Application state lives in the main app class
- UI builders receive the app instance and attach widgets as needed

## Testing

When writing tests:

- Place tests in a `tests/` directory at the project root
- Mirror the source structure in test files
- Use descriptive test names: `test_create_brushset_with_empty_folder`
- Use pytest as the testing framework
- Mock file system operations when appropriate

## Version Control

### Commit Messages

- Use clear, descriptive commit messages
- Start with a verb: "Add", "Fix", "Update", "Remove"
- Keep the first line under 72 characters
- Add details in subsequent lines if needed

Example:

```text
Add bulk processing progress window

- Create progress window with status label and progress bar
- Update progress as folders are processed
- Show completion summary with error details
```

## Dependencies

- Use `pyproject.toml` for dependency management
- Pin major versions, allow minor updates: `toga>=0.4.0`
- Document any macOS-specific dependencies in the appropriate section

## Code Quality Tools

### Ruff

The project uses [Ruff](https://docs.astral.sh/ruff/) for linting and code formatting. The configuration is defined in `pyproject.toml` under `[tool.ruff]`.

**Check code style:**

```bash
ruff check .
```

**Auto-fix issues:**

```bash
ruff check --fix .
```

**Format code:**

```bash
ruff format .
```

The ruff configuration enforces:

- 100 character line length (soft limit)
- Double quotes for strings
- Proper import organization (stdlib → third-party → local)
- Python 3.12+ syntax
- Google-style docstrings
- Pathlib usage over os.path

**Pre-commit checking** is recommended before committing code.

---

## Summary

The BrushsetMaker codebase follows clean, readable Python conventions with a focus on:

- **Clarity**: Descriptive names and straightforward logic
- **Consistency**: Uniform style throughout the project
- **Maintainability**: Well-organized structure and proper documentation
- **User Experience**: Graceful error handling and clear feedback

When in doubt, look at existing code for guidance and maintain consistency with the established patterns.
