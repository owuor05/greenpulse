# Local Development Guide

This guide will help you set up and run the Terraguard system on your local machine for development purposes.

---

## Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** 18.x or higher
- **Python** 3.10 or higher
- **Git** for version control
- **Code Editor** (VS Code recommended)

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/MuganziJames/terraguard-system.git
cd terraguard-system
```

---

## Frontend Setup (React + Vite)

### 1. Navigate to Frontend Directory

```bash
cd frontend
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Configure Environment Variables

Create a `.env` file in the `frontend` directory:

```env
VITE_API_URL=http://localhost:8000
VITE_SUPABASE_URL=your_supabase_project_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

**Note:** Replace the placeholder values with your actual credentials. Never commit `.env` files to version control.

### 4. Start Development Server

```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

### 5. Build for Production (Optional)

```bash
npm run build
```

---

## Backend Setup (FastAPI)

### 1. Navigate to Backend Directory

```bash
cd backend
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the `backend` directory:

```env
# Application
APP_NAME=Terraguard API
APP_VERSION=1.0.0
DEBUG=True
PORT=8000
HOST=0.0.0.0

# Database (Supabase)
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key

# AI Service (OpenRouter)
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=openai/gpt-5-mini

# Google Maps API
GOOGLE_MAPS_API_KEY=your_google_maps_api_key

# Telegram Bot (Optional for local testing)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

# Twilio (Optional for WhatsApp testing)
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Security
CRON_SECRET=any_random_string_for_local_dev
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Feature Flags
ENABLE_AI_CHAT=True
```

**Important:** 
- Never commit your `.env` file
- Keep all API keys secure
- Use test/sandbox credentials for local development

### 5. Start Development Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### 6. Access API Documentation

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## Telegram Bot Setup (Optional)

### 1. Create a Bot

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` and follow the instructions
3. Save your bot token (you'll need it for the `.env` file)

### 2. Run the Bot Locally

```bash
cd backend
python start_telegram_bot.py
```

The bot will start polling for messages.

---

## Database Setup (Supabase)

### 1. Create a Supabase Project

1. Go to [Supabase Dashboard](https://app.supabase.com/)
2. Click "New Project"
3. Choose a name and password
4. Wait for setup to complete

### 2. Create Database Tables

1. Go to **SQL Editor** in Supabase dashboard
2. Copy the SQL schema from `database_schema.sql`
3. Execute the SQL to create all required tables

### 3. Get API Credentials

1. Go to **Settings → API**
2. Copy your **Project URL** and **Anon Key**
3. Add them to your `.env` files

---

## Getting API Keys

### OpenRouter (AI Service)

1. Visit [OpenRouter](https://openrouter.ai/)
2. Sign up for an account
3. Go to [API Keys](https://openrouter.ai/keys)
4. Generate a new API key
5. Add credits to your account ($5 minimum recommended)

### Google Maps API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable **Geocoding API** and **Places API**
4. Go to **Credentials** → **Create Credentials** → **API Key**
5. Restrict the key to specific APIs (recommended)

### NASA POWER API

**Good news:** No API key required! NASA POWER API is completely free and open.

---

## Testing the Setup

### 1. Check Backend Health

```bash
curl http://localhost:8000/health
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

### 2. Test Frontend

1. Open `http://localhost:5173` in your browser
2. You should see the Terraguard home page
3. Check browser console for any errors

### 3. Test API from Frontend

1. The frontend should automatically connect to `http://localhost:8000`
2. Try using the AI chat or viewing alerts
3. Check network tab for API calls

---

## Common Issues

### Port Already in Use

**Frontend (5173):**
```bash
# Kill the process using port 5173
npx kill-port 5173
```

**Backend (8000):**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

### Module Not Found Errors

**Frontend:**
```bash
rm -rf node_modules package-lock.json
npm install
```

**Backend:**
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Database Connection Errors

1. Verify `SUPABASE_URL` and `SUPABASE_KEY` are correct
2. Check if tables are created in Supabase dashboard
3. Ensure your IP is not blocked (check Supabase dashboard)

### CORS Errors

1. Ensure `CORS_ORIGINS` in backend `.env` includes `http://localhost:5173`
2. Restart the backend server after changing `.env`

---

## Development Workflow

### Making Changes

1. **Frontend:** Changes hot-reload automatically
2. **Backend:** Server restarts automatically with `--reload` flag

### Testing

```bash
# Frontend
cd frontend
npm run test

# Backend
cd backend
pytest
```

### Code Formatting

**Frontend:**
```bash
npm run format
```

**Backend:**
```bash
black .
isort .
```

---

## Project Structure

```
terraguard-system/
├── frontend/
│   ├── src/
│   │   ├── components/    # Reusable UI components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API service layer
│   │   └── utils/         # Helper functions
│   └── .env              # Frontend environment variables
│
├── backend/
│   ├── app/
│   │   ├── routes/        # API endpoints
│   │   ├── services/      # Business logic
│   │   ├── models/        # Data models
│   │   ├── telegram/      # Telegram bot
│   │   └── whatsapp/      # WhatsApp integration
│   └── .env              # Backend environment variables
│
└── docs/                  # Documentation
```

---

## Environment Variables Security

**Important Security Practices:**

1. **Never commit `.env` files** to Git
2. Use `.env.example` for templates (without real values)
3. Use different API keys for development and production
4. Rotate API keys regularly
5. Use environment-specific configurations

### Create `.env.example` Files

**Frontend `.env.example`:**
```env
VITE_API_URL=http://localhost:8000
VITE_SUPABASE_URL=your_supabase_url_here
VITE_SUPABASE_ANON_KEY=your_supabase_key_here
```

**Backend `.env.example`:**
```env
APP_NAME=Terraguard API
DEBUG=True
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_key_here
OPENROUTER_API_KEY=your_openrouter_key_here
GOOGLE_MAPS_API_KEY=your_google_maps_key_here
```

---

## Next Steps

- Review [API Documentation](./API_DOCUMENTATION.md) for endpoint details
- Check [Architecture](./ARCHITECTURE.md) to understand system design
- See [Deployment Guide](./DEPLOYMENT.md) for production deployment

---

## Getting Help

- **GitHub Issues:** Report bugs or request features
- **Discussions:** Ask questions in GitHub Discussions
- **Documentation:** Check other docs in `/docs` folder

---

**Happy Coding!** 🚀
