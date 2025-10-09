"""
Team Collaboration API Router for MYTA
FastAPI endpoints for team management, invitations, and member operations
"""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import JSONResponse

from .team_models import (
    Team, TeamMember, TeamInvitation, TeamPermissions,
    TeamCreateRequest, TeamUpdateRequest, TeamInviteRequest,
    TeamMemberUpdateRequest, InvitationResponseRequest,
    TeamResponse, TeamListResponse, TeamMemberResponse,
    TeamInvitationResponse, TeamPermissionsResponse,
    TeamSummary, TeamRole
)
from .team_service_mock import team_service
from .auth_middleware import get_current_user
from .api_models import create_success_response, create_error_response
from .logging_config import get_logger, LogCategory

logger = get_logger(__name__, LogCategory.API)
router = APIRouter(prefix="/api/teams", tags=["teams"])


@router.post("/", response_model=TeamResponse)
async def create_team(
    request: TeamCreateRequest,
    current_user: dict = Depends(get_current_user)
):
    """Create a new team (requires team subscription)"""
    try:
        user_id = UUID(current_user["id"])
        
        # Check if user has team subscription
        if current_user.get("subscription_tier") != "team":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Team subscription required to create teams"
            )
        
        team = await team_service.create_team(user_id, request)
        
        return TeamResponse(
            message="Team created successfully",
            data=team
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating team: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create team"
        )


@router.get("/my-team", response_model=TeamResponse)
async def get_my_team(
    current_user: dict = Depends(get_current_user)
):
    """Get current user's team"""
    try:
        user_id = UUID(current_user["id"])
        team = await team_service.get_user_team(user_id)
        
        if not team:
            return TeamResponse(
                success=False,
                message="User is not part of any team",
                data=None
            )
        
        return TeamResponse(
            message="Team retrieved successfully",
            data=team
        )
        
    except Exception as e:
        logger.error(f"Error getting user team: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve team"
        )


@router.get("/{team_id}", response_model=TeamResponse)
async def get_team(
    team_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """Get team details (members only)"""
    try:
        user_id = UUID(current_user["id"])
        team = await team_service.get_team_by_id(team_id)
        
        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team not found"
            )
        
        # Check if user is team member
        user_role = await team_service.get_user_role(team_id, user_id)
        if not user_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: not a team member"
            )
        
        return TeamResponse(
            message="Team retrieved successfully",
            data=team
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting team {team_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve team"
        )


@router.put("/{team_id}", response_model=TeamResponse)
async def update_team(
    team_id: UUID,
    request: TeamUpdateRequest,
    current_user: dict = Depends(get_current_user)
):
    """Update team details (owner only)"""
    try:
        user_id = UUID(current_user["id"])
        team = await team_service.update_team(team_id, request, user_id)
        
        return TeamResponse(
            message="Team updated successfully",
            data=team
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating team {team_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update team"
        )


@router.post("/{team_id}/invite", response_model=TeamInvitationResponse)
async def invite_member(
    team_id: UUID,
    request: TeamInviteRequest,
    current_user: dict = Depends(get_current_user)
):
    """Invite a new team member"""
    try:
        user_id = UUID(current_user["id"])
        invitation = await team_service.invite_member(team_id, request, user_id)
        
        return TeamInvitationResponse(
            message="Invitation sent successfully",
            data=invitation
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error inviting member to team {team_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send invitation"
        )


@router.post("/invitations/accept", response_model=TeamMemberResponse)
async def accept_invitation(
    request: InvitationResponseRequest,
    current_user: dict = Depends(get_current_user)
):
    """Accept team invitation"""
    try:
        if request.action != "accept":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid action for this endpoint"
            )
        
        user_id = UUID(current_user["id"])
        member = await team_service.accept_invitation(request.token, user_id)
        
        return TeamMemberResponse(
            message="Invitation accepted successfully",
            data=member
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error accepting invitation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to accept invitation"
        )


@router.post("/invitations/decline")
async def decline_invitation(
    request: InvitationResponseRequest,
    current_user: dict = Depends(get_current_user)
):
    """Decline team invitation"""
    try:
        if request.action != "decline":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid action for this endpoint"
            )
        
        await team_service.decline_invitation(request.token)
        
        return JSONResponse(
            content={"success": True, "message": "Invitation declined successfully"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error declining invitation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to decline invitation"
        )


@router.delete("/{team_id}/members/{member_id}")
async def remove_member(
    team_id: UUID,
    member_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """Remove team member (owner only)"""
    try:
        user_id = UUID(current_user["id"])
        await team_service.remove_member(team_id, member_id, user_id)
        
        return JSONResponse(
            content={"success": True, "message": "Member removed successfully"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error removing member {member_id} from team {team_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to remove member"
        )


@router.get("/{team_id}/permissions", response_model=TeamPermissionsResponse)
async def get_user_permissions(
    team_id: UUID,
    current_user: dict = Depends(get_current_user)
):
    """Get current user's permissions in team"""
    try:
        user_id = UUID(current_user["id"])
        
        # Get user role
        role = await team_service.get_user_role(team_id, user_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: not a team member"
            )
        
        # Check if owner
        is_owner = await team_service.is_team_owner(team_id, user_id)
        
        # Get permissions
        permissions = TeamPermissions.for_role(role, is_owner)
        
        return TeamPermissionsResponse(
            message="Permissions retrieved successfully",
            data=permissions
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting permissions for team {team_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve permissions"
        )


# Health check endpoint
@router.get("/health")
async def health_check():
    """Health check for team service"""
    return {"status": "healthy", "service": "team_collaboration"}
