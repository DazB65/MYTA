-- Content Cards Migration Script for Supabase
-- Run this in your Supabase SQL Editor

-- Create custom enum type for card status
-- This matches the statuses currently used in Firebase: 'ideas', 'planning', 'inProgress', 'ready'
CREATE TYPE card_status AS ENUM ('ideas', 'planning', 'inProgress', 'ready');

-- Create the content_cards table
-- This table will replace the Firebase 'content_cards' collection
CREATE TABLE content_cards (
  -- Primary key: UUID that auto-generates
  -- This replaces Firebase's document IDs
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- User identification (matches your existing user system)
  -- Links to the user who owns this content card
  user_id TEXT NOT NULL,
  
  -- Timestamps for tracking creation and modifications
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  
  -- Core content fields
  -- Title is required, description is optional
  title TEXT NOT NULL,
  description TEXT DEFAULT '',
  
  -- Status using our custom enum (matches current Firebase statuses)
  -- Defaults to 'ideas' for new cards
  status card_status DEFAULT 'ideas',
  
  -- Content pillars stored as JSON array
  -- This matches the current Firebase structure
  pillars JSONB DEFAULT '[]',
  
  -- Due date for scheduling content (optional)
  due_date DATE,
  
  -- Progress tracking stored as JSON object
  -- This matches the current Firebase progress structure
  progress JSONB,
  
  -- Soft delete flag instead of hard deletion
  -- This preserves data while hiding archived cards
  archived BOOLEAN DEFAULT FALSE,
  
  -- Order index for drag-and-drop functionality
  -- Higher numbers appear later in the list
  order_index INTEGER NOT NULL DEFAULT 0
);

-- Create indexes for better query performance
-- Index for querying cards by user and status (most common query)
CREATE INDEX idx_content_cards_user_status ON content_cards(user_id, status);

-- Index for ordering cards within columns
CREATE INDEX idx_content_cards_order ON content_cards(order_index);

-- Index for filtering out archived cards
CREATE INDEX idx_content_cards_archived ON content_cards(archived);

-- Index for user-specific queries
CREATE INDEX idx_content_cards_user_id ON content_cards(user_id);

-- Add trigger to automatically update the updated_at timestamp
-- This ensures updated_at is always current when a row is modified
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply the trigger to the content_cards table
CREATE TRIGGER content_cards_updated_at
  BEFORE UPDATE ON content_cards
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();

-- Optional: Add Row Level Security (RLS) for better security
-- This ensures users can only access their own content cards
ALTER TABLE content_cards ENABLE ROW LEVEL SECURITY;

-- Policy to allow users to see only their own cards
CREATE POLICY "Users can view their own cards" ON content_cards
  FOR SELECT USING (user_id = current_setting('app.current_user_id', true));

-- Policy to allow users to insert their own cards
CREATE POLICY "Users can insert their own cards" ON content_cards
  FOR INSERT WITH CHECK (user_id = current_setting('app.current_user_id', true));

-- Policy to allow users to update their own cards
CREATE POLICY "Users can update their own cards" ON content_cards
  FOR UPDATE USING (user_id = current_setting('app.current_user_id', true));

-- Policy to allow users to delete their own cards
CREATE POLICY "Users can delete their own cards" ON content_cards
  FOR DELETE USING (user_id = current_setting('app.current_user_id', true));

-- Insert a sample card for testing (optional)
-- Remove this section if you don't want test data
INSERT INTO content_cards (user_id, title, description, status, pillars, progress) VALUES 
(
  'test_user_id',
  'Sample Content Card',
  'This is a sample content card to test the migration',
  'ideas',
  '[{"name": "Tech Reviews", "icon": "⚡", "color": "from-blue-500 to-cyan-400"}]',
  '{"label": "Research", "value": 25, "check": false}'
);

-- Display success message
DO $$
BEGIN
  RAISE NOTICE 'Content Cards table created successfully!';
  RAISE NOTICE 'You can now proceed with the backend API implementation.';
END $$;