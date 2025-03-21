"""
Tests for the Test Plugin plugin.
"""

import unittest
from karrio.plugins.test_plugin.plugin import TestPluginPlugin


class TestTestPluginPlugin(unittest.TestCase):
    """Test cases for Test Plugin plugin."""

    def setUp(self):
        """Set up test fixtures."""
        self.plugin = TestPluginPlugin(settings={})
        
    def test_initialization(self):
        """Test plugin initialization."""
        self.assertIsNotNone(self.plugin)
        
    def test_execute(self):
        """Test plugin execution."""
        test_data = {"test": "data"}
        result = self.plugin.execute(test_data)
        self.assertTrue(result["success"])
        self.assertEqual(result["data"], test_data)


if __name__ == "__main__":
    unittest.main()
