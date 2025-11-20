# BrushsetMaker - Complete Instructions

## Overview

BrushsetMaker is a macOS GUI application that automatically compiles Procreate brushsets from folders. The application is built with:
- **Python 3.12+**
- **Toga** - Cross-platform GUI toolkit
- **Briefcase** - Package Python apps as native applications
- **uv** - Fast Python package manager

## Prerequisites

### On macOS (for development and building)

1. **Install Homebrew** (if not already installed):
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. **Install Python 3.12+**:
```bash
brew install python@3.12
```

3. **Install uv**:
```bash
pip3 install uv
```

### On Linux (for development only)

1. **Install Python 3.12+**:
```bash
sudo apt update
sudo apt install python3.12 python3-pip
```

2. **Install uv**:
```bash
pip3 install uv
```

## Installation

### Clone the Repository

```bash
git clone https://github.com/bepisdev/brushset-compiler.git
cd brushset-compiler
```

### Install Dependencies

```bash
uv sync
```

This command will:
- Create a virtual environment (`.venv/`)
- Install all required dependencies
- Set up the project for development

## Running the Application

### Method 1: Using Briefcase (Recommended)

#### Development Mode

Run the app in developer mode with hot-reload:

```bash
uv run briefcase dev
```

This will:
- Install Toga and platform-specific dependencies
- Launch the application in development mode
- Show console output for debugging

#### Build and Run

To build and run as a native app:

```bash
# First time: Create the app structure
uv run briefcase create

# Build the app
uv run briefcase build

# Run the built app
uv run briefcase run
```

### Method 2: Direct Python Execution (Development Only)

Run directly from source (requires Toga to be installed):

```bash
uv run python -m brushsetmaker
```

Or:

```bash
uv run python src/brushsetmaker/app.py
```

## Building for Distribution

### Build a macOS Application Bundle

```bash
# Create the Xcode project
uv run briefcase create macOS

# Build the application
uv run briefcase build macOS

# Test the built app
uv run briefcase run macOS
```

The built application will be in `macOS/BrushsetMaker/BrushsetMaker.app`

### Create a .dmg Installer

```bash
uv run briefcase package macOS
```

This creates a `.dmg` file in the `macOS/` directory that can be distributed to other users.

### Open in Xcode (Optional)

To customize the app further in Xcode:

```bash
uv run briefcase open macOS
```

## Using the Application

### Step-by-Step Guide

1. **Launch BrushsetMaker**
   - The application window will open with a clean interface

2. **Select Root Folder**
   - Click the "Select Root Folder" button
   - Choose a folder that contains subfolders of brushes
   - The folder path will be displayed in the log area

3. **Process Folders**
   - Click the "Process Folders" button
   - The app will:
     - Scan all subfolders
     - Create a `.brushset` (zip) file for each subfolder
     - Display progress in the scrollable log area

4. **Review Results**
   - Check the log area for success/error messages
   - Find `.brushset` files in the root folder you selected

### Example Folder Structure

**Before processing:**
```
MyBrushes/
├── WatercolorBrushes/
│   ├── brush1.png
│   ├── brush2.png
│   └── metadata.json
├── OilPaintBrushes/
│   ├── brush1.png
│   └── brush2.png
└── PencilBrushes/
    └── pencil.png
```

**After processing:**
```
MyBrushes/
├── WatercolorBrushes/          (original folder)
├── WatercolorBrushes.brushset  (new zip file)
├── OilPaintBrushes/            (original folder)
├── OilPaintBrushes.brushset    (new zip file)
├── PencilBrushes/              (original folder)
└── PencilBrushes.brushset      (new zip file)
```

## Testing

### Run Unit Tests

```bash
python3 -m unittest discover tests -v
```

### Run Demo Script

To see the core functionality in action without the GUI:

```bash
python3 examples/demo.py
```

This creates a sample folder structure and processes it, demonstrating the brushset compilation logic.

## Project Structure

```
brushset-compiler/
├── src/
│   └── brushsetmaker/
│       ├── __init__.py       # Package initialization
│       ├── __main__.py       # Entry point for python -m
│       ├── app.py            # Main application code (Toga GUI)
│       └── resources/        # App resources (icons, etc.)
├── tests/
│   ├── test_brushsetmaker.py  # Basic module tests
│   └── test_zip_logic.py      # Zip functionality tests
├── examples/
│   └── demo.py               # Demonstration script
├── pyproject.toml            # Project configuration
├── README.md                 # User documentation
├── INSTRUCTIONS.md           # This file
├── LICENSE                   # MIT License
└── .gitignore               # Git ignore patterns
```

## Configuration

### pyproject.toml

The project configuration includes:

- **Project metadata**: name, version, description
- **Dependencies**: Briefcase and Toga
- **Briefcase configuration**: Bundle ID, formal name, descriptions
- **Platform-specific settings**: macOS requires toga-cocoa

### Customization

To customize the app:

1. **Change App Name**: Edit `formal_name` in `pyproject.toml`
2. **Change Bundle ID**: Edit `bundle` in `pyproject.toml`
3. **Add Icon**: Place icon files in `src/brushsetmaker/resources/`
4. **Modify UI**: Edit `src/brushsetmaker/app.py`

## Troubleshooting

### "No module named 'toga'" Error

**Solution**: Install dependencies with `uv sync`, then use `uv run briefcase dev`

### Briefcase Commands Fail

**Solution**: Always prefix briefcase commands with `uv run`:
```bash
uv run briefcase dev
```

### Permission Issues on macOS

**Solution**: After building, go to System Preferences > Security & Privacy and allow the app to run.

### Build Errors on First Run

**Solution**: Briefcase may need to download platform-specific tools on first run. This is normal and only happens once.

## Development

### Adding Dependencies

```bash
# Add a Python package
uv add package-name

# Sync dependencies
uv sync
```

### Modifying the Application

1. Edit `src/brushsetmaker/app.py`
2. Test with `uv run briefcase dev`
3. Run tests with `python3 -m unittest discover tests`
4. Build with `uv run briefcase build`

### Code Style

The application follows:
- PEP 8 style guidelines
- Descriptive variable and function names
- Comprehensive docstrings
- Type hints where applicable

## Platform Support

### Currently Supported

- **macOS**: Full support with native Cocoa GUI

### Potential Future Support

Briefcase and Toga support other platforms. To add support:

```bash
# For Windows
uv run briefcase create windows

# For Linux
uv run briefcase create linux
```

Update `pyproject.toml` to include platform-specific configurations.

## Resources

- **Toga Documentation**: https://toga.readthedocs.io/
- **Briefcase Documentation**: https://briefcase.readthedocs.io/
- **uv Documentation**: https://github.com/astral-sh/uv
- **Project Repository**: https://github.com/bepisdev/brushset-compiler

## License

MIT License - See LICENSE file for details.

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Submit a pull request
- Contact: dev@bepis.dev

## Quick Reference

| Task | Command |
|------|---------|
| Install dependencies | `uv sync` |
| Run in dev mode | `uv run briefcase dev` |
| Create app structure | `uv run briefcase create` |
| Build app | `uv run briefcase build` |
| Run built app | `uv run briefcase run` |
| Package for distribution | `uv run briefcase package` |
| Run tests | `python3 -m unittest discover tests` |
| Run demo | `python3 examples/demo.py` |
| Add dependency | `uv add package-name` |
| Update dependencies | `uv sync --upgrade` |
