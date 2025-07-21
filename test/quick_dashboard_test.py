#!/usr/bin/env python3
"""
Quick Dashboard Test - Auto-run version (no user input required)
Tests dashboard with messages sent every 2 minutes for 15 minutes
"""

import requests
import json
from datetime import datetime, timedelta
import time
import random
from live_dashboard_test import DashboardTester, TEST_MESSAGES, CUSTOMERS

def run_quick_test():
    """Run a quick 15-minute test automatically"""
    print(f"🚀 STARTING QUICK DASHBOARD TEST")
    print("=" * 60)
    print(f"⏱️  Duration: 15 minutes")
    print(f"📧 Message Interval: 2 minutes")
    print(f"🎯 Expected Messages: ~7-8 messages")
    print(f"🕐 Start Time: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 60)
    
    tester = DashboardTester()
    
    # Test initial connectivity
    print("\n🔍 Testing initial API connectivity...")
    api_results = tester.test_dashboard_apis()
    if not api_results:
        print("❌ Cannot connect to APIs. Please ensure Flask server is running.")
        return
    
    tester.print_dashboard_summary(api_results)
    
    # Run for 15 minutes with 2-minute intervals
    duration_minutes = 15
    interval_minutes = 2
    end_time = datetime.now() + timedelta(minutes=duration_minutes)
    
    message_count = 0
    
    try:
        while datetime.now() < end_time:
            # Send a message
            print(f"\n📤 [{datetime.now().strftime('%H:%M:%S')}] Sending message #{message_count + 1}...")
            
            # Weighted distribution for realistic data
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
            
            success = tester.send_message(emotion, text, customer_name, customer_email)
            
            if success:
                message_count += 1
                
                # Test APIs every 2 messages and show dashboard state
                if message_count % 2 == 0:
                    print(f"\n🧪 Testing dashboard APIs after {message_count} messages...")
                    api_results = tester.test_dashboard_apis()
                    tester.print_dashboard_summary(api_results)
            
            # Wait for next interval (if time remains)
            remaining_time = end_time - datetime.now()
            if remaining_time.total_seconds() > interval_minutes * 60:
                next_message_time = datetime.now() + timedelta(minutes=interval_minutes)
                print(f"\n⏳ Waiting {interval_minutes} minutes until next message...")
                print(f"   Next message at: {next_message_time.strftime('%H:%M:%S')}")
                print(f"   Test ends at: {end_time.strftime('%H:%M:%S')}")
                time.sleep(interval_minutes * 60)
            else:
                break
                
    except KeyboardInterrupt:
        print("\n⏹️  Test stopped by user")
    
    # Final summary
    print(f"\n🏁 QUICK TEST COMPLETED")
    print("=" * 60)
    final_results = tester.test_dashboard_apis()
    tester.print_dashboard_summary(final_results)
    
    print(f"\n🎯 DASHBOARD VALIDATION COMPLETE")
    print(f"   📧 Total messages sent: {message_count}")
    print(f"   ⏱️  Test duration: {datetime.now() - tester.test_start_time}")
    print(f"   📈 Emotion distribution: {dict(tester.emotion_stats)}")
    
    print(f"\n💡 NEXT STEPS:")
    print(f"   • Open your dashboard at: http://localhost:3000")
    print(f"   • Click 'Live' button to see real-time updates")  
    print(f"   • Check emotion percentages are updating")
    print(f"   • Verify flagged conversations show angry messages")
    print(f"   • Watch emotion trends chart for data points")
    print("=" * 60)

if __name__ == "__main__":
    run_quick_test()
