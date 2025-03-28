#!/usr/bin/env python
"""
Run Chit Chats API tests.
This script provides a simple way to run all the Chit Chats API tests.
"""

import os
import sys
import unittest
import importlib.util

# Try to import pytest
try:
    import pytest
    PYTEST_AVAILABLE = True
except ImportError:
    PYTEST_AVAILABLE = False

# Determine if the script is run from the project root or the tests directory
if os.path.basename(os.getcwd()) == 'tests':
    TEST_DIR = os.getcwd()
else:
    TEST_DIR = os.path.join(os.getcwd(), 'modules', 'connectors', 'chitchats', 'tests')


def run_unittest_tests():
    """Run tests using unittest framework."""
    print("Running unittest-based tests...")
    loader = unittest.TestLoader()
    suite = loader.discover(TEST_DIR, pattern="test_integration.py")
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


def run_pytest_tests():
    """Run tests using pytest framework."""
    print("Running pytest-based tests...")
    sys.exit(pytest.main(['-xvs', TEST_DIR]))


def main():
    """Main entry point for test runner."""
    print("=== Chit Chats API Test Runner ===")
    print(f"Test directory: {TEST_DIR}")
    
    # Check for requirements
    try:
        import requests
        print("✅ requests package found")
    except ImportError:
        print("❌ requests package not found. Install with: pip install requests")
        return 1
    
    if PYTEST_AVAILABLE:
        print("✅ pytest package found")
    else:
        print("⚠️ pytest package not found. Only unittest tests will be run.")
        print("   Install pytest with: pip install pytest")
    
    # Run unittest tests
    run_unittest_tests()
    
    # Run pytest tests if available
    if PYTEST_AVAILABLE:
        run_pytest_tests()
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 
