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
from . import __version__


class BrushsetMaker(toga.App):
    """Main application class for BrushsetMaker."""

    def startup(self):
        """Construct and show the Toga application."""
        # Main box container with macOS-style padding
        main_box = toga.Box(style=Pack(direction=COLUMN, padding=30))

        # Title section
        title_label = toga.Label(
            "BrushsetMaker",
            style=Pack(padding=(0, 0, 5, 0), font_size=24, font_weight="bold")
        )
        
        subtitle_label = toga.Label(
            "Procreate Brushset Compiler",
            style=Pack(padding=(0, 0, 20, 0), font_size=13)
        )

        # Single brushset section
        single_box = toga.Box(style=Pack(
            direction=COLUMN,
            padding=20
        ))
        
        single_label = toga.Label(
            "📦 Package Single Brushset",
            style=Pack(padding=(0, 0, 10, 0), font_size=16, font_weight="bold")
        )
        
        single_instructions = toga.Label(
            "Select a folder to package as a single .brushset file",
            style=Pack(padding=(0, 0, 15, 0), font_size=12)
        )

        single_button = toga.Button(
            "Select Folder & Create Brushset",
            on_press=self.create_single_brushset,
            style=Pack(padding=(0, 0, 0, 0), width=300, height=40)
        )
        
        single_box.add(single_label)
        single_box.add(single_instructions)
        single_box.add(single_button)

        # Bulk processing section
        bulk_box = toga.Box(style=Pack(
            direction=COLUMN,
            padding=20
        ))
        
        bulk_label = toga.Label(
            "⚡ Bulk Process Brushsets",
            style=Pack(padding=(0, 0, 10, 0), font_size=16, font_weight="bold")
        )

        bulk_instructions = toga.Label(
            "Select a root folder containing subfolders. Each subfolder will be packaged as a .brushset",
            style=Pack(padding=(0, 0, 15, 0), font_size=12)
        )

        # Button row
        button_row = toga.Box(style=Pack(direction=ROW, padding=(0, 0, 10, 0)))
        
        select_button = toga.Button(
            "Select Root Folder",
            on_press=self.select_bulk_folder,
            style=Pack(padding=(0, 5, 0, 0), flex=1, height=36)
        )
        
        button_row.add(select_button)

        # Selected folder label
        self.folder_label = toga.Label(
            "No folder selected",
            style=Pack(padding=(0, 0, 15, 0), font_size=11)
        )

        # Process button
        self.process_button = toga.Button(
            "Process All Subfolders",
            on_press=self.process_folders,
            enabled=False,
            style=Pack(padding=(0, 0, 0, 0), width=300, height=40)
        )
        
        bulk_box.add(bulk_label)
        bulk_box.add(bulk_instructions)
        bulk_box.add(button_row)
        bulk_box.add(self.folder_label)
        bulk_box.add(self.process_button)

        # Add all widgets to main box with proper spacing
        main_box.add(title_label)
        main_box.add(subtitle_label)
        
        # Add divider
        divider1 = toga.Divider(style=Pack(padding=(0, 0, 20, 0)))
        main_box.add(divider1)
        
        main_box.add(single_box)
        
        # Add divider between sections
        divider2 = toga.Divider(style=Pack(padding=(20, 0, 20, 0)))
        main_box.add(divider2)
        
        main_box.add(bulk_box)

        # Create the main window
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

        # Initialize selected folder
        self.selected_folder = None
        self.progress_window = None

    async def create_single_brushset(self, widget):
        """Create a single brushset from a selected folder."""
        try:
            # Open folder selection dialog
            folder_path = await self.main_window.select_folder_dialog(
                title="Select Folder to Package"
            )

            if not folder_path:
                return

            folder = Path(folder_path)
            
            # Check if folder has files
            files = list(folder.rglob('*'))
            if not files:
                await self.main_window.error_dialog("Error", "Selected folder is empty.")
                return

            # Ask where to save the brushset
            save_path = await self.main_window.save_file_dialog(
                title="Save Brushset As",
                suggested_filename=f"{folder.name}.brushset",
                file_types=['brushset']
            )

            if not save_path:
                return

            # Ensure .brushset extension
            save_path = Path(save_path)
            if save_path.suffix != '.brushset':
                save_path = save_path.with_suffix('.brushset')

            # Create the brushset
            with zipfile.ZipFile(save_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in files:
                    if file_path.is_file():
                        arcname = file_path.relative_to(folder)
                        zipf.write(file_path, arcname)

            await self.main_window.info_dialog(
                "Success",
                f"Brushset created successfully:\n{save_path.name}"
            )

        except Exception as e:
            await self.main_window.error_dialog("Error", f"Error creating brushset: {e}")

    async def select_bulk_folder(self, widget):
        """Handle bulk folder selection."""
        try:
            # Open folder selection dialog
            folder_path = await self.main_window.select_folder_dialog(
                title="Select Root Folder"
            )

            if folder_path:
                self.selected_folder = folder_path
                self.folder_label.text = f"Selected: {Path(folder_path).name}"
                self.process_button.enabled = True
            else:
                self.folder_label.text = "No folder selected"

        except Exception as e:
            await self.main_window.error_dialog("Error", f"Error selecting folder: {e}")

    def create_progress_window(self, total):
        """Create a progress window."""
        # Create progress window
        self.progress_window = toga.Window(title="Processing Brushsets")
        
        # Create content box with better spacing
        progress_box = toga.Box(style=Pack(
            direction=COLUMN,
            padding=40
        ))
        
        # Status label
        self.progress_label = toga.Label(
            f"Processing 0 of {total} folders...",
            style=Pack(padding=(0, 0, 20, 0), font_size=14, font_weight="bold")
        )
        
        # Progress bar
        self.progress_bar = toga.ProgressBar(
            max=total,
            style=Pack(padding=(0, 0, 15, 0), width=500, height=10)
        )
        
        # Current folder label
        self.current_folder_label = toga.Label(
            "",
            style=Pack(padding=(0, 0, 0, 0), font_size=12)
        )
        
        progress_box.add(self.progress_label)
        progress_box.add(self.progress_bar)
        progress_box.add(self.current_folder_label)
        
        self.progress_window.content = progress_box
        self.progress_window.show()

    async def process_folders(self, widget):
        """Process all subfolders in the selected root folder."""
        if not self.selected_folder:
            await self.main_window.error_dialog("Error", "No folder selected. Please select a folder first.")
            return

        try:
            root_path = Path(self.selected_folder)

            # Get all subdirectories
            subdirs = [d for d in root_path.iterdir() if d.is_dir()]

            if not subdirs:
                await self.main_window.info_dialog("No Folders", "No subfolders found in the selected directory.")
                return

            # Create and show progress window
            self.create_progress_window(len(subdirs))

            processed_count = 0
            error_count = 0
            errors = []

            for idx, subdir in enumerate(subdirs, 1):
                try:
                    self.current_folder_label.text = f"Processing: {subdir.name}"
                    self.progress_label.text = f"Processing {idx} of {len(subdirs)} folders..."
                    
                    # Create zip file path
                    zip_filename = f"{subdir.name}.brushset"
                    zip_path = root_path / zip_filename

                    # Create zip file
                    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        # Get all files in the subfolder
                        files = list(subdir.rglob('*'))

                        if not files:
                            errors.append(f"{subdir.name}: Folder is empty")
                            error_count += 1
                            continue

                        # Add each file to the zip
                        for file_path in files:
                            if file_path.is_file():
                                # Calculate relative path from subfolder
                                arcname = file_path.relative_to(subdir)
                                zipf.write(file_path, arcname)

                    processed_count += 1

                except Exception as e:
                    errors.append(f"{subdir.name}: {str(e)}")
                    error_count += 1

                # Update progress bar
                self.progress_bar.value = idx

            # Close progress window
            self.progress_window.close()
            self.progress_window = None

            # Show completion dialog
            if error_count > 0:
                error_details = "\n".join(errors[:5])  # Show first 5 errors
                if len(errors) > 5:
                    error_details += f"\n... and {len(errors) - 5} more errors"
                await self.main_window.info_dialog(
                    "Processing Complete",
                    f"Successfully processed: {processed_count}\nErrors: {error_count}\n\nErrors:\n{error_details}"
                )
            else:
                await self.main_window.info_dialog(
                    "Success",
                    f"Successfully processed all {processed_count} brushsets!"
                )

        except Exception as e:
            if self.progress_window:
                self.progress_window.close()
                self.progress_window = None
            await self.main_window.error_dialog("Error", f"Fatal error: {e}")


def main():
    """Entry point for the application."""
    app = BrushsetMaker(
        app_name='brushsetmaker',
        formal_name='BrushsetMaker',
        version=__version__,
        app_id='dev.bepis.brushsetmaker',
        author="Josh Burns",
        description="macOS utility to compile brushsets for Procreate",
    )
    return app


if __name__ == '__main__':
    main().main_loop()
