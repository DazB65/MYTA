"""
Security Dashboard API Router
Provides endpoints for security monitoring and metrics
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import sqlite3
import json

from .security_monitoring import security_monitor, SecurityEvent, SecurityMetrics
from .dependency_scanner import dependency_scanner, run_scheduled_scan, get_dependency_status
from .auth_middleware import get_current_user, AuthToken

router = APIRouter(prefix="/api/security", tags=["security"])

@router.get("/metrics")
async def get_security_metrics(
    hours: int = Query(24, ge=1, le=168),  # 1 hour to 1 week
    current_user: AuthToken = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get security metrics for the specified time period"""
    try:
        metrics = security_monitor.get_security_metrics(hours)
        
        return {
            "success": True,
            "data": {
                "timestamp": metrics.timestamp.isoformat(),
                "time_period_hours": hours,
                "metrics": {
                    "total_requests": metrics.total_requests,
                    "failed_auth_attempts": metrics.failed_auth_attempts,
                    "rate_limited_requests": metrics.rate_limited_requests,
                    "suspicious_requests": metrics.suspicious_requests,
                    "blocked_requests": metrics.blocked_requests,
                    "unique_ips": metrics.unique_ips,
                    "auth_success_rate": round(metrics.auth_success_rate * 100, 2),
                    "avg_response_time": metrics.avg_response_time,
                    "security_score": round(metrics.security_score, 1)
                },
                "status": _get_security_status(metrics.security_score)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get security metrics: {str(e)}")

@router.get("/events")
async def get_security_events(
    hours: int = Query(24, ge=1, le=168),
    event_type: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    current_user: AuthToken = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get recent security events"""
    try:
        since_time = datetime.now() - timedelta(hours=hours)
        
        # Build query
        query = "SELECT * FROM security_events WHERE timestamp >= ?"
        params = [since_time]
        
        if event_type:
            query += " AND event_type = ?"
            params.append(event_type)
        
        if severity:
            query += " AND severity = ?"
            params.append(severity)
        
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        with sqlite3.connect(security_monitor.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(query, params)
            events = []
            
            for row in cursor.fetchall():
                events.append({
                    "id": row["id"],
                    "timestamp": row["timestamp"],
                    "event_type": row["event_type"],
                    "severity": row["severity"],
                    "user_id": row["user_id"],
                    "ip_address": row["ip_address"],
                    "user_agent": row["user_agent"],
                    "details": json.loads(row["details"]) if row["details"] else {},
                    "resolved": bool(row["resolved"])
                })
        
        return {
            "success": True,
            "data": {
                "events": events,
                "total_count": len(events),
                "filters": {
                    "hours": hours,
                    "event_type": event_type,
                    "severity": severity,
                    "limit": limit
                }
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get security events: {str(e)}")

@router.get("/threats")
async def get_threat_summary(
    hours: int = Query(24, ge=1, le=168),
    current_user: AuthToken = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get threat summary and analysis"""
    try:
        since_time = datetime.now() - timedelta(hours=hours)
        
        with sqlite3.connect(security_monitor.db_path) as conn:
            # Get threat patterns
            cursor = conn.execute("""
                SELECT 
                    ip_address,
                    COUNT(*) as event_count,
                    COUNT(DISTINCT event_type) as event_types,
                    MAX(severity) as max_severity,
                    MIN(timestamp) as first_seen,
                    MAX(timestamp) as last_seen
                FROM security_events 
                WHERE timestamp >= ? AND severity IN ('high', 'critical')
                GROUP BY ip_address
                ORDER BY event_count DESC
                LIMIT 20
            """, (since_time,))
            
            threat_ips = []
            for row in cursor.fetchall():
                threat_ips.append({
                    "ip_address": row[0],
                    "event_count": row[1],
                    "event_types": row[2],
                    "max_severity": row[3],
                    "first_seen": row[4],
                    "last_seen": row[5]
                })
            
            # Get event type distribution
            cursor = conn.execute("""
                SELECT event_type, COUNT(*) as count
                FROM security_events 
                WHERE timestamp >= ?
                GROUP BY event_type
                ORDER BY count DESC
            """, (since_time,))
            
            event_distribution = dict(cursor.fetchall())
            
            # Get severity distribution
            cursor = conn.execute("""
                SELECT severity, COUNT(*) as count
                FROM security_events 
                WHERE timestamp >= ?
                GROUP BY severity
                ORDER BY count DESC
            """, (since_time,))
            
            severity_distribution = dict(cursor.fetchall())
        
        return {
            "success": True,
            "data": {
                "threat_ips": threat_ips,
                "event_distribution": event_distribution,
                "severity_distribution": severity_distribution,
                "analysis_period_hours": hours,
                "recommendations": _generate_security_recommendations(threat_ips, event_distribution)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get threat summary: {str(e)}")

@router.post("/events/{event_id}/resolve")
async def resolve_security_event(
    event_id: int,
    current_user: AuthToken = Depends(get_current_user)
) -> Dict[str, Any]:
    """Mark a security event as resolved"""
    try:
        with sqlite3.connect(security_monitor.db_path) as conn:
            cursor = conn.execute(
                "UPDATE security_events SET resolved = TRUE WHERE id = ?",
                (event_id,)
            )
            
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Security event not found")
            
            conn.commit()
        
        return {
            "success": True,
            "message": f"Security event {event_id} marked as resolved"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to resolve security event: {str(e)}")

@router.get("/dashboard")
async def get_security_dashboard(
    current_user: AuthToken = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get comprehensive security dashboard data"""
    try:
        # Get metrics for different time periods
        metrics_1h = security_monitor.get_security_metrics(1)
        metrics_24h = security_monitor.get_security_metrics(24)
        metrics_7d = security_monitor.get_security_metrics(168)
        
        # Get recent critical events
        since_time = datetime.now() - timedelta(hours=24)
        with sqlite3.connect(security_monitor.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM security_events 
                WHERE timestamp >= ? AND severity IN ('high', 'critical')
                ORDER BY timestamp DESC 
                LIMIT 10
            """, (since_time,))
            
            critical_events = []
            for row in cursor.fetchall():
                critical_events.append({
                    "id": row["id"],
                    "timestamp": row["timestamp"],
                    "event_type": row["event_type"],
                    "severity": row["severity"],
                    "ip_address": row["ip_address"],
                    "details": json.loads(row["details"]) if row["details"] else {}
                })
        
        return {
            "success": True,
            "data": {
                "overview": {
                    "current_security_score": round(metrics_1h.security_score, 1),
                    "score_trend": _calculate_score_trend(metrics_1h.security_score, metrics_24h.security_score),
                    "status": _get_security_status(metrics_1h.security_score),
                    "last_updated": datetime.now().isoformat()
                },
                "metrics": {
                    "1_hour": _format_metrics(metrics_1h),
                    "24_hours": _format_metrics(metrics_24h),
                    "7_days": _format_metrics(metrics_7d)
                },
                "critical_events": critical_events,
                "alerts": _get_active_alerts()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get security dashboard: {str(e)}")

def _get_security_status(score: float) -> str:
    """Get security status based on score"""
    if score >= 90:
        return "excellent"
    elif score >= 75:
        return "good"
    elif score >= 60:
        return "fair"
    elif score >= 40:
        return "poor"
    else:
        return "critical"

def _calculate_score_trend(current: float, previous: float) -> str:
    """Calculate score trend"""
    diff = current - previous
    if abs(diff) < 2:
        return "stable"
    elif diff > 0:
        return "improving"
    else:
        return "declining"

def _format_metrics(metrics: SecurityMetrics) -> Dict[str, Any]:
    """Format metrics for API response"""
    return {
        "total_requests": metrics.total_requests,
        "failed_auth_attempts": metrics.failed_auth_attempts,
        "rate_limited_requests": metrics.rate_limited_requests,
        "suspicious_requests": metrics.suspicious_requests,
        "blocked_requests": metrics.blocked_requests,
        "unique_ips": metrics.unique_ips,
        "auth_success_rate": round(metrics.auth_success_rate * 100, 2),
        "security_score": round(metrics.security_score, 1)
    }

def _generate_security_recommendations(threat_ips: List[Dict], event_distribution: Dict) -> List[str]:
    """Generate security recommendations based on threat analysis"""
    recommendations = []
    
    if len(threat_ips) > 5:
        recommendations.append("Consider implementing IP-based blocking for repeat offenders")
    
    if event_distribution.get('auth_failure', 0) > 50:
        recommendations.append("High authentication failure rate detected - consider implementing CAPTCHA")
    
    if event_distribution.get('rate_limit', 0) > 100:
        recommendations.append("Frequent rate limiting - consider adjusting rate limits or implementing progressive delays")
    
    if not recommendations:
        recommendations.append("Security posture is good - continue monitoring")
    
    return recommendations

def _get_active_alerts() -> List[Dict[str, Any]]:
    """Get active security alerts"""
    # This would integrate with an alerting system
    # For now, return empty list
    return []

@router.get("/dependencies")
async def get_dependency_status_endpoint(
    current_user: AuthToken = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get current dependency security status"""
    try:
        status = await get_dependency_status()
        return {
            "success": True,
            "data": status
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get dependency status: {str(e)}")

@router.post("/dependencies/scan")
async def run_dependency_scan(
    current_user: AuthToken = Depends(get_current_user)
) -> Dict[str, Any]:
    """Run a new dependency vulnerability scan"""
    try:
        result = await run_scheduled_scan()

        if result:
            return {
                "success": True,
                "data": {
                    "scan_completed": True,
                    "timestamp": result.timestamp.isoformat(),
                    "vulnerabilities_found": result.vulnerabilities_found,
                    "total_packages": result.total_packages,
                    "status": result.status,
                    "scan_duration": round(result.scan_duration, 2)
                }
            }
        else:
            raise HTTPException(status_code=500, detail="Dependency scan failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to run dependency scan: {str(e)}")

@router.get("/dependencies/history")
async def get_dependency_scan_history(
    limit: int = Query(10, ge=1, le=50),
    current_user: AuthToken = Depends(get_current_user)
) -> Dict[str, Any]:
    """Get dependency scan history"""
    try:
        history = dependency_scanner.get_scan_history(limit)
        return {
            "success": True,
            "data": {
                "scan_history": history,
                "total_scans": len(history)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get scan history: {str(e)}")
