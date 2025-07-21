#!/usr/bin/env python3
"""
Comprehensive test suite for dashboard endpoints
Tests the following endpoints:
- /dashboard
- /api/emotion-overview
- /api/emotion-trends  
- /api/realtime-stats
"""

import requests
import json
import time
import unittest
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_URL = "http://localhost:5000"

class DashboardEndpointsTest(unittest.TestCase):
    """Test suite for dashboard endpoints"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test data before running tests"""
        print("\n🔧 Setting up test data...")
        cls.setup_test_data()
    
    @classmethod
    def setup_test_data(cls):
        """Insert sample messages for testing"""
        sample_messages = [
            {
                "id": f"test_dashboard_{int(time.time())}_1",
                "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
                "source": "email",
                "sender": "angry_customer@test.com",
                "text": "I'm extremely frustrated with your terrible service! This is unacceptable!"
            },
            {
                "id": f"test_dashboard_{int(time.time())}_2",
                "timestamp": (datetime.now() - timedelta(hours=1)).isoformat(),
                "source": "chat",
                "sender": "confused_user@test.com",
                "text": "I'm really confused about how this works. Can someone help me understand?"
            },
            {
                "id": f"test_dashboard_{int(time.time())}_3",
                "timestamp": datetime.now().isoformat(),
                "source": "ticket",
                "sender": "happy_customer@test.com",
                "text": "Thank you so much! Your team is amazing and I'm very satisfied with the resolution."
            },
            {
                "id": f"test_dashboard_{int(time.time())}_4",
                "timestamp": datetime.now().isoformat(),
                "source": "email",
                "sender": "neutral_user@test.com",
                "text": "I received your message. Please send me the documentation."
            },
            {
                "id": f"test_dashboard_{int(time.time())}_5",
                "timestamp": (datetime.now() - timedelta(minutes=30)).isoformat(),
                "source": "chat",
                "sender": "another_happy@test.com",
                "text": "Excellent work! I'm really happy with the service quality."
            }
        ]
        
        success_count = 0
        for msg in sample_messages:
            try:
                response = requests.post(f"{BASE_URL}/message", json=msg, timeout=10)
                if response.status_code == 201:
                    success_count += 1
            except Exception as e:
                print(f"⚠️  Failed to send sample message: {e}")
        
        print(f"✅ Successfully inserted {success_count}/{len(sample_messages)} test messages")
        time.sleep(2)  # Give time for processing

    def test_server_running(self):
        """Test if the Flask server is running"""
        try:
            response = requests.get(f"{BASE_URL}/", timeout=5)
            self.assertEqual(response.status_code, 200)
            print("✅ Server is running")
        except requests.exceptions.ConnectionError:
            self.fail("❌ Flask server is not running. Please start the server first.")

    def test_dashboard_endpoint(self):
        """Test /dashboard endpoint"""
        print("\n🧪 Testing /dashboard endpoint...")
        
        try:
            response = requests.get(f"{BASE_URL}/dashboard", timeout=10)
            
            # Test status code
            self.assertEqual(response.status_code, 200, f"Expected 200, got {response.status_code}")
            
            # Parse JSON response
            data = response.json()
            
            # Test response structure
            self.assertIn('dashboard', data)
            dashboard = data['dashboard']
            
            # Test required fields
            required_fields = ['total_messages', 'sentiment_distribution', 'recent_messages', 'negative_alerts']
            for field in required_fields:
                self.assertIn(field, dashboard, f"Missing required field: {field}")
            
            # Test sentiment distribution structure
            sentiment_dist = dashboard['sentiment_distribution']
            self.assertIn('counts', sentiment_dist)
            self.assertIn('percentages', sentiment_dist)
            
            # Test data types
            self.assertIsInstance(dashboard['total_messages'], int)
            self.assertIsInstance(dashboard['recent_messages'], list)
            self.assertIsInstance(dashboard['negative_alerts'], dict)
            
            print(f"   ✅ Total messages: {dashboard['total_messages']}")
            print(f"   ✅ Sentiment counts: {sentiment_dist['counts']}")
            print(f"   ✅ Recent messages count: {len(dashboard['recent_messages'])}")
            print(f"   ✅ Negative alerts count: {dashboard['negative_alerts']['count']}")
            
        except Exception as e:
            self.fail(f"❌ Dashboard endpoint test failed: {e}")

    def test_emotion_overview_endpoint(self):
        """Test /api/emotion-overview endpoint"""
        print("\n🧪 Testing /api/emotion-overview endpoint...")
        
        try:
            response = requests.get(f"{BASE_URL}/api/emotion-overview", timeout=10)
            
            # Test status code
            self.assertEqual(response.status_code, 200, f"Expected 200, got {response.status_code}")
            
            # Parse JSON response
            data = response.json()
            
            # Test that we get emotion data
            self.assertIsInstance(data, dict)
            
            # Expected emotion categories
            possible_emotions = ['anger', 'joy', 'confusion', 'neutral']
            
            # Test structure of emotion data
            for emotion, stats in data.items():
                if isinstance(stats, dict):
                    self.assertIn('count', stats, f"Missing 'count' in {emotion}")
                    self.assertIn('change_percent', stats, f"Missing 'change_percent' in {emotion}")
                    self.assertIsInstance(stats['count'], int)
                    self.assertIsInstance(stats['change_percent'], (int, float))
            
            print(f"   ✅ Emotion overview data received for {len(data)} emotions")
            for emotion, stats in data.items():
                if isinstance(stats, dict):
                    print(f"   • {emotion.title()}: {stats['count']} messages ({stats['change_percent']:+}%)")
            
        except Exception as e:
            self.fail(f"❌ Emotion overview endpoint test failed: {e}")

    def test_emotion_trends_endpoint(self):
        """Test /api/emotion-trends endpoint"""
        print("\n🧪 Testing /api/emotion-trends endpoint...")
        
        try:
            # Test default request
            response = requests.get(f"{BASE_URL}/api/emotion-trends", timeout=10)
            self.assertEqual(response.status_code, 200, f"Expected 200, got {response.status_code}")
            
            data = response.json()
            
            # Test response structure
            self.assertIn('trends', data)
            self.assertIn('time_range_hours', data)
            
            # Test data types
            self.assertIsInstance(data['trends'], dict)
            self.assertIsInstance(data['time_range_hours'], int)
            self.assertEqual(data['time_range_hours'], 6)  # Default value
            
            print(f"   ✅ Trends data for {data['time_range_hours']} hours")
            print(f"   ✅ Trends data points: {len(data['trends'])}")
            
            # Test with custom hours parameter
            response2 = requests.get(f"{BASE_URL}/api/emotion-trends?hours=12", timeout=10)
            self.assertEqual(response2.status_code, 200)
            
            data2 = response2.json()
            self.assertEqual(data2['time_range_hours'], 12)
            
            print(f"   ✅ Custom hours parameter works (tested with 12 hours)")
            
        except Exception as e:
            self.fail(f"❌ Emotion trends endpoint test failed: {e}")

    def test_realtime_stats_endpoint(self):
        """Test /api/realtime-stats endpoint"""
        print("\n🧪 Testing /api/realtime-stats endpoint...")
        
        try:
            response = requests.get(f"{BASE_URL}/api/realtime-stats", timeout=10)
            
            # Test status code
            self.assertEqual(response.status_code, 200, f"Expected 200, got {response.status_code}")
            
            # Parse JSON response
            data = response.json()
            
            # Test response structure
            required_fields = ['current_hour', 'total', 'timestamp']
            for field in required_fields:
                self.assertIn(field, data, f"Missing required field: {field}")
            
            # Test data types
            self.assertIsInstance(data['current_hour'], dict)
            self.assertIsInstance(data['total'], dict)
            self.assertIsInstance(data['timestamp'], str)
            
            # Test timestamp format
            try:
                datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00'))
            except ValueError:
                self.fail("Invalid timestamp format")
            
            print(f"   ✅ Current hour stats: {data['current_hour']}")
            print(f"   ✅ Total stats: {data['total']}")
            print(f"   ✅ Timestamp: {data['timestamp']}")
            
        except Exception as e:
            self.fail(f"❌ Realtime stats endpoint test failed: {e}")

    def test_error_handling(self):
        """Test error handling when database is not available"""
        print("\n🧪 Testing error handling scenarios...")
        
        # Test with invalid endpoint
        try:
            response = requests.get(f"{BASE_URL}/api/invalid-endpoint", timeout=10)
            self.assertEqual(response.status_code, 404)
            print("   ✅ 404 returned for invalid endpoint")
        except Exception as e:
            print(f"   ⚠️  Could not test invalid endpoint: {e}")

    def test_response_times(self):
        """Test response times for all endpoints"""
        print("\n⏱️  Testing response times...")
        
        endpoints = [
            "/dashboard",
            "/api/emotion-overview", 
            "/api/emotion-trends",
            "/api/realtime-stats"
        ]
        
        for endpoint in endpoints:
            try:
                start_time = time.time()
                response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
                end_time = time.time()
                
                response_time = (end_time - start_time) * 1000  # Convert to milliseconds
                
                if response.status_code == 200:
                    print(f"   ✅ {endpoint}: {response_time:.0f}ms")
                    # Assert reasonable response time (less than 5 seconds)
                    self.assertLess(response_time, 5000, f"Response time too slow for {endpoint}")
                else:
                    print(f"   ❌ {endpoint}: {response.status_code} status code")
                    
            except Exception as e:
                print(f"   ❌ {endpoint}: Error - {e}")

def run_quick_test():
    """Run a quick test without unittest framework"""
    print("🚀 Quick Dashboard Endpoints Test")
    print("=" * 50)
    
    endpoints = [
        ("/dashboard", "Main Dashboard"),
        ("/api/emotion-overview", "Emotion Overview"),
        ("/api/emotion-trends", "Emotion Trends"),
        ("/api/realtime-stats", "Realtime Stats")
    ]
    
    for endpoint, name in endpoints:
        print(f"\n📡 Testing {name}: {endpoint}")
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"   ✅ Success! Status: {response.status_code}")
                data = response.json()
                
                # Show sample data
                if endpoint == "/dashboard":
                    dashboard = data.get('dashboard', {})
                    print(f"   • Total messages: {dashboard.get('total_messages', 'N/A')}")
                elif endpoint == "/api/emotion-overview":
                    print(f"   • Emotions tracked: {len(data)} types")
                elif endpoint == "/api/emotion-trends":
                    trends = data.get('trends', {})
                    print(f"   • Time periods: {len(trends)}")
                elif endpoint == "/api/realtime-stats":
                    total = data.get('total', {})
                    print(f"   • Total stats: {len(total)} sentiments")
            else:
                print(f"   ❌ Failed! Status: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print(f"   ⚠️  Connection failed - Make sure Flask app is running on {BASE_URL}")
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    print("🧪 Dashboard Endpoints Comprehensive Test Suite")
    print("=" * 60)
    
    # Check if we should run quick test or full test
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        run_quick_test()
    else:
        # Run full unittest suite
        unittest.main(verbosity=2, argv=[''])
