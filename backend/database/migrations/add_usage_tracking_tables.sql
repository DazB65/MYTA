-- Usage Tracking Database Schema
-- Migration: Add comprehensive usage tracking for MYTA subscription limits

-- Usage tracking table - tracks all user/team usage
CREATE TABLE IF NOT EXISTS usage_tracking (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    user_id TEXT NOT NULL,
    team_id TEXT,
    usage_type TEXT NOT NULL,
    amount INTEGER DEFAULT 1,
    cost_estimate REAL DEFAULT 0.0,
    metadata TEXT DEFAULT '{}',
    period_start TEXT NOT NULL,
    period_end TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now'))
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_usage_tracking_user_period ON usage_tracking(user_id, period_start, period_end);
CREATE INDEX IF NOT EXISTS idx_usage_tracking_team_period ON usage_tracking(team_id, period_start, period_end);
CREATE INDEX IF NOT EXISTS idx_usage_tracking_type ON usage_tracking(usage_type);
CREATE INDEX IF NOT EXISTS idx_usage_tracking_created ON usage_tracking(created_at);

-- Usage limits table - defines limits per subscription plan
CREATE TABLE IF NOT EXISTS usage_limits (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    plan_id TEXT NOT NULL,
    usage_type TEXT NOT NULL,
    limit_amount INTEGER NOT NULL, -- -1 for unlimited
    reset_period TEXT DEFAULT 'monthly', -- monthly, yearly, daily
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),

    -- Ensure unique limits per plan/type
    UNIQUE (plan_id, usage_type)
);

-- Usage summaries table - aggregated usage data for performance
CREATE TABLE IF NOT EXISTS usage_summaries (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    user_id TEXT NOT NULL,
    team_id TEXT,
    usage_type TEXT NOT NULL,
    total_amount INTEGER NOT NULL,
    total_cost REAL DEFAULT 0.0,
    period_start TEXT NOT NULL,
    period_end TEXT NOT NULL,
    last_updated TEXT DEFAULT (datetime('now')),

    -- Ensure unique summaries per user/team/type/period
    UNIQUE (user_id, team_id, usage_type, period_start, period_end)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_usage_summaries_user_period ON usage_summaries(user_id, period_start, period_end);
CREATE INDEX IF NOT EXISTS idx_usage_summaries_team_period ON usage_summaries(team_id, period_start, period_end);

-- Usage alerts table - track when users approach limits
CREATE TABLE IF NOT EXISTS usage_alerts (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    user_id TEXT NOT NULL,
    team_id TEXT,
    usage_type TEXT NOT NULL,
    alert_type TEXT NOT NULL, -- warning, limit_reached, overage
    current_usage INTEGER NOT NULL,
    usage_limit INTEGER NOT NULL,
    percentage_used REAL NOT NULL,
    message TEXT,
    is_read INTEGER DEFAULT 0, -- SQLite uses INTEGER for boolean
    created_at TEXT DEFAULT (datetime('now'))
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_usage_alerts_user ON usage_alerts(user_id);
CREATE INDEX IF NOT EXISTS idx_usage_alerts_team ON usage_alerts(team_id);
CREATE INDEX IF NOT EXISTS idx_usage_alerts_unread ON usage_alerts(is_read, created_at);

-- Insert default usage limits for new three-tier plans
INSERT OR REPLACE INTO usage_limits (plan_id, usage_type, limit_amount, reset_period) VALUES
-- Solo Creator Plan Limits ($4.99)
('solo', 'ai_conversations', 25, 'monthly'),
('solo', 'video_analysis', 5, 'monthly'),
('solo', 'research_projects', 3, 'monthly'),
('solo', 'goals', 3, 'monthly'),
('solo', 'tasks', 25, 'monthly'),
('solo', 'team_members', 1, 'monthly'),
('solo', 'content_pillars', 10, 'monthly'), -- limited to 10

-- Solo Pro Plan Limits ($14.99)
('solo_pro', 'ai_conversations', 100, 'monthly'),
('solo_pro', 'video_analysis', 25, 'monthly'),
('solo_pro', 'research_projects', -1, 'monthly'), -- unlimited
('solo_pro', 'goals', -1, 'monthly'), -- unlimited
('solo_pro', 'tasks', -1, 'monthly'), -- unlimited
('solo_pro', 'team_members', 1, 'monthly'),
('solo_pro', 'content_pillars', -1, 'monthly'), -- unlimited

-- Teams Plan Limits ($29.99 + per seat)
('teams', 'ai_conversations', 250, 'monthly'),
('teams', 'video_analysis', 50, 'monthly'),
('teams', 'research_projects', -1, 'monthly'), -- unlimited
('teams', 'goals', -1, 'monthly'), -- unlimited
('teams', 'tasks', -1, 'monthly'), -- unlimited
('teams', 'team_members', 20, 'monthly'), -- max team size
('teams', 'content_pillars', -1, 'monthly'); -- unlimited

-- SQLite doesn't support stored procedures, so we'll handle this in the application code
-- The usage tracking service will manage billing periods and summary updates
