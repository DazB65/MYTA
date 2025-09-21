-- Performance Optimization Indexes
-- Migration: Add database indexes for frequently queried columns to improve performance

-- Users table indexes (only for existing columns)
-- Note: idx_users_created_at already exists
CREATE INDEX IF NOT EXISTS idx_users_updated_at ON users(updated_at);

-- Channel info indexes (frequently queried by user_id)
-- Note: These indexes already exist, but adding additional ones for performance
-- idx_channel_info_user_id, idx_channel_info_niche, idx_channel_info_subscriber_count,
-- idx_channel_info_monetization_status already exist

CREATE INDEX IF NOT EXISTS idx_channel_info_content_type ON channel_info(content_type);
CREATE INDEX IF NOT EXISTS idx_channel_info_upload_frequency ON channel_info(upload_frequency);
CREATE INDEX IF NOT EXISTS idx_channel_info_updated_at ON channel_info(updated_at);
CREATE INDEX IF NOT EXISTS idx_channel_info_video_count ON channel_info(video_count);
CREATE INDEX IF NOT EXISTS idx_channel_info_total_view_count ON channel_info(total_view_count);

-- Conversation history indexes (for chat functionality)
-- Note: These indexes already exist: idx_conversation_history_user_id,
-- idx_conversation_history_timestamp, idx_conversation_history_user_timestamp

CREATE INDEX IF NOT EXISTS idx_conversation_history_role ON conversation_history(role);

-- Insights indexes (for dashboard and notifications)
-- Note: These indexes already exist: idx_insights_user_id, idx_insights_type,
-- idx_insights_priority, idx_insights_is_read, idx_insights_created_at,
-- idx_insights_user_priority_created

-- Content pillars indexes
-- Note: idx_content_pillars_user_id already exists
CREATE INDEX IF NOT EXISTS idx_content_pillars_name ON content_pillars(name);
CREATE INDEX IF NOT EXISTS idx_content_pillars_created_at ON content_pillars(created_at);
CREATE INDEX IF NOT EXISTS idx_content_pillars_updated_at ON content_pillars(updated_at);

-- Video pillar allocations indexes (existing table)
CREATE INDEX IF NOT EXISTS idx_video_pillar_allocations_user_id ON video_pillar_allocations(user_id);
CREATE INDEX IF NOT EXISTS idx_video_pillar_allocations_video_id ON video_pillar_allocations(video_id);
CREATE INDEX IF NOT EXISTS idx_video_pillar_allocations_pillar_id ON video_pillar_allocations(pillar_id);
CREATE INDEX IF NOT EXISTS idx_video_pillar_allocations_allocation_type ON video_pillar_allocations(allocation_type);
CREATE INDEX IF NOT EXISTS idx_video_pillar_allocations_created_at ON video_pillar_allocations(created_at);
CREATE INDEX IF NOT EXISTS idx_video_pillar_allocations_updated_at ON video_pillar_allocations(updated_at);
CREATE INDEX IF NOT EXISTS idx_video_pillar_allocations_user_video ON video_pillar_allocations(user_id, video_id);

-- Composite indexes for common query patterns (only for existing columns)
-- Note: idx_insights_user_unread and idx_conversation_recent already exist

-- Analyze tables to update statistics after creating indexes
ANALYZE;

-- Vacuum to optimize database file
VACUUM;
