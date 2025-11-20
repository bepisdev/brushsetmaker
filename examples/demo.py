#!/usr/bin/env python3
"""
Example script demonstrating the brushset compilation logic.

This script creates a sample directory structure with brush files
and then processes them into .brushset files, just like the GUI app does.
"""

import os
import zipfile
import tempfile
import shutil
from pathlib import Path


def create_sample_structure():
    """Create a sample directory structure for testing."""
    # Create temporary directory
    test_dir = Path(tempfile.mkdtemp(prefix="brushset_example_"))
    root_folder = test_dir / "MyBrushes"
    root_folder.mkdir()

    print(f"Created test structure in: {root_folder}")
    print()

    # Create sample brush folders
    brush_sets = [
        ("WatercolorBrushes", ["brush1.png", "brush2.png", "metadata.json"]),
        ("OilPaintBrushes", ["brush1.png", "brush2.png", "brush3.png"]),
        ("PencilBrushes", ["pencil1.png", "pencil2.png"]),
    ]

    for folder_name, files in brush_sets:
        folder = root_folder / folder_name
        folder.mkdir()
        for file_name in files:
            (folder / file_name).write_text(f"Sample content for {file_name}")
        print(f"  Created: {folder_name}/ with {len(files)} files")

    print()
    return root_folder


def process_brushsets(root_folder):
    """Process all subfolders into .brushset files."""
    print("Processing brushsets...")
    print("=" * 60)

    subdirs = [d for d in root_folder.iterdir() if d.is_dir()]

    if not subdirs:
        print("No subfolders found!")
        return

    processed_count = 0

    for subdir in subdirs:
        print(f"Processing: {subdir.name}")

        # Create zip file
        zip_filename = f"{subdir.name}.brushset"
        zip_path = root_folder / zip_filename

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            files = list(subdir.rglob('*'))
            file_count = 0

            for file_path in files:
                if file_path.is_file():
                    arcname = file_path.relative_to(subdir)
                    zipf.write(file_path, arcname)
                    file_count += 1

            if file_count > 0:
                print(f"  ✓ Created: {zip_filename} ({file_count} files)")
                processed_count += 1
            else:
                print(f"  ⚠ Skipped: {subdir.name} (empty folder)")
                os.remove(zip_path)

    print("=" * 60)
    print(f"Successfully processed {processed_count} brushset(s)")
    print()
    return processed_count


def verify_brushsets(root_folder):
    """Verify the created brushset files."""
    print("Verifying created brushsets...")
    print()

    brushsets = list(root_folder.glob("*.brushset"))

    for brushset in brushsets:
        print(f"  {brushset.name}:")
        with zipfile.ZipFile(brushset, 'r') as zipf:
            names = zipf.namelist()
            for name in names:
                print(f"    - {name}")
        print()

    return len(brushsets)


def main():
    """Main example function."""
    print("BrushsetMaker - Example Script")
    print("=" * 60)
    print()

    # Create sample structure
    root_folder = create_sample_structure()

    # Process brushsets
    process_brushsets(root_folder)

    # Verify results
    brushset_count = verify_brushsets(root_folder)

    # Show final directory listing
    print("Final directory contents:")
    print(f"  Location: {root_folder}")
    print()
    for item in sorted(root_folder.iterdir()):
        if item.is_dir():
            print(f"  📁 {item.name}/")
        else:
            size = item.stat().st_size
            print(f"  📦 {item.name} ({size} bytes)")

    print()
    print("=" * 60)
    print(f"✅ Example complete! Created {brushset_count} .brushset file(s)")
    print(f"📁 Files are in: {root_folder}")
    print()
    print("Note: This is a temporary directory. Files will be cleaned up")
    print("when your temp directory is purged by the system.")


if __name__ == "__main__":
    main()
