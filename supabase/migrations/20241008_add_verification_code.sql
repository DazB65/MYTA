-- Add verification_code column to users table
-- This allows users to verify their email with a 6-digit code in addition to the token

ALTER TABLE users ADD COLUMN IF NOT EXISTS verification_code TEXT;

-- Create index for verification_code lookups
CREATE INDEX IF NOT EXISTS idx_users_verification_code ON users(verification_code);

-- Add comment
COMMENT ON COLUMN users.verification_code IS '6-digit verification code sent via email';

