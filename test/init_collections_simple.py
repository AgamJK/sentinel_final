#!/usr/bin/env python3
"""
Simple script to initialize all database collections
"""

import os
import sys
from datetime import datetime, timedelta
import json
from dotenv import load_dotenv

# Add current directory to Python path
sys.path.append('.')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables from the current directory
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))

from database import get_database_manager

def initialize_all_collections():
    """Initialize all required collections with sample data"""
    print("🚀 Initializing Database Collections...")
    print("=" * 50)
    
    try:
        # Get database manager
        db_manager = get_database_manager()
        print("✅ Connected to database successfully!")
        
        # Check existing collections
        existing_collections = db_manager.db.list_collection_names()
        print(f"📁 Existing collections: {existing_collections}")
        
        # Initialize settings collection
        print("\n⚙️ Initializing Settings...")
        default_settings = [
            {
                "category": "email_processing",
                "key": "check_interval",
                "value": 10,
                "description": "Email check interval in seconds",
                "created_at": datetime.now().isoformat()
            },
            {
                "category": "alerts",
                "key": "negative_threshold",
                "value": 0.7,
                "description": "Confidence threshold for negative sentiment alerts",
                "created_at": datetime.now().isoformat()
            },
            {
                "category": "dashboard",
                "key": "max_messages_display",
                "value": 50,
                "description": "Maximum messages to show on dashboard",
                "created_at": datetime.now().isoformat()
            }
        ]
        
        for setting in default_settings:
            existing = db_manager.settings.find_one({
                "category": setting["category"],
                "key": setting["key"]
            })
            if not existing:
                db_manager.settings.insert_one(setting)
                print(f"  ✅ Created setting: {setting['category']}.{setting['key']}")
        
        # Initialize users collection
        print("\n👥 Initializing Users...")
        admin_user = {
            "email": "admin@sentiment-sentinel.com",
            "role": "admin",
            "permissions": [
                "view_dashboard",
                "manage_alerts", 
                "export_data",
                "manage_users",
                "system_settings"
            ],
            "created_at": datetime.now().isoformat(),
            "last_login": None,
            "status": "active"
        }
        
        existing_user = db_manager.users.find_one({"email": admin_user["email"]})
        if not existing_user:
            db_manager.users.insert_one(admin_user)
            print(f"  ✅ Created admin user: {admin_user['email']}")
        else:
            print(f"  ℹ️ Admin user already exists: {admin_user['email']}")
        
        # Initialize sample alerts
        print("\n🚨 Initializing Alerts...")
        sample_alerts = [
            {
                "message_id": "sample_001",
                "alert_type": "negative_sentiment",
                "sentiment": "angry",
                "confidence": 0.95,
                "created_at": datetime.now().isoformat(),
                "status": "active",
                "priority": "high",
                "description": "High confidence negative sentiment detected"
            },
            {
                "message_id": "sample_002", 
                "alert_type": "negative_sentiment",
                "sentiment": "frustrated",
                "confidence": 0.87,
                "created_at": (datetime.now() - timedelta(hours=2)).isoformat(),
                "status": "resolved",
                "priority": "medium",
                "description": "Customer frustration detected"
            }
        ]
        
        for alert in sample_alerts:
            existing_alert = db_manager.alerts.find_one({"message_id": alert["message_id"]})
            if not existing_alert:
                db_manager.alerts.insert_one(alert)
                print(f"  ✅ Created alert: {alert['alert_type']} for {alert['message_id']}")
        
        # Initialize analytics collection
        print("\n📊 Initializing Analytics...")
        today_analytics = {
            "date": datetime.now().strftime('%Y-%m-%d'),
            "timestamp": datetime.now().isoformat(),
            "total_messages": 0,
            "sentiment_breakdown": {
                "happy": 0,
                "neutral": 0,
                "angry": 0,
                "confused": 0
            },
            "source_breakdown": {
                "email": 0,
                "chat": 0,
                "ticket": 0
            },
            "alerts_created": 2
        }
        
        existing_analytics = db_manager.analytics.find_one({
            "date": today_analytics["date"]
        })
        if not existing_analytics:
            db_manager.analytics.insert_one(today_analytics)
            print(f"  ✅ Created analytics for {today_analytics['date']}")
        
        # Initialize sentiment history
        print("\n📚 Initializing Sentiment History...")
        sample_history = [
            {
                "message_id": "sample_001",
                "timestamp": datetime.now().isoformat(),
                "sentiment": "angry",
                "confidence_score": 0.95,
                "model_version": "gemini-1.5",
                "processing_time_ms": 1200
            },
            {
                "message_id": "sample_002",
                "timestamp": (datetime.now() - timedelta(hours=1)).isoformat(),
                "sentiment": "frustrated",
                "confidence_score": 0.87,
                "model_version": "gemini-1.5",
                "processing_time_ms": 950
            }
        ]
        
        for history in sample_history:
            existing_history = db_manager.history.find_one({"message_id": history["message_id"]})
            if not existing_history:
                db_manager.history.insert_one(history)
                print(f"  ✅ Created history for {history['message_id']}")
        
        # Get collection counts
        print("\n📈 Collection Summary:")
        print("=" * 30)
        collections = {
            "messages": db_manager.messages.count_documents({}),
            "alerts": db_manager.alerts.count_documents({}),
            "analytics": db_manager.analytics.count_documents({}),
            "users": db_manager.users.count_documents({}),
            "settings": db_manager.settings.count_documents({}),
            "history": db_manager.history.count_documents({})
        }
        
        for collection, count in collections.items():
            print(f"{collection}: {count} documents")
        
        print("\n✅ All collections initialized successfully!")
        return collections
        
    except Exception as e:
        print(f"❌ Error initializing collections: {e}")
        return None
    
    finally:
        if 'db_manager' in locals():
            db_manager.close_connection()

if __name__ == "__main__":
    initialize_all_collections()
