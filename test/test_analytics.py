#!/usr/bin/env python3
"""
Test script for sentiment analytics and history functions
Generates sample analytics data for your collections
"""

from database import get_database_manager
from datetime import datetime, timedelta
import json

def test_analytics_functions():
    """Test all the new analytics functions"""
    print("🧪 Testing Sentiment Analytics & History Functions")
    print("="*60)
    
    db = get_database_manager()
    
    try:
        # Test 1: Generate daily analytics for today
        print("\n📊 Generating Daily Analytics...")
        daily_id = db.generate_daily_analytics()
        if daily_id:
            print(f"✅ Daily analytics created with ID: {daily_id}")
        
        # Test 2: Generate weekly analytics
        print("\n📅 Generating Weekly Analytics...")
        weekly_id = db.generate_weekly_analytics()
        if weekly_id:
            print(f"✅ Weekly analytics created with ID: {weekly_id}")
        
        # Test 3: Check what was saved
        print("\n📈 Checking Saved Analytics...")
        daily_reports = db.get_analytics_by_period("daily", limit=1)
        if daily_reports:
            print("Latest Daily Report:")
            daily_report = daily_reports[0]
            del daily_report['_id']  # Remove for cleaner display
            print(json.dumps(daily_report, indent=2))
        
        weekly_reports = db.get_analytics_by_period("weekly", limit=1)
        if weekly_reports:
            print("\nLatest Weekly Report:")
            weekly_report = weekly_reports[0]
            del weekly_report['_id']
            print(json.dumps(weekly_report, indent=2))
        
        # Test 4: Check sentiment history
        print(f"\n📚 Checking Sentiment History...")
        history = db.get_sentiment_history(limit=3)
        print(f"Total history records: {len(history)}")
        if history:
            for i, record in enumerate(history[:3], 1):
                print(f"{i}. Message: {record.get('original_text', 'N/A')[:50]}...")
                print(f"   Sentiment: {record.get('sentiment')} (confidence: {record.get('confidence_score')})")
                print(f"   Source: {record.get('source')} | Time: {record.get('processing_time_ms')}ms")
                print()
        
        print("✅ All analytics functions tested successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
    finally:
        db.close_connection()

def populate_sample_settings():
    """Add some sample settings to the settings collection"""
    print("\n⚙️ Populating Settings Collection...")
    
    db = get_database_manager()
    
    sample_settings = [
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
        },
        {
            "category": "analytics",
            "key": "auto_generate_weekly",
            "value": True,
            "description": "Automatically generate weekly analytics reports",
            "created_at": datetime.now().isoformat()
        }
    ]
    
    try:
        for setting in sample_settings:
            # Check if setting already exists
            existing = db.settings.find_one({
                "category": setting["category"],
                "key": setting["key"]
            })
            
            if not existing:
                db.settings.insert_one(setting)
                print(f"✅ Added setting: {setting['category']}.{setting['key']}")
            else:
                print(f"⚠️ Setting already exists: {setting['category']}.{setting['key']}")
        
        print(f"✅ Settings collection populated!")
        
    except Exception as e:
        print(f"❌ Error populating settings: {e}")
    finally:
        db.close_connection()

def show_collection_status():
    """Show the status of all collections"""
    print("\n📊 Collection Status Summary")
    print("="*40)
    
    db = get_database_manager()
    
    try:
        collections_status = {
            "messages": db.messages.count_documents({}),
            "alerts": db.alerts.count_documents({}),
            "sentiment_analytics": db.analytics.count_documents({}),
            "sentiment_history": db.history.count_documents({}),
            "settings": db.settings.count_documents({}),
            "users": db.users.count_documents({})
        }
        
        for collection, count in collections_status.items():
            status = "✅" if count > 0 else "⭕"
            print(f"{status} {collection}: {count} documents")
        
        print(f"\n🎯 Total documents across all collections: {sum(collections_status.values())}")
        
    except Exception as e:
        print(f"❌ Error checking collection status: {e}")
    finally:
        db.close_connection()

if __name__ == "__main__":
    print("🎯 SENTIMENT ANALYTICS & HISTORY TESTING")
    print(f"📅 Date: {datetime.now()}")
    
    # Test analytics functions
    test_analytics_functions()
    
    # Populate settings
    populate_sample_settings()
    
    # Show final status
    show_collection_status()
    
    print("\n🎉 Testing completed!")
    print("\nYour empty collections now have data and functions to:")
    print("  📈 Generate daily/weekly analytics automatically")
    print("  📚 Track sentiment analysis history for each message")
    print("  ⚙️ Store system configuration settings")
    print("  🚨 Monitor and analyze alert patterns")
