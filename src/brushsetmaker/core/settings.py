"""Application settings management."""

import json
from pathlib import Path


class Settings:
    """Manages application settings with persistent storage."""

    def __init__(self):
        """Initialize settings with defaults."""
        self.settings_path = Path.home() / ".brushsetmaker" / "settings.json"
        self.settings_path.parent.mkdir(parents=True, exist_ok=True)
        self._settings = self._load_settings()

    def _get_defaults(self):
        """Return default settings."""
        return {
            # Output & File Management
            "default_save_location": str(Path.home() / "Desktop"),
            "remember_last_location": True,
            "overwrite_behavior": "prompt",  # prompt, overwrite, rename
            "open_output_folder": False,

            # Compression Settings
            "compression_level": "normal",  # store, fast, normal, maximum
            "compression_method": "deflate",  # deflate, stored, bzip2, lzma

            # Metadata Defaults
            "default_name_template": "{folder_name}",
            "default_author": "",
            "auto_create_plist": True,
            "auto_populate_brushes": True,

            # Validation & Checks
            "validate_brush_structure": False,
            "warn_empty_folders": True,
            "verify_uuid_format": True,
            "check_duplicate_brushes": False,

            # UI Preferences
            "show_progress_details": True,
            "show_success_dialogs": True,

            # Bulk Processing
            "skip_hidden_folders": True,
            "error_handling": "continue",  # continue, stop
            "generate_report": False,

            # Advanced
            "include_hidden_files": False,
            "preserve_timestamps": False,
            "create_backup": False,
            "logging_level": "info",  # none, errors, info, debug
        }

    def _load_settings(self):
        """Load settings from file or return defaults."""
        if self.settings_path.exists():
            try:
                with open(self.settings_path) as f:
                    loaded = json.load(f)
                    # Merge with defaults to handle new settings
                    defaults = self._get_defaults()
                    defaults.update(loaded)
                    return defaults
            except Exception:
                pass
        return self._get_defaults()

    def save(self):
        """Save current settings to file."""
        try:
            with open(self.settings_path, 'w') as f:
                json.dump(self._settings, f, indent=2)
        except Exception as e:
            print(f"Failed to save settings: {e}")

    def get(self, key, default=None):
        """Get a setting value."""
        return self._settings.get(key, default)

    def set(self, key, value):
        """Set a setting value."""
        self._settings[key] = value

    def get_compression_level(self):
        """Get ZIP compression level as integer."""
        levels = {
            "store": 0,
            "fast": 1,
            "normal": 6,
            "maximum": 9
        }
        level_name = str(self.get("compression_level", "normal"))
        return levels.get(level_name, 6)

    def get_compression_method(self):
        """Get ZIP compression method constant."""
        import zipfile
        methods = {
            "deflate": zipfile.ZIP_DEFLATED,
            "stored": zipfile.ZIP_STORED,
            "bzip2": zipfile.ZIP_BZIP2,
            "lzma": zipfile.ZIP_LZMA
        }
        method_name = str(self.get("compression_method", "deflate"))
        return methods.get(method_name, zipfile.ZIP_DEFLATED)

    def should_skip_folder(self, folder_name):
        """Check if folder should be skipped based on settings."""
        if self.get("skip_hidden_folders", True):
            return folder_name.startswith(('.', '_'))
        return False

    def format_brushset_name(self, folder_name):
        """Format brushset name using template."""
        from datetime import datetime
        template = str(self.get("default_name_template", "{folder_name}"))
        return template.format(
            folder_name=folder_name,
            date=datetime.now().strftime("%Y-%m-%d"),
            datetime=datetime.now().strftime("%Y-%m-%d %H:%M")
        )
