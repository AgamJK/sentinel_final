#!/usr/bin/env python3
"""
Simple Dashboard Test - Sends a few messages and tests the APIs
"""

import requests
import json
from datetime import datetime
import random

BASE_URL = "http://localhost:5000"

# Sample messages for testing
TEST_MESSAGES = {
    "angry": [
        "I am absolutely furious with this service! This is completely unacceptable!",
        "Your product is garbage and your support team is useless!",
        "I'm disgusted with the quality and want my money back immediately!",
    ],
    "happy": [
        "Thank you so much! This service is absolutely amazing!",
        "I'm thrilled with the quality of your product. Outstanding work!",
        "Excellent customer service! You've exceeded my expectations!",
    ],
    "confused": [
        "I'm not sure how to use this feature. Can you help me understand?",
        "I'm confused about the pricing structure. Can you clarify this?",
        "I don't understand these instructions. They're unclear to me.",
    ],
    "neutral": [
        "I received your message about the order update. Please send tracking info.",
        "Could you please provide the documentation for this product?",
        "I need to update my billing address. Here are the new details.",
    ]
}

CUSTOMERS = [
    ("Alice Johnson", "alice.johnson@email.com"),
    ("Bob Smith", "bob.smith@email.com"),
    ("Carol Davis", "carol.davis@email.com"),
    ("David Wilson", "david.wilson@email.com"),
]

def send_test_message(emotion, text, customer_name, customer_email):
    """Send a test message"""
    message_data = {
        "id": f"test_{emotion}_{datetime.now().strftime('%H%M%S')}",
        "timestamp": datetime.now().isoformat(),
        "source": "email",
        "sender": customer_email,
        "text": text,
        "customer_name": customer_name
    }
    
    try:
        response = requests.post(f"{BASE_URL}/message", json=message_data, timeout=10)
        if response.status_code == 201:
            result = response.json()
            detected_sentiment = result.get('sentiment', 'unknown')
            print(f"✅ Sent {emotion} -> Detected: {detected_sentiment}")
            print(f"   From: {customer_name}")
            print(f"   Text: {text[:50]}...")
            return True
        else:
            print(f"❌ Failed to send: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_dashboard_apis():
    """Test all dashboard APIs"""
    print(f"\n🧪 Testing Dashboard APIs at {datetime.now().strftime('%H:%M:%S')}")
    
    # Test emotion overview
    try:
        response = requests.get(f"{BASE_URL}/api/emotion-overview", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Emotion Overview:")
            for emotion, info in data.items():
                if isinstance(info, dict) and 'count' in info:
                    print(f"   • {emotion.title()}: {info['count']} messages ({info.get('percentage_text', 'N/A')})")
        else:
            print(f"❌ Emotion Overview failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Emotion Overview error: {e}")
    
    # Test alerts
    try:
        response = requests.get(f"{BASE_URL}/alerts?limit=5", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Flagged Conversations: {data.get('count', 0)} alerts")
            if 'messages' in data and data['messages']:
                for i, msg in enumerate(data['messages'][:3], 1):
                    sender = msg.get('sender', 'Unknown')[:25]
                    emotion = msg.get('sentiment', 'unknown')
                    print(f"   {i}. {sender} - {emotion.title()}")
        else:
            print(f"❌ Alerts failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Alerts error: {e}")
    
    # Test emotion trends  
    try:
        response = requests.get(f"{BASE_URL}/api/emotion-trends?hours=1", timeout=5)
        if response.status_code == 200:
            data = response.json()
            trends = data.get('trends', [])
            print(f"✅ Emotion Trends: {len(trends)} time periods")
        else:
            print(f"❌ Trends failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Trends error: {e}")

def main():
    print("🚀 SIMPLE DASHBOARD ANALYTICS TEST")
    print("=" * 50)
    print(f"🕐 Start Time: {datetime.now().strftime('%H:%M:%S')}")
    
    # Test initial state
    test_dashboard_apis()
    
    # Send test messages
    print(f"\n📤 Sending test messages...")
    emotions_to_test = ["angry", "happy", "confused", "neutral", "angry"]  # Extra angry for flagged
    
    for i, emotion in enumerate(emotions_to_test, 1):
        print(f"\n📧 Message {i}/5: Sending {emotion} message...")
        text = random.choice(TEST_MESSAGES[emotion])
        customer_name, customer_email = random.choice(CUSTOMERS)
        
        success = send_test_message(emotion, text, customer_name, customer_email)
        
        if success and i % 2 == 0:  # Test APIs every 2 messages
            test_dashboard_apis()
    
    # Final test
    print(f"\n🏁 FINAL DASHBOARD STATE")
    print("=" * 50)
    test_dashboard_apis()
    
    print(f"\n💡 VALIDATION COMPLETE!")
    print("   • Check your dashboard for updated emotion counts")
    print("   • Look for new flagged conversations (angry messages)")
    print("   • Emotion percentages should reflect new data")
    print("   • Trends should show recent activity")
    print("=" * 50)

if __name__ == "__main__":
    main()
