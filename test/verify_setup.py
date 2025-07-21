#!/usr/bin/env python3
"""
Quick setup verification - checks all prerequisites before running tests
"""

import os
import sys
import importlib.util

def check_file_exists(file_path, description):
    """Check if a file exists"""
    if os.path.exists(file_path):
        print(f"✅ {description}: Found")
        return True
    else:
        print(f"❌ {description}: Missing ({file_path})")
        return False

def check_python_package(package_name):
    """Check if a Python package is installed"""
    spec = importlib.util.find_spec(package_name)
    if spec is not None:
        print(f"✅ {package_name}: Installed")
        return True
    else:
        print(f"❌ {package_name}: Not installed")
        return False

def check_environment_variable(var_name):
    """Check if environment variable is set"""
    if os.getenv(var_name):
        print(f"✅ {var_name}: Set")
        return True
    else:
        print(f"❌ {var_name}: Not set")
        return False

def main():
    """Run all prerequisite checks"""
    print("🔍 SYSTEM SETUP VERIFICATION")
    print("="*50)
    
    all_checks_passed = True
    
    # Check core files
    print("\n📁 Core Files:")
    files_to_check = [
        ("app.py", "Flask Application"),
        ("database.py", "Database Manager"),
        ("gemini_emotion_classifier.py", "Emotion Classifier"),
        ("requirements.txt", "Requirements File"),
        (".env", "Environment File (optional)")
    ]
    
    for file_path, description in files_to_check:
        if not check_file_exists(file_path, description):
            if file_path != ".env":  # .env is optional
                all_checks_passed = False
    
    # Check test files
    print("\n🧪 Test Files:")
    test_files = [
        ("test/test_db.py", "Database Test"),
        ("test/test_api.py", "API Test"),
        ("test/test_sentiment.py", "Sentiment Test"),
        ("test_dashboard.py", "Dashboard Test"),
        ("test_all_processes.py", "Master Test")
    ]
    
    for file_path, description in test_files:
        check_file_exists(file_path, description)
    
    # Check Python packages
    print("\n🐍 Python Packages:")
    required_packages = [
        "flask",
        "pymongo",
        "python-dotenv",
        "requests",
        "google-generativeai"
    ]
    
    for package in required_packages:
        if not check_python_package(package):
            all_checks_passed = False
    
    # Check environment variables
    print("\n🌍 Environment Variables:")
    env_vars = [
        "MONGODB_URI",
        "GEMINI_API_KEY"
    ]
    
    for var in env_vars:
        if not check_environment_variable(var):
            print(f"   💡 Set {var} in your .env file or system environment")
            if var == "MONGODB_URI":
                all_checks_passed = False
    
    # Check database collections info
    print("\n📊 Database Info:")
    if check_file_exists("test/DATABASE_COLLECTIONS.md", "Collections Documentation"):
        print("   📖 Database schema documented")
    
    # Final status
    print("\n" + "="*50)
    if all_checks_passed:
        print("🎉 SETUP VERIFICATION PASSED!")
        print("✅ All prerequisites met - ready to run tests")
        print("\n🚀 Next steps:")
        print("   1. Run: python test_all_processes.py")
        print("   2. Or run individual tests:")
        print("      - python test/test_db.py")
        print("      - python test/test_api.py") 
        print("      - python test/test_sentiment.py")
        print("      - python test_dashboard.py")
    else:
        print("⚠️ SETUP ISSUES FOUND!")
        print("❌ Please fix the missing requirements above")
        print("\n💡 Quick fixes:")
        print("   - Install packages: pip install -r requirements.txt")
        print("   - Set environment variables in .env file")
        print("   - Check file paths are correct")
    
    return all_checks_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
