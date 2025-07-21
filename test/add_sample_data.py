#!/usr/bin/env python3
"""
Script to populate database with sample email messages for each sentiment type
Adds 10 messages each for: angry, happy/joy, confused, and neutral sentiments
"""

import requests
import json
from datetime import datetime, timedelta
import random
import time

BASE_URL = "http://localhost:5000"

# Sample email messages for different sentiments
sample_messages = {
    "angry": [
        "I am extremely frustrated with your terrible customer service! This is completely unacceptable!",
        "Your product is absolutely garbage! I want my money back immediately!",
        "I'm furious about the delay in my order. This is the worst experience ever!",
        "Your support team is incompetent! I'm never using your service again!",
        "This is outrageous! I've been waiting for hours with no response!",
        "I'm disgusted with the quality of your product. Complete waste of money!",
        "Your website is broken and your support is useless! Fix this now!",
        "I'm livid about this billing error. How can you be so careless?",
        "This is the most frustrating experience I've ever had with any company!",
        "I'm absolutely fed up with your poor service quality!"
    ],
    "happy": [
        "Thank you so much for the excellent service! I'm very satisfied with my purchase.",
        "Your team is amazing! The product exceeded my expectations completely.",
        "I'm delighted with the quick resolution. Outstanding customer support!",
        "Fantastic experience! Your service is top-notch and I'm very happy.",
        "Wonderful job on the delivery! Everything arrived perfectly and I'm thrilled.",
        "I'm so grateful for your help. This is exactly what I needed!",
        "Excellent work! Your product has made my life so much easier and I love it.",
        "Thank you for the prompt response! I'm really impressed with your service.",
        "Great quality product! I'm very pleased with my purchase and will recommend it.",
        "Outstanding customer service! You've made me a very happy customer today."
    ],
    "confused": [
        "I'm not sure how to use this feature. Can someone please explain it to me?",
        "I'm confused about the billing process. How does this work exactly?",
        "Can you help me understand what this error message means?",
        "I'm uncertain about which option to choose. What would you recommend?",
        "I don't understand the installation instructions. They're not clear to me.",
        "I'm puzzled by the pricing structure. Can someone clarify this for me?",
        "I'm having trouble figuring out how to access my account. Need guidance.",
        "The documentation is confusing. Can you provide a simpler explanation?",
        "I'm not clear on what the next steps should be. What do I do now?",
        "I'm bewildered by all these options. Which one should I select?"
    ],
    "neutral": [
        "I received your message about the order update. Please send me the tracking information.",
        "Could you please provide the documentation for this product?",
        "I need to update my billing address. Here are the new details.",
        "Please confirm the delivery date for my order #12345.",
        "I would like to inquire about your return policy for this item.",
        "Can you send me the invoice for last month's purchase?",
        "I need assistance with downloading the software. Please provide the link.",
        "Could you please explain the features included in the premium plan?",
        "I want to schedule a callback for tomorrow between 2-4 PM.",
        "Please update my email address in your system to this new one."
    ]
}

# Sample customer names and email addresses
customers = [
    ("Sarah Johnson", "sarah.johnson@email.com"),
    ("Mike Chen", "mike.chen@email.com"), 
    ("Emma Davis", "emma.davis@email.com"),
    ("James Wilson", "james.wilson@email.com"),
    ("Lisa Rodriguez", "lisa.rodriguez@email.com"),
    ("David Kim", "david.kim@email.com"),
    ("Anna Thompson", "anna.thompson@email.com"),
    ("Robert Brown", "robert.brown@email.com"),
    ("Jessica Lee", "jessica.lee@email.com"),
    ("Michael Garcia", "michael.garcia@email.com")
]

def send_message(sentiment, text, customer_name, customer_email, message_id):
    """Send a message to the backend API"""
    
    # Generate a timestamp (random time in the last 24 hours)
    now = datetime.now()
    random_hours = random.uniform(0, 24)
    message_time = now - timedelta(hours=random_hours)
    
    message_data = {
        "id": message_id,
        "timestamp": message_time.isoformat(),
        "source": "email",
        "sender": customer_email,
        "text": text,
        "customer_name": customer_name
        # Note: Not including sentiment here to let Gemini AI classify it naturally
    }
    
    try:
        response = requests.post(f"{BASE_URL}/message", json=message_data, timeout=10)
        if response.status_code == 201:
            result = response.json()
            detected_sentiment = result.get('sentiment', 'unknown')
            print(f"✅ Added message from {customer_name} -> Detected: {detected_sentiment}")
            print(f"   Text: {text[:60]}...")
            return True
        else:
            print(f"❌ Failed to add message: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error sending message: {e}")
        return False

def populate_database():
    """Populate database with sample messages for each sentiment"""
    print("🚀 Starting database population with sample email messages...")
    print("=" * 70)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code != 200:
            raise Exception("Server not responding correctly")
        print("✅ Backend server is running")
    except Exception as e:
        print(f"❌ Backend server is not accessible: {e}")
        print("Please make sure your Flask server is running on http://localhost:5000")
        return
    
    total_messages = 0
    successful_messages = 0
    
    # Add messages for each sentiment type
    for intended_sentiment, messages in sample_messages.items():
        print(f"\n📧 Adding 10 messages with {intended_sentiment} content...")
        
        for i, message_text in enumerate(messages):
            customer_name, customer_email = customers[i]
            message_id = f"{intended_sentiment}_{int(time.time())}_{i+1}"
            
            if send_message(intended_sentiment, message_text, customer_name, customer_email, message_id):
                successful_messages += 1
            
            total_messages += 1
            
            # Small delay to avoid overwhelming the server and Gemini API
            time.sleep(2)  # 2 seconds delay for API rate limiting
    
    print("\n" + "=" * 70)
    print("📊 DATABASE POPULATION SUMMARY")
    print("=" * 70)
    print(f"Total messages attempted: {total_messages}")
    print(f"Successfully added: {successful_messages}")
    print(f"Failed: {total_messages - successful_messages}")
    
    if successful_messages > 0:
        print(f"\n🎉 Successfully populated database with {successful_messages} sample messages!")
        print("\n📈 Message breakdown by intended sentiment:")
        print(f"   • Angry content: {len(sample_messages['angry'])} messages")
        print(f"   • Happy content: {len(sample_messages['happy'])} messages")
        print(f"   • Confused content: {len(sample_messages['confused'])} messages")
        print(f"   • Neutral content: {len(sample_messages['neutral'])} messages")
        
        print("\n💡 Your dashboard should now show:")
        print("   • Updated emotion overview cards with real counts")
        print("   • Real-time emotion trends with actual data")
        print("   • Recent flagged conversations in the tickets section")
        
        print("\n🔄 Next steps:")
        print("   1. Refresh your dashboard to see the new data")
        print("   2. Click the 'Live' button to see real-time updates")
        print("   3. Test the emotion trend charts with actual data")
        
        # Test the APIs
        print("\n🧪 Testing dashboard APIs...")
        try:
            health_response = requests.get(f"{BASE_URL}/health")
            if health_response.status_code == 200:
                health_data = health_response.json()
                print(f"   ✅ Health check: {health_data.get('message_count', 0)} total messages in DB")
            
            overview_response = requests.get(f"{BASE_URL}/api/emotion-overview")
            if overview_response.status_code == 200:
                overview_data = overview_response.json()
                print("   ✅ Emotion overview API working")
                for emotion, data in overview_data.items():
                    if isinstance(data, dict) and 'count' in data:
                        print(f"      • {emotion.title()}: {data['count']} messages")
            
        except Exception as e:
            print(f"   ⚠️  Error testing APIs: {e}")
        
    else:
        print("\n⚠️  No messages were successfully added.")
        print("Please check your backend server and database connection.")

if __name__ == "__main__":
    populate_database()
