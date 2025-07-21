#!/usr/bin/env python3
"""
Master test script - runs all tests in sequence
"""

import subprocess
import sys
import time
import requests

def run_test(test_name, test_command):
    """Run a test and return success status"""
    print(f"\n{'='*60}")
    print(f"🧪 Running {test_name}")
    print('='*60)
    
    try:
        result = subprocess.run(test_command, shell=True, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print(f"✅ {test_name} PASSED")
            print(result.stdout)
            return True
        else:
            print(f"❌ {test_name} FAILED")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {test_name} TIMEOUT")
        return False
    except Exception as e:
        print(f"💥 {test_name} ERROR: {e}")
        return False

def check_flask_running():
    """Check if Flask app is running"""
    try:
        response = requests.get("http://127.0.0.1:5000/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    print("🎯 SENTIMENT SENTINEL - COMPLETE SYSTEM TEST")
    print(f"📅 Started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test results tracking
    results = {}
    
    # Test 1: Database
    results["Database"] = run_test("Database Connection & Operations", "python test\\test_db.py")
    
    # Check if Flask is running, if not skip API tests
    if check_flask_running():
        print("\n✅ Flask detected running - proceeding with API tests")
        
        # Test 2: API Endpoints
        results["API"] = run_test("Flask API Endpoints", "python test\\test_api.py")
        
        # Test 3: Dashboard
        results["Dashboard"] = run_test("Dashboard Data Endpoints", "python test\\test_dashboard.py")
        
        # Test 4: Sentiment Analysis
        results["Sentiment"] = run_test("Sentiment Analysis Integration", "python test\\test_sentiment.py")
        
    else:
        print("\n⚠️ Flask not running - skipping API tests")
        print("💡 Start Flask with: python app.py")
        results["API"] = False
        results["Dashboard"] = False
        results["Sentiment"] = False
    
    # Final results
    print(f"\n{'='*60}")
    print("🏆 FINAL TEST RESULTS")
    print('='*60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name} Test")
        if result:
            passed += 1
    
    print(f"\n📊 Summary: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! System is ready for production.")
        print("🚀 Your emotion monitoring dashboard will work perfectly!")
    else:
        print("⚠️ Some tests failed. Please check the logs above.")
        if not check_flask_running():
            print("💡 Make sure to start Flask app: python app.py")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
