#!/usr/bin/env python3
"""
Simple test runner without emoji characters for Windows compatibility
"""

import subprocess
import sys
import time
import requests
from datetime import datetime

def run_simple_test(test_name, test_file):
    """Run a test file and return the result"""
    print(f"\n{'='*50}")
    print(f"Testing {test_name}")
    print('='*50)
    
    try:
        # Use a simpler approach
        import os
        os.chdir('d:/sentiment-sentinel-ai-agam')
        
        if test_name == "Database":
            # Test database directly
            sys.path.append('.')
            from database import get_database_manager
            
            db_manager = get_database_manager()
            test_message = {
                "id": f"simple_test_{datetime.now().timestamp()}",
                "timestamp": datetime.now().isoformat(),
                "source": "email", 
                "sender": "test@example.com",
                "text": "Simple test message"
            }
            
            message_id = db_manager.insert_message(test_message)
            count = db_manager.get_message_count()
            db_manager.close_connection()
            
            print(f"SUCCESS: Database connected, message inserted: {message_id}")
            print(f"Total messages in database: {count}")
            return True
            
        elif test_name == "API Health":
            # Test API health
            response = requests.get("http://127.0.0.1:5000/health", timeout=5)
            if response.status_code == 200:
                health_data = response.json()
                print(f"SUCCESS: API is healthy")
                print(f"Database status: {health_data.get('database')}")
                print(f"Message count: {health_data.get('message_count')}")
                return True
            else:
                print(f"FAILED: API health check failed with status {response.status_code}")
                return False
                
        elif test_name == "Dashboard Data":
            # Test dashboard endpoint
            response = requests.get("http://127.0.0.1:5000/dashboard", timeout=10)
            if response.status_code == 200:
                dashboard_data = response.json()
                total_messages = dashboard_data.get('dashboard', {}).get('total_messages', 0)
                print(f"SUCCESS: Dashboard endpoint working")
                print(f"Total messages: {total_messages}")
                
                sentiment_dist = dashboard_data.get('dashboard', {}).get('sentiment_distribution', {})
                if sentiment_dist.get('counts'):
                    print("Sentiment breakdown:")
                    for sentiment, count in sentiment_dist['counts'].items():
                        print(f"  {sentiment}: {count}")
                
                return True
            else:
                print(f"FAILED: Dashboard endpoint failed with status {response.status_code}")
                return False
                
        elif test_name == "Message Processing":
            # Test message processing with sentiment analysis
            test_message = {
                "id": f"process_test_{datetime.now().timestamp()}",
                "timestamp": datetime.now().isoformat(),
                "source": "chat",
                "sender": "test_user@example.com", 
                "text": "I'm very happy with this service! It's excellent!"
            }
            
            response = requests.post(
                "http://127.0.0.1:5000/message",
                json=test_message,
                headers={'Content-Type': 'application/json'},
                timeout=15
            )
            
            if response.status_code == 201:
                result = response.json()
                print(f"SUCCESS: Message processed")
                print(f"Detected sentiment: {result.get('sentiment', 'unknown')}")
                print(f"Total messages: {result.get('total_messages')}")
                return True
            else:
                print(f"FAILED: Message processing failed with status {response.status_code}")
                return False
                
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False

def check_flask_running():
    """Check if Flask app is running"""
    try:
        response = requests.get("http://127.0.0.1:5000/health", timeout=3)
        return response.status_code == 200
    except:
        return False

def main():
    print("SENTIMENT SENTINEL - SYSTEM TEST")
    print(f"Started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)
    
    # Test results
    results = {}
    
    # Test 1: Database
    print("\n1. Testing Database Connection...")
    results["Database"] = run_simple_test("Database", None)
    
    # Check Flask status
    flask_running = check_flask_running()
    
    if flask_running:
        print("\nFlask app is running - proceeding with API tests")
        
        # Test 2: API Health
        print("\n2. Testing API Health...")
        results["API Health"] = run_simple_test("API Health", None)
        
        # Test 3: Dashboard
        print("\n3. Testing Dashboard Data...")
        results["Dashboard Data"] = run_simple_test("Dashboard Data", None)
        
        # Test 4: Message Processing
        print("\n4. Testing Message Processing...")
        results["Message Processing"] = run_simple_test("Message Processing", None)
        
    else:
        print("\nWARNING: Flask app not running - skipping API tests")
        print("Start Flask with: python app.py")
        results["API Health"] = False
        results["Dashboard Data"] = False  
        results["Message Processing"] = False
    
    # Final results
    print(f"\n{'='*50}")
    print("FINAL TEST RESULTS")
    print('='*50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "PASS" if result else "FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\nSummary: {passed}/{total} tests passed")
    
    if passed == total:
        print("\nALL TESTS PASSED! System is ready!")
        print("Your emotion monitoring dashboard will work perfectly!")
        print("\nTo fetch dashboard data, use these endpoints:")
        print("  - http://127.0.0.1:5000/dashboard")
        print("  - http://127.0.0.1:5000/stats") 
        print("  - http://127.0.0.1:5000/alerts")
    else:
        print("\nSome tests failed. Check the details above.")
        if not flask_running:
            print("Make sure Flask app is running: python app.py")

if __name__ == "__main__":
    main()
