# BrushsetMaker

A macOS GUI application to compile brushsets for Procreate. Built with Python, Toga, and Briefcase, managed with uv.

## Features

- 🎨 Select a root folder containing brush subfolders
- 📦 Automatically zip each subfolder's contents
- 🏷️ Rename zipped files to `.brushset` extension
- 📊 Real-time status logging in a scrollable interface
- 🖥️ Native macOS GUI built with Toga

## Requirements

- Python 3.12+
- uv (Python package manager)
- macOS (for building native app)

## Installation

### 1. Install uv

```bash
pip install uv
```

### 2. Clone the repository

```bash
git clone https://github.com/bepisdev/brushset-compiler.git
cd brushset-compiler
```

### 3. Install dependencies

```bash
uv sync
```

## Running the Application

### Development Mode

Run the application in development mode using uv:

```bash
uv run briefcase dev
```

This will start the application in developer mode with hot-reload capabilities.

### Alternative: Direct Python execution

```bash
uv run python src/brushsetmaker/app.py
```

## Building the Application

### Build for macOS

To create a standalone macOS application:

```bash
# Create the Xcode project
uv run briefcase create

# Build the app
uv run briefcase build

# Run the built app
uv run briefcase run
```

### Package the Application

To create a distributable .dmg file:

```bash
uv run briefcase package
```

The packaged application will be available in the `macOS/` directory.

## Usage

1. **Launch the application**
2. **Click "Select Root Folder"** - Choose a folder containing subfolders with brush files
3. **Click "Process Folders"** - The app will:
   - Scan all subfolders in the selected directory
   - Create a `.brushset` (zip) file for each subfolder
   - Include all files from each subfolder in the respective zip
   - Display progress and results in the log area

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## TODO
- [ ] App Icon
- [ ] Better metadata
- [ ] Top menu bar
- [ ] `.plist` editor / brushset customization