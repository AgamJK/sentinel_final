#!/usr/bin/env python3
"""
Database initialization script for Sentiment Sentinel AI
Creates all required collections with proper schemas, indexes, and sample data
"""

import os
from datetime import datetime, timedelta
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure, CollectionInvalid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DatabaseInitializer:
    def __init__(self):
        self.client = None
        self.db = None
        self.connect()
    
    def connect(self):
        """Connect to MongoDB"""
        try:
            mongodb_uri = os.getenv('MONGODB_URI')
            database_name = os.getenv('DATABASE_NAME', 'sentiment_sentinel')
            
            if not mongodb_uri:
                raise ValueError("MONGODB_URI not found in environment variables")
            
            self.client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=10000)
            self.client.admin.command('ping')
            self.db = self.client[database_name]
            
            print(f"✅ Connected to MongoDB database: {database_name}")
            
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            raise
    
    def create_messages_collection(self):
        """Create the main messages collection with schema validation"""
        collection_name = "messages"
        
        try:
            # Drop existing collection if it exists (optional - remove if you want to preserve data)
            # self.db.drop_collection(collection_name)
            
            # Create collection with schema validation
            validator = {
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["id", "timestamp", "source", "sender", "text"],
                    "properties": {
                        "id": {
                            "bsonType": "string",
                            "description": "Unique message identifier"
                        },
                        "timestamp": {
                            "bsonType": "string",
                            "description": "Message timestamp in ISO format"
                        },
                        "source": {
                            "bsonType": "string",
                            "enum": ["email", "chat", "ticket", "phone", "social"],
                            "description": "Message source channel"
                        },
                        "sender": {
                            "bsonType": "string",
                            "description": "Sender identifier (email, username, etc.)"
                        },
                        "text": {
                            "bsonType": "string",
                            "description": "Message content"
                        },
                        "sentiment": {
                            "bsonType": "string",
                            "description": "AI-detected sentiment/emotion"
                        },
                        "emotion": {
                            "bsonType": "string", 
                            "description": "Alternative emotion field for compatibility"
                        },
                        "confidence": {
                            "bsonType": "number",
                            "minimum": 0,
                            "maximum": 1,
                            "description": "Sentiment analysis confidence score"
                        },
                        "priority": {
                            "bsonType": "string",
                            "enum": ["low", "medium", "high", "critical"],
                            "description": "Message priority based on sentiment"
                        },
                        "status": {
                            "bsonType": "string",
                            "enum": ["new", "reviewed", "escalated", "resolved"],
                            "description": "Processing status"
                        },
                        "created_at": {
                            "bsonType": "string",
                            "description": "Record creation timestamp"
                        },
                        "updated_at": {
                            "bsonType": "string",
                            "description": "Record last update timestamp"
                        },
                        "tags": {
                            "bsonType": "array",
                            "items": {
                                "bsonType": "string"
                            },
                            "description": "Message tags for categorization"
                        }
                    }
                }
            }
            
            try:
                self.db.create_collection(collection_name, validator=validator)
                print(f"✅ Created collection: {collection_name}")
            except CollectionInvalid:
                print(f"ℹ️  Collection {collection_name} already exists")
            
            # Create indexes for better performance
            messages = self.db[collection_name]
            
            # Single field indexes
            messages.create_index("id", ASCENDING)
            messages.create_index("timestamp", DESCENDING)
            messages.create_index("source", ASCENDING)
            messages.create_index("sender", ASCENDING)
            messages.create_index("sentiment", ASCENDING)
            messages.create_index("emotion", ASCENDING)
            messages.create_index("priority", ASCENDING)
            messages.create_index("status", ASCENDING)
            messages.create_index("created_at", DESCENDING)
            
            # Compound indexes for common queries
            messages.create_index([("source", ASCENDING), ("timestamp", DESCENDING)])
            messages.create_index([("sentiment", ASCENDING), ("timestamp", DESCENDING)])
            messages.create_index([("status", ASCENDING), ("priority", DESCENDING)])
            messages.create_index([("sender", ASCENDING), ("timestamp", DESCENDING)])
            
            # Text index for full-text search
            messages.create_index([("text", "text"), ("sender", "text")])
            
            print(f"✅ Created indexes for {collection_name}")
            
        except Exception as e:
            print(f"❌ Error creating messages collection: {e}")
            raise
    
    def create_sentiment_analytics_collection(self):
        """Create collection for sentiment analytics and aggregated data"""
        collection_name = "sentiment_analytics"
        
        try:
            validator = {
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["date", "source", "sentiment_counts"],
                    "properties": {
                        "date": {
                            "bsonType": "string",
                            "description": "Analytics date (YYYY-MM-DD)"
                        },
                        "source": {
                            "bsonType": "string",
                            "enum": ["email", "chat", "ticket", "phone", "social", "all"],
                            "description": "Data source"
                        },
                        "sentiment_counts": {
                            "bsonType": "object",
                            "description": "Count of messages by sentiment"
                        },
                        "total_messages": {
                            "bsonType": "int",
                            "minimum": 0,
                            "description": "Total messages for the period"
                        },
                        "negative_percentage": {
                            "bsonType": "number",
                            "minimum": 0,
                            "maximum": 100,
                            "description": "Percentage of negative sentiment messages"
                        },
                        "created_at": {
                            "bsonType": "string",
                            "description": "Record creation timestamp"
                        }
                    }
                }
            }
            
            try:
                self.db.create_collection(collection_name, validator=validator)
                print(f"✅ Created collection: {collection_name}")
            except CollectionInvalid:
                print(f"ℹ️  Collection {collection_name} already exists")
            
            # Create indexes
            analytics = self.db[collection_name]
            analytics.create_index([("date", DESCENDING), ("source", ASCENDING)])
            analytics.create_index("created_at", DESCENDING)
            
            print(f"✅ Created indexes for {collection_name}")
            
        except Exception as e:
            print(f"❌ Error creating sentiment analytics collection: {e}")
            raise
    
    def create_alerts_collection(self):
        """Create collection for sentiment alerts and notifications"""
        collection_name = "alerts"
        
        try:
            validator = {
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["message_id", "alert_type", "severity", "created_at"],
                    "properties": {
                        "message_id": {
                            "bsonType": "string",
                            "description": "Reference to the original message"
                        },
                        "alert_type": {
                            "bsonType": "string",
                            "enum": ["negative_sentiment", "escalation", "volume_spike", "keyword_trigger"],
                            "description": "Type of alert"
                        },
                        "severity": {
                            "bsonType": "string",
                            "enum": ["low", "medium", "high", "critical"],
                            "description": "Alert severity level"
                        },
                        "sentiment": {
                            "bsonType": "string",
                            "description": "Message sentiment that triggered alert"
                        },
                        "description": {
                            "bsonType": "string",
                            "description": "Alert description"
                        },
                        "status": {
                            "bsonType": "string",
                            "enum": ["active", "acknowledged", "resolved", "dismissed"],
                            "description": "Alert status"
                        },
                        "created_at": {
                            "bsonType": "string",
                            "description": "Alert creation timestamp"
                        },
                        "acknowledged_at": {
                            "bsonType": "string",
                            "description": "Alert acknowledgment timestamp"
                        },
                        "resolved_at": {
                            "bsonType": "string",
                            "description": "Alert resolution timestamp"
                        },
                        "assigned_to": {
                            "bsonType": "string",
                            "description": "User assigned to handle the alert"
                        }
                    }
                }
            }
            
            try:
                self.db.create_collection(collection_name, validator=validator)
                print(f"✅ Created collection: {collection_name}")
            except CollectionInvalid:
                print(f"ℹ️  Collection {collection_name} already exists")
            
            # Create indexes
            alerts = self.db[collection_name]
            alerts.create_index("message_id", ASCENDING)
            alerts.create_index([("status", ASCENDING), ("severity", DESCENDING)])
            alerts.create_index("created_at", DESCENDING)
            alerts.create_index("alert_type", ASCENDING)
            
            print(f"✅ Created indexes for {collection_name}")
            
        except Exception as e:
            print(f"❌ Error creating alerts collection: {e}")
            raise
    
    def create_users_collection(self):
        """Create collection for system users and permissions"""
        collection_name = "users"
        
        try:
            validator = {
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["username", "email", "role", "created_at"],
                    "properties": {
                        "username": {
                            "bsonType": "string",
                            "description": "Unique username"
                        },
                        "email": {
                            "bsonType": "string",
                            "description": "User email address"
                        },
                        "role": {
                            "bsonType": "string",
                            "enum": ["admin", "manager", "agent", "viewer"],
                            "description": "User role for permissions"
                        },
                        "permissions": {
                            "bsonType": "array",
                            "items": {
                                "bsonType": "string"
                            },
                            "description": "Specific permissions for the user"
                        },
                        "active": {
                            "bsonType": "bool",
                            "description": "Whether the user account is active"
                        },
                        "created_at": {
                            "bsonType": "string",
                            "description": "Account creation timestamp"
                        },
                        "last_login": {
                            "bsonType": "string",
                            "description": "Last login timestamp"
                        }
                    }
                }
            }
            
            try:
                self.db.create_collection(collection_name, validator=validator)
                print(f"✅ Created collection: {collection_name}")
            except CollectionInvalid:
                print(f"ℹ️  Collection {collection_name} already exists")
            
            # Create indexes
            users = self.db[collection_name]
            users.create_index("username", ASCENDING, unique=True)
            users.create_index("email", ASCENDING, unique=True)
            users.create_index("role", ASCENDING)
            
            print(f"✅ Created indexes for {collection_name}")
            
        except Exception as e:
            print(f"❌ Error creating users collection: {e}")
            raise
    
    def create_settings_collection(self):
        """Create collection for system settings and configuration"""
        collection_name = "settings"
        
        try:
            validator = {
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": ["key", "value", "updated_at"],
                    "properties": {
                        "key": {
                            "bsonType": "string",
                            "description": "Setting key/name"
                        },
                        "value": {
                            "description": "Setting value (any type)"
                        },
                        "category": {
                            "bsonType": "string",
                            "enum": ["sentiment", "alerts", "notifications", "general"],
                            "description": "Setting category"
                        },
                        "description": {
                            "bsonType": "string",
                            "description": "Setting description"
                        },
                        "updated_at": {
                            "bsonType": "string",
                            "description": "Last update timestamp"
                        }
                    }
                }
            }
            
            try:
                self.db.create_collection(collection_name, validator=validator)
                print(f"✅ Created collection: {collection_name}")
            except CollectionInvalid:
                print(f"ℹ️  Collection {collection_name} already exists")
            
            # Create indexes
            settings = self.db[collection_name]
            settings.create_index("key", ASCENDING, unique=True)
            settings.create_index("category", ASCENDING)
            
            print(f"✅ Created indexes for {collection_name}")
            
        except Exception as e:
            print(f"❌ Error creating settings collection: {e}")
            raise
    
    def insert_sample_data(self):
        """Insert sample data for testing"""
        print("\n📝 Inserting sample data...")
        
        # Sample messages
        sample_messages = [
            {
                "id": "sample_001",
                "timestamp": datetime.now().isoformat(),
                "source": "email",
                "sender": "customer1@example.com",
                "text": "I'm extremely disappointed with the delayed delivery. This is unacceptable!",
                "sentiment": "angry",
                "priority": "high",
                "status": "new",
                "created_at": datetime.now().isoformat(),
                "tags": ["delivery", "complaint"]
            },
            {
                "id": "sample_002", 
                "timestamp": datetime.now().isoformat(),
                "source": "chat",
                "sender": "customer2@example.com",
                "text": "Thank you so much for the quick resolution! Your support team is amazing!",
                "sentiment": "happy",
                "priority": "low",
                "status": "resolved",
                "created_at": datetime.now().isoformat(),
                "tags": ["praise", "support"]
            },
            {
                "id": "sample_003",
                "timestamp": datetime.now().isoformat(),
                "source": "ticket",
                "sender": "customer3@example.com",
                "text": "I'm confused about the billing process. Could you please explain how it works?",
                "sentiment": "confused",
                "priority": "medium",
                "status": "new",
                "created_at": datetime.now().isoformat(),
                "tags": ["billing", "question"]
            }
        ]
        
        try:
            self.db.messages.insert_many(sample_messages)
            print("✅ Inserted sample messages")
        except Exception as e:
            print(f"ℹ️  Sample messages might already exist: {e}")
        
        # Sample settings
        sample_settings = [
            {
                "key": "negative_sentiment_threshold",
                "value": 0.7,
                "category": "sentiment",
                "description": "Threshold for negative sentiment alerts",
                "updated_at": datetime.now().isoformat()
            },
            {
                "key": "alert_email_recipients",
                "value": ["admin@company.com", "manager@company.com"],
                "category": "alerts",
                "description": "Email recipients for alerts",
                "updated_at": datetime.now().isoformat()
            }
        ]
        
        try:
            self.db.settings.insert_many(sample_settings)
            print("✅ Inserted sample settings")
        except Exception as e:
            print(f"ℹ️  Sample settings might already exist: {e}")
    
    def initialize_all_collections(self):
        """Initialize all collections and data"""
        print("🚀 Initializing Sentiment Sentinel AI Database...")
        print("=" * 50)
        
        try:
            # Create all collections
            self.create_messages_collection()
            print()
            
            self.create_sentiment_analytics_collection() 
            print()
            
            self.create_alerts_collection()
            print()
            
            self.create_users_collection()
            print()
            
            self.create_settings_collection()
            print()
            
            # Insert sample data
            self.insert_sample_data()
            print()
            
            # Show collection info
            self.show_database_info()
            
            print("=" * 50)
            print("✅ Database initialization completed successfully!")
            
        except Exception as e:
            print(f"❌ Database initialization failed: {e}")
            raise
    
    def show_database_info(self):
        """Display information about created collections"""
        print("📊 Database Information:")
        print("-" * 30)
        
        collections = self.db.list_collection_names()
        for collection_name in sorted(collections):
            collection = self.db[collection_name]
            count = collection.count_documents({})
            indexes = len(list(collection.list_indexes()))
            print(f"  📂 {collection_name}: {count} documents, {indexes} indexes")
    
    def close_connection(self):
        """Close database connection"""
        if self.client:
            self.client.close()
            print("✅ Database connection closed")

def main():
    """Main function to run database initialization"""
    try:
        initializer = DatabaseInitializer()
        initializer.initialize_all_collections()
        
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return 1
    finally:
        if 'initializer' in locals():
            initializer.close_connection()
    
    return 0

if __name__ == "__main__":
    exit(main())
