#!/usr/bin/env python3
"""
Test script to verify sentiment analysis integration
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000"

def test_sentiment_features():
    """Test all sentiment-related features"""
    print("🧠 Testing Sentiment Analysis Integration...")
    
    # Test messages with different sentiments
    test_messages = [
        {
            "id": f"sentiment_test_angry_{datetime.now().timestamp()}",
            "timestamp": datetime.now().isoformat(),
            "source": "chat",
            "sender": "angry_customer@example.com",
            "text": "This is absolutely terrible! I'm furious about the poor service and I want my money back immediately!"
        },
        {
            "id": f"sentiment_test_happy_{datetime.now().timestamp()}",
            "timestamp": datetime.now().isoformat(),
            "source": "email",
            "sender": "happy_customer@example.com",
            "text": "Thank you so much! Your team was incredibly helpful and I'm very satisfied with the resolution."
        },
        {
            "id": f"sentiment_test_confused_{datetime.now().timestamp()}",
            "timestamp": datetime.now().isoformat(),
            "source": "ticket",
            "sender": "confused_customer@example.com",
            "text": "I'm not sure I understand how this works. Can someone please explain the process to me?"
        }
    ]
    
    try:
        print("\n📝 Testing sentiment analysis on message submission...")
        for message in test_messages:
            print(f"Sending message: '{message['text'][:50]}...'")
            response = requests.post(
                f"{BASE_URL}/message",
                json=message,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 201:
                result = response.json()
                print(f"✅ Detected sentiment: {result.get('sentiment', 'unknown')}")
            else:
                print(f"❌ Failed: {response.status_code}")
        
        print("\n📊 Testing sentiment statistics...")
        response = requests.get(f"{BASE_URL}/stats")
        if response.status_code == 200:
            stats = response.json()
            print("✅ Stats retrieved:")
            print(f"   Total messages: {stats.get('total_messages')}")
            print(f"   Sentiment breakdown: {stats.get('by_sentiment', {})}")
        
        print("\n🔍 Testing sentiment filtering...")
        # Test filtering by angry sentiment
        response = requests.get(f"{BASE_URL}/sentiment/angry")
        if response.status_code == 200:
            angry_messages = response.json()
            print(f"✅ Found {angry_messages.get('count', 0)} angry messages")
        
        # Test filtering by happy sentiment
        response = requests.get(f"{BASE_URL}/sentiment/happy")
        if response.status_code == 200:
            happy_messages = response.json()
            print(f"✅ Found {happy_messages.get('count', 0)} happy messages")
        
        print("\n🚨 Testing negative sentiment alerts...")
        response = requests.get(f"{BASE_URL}/alerts")
        if response.status_code == 200:
            alerts = response.json()
            print(f"✅ Found {alerts.get('count', 0)} negative sentiment alerts")
            if alerts.get('messages'):
                for msg in alerts['messages'][:2]:  # Show first 2
                    sentiment = msg.get('sentiment', msg.get('emotion', 'unknown'))
                    print(f"   Alert: {sentiment} - {msg['text'][:50]}...")
        
        print("\n🧪 Testing standalone sentiment analysis...")
        test_text = "I'm extremely disappointed with this product. It doesn't work as advertised!"
        response = requests.post(
            f"{BASE_URL}/analyze",
            json={"text": test_text},
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code == 200:
            analysis = response.json()
            print(f"✅ Analyzed text sentiment: {analysis.get('sentiment')}")
            print(f"   Text: {analysis.get('text')[:50]}...")
        
        print("\n✅ All sentiment analysis tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Flask app. Make sure it's running on http://127.0.0.1:5000")
    except Exception as e:
        print(f"❌ Sentiment test failed: {e}")

if __name__ == "__main__":
    test_sentiment_features()
