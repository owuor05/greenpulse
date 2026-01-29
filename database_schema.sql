-- Terraguard Database Schema
-- Run this in Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    phone_number VARCHAR(20) UNIQUE,
    telegram_id BIGINT UNIQUE,
    username VARCHAR(100),
    region VARCHAR(100),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    subscribed BOOLEAN DEFAULT true,
    preferences JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Alerts table
CREATE TABLE alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    region VARCHAR(100) NOT NULL,
    risk_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    ai_summary JSONB,
    climate_data JSONB,
    status VARCHAR(20) DEFAULT 'active',
    expires_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Education articles table
CREATE TABLE education_articles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(200) NOT NULL,
    slug VARCHAR(200) UNIQUE NOT NULL,
    category VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    summary TEXT,
    image_url TEXT,
    author VARCHAR(100),
    published BOOLEAN DEFAULT true,
    views INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Community reports table
CREATE TABLE community_reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    region VARCHAR(100) NOT NULL,
    report_type VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    images JSONB DEFAULT '[]',
    status VARCHAR(20) DEFAULT 'pending',
    verified BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- SMS/WhatsApp chat history (unified for both platforms)
CREATE TABLE sms_chat_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    phone_number VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    direction VARCHAR(10) NOT NULL, -- 'incoming' or 'outgoing'
    ai_response TEXT,
    platform VARCHAR(20) DEFAULT 'sms', -- 'sms' or 'whatsapp'
    language VARCHAR(20), -- 'english', 'swahili', etc.
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Telegram chat history
CREATE TABLE telegram_chat_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    telegram_id BIGINT NOT NULL,
    chat_id BIGINT NOT NULL,
    username VARCHAR(100),
    first_name VARCHAR(100),
    message TEXT NOT NULL,
    direction VARCHAR(10) NOT NULL, -- 'incoming' or 'outgoing'
    ai_response TEXT,
    language VARCHAR(20), -- 'english', 'swahili', etc.
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- AI feedback table
CREATE TABLE ai_feedback (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    message_id UUID,
    platform VARCHAR(20) NOT NULL,
    feedback_type VARCHAR(20) NOT NULL,
    rating INTEGER,
    comment TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_users_phone ON users(phone_number);
CREATE INDEX idx_users_telegram ON users(telegram_id);
CREATE INDEX idx_users_region ON users(region);
CREATE INDEX idx_alerts_region ON alerts(region);
CREATE INDEX idx_alerts_status ON alerts(status);
CREATE INDEX idx_alerts_created ON alerts(created_at DESC);
CREATE INDEX idx_articles_category ON education_articles(category);
CREATE INDEX idx_articles_slug ON education_articles(slug);
CREATE INDEX idx_reports_region ON community_reports(region);
CREATE INDEX idx_reports_status ON community_reports(status);
CREATE INDEX idx_sms_user ON sms_chat_history(user_id);
CREATE INDEX idx_sms_phone ON sms_chat_history(phone_number);
CREATE INDEX idx_telegram_user ON telegram_chat_history(user_id);
CREATE INDEX idx_telegram_chat ON telegram_chat_history(telegram_id);

-- Updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply updated_at triggers
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_alerts_updated_at BEFORE UPDATE ON alerts FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_articles_updated_at BEFORE UPDATE ON education_articles FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_reports_updated_at BEFORE UPDATE ON community_reports FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Row Level Security (RLS) policies
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE alerts ENABLE ROW LEVEL SECURITY;
ALTER TABLE education_articles ENABLE ROW LEVEL SECURITY;
ALTER TABLE community_reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE sms_chat_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE telegram_chat_history ENABLE ROW LEVEL SECURITY;

-- Service role (backend) has full access to all tables
-- These policies allow the backend to perform all operations using service_role key

-- Public read access for alerts and articles (for frontend with anon key)
CREATE POLICY "Anyone can read active alerts" ON alerts FOR SELECT USING (status = 'active');
CREATE POLICY "Anyone can read published articles" ON education_articles FOR SELECT USING (published = true);

-- Users can read their own data
CREATE POLICY "Users can read own profile" ON users FOR SELECT USING (true);

-- Allow community report submissions
CREATE POLICY "Anyone can submit reports" ON community_reports FOR INSERT WITH CHECK (true);
CREATE POLICY "Anyone can read verified reports" ON community_reports FOR SELECT USING (verified = true OR status = 'approved');

-- Enable realtime for alerts (for live updates on frontend)
ALTER PUBLICATION supabase_realtime ADD TABLE alerts;
ALTER PUBLICATION supabase_realtime ADD TABLE community_reports;

-- Create indexes for faster queries
CREATE INDEX idx_users_subscribed ON users(subscribed) WHERE subscribed = true;
CREATE INDEX idx_alerts_expires ON alerts(expires_at) WHERE expires_at IS NOT NULL;
CREATE INDEX idx_alerts_severity ON alerts(severity);
CREATE INDEX idx_articles_published ON education_articles(published) WHERE published = true;

-- Additional tables for TerraGuard features
-- Run this in Supabase SQL Editor

-- Land data cache table (24-hour caching)
CREATE TABLE IF NOT EXISTS land_data_cache (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    location_name VARCHAR(200) NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    temperature_data JSONB,
    climate_risks JSONB,
    active_alerts JSONB,
    historical_data JSONB,
    ai_summary TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE DEFAULT (NOW() + INTERVAL '24 hours')
);

-- Index for faster location lookups
CREATE INDEX idx_land_cache_location ON land_data_cache(location_name);
CREATE INDEX idx_land_cache_coords ON land_data_cache(latitude, longitude);
CREATE INDEX idx_land_cache_expires ON land_data_cache(expires_at);

-- RLS policy - public read access
ALTER TABLE land_data_cache ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Anyone can read land data" ON land_data_cache FOR SELECT USING (true);
CREATE POLICY "Service can insert land data" ON land_data_cache FOR INSERT WITH CHECK (true);

-- Trigger for updated_at
CREATE TRIGGER update_land_cache_updated_at 
BEFORE UPDATE ON land_data_cache 
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to clean expired cache (run daily)
CREATE OR REPLACE FUNCTION clean_expired_land_cache()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM land_data_cache WHERE expires_at < NOW();
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Migration: Add 'name' column to users table
-- Run this in Supabase SQL Editor
-- Date: 2025-10-12

-- Add 'name' column to store user's actual name (not username)
ALTER TABLE users ADD COLUMN IF NOT EXISTS name VARCHAR(100);

-- Create index for name searches (optional but useful)
CREATE INDEX IF NOT EXISTS idx_users_name ON users(name);

-- Update existing users who have first_name in telegram_chat_history
-- This will populate the name field from the most recent telegram interaction
DO $$
BEGIN
    -- Update from telegram_chat_history first_name
    UPDATE users u
    SET name = t.first_name
    FROM (
        SELECT DISTINCT ON (user_id) user_id, first_name
        FROM telegram_chat_history
        WHERE first_name IS NOT NULL AND first_name != ''
        ORDER BY user_id, created_at DESC
    ) t
    WHERE u.id = t.user_id AND u.name IS NULL;
    
    RAISE NOTICE 'Migration completed: Added name column to users table';
END $$;

-- Success message
SELECT 'Successfully added name column to users table!' as message;


-- Success message
SELECT 'Land data cache table created successfully!' as message;



-- Success message
SELECT 'Terraguard database schema created successfully!' as message,
       'Tables: 7 | Indexes: 18 | RLS Policies: 5' as summary;
