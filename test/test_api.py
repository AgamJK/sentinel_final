#!/usr/bin/env python3
"""
Test script to verify Flask API endpoints with MongoDB
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000"

def test_api_endpoints():
    """Test all API endpoints"""
    print("🧪 Testing Flask API endpoints...")
    
    try:
        # Test health endpoint
        print("\n💓 Testing health endpoint...")
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Health Response: {response.json()}")
        
        # Test home endpoint
        print("\n🏠 Testing home endpoint...")
        response = requests.get(f"{BASE_URL}/")
        print(f"Home Status: {response.status_code}")
        print(f"Home Response: {response.text}")
        
        # Test posting a message
        print("\n📝 Testing message POST...")
        test_message = {
            "id": f"api_test_{datetime.now().timestamp()}",
            "timestamp": datetime.now().isoformat(),
            "source": "email",
            "sender": "api_test@example.com",
            "text": "This is a test message sent via API to verify MongoDB integration."
        }
        
        response = requests.post(
            f"{BASE_URL}/message",
            json=test_message,
            headers={'Content-Type': 'application/json'}
        )
        print(f"POST Message Status: {response.status_code}")
        if response.status_code == 201:
            print(f"POST Response: {response.json()}")
        
        # Test getting all messages
        print("\n📋 Testing messages GET...")
        response = requests.get(f"{BASE_URL}/messages")
        print(f"GET Messages Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Total messages: {data.get('total_count', 'N/A')}")
            print(f"Retrieved: {len(data.get('messages', []))} messages")
        
        # Test stats endpoint
        print("\n📊 Testing stats endpoint...")
        response = requests.get(f"{BASE_URL}/stats")
        print(f"Stats Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Stats: {response.json()}")
        
        # Test filtering by source
        print("\n🔍 Testing filtering by source...")
        response = requests.get(f"{BASE_URL}/messages?source=email&limit=3")
        print(f"Filter Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Email messages: {len(data.get('messages', []))}")
        
        print("\n✅ All API tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Flask app. Make sure it's running on http://127.0.0.1:5000")
    except Exception as e:
        print(f"❌ API test failed: {e}")

if __name__ == "__main__":
    test_api_endpoints()
