/**
 * Database Setup Script for MYTA Waitlist
 * Run this to automatically create the waitlist tables
 */

import { createClient } from "@supabase/supabase-js";
import { readFileSync } from "fs";

// Load environment variables from .env.local
let supabaseUrl, supabaseKey;

try {
  const envFile = readFileSync(".env.local", "utf8");
  const envLines = envFile.split("\n");

  for (const line of envLines) {
    if (line.startsWith("VITE_SUPABASE_URL=")) {
      supabaseUrl = line.split("=")[1];
    }
    if (line.startsWith("VITE_SUPABASE_ANON_KEY=")) {
      supabaseKey = line.split("=")[1];
    }
  }
} catch (error) {
  console.error("❌ Could not read .env.local file");
}

if (!supabaseUrl || !supabaseKey) {
  console.error("❌ Missing Supabase environment variables");
  console.log(
    "Make sure VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY are set in .env.local"
  );
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseKey);

console.log("🗄️ Setting up MYTA waitlist database...\n");

const createWaitlistTable = `
-- Waitlist table - stores all waitlist signups
CREATE TABLE IF NOT EXISTS waitlist (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255),
    youtube_channel_name VARCHAR(255),
    youtube_channel_url TEXT,
    subscriber_count INTEGER,
    subscriber_range VARCHAR(50),
    content_niche VARCHAR(100),
    signup_source VARCHAR(100),
    referral_code VARCHAR(50),
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
    status VARCHAR(50) DEFAULT 'active',
    early_access_granted BOOLEAN DEFAULT FALSE,
    early_access_granted_at TIMESTAMP WITH TIME ZONE,
    converted_to_user BOOLEAN DEFAULT FALSE,
    converted_at TIMESTAMP WITH TIME ZONE,
    
    -- Metadata
    ip_address INET,
    user_agent TEXT,
    browser_info JSONB,
    device_info JSONB,
    location_data JSONB,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT valid_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'),
    CONSTRAINT valid_subscriber_range CHECK (subscriber_range IN ('0-1k', '1k-10k', '10k-100k', '100k-1M', '1M+', 'prefer_not_to_say')),
    CONSTRAINT valid_status CHECK (status IN ('active', 'invited', 'converted', 'unsubscribed'))
);
`;

const createIndexes = `
-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_waitlist_email ON waitlist(email);
CREATE INDEX IF NOT EXISTS idx_waitlist_status ON waitlist(status);
CREATE INDEX IF NOT EXISTS idx_waitlist_created_at ON waitlist(created_at);
CREATE INDEX IF NOT EXISTS idx_waitlist_signup_source ON waitlist(signup_source);
CREATE INDEX IF NOT EXISTS idx_waitlist_content_niche ON waitlist(content_niche);
CREATE INDEX IF NOT EXISTS idx_waitlist_subscriber_range ON waitlist(subscriber_range);
CREATE INDEX IF NOT EXISTS idx_waitlist_early_access ON waitlist(early_access_granted);
CREATE INDEX IF NOT EXISTS idx_waitlist_converted ON waitlist(converted_to_user);
`;

const createEmailEventsTable = `
-- Email engagement tracking table for detailed analytics
CREATE TABLE IF NOT EXISTS waitlist_email_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    waitlist_id UUID NOT NULL REFERENCES waitlist(id) ON DELETE CASCADE,
    event_type VARCHAR(50) NOT NULL,
    email_template VARCHAR(100),
    event_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT valid_event_type CHECK (event_type IN ('sent', 'delivered', 'opened', 'clicked', 'bounced', 'complained', 'unsubscribed'))
);
`;

const createEmailIndexes = `
-- Indexes for email events
CREATE INDEX IF NOT EXISTS idx_email_events_waitlist_id ON waitlist_email_events(waitlist_id);
CREATE INDEX IF NOT EXISTS idx_email_events_type ON waitlist_email_events(event_type);
CREATE INDEX IF NOT EXISTS idx_email_events_template ON waitlist_email_events(email_template);
CREATE INDEX IF NOT EXISTS idx_email_events_created_at ON waitlist_email_events(created_at);
`;

const createTrigger = `
-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_waitlist_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to automatically update updated_at
DROP TRIGGER IF EXISTS trigger_update_waitlist_updated_at ON waitlist;
CREATE TRIGGER trigger_update_waitlist_updated_at
    BEFORE UPDATE ON waitlist
    FOR EACH ROW
    EXECUTE FUNCTION update_waitlist_updated_at();
`;

async function setupDatabase() {
  try {
    console.log("1. Creating waitlist table...");
    const { error: tableError } = await supabase.rpc("exec_sql", {
      sql: createWaitlistTable,
    });
    if (tableError) throw tableError;
    console.log("✅ Waitlist table created");

    console.log("2. Creating indexes...");
    const { error: indexError } = await supabase.rpc("exec_sql", {
      sql: createIndexes,
    });
    if (indexError) throw indexError;
    console.log("✅ Indexes created");

    console.log("3. Creating email events table...");
    const { error: eventsError } = await supabase.rpc("exec_sql", {
      sql: createEmailEventsTable,
    });
    if (eventsError) throw eventsError;
    console.log("✅ Email events table created");

    console.log("4. Creating email indexes...");
    const { error: emailIndexError } = await supabase.rpc("exec_sql", {
      sql: createEmailIndexes,
    });
    if (emailIndexError) throw emailIndexError;
    console.log("✅ Email indexes created");

    console.log("5. Creating triggers...");
    const { error: triggerError } = await supabase.rpc("exec_sql", {
      sql: createTrigger,
    });
    if (triggerError) throw triggerError;
    console.log("✅ Triggers created");

    console.log("\n🎉 Database setup complete!");
    console.log("\nYour waitlist system is ready. Next steps:");
    console.log("1. Run: npm install");
    console.log("2. Run: npm run test");
    console.log("3. Deploy: vercel --prod");
  } catch (error) {
    console.error("❌ Database setup failed:", error.message);
    console.log("\n💡 Manual setup required:");
    console.log("1. Go to your Supabase Dashboard → SQL Editor");
    console.log(
      "2. Copy and paste the SQL from backend/database/migrations/create_waitlist_table.sql"
    );
    console.log("3. Run the SQL query");
  }
}

setupDatabase();
