#!/usr/bin/env python3
"""
Mock test for dashboard endpoints - tests endpoint availability without database
This test mocks the database responses to test endpoint logic and structure
"""

import unittest
from unittest.mock import Mock, patch
import sys
import os
import json

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import Flask app
from app import app

class MockDashboardTest(unittest.TestCase):
    """Test dashboard endpoints with mocked database"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True
        
        # Mock database responses
        self.mock_db_manager = Mock()
        
        # Configure mock responses
        self.mock_db_manager.get_message_count.return_value = 150
        self.mock_db_manager.get_sentiment_stats.return_value = {
            'happy': 45,
            'angry': 25, 
            'confused': 15,
            'neutral': 65
        }
        self.mock_db_manager.get_sentiment_stats_comparison.return_value = {
            'happy': 40,
            'angry': 30,
            'confused': 10,
            'neutral': 60
        }
        self.mock_db_manager.get_all_messages.return_value = [
            {
                'id': 'msg1',
                'timestamp': '2025-07-20T10:00:00',
                'source': 'email',
                'sender': 'test@example.com',
                'text': 'Test message',
                'sentiment': 'happy'
            }
        ]
        self.mock_db_manager.get_negative_sentiment_messages.return_value = [
            {
                'id': 'msg2', 
                'timestamp': '2025-07-20T11:00:00',
                'source': 'chat',
                'sender': 'angry@example.com',
                'text': 'Angry message',
                'sentiment': 'angry'
            }
        ]
        self.mock_db_manager.get_hourly_emotion_trends.return_value = {
            '2025-07-20T10:00:00': {'happy': 5, 'angry': 2},
            '2025-07-20T11:00:00': {'happy': 3, 'angry': 4}
        }
        self.mock_db_manager.get_current_hour_stats.return_value = {
            'happy': 12,
            'angry': 3,
            'neutral': 8
        }

    @patch('app.db_manager')
    def test_dashboard_endpoint(self, mock_db):
        """Test /dashboard endpoint with mocked database"""
        mock_db = self.mock_db_manager
        
        response = self.app.get('/dashboard')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        
        # Test structure
        self.assertIn('dashboard', data)
        dashboard = data['dashboard']
        
        # Test required fields
        required_fields = ['total_messages', 'sentiment_distribution', 'recent_messages', 'negative_alerts']
        for field in required_fields:
            self.assertIn(field, dashboard)
        
        # Test data values
        self.assertEqual(dashboard['total_messages'], 150)
        self.assertIn('counts', dashboard['sentiment_distribution'])
        self.assertIn('percentages', dashboard['sentiment_distribution'])
        
        print("✅ Dashboard endpoint structure test PASSED")

    @patch('app.db_manager')
    def test_emotion_overview_endpoint(self, mock_db):
        """Test /api/emotion-overview endpoint with mocked database"""
        mock_db = self.mock_db_manager
        
        response = self.app.get('/api/emotion-overview')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        
        # Test that we get emotion data
        self.assertIsInstance(data, dict)
        
        # Test structure of emotion data
        for emotion, stats in data.items():
            if isinstance(stats, dict):
                self.assertIn('count', stats)
                self.assertIn('change_percent', stats)
                self.assertIsInstance(stats['count'], int)
                self.assertIsInstance(stats['change_percent'], (int, float))
        
        print("✅ Emotion overview endpoint structure test PASSED")

    @patch('app.db_manager')  
    def test_emotion_trends_endpoint(self, mock_db):
        """Test /api/emotion-trends endpoint with mocked database"""
        mock_db = self.mock_db_manager
        
        # Test default request
        response = self.app.get('/api/emotion-trends')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        
        # Test structure
        self.assertIn('trends', data)
        self.assertIn('time_range_hours', data)
        self.assertEqual(data['time_range_hours'], 6)  # Default
        
        # Test with parameter
        response2 = self.app.get('/api/emotion-trends?hours=12')
        self.assertEqual(response2.status_code, 200)
        
        data2 = json.loads(response2.data)
        self.assertEqual(data2['time_range_hours'], 12)
        
        print("✅ Emotion trends endpoint structure test PASSED")

    @patch('app.db_manager')
    def test_realtime_stats_endpoint(self, mock_db):
        """Test /api/realtime-stats endpoint with mocked database"""
        mock_db = self.mock_db_manager
        
        response = self.app.get('/api/realtime-stats')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        
        # Test structure  
        required_fields = ['current_hour', 'total', 'timestamp']
        for field in required_fields:
            self.assertIn(field, data)
        
        # Test data types
        self.assertIsInstance(data['current_hour'], dict)
        self.assertIsInstance(data['total'], dict) 
        self.assertIsInstance(data['timestamp'], str)
        
        print("✅ Realtime stats endpoint structure test PASSED")

    def test_endpoint_without_db(self):
        """Test endpoints when database is not available"""
        # Test with no db_manager (simulates database connection failure)
        with patch('app.db_manager', None):
            
            endpoints = ['/dashboard', '/api/emotion-overview', '/api/emotion-trends', '/api/realtime-stats']
            
            for endpoint in endpoints:
                response = self.app.get(endpoint)
                self.assertEqual(response.status_code, 500)
                
                data = json.loads(response.data)
                self.assertIn('error', data)
                self.assertIn('Database connection not available', data['error'])
        
        print("✅ Database unavailable error handling test PASSED")

def run_mock_tests():
    """Run the mock tests"""
    print("🧪 Running Mock Dashboard Endpoints Tests")
    print("=" * 50)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(MockDashboardTest)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=0, stream=open(os.devnull, 'w'))
    result = runner.run(suite)
    
    # Print summary
    tests_run = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    
    print(f"\n📊 Mock Test Results:")
    print(f"   Tests run: {tests_run}")
    print(f"   Failures: {failures}")  
    print(f"   Errors: {errors}")
    
    if failures == 0 and errors == 0:
        print("🎉 All mock tests PASSED! The endpoint logic is working correctly.")
        print("   Issue is with database connection, not endpoint code.")
    else:
        print("⚠️  Some mock tests failed - there may be issues with endpoint logic.")
        
        if result.failures:
            print("\nFailures:")
            for test, error in result.failures:
                print(f"   ❌ {test}: {error}")
        
        if result.errors:
            print("\nErrors:")
            for test, error in result.errors:
                print(f"   ❌ {test}: {error}")

if __name__ == "__main__":
    run_mock_tests()
