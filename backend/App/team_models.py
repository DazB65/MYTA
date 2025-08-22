"""
Team Collaboration Models for MYTA
Pydantic models for team management, invitations, and role-based access
"""

from datetime import datetime, timedelta
from enum import Enum
from typing import List, Optional, Dict, Any
from uuid import UUID

from pydantic.v1 import BaseModel, EmailStr, Field, validator
import secrets
import string


class TeamRole(str, Enum):
    """Team member roles with different permission levels"""
    OWNER = "owner"      # Full access, billing, team management
    EDITOR = "editor"    # Create/edit content, tasks, pillars
    VIEWER = "viewer"    # Read-only access to analytics and content


class TeamMemberStatus(str, Enum):
    """Status of team member"""
    ACTIVE = "active"
    INVITED = "invited"
    INACTIVE = "inactive"


class InvitationStatus(str, Enum):
    """Status of team invitation"""
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    EXPIRED = "expired"


# Base Models
class TeamBase(BaseModel):
    """Base team model"""
    name: str = Field(..., min_length=1, max_length=255, description="Team name")
    max_seats: int = Field(default=3, ge=1, le=10, description="Maximum team members")


class TeamMemberBase(BaseModel):
    """Base team member model"""
    role: TeamRole = Field(default=TeamRole.VIEWER, description="Member role")


class TeamInvitationBase(BaseModel):
    """Base team invitation model"""
    email: EmailStr = Field(..., description="Email address to invite")
    role: TeamRole = Field(default=TeamRole.VIEWER, description="Role for invited member")
    
    @validator('role')
    def validate_invitation_role(cls, v):
        """Owners can only be created, not invited"""
        if v == TeamRole.OWNER:
            raise ValueError("Cannot invite someone as owner")
        return v


# Request Models
class TeamCreateRequest(TeamBase):
    """Request to create a new team"""
    pass


class TeamUpdateRequest(BaseModel):
    """Request to update team details"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    max_seats: Optional[int] = Field(None, ge=1, le=10)


class TeamInviteRequest(TeamInvitationBase):
    """Request to invite a team member"""
    message: Optional[str] = Field(None, max_length=500, description="Optional invitation message")


class TeamMemberUpdateRequest(BaseModel):
    """Request to update team member role"""
    role: TeamRole = Field(..., description="New role for team member")
    
    @validator('role')
    def validate_role_change(cls, v):
        """Validate role change rules"""
        if v == TeamRole.OWNER:
            raise ValueError("Cannot change role to owner")
        return v


class InvitationResponseRequest(BaseModel):
    """Request to accept or decline invitation"""
    action: str = Field(..., regex="^(accept|decline)$")
    token: str = Field(..., min_length=32, max_length=128)


# Response Models
class TeamMember(TeamMemberBase):
    """Team member with user details"""
    id: UUID
    team_id: UUID
    user_id: UUID
    user_name: str
    user_email: EmailStr
    joined_at: datetime
    invited_by: Optional[UUID] = None
    invited_by_name: Optional[str] = None
    status: TeamMemberStatus = TeamMemberStatus.ACTIVE

    class Config:
        from_attributes = True


class TeamInvitation(TeamInvitationBase):
    """Team invitation details"""
    id: UUID
    team_id: UUID
    token: str
    invited_by: UUID
    invited_by_name: str
    invited_by_email: EmailStr
    expires_at: datetime
    created_at: datetime
    accepted_at: Optional[datetime] = None
    declined_at: Optional[datetime] = None
    status: InvitationStatus

    class Config:
        from_attributes = True

    @property
    def is_expired(self) -> bool:
        """Check if invitation is expired"""
        return datetime.utcnow() > self.expires_at

    @property
    def is_pending(self) -> bool:
        """Check if invitation is still pending"""
        return (
            self.accepted_at is None and 
            self.declined_at is None and 
            not self.is_expired
        )


class Team(TeamBase):
    """Complete team details"""
    id: UUID
    owner_id: UUID
    subscription_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    # Related data
    members: List[TeamMember] = []
    pending_invitations: List[TeamInvitation] = []
    
    # Computed properties
    member_count: int = 0
    available_seats: int = 0
    is_full: bool = False

    class Config:
        from_attributes = True

    def __init__(self, **data):
        super().__init__(**data)
        self.member_count = len(self.members)
        self.available_seats = max(0, self.max_seats - self.member_count)
        self.is_full = self.member_count >= self.max_seats


class TeamSummary(BaseModel):
    """Lightweight team summary"""
    id: UUID
    name: str
    member_count: int
    max_seats: int
    available_seats: int
    is_owner: bool
    user_role: TeamRole

    class Config:
        from_attributes = True


# Utility Models
class TeamPermissions(BaseModel):
    """User permissions within a team"""
    can_invite_members: bool = False
    can_remove_members: bool = False
    can_change_roles: bool = False
    can_edit_team: bool = False
    can_manage_billing: bool = False
    can_delete_team: bool = False
    can_create_content: bool = False
    can_edit_content: bool = False
    can_view_analytics: bool = True

    @classmethod
    def for_role(cls, role: TeamRole, is_owner: bool = False) -> "TeamPermissions":
        """Get permissions for a specific role"""
        if role == TeamRole.OWNER or is_owner:
            return cls(
                can_invite_members=True,
                can_remove_members=True,
                can_change_roles=True,
                can_edit_team=True,
                can_manage_billing=True,
                can_delete_team=True,
                can_create_content=True,
                can_edit_content=True,
                can_view_analytics=True
            )
        elif role == TeamRole.EDITOR:
            return cls(
                can_create_content=True,
                can_edit_content=True,
                can_view_analytics=True
            )
        else:  # VIEWER
            return cls(
                can_view_analytics=True
            )


class TeamActivity(BaseModel):
    """Team activity log entry"""
    id: UUID
    team_id: UUID
    user_id: UUID
    user_name: str
    action: str
    details: Dict[str, Any] = {}
    timestamp: datetime

    class Config:
        from_attributes = True


# Helper Functions
def generate_invitation_token() -> str:
    """Generate secure invitation token"""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(64))


def get_invitation_expiry() -> datetime:
    """Get expiration time for invitations (7 days from now)"""
    return datetime.utcnow() + timedelta(days=7)


# Response Wrappers
class TeamResponse(BaseModel):
    """Standard team response wrapper"""
    success: bool = True
    message: str = "Success"
    data: Optional[Team] = None


class TeamListResponse(BaseModel):
    """Team list response"""
    success: bool = True
    message: str = "Success"
    data: List[TeamSummary] = []
    total: int = 0


class TeamMemberResponse(BaseModel):
    """Team member response wrapper"""
    success: bool = True
    message: str = "Success"
    data: Optional[TeamMember] = None


class TeamInvitationResponse(BaseModel):
    """Team invitation response wrapper"""
    success: bool = True
    message: str = "Success"
    data: Optional[TeamInvitation] = None


class TeamPermissionsResponse(BaseModel):
    """Team permissions response wrapper"""
    success: bool = True
    message: str = "Success"
    data: Optional[TeamPermissions] = None


# Error Models
class TeamError(BaseModel):
    """Team-related error"""
    error_code: str
    message: str
    details: Optional[Dict[str, Any]] = None


class TeamValidationError(TeamError):
    """Team validation error"""
    error_code: str = "VALIDATION_ERROR"
    field_errors: Dict[str, List[str]] = {}
