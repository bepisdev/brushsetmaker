---
layout: page
title: Download BrushsetMaker
subtitle: Get the latest version for macOS
---

## Latest Release

Download the most recent version of BrushsetMaker for macOS. The application is distributed as a native macOS app bundle, ready to run on your system.

<div style="background: linear-gradient(135deg, var(--primary-color), var(--accent-color)); padding: 2rem; border-radius: 1rem; text-align: center; margin: 2rem 0; color: white;">
  <h3 style="color: white; margin-bottom: 1rem;">BrushsetMaker v0.2.0</h3>
  <p style="color: rgba(255, 255, 255, 0.9); margin-bottom: 1.5rem;">The latest stable release for macOS</p>
  <a href="https://github.com/bepisdev/brushsetmaker/releases/latest" class="btn btn-primary btn-lg" style="background-color: white; color: var(--primary-color);">
    Download for macOS
  </a>
</div>

## System Requirements

- **Operating System**: macOS 11.0 (Big Sur) or later
- **Architecture**: Apple Silicon (M1/M2/M3) or Intel
- **Disk Space**: ~50 MB
- **Memory**: 512 MB RAM minimum

## Installation Instructions

### Download Method

1. **Download** the latest `.dmg` file from the [releases page](https://github.com/bepisdev/brushsetmaker/releases)
2. **Open** the downloaded `.dmg` file
3. **Drag** BrushsetMaker.app to your Applications folder
4. **Launch** BrushsetMaker from your Applications folder

> **Note**: On first launch, you may need to right-click the app and select "Open" to bypass macOS Gatekeeper security settings.

### Build from Source

If you prefer to build from source or want the latest development version:

```bash
# Install uv (if not already installed)
pip install uv

# Clone the repository
git clone https://github.com/bepisdev/brushsetmaker.git
cd brushsetmaker

# Install dependencies
uv sync

# Build the app
make build
```

The built application will be available in the `build/brushsetmaker/macos/app/` directory.

## What's New

Check out the [changelog](https://github.com/bepisdev/brushsetmaker/blob/main/CHANGELOG.md) to see what's new in each release, including bug fixes, new features, and improvements.

## Previous Versions

Looking for an older version? All previous releases are available on the [GitHub releases page](https://github.com/bepisdev/brushsetmaker/releases).

## Troubleshooting

### "App is damaged and can't be opened"

This error occurs when macOS Gatekeeper blocks unsigned applications. To resolve:

1. Right-click the app in Applications
2. Select "Open" from the context menu
3. Click "Open" in the confirmation dialog

Alternatively, you can remove the quarantine flag:

```bash
xattr -cr /Applications/BrushsetMaker.app
```

### App won't launch

Ensure you're running macOS 11.0 or later. Check the system requirements above and verify your macOS version in System Preferences.

### Other Issues

If you encounter other issues, please:

1. Check the [documentation](/brushsetmaker/documentation) for common solutions
2. Search [existing issues](https://github.com/bepisdev/brushsetmaker/issues) on GitHub
3. [Open a new issue](https://github.com/bepisdev/brushsetmaker/issues/new) if your problem isn't already reported

## Stay Updated

- **GitHub**: [Watch the repository](https://github.com/bepisdev/brushsetmaker) to get notified of new releases
- **RSS**: Subscribe to the [releases feed](https://github.com/bepisdev/brushsetmaker/releases.atom)

---

<div style="background-color: var(--bg-secondary); padding: 1.5rem; border-radius: 0.75rem; margin-top: 2rem;">
  <h4>💡 Pro Tip</h4>
  <p>Enable automatic updates by watching the GitHub repository. You'll receive notifications whenever a new version is released!</p>
</div>
