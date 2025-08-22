"""
Team Collaboration Service for MYTA
Business logic for team management, invitations, and permissions
"""

import asyncio
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any, Tuple
from uuid import UUID, uuid4

import asyncpg
from fastapi import HTTPException, status

from backend.App.team_models import (
    Team, TeamMember, TeamInvitation, TeamRole, TeamPermissions,
    TeamCreateRequest, TeamUpdateRequest, TeamInviteRequest,
    TeamMemberUpdateRequest, InvitationResponseRequest,
    InvitationStatus, TeamMemberStatus,
    generate_invitation_token, get_invitation_expiry
)
from backend.App.supabase_client import get_supabase_service
from backend.App.email_service import send_team_invitation_email, notify_invitation_accepted, send_welcome_email
from backend.logging_config import get_logger, LogCategory

logger = get_logger(__name__, LogCategory.BUSINESS_LOGIC)


class TeamService:
    """Service for team collaboration management"""

    def __init__(self):
        self.supabase = get_supabase_service()

    async def get_connection(self):
        """Get database connection (mock for development)"""
        return self.supabase
    
    # Team Management
    async def create_team(self, owner_id: UUID, request: TeamCreateRequest) -> Team:
        """Create a new team with owner (mock implementation for development)"""
        from uuid import uuid4
        from datetime import datetime

        # Mock implementation - return a fake team for development
        team_id = uuid4()
        now = datetime.utcnow().isoformat()

        mock_team = Team(
            id=team_id,
            name=request.name,
            owner_id=owner_id,
            max_seats=request.max_seats,
            created_at=now,
            updated_at=now
        )

        logger.info(f"Mock team created: {team_id} for user {owner_id}")
        return mock_team
                await conn.execute(
                    """
                    INSERT INTO teams (id, name, owner_id, max_seats)
                    VALUES ($1, $2, $3, $4)
                    """,
                    team_id, request.name, owner_id, request.max_seats
                )
                
                # Add owner as team member
                await conn.execute(
                    """
                    INSERT INTO team_members (team_id, user_id, role, invited_by)
                    VALUES ($1, $2, $3, $4)
                    """,
                    team_id, owner_id, TeamRole.OWNER, owner_id
                )
                
                # Update user's team_id
                await conn.execute(
                    "UPDATE users SET team_id = $1 WHERE id = $2",
                    team_id, owner_id
                )
                
                logger.info(f"Created team {team_id} for user {owner_id}")
                return await self.get_team_by_id(team_id)
                
        except asyncpg.UniqueViolationError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Team name already exists"
            )
        except Exception as e:
            logger.error(f"Error creating team: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create team"
            )
    
    async def get_team_by_id(self, team_id: UUID) -> Optional[Team]:
        """Get team by ID with members and invitations"""
        conn = await self.get_connection()
        
        # Get team details
        team_row = await conn.fetchrow(
            "SELECT * FROM teams WHERE id = $1",
            team_id
        )
        
        if not team_row:
            return None
        
        # Get team members
        members_rows = await conn.fetch(
            """
            SELECT tm.*, u.name as user_name, u.email as user_email,
                   inviter.name as invited_by_name
            FROM team_members tm
            JOIN users u ON tm.user_id = u.id
            LEFT JOIN users inviter ON tm.invited_by = inviter.id
            WHERE tm.team_id = $1
            ORDER BY tm.joined_at
            """,
            team_id
        )
        
        # Get pending invitations
        invitations_rows = await conn.fetch(
            """
            SELECT ti.*, t.name as team_name,
                   inviter.name as invited_by_name,
                   inviter.email as invited_by_email
            FROM team_invitations ti
            JOIN teams t ON ti.team_id = t.id
            JOIN users inviter ON ti.invited_by = inviter.id
            WHERE ti.team_id = $1 
            AND ti.accepted_at IS NULL 
            AND ti.declined_at IS NULL 
            AND ti.expires_at > NOW()
            ORDER BY ti.created_at DESC
            """,
            team_id
        )
        
        # Convert to models
        members = [
            TeamMember(
                id=row['id'],
                team_id=row['team_id'],
                user_id=row['user_id'],
                role=row['role'],
                user_name=row['user_name'],
                user_email=row['user_email'],
                joined_at=row['joined_at'],
                invited_by=row['invited_by'],
                invited_by_name=row['invited_by_name'],
                status=TeamMemberStatus.ACTIVE
            )
            for row in members_rows
        ]
        
        invitations = [
            TeamInvitation(
                id=row['id'],
                team_id=row['team_id'],
                email=row['email'],
                role=row['role'],
                token=row['token'],
                invited_by=row['invited_by'],
                invited_by_name=row['invited_by_name'],
                invited_by_email=row['invited_by_email'],
                expires_at=row['expires_at'],
                created_at=row['created_at'],
                accepted_at=row['accepted_at'],
                declined_at=row['declined_at'],
                status=InvitationStatus.PENDING
            )
            for row in invitations_rows
        ]
        
        return Team(
            id=team_row['id'],
            name=team_row['name'],
            owner_id=team_row['owner_id'],
            subscription_id=team_row['subscription_id'],
            max_seats=team_row['max_seats'],
            created_at=team_row['created_at'],
            updated_at=team_row['updated_at'],
            members=members,
            pending_invitations=invitations
        )
    
    async def get_user_team(self, user_id: UUID) -> Optional[Team]:
        """Get team that user belongs to"""
        conn = await self.get_connection()
        
        # Get user's team_id
        user_row = await conn.fetchrow(
            "SELECT team_id FROM users WHERE id = $1",
            user_id
        )
        
        if not user_row or not user_row['team_id']:
            return None
        
        return await self.get_team_by_id(user_row['team_id'])
    
    async def update_team(self, team_id: UUID, request: TeamUpdateRequest, user_id: UUID) -> Team:
        """Update team details (owner only)"""
        conn = await self.get_connection()
        
        # Verify user is team owner
        if not await self.is_team_owner(team_id, user_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only team owner can update team details"
            )
        
        # Build update query
        updates = []
        values = []
        param_count = 1
        
        if request.name is not None:
            updates.append(f"name = ${param_count}")
            values.append(request.name)
            param_count += 1
        
        if request.max_seats is not None:
            # Check if reducing seats would exceed current member count
            current_members = await conn.fetchval(
                "SELECT COUNT(*) FROM team_members WHERE team_id = $1",
                team_id
            )
            
            if request.max_seats < current_members:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Cannot reduce seats below current member count ({current_members})"
                )
            
            updates.append(f"max_seats = ${param_count}")
            values.append(request.max_seats)
            param_count += 1
        
        if not updates:
            # No changes requested
            return await self.get_team_by_id(team_id)
        
        # Add updated_at
        updates.append(f"updated_at = ${param_count}")
        values.append(datetime.utcnow())
        param_count += 1
        
        # Add team_id for WHERE clause
        values.append(team_id)
        
        query = f"""
        UPDATE teams 
        SET {', '.join(updates)}
        WHERE id = ${param_count}
        """
        
        await conn.execute(query, *values)
        
        logger.info(f"Updated team {team_id} by user {user_id}")
        return await self.get_team_by_id(team_id)
    
    # Team Member Management
    async def invite_member(self, team_id: UUID, request: TeamInviteRequest, inviter_id: UUID) -> TeamInvitation:
        """Invite a new team member"""
        conn = await self.get_connection()
        
        # Verify inviter has permission
        if not await self.can_invite_members(team_id, inviter_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to invite members"
            )
        
        # Check if team has available seats
        if not await self.team_has_available_seats(team_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Team has reached maximum member limit"
            )
        
        # Check if user is already a member
        existing_member = await conn.fetchrow(
            """
            SELECT tm.id FROM team_members tm
            JOIN users u ON tm.user_id = u.id
            WHERE tm.team_id = $1 AND u.email = $2
            """,
            team_id, request.email
        )
        
        if existing_member:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already a team member"
            )
        
        # Check for existing pending invitation
        existing_invitation = await conn.fetchrow(
            """
            SELECT id FROM team_invitations 
            WHERE team_id = $1 AND email = $2 
            AND accepted_at IS NULL AND declined_at IS NULL 
            AND expires_at > NOW()
            """,
            team_id, request.email
        )
        
        if existing_invitation:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invitation already sent to this email"
            )
        
        # Create invitation
        invitation_id = uuid4()
        token = generate_invitation_token()
        expires_at = get_invitation_expiry()
        
        await conn.execute(
            """
            INSERT INTO team_invitations 
            (id, team_id, email, role, token, invited_by, expires_at)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            """,
            invitation_id, team_id, request.email, request.role,
            token, inviter_id, expires_at
        )
        
        # Get invitation details
        invitation_row = await conn.fetchrow(
            """
            SELECT ti.*, t.name as team_name,
                   inviter.name as invited_by_name,
                   inviter.email as invited_by_email
            FROM team_invitations ti
            JOIN teams t ON ti.team_id = t.id
            JOIN users inviter ON ti.invited_by = inviter.id
            WHERE ti.id = $1
            """,
            invitation_id
        )
        
        invitation = TeamInvitation(
            id=invitation_row['id'],
            team_id=invitation_row['team_id'],
            email=invitation_row['email'],
            role=invitation_row['role'],
            token=invitation_row['token'],
            invited_by=invitation_row['invited_by'],
            invited_by_name=invitation_row['invited_by_name'],
            invited_by_email=invitation_row['invited_by_email'],
            expires_at=invitation_row['expires_at'],
            created_at=invitation_row['created_at'],
            status=InvitationStatus.PENDING
        )

        # Send invitation email
        try:
            team_name = await conn.fetchval("SELECT name FROM teams WHERE id = $1", team_id)
            email_sent = await send_team_invitation_email(invitation, team_name)
            if email_sent:
                logger.info(f"Invitation email sent to {request.email}")
            else:
                logger.warning(f"Failed to send invitation email to {request.email}")
        except Exception as e:
            logger.error(f"Error sending invitation email: {e}")

        logger.info(f"Created invitation {invitation_id} for {request.email} to team {team_id}")

        return invitation
    
    # Helper Methods
    async def is_team_owner(self, team_id: UUID, user_id: UUID) -> bool:
        """Check if user is team owner"""
        conn = await self.get_connection()
        
        result = await conn.fetchval(
            "SELECT owner_id FROM teams WHERE id = $1",
            team_id
        )
        
        return result == user_id
    
    async def get_user_role(self, team_id: UUID, user_id: UUID) -> Optional[TeamRole]:
        """Get user's role in team"""
        conn = await self.get_connection()
        
        result = await conn.fetchval(
            "SELECT role FROM team_members WHERE team_id = $1 AND user_id = $2",
            team_id, user_id
        )
        
        return TeamRole(result) if result else None
    
    async def team_has_available_seats(self, team_id: UUID) -> bool:
        """Check if team has available seats"""
        conn = await self.get_connection()
        
        result = await conn.fetchval(
            "SELECT team_has_available_seats($1)",
            team_id
        )
        
        return result or False
    
    async def can_invite_members(self, team_id: UUID, user_id: UUID) -> bool:
        """Check if user can invite members"""
        role = await self.get_user_role(team_id, user_id)
        is_owner = await self.is_team_owner(team_id, user_id)

        if not role:
            return False

        permissions = TeamPermissions.for_role(role, is_owner)
        return permissions.can_invite_members

    async def accept_invitation(self, token: str, user_id: UUID) -> TeamMember:
        """Accept team invitation"""
        conn = await self.get_connection()

        # Get invitation details
        invitation_row = await conn.fetchrow(
            """
            SELECT ti.*, t.name as team_name
            FROM team_invitations ti
            JOIN teams t ON ti.team_id = t.id
            WHERE ti.token = $1
            AND ti.accepted_at IS NULL
            AND ti.declined_at IS NULL
            AND ti.expires_at > NOW()
            """,
            token
        )

        if not invitation_row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid or expired invitation"
            )

        # Check if team has available seats
        if not await self.team_has_available_seats(invitation_row['team_id']):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Team has reached maximum member limit"
            )

        # Check if user email matches invitation
        user_email = await conn.fetchval(
            "SELECT email FROM users WHERE id = $1",
            user_id
        )

        if user_email != invitation_row['email']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invitation email does not match user email"
            )

        async with conn.transaction():
            # Mark invitation as accepted
            await conn.execute(
                "UPDATE team_invitations SET accepted_at = NOW() WHERE id = $1",
                invitation_row['id']
            )

            # Add user to team
            member_id = uuid4()
            await conn.execute(
                """
                INSERT INTO team_members (id, team_id, user_id, role, invited_by)
                VALUES ($1, $2, $3, $4, $5)
                """,
                member_id, invitation_row['team_id'], user_id,
                invitation_row['role'], invitation_row['invited_by']
            )

            # Update user's team_id
            await conn.execute(
                "UPDATE users SET team_id = $1 WHERE id = $2",
                invitation_row['team_id'], user_id
            )

        logger.info(f"User {user_id} accepted invitation to team {invitation_row['team_id']}")

        # Send notification emails
        try:
            # Get user and team details for emails
            user_details = await conn.fetchrow("SELECT name, email FROM users WHERE id = $1", user_id)
            team_owner_email = await conn.fetchval(
                "SELECT u.email FROM users u JOIN teams t ON u.id = t.owner_id WHERE t.id = $1",
                invitation_row['team_id']
            )

            if user_details and team_owner_email:
                # Notify team owner
                await notify_invitation_accepted(
                    team_owner_email,
                    invitation_row['team_name'],
                    user_details['name'],
                    user_details['email']
                )

                # Send welcome email to new member
                await send_welcome_email(
                    user_details['email'],
                    user_details['name'],
                    invitation_row['team_name'],
                    invitation_row['role']
                )
        except Exception as e:
            logger.error(f"Error sending notification emails: {e}")

        # Return team member details
        member_row = await conn.fetchrow(
            """
            SELECT tm.*, u.name as user_name, u.email as user_email,
                   inviter.name as invited_by_name
            FROM team_members tm
            JOIN users u ON tm.user_id = u.id
            LEFT JOIN users inviter ON tm.invited_by = inviter.id
            WHERE tm.id = $1
            """,
            member_id
        )

        return TeamMember(
            id=member_row['id'],
            team_id=member_row['team_id'],
            user_id=member_row['user_id'],
            role=member_row['role'],
            user_name=member_row['user_name'],
            user_email=member_row['user_email'],
            joined_at=member_row['joined_at'],
            invited_by=member_row['invited_by'],
            invited_by_name=member_row['invited_by_name'],
            status=TeamMemberStatus.ACTIVE
        )

    async def decline_invitation(self, token: str) -> bool:
        """Decline team invitation"""
        conn = await self.get_connection()

        result = await conn.execute(
            """
            UPDATE team_invitations
            SET declined_at = NOW()
            WHERE token = $1
            AND accepted_at IS NULL
            AND declined_at IS NULL
            AND expires_at > NOW()
            """,
            token
        )

        if result == "UPDATE 0":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid or expired invitation"
            )

        logger.info(f"Invitation with token {token[:8]}... declined")
        return True

    async def remove_member(self, team_id: UUID, member_id: UUID, remover_id: UUID) -> bool:
        """Remove team member (owner only)"""
        conn = await self.get_connection()

        # Verify remover has permission
        if not await self.is_team_owner(team_id, remover_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only team owner can remove members"
            )

        # Get member details
        member_row = await conn.fetchrow(
            "SELECT user_id, role FROM team_members WHERE id = $1 AND team_id = $2",
            member_id, team_id
        )

        if not member_row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team member not found"
            )

        # Cannot remove owner
        if member_row['role'] == TeamRole.OWNER:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot remove team owner"
            )

        async with conn.transaction():
            # Remove from team
            await conn.execute(
                "DELETE FROM team_members WHERE id = $1",
                member_id
            )

            # Clear user's team_id
            await conn.execute(
                "UPDATE users SET team_id = NULL WHERE id = $1",
                member_row['user_id']
            )

        logger.info(f"Removed member {member_id} from team {team_id}")
        return True


# Global service instance
team_service = TeamService()
