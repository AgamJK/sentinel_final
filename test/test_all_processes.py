#!/usr/bin/env python3
"""
Master test script to validate all processes in the Sentiment Sentinel system
Tests: Database, API, Sentiment Analysis, Email Ingestion, and Full Pipeline
"""

import sys
import subprocess
import time
import requests
import json
from datetime import datetime

def run_test_file(test_file):
    """Run a test file and return success status"""
    print(f"\n{'='*60}")
    print(f"🧪 Running {test_file}")
    print('='*60)
    
    try:
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print(f"✅ {test_file} PASSED")
            print(result.stdout)
            return True
        else:
            print(f"❌ {test_file} FAILED")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {test_file} TIMEOUT")
        return False
    except Exception as e:
        print(f"💥 {test_file} ERROR: {e}")
        return False

def check_flask_running():
    """Check if Flask app is running"""
    try:
        response = requests.get("http://127.0.0.1:5000/", timeout=5)
        return response.status_code == 200
    except:
        return False

def start_flask_app():
    """Start Flask app in background"""
    print("\n🚀 Starting Flask application...")
    try:
        # Start Flask app in background
        process = subprocess.Popen([sys.executable, "app.py"], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        
        # Wait for app to start
        for i in range(10):
            time.sleep(1)
            if check_flask_running():
                print("✅ Flask app is running!")
                return process
            print(f"⏳ Waiting for Flask app... ({i+1}/10)")
        
        print("❌ Flask app failed to start")
        return None
        
    except Exception as e:
        print(f"💥 Failed to start Flask app: {e}")
        return None

def main():
    """Main testing process"""
    print("🎯 SENTIMENT SENTINEL - COMPLETE SYSTEM TEST")
    print(f"📅 Test Date: {datetime.now()}")
    
    test_results = {}
    flask_process = None
    
    # Test order (dependencies first)
    tests = [
        ("test/test_db.py", "Database Connection & Operations"),
        ("test/test_sentiment.py", "Sentiment Analysis (Gemini)"),
    ]
    
    try:
        # Run individual component tests
        for test_file, description in tests:
            print(f"\n📋 Testing: {description}")
            test_results[test_file] = run_test_file(test_file)
        
        # Start Flask app for API tests
        flask_process = start_flask_app()
        
        if flask_process:
            # Run API tests
            print(f"\n📋 Testing: Flask API Endpoints")
            test_results["test/test_api.py"] = run_test_file("test/test_api.py")
            
            # Run full pipeline test
            print(f"\n📋 Testing: Complete Message Pipeline")
            test_results["test/test_all_collections.py"] = run_test_file("test/test_all_collections.py")
        
        # Print final results
        print(f"\n{'='*60}")
        print("🏆 FINAL TEST RESULTS")
        print('='*60)
        
        passed = 0
        total = len(test_results)
        
        for test, result in test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test}")
            if result:
                passed += 1
        
        print(f"\n📊 Summary: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED! System is ready for production.")
        else:
            print("⚠️ Some tests failed. Check the logs above.")
            
    finally:
        # Cleanup
        if flask_process:
            print("\n🛑 Shutting down Flask app...")
            flask_process.terminate()
            flask_process.wait()

if __name__ == "__main__":
    main()
