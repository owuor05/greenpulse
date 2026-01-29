# Terraguard System Architecture

**Version:** 1.0.0  
**Last Updated:** October 13, 2025

## Overview

Terraguard is an AI-powered climate risk and land conservation platform designed to detect, communicate, and educate about environmental threats across African regions, with a focus on Kenya. The system combines real-time climate data, AI-driven insights, and multi-channel communication (web, SMS, WhatsApp, Telegram) to empower communities.

---

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         EXTERNAL DATA SOURCES                        │
├──────────────────┬──────────────────┬─────────────────┬─────────────┤
│  NASA POWER API  │  Google Maps API │ OpenRouter AI   │  Supabase   │
│  (Climate Data)  │  (Geocoding)     │  (GPT-5 mini)   │  (Database) │
└────────┬─────────┴──────────┬───────┴────────┬────────┴──────┬──────┘
         │                    │                 │               │
         └────────────────────┼─────────────────┼───────────────┘
                              │                 │
                    ┌─────────▼─────────────────▼────────────┐
                    │    TERRAGUARD BACKEND (FastAPI)        │
                    │    https://terraguard-api.onrender.com │
                    ├────────────────────────────────────────┤
                    │  • Climate Risk Detection Engine      │
                    │  • AI Service (OpenRouter)             │
                    │  • Database Service (Supabase)         │
                    │  • Location Caching                    │
                    │  • Alert Generation                    │
                    │  • API Routes                          │
                    └──────────┬──────────────────────────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         │                     │                     │
    ┌────▼─────┐       ┌──────▼──────┐      ┌──────▼────────┐
    │  WEB APP │       │  TELEGRAM   │      │   WHATSAPP    │
    │  (React) │       │    BOT      │      │  (via Twilio) │
    │  Vercel  │       │  (Railway)  │      │   (Render)    │
    └──────────┘       └─────────────┘      └───────────────┘
         │                     │                     │
         └─────────────────────┼─────────────────────┘
                               │
                       ┌───────▼────────┐
                       │      USERS     │
                       │  • Farmers     │
                       │  • Communities │
                       │  • Researchers │
                       └────────────────┘
```

---

## Technology Stack

### Frontend

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Framework** | React 18.3 | UI framework with modern hooks |
| **Build Tool** | Vite 5.4 | Fast development server and bundler |
| **Routing** | React Router v6 | Client-side navigation |
| **Styling** | Tailwind CSS 3.4 | Utility-first CSS framework |
| **Maps** | Leaflet.js | Interactive maps for risk visualization |
| **HTTP Client** | Axios | API communication |
| **Hosting** | Vercel | Serverless frontend hosting |

**Deployment URL:** https://terraguard-system.vercel.app/

### Backend

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Framework** | FastAPI 0.115 | High-performance Python API framework |
| **Server** | Uvicorn 0.32 | ASGI server |
| **AI Service** | OpenRouter (GPT-5 mini) | Natural language processing and chat |
| **Climate Data** | NASA POWER API | Historical and real-time climate data |
| **Geocoding** | Google Maps API | Location services and reverse geocoding |
| **Database** | Supabase (PostgreSQL) | User data, alerts, and chat history |
| **SMS** | Twilio | WhatsApp messaging integration |
| **Telegram** | python-telegram-bot 21.8 | Telegram bot framework |
| **Data Processing** | Pandas, NumPy | Climate data analysis |
| **Hosting (API)** | Render Web Services | Backend hosting |
| **Hosting (Bot)** | Railway | Telegram bot worker hosting |

**API URL:** https://terraguard-api.onrender.com  
**Bot Hosting:** Railway (long-running worker process)

### Database (Supabase)

**Technology:** PostgreSQL 15+  
**Features:** Row-level security, real-time subscriptions, auto-generated REST API

---

## Core Components

### 1. Climate Risk Detection Engine

**Location:** `backend/app/services/climate_risk_service.py`

**Responsibilities:**
- Fetch climate data from NASA POWER API
- Analyze historical trends (30-day rolling windows)
- Detect anomalies: drought, flood, temperature extremes
- Calculate risk severity scores
- Generate alerts with AI-powered summaries

**Data Sources:**
- Temperature (daily min/max/avg)
- Precipitation (rainfall amounts)
- Soil moisture estimates
- Relative humidity
- Wind speed

**Detection Algorithms:**
- **Drought:** Rainfall deficit > 50% below 30-day average
- **Flood:** Rainfall excess > 200% above average
- **Heat Stress:** Temperatures > 35°C for 5+ consecutive days

### 2. AI Service (OpenRouter Integration)

**Location:** `backend/app/services/ai_service.py`, `backend/app/services/intent_parser.py`

**Models Used:**
- **Primary:** GPT-5 mini (via OpenRouter)
- **Purpose:** Natural language understanding, response generation, intent detection

**Key Features:**
- **Stateless Q&A:** Single-turn conversations for web AI chat
- **Conversational AI:** Multi-turn conversations for Telegram/WhatsApp
- **Language Detection:** Automatic English/Swahili detection
- **Location Extraction:** Parse location names from user messages
- **Intent Recognition:** Identify user needs (weather, crops, alerts, etc.)

**System Prompt Focus:**
- Land conservation and rehabilitation
- Climate resilience education
- Practical farming advice
- African environmental wisdom

### 3. Multi-Channel Communication

#### Web Application (React)

**Location:** `frontend/src/`

**Features:**
- Interactive risk map of Kenya
- Real-time alert dashboard
- AI chat assistant
- Educational content hub
- Community reporting system

**Key Pages:**
- Home: Subscription and overview
- Alerts: Browse and filter active alerts
- AI Assistant: Chat interface for farming questions
- Education: Articles and guides
- Reports: Community observations

#### Telegram Bot

**Location:** `backend/app/telegram/bot.py`

**Deployment:** Railway (long-running worker)

**Features:**
- Natural conversational AI (no commands required)
- Automatic location detection from messages
- GPS location sharing support
- Daily climate alerts
- Bilingual support (English/Swahili)
- Personalized recommendations

**User Flow:**
1. User starts bot with `/start`
2. Bot asks for location (GPS or text)
3. User can ask any question naturally
4. Bot provides AI-powered responses with real climate data
5. Optionally subscribes to daily alerts

#### WhatsApp Integration

**Location:** `backend/app/whatsapp/twilio_client.py`

**Deployment:** Render (webhook receiver)

**Features:**
- Webhook-based message handling
- AI-powered conversation
- Alert delivery via WhatsApp
- Profile name recognition

### 4. Database Service

**Location:** `backend/app/services/database.py`

**Schema:**

```sql
-- Users Table
users (
  id UUID PRIMARY KEY,
  phone_number VARCHAR UNIQUE,
  telegram_id BIGINT UNIQUE,
  username VARCHAR,
  first_name VARCHAR,
  region VARCHAR,
  latitude FLOAT,
  longitude FLOAT,
  subscribed BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT now()
)

-- Alerts Table
alerts (
  id UUID PRIMARY KEY,
  region VARCHAR NOT NULL,
  risk_type VARCHAR NOT NULL, -- drought, flood, heat, etc.
  severity VARCHAR NOT NULL, -- low, moderate, high, critical
  title TEXT,
  description TEXT,
  ai_summary TEXT,
  preventive_measures JSONB,
  immediate_actions JSONB,
  created_at TIMESTAMPTZ DEFAULT now(),
  expires_at TIMESTAMPTZ,
  data_source JSONB
)

-- Chat Messages Table (Telegram)
telegram_messages (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  telegram_id BIGINT,
  chat_id BIGINT,
  message TEXT,
  direction VARCHAR, -- incoming/outgoing
  ai_response TEXT,
  language VARCHAR,
  created_at TIMESTAMPTZ DEFAULT now()
)

-- WhatsApp Messages Table
whatsapp_messages (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  phone_number VARCHAR,
  message TEXT,
  direction VARCHAR,
  ai_response TEXT,
  message_sid VARCHAR,
  created_at TIMESTAMPTZ DEFAULT now()
)
```

### 5. Location Caching System

**Location:** `backend/app/services/location_cache.py`

**Purpose:** Reduce Google Maps API costs by caching frequently queried locations

**Features:**
- In-memory cache for Kenyan counties and major cities
- Reduces API calls by ~80%
- Instant lookup for common locations

**Cached Locations:**
- All 47 Kenyan counties
- Major cities (Nairobi, Mombasa, Kisumu, etc.)
- Common misspellings and variations

### 6. Cron Jobs & Scheduled Tasks

**Location:** `backend/app/routes/cron.py`

**Scheduled Jobs:**

| Job | Frequency | Purpose |
|-----|-----------|---------|
| `detect-risks` | Every 6 hours | Analyze climate data for all regions |
| `send-daily-alerts` | Daily at 7 AM EAT | Send morning alerts to subscribed users |
| `cleanup-old-alerts` | Daily at midnight | Remove expired alerts from database |

**Security:** All cron endpoints require `X-Cron-Secret` header

---

## Data Flow Examples

### 1. User Subscribes via Web

```
User fills form → Frontend POST /api/subscribe
                ↓
            Backend validates data
                ↓
        Geocode location (Google Maps)
                ↓
        Save to Supabase users table
                ↓
        Return success to frontend
```

### 2. Climate Risk Detection

```
Cron job triggers → GET /cron/detect-risks
                         ↓
            Loop through all regions
                         ↓
        Fetch NASA POWER data (30 days)
                         ↓
        Analyze for anomalies
                         ↓
        If risk detected → Generate AI summary
                         ↓
        Create alert in database
                         ↓
        Query subscribed users in region
                         ↓
        Send via Telegram/WhatsApp
```

### 3. Telegram Conversation

```
User sends message → Telegram → Webhook/Polling
                                      ↓
                    Backend receives update
                                      ↓
                    Parse message with AI
                                      ↓
                Extract: location, language, intent
                                      ↓
        If location detected → Fetch climate data
                                      ↓
                Generate AI response
                                      ↓
        Save conversation to database
                                      ↓
        Send reply to Telegram
```

### 4. WhatsApp Message

```
User sends WhatsApp → Twilio webhook → POST /webhook/whatsapp
                                              ↓
                            Parse From and Body
                                              ↓
                        Generate AI response
                                              ↓
                    Send reply via Twilio API
                                              ↓
                Save to database
```

---

## Security & Privacy

### API Security

- **CORS:** Restricted to frontend domain (terraguard-system.vercel.app)
- **Rate Limiting:** IP-based rate limits on all endpoints
- **Input Validation:** Pydantic models for all request bodies
- **Error Handling:** Sanitized error messages (no internal details exposed)

### Data Privacy

- **No PII in Logs:** Phone numbers and personal data excluded from logs
- **Optional Anonymous Reporting:** Users can submit reports without identification
- **Data Retention:** Old chat messages archived after 90 days

### Secrets Management

- **Environment Variables:** All API keys stored in platform-specific env vars
- **Supabase Row-Level Security:** Database-level access controls
- **Webhook Verification:** Cron endpoints require secret header

---

## Scalability Considerations

### Current Architecture (MVP)

- **Stateless API:** Horizontal scaling ready
- **Serverless Frontend:** Auto-scaling on Vercel
- **Database:** Supabase managed PostgreSQL with connection pooling
- **Background Jobs:** Cron-based (can migrate to queue-based system)

### Future Improvements

1. **Message Queue:** Implement Celery + Redis for async task processing
2. **CDN Caching:** Cache static climate data and educational content
3. **Database Optimization:** Add indexes on frequently queried fields
4. **API Gateway:** Add rate limiting at infrastructure level
5. **Microservices:** Split AI service, climate detection, and alerts into separate services

---

## Monitoring & Observability

### Health Checks

- **API Health:** `/health` endpoint monitors all services
- **Database Connectivity:** Connection pooling with retry logic
- **External APIs:** Fallback strategies for NASA POWER and Google Maps

### Logging

- **Structured Logging:** JSON format for easy parsing
- **Log Levels:** INFO for operations, ERROR for failures
- **Sensitive Data:** Phone numbers and API keys excluded

### Error Tracking

- **HTTP Errors:** Consistent error response format
- **AI Failures:** Graceful degradation with fallback messages
- **Database Errors:** Retry logic with exponential backoff

---

## Development Workflow

### Local Development

```bash
# Frontend
cd frontend
npm install
npm run dev  # Runs on http://localhost:5173

# Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload  # Runs on http://localhost:8000

# Telegram Bot (local testing)
python start_telegram_bot.py
```

### Environment Variables Required

**Backend (.env):**
```
# Database
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key

# AI
OPENROUTER_API_KEY=your-key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=openai/gpt-5-mini

# Google Maps
GOOGLE_MAPS_API_KEY=your-key

# Telegram
TELEGRAM_BOT_TOKEN=your-token

# Twilio (WhatsApp)
TWILIO_ACCOUNT_SID=your-sid
TWILIO_AUTH_TOKEN=your-token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Security
CRON_SECRET=your-secret-key
CORS_ORIGINS=http://localhost:5173,https://terraguard-system.vercel.app
```

**Frontend (.env):**
```
VITE_API_URL=https://terraguard-api.onrender.com
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
```

---

## Deployment Architecture

### Frontend (Vercel)

- **Build Command:** `npm run build`
- **Output Directory:** `dist`
- **Auto-Deploy:** Pushes to `main` branch
- **Environment:** Node.js 18+

### Backend API (Render)

- **Type:** Web Service
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Health Check:** `/health` endpoint
- **Auto-Deploy:** Pushes to `main` branch

### Telegram Bot (Railway)

- **Type:** Worker Service
- **Start Command:** `python start_telegram_bot.py`
- **No HTTP port required** (uses Telegram long polling)
- **Keep-Alive:** Runs continuously

### Database (Supabase)

- **Type:** Managed PostgreSQL
- **Backups:** Automatic daily backups
- **Scaling:** Auto-scaling connections

---

## API Versioning

**Current Version:** v1.0.0

**Versioning Strategy:**
- Major version (1.x.x): Breaking changes
- Minor version (x.1.x): New features, backward compatible
- Patch version (x.x.1): Bug fixes

**Deprecation Policy:**
- Deprecated endpoints marked 6 months before removal
- Breaking changes communicated via API changelog

---

## Performance Metrics

### Target Performance

| Metric | Target | Current |
|--------|--------|---------|
| API Response Time | < 200ms | ~150ms |
| Alert Generation | < 5 min | ~3 min |
| AI Response Time | < 3s | ~2s |
| Database Queries | < 50ms | ~30ms |
| Uptime | 99.5% | 99.7% |

### Optimization Strategies

- **Location Caching:** Reduces API calls by 80%
- **Database Indexing:** Fast lookups on user IDs and regions
- **Async Operations:** Non-blocking SMS/Telegram sends
- **Connection Pooling:** Reuse database connections

---

## Future Architecture Plans

### Phase 2 Enhancements

1. **Mobile App:** React Native for iOS/Android
2. **Offline Mode:** PWA with service workers
3. **Advanced Analytics:** Risk prediction models
4. **Multi-Region Support:** Expand beyond Kenya to East Africa
5. **Voice Integration:** WhatsApp voice notes support
6. **Image Analysis:** Crop disease detection from photos

### Phase 3 (Enterprise)

1. **Government Dashboard:** Admin panel for authorities
2. **API Partnerships:** White-label API for NGOs
3. **Data Marketplace:** Sell aggregated climate insights
4. **Community Moderation:** User-generated content verification

---

## Contributing

For architecture proposals or improvements:

1. Review this document
2. Open GitHub issue with `[ARCHITECTURE]` tag
3. Submit PR with architecture diagram updates

---

**Maintained by:** Terraguard Team  
**Last Reviewed:** October 13, 2025
