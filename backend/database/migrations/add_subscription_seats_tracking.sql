-- Subscription Seats Tracking Database Schema
-- Migration: Add seat management for Teams subscriptions

-- Subscription seats table - tracks seat purchases and usage
CREATE TABLE IF NOT EXISTS subscription_seats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    subscription_id VARCHAR(255) NOT NULL, -- LemonSqueezy subscription ID
    plan_id VARCHAR(50) NOT NULL, -- teams, solo_pro, etc.
    total_seats INTEGER NOT NULL DEFAULT 1,
    used_seats INTEGER NOT NULL DEFAULT 1,
    seat_price_monthly DECIMAL(10,2) NOT NULL DEFAULT 9.99,
    seat_price_yearly DECIMAL(10,2) NOT NULL DEFAULT 99.99,
    billing_cycle VARCHAR(20) NOT NULL DEFAULT 'monthly',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT subscription_seats_total_check CHECK (total_seats >= 1 AND total_seats <= 20),
    CONSTRAINT subscription_seats_used_check CHECK (used_seats >= 1 AND used_seats <= total_seats),
    CONSTRAINT subscription_seats_billing_check CHECK (billing_cycle IN ('monthly', 'yearly')),
    CONSTRAINT subscription_seats_plan_check CHECK (plan_id IN ('solo', 'solo_pro', 'teams')),
    CONSTRAINT subscription_seats_unique_user UNIQUE (user_id, subscription_id)
);

-- Seat transactions table - tracks seat additions/removals
CREATE TABLE IF NOT EXISTS seat_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subscription_seats_id UUID NOT NULL REFERENCES subscription_seats(id) ON DELETE CASCADE,
    transaction_type VARCHAR(20) NOT NULL, -- 'add', 'remove'
    seats_changed INTEGER NOT NULL,
    old_total_seats INTEGER NOT NULL,
    new_total_seats INTEGER NOT NULL,
    cost_change DECIMAL(10,2) NOT NULL, -- Positive for additions, negative for removals
    effective_date TIMESTAMP WITH TIME ZONE NOT NULL,
    lemonsqueezy_order_id VARCHAR(255), -- LemonSqueezy order ID for the transaction
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT seat_transactions_type_check CHECK (transaction_type IN ('add', 'remove')),
    CONSTRAINT seat_transactions_seats_positive CHECK (seats_changed > 0),
    CONSTRAINT seat_transactions_totals_check CHECK (old_total_seats >= 1 AND new_total_seats >= 1)
);

-- Update teams table to reference subscription_seats
ALTER TABLE teams ADD COLUMN IF NOT EXISTS subscription_seats_id UUID REFERENCES subscription_seats(id);

-- Function to update used_seats when team members change
CREATE OR REPLACE FUNCTION update_subscription_seats_usage()
RETURNS TRIGGER AS $$
DECLARE
    team_record RECORD;
    member_count INTEGER;
BEGIN
    -- Get team and subscription info
    IF TG_OP = 'DELETE' THEN
        SELECT t.*, ss.id as seats_id INTO team_record
        FROM teams t
        LEFT JOIN subscription_seats ss ON t.subscription_seats_id = ss.id
        WHERE t.id = OLD.team_id;
        
        -- Count remaining members after deletion
        SELECT COUNT(*) INTO member_count
        FROM team_members 
        WHERE team_id = OLD.team_id AND id != OLD.id;
    ELSE
        SELECT t.*, ss.id as seats_id INTO team_record
        FROM teams t
        LEFT JOIN subscription_seats ss ON t.subscription_seats_id = ss.id
        WHERE t.id = NEW.team_id;
        
        -- Count current members
        SELECT COUNT(*) INTO member_count
        FROM team_members 
        WHERE team_id = NEW.team_id;
    END IF;
    
    -- Update used_seats if subscription_seats exists
    IF team_record.seats_id IS NOT NULL THEN
        UPDATE subscription_seats 
        SET used_seats = member_count,
            updated_at = NOW()
        WHERE id = team_record.seats_id;
    END IF;
    
    IF TG_OP = 'DELETE' THEN
        RETURN OLD;
    ELSE
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Triggers to update seat usage
CREATE TRIGGER trigger_update_seats_on_member_add
    AFTER INSERT ON team_members
    FOR EACH ROW
    EXECUTE FUNCTION update_subscription_seats_usage();

CREATE TRIGGER trigger_update_seats_on_member_remove
    AFTER DELETE ON team_members
    FOR EACH ROW
    EXECUTE FUNCTION update_subscription_seats_usage();

-- Function to calculate total subscription cost including seats
CREATE OR REPLACE FUNCTION calculate_subscription_cost(seats_record_id UUID)
RETURNS DECIMAL(10,2) AS $$
DECLARE
    seats_record subscription_seats%ROWTYPE;
    base_cost DECIMAL(10,2);
    additional_seats INTEGER;
    seat_cost DECIMAL(10,2);
    total_cost DECIMAL(10,2);
BEGIN
    SELECT * INTO seats_record FROM subscription_seats WHERE id = seats_record_id;
    
    IF NOT FOUND THEN
        RETURN 0;
    END IF;
    
    -- Base costs for different plans
    CASE seats_record.plan_id
        WHEN 'solo' THEN
            base_cost := CASE WHEN seats_record.billing_cycle = 'yearly' THEN 49.99 ELSE 4.99 END;
        WHEN 'solo_pro' THEN
            base_cost := CASE WHEN seats_record.billing_cycle = 'yearly' THEN 149.99 ELSE 14.99 END;
        WHEN 'teams' THEN
            base_cost := CASE WHEN seats_record.billing_cycle = 'yearly' THEN 299.99 ELSE 29.99 END;
        ELSE
            base_cost := 0;
    END CASE;
    
    -- Calculate additional seat cost (first seat included in base for teams plan)
    IF seats_record.plan_id = 'teams' THEN
        additional_seats := GREATEST(0, seats_record.total_seats - 1);
        seat_cost := CASE WHEN seats_record.billing_cycle = 'yearly' 
                     THEN seats_record.seat_price_yearly 
                     ELSE seats_record.seat_price_monthly END;
        total_cost := base_cost + (additional_seats * seat_cost);
    ELSE
        total_cost := base_cost;
    END IF;
    
    RETURN total_cost;
END;
$$ LANGUAGE plpgsql;

-- Function to check if seats can be added
CREATE OR REPLACE FUNCTION can_add_seats(seats_record_id UUID, seats_to_add INTEGER)
RETURNS BOOLEAN AS $$
DECLARE
    current_total INTEGER;
BEGIN
    SELECT total_seats INTO current_total 
    FROM subscription_seats 
    WHERE id = seats_record_id;
    
    IF NOT FOUND THEN
        RETURN FALSE;
    END IF;
    
    RETURN (current_total + seats_to_add) <= 20;
END;
$$ LANGUAGE plpgsql;

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_subscription_seats_user_id ON subscription_seats(user_id);
CREATE INDEX IF NOT EXISTS idx_subscription_seats_subscription_id ON subscription_seats(subscription_id);
CREATE INDEX IF NOT EXISTS idx_subscription_seats_plan_id ON subscription_seats(plan_id);
CREATE INDEX IF NOT EXISTS idx_seat_transactions_subscription_seats_id ON seat_transactions(subscription_seats_id);
CREATE INDEX IF NOT EXISTS idx_seat_transactions_effective_date ON seat_transactions(effective_date);
CREATE INDEX IF NOT EXISTS idx_teams_subscription_seats_id ON teams(subscription_seats_id);

-- Views for easier querying
CREATE OR REPLACE VIEW subscription_seats_with_cost AS
SELECT 
    ss.*,
    calculate_subscription_cost(ss.id) as total_monthly_cost,
    (ss.total_seats - ss.used_seats) as available_seats,
    CASE 
        WHEN ss.used_seats >= ss.total_seats THEN 'full'
        WHEN ss.used_seats >= (ss.total_seats * 0.8) THEN 'near_full'
        ELSE 'available'
    END as usage_status
FROM subscription_seats ss;

CREATE OR REPLACE VIEW team_seat_summary AS
SELECT 
    t.id as team_id,
    t.name as team_name,
    t.owner_id,
    ss.total_seats,
    ss.used_seats,
    ss.seat_price_monthly,
    ss.billing_cycle,
    calculate_subscription_cost(ss.id) as total_cost,
    COUNT(tm.id) as actual_members
FROM teams t
LEFT JOIN subscription_seats ss ON t.subscription_seats_id = ss.id
LEFT JOIN team_members tm ON t.id = tm.team_id
GROUP BY t.id, t.name, t.owner_id, ss.total_seats, ss.used_seats, 
         ss.seat_price_monthly, ss.billing_cycle, ss.id;

-- Grant permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON subscription_seats TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON seat_transactions TO authenticated;
GRANT SELECT ON subscription_seats_with_cost TO authenticated;
GRANT SELECT ON team_seat_summary TO authenticated;
GRANT EXECUTE ON FUNCTION calculate_subscription_cost(UUID) TO authenticated;
GRANT EXECUTE ON FUNCTION can_add_seats(UUID, INTEGER) TO authenticated;

-- Comments for documentation
COMMENT ON TABLE subscription_seats IS 'Tracks seat purchases and usage for team subscriptions';
COMMENT ON TABLE seat_transactions IS 'Audit log of seat additions and removals';
COMMENT ON COLUMN subscription_seats.total_seats IS 'Total seats purchased';
COMMENT ON COLUMN subscription_seats.used_seats IS 'Currently used seats (active team members)';
COMMENT ON COLUMN seat_transactions.cost_change IS 'Cost impact of the transaction (positive for additions)';
