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

CREATE INDEX IF NOT EXISTS idx_usage_tracking_user_period ON usage_tracking(user_id, period_start, period_end);
CREATE INDEX IF NOT EXISTS idx_usage_tracking_team_period ON usage_tracking(team_id, period_start, period_end);
CREATE INDEX IF NOT EXISTS idx_usage_tracking_type ON usage_tracking(usage_type);
CREATE INDEX IF NOT EXISTS idx_usage_tracking_created ON usage_tracking(created_at);

CREATE TABLE IF NOT EXISTS usage_limits (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    plan_id TEXT NOT NULL,
    usage_type TEXT NOT NULL,
    limit_amount INTEGER NOT NULL,
    reset_period TEXT DEFAULT 'monthly',
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    UNIQUE (plan_id, usage_type)
);

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
    UNIQUE (user_id, team_id, usage_type, period_start, period_end)
);

CREATE INDEX IF NOT EXISTS idx_usage_summaries_user_period ON usage_summaries(user_id, period_start, period_end);
CREATE INDEX IF NOT EXISTS idx_usage_summaries_team_period ON usage_summaries(team_id, period_start, period_end);

CREATE TABLE IF NOT EXISTS usage_alerts (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    user_id TEXT NOT NULL,
    team_id TEXT,
    usage_type TEXT NOT NULL,
    alert_type TEXT NOT NULL,
    current_usage INTEGER NOT NULL,
    usage_limit INTEGER NOT NULL,
    percentage_used REAL NOT NULL,
    message TEXT,
    is_read INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_usage_alerts_user ON usage_alerts(user_id);
CREATE INDEX IF NOT EXISTS idx_usage_alerts_team ON usage_alerts(team_id);
CREATE INDEX IF NOT EXISTS idx_usage_alerts_unread ON usage_alerts(is_read, created_at);

INSERT OR REPLACE INTO usage_limits (plan_id, usage_type, limit_amount, reset_period) VALUES
('solo', 'ai_conversations', 25, 'monthly'),
('solo', 'video_analysis', 5, 'monthly'),
('solo', 'research_projects', 3, 'monthly'),
('solo', 'goals', 3, 'monthly'),
('solo', 'tasks', 25, 'monthly'),
('solo', 'team_members', 1, 'monthly'),
('solo', 'content_pillars', -1, 'monthly'),
('team', 'ai_conversations', 100, 'monthly'),
('team', 'video_analysis', 25, 'monthly'),
('team', 'research_projects', -1, 'monthly'),
('team', 'goals', -1, 'monthly'),
('team', 'tasks', -1, 'monthly'),
('team', 'team_members', 10, 'monthly'),
('team', 'content_pillars', -1, 'monthly');
