"""
BrushsetMaker - macOS utility to compile brushsets for Procreate.

Entry point for the application.
"""

import toga
from . import __version__
from .ui import UIBuilder
from .core import BrushsetHandlers
from .core.settings import Settings


class BrushsetMaker(toga.App):
    """Main application class for BrushsetMaker."""

    def startup(self):
        """Construct and show the Toga application."""
        # Initialize settings
        self.settings = Settings()

        # Build the main window UI
        main_box = UIBuilder.build_main_window(self)
        self.icon = "icon.icns"

        # Create the main window
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box # type: ignore
        self.main_window.show() #type: ignore

        # Initialize state
        self.selected_folder = None
        self.selected_single_folder = None
        self.progress_window = None

        # Add menu commands
        self._add_settings_command()
        self._add_file_menu_commands()

    def _add_settings_command(self):
        """Add settings/preferences command to app menu."""
        def open_settings_action(command, **kwargs):
            self._handle_open_settings(command)
            return True

        settings_cmd = toga.Command(
            open_settings_action,
            text="Preferences...",
            tooltip="Open application settings",
            group=toga.Group.APP,
            section=0
        )
        self.commands.add(settings_cmd)

    def _add_file_menu_commands(self):
        """Add file menu commands for folder selection."""
        def select_single_action(command, **kwargs):
            import asyncio
            asyncio.create_task(self._handle_create_single(command))
            return True

        def select_bulk_action(command, **kwargs):
            import asyncio
            asyncio.create_task(self._handle_select_bulk(command))
            return True

        select_single_cmd = toga.Command(
            select_single_action,
            text="Select Single Brushset Folder...",
            tooltip="Select a folder to package as a single brushset",
            group=toga.Group.FILE,
            section=1
        )

        select_bulk_cmd = toga.Command(
            select_bulk_action,
            text="Select Bulk Processing Folder...",
            tooltip="Select a root folder for bulk processing",
            group=toga.Group.FILE,
            section=1
        )

        self.commands.add(select_single_cmd)
        self.commands.add(select_bulk_cmd)

    # Handler wrappers to bridge UI callbacks to handler methods
    async def _handle_create_single(self, widget):
        """Wrapper for create single brushset handler."""
        await BrushsetHandlers.create_single_brushset(self, widget)

    async def _handle_compile_single(self, widget):
        """Wrapper for compile single brushset handler."""
        await BrushsetHandlers.compile_single_brushset(self, widget)

    async def _handle_edit_metadata(self, widget):
        """Wrapper for edit metadata handler."""
        await BrushsetHandlers.open_metadata_editor(self, widget)

    async def _handle_select_bulk(self, widget):
        """Wrapper for select bulk folder handler."""
        await BrushsetHandlers.select_bulk_folder(self, widget)

    async def _handle_process_folders(self, widget):
        """Wrapper for process folders handler."""
        await BrushsetHandlers.process_folders(self, widget)

    def _handle_open_settings(self, widget):
        """Open the settings dialog."""
        from .ui.settings_dialog import SettingsWindow
        settings_window = SettingsWindow(self)
        settings_window.show()


def main():
    """Entry point for the application."""
    app = BrushsetMaker(
        app_name='brushsetmaker',
        formal_name='BrushsetMaker',
        version=__version__,
        app_id='dev.bepis.brushsetmaker',
        author="Josh Burns",
        description="macOS utility to compile brushsets for Procreate",
        home_page="https://bepisdev.github.io/brushsetmaker/",
        icon='icon.icns'
    )
    return app


if __name__ == '__main__':
    main().main_loop()
