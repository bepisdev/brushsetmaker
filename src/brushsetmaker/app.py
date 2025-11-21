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

        # Add settings command
        self._add_settings_command()

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
