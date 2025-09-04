-- Optimized Video Storage Schema
-- Migration: Create efficient video storage with tiered caching strategy

-- Main videos table - stores core metadata for all videos
CREATE TABLE IF NOT EXISTS videos (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    user_id TEXT NOT NULL,
    youtube_video_id TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    published_at TIMESTAMP NOT NULL,
    duration INTEGER, -- in seconds
    thumbnail_url TEXT,
    
    -- Content categorization
    pillar_id TEXT,
    category TEXT,
    tags TEXT, -- JSON array of tags
    
    -- Cached basic metrics (updated periodically)
    view_count INTEGER DEFAULT 0,
    like_count INTEGER DEFAULT 0,
    comment_count INTEGER DEFAULT 0,
    share_count INTEGER DEFAULT 0,
    
    -- Performance indicators
    performance_score REAL DEFAULT 0, -- 0-100 calculated score
    performance_tier TEXT DEFAULT 'COLD', -- HOT, WARM, COLD
    engagement_rate REAL DEFAULT 0,
    
    -- Cache management
    last_synced TIMESTAMP,
    sync_priority INTEGER DEFAULT 3, -- 1=high, 2=medium, 3=low
    is_deleted BOOLEAN DEFAULT FALSE,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (pillar_id) REFERENCES content_pillars (id),
    UNIQUE(user_id, youtube_video_id)
);

-- Detailed analytics cache - stores comprehensive analytics for recent/important videos
CREATE TABLE IF NOT EXISTS video_analytics_cache (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    video_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    
    -- Detailed metrics
    watch_time_minutes REAL DEFAULT 0,
    average_view_duration REAL DEFAULT 0,
    retention_rate REAL DEFAULT 0,
    click_through_rate REAL DEFAULT 0,
    impressions INTEGER DEFAULT 0,
    
    -- Traffic sources (JSON)
    traffic_sources TEXT DEFAULT '[]', -- [{"name": "YouTube Search", "percentage": 45}]
    
    -- Demographics (JSON)
    top_countries TEXT DEFAULT '[]', -- [{"name": "United States", "percentage": 40}]
    age_demographics TEXT DEFAULT '[]',
    gender_demographics TEXT DEFAULT '[]',
    
    -- Revenue data
    estimated_revenue REAL DEFAULT 0,
    cpm REAL DEFAULT 0,
    
    -- Growth metrics
    views_growth_rate REAL DEFAULT 0,
    subscriber_gain INTEGER DEFAULT 0,
    
    -- Cache metadata
    cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    data_freshness TEXT DEFAULT 'fresh', -- fresh, stale, expired
    
    FOREIGN KEY (video_id) REFERENCES videos (id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users (id),
    UNIQUE(video_id)
);

-- Video sync queue - manages background synchronization
CREATE TABLE IF NOT EXISTS video_sync_queue (
    id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
    video_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    sync_type TEXT NOT NULL, -- 'basic', 'analytics', 'full'
    priority INTEGER DEFAULT 3, -- 1=urgent, 2=high, 3=normal, 4=low
    scheduled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    attempts INTEGER DEFAULT 0,
    max_attempts INTEGER DEFAULT 3,
    last_error TEXT,
    status TEXT DEFAULT 'pending', -- pending, processing, completed, failed
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (video_id) REFERENCES videos (id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Performance indexes for efficient queries
CREATE INDEX IF NOT EXISTS idx_videos_user_published ON videos(user_id, published_at DESC);
CREATE INDEX IF NOT EXISTS idx_videos_user_performance ON videos(user_id, performance_tier, performance_score DESC);
CREATE INDEX IF NOT EXISTS idx_videos_user_sync ON videos(user_id, last_synced ASC, sync_priority ASC);
CREATE INDEX IF NOT EXISTS idx_videos_pillar ON videos(pillar_id, performance_score DESC);
CREATE INDEX IF NOT EXISTS idx_videos_search ON videos(user_id, title, tags);

CREATE INDEX IF NOT EXISTS idx_analytics_cache_expires ON video_analytics_cache(expires_at, data_freshness);
CREATE INDEX IF NOT EXISTS idx_analytics_cache_user ON video_analytics_cache(user_id, cached_at DESC);

CREATE INDEX IF NOT EXISTS idx_sync_queue_priority ON video_sync_queue(status, priority ASC, scheduled_at ASC);
CREATE INDEX IF NOT EXISTS idx_sync_queue_user ON video_sync_queue(user_id, status);

-- Video performance view for quick analytics
CREATE VIEW IF NOT EXISTS video_performance_summary AS
SELECT 
    v.id,
    v.user_id,
    v.youtube_video_id,
    v.title,
    v.published_at,
    v.duration,
    v.view_count,
    v.like_count,
    v.comment_count,
    v.performance_score,
    v.performance_tier,
    v.engagement_rate,
    
    -- Analytics data (if cached)
    ac.retention_rate,
    ac.click_through_rate,
    ac.watch_time_minutes,
    ac.estimated_revenue,
    ac.views_growth_rate,
    
    -- Calculated fields
    CASE 
        WHEN v.view_count > 0 THEN (v.like_count + v.comment_count) * 100.0 / v.view_count 
        ELSE 0 
    END as engagement_percentage,
    
    CASE 
        WHEN ac.expires_at > datetime('now') THEN 'fresh'
        WHEN ac.expires_at IS NOT NULL THEN 'stale'
        ELSE 'no_analytics'
    END as analytics_status,
    
    julianday('now') - julianday(v.published_at) as days_since_published,
    julianday('now') - julianday(v.last_synced) as days_since_sync

FROM videos v
LEFT JOIN video_analytics_cache ac ON v.id = ac.video_id
WHERE v.is_deleted = FALSE;

-- Trigger to update video updated_at timestamp
CREATE TRIGGER IF NOT EXISTS update_videos_timestamp 
    AFTER UPDATE ON videos
    FOR EACH ROW
BEGIN
    UPDATE videos SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Trigger to clean up expired analytics cache
CREATE TRIGGER IF NOT EXISTS cleanup_expired_analytics
    AFTER INSERT ON video_analytics_cache
    FOR EACH ROW
BEGIN
    DELETE FROM video_analytics_cache 
    WHERE expires_at < datetime('now', '-7 days');
END;
