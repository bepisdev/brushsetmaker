"""UI builder for the main application window."""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW # type: ignore


class UIBuilder:
    """Builds the main application UI."""

    @staticmethod
    def build_main_window(app):
        """Build and return the main window content."""
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
        single_box = UIBuilder._build_single_section(app)

        # Bulk processing section
        bulk_box = UIBuilder._build_bulk_section(app)

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

        return main_box

    @staticmethod
    def _build_single_section(app):
        """Build the single brushset section."""
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
            "Select Folder",
            on_press=app._handle_create_single,
            style=Pack(padding=(0, 0, 0, 0), width=300, height=40)
        )

        # Selected folder label (hidden initially)
        app.single_folder_label = toga.Label(
            "",
            style=Pack(padding=(15, 0, 15, 0), font_size=11)
        )

        # Action buttons row (hidden initially)
        app.single_actions_box = toga.Box(style=Pack(direction=ROW, padding=(0, 0, 0, 0)))

        app.compile_button = toga.Button(
            "Create Brushset",
            on_press=app._handle_compile_single,
            style=Pack(padding=(0, 5, 0, 0), flex=1, height=40)
        )

        app.edit_metadata_button = toga.Button(
            "Edit Metadata",
            on_press=app._handle_edit_metadata,
            style=Pack(padding=(0, 0, 0, 0), flex=1, height=40)
        )

        app.single_actions_box.add(app.compile_button)
        app.single_actions_box.add(app.edit_metadata_button)

        single_box.add(single_label)
        single_box.add(single_instructions)
        single_box.add(single_button)
        single_box.add(app.single_folder_label)
        single_box.add(app.single_actions_box)

        return single_box

    @staticmethod
    def _build_bulk_section(app):
        """Build the bulk processing section."""
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
            on_press=app._handle_select_bulk,
            style=Pack(padding=(0, 5, 0, 0), flex=1, height=36)
        )

        button_row.add(select_button)

        # Selected folder label
        app.folder_label = toga.Label(
            "No folder selected",
            style=Pack(padding=(0, 0, 15, 0), font_size=11)
        )

        # Process button
        app.process_button = toga.Button(
            "Process All Subfolders",
            on_press=app._handle_process_folders,
            enabled=False,
            style=Pack(padding=(0, 0, 0, 0), width=300, height=40)
        )

        bulk_box.add(bulk_label)
        bulk_box.add(bulk_instructions)
        bulk_box.add(button_row)
        bulk_box.add(app.folder_label)
        bulk_box.add(app.process_button)

        return bulk_box
