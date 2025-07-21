#!/usr/bin/env python3
"""
Test script to verify MongoDB connection and basic operations
"""

import sys
import json
import os
from datetime import datetime

# Add parent directory to path to import database module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_database_manager

def test_database_connection():
    """Test database connection and basic operations"""
    print("🧪 Testing database connection...")
    
    try:
        # Initialize database manager
        db_manager = get_database_manager()
        print("✅ Database connection successful!")
        
        # Test inserting a sample message
        test_message = {
            "id": f"test_{datetime.now().timestamp()}",
            "timestamp": datetime.now().isoformat(),
            "source": "email",
            "sender": "test@example.com",
            "text": "This is a test message to verify database connectivity."
        }
        
        print("\n📝 Testing message insertion...")
        message_id = db_manager.insert_message(test_message)
        print(f"✅ Message inserted with ID: {message_id}")
        
        # Test retrieving messages
        print("\n📋 Testing message retrieval...")
        messages = db_manager.get_all_messages(limit=5)
        print(f"✅ Retrieved {len(messages)} messages")
        
        # Print the latest message
        if messages:
            latest_message = messages[0]
            print(f"📄 Latest message: {latest_message['text'][:50]}...")
        
        # Test message count
        total_count = db_manager.get_message_count()
        print(f"📊 Total messages in database: {total_count}")
        
        # Test filtering by source
        print("\n🔍 Testing filtering by source...")
        email_messages = db_manager.get_messages_by_source("email", limit=3)
        print(f"✅ Found {len(email_messages)} email messages")
        
        print("\n✅ All database tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False
    finally:
        if 'db_manager' in locals():
            db_manager.close_connection()

if __name__ == "__main__":
    success = test_database_connection()
    sys.exit(0 if success else 1)
