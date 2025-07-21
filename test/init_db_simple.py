#!/usr/bin/env python3
"""
Simple database initialization script for Sentiment Sentinel AI
Creates collections and indexes without complex validation
"""

import os
from datetime import datetime
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def initialize_database():
    """Initialize database with all required collections"""
    try:
        # Connect to MongoDB
        mongodb_uri = os.getenv('MONGODB_URI')
        database_name = os.getenv('DATABASE_NAME', 'sentiment_sentinel')
        
        if not mongodb_uri:
            raise ValueError("MONGODB_URI not found in environment variables")
        
        client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=10000)
        client.admin.command('ping')
        db = client[database_name]
        
        print(f"✅ Connected to MongoDB database: {database_name}")
        print("🚀 Creating collections and indexes...")
        
        # Collection 1: Messages (main collection)
        print("\n📂 Creating messages collection...")
        messages = db.messages
        
        # Create indexes for messages
        print("   Creating indexes...")
        messages.create_index("id", unique=True)
        messages.create_index("timestamp")
        messages.create_index("source")
        messages.create_index("sender")
        messages.create_index("sentiment")
        messages.create_index("emotion")
        messages.create_index([("source", ASCENDING), ("timestamp", DESCENDING)])
        messages.create_index([("sentiment", ASCENDING), ("timestamp", DESCENDING)])
        messages.create_index([("text", "text")])  # Full-text search
        print("   ✅ Messages collection ready")
        
        # Collection 2: Sentiment Analytics
        print("\n📊 Creating sentiment_analytics collection...")
        analytics = db.sentiment_analytics
        analytics.create_index([("date", DESCENDING), ("source", ASCENDING)])
        analytics.create_index("created_at")
        print("   ✅ Sentiment analytics collection ready")
        
        # Collection 3: Alerts
        print("\n🚨 Creating alerts collection...")
        alerts = db.alerts
        alerts.create_index("message_id")
        alerts.create_index([("status", ASCENDING), ("severity", DESCENDING)])
        alerts.create_index("created_at")
        alerts.create_index("alert_type")
        print("   ✅ Alerts collection ready")
        
        # Collection 4: Users
        print("\n👤 Creating users collection...")
        users = db.users
        users.create_index("username", unique=True)
        users.create_index("email", unique=True)
        users.create_index("role")
        print("   ✅ Users collection ready")
        
        # Collection 5: Settings
        print("\n⚙️ Creating settings collection...")
        settings = db.settings
        settings.create_index("key", unique=True)
        settings.create_index("category")
        print("   ✅ Settings collection ready")
        
        # Collection 6: Sentiment History (for tracking changes over time)
        print("\n📈 Creating sentiment_history collection...")
        history = db.sentiment_history
        history.create_index([("date", DESCENDING)])
        history.create_index([("sentiment", ASCENDING), ("date", DESCENDING)])
        print("   ✅ Sentiment history collection ready")
        
        # Insert sample data
        print("\n📝 Inserting sample data...")
        
        # Sample messages
        sample_messages = [
            {
                "id": "init_sample_001",
                "timestamp": datetime.now().isoformat(),
                "source": "email",
                "sender": "angry_customer@test.com",
                "text": "This service is terrible! I'm extremely frustrated with the poor quality!",
                "sentiment": "angry",
                "priority": "high",
                "status": "new",
                "created_at": datetime.now().isoformat(),
                "tags": ["complaint", "quality"]
            },
            {
                "id": "init_sample_002",
                "timestamp": datetime.now().isoformat(),
                "source": "chat", 
                "sender": "happy_customer@test.com",
                "text": "Amazing service! Thank you so much for the excellent support!",
                "sentiment": "happy",
                "priority": "low",
                "status": "resolved",
                "created_at": datetime.now().isoformat(),
                "tags": ["praise", "support"]
            },
            {
                "id": "init_sample_003",
                "timestamp": datetime.now().isoformat(),
                "source": "ticket",
                "sender": "neutral_customer@test.com",
                "text": "I need help understanding how the billing system works.",
                "sentiment": "neutral",
                "priority": "medium",
                "status": "new",
                "created_at": datetime.now().isoformat(),
                "tags": ["question", "billing"]
            }
        ]
        
        # Insert sample messages (avoid duplicates)
        for msg in sample_messages:
            try:
                messages.insert_one(msg)
            except:
                pass  # Skip if already exists
        
        # Sample settings
        sample_settings = [
            {
                "key": "sentiment_alert_threshold",
                "value": 0.7,
                "category": "sentiment",
                "description": "Threshold for negative sentiment alerts",
                "updated_at": datetime.now().isoformat()
            },
            {
                "key": "alert_recipients",
                "value": ["admin@company.com"],
                "category": "alerts",
                "description": "Alert notification recipients",
                "updated_at": datetime.now().isoformat()
            },
            {
                "key": "negative_sentiments",
                "value": ["angry", "frustrated", "upset", "disappointed", "furious", "irritated"],
                "category": "sentiment",
                "description": "List of negative sentiment keywords",
                "updated_at": datetime.now().isoformat()
            }
        ]
        
        # Insert sample settings (avoid duplicates)
        for setting in sample_settings:
            try:
                settings.insert_one(setting)
            except:
                pass  # Skip if already exists
        
        # Show database status
        print("\n📊 Database Status:")
        print("-" * 40)
        collections = db.list_collection_names()
        for collection_name in sorted(collections):
            collection = db[collection_name]
            count = collection.count_documents({})
            indexes = len(list(collection.list_indexes()))
            print(f"  📂 {collection_name}: {count} documents, {indexes} indexes")
        
        print("\n" + "=" * 50)
        print("✅ Database initialization completed successfully!")
        print("💾 All collections created with proper indexes")
        print("📝 Sample data inserted for testing")
        print("🚀 Sentiment Sentinel AI database is ready!")
        print("=" * 50)
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        if 'client' in locals():
            client.close()
        return False

if __name__ == "__main__":
    success = initialize_database()
    exit(0 if success else 1)
