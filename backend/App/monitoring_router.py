"""
Monitoring Dashboard Router
API endpoints for agent performance monitoring and system health metrics
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional
from datetime import datetime, timedelta

from backend.App.agent_performance_tracker import get_performance_tracker
from backend.App.agent_performance_models import (
    AgentType
)
from backend.App.auth_middleware import get_current_user, AuthToken
from backend.App.api_models import create_success_response
from backend.App.logging_config import get_logger, LogCategory

logger = get_logger(__name__, LogCategory.PERFORMANCE)

# Create router
router = APIRouter(
    prefix="/api/monitoring",
    tags=["monitoring"],
    responses={404: {"description": "Not found"}}
)

@router.get("/health/agents")
async def get_agent_health(
    agent_type: Optional[str] = Query(None, description="Specific agent type to monitor"),
    time_window_minutes: int = Query(60, description="Time window in minutes", ge=5, le=1440),
    current_user: AuthToken = Depends(get_current_user)
):
    """Get health metrics for agents"""
    try:
        performance_tracker = get_performance_tracker()
        
        # Parse agent type if provided
        perf_agent_type = None
        if agent_type:
            try:
                perf_agent_type = AgentType(agent_type)
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid agent type: {agent_type}")
        
        # Get health snapshots
        health_snapshots = await performance_tracker.get_agent_health(
            agent_type=perf_agent_type,
            time_window_minutes=time_window_minutes
        )
        
        # Convert to dict format
        health_data = []
        for snapshot in health_snapshots:
            health_data.append({
                "agent_type": snapshot.agent_type.value,
                "time_window_minutes": snapshot.time_window_minutes,
                "total_requests": snapshot.total_requests,
                "successful_requests": snapshot.successful_requests,
                "failed_requests": snapshot.failed_requests,
                "cache_hits": snapshot.cache_hits,
                "performance_metrics": {
                    "avg_latency_ms": round(snapshot.avg_latency_ms, 2),
                    "p95_latency_ms": round(snapshot.p95_latency_ms, 2),
                    "p99_latency_ms": round(snapshot.p99_latency_ms, 2),
                    "max_latency_ms": round(snapshot.max_latency_ms, 2)
                },
                "cost_metrics": {
                    "total_input_tokens": snapshot.total_input_tokens,
                    "total_output_tokens": snapshot.total_output_tokens,
                    "total_cost_estimate": round(snapshot.total_cost_estimate, 4)
                },
                "error_metrics": {
                    "error_rate": round(snapshot.error_rate, 3),
                    "timeout_rate": round(snapshot.timeout_rate, 3),
                    "rate_limit_rate": round(snapshot.rate_limit_rate, 3)
                },
                "cache_metrics": {
                    "cache_hit_rate": round(snapshot.cache_hit_rate, 3),
                    "avg_cache_lookup_time_ms": round(snapshot.avg_cache_lookup_time_ms, 2)
                },
                "health_score": round(snapshot.health_score, 1),
                "timestamp": snapshot.timestamp.isoformat()
            })
        
        logger.info(
            f"Retrieved health data for {len(health_data)} agents",
            extra={
                'category': LogCategory.MONITORING.value,
                'user_id': current_user.user_id,
                'metadata': {
                    'agent_type': agent_type,
                    'time_window_minutes': time_window_minutes,
                    'agents_count': len(health_data)
                }
            }
        )
        
        return create_success_response(
            "Agent health metrics retrieved successfully",
            {
                "agents": health_data,
                "summary": {
                    "total_agents": len(health_data),
                    "time_window_minutes": time_window_minutes,
                    "avg_health_score": round(
                        sum(agent["health_score"] for agent in health_data) / len(health_data)
                        if health_data else 0, 1
                    )
                }
            }
        )
        
    except Exception as e:
        logger.error(
            f"Failed to retrieve agent health: {e}",
            extra={
                'category': LogCategory.ERROR.value,
                'user_id': current_user.user_id,
                'metadata': {
                    'error_type': type(e).__name__,
                    'error_message': str(e)
                }
            },
            exc_info=True
        )
        raise HTTPException(status_code=500, detail="Failed to retrieve agent health metrics")

@router.get("/metrics/real-time")
async def get_real_time_metrics(
    current_user: AuthToken = Depends(get_current_user)
):
    """Get real-time system performance metrics"""
    try:
        performance_tracker = get_performance_tracker()
        
        # Get recent health data (last 5 minutes)
        recent_health = await performance_tracker.get_agent_health(time_window_minutes=5)
        
        # Calculate system-wide metrics
        total_requests = sum(agent.total_requests for agent in recent_health)
        total_errors = sum(agent.failed_requests for agent in recent_health)
        total_cost = sum(agent.total_cost_estimate for agent in recent_health)
        avg_latency = (
            sum(agent.avg_latency_ms * agent.total_requests for agent in recent_health) / 
            total_requests if total_requests > 0 else 0
        )
        
        # Agent status summary
        agent_status = {}
        for agent in recent_health:
            agent_status[agent.agent_type.value] = {
                "health_score": round(agent.health_score, 1),
                "status": "healthy" if agent.health_score >= 80 else "degraded" if agent.health_score >= 60 else "unhealthy",
                "requests": agent.total_requests,
                "avg_latency_ms": round(agent.avg_latency_ms, 2),
                "error_rate": round(agent.error_rate, 3)
            }
        
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "time_window_minutes": 5,
            "system_overview": {
                "total_requests": total_requests,
                "total_errors": total_errors,
                "error_rate": round(total_errors / total_requests if total_requests > 0 else 0, 3),
                "avg_latency_ms": round(avg_latency, 2),
                "total_cost_last_5min": round(total_cost, 4)
            },
            "agent_status": agent_status,
            "system_health": {
                "overall_score": round(
                    sum(agent.health_score for agent in recent_health) / len(recent_health)
                    if recent_health else 0, 1
                ),
                "healthy_agents": len([a for a in recent_health if a.health_score >= 80]),
                "total_agents": len(recent_health)
            }
        }
        
        return create_success_response("Real-time metrics retrieved", metrics)
        
    except Exception as e:
        logger.error(f"Failed to get real-time metrics: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve real-time metrics")

@router.get("/alerts")
async def get_performance_alerts(
    severity: Optional[str] = Query(None, description="Filter by severity"),
    agent_type: Optional[str] = Query(None, description="Filter by agent type"),
    limit: int = Query(50, description="Maximum number of alerts", ge=1, le=500),
    acknowledged: Optional[bool] = Query(None, description="Filter by acknowledgment status"),
    current_user: AuthToken = Depends(get_current_user)
):
    """Get performance alerts"""
    try:
        from backend.App.database import get_db_connection
        
        # Build query
        query = """
            SELECT 
                alert_id, timestamp, severity, alert_type, agent_type,
                metric_name, current_value, threshold_value, description,
                recommendation, time_window_minutes, acknowledged, resolved
            FROM performance_alerts
            WHERE 1=1
        """
        params = []
        
        if severity:
            query += " AND severity = ?"
            params.append(severity)
        
        if agent_type:
            query += " AND agent_type = ?"
            params.append(agent_type)
        
        if acknowledged is not None:
            query += " AND acknowledged = ?"
            params.append(acknowledged)
        
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
        
        alerts = []
        for row in rows:
            (alert_id, timestamp, severity, alert_type, agent_type_val,
             metric_name, current_value, threshold_value, description,
             recommendation, time_window_minutes, acknowledged, resolved) = row
            
            alerts.append({
                "alert_id": alert_id,
                "timestamp": timestamp,
                "severity": severity,
                "alert_type": alert_type,
                "agent_type": agent_type_val,
                "metric": {
                    "name": metric_name,
                    "current_value": current_value,
                    "threshold_value": threshold_value
                },
                "description": description,
                "recommendation": recommendation,
                "time_window_minutes": time_window_minutes,
                "status": {
                    "acknowledged": bool(acknowledged),
                    "resolved": bool(resolved)
                }
            })
        
        return create_success_response(
            f"Retrieved {len(alerts)} alerts",
            {
                "alerts": alerts,
                "total_count": len(alerts),
                "filters_applied": {
                    "severity": severity,
                    "agent_type": agent_type,
                    "acknowledged": acknowledged
                }
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to get alerts: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve alerts")

@router.post("/alerts/{alert_id}/acknowledge")
async def acknowledge_alert(
    alert_id: str,
    current_user: AuthToken = Depends(get_current_user)
):
    """Acknowledge a performance alert"""
    try:
        from backend.App.database import get_db_connection
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Check if alert exists
            cursor.execute("SELECT alert_id FROM performance_alerts WHERE alert_id = ?", (alert_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Alert not found")
            
            # Acknowledge the alert
            cursor.execute("""
                UPDATE performance_alerts 
                SET acknowledged = 1, acknowledged_by = ?
                WHERE alert_id = ?
            """, (current_user.user_id, alert_id))
            
            conn.commit()
        
        logger.info(
            f"Alert acknowledged: {alert_id}",
            extra={
                'category': LogCategory.MONITORING.value,
                'user_id': current_user.user_id,
                'metadata': {'alert_id': alert_id}
            }
        )
        
        return create_success_response("Alert acknowledged successfully")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to acknowledge alert: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to acknowledge alert")

@router.get("/costs/analysis")
async def get_cost_analysis(
    time_window_hours: int = Query(24, description="Time window in hours", ge=1, le=168),
    group_by: str = Query("agent", description="Group by: agent, user, hour"),
    current_user: AuthToken = Depends(get_current_user)
):
    """Get cost analysis and breakdown"""
    try:
        from backend.App.database import get_db_connection
        
        start_time = datetime.now() - timedelta(hours=time_window_hours)
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            if group_by == "agent":
                cursor.execute("""
                    SELECT 
                        agent_type,
                        COUNT(*) as total_requests,
                        SUM(input_tokens) as total_input_tokens,
                        SUM(output_tokens) as total_output_tokens,
                        SUM(cost_estimate) as total_cost,
                        AVG(cost_estimate) as avg_cost_per_request,
                        SUM(CASE WHEN cache_hit = 1 THEN 1 ELSE 0 END) as cache_hits
                    FROM agent_performance_metrics 
                    WHERE timestamp >= ?
                    GROUP BY agent_type
                    ORDER BY total_cost DESC
                """, (start_time,))
            
            elif group_by == "user":
                cursor.execute("""
                    SELECT 
                        user_id,
                        COUNT(*) as total_requests,
                        SUM(cost_estimate) as total_cost,
                        AVG(cost_estimate) as avg_cost_per_request,
                        COUNT(DISTINCT agent_type) as agents_used
                    FROM agent_performance_metrics 
                    WHERE timestamp >= ?
                    GROUP BY user_id
                    ORDER BY total_cost DESC
                    LIMIT 20
                """, (start_time,))
            
            elif group_by == "hour":
                cursor.execute("""
                    SELECT 
                        strftime('%Y-%m-%d %H:00:00', timestamp) as hour,
                        COUNT(*) as total_requests,
                        SUM(cost_estimate) as total_cost,
                        AVG(total_latency_ms) as avg_latency_ms
                    FROM agent_performance_metrics 
                    WHERE timestamp >= ?
                    GROUP BY strftime('%Y-%m-%d %H:00:00', timestamp)
                    ORDER BY hour DESC
                """, (start_time,))
            
            rows = cursor.fetchall()
        
        # Format results based on grouping
        if group_by == "agent":
            cost_data = []
            for row in rows:
                (agent_type, total_requests, total_input_tokens, total_output_tokens,
                 total_cost, avg_cost_per_request, cache_hits) = row
                
                cost_data.append({
                    "agent_type": agent_type,
                    "metrics": {
                        "total_requests": total_requests,
                        "total_input_tokens": total_input_tokens or 0,
                        "total_output_tokens": total_output_tokens or 0,
                        "total_cost": round(total_cost or 0, 4),
                        "avg_cost_per_request": round(avg_cost_per_request or 0, 4),
                        "cache_hits": cache_hits or 0,
                        "cache_hit_rate": round((cache_hits or 0) / total_requests, 3) if total_requests > 0 else 0
                    }
                })
        
        elif group_by == "user":
            cost_data = []
            for row in rows:
                user_id, total_requests, total_cost, avg_cost_per_request, agents_used = row
                cost_data.append({
                    "user_id": user_id,
                    "total_requests": total_requests,
                    "total_cost": round(total_cost or 0, 4),
                    "avg_cost_per_request": round(avg_cost_per_request or 0, 4),
                    "agents_used": agents_used
                })
        
        elif group_by == "hour":
            cost_data = []
            for row in rows:
                hour, total_requests, total_cost, avg_latency_ms = row
                cost_data.append({
                    "hour": hour,
                    "total_requests": total_requests,
                    "total_cost": round(total_cost or 0, 4),
                    "avg_latency_ms": round(avg_latency_ms or 0, 2)
                })
        
        # Calculate summary statistics
        total_cost = sum(item.get("total_cost", item.get("metrics", {}).get("total_cost", 0)) for item in cost_data)
        total_requests = sum(item.get("total_requests", item.get("metrics", {}).get("total_requests", 0)) for item in cost_data)
        
        return create_success_response(
            "Cost analysis retrieved successfully",
            {
                "cost_breakdown": cost_data,
                "summary": {
                    "time_window_hours": time_window_hours,
                    "group_by": group_by,
                    "total_cost": round(total_cost, 4),
                    "total_requests": total_requests,
                    "avg_cost_per_request": round(total_cost / total_requests if total_requests > 0 else 0, 4),
                    "projected_daily_cost": round(total_cost * (24 / time_window_hours), 4),
                    "projected_monthly_cost": round(total_cost * (24 * 30 / time_window_hours), 4)
                }
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to get cost analysis: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve cost analysis")

@router.get("/performance/trends")
async def get_performance_trends(
    metric: str = Query("latency", description="Metric to analyze: latency, error_rate, cost, throughput"),
    time_window_hours: int = Query(24, description="Time window in hours", ge=1, le=168),
    interval_minutes: int = Query(60, description="Data interval in minutes", ge=5, le=1440),
    agent_type: Optional[str] = Query(None, description="Filter by agent type"),
    current_user: AuthToken = Depends(get_current_user)
):
    """Get performance trends over time"""
    try:
        from backend.App.database import get_db_connection
        
        start_time = datetime.now() - timedelta(hours=time_window_hours)
        
        # Build interval format for SQLite
        interval_format = f"strftime('%Y-%m-%d %H:%M:00', datetime(timestamp, '-' || (strftime('%M', timestamp) % {interval_minutes}) || ' minutes'))"
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Build query based on metric
            if metric == "latency":
                select_metric = "AVG(total_latency_ms) as metric_value"
            elif metric == "error_rate":
                select_metric = "CAST(SUM(CASE WHEN status = 'error' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) as metric_value"
            elif metric == "cost":
                select_metric = "SUM(cost_estimate) as metric_value"
            elif metric == "throughput":
                select_metric = "COUNT(*) as metric_value"
            else:
                raise HTTPException(status_code=400, detail=f"Invalid metric: {metric}")
            
            query = f"""
                SELECT 
                    {interval_format} as time_interval,
                    {select_metric},
                    COUNT(*) as total_requests
                FROM agent_performance_metrics 
                WHERE timestamp >= ?
            """
            params = [start_time]
            
            if agent_type:
                query += " AND agent_type = ?"
                params.append(agent_type)
            
            query += f" GROUP BY {interval_format} ORDER BY time_interval"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
        
        # Format trend data
        trend_data = []
        for row in rows:
            time_interval, metric_value, total_requests = row
            trend_data.append({
                "timestamp": time_interval,
                "metric_value": round(metric_value or 0, 4),
                "total_requests": total_requests
            })
        
        # Calculate trend analysis
        if len(trend_data) >= 2:
            recent_avg = sum(point["metric_value"] for point in trend_data[-3:]) / min(3, len(trend_data))
            early_avg = sum(point["metric_value"] for point in trend_data[:3]) / min(3, len(trend_data))
            trend_direction = "improving" if recent_avg < early_avg and metric != "throughput" else "degrading" if recent_avg > early_avg and metric != "throughput" else "stable"
            if metric == "throughput":
                trend_direction = "improving" if recent_avg > early_avg else "degrading" if recent_avg < early_avg else "stable"
        else:
            trend_direction = "insufficient_data"
        
        return create_success_response(
            "Performance trends retrieved successfully",
            {
                "metric": metric,
                "time_window_hours": time_window_hours,
                "interval_minutes": interval_minutes,
                "agent_type": agent_type,
                "trend_data": trend_data,
                "analysis": {
                    "trend_direction": trend_direction,
                    "data_points": len(trend_data),
                    "current_value": trend_data[-1]["metric_value"] if trend_data else 0,
                    "min_value": min(point["metric_value"] for point in trend_data) if trend_data else 0,
                    "max_value": max(point["metric_value"] for point in trend_data) if trend_data else 0,
                    "avg_value": sum(point["metric_value"] for point in trend_data) / len(trend_data) if trend_data else 0
                }
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get performance trends: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve performance trends")

@router.get("/dashboard")
async def get_monitoring_dashboard(
    current_user: AuthToken = Depends(get_current_user)
):
    """Get comprehensive monitoring dashboard data"""
    try:
        # Get multiple metrics in parallel
        from concurrent.futures import ThreadPoolExecutor
        import asyncio
        
        async def get_dashboard_data():
            performance_tracker = get_performance_tracker()
            
            # Get recent health data
            agent_health = await performance_tracker.get_agent_health(time_window_minutes=60)
            recent_health = await performance_tracker.get_agent_health(time_window_minutes=5)
            
            return agent_health, recent_health
        
        agent_health, recent_health = await get_dashboard_data()
        
        # Calculate dashboard metrics
        total_requests_1h = sum(agent.total_requests for agent in agent_health)
        total_requests_5m = sum(agent.total_requests for agent in recent_health)
        total_errors_1h = sum(agent.failed_requests for agent in agent_health)
        total_cost_1h = sum(agent.total_cost_estimate for agent in agent_health)
        
        # Agent status overview
        agent_overview = {}
        for agent in agent_health:
            agent_overview[agent.agent_type.value] = {
                "health_score": round(agent.health_score, 1),
                "status": "healthy" if agent.health_score >= 80 else "warning" if agent.health_score >= 60 else "critical",
                "requests_1h": agent.total_requests,
                "avg_latency_ms": round(agent.avg_latency_ms, 2),
                "error_rate": round(agent.error_rate, 3),
                "cache_hit_rate": round(agent.cache_hit_rate, 3),
                "cost_1h": round(agent.total_cost_estimate, 4)
            }
        
        # System overview
        system_overview = {
            "overall_health": round(
                sum(agent.health_score for agent in agent_health) / len(agent_health)
                if agent_health else 0, 1
            ),
            "total_requests_1h": total_requests_1h,
            "requests_per_minute": round(total_requests_5m / 5, 1),
            "error_rate_1h": round(total_errors_1h / total_requests_1h if total_requests_1h > 0 else 0, 3),
            "total_cost_1h": round(total_cost_1h, 4),
            "projected_daily_cost": round(total_cost_1h * 24, 4),
            "active_agents": len([a for a in agent_health if a.total_requests > 0])
        }
        
        # Recent activity
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) 
                FROM performance_alerts 
                WHERE timestamp >= ? AND acknowledged = 0
            """, (datetime.now() - timedelta(hours=1),))
            unacknowledged_alerts = cursor.fetchone()[0]
        
        dashboard_data = {
            "timestamp": datetime.now().isoformat(),
            "system_overview": system_overview,
            "agent_overview": agent_overview,
            "alerts": {
                "unacknowledged_count": unacknowledged_alerts,
                "status": "ok" if unacknowledged_alerts == 0 else "warning" if unacknowledged_alerts < 5 else "critical"
            },
            "last_updated": datetime.now().isoformat()
        }
        
        return create_success_response("Dashboard data retrieved successfully", dashboard_data)
        
    except Exception as e:
        logger.error(f"Failed to get dashboard data: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve dashboard data")

@router.get("/optimization/recommendations")
async def get_optimization_recommendations(
    time_window_hours: int = Query(24, description="Time window for analysis", ge=1, le=168),
    current_user: AuthToken = Depends(get_current_user)
):
    """Get cost optimization recommendations"""
    try:
        from backend.App.cost_optimizer import get_cost_optimizer
        
        cost_optimizer = get_cost_optimizer()
        recommendations = await cost_optimizer.generate_recommendations(time_window_hours)
        
        # Format recommendations for API response
        formatted_recommendations = []
        for rec in recommendations:
            formatted_recommendations.append({
                "recommendation_id": rec.recommendation_id,
                "type": rec.type,
                "priority": rec.priority,
                "description": rec.description,
                "estimated_savings_per_day": round(rec.estimated_savings_per_day, 4),
                "current_cost_per_day": round(rec.current_cost_per_day, 4),
                "projected_cost_per_day": round(rec.projected_cost_per_day, 4),
                "implementation_effort": rec.implementation_effort,
                "affected_agents": [agent.value for agent in rec.affected_agents],
                "implementation_steps": rec.implementation_steps,
                "risks": rec.risks,
                "implemented": rec.implemented,
                "timestamp": rec.timestamp.isoformat()
            })
        
        # Calculate summary statistics
        total_potential_savings = sum(rec.estimated_savings_per_day for rec in recommendations)
        total_current_cost = sum(rec.current_cost_per_day for rec in recommendations if rec.current_cost_per_day > 0)
        
        return create_success_response(
            "Cost optimization recommendations retrieved successfully",
            {
                "recommendations": formatted_recommendations,
                "summary": {
                    "total_recommendations": len(recommendations),
                    "total_potential_daily_savings": round(total_potential_savings, 4),
                    "total_potential_monthly_savings": round(total_potential_savings * 30, 4),
                    "current_daily_cost": round(total_current_cost, 4),
                    "max_savings_percentage": round(
                        (total_potential_savings / total_current_cost * 100) if total_current_cost > 0 else 0, 1
                    ),
                    "time_window_hours": time_window_hours
                }
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to get optimization recommendations: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve optimization recommendations")

@router.get("/optimization/analysis")
async def get_cost_analysis(
    time_window_hours: int = Query(24, description="Time window for analysis", ge=1, le=168),
    current_user: AuthToken = Depends(get_current_user)
):
    """Get detailed cost analysis by agent"""
    try:
        from backend.App.cost_optimizer import get_cost_optimizer
        
        cost_optimizer = get_cost_optimizer()
        cost_analyses = await cost_optimizer.analyze_costs(time_window_hours)
        
        # Format analysis results
        formatted_analyses = []
        for analysis in cost_analyses:
            formatted_analyses.append({
                "agent_type": analysis.agent_type.value if analysis.agent_type else "system",
                "time_window_hours": analysis.time_window_hours,
                "metrics": {
                    "total_cost": round(analysis.total_cost, 4),
                    "total_requests": analysis.total_requests,
                    "avg_cost_per_request": round(analysis.avg_cost_per_request, 6),
                    "projected_daily_cost": round(analysis.total_cost * (24 / analysis.time_window_hours), 4),
                    "projected_monthly_cost": round(analysis.total_cost * (24 * 30 / analysis.time_window_hours), 4)
                },
                "analysis": {
                    "cost_trend": analysis.cost_trend,
                    "primary_cost_drivers": analysis.primary_cost_drivers,
                    "optimization_potential_percent": round(analysis.optimization_potential * 100, 1)
                }
            })
        
        # Calculate system totals
        total_cost = sum(a.total_cost for a in cost_analyses)
        total_requests = sum(a.total_requests for a in cost_analyses)
        avg_optimization_potential = (
            sum(a.optimization_potential for a in cost_analyses) / len(cost_analyses)
            if cost_analyses else 0
        )
        
        return create_success_response(
            "Cost analysis retrieved successfully",
            {
                "agent_analyses": formatted_analyses,
                "system_summary": {
                    "total_cost": round(total_cost, 4),
                    "total_requests": total_requests,
                    "avg_cost_per_request": round(total_cost / total_requests if total_requests > 0 else 0, 6),
                    "projected_daily_cost": round(total_cost * (24 / time_window_hours), 4),
                    "projected_monthly_cost": round(total_cost * (24 * 30 / time_window_hours), 4),
                    "avg_optimization_potential_percent": round(avg_optimization_potential * 100, 1),
                    "time_window_hours": time_window_hours
                }
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to get cost analysis: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve cost analysis")