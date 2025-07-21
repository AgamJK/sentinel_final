#!/usr/bin/env python3
"""
Utility functions to populate and use the empty MongoDB collections
"""

from database import get_database_manager
from datetime import datetime, timedelta
import json

class AnalyticsManager:
    def __init__(self):
        self.db = get_database_manager()
    
    def generate_daily_analytics(self, date=None):
        """Generate daily analytics and store in sentiment_analytics collection"""
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        # Get all messages for the day
        messages = self.db.get_all_messages()
        
        # Calculate analytics
        daily_stats = {
            "date": date,
            "timestamp": datetime.now().isoformat(),
            "total_messages": len(messages),
            "sentiment_breakdown": {},
            "source_breakdown": {},
            "hourly_distribution": {},
            "alerts_created": 0
        }
        
        # Count sentiments and sources
        for msg in messages:
            sentiment = msg.get('sentiment', msg.get('emotion', 'unknown'))
            source = msg.get('source', 'unknown')
            
            # Count sentiments
            daily_stats["sentiment_breakdown"][sentiment] = \
                daily_stats["sentiment_breakdown"].get(sentiment, 0) + 1
            
            # Count sources  
            daily_stats["source_breakdown"][source] = \
                daily_stats["source_breakdown"].get(source, 0) + 1
        
        # Count alerts
        alerts = self.db.get_active_alerts()
        daily_stats["alerts_created"] = len(alerts)
        
        # Store in analytics collection
        self.db.analytics.insert_one(daily_stats)
        print(f"✅ Daily analytics generated for {date}")
        return daily_stats
    
    def log_sentiment_processing(self, message_id, sentiment, confidence=0.8, processing_time=1.0):
        """Log sentiment processing history"""
        history_entry = {
            "message_id": message_id,
            "timestamp": datetime.now().isoformat(),
            "sentiment": sentiment,
            "confidence_score": confidence,
            "model_version": "gemini-1.5",
            "processing_time_ms": processing_time * 1000
        }
        
        self.db.history.insert_one(history_entry)
        print(f"📚 Sentiment history logged for message {message_id}")
    
    def initialize_settings(self):
        """Initialize default system settings"""
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
            },
            {
                "category": "analytics",
                "key": "enable_daily_reports",
                "value": True,
                "description": "Enable automatic daily analytics generation",
                "created_at": datetime.now().isoformat()
            }
        ]
        
        for setting in default_settings:
            # Check if setting already exists
            existing = self.db.settings.find_one({
                "category": setting["category"],
                "key": setting["key"]
            })
            
            if not existing:
                self.db.settings.insert_one(setting)
                print(f"⚙️ Setting created: {setting['category']}.{setting['key']}")
        
        print("✅ Settings initialization completed")
    
    def create_admin_user(self, email="admin@sentiment-sentinel.com"):
        """Create default admin user"""
        admin_user = {
            "email": email,
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
        
        # Check if user exists
        existing = self.db.users.find_one({"email": email})
        if not existing:
            self.db.users.insert_one(admin_user)
            print(f"👥 Admin user created: {email}")
        else:
            print(f"👥 Admin user already exists: {email}")
    
    def get_analytics_summary(self):
        """Get summary of all collections"""
        summary = {
            "messages": self.db.get_message_count(),
            "alerts": len(self.db.get_active_alerts()),
            "analytics_reports": self.db.analytics.count_documents({}),
            "sentiment_history": self.db.history.count_documents({}),
            "settings": self.db.settings.count_documents({}),
            "users": self.db.users.count_documents({})
        }
        
        return summary
    
    def close(self):
        """Close database connection"""
        self.db.close_connection()

def main():
    """Initialize all collections with sample data"""
    print("🚀 Initializing Empty Collections...")
    
    analytics = AnalyticsManager()
    
    try:
        # Initialize settings
        analytics.initialize_settings()
        
        # Create admin user
        analytics.create_admin_user()
        
        # Generate today's analytics
        daily_stats = analytics.generate_daily_analytics()
        
        # Log some sample sentiment history
        messages = analytics.db.get_all_messages(limit=3)
        for msg in messages:
            analytics.log_sentiment_processing(
                msg.get('id', 'unknown'),
                msg.get('sentiment', msg.get('emotion', 'neutral'))
            )
        
        # Show summary
        summary = analytics.get_analytics_summary()
        print("\n📊 Collections Summary:")
        print("="*40)
        for collection, count in summary.items():
            print(f"{collection}: {count} records")
        
        print("\n✅ All collections initialized successfully!")
        
    finally:
        analytics.close()

if __name__ == "__main__":
    main()
