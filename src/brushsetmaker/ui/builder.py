"""UI builder for the main application window."""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW # type: ignore


class UIBuilder:
    """Builds the main application UI."""

    @staticmethod
    def build_main_window(app):
        """Build and return the main window content."""
        # Create main container with sidebar and content area
        main_container = toga.Box(style=Pack(direction=ROW, flex=1))

        # Create sidebar
        sidebar = UIBuilder._build_sidebar(app)

        # Create content area container
        app.content_container = toga.Box(style=Pack(direction=COLUMN, flex=1, padding=(30, 30, 30, 20)))

        # Build all view sections
        app.single_view = UIBuilder._build_single_section(app)
        app.bulk_view = UIBuilder._build_bulk_section(app)
        app.brush_view = UIBuilder._build_brush_section(app)

        # Show single view by default
        app.content_container.add(app.single_view)
        app.current_view = "single"

        # Add sidebar and content to main container
        main_container.add(sidebar)
        main_container.add(app.content_container)

        return main_container

    @staticmethod
    def _build_sidebar(app):
        """Build the sidebar navigation menu."""
        sidebar = toga.Box(style=Pack(
            direction=COLUMN,
            padding=(20, 15, 20, 15),
            width=150
        ))

        # App title in sidebar
        title_label = toga.Label(
            "BrushsetMaker",
            style=Pack(padding=(0, 0, 3, 0), font_size=14, font_weight="bold")
        )

        subtitle_label = toga.Label(
            "Procreate Tools",
            style=Pack(padding=(0, 0, 25, 0), font_size=10)
        )

        sidebar.add(title_label)
        sidebar.add(subtitle_label)

        # Navigation buttons
        single_btn = toga.Button(
            "📦 Single",
            on_press=lambda w: UIBuilder._switch_view(app, "single"),
            style=Pack(padding=(0, 0, 8, 0), height=36)
        )

        bulk_btn = toga.Button(
            "⚡ Bulk",
            on_press=lambda w: UIBuilder._switch_view(app, "bulk"),
            style=Pack(padding=(0, 0, 8, 0), height=36)
        )

        brush_btn = toga.Button(
            "🖌️ Brush",
            on_press=lambda w: UIBuilder._switch_view(app, "brush"),
            style=Pack(padding=(0, 0, 8, 0), height=36)
        )

        sidebar.add(single_btn)
        sidebar.add(bulk_btn)
        sidebar.add(brush_btn)

        return sidebar

    @staticmethod
    def _switch_view(app, view_name):
        """Switch between different views."""
        # Remove current view
        if hasattr(app, 'current_view'):
            if app.current_view == "single":
                app.content_container.remove(app.single_view)
            elif app.current_view == "bulk":
                app.content_container.remove(app.bulk_view)
            elif app.current_view == "brush":
                app.content_container.remove(app.brush_view)

        # Add new view
        if view_name == "single":
            app.content_container.add(app.single_view)
        elif view_name == "bulk":
            app.content_container.add(app.bulk_view)
        elif view_name == "brush":
            app.content_container.add(app.brush_view)

        app.current_view = view_name

    @staticmethod
    def _build_single_section(app):
        """Build the single brushset section."""
        single_box = toga.Box(style=Pack(
            direction=COLUMN,
            padding=20
        ))

        single_label = toga.Label(
            "📦 Package Single Brushset",
            style=Pack(padding=(0, 0, 10, 0), font_size=24, font_weight="bold")
        )

        single_instructions = toga.Label(
            "Select a folder to package as a single .brushset file",
            style=Pack(padding=(0, 0, 15, 0), font_size=13)
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
            style=Pack(padding=(0, 0, 10, 0), font_size=24, font_weight="bold")
        )

        bulk_instructions = toga.Label(
            "Select a root folder containing subfolders. Each subfolder will be packaged as a .brushset",
            style=Pack(padding=(0, 0, 15, 0), font_size=13)
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

    @staticmethod
    def _build_brush_section(app):
        """Build the brush section (placeholder)."""
        brush_box = toga.Box(style=Pack(
            direction=COLUMN,
            padding=20
        ))

        brush_label = toga.Label(
            "🖌️ Brush Tools",
            style=Pack(padding=(0, 0, 10, 0), font_size=24, font_weight="bold")
        )

        brush_instructions = toga.Label(
            "Brush creation and editing tools coming soon...",
            style=Pack(padding=(0, 0, 15, 0), font_size=14)
        )

        brush_box.add(brush_label)
        brush_box.add(brush_instructions)

        return brush_box
