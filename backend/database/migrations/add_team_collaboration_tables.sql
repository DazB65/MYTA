-- Team Collaboration Database Schema
-- Migration: Add team management tables for MYTA collaboration features

-- Teams table - represents a team/workspace
CREATE TABLE IF NOT EXISTS teams (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    owner_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    subscription_id VARCHAR(255), -- Stripe subscription ID for team billing
    max_seats INTEGER DEFAULT 3, -- Maximum team members allowed
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Indexes
    CONSTRAINT teams_name_length CHECK (length(name) >= 1 AND length(name) <= 255)
);

-- Team members table - tracks who belongs to which team and their role
CREATE TABLE IF NOT EXISTS team_members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    team_id UUID NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL DEFAULT 'viewer',
    joined_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    invited_by UUID REFERENCES users(id),
    
    -- Constraints
    CONSTRAINT team_members_role_check CHECK (role IN ('owner', 'editor', 'viewer')),
    CONSTRAINT team_members_unique_user_team UNIQUE (team_id, user_id)
);

-- Team invitations table - manages pending invitations
CREATE TABLE IF NOT EXISTS team_invitations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    team_id UUID NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
    email VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'viewer',
    token VARCHAR(255) NOT NULL UNIQUE,
    invited_by UUID NOT NULL REFERENCES users(id),
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    accepted_at TIMESTAMP WITH TIME ZONE,
    declined_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT team_invitations_role_check CHECK (role IN ('editor', 'viewer')),
    CONSTRAINT team_invitations_email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    CONSTRAINT team_invitations_unique_pending UNIQUE (team_id, email) 
        DEFERRABLE INITIALLY DEFERRED -- Allow updates during acceptance
);

-- Add team_id to users table to track which team they belong to
ALTER TABLE users ADD COLUMN IF NOT EXISTS team_id UUID REFERENCES teams(id);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_teams_owner_id ON teams(owner_id);
CREATE INDEX IF NOT EXISTS idx_team_members_team_id ON team_members(team_id);
CREATE INDEX IF NOT EXISTS idx_team_members_user_id ON team_members(user_id);
CREATE INDEX IF NOT EXISTS idx_team_invitations_team_id ON team_invitations(team_id);
CREATE INDEX IF NOT EXISTS idx_team_invitations_email ON team_invitations(email);
CREATE INDEX IF NOT EXISTS idx_team_invitations_token ON team_invitations(token);
CREATE INDEX IF NOT EXISTS idx_team_invitations_expires_at ON team_invitations(expires_at);
CREATE INDEX IF NOT EXISTS idx_users_team_id ON users(team_id);

-- Function to automatically create team for new users with team subscription
CREATE OR REPLACE FUNCTION create_team_for_user()
RETURNS TRIGGER AS $$
BEGIN
    -- Only create team if user has team subscription and no team yet
    IF NEW.subscription_tier = 'team' AND NEW.team_id IS NULL THEN
        INSERT INTO teams (name, owner_id, max_seats)
        VALUES (NEW.name || '''s Team', NEW.id, 3)
        RETURNING id INTO NEW.team_id;
        
        -- Add user as team owner
        INSERT INTO team_members (team_id, user_id, role, invited_by)
        VALUES (NEW.team_id, NEW.id, 'owner', NEW.id);
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to auto-create team for team subscription users
CREATE TRIGGER trigger_create_team_for_user
    BEFORE INSERT OR UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION create_team_for_user();

-- Function to clean up expired invitations
CREATE OR REPLACE FUNCTION cleanup_expired_invitations()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM team_invitations 
    WHERE expires_at < NOW() 
    AND accepted_at IS NULL 
    AND declined_at IS NULL;
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Function to get team member count
CREATE OR REPLACE FUNCTION get_team_member_count(team_uuid UUID)
RETURNS INTEGER AS $$
BEGIN
    RETURN (
        SELECT COUNT(*) 
        FROM team_members 
        WHERE team_id = team_uuid
    );
END;
$$ LANGUAGE plpgsql;

-- Function to check if team has available seats
CREATE OR REPLACE FUNCTION team_has_available_seats(team_uuid UUID)
RETURNS BOOLEAN AS $$
DECLARE
    current_members INTEGER;
    max_allowed INTEGER;
BEGIN
    SELECT 
        get_team_member_count(team_uuid),
        max_seats
    INTO current_members, max_allowed
    FROM teams 
    WHERE id = team_uuid;
    
    RETURN current_members < max_allowed;
END;
$$ LANGUAGE plpgsql;

-- Views for easier querying
CREATE OR REPLACE VIEW team_members_with_details AS
SELECT 
    tm.id,
    tm.team_id,
    tm.user_id,
    tm.role,
    tm.joined_at,
    tm.invited_by,
    u.name as user_name,
    u.email as user_email,
    t.name as team_name,
    inviter.name as invited_by_name
FROM team_members tm
JOIN users u ON tm.user_id = u.id
JOIN teams t ON tm.team_id = t.id
LEFT JOIN users inviter ON tm.invited_by = inviter.id;

CREATE OR REPLACE VIEW pending_invitations AS
SELECT 
    ti.id,
    ti.team_id,
    ti.email,
    ti.role,
    ti.token,
    ti.expires_at,
    ti.created_at,
    t.name as team_name,
    inviter.name as invited_by_name,
    inviter.email as invited_by_email
FROM team_invitations ti
JOIN teams t ON ti.team_id = t.id
JOIN users inviter ON ti.invited_by = inviter.id
WHERE ti.accepted_at IS NULL 
AND ti.declined_at IS NULL 
AND ti.expires_at > NOW();

-- Grant permissions (adjust based on your user roles)
GRANT SELECT, INSERT, UPDATE, DELETE ON teams TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON team_members TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON team_invitations TO authenticated;
GRANT SELECT ON team_members_with_details TO authenticated;
GRANT SELECT ON pending_invitations TO authenticated;
GRANT EXECUTE ON FUNCTION cleanup_expired_invitations() TO authenticated;
GRANT EXECUTE ON FUNCTION get_team_member_count(UUID) TO authenticated;
GRANT EXECUTE ON FUNCTION team_has_available_seats(UUID) TO authenticated;

-- Comments for documentation
COMMENT ON TABLE teams IS 'Teams/workspaces for collaboration';
COMMENT ON TABLE team_members IS 'Users belonging to teams with their roles';
COMMENT ON TABLE team_invitations IS 'Pending invitations to join teams';
COMMENT ON COLUMN teams.max_seats IS 'Maximum number of team members allowed';
COMMENT ON COLUMN team_members.role IS 'User role: owner, editor, or viewer';
COMMENT ON COLUMN team_invitations.token IS 'Secure token for invitation acceptance';
