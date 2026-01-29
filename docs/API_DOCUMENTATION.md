# Terraguard API Documentation

**Base URL (Development):** `http://localhost:8000`  
**Base URL (Production):** `https://terraguard-api.onrender.com`  
**Interactive Docs:** `https://terraguard-api.onrender.com/docs`

## Overview

Terraguard API provides AI-powered climate risk detection, real-time alerts, and agricultural guidance for African regions, with a focus on Kenya. The API integrates with NASA POWER climate data, Google Maps, and DeepSeek AI to deliver actionable insights.

## Authentication

All endpoints are currently public for the MVP phase. Future versions will implement JWT-based authentication for admin features and user-specific data management.

---

## Table of Contents

1. [Health & Status](#health--status)
2. [Climate Risk Detection](#climate-risk-detection)
3. [Alerts](#alerts)
4. [Subscriptions](#subscriptions)
5. [AI Assistant](#ai-assistant)
6. [Webhooks](#webhooks)
7. [Cron Jobs](#cron-jobs)
8. [Land Data](#land-data)
9. [Error Responses](#error-responses)

---

## Health & Status

### `GET /`

Root endpoint - API health check and welcome message.

**Response:**

```json
{
  "status": "online",
  "message": "Terraguard API - Guarding the Land. Empowering the People.",
  "version": "1.0.0",
  "timestamp": "2025-10-13T10:00:00.000Z",
  "docs": "/docs",
  "health": "/health"
}
```

### `GET /health`

Detailed health check showing all service statuses.

**Response:**

```json
{
  "status": "healthy",
  "timestamp": "2025-10-13T10:00:00.000Z",
  "services": {
    "api": "running",
    "database": "connected",
    "telegram_bot": "active",
    "whatsapp": "active"
  },
  "features": {
    "ai_chat": true,
    "alerts": true,
    "climate_detection": true
  },
  "version": "1.0.0"
}
```

---

## Climate Risk Detection

### `POST /api/risk/detect`

Detect climate risks for a specific region based on last 30 days of data.

**Request Body:**

```json
{
  "region": "Kitui County"
}
```

**Response:**

```json
{
  "success": true,
  "region": "Kitui County",
  "risks_detected": 2,
  "risks": [
    {
      "type": "drought",
      "severity": "high",
      "confidence": 0.85,
      "description": "Significant rainfall deficit detected",
      "data": {
        "rainfall_deficit_percent": 65,
        "days_without_rain": 45,
        "soil_moisture": "critically_low"
      }
    },
    {
      "type": "temperature_extreme",
      "severity": "moderate",
      "confidence": 0.72,
      "description": "Above average temperatures recorded",
      "data": {
        "temperature_anomaly": "+2.5°C",
        "days_above_threshold": 18
      }
    }
  ]
}
```

### `POST /api/risk/forecast`

Get current risk status and forecast for a region.

**Request Body:**

```json
{
  "region": "Nairobi"
}
```

**Response:**

```json
{
  "success": true,
  "data": {
    "region": "Nairobi",
    "coordinates": {
      "latitude": -1.286389,
      "longitude": 36.817223
    },
    "current_conditions": {
      "temperature": 22.5,
      "rainfall_last_7days": 12.3,
      "humidity": 68
    },
    "risk_levels": {
      "drought": "low",
      "flood": "low",
      "heat_stress": "moderate"
    },
    "active_alerts": [],
    "forecast_summary": "Normal conditions expected for the next 7 days",
    "last_updated": "2025-10-13T08:00:00Z"
  }
}
```

### `POST /api/risk/analyze-coordinates`

Analyze climate risks for specific GPS coordinates.

**Request Body:**

```json
{
  "latitude": -1.367,
  "longitude": 38.017
}
```

**Response:**

```json
{
  "success": true,
  "data": {
    "coordinates": {
      "latitude": -1.367,
      "longitude": 38.017
    },
    "location": "Kitui County",
    "climate_zone": "semi-arid",
    "risks": [...],
    "recommendations": [
      "Plant drought-resistant crops",
      "Implement water harvesting",
      "Use mulching techniques"
    ]
  }
}
```

---

## Alerts

### `GET /api/alerts`

Get all active climate alerts, optionally filtered by region.

**Query Parameters:**

- `region` (optional): Filter by region name

**Response:**

```json
{
  "success": true,
  "count": 3,
  "alerts": [
    {
      "id": "uuid-here",
      "region": "Kitui County",
      "risk_type": "drought",
      "severity": "high",
      "title": "Severe Drought Warning",
      "description": "Extended dry period with significant rainfall deficit",
      "ai_summary": "Kitui County is experiencing severe drought conditions...",
      "preventive_measures": [
        "Plant drought-resistant crops like sorghum and millet",
        "Implement rainwater harvesting systems",
        "Use mulching to retain soil moisture"
      ],
      "immediate_actions": [
        "Ration water supplies carefully",
        "Provide supplemental feed for livestock",
        "Monitor weather forecasts daily"
      ],
      "created_at": "2025-10-08T10:00:00Z",
      "expires_at": "2025-10-15T10:00:00Z",
      "data_source": {
        "api": "NASA POWER",
        "last_updated": "2025-10-08T09:00:00Z"
      }
    }
  ]
}
```

### `GET /api/alerts/{alert_id}`

Get detailed information about a specific alert.

**Response:**

```json
{
  "success": true,
  "alert": {
    "id": "uuid-here",
    "region": "Machakos County",
    "risk_type": "flood",
    "severity": "moderate",
    "...": "..."
  }
}
```

---

## Subscriptions

### `POST /api/subscribe`

Subscribe to climate alerts for a specific region. Supports both SMS (phone number) and Telegram.

**Request Body:**

```json
{
  "phone_number": "+254712345678",
  "telegram_id": 123456789,
  "region": "Nairobi",
  "latitude": -1.286389,
  "longitude": 36.817223
}
```

**Note:** Either `phone_number` or `telegram_id` must be provided.

**Response:**

```json
{
  "success": true,
  "message": "Subscribed to climate alerts",
  "user_id": "uuid-here"
}
```

### `GET /api/regions`

Get list of supported regions in Kenya.

**Response:**

```json
{
  "success": true,
  "count": 15,
  "regions": [
    {
      "name": "Nairobi",
      "climate_zone": "Temperate"
    },
    {
      "name": "Mombasa",
      "climate_zone": "Tropical"
    },
    {
      "name": "Kisumu",
      "climate_zone": "Tropical"
    }
  ]
}
```

### `POST /api/geocode`

Convert location name to GPS coordinates.

**Request Body:**

```json
{
  "region": "Eldoret"
}
```

**Response:**

```json
{
  "success": true,
  "location": {
    "name": "Eldoret",
    "latitude": 0.5143,
    "longitude": 35.2698,
    "formatted_address": "Eldoret, Kenya"
  }
}
```

---

## AI Assistant

### `POST /api/ai/answer`

Get AI-powered answers to farming and climate questions. Stateless endpoint with no conversation memory.

**Request Body:**

```json
{
  "question": "What crops should I plant after heavy rains in Kisumu?"
}
```

**Response:**

```json
{
  "answer": "After heavy rains in Kisumu, consider planting maize, beans, and sukuma wiki. These crops thrive in moist conditions. Ensure proper spacing to prevent fungal diseases. Tuchunge mazingira yetu - plant cover crops to prevent soil erosion.",
  "model": "openai/gpt-5-mini",
  "timestamp": "2025-10-13T12:30:00.000Z"
}
```

**Rate Limiting:** 10 requests per minute per IP address.

### `GET /api/ai/status`

Check AI service configuration and availability.

**Response:**

```json
{
  "status": "configured",
  "model": "openai/gpt-5-mini",
  "rate_limit": "10 requests/minute",
  "features": {
    "stateless": true,
    "no_memory": true,
    "agriculture_focused": true
  }
}
```

---

## Webhooks

### `POST /webhook/whatsapp`

Twilio WhatsApp webhook endpoint for incoming messages.

**Request Body (from Twilio):**

```
From=whatsapp:+254712345678
Body=How is the weather in Nairobi?
MessageSid=SM...
ProfileName=John Doe
```

**Response:**

```json
{
  "status": "success",
  "message_sid": "SM..."
}
```

### `GET /webhook/whatsapp`

WhatsApp webhook verification endpoint.

**Response:**

```json
{
  "status": "active",
  "service": "Terraguard WhatsApp Webhook"
}
```

### `POST /webhook/telegram`

Telegram webhook endpoint (currently using polling mode, but ready for webhook).

**Request Body:**

```json
{
  "update_id": 123456,
  "message": {
    "message_id": 1,
    "from": {...},
    "text": "Hello"
  }
}
```

---

## Cron Jobs

### `GET /cron/detect-risks`

Trigger climate risk detection for all regions (scheduled job).

**Headers Required:**

```
X-Cron-Secret: <CRON_SECRET_KEY>
```

**Response:**

```json
{
  "status": "completed",
  "regions_analyzed": 15,
  "risks_detected": 8,
  "alerts_created": 5,
  "execution_time_seconds": 42.5
}
```

### `GET /cron/send-daily-alerts`

Send daily climate alerts to subscribed users (scheduled job).

**Headers Required:**

```
X-Cron-Secret: <CRON_SECRET_KEY>
```

**Response:**

```json
{
  "status": "completed",
  "users_notified": 1247,
  "sms_sent": 980,
  "telegram_sent": 267,
  "failed": 0
}
```

---

## Land Data

### `GET /api/land/elevation`

Get elevation data for specific coordinates.

**Query Parameters:**

- `latitude` (required): Latitude coordinate
- `longitude` (required): Longitude coordinate

**Response:**

```json
{
  "success": true,
  "elevation_meters": 1795.5,
  "coordinates": {
    "latitude": -1.286389,
    "longitude": 36.817223
  }
}
```

### `GET /api/land/soil-type`

Get soil type information for a location.

**Query Parameters:**

- `latitude` (required)
- `longitude` (required)

**Response:**

```json
{
  "success": true,
  "soil_type": "clay_loam",
  "characteristics": {
    "water_retention": "high",
    "drainage": "moderate",
    "fertility": "good"
  },
  "recommended_crops": ["maize", "beans", "vegetables"]
}
```

---

## Error Responses

All endpoints return errors in this consistent format:

```json
{
  "error": true,
  "message": "Detailed error message",
  "code": "ERROR_CODE",
  "timestamp": "2025-10-13T10:00:00.000Z"
}
```

**Common HTTP Status Codes:**

- `200` - Success
- `201` - Created
- `400` - Bad Request (validation error)
- `401` - Unauthorized
- `404` - Not Found
- `429` - Too Many Requests (rate limit exceeded)
- `500` - Internal Server Error
- `503` - Service Unavailable

---

## Rate Limiting

| Endpoint Category | Rate Limit |
|-------------------|------------|
| Public endpoints | 100 requests/minute |
| AI endpoints | 10 requests/minute |
| Webhook endpoints | 1000 requests/minute |

Rate limits are enforced per IP address. When exceeded, you'll receive a `429 Too Many Requests` response.

---

## Testing & Documentation

**Interactive API Documentation:**

- Swagger UI: `https://terraguard-api.onrender.com/docs`
- ReDoc: `https://terraguard-api.onrender.com/redoc`

Both provide interactive testing environments where you can try all endpoints directly in your browser.

---

## SDKs & Examples

### Python Example

```python
import requests

# Detect climate risks
response = requests.post(
    "https://terraguard-api.onrender.com/api/risk/detect",
    json={"region": "Nairobi"}
)
data = response.json()
print(f"Risks detected: {data['risks_detected']}")

# Ask AI assistant
response = requests.post(
    "https://terraguard-api.onrender.com/api/ai/answer",
    json={"question": "Best crops for drought?"}
)
answer = response.json()
print(answer['answer'])
```

### JavaScript Example

```javascript
// Fetch active alerts
fetch('https://terraguard-api.onrender.com/api/alerts')
  .then(res => res.json())
  .then(data => {
    console.log(`Active alerts: ${data.count}`);
    data.alerts.forEach(alert => {
      console.log(`${alert.region}: ${alert.title}`);
    });
  });

// Subscribe to alerts
fetch('https://terraguard-api.onrender.com/api/subscribe', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    phone_number: '+254712345678',
    region: 'Nairobi'
  })
})
  .then(res => res.json())
  .then(data => console.log(data.message));
```

---

## Support

For issues, questions, or feature requests:

- **GitHub:** [MuganziJames/terraguard-system](https://github.com/MuganziJames/terraguard-system)
- **API Status:** Check `/health` endpoint
- **Interactive Docs:** `https://terraguard-api.onrender.com/docs`

---

**Last Updated:** October 13, 2025  
**API Version:** 1.0.0
