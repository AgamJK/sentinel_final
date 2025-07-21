#!/usr/bin/env python3
"""
Comprehensive Dashboard Test - Live Analytics Simulation
Sends messages every 5 minutes for 1 hour to test dashboard functionality
"""

import requests
import json
from datetime import datetime, timedelta
import time
import random
import threading
from typing import List, Dict

BASE_URL = "http://localhost:5000"

# Sample messages for different emotions
TEST_MESSAGES = {
    "angry": [
        "I am absolutely furious with this service! This is completely unacceptable!",
        "Your product is garbage and your support team is useless!",
        "I'm disgusted with the quality and want my money back immediately!",
        "This is the worst experience I've ever had! Fix this now!",
        "I'm livid about this delay. Your company is incompetent!",
        "This is outrageous! I demand to speak to a manager right now!",
        "I hate this service! It's terrible and broken!",
        "Your website is completely useless and frustrating!",
    ],
    "happy": [
        "Thank you so much! This service is absolutely amazing!",
        "I'm thrilled with the quality of your product. Outstanding work!",
        "Excellent customer service! You've exceeded my expectations!",
        "I love this product! It's exactly what I needed. Thank you!",
        "Fantastic experience! Your team is wonderful and helpful!",
        "Perfect! This is exactly what I was looking for. Great job!",
        "Amazing quality and fast delivery! I'm very satisfied!",
        "Outstanding support! You've made my day. Thank you so much!",
    ],
    "confused": [
        "I'm not sure how to use this feature. Can you help me understand?",
        "I'm confused about the pricing structure. Can you clarify this?",
        "I don't understand these instructions. They're unclear to me.",
        "Can you explain how this works? I'm having trouble figuring it out.",
        "I'm uncertain about which option to choose. What do you recommend?",
        "The documentation is confusing. Can you provide a simpler explanation?",
        "I'm puzzled by this error message. What does it mean?",
        "I'm not clear on the next steps. What should I do now?",
    ],
    "neutral": [
        "I received your message about the order update. Please send tracking info.",
        "Could you please provide the documentation for this product?",
        "I need to update my billing address. Here are the new details.",
        "Please confirm the delivery date for my order.",
        "I would like to inquire about your return policy.",
        "Can you send me the invoice for last month's purchase?",
        "I need assistance with downloading the software.",
        "Please schedule a callback for tomorrow afternoon.",
    ]
}

# Sample customer data
CUSTOMERS = [
    ("Alice Johnson", "alice.johnson@email.com"),
    ("Bob Smith", "bob.smith@email.com"),
    ("Carol Davis", "carol.davis@email.com"),
    ("David Wilson", "david.wilson@email.com"),
    ("Emma Brown", "emma.brown@email.com"),
    ("Frank Miller", "frank.miller@email.com"),
    ("Grace Taylor", "grace.taylor@email.com"),
    ("Henry Anderson", "henry.anderson@email.com"),
    ("Iris Clark", "iris.clark@email.com"),
    ("Jack Thompson", "jack.thompson@email.com"),
]

class DashboardTester:
    def __init__(self):
        self.messages_sent = 0
        self.test_start_time = datetime.now()
        self.test_running = False
        self.emotion_stats = {"angry": 0, "happy": 0, "confused": 0, "neutral": 0}
        
    def send_message(self, emotion: str, text: str, customer_name: str, customer_email: str) -> bool:
        """Send a message to the backend API"""
        
        message_data = {
            "id": f"test_{emotion}_{int(time.time())}_{self.messages_sent}",
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
                print(f"✅ [{datetime.now().strftime('%H:%M:%S')}] Sent {emotion} message -> Detected: {detected_sentiment}")
                print(f"   From: {customer_name} ({customer_email})")
                print(f"   Text: {text[:60]}...")
                self.emotion_stats[emotion] += 1
                self.messages_sent += 1
                return True
            else:
                print(f"❌ Failed to send message: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Error sending message: {e}")
            return False
    
    def test_dashboard_apis(self) -> Dict:
        """Test all dashboard APIs and return results"""
        print(f"\n🧪 [{datetime.now().strftime('%H:%M:%S')}] Testing Dashboard APIs...")
        
        api_results = {}
        
        # Test emotion overview
        try:
            response = requests.get(f"{BASE_URL}/api/emotion-overview", timeout=5)
            if response.status_code == 200:
                api_results['emotion_overview'] = response.json()
                print("   ✅ Emotion Overview API working")
            else:
                print(f"   ❌ Emotion Overview API failed: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Emotion Overview API error: {e}")
        
        # Test emotion trends
        try:
            response = requests.get(f"{BASE_URL}/api/emotion-trends?hours=2", timeout=5)
            if response.status_code == 200:
                api_results['emotion_trends'] = response.json()
                print("   ✅ Emotion Trends API working")
            else:
                print(f"   ❌ Emotion Trends API failed: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Emotion Trends API error: {e}")
        
        # Test alerts/flagged conversations
        try:
            response = requests.get(f"{BASE_URL}/alerts?limit=5", timeout=5)
            if response.status_code == 200:
                api_results['alerts'] = response.json()
                print("   ✅ Alerts API working")
            else:
                print(f"   ❌ Alerts API failed: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Alerts API error: {e}")
        
        # Test realtime stats
        try:
            response = requests.get(f"{BASE_URL}/api/realtime-stats", timeout=5)
            if response.status_code == 200:
                api_results['realtime_stats'] = response.json()
                print("   ✅ Realtime Stats API working")
            else:
                print(f"   ❌ Realtime Stats API failed: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Realtime Stats API error: {e}")
        
        return api_results
    
    def print_dashboard_summary(self, api_results: Dict):
        """Print a summary of current dashboard state"""
        print(f"\n📊 [{datetime.now().strftime('%H:%M:%S')}] DASHBOARD SUMMARY")
        print("=" * 70)
        
        # Emotion Overview
        if 'emotion_overview' in api_results:
            overview = api_results['emotion_overview']
            print("🎯 Emotion Overview:")
            for emotion, data in overview.items():
                if isinstance(data, dict):
                    count = data.get('count', 0)
                    percentage = data.get('percentage_text', 'N/A')
                    print(f"   • {emotion.title()}: {count} messages ({percentage})")
        
        # Emotion Trends
        if 'emotion_trends' in api_results:
            trends = api_results['emotion_trends']
            if 'trends' in trends and trends['trends']:
                active_periods = [t for t in trends['trends'] if sum(t.values()) - 1 > 0]  # -1 for 'time' key
                print(f"\n📈 Emotion Trends: {len(active_periods)} active time periods")
                if active_periods:
                    latest = active_periods[-1]
                    print(f"   Latest period ({latest['time']}): Anger={latest.get('anger', 0)}, Joy={latest.get('joy', 0)}, Confusion={latest.get('confusion', 0)}, Neutral={latest.get('neutral', 0)}")
        
        # Recent Alerts
        if 'alerts' in api_results:
            alerts = api_results['alerts']
            alert_count = alerts.get('count', 0)
            print(f"\n🚨 Recent Flagged Conversations: {alert_count} alerts")
            if 'messages' in alerts and alerts['messages']:
                for i, msg in enumerate(alerts['messages'][:3], 1):
                    sender = msg.get('sender', 'Unknown')[:30]
                    emotion = msg.get('sentiment', 'unknown')
                    print(f"   {i}. {sender} - {emotion.title()}")
        
        print(f"\n⏱️  Test Runtime: {datetime.now() - self.test_start_time}")
        print(f"📧 Messages Sent: {self.messages_sent}")
        print(f"📈 Distribution: {dict(self.emotion_stats)}")
        print("=" * 70)
    
    def send_random_message(self):
        """Send a random message with weighted distribution"""
        # Weighted distribution: more neutral and happy, some angry and confused
        emotion_weights = {
            "neutral": 0.4,   # 40%
            "happy": 0.3,     # 30%
            "angry": 0.2,     # 20%
            "confused": 0.1   # 10%
        }
        
        emotion = random.choices(
            list(emotion_weights.keys()), 
            weights=list(emotion_weights.values())
        )[0]
        
        text = random.choice(TEST_MESSAGES[emotion])
        customer_name, customer_email = random.choice(CUSTOMERS)
        
        return self.send_message(emotion, text, customer_name, customer_email)
    
    def run_live_test(self, duration_hours: float = 1.0, interval_minutes: int = 5):
        """Run the live dashboard test for specified duration"""
        print(f"🚀 STARTING LIVE DASHBOARD TEST")
        print("=" * 70)
        print(f"⏱️  Duration: {duration_hours} hour(s)")
        print(f"📧 Message Interval: {interval_minutes} minutes")
        print(f"🎯 Expected Messages: ~{int(duration_hours * 60 / interval_minutes)} messages")
        print(f"🕐 Start Time: {self.test_start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        # Test initial API connectivity
        print("\n🔍 Testing initial API connectivity...")
        api_results = self.test_dashboard_apis()
        if not api_results:
            print("❌ Cannot connect to dashboard APIs. Please ensure the Flask server is running.")
            return
        
        self.test_running = True
        end_time = self.test_start_time + timedelta(hours=duration_hours)
        interval_seconds = interval_minutes * 60
        
        try:
            while datetime.now() < end_time and self.test_running:
                # Send a random message
                print(f"\n📤 [{datetime.now().strftime('%H:%M:%S')}] Sending random message...")
                success = self.send_random_message()
                
                if success:
                    # Test dashboard APIs every few messages
                    if self.messages_sent % 3 == 0:  # Test APIs every 3rd message
                        api_results = self.test_dashboard_apis()
                        self.print_dashboard_summary(api_results)
                
                # Wait for next interval
                remaining_time = end_time - datetime.now()
                if remaining_time.total_seconds() > interval_seconds:
                    print(f"⏳ Waiting {interval_minutes} minutes until next message...")
                    print(f"   Next message at: {(datetime.now() + timedelta(seconds=interval_seconds)).strftime('%H:%M:%S')}")
                    print(f"   Test ends at: {end_time.strftime('%H:%M:%S')}")
                    time.sleep(interval_seconds)
                else:
                    break
        
        except KeyboardInterrupt:
            print("\n⏹️  Test stopped by user")
            self.test_running = False
        
        # Final summary
        print(f"\n🏁 LIVE TEST COMPLETED")
        print("=" * 70)
        final_api_results = self.test_dashboard_apis()
        self.print_dashboard_summary(final_api_results)
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        print(f"   • Refresh your dashboard to see the latest data")
        print(f"   • Click 'Live' button in emotion trends to see real-time updates")
        print(f"   • Check Recent Flagged Conversations for angry messages")
        print(f"   • Verify emotion percentages are updating correctly")
        print("=" * 70)

def main():
    print("🧪 COMPREHENSIVE DASHBOARD ANALYTICS TEST")
    print("This test will simulate real customer interactions to verify dashboard functionality")
    print()
    
    # Get user preferences
    try:
        duration = float(input("Enter test duration in hours (default: 1.0): ") or "1.0")
        interval = int(input("Enter message interval in minutes (default: 5): ") or "5")
    except ValueError:
        duration = 1.0
        interval = 5
    
    print(f"\n✅ Configuration:")
    print(f"   Duration: {duration} hour(s)")
    print(f"   Interval: {interval} minute(s)")
    print(f"   Expected messages: ~{int(duration * 60 / interval)}")
    
    confirm = input(f"\nStart live test? (y/N): ").lower().strip()
    if confirm in ['y', 'yes']:
        tester = DashboardTester()
        tester.run_live_test(duration, interval)
    else:
        print("Test cancelled.")

if __name__ == "__main__":
    main()
