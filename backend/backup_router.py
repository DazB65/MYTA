"""
Database Backup Management API Router
Provides comprehensive backup management endpoints for the Vidalytics application
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging
import os

from api_models import StandardResponse, create_success_response, create_error_response
from backup_service import (
    get_backup_service, BackupService, BackupHealthChecker,
    BackupSchedule, BackupAlert, BackupFrequency
)
from migration_manager import BackupInfo
from auth_middleware import get_current_user, AuthToken
from config import get_settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/backup", tags=["backup"])


# Pydantic models for API requests/responses
from pydantic import BaseModel, Field

class BackupCreateRequest(BaseModel):
    """Request model for creating a manual backup"""
    description: Optional[str] = Field(None, description="Optional description for the backup")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")

class BackupScheduleRequest(BaseModel):
    """Request model for updating backup schedule"""
    frequency: BackupFrequency = Field(description="Backup frequency")
    time: str = Field(description="Time for backup (HH:MM for daily/weekly/monthly, MM for hourly)")
    enabled: bool = Field(default=True, description="Whether backups are enabled")
    compression: bool = Field(default=True, description="Whether to compress backups")
    max_backups: int = Field(default=10, description="Maximum number of backups to retain")
    cleanup_enabled: bool = Field(default=True, description="Whether to auto-cleanup old backups")

class BackupAlertRequest(BaseModel):
    """Request model for updating backup alert configuration"""
    email_enabled: bool = Field(default=False, description="Enable email alerts")
    email_recipients: Optional[List[str]] = Field(default=None, description="Email recipients")
    webhook_url: Optional[str] = Field(default=None, description="Webhook URL for alerts")
    alert_on_failure: bool = Field(default=True, description="Alert on backup failures")
    alert_on_success: bool = Field(default=False, description="Alert on backup success")
    alert_on_cleanup: bool = Field(default=False, description="Alert on cleanup operations")

class BackupInfoResponse(BaseModel):
    """Response model for backup information"""
    backup_id: str
    filename: str
    size_mb: float
    created_at: str
    database_version: str
    backup_type: str
    compression: bool
    metadata: Dict[str, Any]

class BackupStatusResponse(BaseModel):
    """Response model for backup service status"""
    running: bool
    schedule: Dict[str, Any]
    alerts: Dict[str, Any]
    last_check: str

class BackupHealthResponse(BaseModel):
    """Response model for backup health check"""
    timestamp: str
    overall_status: str
    checks: Dict[str, Any]
    failed_checks: Optional[List[str]] = None
    error: Optional[str] = None


@router.get("/status", response_model=BackupStatusResponse)
async def get_backup_status(
    current_user: AuthToken = Depends(get_current_user)
) -> BackupStatusResponse:
    """
    Get the current status of the backup service
    
    Returns:
        BackupStatusResponse: Current backup service status and configuration
    """
    try:
        backup_service = get_backup_service()
        status = backup_service.get_service_status()
        
        return BackupStatusResponse(**status)
        
    except Exception as e:
        logger.error(f"Error getting backup status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get backup status")


@router.post("/create")
async def create_manual_backup(
    request: BackupCreateRequest,
    background_tasks: BackgroundTasks,
    current_user: AuthToken = Depends(get_current_user)
) -> StandardResponse:
    """
    Create a manual backup of the database
    
    Args:
        request: Backup creation request with optional description and metadata
        background_tasks: FastAPI background tasks for async execution
        current_user: Authenticated user token
    
    Returns:
        StandardResponse: Success/failure response with backup ID
    """
    try:
        backup_service = get_backup_service()
        
        # Prepare metadata
        metadata = request.metadata or {}
        metadata.update({
            "created_by": current_user.user_id,
            "description": request.description or "Manual backup",
            "created_via": "api"
        })
        
        # Create backup in background for faster response
        def create_backup():
            backup_id = backup_service.create_manual_backup(metadata=metadata)
            if backup_id:
                logger.info(f"Manual backup created successfully: {backup_id}")
            else:
                logger.error("Manual backup creation failed")
        
        background_tasks.add_task(create_backup)
        
        return create_success_response(
            message="Backup creation initiated successfully",
            data={"status": "initiated"}
        )
        
    except Exception as e:
        logger.error(f"Error creating manual backup: {e}")
        raise HTTPException(status_code=500, detail="Failed to create backup")


@router.get("/list", response_model=List[BackupInfoResponse])
async def list_backups(
    limit: Optional[int] = 50,
    backup_type: Optional[str] = None,
    current_user: AuthToken = Depends(get_current_user)
) -> List[BackupInfoResponse]:
    """
    List all available database backups
    
    Args:
        limit: Maximum number of backups to return (default: 50)
        backup_type: Filter by backup type (manual, automatic, pre_migration, etc.)
        current_user: Authenticated user token
    
    Returns:
        List[BackupInfoResponse]: List of backup information
    """
    try:
        backup_service = get_backup_service()
        backups = backup_service.migration_manager.list_backups()
        
        # Filter by backup type if specified
        if backup_type:
            backups = [b for b in backups if b.backup_type == backup_type]
        
        # Limit results
        if limit:
            backups = backups[:limit]
        
        # Convert to response model
        backup_responses = []
        for backup in backups:
            backup_responses.append(BackupInfoResponse(
                backup_id=backup.backup_id,
                filename=backup.filename,
                size_mb=round(backup.size_bytes / (1024 * 1024), 2),
                created_at=backup.created_at.isoformat(),
                database_version=backup.database_version,
                backup_type=backup.backup_type,
                compression=backup.compression,
                metadata=backup.metadata
            ))
        
        return backup_responses
        
    except Exception as e:
        logger.error(f"Error listing backups: {e}")
        raise HTTPException(status_code=500, detail="Failed to list backups")


@router.post("/restore/{backup_id}")
async def restore_backup(
    backup_id: str,
    verify_integrity: bool = True,
    current_user: AuthToken = Depends(get_current_user)
) -> StandardResponse:
    """
    Restore database from a specific backup
    
    Args:
        backup_id: ID of the backup to restore
        verify_integrity: Whether to verify backup integrity before restore
        current_user: Authenticated user token
    
    Returns:
        StandardResponse: Success/failure response
    """
    try:
        backup_service = get_backup_service()
        
        # Get backup info first to validate it exists
        backup_info = backup_service.migration_manager.get_backup_info(backup_id)
        if not backup_info:
            raise HTTPException(status_code=404, detail="Backup not found")
        
        # Restore the backup
        success = backup_service.migration_manager.restore_backup(
            backup_id=backup_id,
            verify_integrity=verify_integrity
        )
        
        if success:
            logger.info(f"Database restored successfully from backup: {backup_id}")
            return create_success_response(
                message=f"Database restored successfully from backup {backup_id}",
                data={
                    "backup_id": backup_id,
                    "restore_time": datetime.now().isoformat(),
                    "verified": verify_integrity
                }
            )
        else:
            raise HTTPException(status_code=500, detail="Backup restore failed")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error restoring backup {backup_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to restore backup")


@router.delete("/delete/{backup_id}")
async def delete_backup(
    backup_id: str,
    current_user: AuthToken = Depends(get_current_user)
) -> StandardResponse:
    """
    Delete a specific backup
    
    Args:
        backup_id: ID of the backup to delete
        current_user: Authenticated user token
    
    Returns:
        StandardResponse: Success/failure response
    """
    try:
        backup_service = get_backup_service()
        
        # Get backup info first to validate it exists
        backup_info = backup_service.migration_manager.get_backup_info(backup_id)
        if not backup_info:
            raise HTTPException(status_code=404, detail="Backup not found")
        
        # Delete the backup
        success = backup_service.migration_manager.delete_backup(backup_id)
        
        if success:
            logger.info(f"Backup deleted successfully: {backup_id}")
            return create_success_response(
                message=f"Backup {backup_id} deleted successfully",
                data={"backup_id": backup_id}
            )
        else:
            raise HTTPException(status_code=500, detail="Backup deletion failed")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting backup {backup_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete backup")


@router.get("/health", response_model=BackupHealthResponse)
async def get_backup_health(
    current_user: AuthToken = Depends(get_current_user)
) -> BackupHealthResponse:
    """
    Perform comprehensive backup system health check
    
    Args:
        current_user: Authenticated user token
    
    Returns:
        BackupHealthResponse: Detailed health check results
    """
    try:
        settings = get_settings()
        db_path = settings.database_url.replace("sqlite:///", "").replace("./", "")
        
        health_checker = BackupHealthChecker(db_path)
        health_report = health_checker.run_health_check()
        
        return BackupHealthResponse(**health_report)
        
    except Exception as e:
        logger.error(f"Error performing backup health check: {e}")
        raise HTTPException(status_code=500, detail="Failed to perform health check")


@router.put("/schedule")
async def update_backup_schedule(
    request: BackupScheduleRequest,
    current_user: AuthToken = Depends(get_current_user)
) -> StandardResponse:
    """
    Update backup schedule configuration
    
    Args:
        request: New backup schedule configuration
        current_user: Authenticated user token
    
    Returns:
        StandardResponse: Success/failure response
    """
    try:
        backup_service = get_backup_service()
        
        # Create new schedule configuration
        new_schedule = BackupSchedule(
            frequency=request.frequency,
            time=request.time,
            enabled=request.enabled,
            compression=request.compression,
            max_backups=request.max_backups,
            cleanup_enabled=request.cleanup_enabled
        )
        
        # Update the schedule
        backup_service.update_schedule(new_schedule)
        
        logger.info(f"Backup schedule updated: {request.frequency.value} at {request.time}")
        return create_success_response(
            message="Backup schedule updated successfully",
            data={
                "frequency": request.frequency.value,
                "time": request.time,
                "enabled": request.enabled
            }
        )
        
    except Exception as e:
        logger.error(f"Error updating backup schedule: {e}")
        raise HTTPException(status_code=500, detail="Failed to update backup schedule")


@router.put("/alerts")
async def update_backup_alerts(
    request: BackupAlertRequest,
    current_user: AuthToken = Depends(get_current_user)
) -> StandardResponse:
    """
    Update backup alert configuration
    
    Args:
        request: New backup alert configuration
        current_user: Authenticated user token
    
    Returns:
        StandardResponse: Success/failure response
    """
    try:
        backup_service = get_backup_service()
        
        # Create new alert configuration
        new_alert_config = BackupAlert(
            email_enabled=request.email_enabled,
            email_recipients=request.email_recipients or [],
            webhook_url=request.webhook_url,
            alert_on_failure=request.alert_on_failure,
            alert_on_success=request.alert_on_success,
            alert_on_cleanup=request.alert_on_cleanup
        )
        
        # Update alert configuration
        backup_service.update_alerts(new_alert_config)
        
        logger.info("Backup alert configuration updated successfully")
        return create_success_response(
            message="Backup alert configuration updated successfully",
            data={
                "email_enabled": request.email_enabled,
                "webhook_enabled": bool(request.webhook_url)
            }
        )
        
    except Exception as e:
        logger.error(f"Error updating backup alerts: {e}")
        raise HTTPException(status_code=500, detail="Failed to update backup alerts")


@router.post("/cleanup")
async def cleanup_old_backups(
    keep_days: int = 30,
    keep_count: int = 10,
    current_user: AuthToken = Depends(get_current_user)
) -> StandardResponse:
    """
    Manually trigger cleanup of old backups
    
    Args:
        keep_days: Number of days to keep backups (default: 30)
        keep_count: Minimum number of recent backups to keep (default: 10)
        current_user: Authenticated user token
    
    Returns:
        StandardResponse: Success response with cleanup statistics
    """
    try:
        backup_service = get_backup_service()
        
        # Perform cleanup
        deleted_count = backup_service.migration_manager.cleanup_old_backups(
            keep_days=keep_days,
            keep_count=keep_count
        )
        
        logger.info(f"Manual backup cleanup completed: {deleted_count} backups removed")
        return create_success_response(
            message=f"Cleanup completed: {deleted_count} old backups removed",
            data={
                "deleted_count": deleted_count,
                "keep_days": keep_days,
                "keep_count": keep_count
            }
        )
        
    except Exception as e:
        logger.error(f"Error during backup cleanup: {e}")
        raise HTTPException(status_code=500, detail="Failed to cleanup old backups")


@router.get("/info/{backup_id}", response_model=BackupInfoResponse)
async def get_backup_info(
    backup_id: str,
    current_user: AuthToken = Depends(get_current_user)
) -> BackupInfoResponse:
    """
    Get detailed information about a specific backup
    
    Args:
        backup_id: ID of the backup
        current_user: Authenticated user token
    
    Returns:
        BackupInfoResponse: Detailed backup information
    """
    try:
        backup_service = get_backup_service()
        backup_info = backup_service.migration_manager.get_backup_info(backup_id)
        
        if not backup_info:
            raise HTTPException(status_code=404, detail="Backup not found")
        
        return BackupInfoResponse(
            backup_id=backup_info.backup_id,
            filename=backup_info.filename,
            size_mb=round(backup_info.size_bytes / (1024 * 1024), 2),
            created_at=backup_info.created_at.isoformat(),
            database_version=backup_info.database_version,
            backup_type=backup_info.backup_type,
            compression=backup_info.compression,
            metadata=backup_info.metadata
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting backup info for {backup_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get backup information")