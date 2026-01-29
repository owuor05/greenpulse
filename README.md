# 🌍 Terraguard System

## Overview

Terraguard is a comprehensive full-stack climate resilience platform that combines a React web application with Telegram and WhatsApp bots to detect environmental risks, provide AI-powered conservation advice, and deliver real-time climate alerts to Kenyan communities. Our system integrates satellite climate data, AI natural language processing, and location intelligence to protect land and empower people across Kenya and beyond.

**🔗 Live Platform: [terraguard-system.vercel.app](https://terraguard-system.vercel.app/)**

> **NB:** Due to free tier usage, the system is deployed on different platforms such as Render, Railway, Vercel, and even utilizes UptimeBot to keep our servers awake. With WhatsApp, you might experience delays due to rate limiting, but as this is a new system, rate limiting may not affect you that much. On the web app the only issue might be google api key due to free tier may delay to suggest areas but don't worry even small areas eg matulo in bungoma county will still be geocoded well while searching for alerts in that area, when you just search "matulo". Thank you for your patience as we grow. Together, let's protect our land and secure our future. Tuchunge mazingira yetu!

## Solving Sustainable Development Goals

Terraguard addresses key UN Sustainable Development Goals:

- **🌱 SDG 13: Climate Action** - Monitoring, alerting, and education about climate risks
- **🌿 SDG 15: Life on Land** - Preventing land degradation through conservation practices
- **🌾 SDG 2: Zero Hunger** - Supporting sustainable agriculture and food security
- **💧 SDG 6: Clean Water** - Water conservation and drought/flood management 
- **🤝 SDG 17: Partnerships for the Goals** - Community-based environmental stewardship

## ✨ Features
### 📚 Educational Resources
Access to curated articles and guides about climate resilience, sustainable farming practices, land conservation techniques, and traditional environmental wisdom. Our educational content is designed to be practical and locally relevant for Kenyan communities.

### 👥 Community Reporting System
Users can submit real-time reports about local climate events (heavy rains, drought conditions, etc.) which are stored in our database. These community observations enhance our data collection and create a participatory approach to environmental monitoring - if people in Nairobi report heavy rainfall, this valuable ground-truth data complements our satellite information.

### 🔍 Climate Risk Detection
Leveraging NASA POWER API data to analyze climate patterns and detect risks like droughts, floods, and extreme temperatures. Our algorithms calculate 30-day rolling windows and anomalies to provide early warnings to communities.

### 🧠 AI-Powered Insights
Utilizing OpenRouter (GPT-5 mini) to generate practical, actionable insights from climate data. The AI assistant provides conservation advice, crop recommendations, and land management strategies in both English and Swahili.

### 📱 Multi-Channel Communication
Delivering climate alerts and educational content through multiple channels:
- **Web Interface**: Interactive risk map and dashboard
- **Telegram Bot**: Conversational AI assistant with location awareness
- **WhatsApp**: Twilio-powered messaging for widespread access

### 📊 Location Intelligence
Using Google Maps API for precise geocoding and location-based climate analysis. Our location caching system reduces API costs by 80% while maintaining accurate region-specific alerts.

### 🌱 Land Conservation Focus
Every interaction with Terraguard emphasizes land conservation, soil protection, and sustainable practices. The system promotes tree planting, erosion prevention, and community environmental stewardship.

### 🔄 Real-Time Alerts
Automated detection and distribution of alerts about imminent climate risks, with personalized recommendations based on location and conditions.


## 🤖 AI Assistant Demo

Here's how a conversation with the Terraguard AI assistant works:

```
User: Hello, I'm a farmer in Kitui. What crops should I plant?

Terraguard: Hello farmer from Kitui! 👋 

For your semi-arid region, I recommend these drought-resistant crops:

1. Sorghum - Thrives in low rainfall and poor soils
2. Cowpeas - Fixes nitrogen and needs little water
3. Green grams (mung beans) - Short growing season
4. Cassava - Tolerates drought once established
5. Pigeon peas - Deep roots access moisture

Consider intercropping legumes with cereals to improve soil fertility. Also, implement water harvesting techniques like zai pits or half-moon basins to maximize rainfall retention.

Remember: "Mmea moja, linda udongo wako" - Plant one tree, save your soil! 🌱
```

```
User: I'm worried about drought. What should I do?

Terraguard: I understand your concern about drought in Kitui. Here are practical steps to prepare:

WATER CONSERVATION:
• Dig water harvesting structures now (zai pits, terraces)
• Mulch around plants to retain soil moisture
• Consider drip irrigation for efficient water use

LAND PROTECTION:
• Plant drought-resistant trees like Acacia and Melia volkensii
• Create contour bunds to prevent soil erosion
• Use cover crops to protect topsoil

FARMING ADAPTATIONS:
• Switch to early-maturing crop varieties
• Practice conservation agriculture (minimal tillage)
• Space plants farther apart to reduce competition

Remember to listen for weather updates on local radio. Working with neighbors on community-based conservation makes everyone more resilient!

Would you like specific crop recommendations for this dry season?
```

## 📱 Access Terraguard

### Web Application
Visit our interactive platform at [terraguard-system.vercel.app](https://terraguard-system.vercel.app/)

### Telegram Bot
Start a conversation with [@TerraguardBot](https://t.me/TerraGuard_Bot) on Telegram

### WhatsApp (Sandbox)
To join our WhatsApp sandbox:
1. Send a WhatsApp message to: **+1 415 523 8886** with code `join actual-mother`
2. Once connected, you can ask questions about climate, farming, and land conservation
3. Share your location to receive personalized alerts and recommendations

## � Technical Stack & APIs

### 🌐 Core Technologies
- **Frontend**: React 18.3, Vite 5.4, Tailwind CSS 3.4
- **Backend**: FastAPI 0.115, Python 3.10+
- **Database**: Supabase (PostgreSQL)
- **Hosting**: Vercel (frontend), Render (API), Railway (Telegram bot)

### 📡 External APIs & Services
- **NASA POWER API**: Provides climate data for drought and flood risk detection, including temperature, rainfall, and soil moisture metrics
- **Google Maps API**: Handles geocoding (converting location names to coordinates) and reverse geocoding (coordinates to locations) for precise regional alerts
- **OpenRouter AI**: Powers our AI assistant using GPT-5 mini model for natural language understanding and generation in both English and Swahili
- **Twilio API**: Enables WhatsApp messaging for alerts and conversation with users without smartphones
- **Telegram Bot API**: Manages real-time climate assistant conversations through the messaging platform

### ⏱️ Automated Processes
- **Risk Detection Cron Job**: Runs every 6 hours to analyze climate data across all monitored regions
- **Daily Alert Distribution**: Scheduled job that runs at 7 AM EAT to send morning alerts to subscribed users
- **Alert Cleanup**: Automatically removes expired alerts to keep the database optimized

### 🔐 Location Caching System
Our proprietary location caching system reduces Google Maps API costs by 80% by storing coordinates for all 47 Kenyan counties and major cities, enabling instant location lookup without repeated API calls.

## �📚 Documentation

For detailed information about the system, check out our documentation:

- [API Documentation](./docs/API_DOCUMENTATION.md) - Endpoints and usage guides
- [Architecture](./docs/ARCHITECTURE.md) - System design and components
- [Deployment Guide](./docs/DEPLOYMENT.md) - How the system is deployed
- [Local Development](./docs/LOCAL_DEVELOPMENT.md) - Setting up for development

## 🌍 Making a Difference

Terraguard combines cutting-edge AI with practical conservation knowledge to empower communities facing climate challenges. By providing timely alerts and actionable advice, we help protect land, improve agricultural resilience, and preserve natural resources.

Our mission: **"Guard the land. Mazingira yetu ni urithi wetu."**

## 👥 Team

- [MuganziJames](https://github.com/MuganziJames) - Lead Developer
- Contributors welcome! Join us in our mission to combat land degradation in Kenya.

## 📝 License

Copyright © 2025 Terraguard Team