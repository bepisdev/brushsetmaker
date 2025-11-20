"""Functional tests for brushset compilation logic."""

import unittest
import os
import zipfile
import tempfile
import shutil
from pathlib import Path


class TestBrushsetCompilation(unittest.TestCase):
    """Test the core brushset compilation logic."""

    def setUp(self):
        """Create temporary test directories."""
        self.test_dir = tempfile.mkdtemp()
        self.root_folder = Path(self.test_dir) / "test_root"
        self.root_folder.mkdir()

        # Create test subfolders with files
        self.brush_folders = []
        for i in range(3):
            folder = self.root_folder / f"BrushSet{i}"
            folder.mkdir()
            # Add some test files
            (folder / f"brush{i}_1.png").write_text("fake png data")
            (folder / f"brush{i}_2.png").write_text("fake png data")
            (folder / "metadata.json").write_text('{"name": "test"}')
            self.brush_folders.append(folder)

    def tearDown(self):
        """Clean up temporary directories."""
        shutil.rmtree(self.test_dir)

    def test_zip_subfolder(self):
        """Test that a subfolder can be zipped correctly."""
        subfolder = self.brush_folders[0]
        zip_path = self.root_folder / f"{subfolder.name}.brushset"

        # Create the zip
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in subfolder.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(subfolder)
                    zipf.write(file_path, arcname)

        # Verify the zip was created
        self.assertTrue(zip_path.exists())
        self.assertTrue(zip_path.suffix == '.brushset')

        # Verify contents
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            names = zipf.namelist()
            self.assertIn('brush0_1.png', names)
            self.assertIn('brush0_2.png', names)
            self.assertIn('metadata.json', names)
            self.assertEqual(len(names), 3)

    def test_multiple_subfolders(self):
        """Test that multiple subfolders can be processed."""
        created_brushsets = []

        for subfolder in self.brush_folders:
            zip_path = self.root_folder / f"{subfolder.name}.brushset"

            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in subfolder.rglob('*'):
                    if file_path.is_file():
                        arcname = file_path.relative_to(subfolder)
                        zipf.write(file_path, arcname)

            created_brushsets.append(zip_path)

        # Verify all brushsets were created
        self.assertEqual(len(created_brushsets), 3)
        for brushset in created_brushsets:
            self.assertTrue(brushset.exists())
            self.assertTrue(brushset.suffix == '.brushset')

    def test_empty_subfolder(self):
        """Test handling of empty subfolders."""
        empty_folder = self.root_folder / "EmptyBrushSet"
        empty_folder.mkdir()

        files = list(empty_folder.rglob('*'))
        # Should have no files
        self.assertEqual(len([f for f in files if f.is_file()]), 0)

    def test_nested_files(self):
        """Test that nested files in subfolders are included."""
        nested_folder = self.root_folder / "NestedBrushSet"
        nested_folder.mkdir()
        (nested_folder / "brush.png").write_text("data")

        sub_nested = nested_folder / "textures"
        sub_nested.mkdir()
        (sub_nested / "texture1.png").write_text("texture data")

        zip_path = self.root_folder / "NestedBrushSet.brushset"

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in nested_folder.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(nested_folder)
                    zipf.write(file_path, arcname)

        # Verify nested structure is preserved
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            names = zipf.namelist()
            self.assertIn('brush.png', names)
            self.assertIn('textures/texture1.png', names)


if __name__ == '__main__':
    unittest.main()
