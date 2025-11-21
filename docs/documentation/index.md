---
layout: page
title: Documentation
subtitle: Complete guide to using BrushsetMaker
toc: true
---

## Overview

BrushsetMaker is a macOS application designed to compile Procreate brushsets from organized folder structures. This guide will help you get the most out of the application.

## Getting Started

### Installation

Follow the [download instructions](/brushsetmaker/download) to install BrushsetMaker on your Mac. Once installed, the application will be available in your Applications folder.

### First Launch

On your first launch, macOS may display a security warning. This is normal for applications not distributed through the Mac App Store. Simply:

1. Right-click the application
2. Select "Open"
3. Click "Open" again in the confirmation dialog

## How to Use BrushsetMaker

### Basic Workflow

The typical workflow for using BrushsetMaker involves these steps:

1. **Organize Your Brushes**: Create a folder structure where each subfolder contains the brush files you want to package
2. **Select Root Folder**: Launch BrushsetMaker and select the parent folder containing your brush subfolders
3. **Process**: Click the process button and watch the status log
4. **Import**: Use the generated `.brushset` files in Procreate

### Folder Structure

BrushsetMaker expects a specific folder structure:

```
Root Folder/
├── Brush Set 1/
│   ├── brush1.brush
│   ├── brush2.brush
│   └── brush3.brush
├── Brush Set 2/
│   ├── brush4.brush
│   └── brush5.brush
└── Brush Set 3/
    └── brush6.brush
```

**Output:**

- `Brush Set 1.brushset`
- `Brush Set 2.brushset`
- `Brush Set 3.brushset`

### Selecting Folders

1. Click the **"Select Folder"** button in the application
2. Navigate to your root brush folder
3. Click **"Choose"** to confirm your selection

The application will display the selected path in the interface.

### Processing Brushsets

Once you've selected a folder:

1. Click the **"Process"** or **"Create Brushsets"** button
2. Watch the status log for real-time progress updates
3. Wait for the "Complete" message

The application will:

- Scan all subfolders in your selected directory
- Create a zip archive of each subfolder's contents
- Rename the archives with the `.brushset` extension
- Display success or error messages in the log

### Status Log

The status log provides detailed information about the processing:

- **Info messages**: General progress updates
- **Success messages**: Completed operations
- **Warning messages**: Non-critical issues
- **Error messages**: Problems that need attention

The log is scrollable and automatically focuses on the most recent message.

## Advanced Usage

### Custom Naming

The brushset files are automatically named after their parent folder. To customize names:

1. Rename the source folders before processing
2. The output `.brushset` files will reflect the new names

### Batch Processing

BrushsetMaker processes all subfolders in the selected directory. For batch operations:

1. Organize multiple brush collections in subfolders
2. Select the parent folder
3. Process once to create all brushsets simultaneously

### File Locations

By default, BrushsetMaker creates `.brushset` files in the same directory as their source folders.

## Importing to Procreate

After creating brushsets:

1. **Transfer to iPad**: Use AirDrop, iCloud Drive, or any file transfer method
2. **Open in Procreate**: Tap the `.brushset` file on your iPad
3. **Import**: Procreate will automatically import the brush collection
4. **Verify**: Check the brush library to confirm successful import

## Troubleshooting

### Common Issues

#### "Permission Denied" Errors

**Problem**: The application can't access the selected folder.

**Solution**:

- Ensure the folder isn't in a restricted location (like System directories)
- Grant full disk access to BrushsetMaker in System Preferences > Security & Privacy
- Try selecting a folder in your user directory (Documents, Desktop, etc.)

#### "No Subfolders Found"

**Problem**: The application doesn't detect any subfolders to process.

**Solution**:

- Verify your folder structure matches the expected format
- Ensure subfolders exist in the selected directory
- Check that subfolders contain brush files

#### Brushsets Won't Import to Procreate

**Problem**: The generated `.brushset` files don't work in Procreate.

**Solution**:

- Verify the source files are valid Procreate brush files (`.brush` extension)
- Check that the `.brushset` files aren't corrupted
- Try regenerating the brushset
- Ensure you're using a compatible version of Procreate

#### Application Crashes on Launch

**Problem**: BrushsetMaker won't start or crashes immediately.

**Solution**:

- Check system requirements (macOS 11.0 or later)
- Remove and reinstall the application
- Check Console.app for error messages
- Report the issue on GitHub with crash logs

### Performance Issues

If processing is slow:

- Reduce the number of subfolders processed at once
- Close other resource-intensive applications
- Ensure adequate disk space is available
- Process smaller brush collections individually

### Getting Help

If you can't resolve your issue:

1. **Check existing documentation**: Review all sections of this guide
2. **Search GitHub Issues**: Look for similar problems and solutions
3. **Open a new issue**: Provide detailed information about your problem
4. **Include system details**: macOS version, application version, error messages

## Technical Details

### Built With

BrushsetMaker is built using modern Python tools:

- **Python 3.12+**: Core programming language
- **Toga**: Native GUI framework
- **Briefcase**: Application packaging and distribution
- **uv**: Fast, reliable Python package management

### File Format

The `.brushset` format is essentially a renamed `.zip` archive containing individual `.brush` files and metadata. BrushsetMaker creates standards-compliant archives that Procreate recognizes and imports.

### Source Code

The full source code is available on [GitHub](https://github.com/bepisdev/brushsetmaker). Contributions, bug reports, and feature requests are welcome!

## Best Practices

### Organization Tips

1. **Use descriptive folder names**: These become your brushset names
2. **Group related brushes**: Keep similar brushes in the same folder
3. **Test small batches first**: Verify the process works before processing large collections
4. **Keep backups**: Always maintain copies of your original brush files

### Workflow Optimization

1. **Prepare folders in advance**: Organize all brush files before launching the app
2. **Process in stages**: Break large collections into manageable batches
3. **Verify output**: Check generated brushsets before transferring to iPad
4. **Document your organization**: Keep notes on your folder structure for future reference

## FAQ

### Is BrushsetMaker free?

Yes! BrushsetMaker is completely free and open source.

### Does it work on Windows or Linux?

Currently, BrushsetMaker is macOS-only. However, the source code is available if you want to adapt it for other platforms.

### Can I distribute brushsets created with BrushsetMaker?

Yes! The brushsets you create are yours to use, share, or sell as you wish.

### How do I update BrushsetMaker?

Download the latest version from the [releases page](/brushsetmaker/download) and replace the old application in your Applications folder.

### Can I contribute to the project?

Absolutely! Visit the [GitHub repository](https://github.com/bepisdev/brushsetmaker) to contribute code, report bugs, or suggest features. Read the [Contributor Documentation](/brushsetmaker/documentation/contribute) to read about the guidelines and best practices for contributing to the project.

---

<div style="background-color: var(--bg-secondary); padding: 1.5rem; border-radius: 0.75rem; margin-top: 3rem;">
  <h4>📚 Need More Help?</h4>
  <p>Still have questions? Check out our <a href="https://github.com/bepisdev/brushsetmaker/issues">GitHub Issues</a> page or <a href="https://github.com/bepisdev/brushsetmaker/discussions">start a discussion</a> with the community.</p>
</div>
