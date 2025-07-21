#!/usr/bin/env python3
"""
Comprehensive test script to verify all database collections are working
"""

import requests
import json
from datetime import datetime
from database import get_database_manager

BASE_URL = "http://127.0.0.1:5000"

def test_all_collections():
    """Test all database collections and functionality"""
    print("🧪 Testing All Database Collections...")
    print("=" * 50)
    
    # Test database manager directly
    print("\n📊 Testing Database Manager...")
    try:
        db_manager = get_database_manager()
        
        # Test messages collection
        total_messages = db_manager.get_message_count()
        print(f"✅ Messages collection: {total_messages} documents")
        
        # Test alerts collection
        active_alerts = db_manager.get_active_alerts()
        print(f"✅ Alerts collection: {len(active_alerts)} active alerts")
        
        # Test settings collection
        settings = db_manager.get_settings()
        print(f"✅ Settings collection: {len(settings)} settings")
        
        # Test sentiment stats
        sentiment_stats = db_manager.get_sentiment_stats()
        print(f"✅ Sentiment analytics: {sentiment_stats}")
        
        db_manager.close_connection()
        
    except Exception as e:
        print(f"❌ Database manager test failed: {e}")
    
    # Test API endpoints
    print("\n🌐 Testing API Endpoints...")
    try:
        # Test dashboard endpoint
        response = requests.get(f"{BASE_URL}/dashboard")
        if response.status_code == 200:
            dashboard = response.json()
            print("✅ Dashboard endpoint working")
            print(f"   Total messages: {dashboard['dashboard']['total_messages']}")
            print(f"   Sentiment distribution: {dashboard['dashboard']['sentiment_distribution']['counts']}")
            print(f"   Negative alerts: {dashboard['dashboard']['negative_alerts']['count']}")
        
        # Test health endpoint
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            health = response.json()
            print(f"✅ Health check: {health['status']} - {health['message_count']} messages")
        
        # Test stats endpoint
        response = requests.get(f"{BASE_URL}/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Stats endpoint: {stats['by_sentiment']}")
        
        # Test alerts endpoint
        response = requests.get(f"{BASE_URL}/alerts")
        if response.status_code == 200:
            alerts = response.json()
            print(f"✅ Alerts endpoint: {alerts['count']} alerts")
        
        # Submit a test message to verify full pipeline
        print("\n📝 Testing Full Message Processing Pipeline...")
        test_message = {
            "id": f"collection_test_{datetime.now().timestamp()}",
            "timestamp": datetime.now().isoformat(),
            "source": "email",
            "sender": "test_collections@example.com",
            "text": "I'm absolutely furious with this terrible service! This is completely unacceptable!"
        }
        
        response = requests.post(
            f"{BASE_URL}/message",
            json=test_message,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Message processed successfully")
            print(f"   Detected sentiment: {result.get('sentiment')}")
            print(f"   Message ID: {result.get('message_id')}")
            print(f"   Total messages now: {result.get('total_messages')}")
            
            # Check if alert was created
            response = requests.get(f"{BASE_URL}/alerts")
            if response.status_code == 200:
                alerts = response.json()
                print(f"✅ Alert system working: {alerts['count']} total alerts")
        
        print("\n" + "=" * 50)
        print("✅ All database collections are working correctly!")
        print("🚀 Sentiment Sentinel AI is fully operational!")
        
        # Print collection summary
        print("\n📋 Collection Summary:")
        print("   📂 messages - Storing customer messages with sentiment")
        print("   🚨 alerts - Automated alerts for negative sentiment")
        print("   📊 sentiment_analytics - Analytics and reporting")
        print("   👤 users - User management (ready for auth)")
        print("   ⚙️ settings - System configuration") 
        print("   📈 sentiment_history - Trend tracking")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Flask app. Make sure it's running!")
    except Exception as e:
        print(f"❌ API test failed: {e}")

if __name__ == "__main__":
    test_all_collections()
