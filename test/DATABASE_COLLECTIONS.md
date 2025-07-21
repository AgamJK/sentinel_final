# Sentiment Sentinel AI - Database Collections Overview

This document provides a comprehensive overview of all database collections created for the Sentiment Sentinel AI system.

## 🗄️ Database Structure

**Database Name:** `sentiment_sentinel`  
**MongoDB Connection:** MongoDB Atlas cluster  
**Total Collections:** 6 core collections  

---

## 📋 Collection Details

### 1. **`messages`** - Main Messages Collection
**Purpose:** Stores all customer support messages with sentiment analysis results

**Schema:**
```json
{
  "_id": "ObjectId",
  "id": "unique_message_identifier",
  "timestamp": "ISO_datetime_string",
  "source": "email|chat|ticket|phone|social",
  "sender": "customer_email_or_identifier",
  "text": "message_content_text",
  "sentiment": "detected_emotion (e.g., angry, happy, confused)",
  "emotion": "alternative_emotion_field",
  "priority": "low|medium|high|critical",
  "status": "new|reviewed|escalated|resolved",
  "created_at": "record_creation_timestamp",
  "updated_at": "last_update_timestamp",
  "tags": ["array", "of", "tags"],
  "confidence": 0.85
}
```

**Key Features:**
- ✅ Automatic sentiment analysis on message insertion
- ✅ Priority assignment based on sentiment
- ✅ Full-text search index on message content
- ✅ Multiple filtering options (source, sender, sentiment)
- ✅ Automatic alert generation for negative sentiments

**Indexes:**
- `id` (unique)
- `timestamp`
- `source`
- `sender`
- `sentiment`
- `emotion`
- `source + timestamp` (compound)
- `sentiment + timestamp` (compound)
- `text` (full-text search)

---

### 2. **`alerts`** - Alert Management Collection
**Purpose:** Stores alerts generated for negative sentiments and other triggers

**Schema:**
```json
{
  "_id": "ObjectId",
  "message_id": "reference_to_original_message",
  "alert_type": "negative_sentiment|escalation|volume_spike|keyword_trigger",
  "severity": "low|medium|high|critical",
  "sentiment": "emotion_that_triggered_alert",
  "description": "human_readable_alert_description",
  "status": "active|acknowledged|resolved|dismissed",
  "created_at": "alert_creation_timestamp",
  "acknowledged_at": "alert_acknowledgment_timestamp",
  "resolved_at": "alert_resolution_timestamp",
  "assigned_to": "user_assigned_to_handle_alert"
}
```

**Key Features:**
- 🚨 Automatic creation for negative sentiment messages
- 📊 Severity levels based on sentiment intensity
- 👤 Assignment and tracking capabilities
- 📈 Status workflow management

**Indexes:**
- `message_id`
- `status + severity` (compound)
- `created_at`
- `alert_type`

---

### 3. **`sentiment_analytics`** - Analytics Collection
**Purpose:** Stores aggregated sentiment data for reporting and analytics

**Schema:**
```json
{
  "_id": "ObjectId",
  "date": "YYYY-MM-DD",
  "source": "email|chat|ticket|phone|social|all",
  "sentiment_counts": {
    "angry": 15,
    "happy": 45,
    "neutral": 30,
    "confused": 10
  },
  "total_messages": 100,
  "negative_percentage": 25.0,
  "created_at": "record_creation_timestamp"
}
```

**Key Features:**
- 📊 Daily sentiment distribution tracking
- 📈 Source-specific analytics
- 🎯 Negative sentiment percentage monitoring
- 📅 Historical trend analysis

**Indexes:**
- `date + source` (compound)
- `created_at`

---

### 4. **`users`** - User Management Collection
**Purpose:** Stores system users and their permissions

**Schema:**
```json
{
  "_id": "ObjectId",
  "username": "unique_username",
  "email": "user_email_address",
  "role": "admin|manager|agent|viewer",
  "permissions": ["read_messages", "create_alerts", "manage_users"],
  "active": true,
  "created_at": "account_creation_timestamp",
  "last_login": "last_login_timestamp"
}
```

**Key Features:**
- 👤 Role-based access control
- 🔐 Permission management system
- 📊 User activity tracking
- ✅ Account status management

**Indexes:**
- `username` (unique)
- `email` (unique)
- `role`

---

### 5. **`settings`** - System Configuration Collection
**Purpose:** Stores system settings and configuration parameters

**Schema:**
```json
{
  "_id": "ObjectId",
  "key": "setting_key_name",
  "value": "setting_value (any type)",
  "category": "sentiment|alerts|notifications|general",
  "description": "setting_description",
  "updated_at": "last_update_timestamp"
}
```

**Current Settings:**
```json
{
  "sentiment_alert_threshold": 0.7,
  "alert_recipients": ["admin@company.com"],
  "negative_sentiments": ["angry", "frustrated", "upset", "disappointed", "furious", "irritated"]
}
```

**Key Features:**
- ⚙️ Centralized configuration management
- 🔄 Dynamic setting updates
- 📂 Categorized settings
- 📝 Setting descriptions and documentation

**Indexes:**
- `key` (unique)
- `category`

---

### 6. **`sentiment_history`** - Historical Tracking Collection
**Purpose:** Tracks sentiment trends and changes over time

**Schema:**
```json
{
  "_id": "ObjectId",
  "date": "YYYY-MM-DD",
  "hour": 14,
  "sentiment_snapshot": {
    "angry": 5,
    "happy": 20,
    "neutral": 15
  },
  "total_messages": 40,
  "created_at": "snapshot_creation_timestamp"
}
```

**Key Features:**
- 📈 Hourly sentiment tracking
- 🕐 Time-series data for trends
- 📊 Historical comparison capabilities
- 🎯 Pattern recognition data

**Indexes:**
- `date` (descending)
- `sentiment + date` (compound)

---

## 🔄 Data Flow

### Message Processing Flow:
1. **Message Received** → `POST /message`
2. **Sentiment Analysis** → Gemini AI classification
3. **Database Storage** → `messages` collection
4. **Priority Assignment** → Based on sentiment
5. **Alert Generation** → `alerts` collection (if negative)
6. **Analytics Update** → `sentiment_analytics` collection

### Alert Processing Flow:
1. **Negative Sentiment Detected** → Automatic trigger
2. **Alert Created** → `alerts` collection
3. **Notification Sent** → Based on `settings`
4. **Status Tracking** → Until resolution

---

## 📊 Current Database Status

```
📂 alerts: 3 documents, 5 indexes
📂 messages: 11 documents, 10 indexes  
📂 sentiment_analytics: 0 documents, 3 indexes
📂 sentiment_history: 0 documents, 3 indexes
📂 settings: 3 documents, 3 indexes
📂 users: 0 documents, 4 indexes
```

---

## 🔍 Query Examples

### Get Messages by Sentiment:
```javascript
db.messages.find({"sentiment": "angry"})
```

### Get Active Alerts:
```javascript
db.alerts.find({"status": "active"})
```

### Get Daily Analytics:
```javascript
db.sentiment_analytics.find({"date": "2025-07-20"})
```

### Get System Settings:
```javascript
db.settings.find({"category": "sentiment"})
```

---

## 🚀 API Endpoints Supporting Collections

### Messages Collection:
- `POST /message` - Store new message with sentiment
- `GET /messages` - Retrieve messages with filters
- `GET /sentiment/{type}` - Filter by sentiment type

### Alerts Collection:
- `GET /alerts` - Get negative sentiment alerts
- `GET /dashboard` - Dashboard with alert overview

### Analytics Collection:
- `GET /stats` - Sentiment statistics
- `GET /dashboard` - Comprehensive analytics

### Settings Collection:
- System configuration (internal use)

---

## 💾 Backup and Maintenance

### Recommended Practices:
- 🔄 Daily automated backups
- 📊 Weekly analytics aggregation
- 🧹 Monthly alert cleanup (resolved alerts)
- 📈 Quarterly data archival

### Performance Optimization:
- ✅ All collections have appropriate indexes
- 📊 Compound indexes for common query patterns
- 🔍 Full-text search capability on messages
- 🎯 Optimized aggregation pipelines

---

## 🔒 Security Considerations

### Data Protection:
- 🔐 MongoDB Atlas security enabled
- 🌐 Network access restrictions
- 👤 User authentication required
- 🔑 Role-based permissions

### Sensitive Data:
- ❌ No passwords stored in plain text
- 🔒 Customer PII handled appropriately  
- 📝 Audit trail for data changes
- 🛡️ Data encryption in transit and at rest

---

## ✅ Collection Creation Status

All collections have been successfully created and are ready for use:

- ✅ **messages** - Primary data storage
- ✅ **alerts** - Automated alert system  
- ✅ **sentiment_analytics** - Reporting and analytics
- ✅ **users** - User management (ready for implementation)
- ✅ **settings** - System configuration
- ✅ **sentiment_history** - Trend tracking (ready for implementation)

The Sentiment Sentinel AI database is now fully operational with comprehensive sentiment analysis, alerting, and analytics capabilities! 🚀
