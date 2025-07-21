#!/usr/bin/env python3
"""
Test script for new dashboard endpoints
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000"

def test_new_dashboard_endpoints():
    """Test all new dashboard endpoints"""
    print("🧪 Testing New Dashboard Endpoints...")
    
    endpoints_to_test = [
        ("/api/emotion-overview", "Emotion Overview Cards"),
        ("/api/emotion-trends", "Real-time Emotion Trends"),
        ("/api/realtime-stats", "Real-time Statistics"),
        ("/dashboard", "Original Dashboard (Enhanced)")
    ]
    
    for endpoint, description in endpoints_to_test:
        print(f"\n📡 Testing {description}: {endpoint}")
        try:
            response = requests.get(f"{BASE_URL}{endpoint}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Success! Status: {response.status_code}")
                
                # Pretty print some key data
                if endpoint == "/api/emotion-overview":
                    for emotion, stats in data.items():
                        if isinstance(stats, dict):
                            count = stats.get('count', 0)
                            change = stats.get('change_percent', 0)
                            print(f"      {emotion.title()}: {count} messages ({change:+}%)")
                
                elif endpoint == "/api/emotion-trends":
                    trends = data.get('trends', {})
                    if trends:
                        sample_time = list(trends.keys())[0]
                        sample_data = trends[sample_time]
                        print(f"      Sample hour {sample_time}: {sample_data}")
                    
                elif endpoint == "/api/realtime-stats":
                    current = data.get('current_hour', {})
                    total = data.get('total', {})
                    timestamp = data.get('timestamp', 'N/A')
                    print(f"      Current hour: {current}")
                    print(f"      Total counts: {total}")
                    print(f"      Last updated: {timestamp}")
                
                elif endpoint == "/dashboard":
                    dashboard_data = data.get('dashboard', {})
                    total_msg = dashboard_data.get('total_messages', 'N/A')
                    print(f"      Total messages: {total_msg}")
                    
            else:
                print(f"   ❌ Failed! Status: {response.status_code}")
                if response.status_code != 500:
                    print(f"      Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print(f"   ⚠️  Connection failed - Make sure Flask app is running on {BASE_URL}")
        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_with_sample_data():
    """Send some sample data first"""
    print("\n📝 Sending sample data for testing...")
    
    sample_messages = [
        {
            "id": f"test_{datetime.now().strftime('%H%M%S')}_1",
            "timestamp": datetime.now().isoformat(),
            "source": "email", 
            "sender": "customer1@test.com",
            "text": "I'm very angry about this service delay!"
        },
        {
            "id": f"test_{datetime.now().strftime('%H%M%S')}_2", 
            "timestamp": datetime.now().isoformat(),
            "source": "chat",
            "sender": "customer2@test.com", 
            "text": "I'm confused about how to use this feature."
        },
        {
            "id": f"test_{datetime.now().strftime('%H%M%S')}_3",
            "timestamp": datetime.now().isoformat(),
            "source": "ticket",
            "sender": "customer3@test.com",
            "text": "Thank you for the excellent support! I'm very happy."
        }
    ]
    
    for msg in sample_messages:
        try:
            response = requests.post(f"{BASE_URL}/message", json=msg)
            if response.status_code == 201:
                print(f"   ✅ Sample message sent: {msg['text'][:50]}...")
            else:
                print(f"   ⚠️  Failed to send sample: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error sending sample: {e}")

if __name__ == "__main__":
    print("🚀 Dashboard Endpoints Test Suite")
    print("=" * 50)
    
    # First send some sample data
    test_with_sample_data()
    
    # Then test the endpoints
    test_new_dashboard_endpoints()
    
    print("\n" + "=" * 50)
    print("✅ Test complete! Check your frontend can now consume these endpoints:")
    print("   • /api/emotion-overview - For dashboard cards")
    print("   • /api/emotion-trends - For the trends chart")
    print("   • /api/realtime-stats - For real-time updates")
    print("   • /dashboard - Enhanced dashboard data")
