"""
BrushsetMaker - macOS utility to compile brushsets for Procreate.

This application allows users to:
1. Select a root folder containing subfolders
2. Automatically zip each subfolder's contents
3. Rename each zip file with the .brushset extension
4. View processing status in real-time
"""

import os
import zipfile
from pathlib import Path
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class BrushsetMaker(toga.App):
    """Main application class for BrushsetMaker."""

    def startup(self):
        """Construct and show the Toga application."""
        # Main box container
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

        # Title label
        title_label = toga.Label(
            "BrushsetMaker - Procreate Brushset Compiler",
            style=Pack(padding=(0, 5), font_size=16, font_weight="bold")
        )

        # Instructions label
        instructions = toga.Label(
            "Select a root folder containing subfolders. Each subfolder will be zipped and renamed to .brushset",
            style=Pack(padding=(5, 5), font_size=11)
        )

        # Folder selection button
        select_button = toga.Button(
            "Select Root Folder",
            on_press=self.select_folder,
            style=Pack(padding=5, width=200)
        )

        # Status log area (multiline text input for display)
        self.log_display = toga.MultilineTextInput(
            readonly=True,
            placeholder="Status logs will appear here...",
            style=Pack(flex=1, padding=5, height=300)
        )

        # Process button
        self.process_button = toga.Button(
            "Process Folders",
            on_press=self.process_folders,
            enabled=False,
            style=Pack(padding=5, width=200)
        )

        # Add all widgets to main box
        main_box.add(title_label)
        main_box.add(instructions)
        main_box.add(select_button)
        main_box.add(self.log_display)
        main_box.add(self.process_button)

        # Create the main window
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

        # Initialize selected folder
        self.selected_folder = None

    def log(self, message):
        """Add a message to the log display."""
        current_text = self.log_display.value or ""
        self.log_display.value = current_text + message + "\n"

    async def select_folder(self, widget):
        """Handle folder selection."""
        try:
            # Open folder selection dialog
            folder_path = await self.main_window.select_folder_dialog(
                title="Select Root Folder"
            )

            if folder_path:
                self.selected_folder = folder_path
                self.log(f"Selected folder: {folder_path}")
                self.process_button.enabled = True
            else:
                self.log("No folder selected.")

        except Exception as e:
            self.log(f"Error selecting folder: {e}")

    async def process_folders(self, widget):
        """Process all subfolders in the selected root folder."""
        if not self.selected_folder:
            self.log("No folder selected. Please select a folder first.")
            return

        self.log("\n" + "=" * 50)
        self.log("Starting brushset compilation...")
        self.log("=" * 50)

        try:
            root_path = Path(self.selected_folder)

            # Get all subdirectories
            subdirs = [d for d in root_path.iterdir() if d.is_dir()]

            if not subdirs:
                self.log("No subfolders found in the selected directory.")
                return

            self.log(f"Found {len(subdirs)} subfolder(s) to process.")
            self.log("")

            processed_count = 0
            error_count = 0

            for subdir in subdirs:
                try:
                    self.log(f"Processing: {subdir.name}")

                    # Create zip file path
                    zip_filename = f"{subdir.name}.brushset"
                    zip_path = root_path / zip_filename

                    # Create zip file
                    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        # Get all files in the subfolder
                        files = list(subdir.rglob('*'))

                        if not files:
                            self.log(f"  Warning: {subdir.name} is empty, skipping.")
                            continue

                        # Add each file to the zip
                        for file_path in files:
                            if file_path.is_file():
                                # Calculate relative path from subfolder
                                arcname = file_path.relative_to(subdir)
                                zipf.write(file_path, arcname)

                    self.log(f"  ✓ Created: {zip_filename}")
                    processed_count += 1

                except Exception as e:
                    self.log(f"  ✗ Error processing {subdir.name}: {e}")
                    error_count += 1

            # Summary
            self.log("")
            self.log("=" * 50)
            self.log(f"Compilation complete!")
            self.log(f"Successfully processed: {processed_count}")
            if error_count > 0:
                self.log(f"Errors encountered: {error_count}")
            self.log("=" * 50)

        except Exception as e:
            self.log(f"Fatal error: {e}")


def main():
    """Entry point for the application."""
    return BrushsetMaker(
        'brushsetmaker',
        'dev.bepis.brushsetmaker',
        description="macOS utility to compile brushsets for Procreate"
    )


if __name__ == '__main__':
    main().main_loop()
