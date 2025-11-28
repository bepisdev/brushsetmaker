"""Settings dialog window."""

import toga
from toga.style import Pack


class SettingsWindow:
    """Window for configuring application settings."""

    def __init__(self, app):
        """Initialize the settings window."""
        self.app = app
        self.settings = app.settings

        # Create the window
        self.window = toga.Window(title="Settings")
        self.window.content = self._build_ui()

    def _build_ui(self):
        """Build the settings UI."""
        main_box = toga.Box(style=Pack(direction="column", padding=20))

        # Title
        title_label = toga.Label(
            "BrushsetMaker Settings",
            style=Pack(padding=(0, 0, 20, 0), font_size=18, font_weight="bold")
        )

        # Create scrollable container for all settings
        scroll_container = toga.ScrollContainer(
            style=Pack(flex=1, width=600, height=500)
        )

        settings_box = toga.Box(style=Pack(direction="column", padding=10))

        # Output & File Management Section
        settings_box.add(self._create_section_header("Output & File Management"))

        self.remember_location = self._create_switch(
            "Remember last save location",
            self.settings.get("remember_last_location", True)
        )
        settings_box.add(self.remember_location)

        self.open_folder = self._create_switch(
            "Open output folder after creation",
            self.settings.get("open_output_folder", False)
        )
        settings_box.add(self.open_folder)

        overwrite_box = self._create_dropdown(
            "Overwrite behavior:",
            ["prompt", "overwrite", "rename"],
            self.settings.get("overwrite_behavior", "prompt")
        )
        self.overwrite_dropdown = overwrite_box.children[1]
        settings_box.add(overwrite_box)

        # Compression Settings Section
        settings_box.add(self._create_section_header("Compression Settings"))

        compression_box = self._create_dropdown(
            "Compression level:",
            ["store", "fast", "normal", "maximum"],
            self.settings.get("compression_level", "normal")
        )
        self.compression_dropdown = compression_box.children[1]
        settings_box.add(compression_box)

        method_box = self._create_dropdown(
            "Compression method:",
            ["deflate", "stored", "bzip2", "lzma"],
            self.settings.get("compression_method", "deflate")
        )
        self.method_dropdown = method_box.children[1]
        settings_box.add(method_box)

        # Metadata Defaults Section
        settings_box.add(self._create_section_header("Metadata Defaults"))

        template_box = self._create_text_field(
            "Brushset name template:",
            self.settings.get("default_name_template", "{folder_name}"),
            "Use {folder_name}, {date}, {datetime}"
        )
        self.template_input = template_box.children[1]
        settings_box.add(template_box)

        author_box = self._create_text_field(
            "Default author:",
            self.settings.get("default_author", ""),
            "Your name"
        )
        self.author_input = author_box.children[1]
        settings_box.add(author_box)

        self.auto_create_plist = self._create_switch(
            "Auto-create brushset.plist if missing",
            self.settings.get("auto_create_plist", True)
        )
        settings_box.add(self.auto_create_plist)

        self.auto_populate = self._create_switch(
            "Auto-populate brushes array",
            self.settings.get("auto_populate_brushes", True)
        )
        settings_box.add(self.auto_populate)

        # Validation & Checks Section
        settings_box.add(self._create_section_header("Validation & Checks"))

        self.validate_structure = self._create_switch(
            "Validate brush structure",
            self.settings.get("validate_brush_structure", False)
        )
        settings_box.add(self.validate_structure)

        self.warn_empty = self._create_switch(
            "Warn on empty folders",
            self.settings.get("warn_empty_folders", True)
        )
        settings_box.add(self.warn_empty)

        self.verify_uuid = self._create_switch(
            "Verify UUID format",
            self.settings.get("verify_uuid_format", True)
        )
        settings_box.add(self.verify_uuid)

        self.check_duplicates = self._create_switch(
            "Check for duplicate brushes",
            self.settings.get("check_duplicate_brushes", False)
        )
        settings_box.add(self.check_duplicates)

        # UI Preferences Section
        settings_box.add(self._create_section_header("UI Preferences"))

        self.show_progress = self._create_switch(
            "Show progress details",
            self.settings.get("show_progress_details", True)
        )
        settings_box.add(self.show_progress)

        self.show_success = self._create_switch(
            "Show success dialogs",
            self.settings.get("show_success_dialogs", True)
        )
        settings_box.add(self.show_success)

        # Bulk Processing Section
        settings_box.add(self._create_section_header("Bulk Processing"))

        self.skip_hidden = self._create_switch(
            "Skip hidden folders (starting with . or _)",
            self.settings.get("skip_hidden_folders", True)
        )
        settings_box.add(self.skip_hidden)

        error_box = self._create_dropdown(
            "Error handling:",
            ["continue", "stop"],
            self.settings.get("error_handling", "continue")
        )
        self.error_dropdown = error_box.children[1]
        settings_box.add(error_box)

        self.generate_report = self._create_switch(
            "Generate processing report",
            self.settings.get("generate_report", False)
        )
        settings_box.add(self.generate_report)

        # Advanced Section
        settings_box.add(self._create_section_header("Advanced"))

        self.include_hidden = self._create_switch(
            "Include hidden files in brushsets",
            self.settings.get("include_hidden_files", False)
        )
        settings_box.add(self.include_hidden)

        self.preserve_timestamps = self._create_switch(
            "Preserve file timestamps",
            self.settings.get("preserve_timestamps", False)
        )
        settings_box.add(self.preserve_timestamps)

        self.create_backup = self._create_switch(
            "Create backup before overwriting",
            self.settings.get("create_backup", False)
        )
        settings_box.add(self.create_backup)

        log_box = self._create_dropdown(
            "Logging level:",
            ["none", "errors", "info", "debug"],
            self.settings.get("logging_level", "info")
        )
        self.log_dropdown = log_box.children[1]
        settings_box.add(log_box)

        scroll_container.content = settings_box

        # Buttons
        button_box = toga.Box(style=Pack(direction="row", padding=(20, 0, 0, 0)))

        save_button = toga.Button(
            "Save Settings",
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

        main_box.add(title_label)
        main_box.add(scroll_container)
        main_box.add(button_box)

        return main_box

    def _create_section_header(self, text):
        """Create a section header."""
        return toga.Label(
            text,
            style=Pack(padding=(20, 0, 10, 0), font_size=14, font_weight="bold")
        )

    def _create_switch(self, label_text, value):
        """Create a labeled switch."""
        box = toga.Box(style=Pack(direction="row", padding=(5, 0, 5, 0)))

        switch = toga.Switch(
            text=label_text,
            value=value,
            style=Pack(flex=1)
        )

        box.add(switch)
        return switch

    def _create_dropdown(self, label_text, items, current_value):
        """Create a labeled dropdown selection."""
        box = toga.Box(style=Pack(direction="column", padding=(5, 0, 10, 0)))

        label = toga.Label(
            label_text,
            style=Pack(padding=(0, 0, 5, 0), font_size=12)
        )

        selection = toga.Selection(
            items=items,
            value=current_value,
            style=Pack(width=250)
        )

        box.add(label)
        box.add(selection)
        return box

    def _create_text_field(self, label_text, value, placeholder=""):
        """Create a labeled text input field."""
        box = toga.Box(style=Pack(direction="column", padding=(5, 0, 10, 0)))

        label = toga.Label(
            label_text,
            style=Pack(padding=(0, 0, 5, 0), font_size=12)
        )

        input_field = toga.TextInput(
            value=value,
            placeholder=placeholder,
            style=Pack(width=400)
        )

        box.add(label)
        box.add(input_field)
        return box

    async def _handle_save(self, widget):
        """Save all settings."""
        try:
            # Output & File Management
            self.settings.set("remember_last_location", self.remember_location.value)
            self.settings.set("open_output_folder", self.open_folder.value)
            self.settings.set("overwrite_behavior", self.overwrite_dropdown.value)

            # Compression
            self.settings.set("compression_level", self.compression_dropdown.value)
            self.settings.set("compression_method", self.method_dropdown.value)

            # Metadata
            self.settings.set("default_name_template", self.template_input.value)
            self.settings.set("default_author", self.author_input.value)
            self.settings.set("auto_create_plist", self.auto_create_plist.value)
            self.settings.set("auto_populate_brushes", self.auto_populate.value)

            # Validation
            self.settings.set("validate_brush_structure", self.validate_structure.value)
            self.settings.set("warn_empty_folders", self.warn_empty.value)
            self.settings.set("verify_uuid_format", self.verify_uuid.value)
            self.settings.set("check_duplicate_brushes", self.check_duplicates.value)

            # UI Preferences
            self.settings.set("show_progress_details", self.show_progress.value)
            self.settings.set("show_success_dialogs", self.show_success.value)

            # Bulk Processing
            self.settings.set("skip_hidden_folders", self.skip_hidden.value)
            self.settings.set("error_handling", self.error_dropdown.value)
            self.settings.set("generate_report", self.generate_report.value)

            # Advanced
            self.settings.set("include_hidden_files", self.include_hidden.value)
            self.settings.set("preserve_timestamps", self.preserve_timestamps.value)
            self.settings.set("create_backup", self.create_backup.value)
            self.settings.set("logging_level", self.log_dropdown.value)

            # Save to disk
            self.settings.save()

            await self.app.main_window.info_dialog(
                "Settings Saved",
                "Your settings have been saved successfully."
            )

            self.window.close()

        except Exception as e:
            await self.app.main_window.error_dialog(
                "Error",
                f"Failed to save settings: {e}"
            )

    def _handle_cancel(self, widget):
        """Close without saving."""
        self.window.close()

    def show(self):
        """Show the settings window."""
        self.window.show()
