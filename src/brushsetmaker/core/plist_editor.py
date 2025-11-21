"""Plist editor window for editing brushset metadata."""

import plistlib
from pathlib import Path

import toga
from toga.style import Pack


class PlistEditorWindow:
    """Window for editing brushset metadata plist files."""

    def __init__(self, app, folder_path):
        """Initialize the plist editor window."""
        self.app = app
        self.folder_path = Path(folder_path)
        self.plist_path = self.folder_path / "brushset.plist"
        self.metadata = self._load_or_create_metadata()

        # Create the window
        self.window = toga.Window(title="Edit Brushset Metadata")
        self.window.content = self._build_editor_ui()

    def _load_or_create_metadata(self):
        """Load existing plist or create default metadata."""
        if self.plist_path.exists():
            try:
                with open(self.plist_path, 'rb') as f:
                    return plistlib.load(f)
            except Exception:
                # If plist is invalid, return default
                pass

        # Auto-detect brush folders (UUID format)
        brush_uuids = []
        for item in self.folder_path.iterdir():
            if item.is_dir() and self._is_uuid_format(item.name):
                brush_uuids.append(item.name)

        # Default metadata structure for Procreate brushsets
        return {
            'name': self.folder_path.name,
            'brushes': brush_uuids
        }

    def _is_uuid_format(self, name):
        """Check if string matches UUID format."""
        # UUID format: 8-4-4-4-12 hex digits
        parts = name.split('-')
        if len(parts) != 5:
            return False
        try:
            return (len(parts[0]) == 8 and len(parts[1]) == 4 and
                    len(parts[2]) == 4 and len(parts[3]) == 4 and len(parts[4]) == 12)
        except Exception:
            return False

    def _build_editor_ui(self):
        """Build the editor UI."""
        main_box = toga.Box(style=Pack(direction="column", padding=30))

        # Title
        title_label = toga.Label(
            "Brushset Metadata",
            style=Pack(padding=(0, 0, 20, 0), font_size=18, font_weight="bold")
        )

        # Name field
        name_box = self._create_field_row("Brushset Name:", self.metadata.get('name', ''))
        self.name_input = name_box.children[1]

        # Brushes info (read-only display)
        brushes_label = toga.Label(
            "Brushes:",
            style=Pack(padding=(10, 0, 5, 0), font_size=12, font_weight="bold")
        )

        brush_count = len(self.metadata.get('brushes', []))
        brushes_info = toga.Label(
            f"{brush_count} brush(es) detected in folder",
            style=Pack(padding=(0, 0, 15, 0), font_size=11)
        )

        # Buttons row
        button_box = toga.Box(style=Pack(direction="row", padding=(20, 0, 0, 0)))

        save_button = toga.Button(
            "Save Metadata",
            on_press=self._handle_save,
            style=Pack(padding=(0, 10, 0, 0), flex=1, height=40)
        )

        cancel_button = toga.Button(
            "Cancel",
            on_press=self._handle_cancel,
            style=Pack(padding=(0, 0, 0, 0), flex=1, height=40)
        )

        button_box.add(save_button)
        button_box.add(cancel_button)

        # Add all elements to main box
        main_box.add(title_label)
        main_box.add(name_box)
        main_box.add(brushes_label)
        main_box.add(brushes_info)
        main_box.add(button_box)

        return main_box

    def _create_field_row(self, label_text, value):
        """Create a labeled input field row."""
        row = toga.Box(style=Pack(direction="column", padding=(0, 0, 15, 0)))

        label = toga.Label(
            label_text,
            style=Pack(padding=(0, 0, 5, 0), font_size=12, font_weight="bold")
        )

        input_field = toga.TextInput(
            value=value,
            style=Pack(padding=(0, 0, 0, 0), width=500)
        )

        row.add(label)
        row.add(input_field)

        return row

    async def _handle_save(self, widget):
        """Save the metadata to plist file."""
        try:
            # Update only the name field, keep brushes array intact
            self.metadata['name'] = self.name_input.value

            # Write to plist file
            with open(self.plist_path, 'wb') as f:
                plistlib.dump(self.metadata, f)

            await self.app.main_window.info_dialog(
                "Success",
                "Metadata saved successfully!"
            )

            self.window.close()

        except Exception as e:
            await self.app.main_window.error_dialog(
                "Error",
                f"Failed to save metadata: {e}"
            )

    def _handle_cancel(self, widget):
        """Close the window without saving."""
        self.window.close()

    def show(self):
        """Show the editor window."""
        self.window.show()
