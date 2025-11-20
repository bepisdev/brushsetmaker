# BrushsetMaker

A macOS application to compile brushsets for Procreate. Built with Python, Toga, and Briefcase, managed with uv.

## Screenshot

![BrushsetMaker Application](screenshot.png)

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

### Download the latest release

You can download the latest release from [here](https://github.com/bepisdev/brushsetmaker/tags).

### Build From Source

#### 1. Install uv

```bash
pip install uv
```

#### 2. Clone the repository

```bash
git clone https://github.com/bepisdev/brushsetmaker.git
cd brushsetmaker
```

#### 3. Install dependencies

```bash
uv sync
```

#### 4. Build app

```bash
uv run briefcase build
uv run briefcase package
```

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

## v1.0 TODO
- [x] App Icon
- [x] Better metadata
- [x] Code organisation and seperation
- [ ] Top menu bar
- [ ] `.plist` editor / brushset customization
- [ ] Update and improve website
- [ ] Move website to seperate branch
- [ ] Script release prep (increment semver based on flag, create zip of .app and move .zip and .dmg to a 'release' folder in root)
- [ ] Proper 'about' prompt
- [ ] Improved UI with seperate screens for multiple features
