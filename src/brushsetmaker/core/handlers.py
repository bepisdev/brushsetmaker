"""Event handlers for BrushsetMaker application."""

import zipfile
from pathlib import Path


class BrushsetHandlers:
    """Handles all application event logic."""

    @staticmethod
    async def create_single_brushset(app, widget):
        """Create a single brushset from a selected folder."""
        try:
            # Open folder selection dialog
            folder_path = await app.main_window.select_folder_dialog(
                title="Select Folder to Package"
            )

            if not folder_path:
                return

            folder = Path(folder_path)
            
            # Check if folder has files
            files = list(folder.rglob('*'))
            if not files:
                await app.main_window.error_dialog("Error", "Selected folder is empty.")
                return

            # Ask where to save the brushset
            save_path = await app.main_window.save_file_dialog(
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

            await app.main_window.info_dialog(
                "Success",
                f"Brushset created successfully:\n{save_path.name}"
            )

        except Exception as e:
            await app.main_window.error_dialog("Error", f"Error creating brushset: {e}")

    @staticmethod
    async def select_bulk_folder(app, widget):
        """Handle bulk folder selection."""
        try:
            # Open folder selection dialog
            folder_path = await app.main_window.select_folder_dialog(
                title="Select Root Folder"
            )

            if folder_path:
                app.selected_folder = folder_path
                app.folder_label.text = f"Selected: {Path(folder_path).name}"
                app.process_button.enabled = True
            else:
                app.folder_label.text = "No folder selected"

        except Exception as e:
            await app.main_window.error_dialog("Error", f"Error selecting folder: {e}")

    @staticmethod
    def create_progress_window(app, total):
        """Create a progress window."""
        from toga.style import Pack
        from toga.style.pack import COLUMN
        import toga
        
        # Create progress window
        app.progress_window = toga.Window(title="Processing Brushsets")
        
        # Create content box with better spacing
        progress_box = toga.Box(style=Pack(
            direction=COLUMN,
            padding=40
        ))
        
        # Status label
        app.progress_label = toga.Label(
            f"Processing 0 of {total} folders...",
            style=Pack(padding=(0, 0, 20, 0), font_size=14, font_weight="bold")
        )
        
        # Progress bar
        app.progress_bar = toga.ProgressBar(
            max=total,
            style=Pack(padding=(0, 0, 15, 0), width=500, height=10)
        )
        
        # Current folder label
        app.current_folder_label = toga.Label(
            "",
            style=Pack(padding=(0, 0, 0, 0), font_size=12)
        )
        
        progress_box.add(app.progress_label)
        progress_box.add(app.progress_bar)
        progress_box.add(app.current_folder_label)
        
        app.progress_window.content = progress_box
        app.progress_window.show()

    @staticmethod
    async def process_folders(app, widget):
        """Process all subfolders in the selected root folder."""
        if not app.selected_folder:
            await app.main_window.error_dialog("Error", "No folder selected. Please select a folder first.")
            return

        try:
            root_path = Path(app.selected_folder)

            # Get all subdirectories
            subdirs = [d for d in root_path.iterdir() if d.is_dir()]

            if not subdirs:
                await app.main_window.info_dialog("No Folders", "No subfolders found in the selected directory.")
                return

            # Create and show progress window
            BrushsetHandlers.create_progress_window(app, len(subdirs))

            processed_count = 0
            error_count = 0
            errors = []

            for idx, subdir in enumerate(subdirs, 1):
                try:
                    app.current_folder_label.text = f"Processing: {subdir.name}"
                    app.progress_label.text = f"Processing {idx} of {len(subdirs)} folders..."
                    
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
                app.progress_bar.value = idx

            # Close progress window
            app.progress_window.close()
            app.progress_window = None

            # Show completion dialog
            if error_count > 0:
                error_details = "\n".join(errors[:5])  # Show first 5 errors
                if len(errors) > 5:
                    error_details += f"\n... and {len(errors) - 5} more errors"
                await app.main_window.info_dialog(
                    "Processing Complete",
                    f"Successfully processed: {processed_count}\nErrors: {error_count}\n\nErrors:\n{error_details}"
                )
            else:
                await app.main_window.info_dialog(
                    "Success",
                    f"Successfully processed all {processed_count} brushsets!"
                )

        except Exception as e:
            if app.progress_window:
                app.progress_window.close()
                app.progress_window = None
            await app.main_window.error_dialog("Error", f"Fatal error: {e}")
