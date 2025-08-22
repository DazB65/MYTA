"""
Mock Team Service for MYTA (Development Only)
Simplified implementation for frontend development
"""

from typing import List, Optional, Dict, Any
from uuid import UUID, uuid4
from datetime import datetime, timedelta

from fastapi import HTTPException, status

from backend.App.team_models import (
    Team, TeamMember, TeamInvitation, TeamRole, TeamPermissions,
    TeamCreateRequest, TeamUpdateRequest, TeamInviteRequest,
    TeamMemberUpdateRequest, InvitationResponseRequest,
    InvitationStatus, TeamMemberStatus,
    generate_invitation_token, get_invitation_expiry
)
from backend.logging_config import get_logger, LogCategory

logger = get_logger(__name__, LogCategory.API)


class MockTeamService:
    """Mock service for team collaboration management (development only)"""
    
    def __init__(self):
        # In-memory storage for development
        self.teams = {}
        self.members = {}
        self.invitations = {}
    
    async def create_team(self, owner_id: UUID, request: TeamCreateRequest) -> Team:
        """Create a new team with owner (mock implementation)"""
        team_id = uuid4()
        now = datetime.utcnow().isoformat()
        
        team = Team(
            id=team_id,
            name=request.name,
            owner_id=owner_id,
            max_seats=request.max_seats,
            created_at=now,
            updated_at=now
        )
        
        # Store in mock storage
        self.teams[str(team_id)] = team
        
        # Add owner as team member
        member = TeamMember(
            id=uuid4(),
            team_id=team_id,
            user_id=owner_id,
            role=TeamRole.OWNER,
            status=TeamMemberStatus.ACTIVE,
            invited_by=owner_id,
            joined_at=now,
            created_at=now,
            updated_at=now
        )
        self.members[str(member.id)] = member
        
        logger.info(f"Mock team created: {team_id} for user {owner_id}")
        return team
    
    async def get_user_team(self, user_id: UUID) -> Optional[Team]:
        """Get user's team (mock implementation)"""
        # Return first team where user is a member
        for team in self.teams.values():
            if team.owner_id == user_id:
                return team
        return None
    
    async def get_team_by_id(self, team_id: UUID) -> Optional[Team]:
        """Get team by ID (mock implementation)"""
        return self.teams.get(str(team_id))
    
    async def get_user_role(self, team_id: UUID, user_id: UUID) -> Optional[TeamRole]:
        """Get user's role in team (mock implementation)"""
        for member in self.members.values():
            if member.team_id == team_id and member.user_id == user_id:
                return member.role
        return None
    
    async def is_team_owner(self, team_id: UUID, user_id: UUID) -> bool:
        """Check if user is team owner (mock implementation)"""
        team = self.teams.get(str(team_id))
        return team and team.owner_id == user_id
    
    async def update_team(self, team_id: UUID, request: TeamUpdateRequest, user_id: UUID) -> Team:
        """Update team details (mock implementation)"""
        team = self.teams.get(str(team_id))
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
        
        if team.owner_id != user_id:
            raise HTTPException(status_code=403, detail="Only team owner can update team")
        
        if request.name:
            team.name = request.name
        if request.max_seats:
            team.max_seats = request.max_seats
        
        team.updated_at = datetime.utcnow().isoformat()
        return team
    
    async def invite_member(self, team_id: UUID, request: TeamInviteRequest, inviter_id: UUID) -> TeamInvitation:
        """Invite a new team member (mock implementation)"""
        invitation_id = uuid4()
        token = generate_invitation_token()
        now = datetime.utcnow().isoformat()
        
        invitation = TeamInvitation(
            id=invitation_id,
            team_id=team_id,
            email=request.email,
            role=request.role,
            token=token,
            status=InvitationStatus.PENDING,
            invited_by=inviter_id,
            expires_at=get_invitation_expiry(),
            message=request.message,
            created_at=now,
            updated_at=now
        )
        
        self.invitations[str(invitation_id)] = invitation
        logger.info(f"Mock invitation created: {invitation_id} for {request.email}")
        return invitation
    
    async def accept_invitation(self, token: str, user_id: UUID) -> TeamMember:
        """Accept team invitation (mock implementation)"""
        # Find invitation by token
        invitation = None
        for inv in self.invitations.values():
            if inv.token == token:
                invitation = inv
                break
        
        if not invitation:
            raise HTTPException(status_code=404, detail="Invitation not found")
        
        # Create team member
        member_id = uuid4()
        now = datetime.utcnow().isoformat()
        
        member = TeamMember(
            id=member_id,
            team_id=invitation.team_id,
            user_id=user_id,
            role=invitation.role,
            status=TeamMemberStatus.ACTIVE,
            invited_by=invitation.invited_by,
            joined_at=now,
            created_at=now,
            updated_at=now
        )
        
        self.members[str(member_id)] = member
        invitation.status = InvitationStatus.ACCEPTED
        
        logger.info(f"Mock invitation accepted: {invitation.id} by user {user_id}")
        return member
    
    async def decline_invitation(self, token: str):
        """Decline team invitation (mock implementation)"""
        for inv in self.invitations.values():
            if inv.token == token:
                inv.status = InvitationStatus.DECLINED
                logger.info(f"Mock invitation declined: {inv.id}")
                return
        
        raise HTTPException(status_code=404, detail="Invitation not found")
    
    async def remove_member(self, team_id: UUID, member_id: UUID, remover_id: UUID):
        """Remove team member (mock implementation)"""
        # Check if remover is team owner
        if not await self.is_team_owner(team_id, remover_id):
            raise HTTPException(status_code=403, detail="Only team owner can remove members")
        
        # Find and remove member
        for mid, member in list(self.members.items()):
            if member.id == member_id and member.team_id == team_id:
                del self.members[mid]
                logger.info(f"Mock member removed: {member_id} from team {team_id}")
                return
        
        raise HTTPException(status_code=404, detail="Member not found")


# Global service instance
team_service = MockTeamService()
