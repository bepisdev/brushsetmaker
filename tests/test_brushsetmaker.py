"""Tests for BrushsetMaker app."""

import unittest
import sys
import os
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from brushsetmaker import __version__


class TestBrushsetMaker(unittest.TestCase):
    """Test basic module functionality."""

    def test_version(self):
        """Test that version is defined."""
        self.assertEqual(__version__, "0.1.0")

    def test_app_import(self):
        """Test that app module can be imported."""
        try:
            from brushsetmaker import app
            self.assertTrue(hasattr(app, 'BrushsetMaker'))
            self.assertTrue(hasattr(app, 'main'))
        except ImportError as e:
            self.skipTest(f"Toga not installed in test environment: {e}")


if __name__ == '__main__':
    unittest.main()
