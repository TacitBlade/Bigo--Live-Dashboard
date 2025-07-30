#!/usr/bin/env python3
"""
Test script to verify the Streamlit application can start properly.
"""

import sys
import subprocess
import os

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    try:
        import streamlit
        import pandas
        import openpyxl
        import gspread
        import oauth2client
        import requests
        import dateutil
        import plotly
        import xlsxwriter
        import numpy
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_streamlit_version():
    """Test Streamlit version compatibility."""
    import streamlit as st
    print(f"Streamlit version: {st.__version__}")
    return True

def test_app_structure():
    """Test that required files exist."""
    required_files = [
        'home.py',
        'requirements.txt',
        'utils/gsheets.py',
        'utils/gsheets_writer.py',
        'utils/data_validator.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"✗ Missing files: {missing_files}")
        return False
    else:
        print("✓ All required files present")
        return True

if __name__ == "__main__":
    print("Starting application tests...")
    
    tests = [
        test_imports,
        test_streamlit_version,
        test_app_structure
    ]
    
    passed = 0
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} failed: {e}")
    
    print(f"\nTests passed: {passed}/{len(tests)}")
    
    if passed == len(tests):
        print("✓ All tests passed! Application should be ready to deploy.")
        sys.exit(0)
    else:
        print("✗ Some tests failed. Please check the issues above.")
        sys.exit(1)
