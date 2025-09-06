-- Waitlist Database Schema
-- Migration: Create waitlist table for MYTA email capture and management

-- Waitlist table - stores all waitlist signups
CREATE TABLE IF NOT EXISTS waitlist (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255),
    youtube_channel_name VARCHAR(255),
    youtube_channel_url TEXT,
    subscriber_count INTEGER,
    subscriber_range VARCHAR(50), -- '0-1k', '1k-10k', '10k-100k', '100k-1M', '1M+'
    content_niche VARCHAR(100), -- 'gaming', 'education', 'lifestyle', 'tech', 'business', etc.
    signup_source VARCHAR(100), -- 'landing_page', 'social_media', 'referral', etc.
    referral_code VARCHAR(50), -- for tracking referrals
    utm_source VARCHAR(100),
    utm_medium VARCHAR(100),
    utm_campaign VARCHAR(100),
    
    -- Email engagement tracking
    welcome_email_sent BOOLEAN DEFAULT FALSE,
    welcome_email_sent_at TIMESTAMP WITH TIME ZONE,
    last_email_sent_at TIMESTAMP WITH TIME ZONE,
    email_opens INTEGER DEFAULT 0,
    email_clicks INTEGER DEFAULT 0,
    unsubscribed BOOLEAN DEFAULT FALSE,
    unsubscribed_at TIMESTAMP WITH TIME ZONE,
    
    -- Status tracking
    status VARCHAR(50) DEFAULT 'active', -- 'active', 'invited', 'converted', 'unsubscribed'
    early_access_granted BOOLEAN DEFAULT FALSE,
    early_access_granted_at TIMESTAMP WITH TIME ZONE,
    converted_to_user BOOLEAN DEFAULT FALSE,
    converted_at TIMESTAMP WITH TIME ZONE,
    
    -- Metadata
    ip_address INET,
    user_agent TEXT,
    browser_info JSONB,
    device_info JSONB,
    location_data JSONB, -- country, city, timezone
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT valid_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    CONSTRAINT valid_subscriber_range CHECK (subscriber_range IN ('0-1k', '1k-10k', '10k-100k', '100k-1M', '1M+', 'prefer_not_to_say')),
    CONSTRAINT valid_status CHECK (status IN ('active', 'invited', 'converted', 'unsubscribed'))
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_waitlist_email ON waitlist(email);
CREATE INDEX IF NOT EXISTS idx_waitlist_status ON waitlist(status);
CREATE INDEX IF NOT EXISTS idx_waitlist_created_at ON waitlist(created_at);
CREATE INDEX IF NOT EXISTS idx_waitlist_signup_source ON waitlist(signup_source);
CREATE INDEX IF NOT EXISTS idx_waitlist_content_niche ON waitlist(content_niche);
CREATE INDEX IF NOT EXISTS idx_waitlist_subscriber_range ON waitlist(subscriber_range);
CREATE INDEX IF NOT EXISTS idx_waitlist_early_access ON waitlist(early_access_granted);
CREATE INDEX IF NOT EXISTS idx_waitlist_converted ON waitlist(converted_to_user);

-- Email engagement tracking table for detailed analytics
CREATE TABLE IF NOT EXISTS waitlist_email_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    waitlist_id UUID NOT NULL REFERENCES waitlist(id) ON DELETE CASCADE,
    event_type VARCHAR(50) NOT NULL, -- 'sent', 'delivered', 'opened', 'clicked', 'bounced', 'complained'
    email_template VARCHAR(100), -- 'welcome', 'update_1', 'early_access', etc.
    event_data JSONB, -- additional event metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT valid_event_type CHECK (event_type IN ('sent', 'delivered', 'opened', 'clicked', 'bounced', 'complained', 'unsubscribed'))
);

-- Indexes for email events
CREATE INDEX IF NOT EXISTS idx_email_events_waitlist_id ON waitlist_email_events(waitlist_id);
CREATE INDEX IF NOT EXISTS idx_email_events_type ON waitlist_email_events(event_type);
CREATE INDEX IF NOT EXISTS idx_email_events_template ON waitlist_email_events(email_template);
CREATE INDEX IF NOT EXISTS idx_email_events_created_at ON waitlist_email_events(created_at);

-- Waitlist analytics view for easy reporting
CREATE OR REPLACE VIEW waitlist_analytics AS
SELECT 
    DATE_TRUNC('day', created_at) as signup_date,
    COUNT(*) as total_signups,
    COUNT(*) FILTER (WHERE welcome_email_sent = true) as welcome_emails_sent,
    COUNT(*) FILTER (WHERE early_access_granted = true) as early_access_granted,
    COUNT(*) FILTER (WHERE converted_to_user = true) as converted_users,
    COUNT(*) FILTER (WHERE unsubscribed = true) as unsubscribed,
    signup_source,
    content_niche,
    subscriber_range
FROM waitlist 
GROUP BY DATE_TRUNC('day', created_at), signup_source, content_niche, subscriber_range
ORDER BY signup_date DESC;

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_waitlist_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to automatically update updated_at
CREATE TRIGGER trigger_update_waitlist_updated_at
    BEFORE UPDATE ON waitlist
    FOR EACH ROW
    EXECUTE FUNCTION update_waitlist_updated_at();
