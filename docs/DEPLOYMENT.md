# Terraguard Deployment Guide

**Version:** 1.0.0  
**Last Updated:** October 13, 2025

This document provides comprehensive deployment instructions for all components of the Terraguard system.

---

## Table of Contents

1. [Deployment Overview](#deployment-overview)
2. [Frontend Deployment (Vercel)](#frontend-deployment-vercel)
3. [Backend API Deployment (Render)](#backend-api-deployment-render)
4. [Telegram Bot Deployment (Railway)](#telegram-bot-deployment-railway)
5. [Database Setup (Supabase)](#database-setup-supabase)
6. [Environment Variables](#environment-variables)
7. [Monitoring & Maintenance](#monitoring--maintenance)
8. [Troubleshooting](#troubleshooting)

---

## Deployment Overview

### Current Production URLs

| Component | Platform | URL | Status |
|-----------|----------|-----|--------|
| **Web App** | Vercel | https://terraguard-system.vercel.app/ | ✅ Live |
| **Backend API** | Render Web Services | https://terraguard-api.onrender.com/docs | ✅ Live |
| **Telegram Bot** | Railway | (Worker - No Public URL) | ✅ Active |
| **Database** | Supabase | (Managed PostgreSQL) | ✅ Connected |

### Architecture Overview

```
┌──────────────────────────────────────────────────────────┐
│                    PRODUCTION STACK                       │
├────────────────┬────────────────┬────────────────────────┤
│   FRONTEND     │   BACKEND API  │   TELEGRAM BOT         │
│   (Vercel)     │   (Render)     │   (Railway)            │
│                │                │                        │
│ React + Vite   │ FastAPI        │ python-telegram-bot    │
│ Tailwind CSS   │ Uvicorn        │ Long-polling mode      │
│ Auto-deploy    │ Auto-deploy    │ Continuous worker      │
└────────────────┴────────────────┴────────────────────────┘
                         │
                         ▼
           ┌─────────────────────────┐
           │  SUPABASE (Database)    │
           │  PostgreSQL + REST API  │
           └─────────────────────────┘
```

---

## Frontend Deployment (Vercel)

### Platform: Vercel

**Live URL:** https://terraguard-system.vercel.app/

### Prerequisites

- GitHub repository connected to Vercel
- Node.js 18+ environment
- Vercel CLI (optional): `npm install -g vercel`

### Deployment Steps

#### 1. Connect Repository to Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **"New Project"**
3. Import your GitHub repository: `MuganziJames/terraguard-system`
4. Select **"frontend"** as the root directory
5. Framework preset: **Vite** (auto-detected)

#### 2. Configure Build Settings

```yaml
Build Command: npm run build
Output Directory: dist
Install Command: npm install
```

#### 3. Environment Variables

Add these in **Project Settings → Environment Variables:**

```env
VITE_API_URL=https://terraguard-api.onrender.com
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-supabase-anon-key
```

#### 4. Deploy

**Automatic Deployment:**
- Push to `main` branch → Vercel auto-deploys
- Preview deployments for all branches

**Manual Deployment (CLI):**

```bash
cd frontend
vercel --prod
```

### Post-Deployment

1. **Verify Deployment:**
   - Visit https://terraguard-system.vercel.app/
   - Check browser console for errors
   - Test API connectivity

2. **Custom Domain (Optional):**
   - Go to **Project Settings → Domains**
   - Add custom domain: `www.terraguard.com`
   - Configure DNS records as instructed

3. **Performance Optimization:**
   - Vercel automatically handles:
     - CDN distribution
     - Image optimization
     - Automatic SSL/TLS

---

## Backend API Deployment (Render)

### Platform: Render Web Services

**Live URL:** https://terraguard-api.onrender.com  
**API Docs:** https://terraguard-api.onrender.com/docs

### Prerequisites

- GitHub repository
- Render account
- Python 3.10+ runtime

### Deployment Steps

#### 1. Create New Web Service

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +" → "Web Service"**
3. Connect GitHub repository: `MuganziJames/terraguard-system`
4. Configure:
   - **Name:** `terraguard-api`
   - **Root Directory:** `backend`
   - **Environment:** `Python 3`
   - **Region:** `Oregon (US West)` or closest to Kenya
   - **Branch:** `main`

#### 2. Build & Start Commands

```yaml
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

#### 3. Environment Variables

Add in **Environment → Environment Variables:**

```env
# Python Runtime
PYTHON_VERSION=3.10.0

# Application
APP_NAME=Terraguard API
APP_VERSION=1.0.0
DEBUG=False
PORT=8000
HOST=0.0.0.0

# Database (Supabase)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key

# AI (OpenRouter)
OPENROUTER_API_KEY=your-openrouter-key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=openai/gpt-5-mini

# Google Maps
GOOGLE_MAPS_API_KEY=your-google-maps-key

# Telegram
TELEGRAM_BOT_TOKEN=your-bot-token

# Twilio (WhatsApp)
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_WHATSAPP_NUMBER=whatsapp number

# Security
CRON_SECRET=your-random-secret-key
CORS_ORIGINS=https://terraguard-system.vercel.app,http://localhost:5173

# Feature Flags
ENABLE_AI_CHAT=True
```

#### 4. Health Check Configuration

```yaml
Health Check Path: /health
```

Render will ping this endpoint every 30 seconds to verify service health.

#### 5. Deploy

1. Click **"Create Web Service"**
2. Render will:
   - Clone repository
   - Install dependencies
   - Start Uvicorn server
   - Assign public URL

**Deployment time:** ~5-7 minutes

### Post-Deployment

1. **Verify API:**

```bash
curl https://terraguard-api.onrender.com/health
```

Expected response:

```json
{
  "status": "healthy",
  "services": {
    "api": "running",
    "database": "connected"
  }
}
```

2. **Test Interactive Docs:**
   - Visit: https://terraguard-api.onrender.com/docs
   - Test endpoints directly in Swagger UI

3. **Monitor Logs:**
   - Go to **Logs** tab in Render dashboard
   - Check for startup errors or warnings

### Render Configuration Files

**Optional:** You can use `render.yaml` for infrastructure-as-code:

```yaml
# backend/render.yaml
services:
  - type: web
    name: terraguard-api
    env: python
    rootDir: backend
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    healthCheckPath: /health
    envVars:
      - key: PYTHON_VERSION
        value: 3.10.0
      - key: APP_NAME
        value: Terraguard API
```

---

## Telegram Bot Deployment (Railway)

### Platform: Railway

**Type:** Worker Service (Long-Running Process)  
**Invite Link:** https://railway.com/invite/b6pZTByMl_R

### Prerequisites

- GitHub repository
- Railway account
- Telegram Bot Token (from @BotFather)

### Why Railway for Telegram Bot?

Unlike the REST API, Telegram bots need to:
- Run continuously (24/7)
- Use long-polling to receive messages
- Not require HTTP port exposure
- Handle WebSocket-like connections

Railway is perfect for worker processes that don't need a public URL.

### Deployment Steps

#### 1. Create New Project

1. Go to [Railway Dashboard](https://railway.app/)
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose: `MuganziJames/terraguard-system`

#### 2. Configure Service

1. **Service Name:** `terraguard-telegram-bot`
2. **Root Directory:** `backend`
3. **Start Command:**

```bash
python start_telegram_bot.py
```

4. **Runtime:** Python 3.10+

#### 3. Environment Variables

Add in **Variables** tab:

```env
# Python
PYTHON_VERSION=3.10.0

# Telegram
TELEGRAM_BOT_TOKEN=your-bot-token-from-botfather

# Database (Supabase)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key

# AI (OpenRouter)
OPENROUTER_API_KEY=your-openrouter-key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=openai/gpt-5-mini

# Google Maps
GOOGLE_MAPS_API_KEY=your-google-maps-key

# Feature Flags
ENABLE_AI_CHAT=True
```

#### 4. Procfile Configuration

Ensure `backend/Procfile` contains:

```
worker: python start_telegram_bot.py
```

#### 5. Deploy

Railway will:
1. Install dependencies from `requirements.txt`
2. Start bot script
3. Bot begins polling Telegram for messages

**Deployment time:** ~3-4 minutes

### Post-Deployment

1. **Verify Bot is Running:**

Open Telegram and send `/start` to your bot. You should receive a welcome message.

2. **Check Logs:**

In Railway dashboard:
- Go to **Deployments** → **View Logs**
- Look for: `"Terraguard Telegram Bot started successfully"`

3. **Test Functionality:**

Send test messages:
```
"Hello" → Should get greeting
"What's the weather in Nairobi?" → Should get AI response
Share location → Should save location
```

### Telegram Bot Setup (One-Time)

#### Create Bot with @BotFather

1. Open Telegram and search for `@BotFather`
2. Send `/newbot`
3. Provide bot name: `Terraguard Climate Bot`
4. Choose username: `terraguard_bot` (or similar)
5. Copy the bot token (keep it secret!)

#### Configure Bot Settings

```
/setdescription - AI-powered climate assistant for African farmers
/setabouttext - Get weather forecasts, crop advice, and climate alerts
/setcommands - start - Start the bot and get help
```

#### Set Bot Commands (Optional)

While the bot uses natural conversation, these commands are available:

```
start - Welcome message and setup
help - Show available features
```

---

## Database Setup (Supabase)

### Platform: Supabase (Managed PostgreSQL)

### Prerequisites

- Supabase account
- Database schema (see `database_schema.sql`)

### Setup Steps

#### 1. Create New Project

1. Go to [Supabase Dashboard](https://app.supabase.com/)
2. Click **"New Project"**
3. Configure:
   - **Name:** `terraguard-production`
   - **Database Password:** (Generate strong password)
   - **Region:** Choose closest to Kenya (e.g., `eu-west-2` - London)
   - **Pricing Plan:** Free tier (upgradeable)

#### 2. Create Tables

1. Go to **SQL Editor**
2. Run the schema from `database_schema.sql`:

```sql
-- Users Table
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  phone_number VARCHAR(20) UNIQUE,
  telegram_id BIGINT UNIQUE,
  username VARCHAR(255),
  first_name VARCHAR(255),
  region VARCHAR(255),
  latitude FLOAT,
  longitude FLOAT,
  subscribed BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- Alerts Table
CREATE TABLE alerts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  region VARCHAR(255) NOT NULL,
  risk_type VARCHAR(100) NOT NULL,
  severity VARCHAR(50) NOT NULL,
  title TEXT,
  description TEXT,
  ai_summary TEXT,
  preventive_measures JSONB,
  immediate_actions JSONB,
  created_at TIMESTAMPTZ DEFAULT now(),
  expires_at TIMESTAMPTZ,
  data_source JSONB
);

-- Telegram Messages Table
CREATE TABLE telegram_messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  telegram_id BIGINT,
  chat_id BIGINT,
  username VARCHAR(255),
  first_name VARCHAR(255),
  message TEXT,
  direction VARCHAR(20),
  ai_response TEXT,
  language VARCHAR(20),
  created_at TIMESTAMPTZ DEFAULT now()
);

-- WhatsApp Messages Table
CREATE TABLE whatsapp_messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  phone_number VARCHAR(20),
  profile_name VARCHAR(255),
  message TEXT,
  direction VARCHAR(20),
  ai_response TEXT,
  message_sid VARCHAR(255),
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Indexes for performance
CREATE INDEX idx_users_phone ON users(phone_number);
CREATE INDEX idx_users_telegram ON users(telegram_id);
CREATE INDEX idx_alerts_region ON alerts(region);
CREATE INDEX idx_alerts_created ON alerts(created_at);
CREATE INDEX idx_telegram_messages_user ON telegram_messages(user_id);
CREATE INDEX idx_whatsapp_messages_user ON whatsapp_messages(user_id);
```

#### 3. Get API Credentials

1. Go to **Settings → API**
2. Copy:
   - **Project URL:** `https://your-project.supabase.co`
   - **Anon Public Key:** `eyJhbGc...` (use this in production)

#### 4. Configure Row-Level Security (RLS)

For now, disable RLS for MVP (enable in production):

```sql
ALTER TABLE users DISABLE ROW LEVEL SECURITY;
ALTER TABLE alerts DISABLE ROW LEVEL SECURITY;
ALTER TABLE telegram_messages DISABLE ROW LEVEL SECURITY;
ALTER TABLE whatsapp_messages DISABLE ROW LEVEL SECURITY;
```

**For production security, enable RLS with policies:**

```sql
-- Enable RLS
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Allow service role full access
CREATE POLICY "Service role full access" ON users
  FOR ALL USING (auth.role() = 'service_role');
```

---

## Environment Variables

### Complete Environment Variables Checklist

#### Frontend (.env in Vercel)

```env
VITE_API_URL=https://terraguard-api.onrender.com
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-supabase-anon-key
```

#### Backend API (.env in Render)

```env
# Application
APP_NAME=Terraguard API
APP_VERSION=1.0.0
DEBUG=False
PORT=8000
HOST=0.0.0.0

# Database
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key

# AI
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=openai/gpt-5-mini

# External APIs
GOOGLE_MAPS_API_KEY=AIza...
TELEGRAM_BOT_TOKEN=7654321:ABC...
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Security
CRON_SECRET=random-secure-string-here
CORS_ORIGINS=https://terraguard-system.vercel.app,http://localhost:5173

# Features
ENABLE_AI_CHAT=True
```

#### Telegram Bot (.env in Railway)

```env
# Telegram
TELEGRAM_BOT_TOKEN=7654321:ABC...

# Database
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key

# AI
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=openai/gpt-5-mini

# Google Maps
GOOGLE_MAPS_API_KEY=AIza...

# Features
ENABLE_AI_CHAT=True
```

### How to Get API Keys

| Service | How to Get |
|---------|-----------|
| **Supabase** | Create project → Settings → API |
| **OpenRouter** | https://openrouter.ai/keys |
| **Google Maps** | https://console.cloud.google.com/apis/credentials |
| **Telegram Bot** | Talk to @BotFather on Telegram |
| **Twilio** | https://console.twilio.com/ |

---

## Monitoring & Maintenance

### Health Checks

**API Health:**

```bash
curl https://terraguard-api.onrender.com/health
```

**Expected Response:**

```json
{
  "status": "healthy",
  "services": {
    "api": "running",
    "database": "connected",
    "telegram_bot": "active",
    "whatsapp": "active"
  }
}
```

### Log Monitoring

**Render (API):**
- Dashboard → Service → Logs tab
- Real-time log streaming
- Search and filter capabilities

**Railway (Telegram Bot):**
- Dashboard → Deployment → Logs
- View bot startup and message handling

**Vercel (Frontend):**
- Dashboard → Deployments → Function Logs
- Build logs for each deployment

### Performance Monitoring

**Key Metrics to Track:**

| Metric | Tool | Target |
|--------|------|--------|
| API Response Time | Render Dashboard | < 200ms |
| Database Query Time | Supabase Logs | < 50ms |
| Bot Message Response | Telegram Analytics | < 3s |
| Frontend Load Time | Vercel Analytics | < 2s |
| Uptime | UptimeRobot (optional) | > 99.5% |

### Scheduled Maintenance

**Weekly:**
- Review error logs
- Check API rate limits
- Monitor database size

**Monthly:**
- Update dependencies
- Review security alerts
- Database backup verification

---

## Troubleshooting

### Common Issues

#### 1. API Not Responding

**Symptoms:** 502 Bad Gateway, timeout errors

**Solutions:**
1. Check Render service status
2. Verify environment variables are set
3. Check database connection:
   ```bash
   curl https://terraguard-api.onrender.com/health
   ```
4. Restart service in Render dashboard

#### 2. Telegram Bot Not Responding

**Symptoms:** Bot offline, no responses

**Solutions:**
1. Check Railway deployment logs
2. Verify `TELEGRAM_BOT_TOKEN` is correct
3. Test bot token:
   ```bash
   curl https://api.telegram.org/bot<YOUR_TOKEN>/getMe
   ```
4. Restart worker in Railway

#### 3. Database Connection Errors

**Symptoms:** 500 errors, "database not connected"

**Solutions:**
1. Verify Supabase project is running
2. Check `SUPABASE_URL` and `SUPABASE_KEY`
3. Test connection:
   ```bash
   curl https://your-project.supabase.co/rest/v1/users \
     -H "apikey: your-key"
   ```
4. Check Supabase connection pooling limits

#### 4. CORS Errors (Frontend)

**Symptoms:** Browser console shows CORS errors

**Solutions:**
1. Verify `CORS_ORIGINS` includes frontend URL
2. Check Vercel deployment URL matches
3. Ensure protocol (https) is correct

#### 5. AI Not Responding

**Symptoms:** Chat returns generic errors

**Solutions:**
1. Verify `OPENROUTER_API_KEY` is valid
2. Check OpenRouter account credits
3. Test API key:
   ```bash
   curl https://openrouter.ai/api/v1/auth/key \
     -H "Authorization: Bearer your-key"
   ```

### Emergency Rollback

**Render (API):**
1. Go to Deployments
2. Find previous successful deployment
3. Click "Redeploy"

**Vercel (Frontend):**
1. Go to Deployments
2. Find stable deployment
3. Click "Promote to Production"

**Railway (Bot):**
1. Go to Deployments
2. Find previous version
3. Click "Redeploy"

---

## Deployment Checklist

Before going live, verify:

- [ ] All environment variables set correctly
- [ ] Database tables created with indexes
- [ ] API health endpoint returns `healthy`
- [ ] Frontend loads without errors
- [ ] Telegram bot responds to messages
- [ ] WhatsApp webhook configured in Twilio
- [ ] CORS origins include production URL
- [ ] SSL/TLS certificates active (automatic)
- [ ] Domain names configured (if custom)
- [ ] Monitoring and logging enabled
- [ ] Backup strategy in place
- [ ] Error tracking configured
- [ ] Rate limiting tested
- [ ] API documentation accessible

---

## Support & Resources

### Platform Documentation

- **Vercel:** https://vercel.com/docs
- **Render:** https://render.com/docs
- **Railway:** https://docs.railway.app/
- **Supabase:** https://supabase.com/docs

### Terraguard Resources

- **GitHub Repository:** https://github.com/MuganziJames/terraguard-system
- **API Documentation:** https://terraguard-api.onrender.com/docs
- **Web App:** https://terraguard-system.vercel.app/

### Getting Help

For deployment issues:
1. Check this guide
2. Review platform-specific logs
3. Consult platform documentation
4. Open GitHub issue with `[DEPLOYMENT]` tag

---

**Last Updated:** October 13, 2025  
**Maintained by:** Terraguard Team
