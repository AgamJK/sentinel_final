#!/usr/bin/env python3
"""
Quick Flask Server Check - Run this before the live test
"""

import requests
from datetime import datetime

BASE_URL = "http://localhost:5000"

def check_server():
    """Check if Flask server is running and all APIs are accessible"""
    print("🔍 Checking Flask server status...")
    
    apis_to_test = [
        ("/api/emotion-overview", "Emotion Overview"),
        ("/api/emotion-trends?hours=1", "Emotion Trends"),
        ("/alerts?limit=3", "Alerts/Flagged Conversations"),
        ("/api/realtime-stats", "Realtime Stats")
    ]
    
    server_running = False
    working_apis = 0
    
    for endpoint, name in apis_to_test:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"   ✅ {name}: Working")
                working_apis += 1
                server_running = True
            else:
                print(f"   ❌ {name}: Status {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"   ❌ {name}: Connection refused (server not running?)")
        except requests.exceptions.Timeout:
            print(f"   ❌ {name}: Timeout")
        except Exception as e:
            print(f"   ❌ {name}: Error - {e}")
    
    print(f"\n📊 Results: {working_apis}/{len(apis_to_test)} APIs working")
    
    if server_running and working_apis == len(apis_to_test):
        print("🎉 Server is ready! You can run the live dashboard test.")
        return True
    elif server_running and working_apis > 0:
        print("⚠️  Server is partially working. Some APIs may not respond during the test.")
        return True
    else:
        print("❌ Server appears to be down. Please start the Flask server first:")
        print("   cd backend-aashish-f")
        print("   python app.py")
        return False

if __name__ == "__main__":
    print(f"🕐 Server Check at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    check_server()
    print("=" * 60)
