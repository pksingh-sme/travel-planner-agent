#!/usr/bin/env python3
"""
Test runner for Travel Planner Agent
"""

import unittest
import sys
import os

def run_tests():
    """Discover and run all tests"""
    loader = unittest.TestLoader()
    start_dir = 'tests'
    suite = loader.discover(start_dir)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)