#!/usr/bin/env python3
"""
DASHBOARD ENDPOINTS TEST SUITE - COMPREHENSIVE SUMMARY

This file provides a complete testing solution for the dashboard endpoints:
- /dashboard
- /api/emotion-overview  
- /api/emotion-trends
- /api/realtime-stats

USAGE:
1. Basic connectivity test: python test_endpoints_simple.py
2. Quick functional test: python quick_dashboard_test.py  
3. Full test suite: python test_dashboard_comprehensive.py
4. Mock tests: python test_dashboard_mock.py
"""

import os
import sys
import requests

def check_server_status():
    """Check if server is running"""
    try:
        response = requests.get("http://localhost:5000/", timeout=2)
        return response.status_code == 200
    except:
        return False

def check_database_status():
    """Check if database is connected"""
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("database") == "connected"
        return False
    except:
        return False

def main():
    """Run diagnostic and provide test recommendations"""
    print("🧪 DASHBOARD ENDPOINTS TEST SUITE")
    print("=" * 60)
    
    # Check prerequisites
    print("🔍 SYSTEM CHECK")
    print("-" * 30)
    
    server_running = check_server_status()
    database_connected = check_database_status()
    
    print(f"Flask Server: {'✅ Running' if server_running else '❌ Not running'}")
    print(f"Database:     {'✅ Connected' if database_connected else '❌ Not connected'}")
    
    # Provide recommendations
    print("\n📋 TESTING RECOMMENDATIONS")
    print("-" * 30)
    
    if not server_running:
        print("❌ Server is not running!")
        print("   Run: python app.py")
        print("   Make sure you're in the backend directory")
        return
    
    if not database_connected:
        print("⚠️  Database is not connected")
        print("   This is expected if you haven't set up MongoDB yet")
        print("   The endpoints will return 500 errors but are still testable")
        
        print("\n🧪 RECOMMENDED TEST:")
        print("   python test\\test_endpoints_simple.py")
        print("   ↳ Tests endpoint accessibility and error handling")
    
    else:
        print("✅ Full system is operational!")
        
        print("\n🧪 RECOMMENDED TESTS (in order):")
        print("   1. python test\\quick_dashboard_test.py")
        print("      ↳ Quick functional test with real data")
        print("   2. python test\\test_dashboard_comprehensive.py")
        print("      ↳ Full test suite with detailed validation")
    
    # Show available test files
    print("\n📁 AVAILABLE TEST FILES")
    print("-" * 30)
    
    test_files = [
        ("test_endpoints_simple.py", "Basic connectivity & error handling"),
        ("quick_dashboard_test.py", "Quick functional test"), 
        ("test_dashboard_comprehensive.py", "Full test suite with unittest"),
        ("test_dashboard_mock.py", "Mock tests (no database needed)"),
        ("test_dashboard_endpoints.py", "Original dashboard test")
    ]
    
    for filename, description in test_files:
        filepath = f"test\\{filename}"
        exists = os.path.exists(filepath)
        status = "✅" if exists else "❌"
        print(f"   {status} {filename}")
        print(f"      ↳ {description}")
    
    print("\n" + "=" * 60)
    print("💡 QUICK START GUIDE")
    print("=" * 60)
    
    print("1. 📡 Test endpoint accessibility (works without database):")
    print("   python test\\test_endpoints_simple.py")
    
    print("\n2. 🔧 If you have database setup:")
    print("   python test\\quick_dashboard_test.py")
    
    print("\n3. 🧪 For comprehensive testing:")
    print("   python test\\test_dashboard_comprehensive.py")
    
    print("\n4. 📊 Current endpoint status:")
    endpoints = [
        "/dashboard",
        "/api/emotion-overview", 
        "/api/emotion-trends",
        "/api/realtime-stats"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"http://localhost:5000{endpoint}", timeout=2)
            if response.status_code == 200:
                print(f"   ✅ {endpoint} - Working")
            elif response.status_code == 500:
                print(f"   ⚠️  {endpoint} - Accessible (DB error expected)")
            else:
                print(f"   ❌ {endpoint} - Status {response.status_code}")
        except:
            print(f"   ❌ {endpoint} - Connection failed")

if __name__ == "__main__":
    main()
