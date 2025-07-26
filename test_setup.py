#!/usr/bin/env python3
"""
Test script for Bigo Live Dashboard
Validates basic functionality and dependencies
"""

import streamlit as st
import pandas as pd
import sys
import importlib
import os

def test_imports():
    """Test all required imports"""
    required_modules = [
        'streamlit',
        'pandas', 
        'requests',
        'openpyxl',
        'gspread', 
        'oauth2client'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module} - OK")
        except ImportError:
            missing_modules.append(module)
            print(f"❌ {module} - MISSING")
    
    return missing_modules

def test_file_structure():
    """Test if all required files exist"""
    required_files = [
        'app.py',
        'utils/gsheets.py',
        'utils/gsheets_writer.py',
        'utils/data_validator.py',
        'requirements.txt',
        'static/enhanced_style.css'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} - EXISTS")
        else:
            missing_files.append(file_path)
            print(f"❌ {file_path} - MISSING")
    
    return missing_files

def test_dataframe_operations():
    """Test basic DataFrame operations"""
    try:
        # Create sample data
        df = pd.DataFrame({
            'Date': ['2025-01-01', '2025-01-02'],
            'Agency Name.1': ['Agency A', 'Agency B'],
            'Agency Name.2': ['Agency B', 'Agency A'],
            'ID1': ['123', '456'],
            'ID.2': ['789', '012']
        })
        
        # Test date conversion
        df['Date'] = pd.to_datetime(df['Date'])
        print("✅ Date conversion - OK")
        
        # Test filtering
        filtered = df[df['Agency Name.1'].isin(['Agency A'])]
        print("✅ DataFrame filtering - OK")
        
        # Test search functionality  
        mask = df.astype(str).apply(lambda x: x.str.lower().str.contains('agency', na=False)).any(axis=1)
        search_result = df[mask]
        print("✅ Search functionality - OK")
        
        return True
        
    except Exception as e:
        print(f"❌ DataFrame operations - ERROR: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Bigo Live Dashboard Setup...")
    print("="*50)
    
    print("\n📦 Testing imports...")
    missing_modules = test_imports()
    
    print("\n📁 Testing file structure...")
    missing_files = test_file_structure()
    
    print("\n🐼 Testing DataFrame operations...")
    df_test_passed = test_dataframe_operations()
    
    print("\n" + "="*50)
    print("📊 TEST SUMMARY")
    print("="*50)
    
    if missing_modules:
        print(f"❌ Missing modules: {', '.join(missing_modules)}")
        print("   Run: pip install -r requirements.txt")
    else:
        print("✅ All required modules installed")
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
    else:
        print("✅ All required files present")
    
    if df_test_passed:
        print("✅ DataFrame operations working")
    else:
        print("❌ DataFrame operations failed")
    
    if not missing_modules and not missing_files and df_test_passed:
        print("\n🎉 All tests passed! Dashboard should work correctly.")
        print("   Run: streamlit run app.py")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")

if __name__ == "__main__":
    main()
