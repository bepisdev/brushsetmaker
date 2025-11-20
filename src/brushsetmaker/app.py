"""
BrushsetMaker - macOS utility to compile brushsets for Procreate.

Entry point for the application.
"""

import toga
from . import __version__
from .ui import UIBuilder
from .core import BrushsetHandlers


class BrushsetMaker(toga.App):
    """Main application class for BrushsetMaker."""

    def startup(self):
        """Construct and show the Toga application."""
        # Build the main window UI
        main_box = UIBuilder.build_main_window(self)

        # Create the main window
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

        # Initialize state
        self.selected_folder = None
        self.progress_window = None

    # Handler wrappers to bridge UI callbacks to handler methods
    async def _handle_create_single(self, widget):
        """Wrapper for create single brushset handler."""
        await BrushsetHandlers.create_single_brushset(self, widget)

    async def _handle_select_bulk(self, widget):
        """Wrapper for select bulk folder handler."""
        await BrushsetHandlers.select_bulk_folder(self, widget)

    async def _handle_process_folders(self, widget):
        """Wrapper for process folders handler."""
        await BrushsetHandlers.process_folders(self, widget)


def main():
    """Entry point for the application."""
    app = BrushsetMaker(
        app_name='brushsetmaker',
        formal_name='BrushsetMaker',
        version=__version__,
        app_id='dev.bepis.brushsetmaker',
        author="Josh Burns",
        description="macOS utility to compile brushsets for Procreate",
        home_page="https://bepisdev.github.io/brushsetmaker/"
    )
    return app


if __name__ == '__main__':
    main().main_loop()
