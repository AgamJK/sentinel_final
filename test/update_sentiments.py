#!/usr/bin/env python3
"""
Script to update existing messages with 'unknown' sentiment using fallback keyword classification
This will fix the messages that failed due to Gemini API quota limits
"""

from database import DatabaseManager
from gemini_emotion_classifier import classify_emotion_by_keywords

def update_unknown_sentiments():
    """Update all messages with 'unknown' or missing sentiment"""
    print("🔄 Starting sentiment update for unknown messages...")
    
    # Connect to database
    db_manager = DatabaseManager()
    
    # Find messages with unknown or missing sentiment
    unknown_messages = list(db_manager.messages.find({
        "$or": [
            {"sentiment": "unknown"},
            {"sentiment": {"$exists": False}},
            {"emotion": {"$exists": False}}
        ]
    }))
    
    print(f"Found {len(unknown_messages)} messages to update")
    
    updated_count = 0
    
    for message in unknown_messages:
        text = message.get('text', '')
        message_id = message['_id']
        
        if text:
            # Classify using keyword-based fallback
            new_sentiment = classify_emotion_by_keywords(text)
            
            # Update the message
            db_manager.messages.update_one(
                {"_id": message_id},
                {"$set": {"sentiment": new_sentiment}}
            )
            
            print(f"✅ Updated message {message_id}: {new_sentiment}")
            print(f"   Text: {text[:50]}...")
            updated_count += 1
    
    print(f"\n🎉 Updated {updated_count} messages!")
    
    # Show updated stats
    current_stats = db_manager.get_sentiment_stats()
    print("\nUpdated emotion counts:")
    for emotion, count in current_stats.items():
        print(f"  • {emotion}: {count}")

if __name__ == "__main__":
    update_unknown_sentiments()
