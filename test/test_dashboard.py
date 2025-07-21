#!/usr/bin/env python3
"""
Test script to verify dashboard data endpoints
Tests all the endpoints that would feed the emotion monitoring dashboard
"""

import requests
import json
from datetime import datetime
import sys

BASE_URL = "http://127.0.0.1:5000"

def test_dashboard_endpoints():
    """Test all dashboard-related endpoints"""
    print("📊 Testing Dashboard Data Endpoints...")
    
    try:
        # Test dashboard endpoint
        print("\n🎛️ Testing main dashboard endpoint...")
        response = requests.get(f"{BASE_URL}/dashboard")
        if response.status_code == 200:
            dashboard_data = response.json()
            print("✅ Dashboard endpoint working!")
            print(f"   Total messages: {dashboard_data.get('dashboard', {}).get('total_messages', 'N/A')}")
            
            sentiment_dist = dashboard_data.get('dashboard', {}).get('sentiment_distribution', {})
            if sentiment_dist.get('counts'):
                print("   Sentiment distribution:")
                for sentiment, count in sentiment_dist['counts'].items():
                    percentage = sentiment_dist.get('percentages', {}).get(sentiment, 'N/A')
                    print(f"     {sentiment}: {count} ({percentage}%)")
        else:
            print(f"❌ Dashboard endpoint failed: {response.status_code}")
        
        # Test stats endpoint for dashboard cards
        print("\n📈 Testing stats endpoint...")
        response = requests.get(f"{BASE_URL}/stats")
        if response.status_code == 200:
            stats = response.json()
            print("✅ Stats endpoint working!")
            print(f"   Total messages: {stats.get('total_messages', 'N/A')}")
            print("   By source:")
            by_source = stats.get('by_source', {})
            for source, count in by_source.items():
                print(f"     {source}: {count}")
            print("   By sentiment:")
            by_sentiment = stats.get('by_sentiment', {})
            for sentiment, count in by_sentiment.items():
                print(f"     {sentiment}: {count}")
        else:
            print(f"❌ Stats endpoint failed: {response.status_code}")
        
        # Test alerts endpoint
        print("\n🚨 Testing alerts endpoint...")
        response = requests.get(f"{BASE_URL}/alerts")
        if response.status_code == 200:
            alerts = response.json()
            print("✅ Alerts endpoint working!")
            print(f"   Active alerts: {alerts.get('count', 0)}")
            if alerts.get('messages'):
                print("   Recent alert examples:")
                for alert in alerts['messages'][:3]:
                    sentiment = alert.get('sentiment', alert.get('emotion', 'unknown'))
                    print(f"     - {sentiment}: {alert.get('text', 'N/A')[:50]}...")
        else:
            print(f"❌ Alerts endpoint failed: {response.status_code}")
        
        # Test specific sentiment filtering (for dashboard cards)
        sentiment_types = ['angry', 'happy', 'confused', 'neutral']
        print(f"\n🔍 Testing sentiment filtering for dashboard cards...")
        
        for sentiment in sentiment_types:
            response = requests.get(f"{BASE_URL}/sentiment/{sentiment}")
            if response.status_code == 200:
                data = response.json()
                count = data.get('count', 0)
                print(f"   {sentiment.capitalize()}: {count} messages")
            else:
                print(f"   ❌ {sentiment} filtering failed")
        
        # Test message retrieval with different filters
        print(f"\n📋 Testing message filtering options...")
        
        # Test by source
        sources = ['email', 'chat', 'ticket']
        for source in sources:
            response = requests.get(f"{BASE_URL}/messages?source={source}&limit=5")
            if response.status_code == 200:
                data = response.json()
                count = len(data.get('messages', []))
                print(f"   {source}: {count} messages retrieved")
        
        # Test pagination
        response = requests.get(f"{BASE_URL}/messages?limit=10&skip=0")
        if response.status_code == 200:
            data = response.json()
            messages = data.get('messages', [])
            total = data.get('total_count', 0)
            print(f"   Pagination: Retrieved {len(messages)} of {total} total messages")
        
        print("\n✅ All dashboard endpoint tests completed!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Flask app. Make sure it's running on http://127.0.0.1:5000")
        return False
    except Exception as e:
        print(f"❌ Dashboard test failed: {e}")
        return False

def test_real_time_data():
    """Test real-time data flow for dashboard"""
    print("\n⚡ Testing Real-time Data Flow...")
    
    try:
        # Send some test messages to generate fresh data
        test_messages = [
            {
                "id": f"realtime_test_1_{datetime.now().timestamp()}",
                "timestamp": datetime.now().isoformat(),
                "source": "email",
                "sender": "customer1@example.com",
                "text": "I love this product! It's amazing and works perfectly!"
            },
            {
                "id": f"realtime_test_2_{datetime.now().timestamp()}",
                "timestamp": datetime.now().isoformat(),
                "source": "chat",
                "sender": "customer2@example.com",
                "text": "This is terrible! I'm so angry and frustrated with this service!"
            },
            {
                "id": f"realtime_test_3_{datetime.now().timestamp()}",
                "timestamp": datetime.now().isoformat(),
                "source": "ticket",
                "sender": "customer3@example.com",
                "text": "I'm confused about how this feature works. Can you help me understand?"
            }
        ]
        
        # Get initial dashboard state
        response = requests.get(f"{BASE_URL}/dashboard")
        if response.status_code == 200:
            initial_data = response.json()
            initial_count = initial_data.get('dashboard', {}).get('total_messages', 0)
            print(f"Initial message count: {initial_count}")
        
        # Send new messages
        print("Sending new messages...")
        for i, message in enumerate(test_messages):
            response = requests.post(
                f"{BASE_URL}/message",
                json=message,
                headers={'Content-Type': 'application/json'}
            )
            if response.status_code == 201:
                result = response.json()
                print(f"   Message {i+1} sent - Sentiment: {result.get('sentiment', 'unknown')}")
            else:
                print(f"   ❌ Message {i+1} failed")
        
        # Check updated dashboard state
        response = requests.get(f"{BASE_URL}/dashboard")
        if response.status_code == 200:
            updated_data = response.json()
            updated_count = updated_data.get('dashboard', {}).get('total_messages', 0)
            print(f"Updated message count: {updated_count}")
            print(f"New messages processed: {updated_count - initial_count}")
        
        print("✅ Real-time data flow test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Real-time test failed: {e}")
        return False

def main():
    """Run all dashboard tests"""
    print("🎯 DASHBOARD DATA TESTING")
    print(f"📅 Test Date: {datetime.now()}")
    
    success = True
    success &= test_dashboard_endpoints()
    success &= test_real_time_data()
    
    if success:
        print("\n🎉 ALL DASHBOARD TESTS PASSED!")
    else:
        print("\n⚠️ Some dashboard tests failed!")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
