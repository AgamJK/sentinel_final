    # User-Specific Email Monitoring - Updated Features

This update adds support for user-specific email monitoring and improves real-time emotion trend tracking.

## New Features

### 1. User-Specific Email Configuration
- Users can now configure their own email accounts
- Multiple users can have separate email monitoring
- Each user's data is stored separately with proper user identification

### 2. Improved Real-Time Emotion Trends
- Fixed timestamp handling for better real-time tracking
- Added user-specific trend filtering
- Improved database indexing for better performance

### 3. Enhanced API Endpoints

## API Usage Examples

### 1. Configure Email for a Specific User

**POST** `/api/email-config`
```json
{
  "user_id": "user123",
  "email": "user@example.com",
  "appPassword": "your-gmail-app-password",
  "telegramUserId": "123456789"
}
```

### 2. Configure Email Globally (Backward Compatible)

**POST** `/api/email-config`
```json
{
  "email": "admin@example.com",
  "appPassword": "your-gmail-app-password",
  "telegramUserId": "987654321"
}
```

### 3. Get Email Configuration

**GET** `/api/email-config?user_id=user123` - Get user-specific config
**GET** `/api/email-config` - Get global config

### 4. Test Email Connection

**GET** `/api/test-email-config?user_id=user123` - Test user-specific config
**GET** `/api/test-email-config` - Test global config

### 5. Start Monitoring

**POST** `/api/start-monitoring`
```json
{
  "user_id": "user123"  // Optional: monitor specific user only
}
```

**POST** `/api/start-monitoring` (empty body) - Monitor all configured users

### 6. Fetch Emails Immediately

**POST** `/api/fetch-emails-now`
```json
{
  "user_id": "user123"  // Use stored config for user
}
```

OR

```json
{
  "email": "temp@example.com",
  "password": "temp-app-password"  // Use temporary credentials
}
```

### 7. Get Emotion Trends with User Filter

**GET** `/api/emotion-trends?user_id=user123&hours=24` - User-specific trends
**GET** `/api/emotion-trends?hours=6` - Global trends

### 8. List All Email Configurations

**GET** `/api/list-email-configs`

Returns:
```json
{
  "configs": [
    {
      "id": "config_id",
      "email": "user1@example.com",
      "user_id": "user123",
      "created_at": "2025-01-01T12:00:00",
      "active": true
    }
  ],
  "count": 1
}
```

## Database Schema Updates

### Email Configurations Collection (`email_configs`)
```json
{
  "_id": "ObjectId",
  "email": "user@example.com",
  "app_password": "encrypted_password",
  "telegram_user_id": "123456789",
  "user_id": "user123",  // New field for user-specific configs
  "active": true,
  "created_at": "ISO_timestamp",
  "updated_at": "ISO_timestamp"
}
```

### Messages Collection Updates
```json
{
  "_id": "ObjectId",
  "timestamp": "original_timestamp_string",
  "timestamp_iso": "ISO_format_timestamp",  // New: standardized timestamp
  "timestamp_parsed": "DateTime_object",    // New: for efficient querying
  "user_id": "user123",                     // New: associate with user
  "email_account": "user@example.com",      // New: track source email
  "source": "email",
  "sender": "sender@domain.com",
  "text": "email_content",
  "emotion": "happy",
  "sentiment": "happy",
  "priority": "medium"
}
```

## Usage Instructions

### 1. For Multiple Users Setup

```python
# Configure User 1
import requests

user1_config = {
    "user_id": "user1",
    "email": "user1@company.com",
    "appPassword": "user1-app-password",
    "telegramUserId": "111111111"
}

response = requests.post("http://localhost:5000/api/email-config", json=user1_config)

# Configure User 2
user2_config = {
    "user_id": "user2",
    "email": "user2@company.com",
    "appPassword": "user2-app-password",
    "telegramUserId": "222222222"
}

response = requests.post("http://localhost:5000/api/email-config", json=user2_config)

# Start monitoring all users
response = requests.post("http://localhost:5000/api/start-monitoring")
```

### 2. Monitor Specific User Only

```python
# Monitor only user1's emails
response = requests.post("http://localhost:5000/api/start-monitoring", 
                        json={"user_id": "user1"})
```

### 3. Get User-Specific Analytics

```python
# Get emotion trends for specific user
response = requests.get("http://localhost:5000/api/emotion-trends", 
                       params={"user_id": "user1", "hours": 24})
```

### 4. One-time Email Fetch with Credentials

```python
# Fetch emails without saving configuration
temp_fetch = {
    "email": "temp@example.com",
    "password": "temp-app-password"
}

response = requests.post("http://localhost:5000/api/fetch-emails-now", json=temp_fetch)
```

## Function Updates

### `ingest_email.py` Functions

- `get_email_config(user_id=None)` - Get config for user or globally
- `test_email_connection(user_id=None)` - Test connection for user or globally
- `fetch_and_forward_emails(specific_email=None, specific_password=None, user_id=None)` - Enhanced with user support
- `fetch_all_user_emails()` - New: Fetch from all configured users
- `continuous_email_monitoring(user_id=None)` - Enhanced with user filtering

### `database.py` Functions

- `save_email_config(config_data, user_id=None)` - Enhanced with user support
- `get_email_config(user_id=None)` - Enhanced with user support
- `get_all_email_configs()` - New: Get all active configurations
- `get_hourly_emotion_trends(hours=6, user_id=None)` - Enhanced with user filtering
- `insert_message(message_data)` - Enhanced with better timestamp handling

## Testing

Run the test script to verify functionality:

```bash
python test_user_email.py
```

Make sure to update the test credentials in the script before running.

## Migration from Single User Setup

Existing single-user setups will continue to work without changes. The system maintains backward compatibility by treating configurations without a `user_id` as global configurations.

To migrate existing setup to user-specific:

1. Get current global config: `GET /api/email-config`
2. Save it with a user_id: `POST /api/email-config` with `user_id` field
3. The old global config will remain for backward compatibility

## Real-Time Emotion Trends Fix

The following improvements were made to fix real-time emotion trend issues:

1. **Better Timestamp Handling**: Added `timestamp_iso` and `timestamp_parsed` fields for efficient querying
2. **Improved Database Queries**: Use datetime objects for range queries instead of string parsing
3. **User Filtering**: Support for user-specific trend analysis
4. **Fallback Mechanisms**: Graceful handling of timestamp parsing errors

## Security Notes

- App passwords are stored in plain text in the database (consider encryption for production)
- API endpoints don't require authentication (add authentication for production)
- Telegram user IDs are stored for notification purposes

## Performance Optimizations

- Database indexes on timestamp fields for faster queries
- Parallel processing of multiple user email accounts
- Efficient MongoDB aggregation queries for trends
- Proper error handling and fallback mechanisms
