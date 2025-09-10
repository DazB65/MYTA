#!/usr/bin/env python3
"""
Security Monitoring Dashboard for MYTA Application
Provides real-time security metrics and alerting status
"""

import os
import sys
import json
import asyncio
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Any
import sqlite3
from pathlib import Path

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

try:
    from App.security_alerting import security_alerting, AlertType, AlertSeverity
    from App.health_checks import get_health_checker
    from App.monitoring_middleware import get_health_middleware
except ImportError as e:
    print(f"Warning: Could not import backend modules: {e}")
    print("Running in standalone mode...")


class SecurityDashboard:
    """Security monitoring dashboard"""
    
    def __init__(self, db_path: str = "Vidalytics.db"):
        self.db_path = db_path
        self.metrics = {}
    
    def get_database_connection(self):
        """Get database connection"""
        if os.path.exists(self.db_path):
            return sqlite3.connect(self.db_path)
        else:
            print(f"Warning: Database {self.db_path} not found")
            return None
    
    async def collect_security_metrics(self) -> Dict[str, Any]:
        """Collect security metrics from various sources"""
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'authentication': await self._get_auth_metrics(),
            'rate_limiting': await self._get_rate_limit_metrics(),
            'api_health': await self._get_api_health_metrics(),
            'recent_alerts': await self._get_recent_alerts(),
            'system_health': await self._get_system_health(),
            'security_score': 0  # Will be calculated
        }
        
        # Calculate overall security score
        metrics['security_score'] = self._calculate_security_score(metrics)
        
        return metrics
    
    async def _get_auth_metrics(self) -> Dict[str, Any]:
        """Get authentication-related metrics"""
        conn = self.get_database_connection()
        if not conn:
            return {'error': 'Database not available'}
        
        try:
            cursor = conn.cursor()
            
            # Get authentication failures in last 24 hours
            yesterday = datetime.now() - timedelta(days=1)
            
            # This would need to be adapted based on your actual database schema
            auth_metrics = {
                'failed_logins_24h': 0,
                'successful_logins_24h': 0,
                'unique_ips_24h': 0,
                'blocked_ips': 0,
                'suspicious_patterns': []
            }
            
            # Example queries (adapt to your schema)
            try:
                cursor.execute("""
                    SELECT COUNT(*) FROM audit_log 
                    WHERE action = 'login_failed' 
                    AND timestamp > ?
                """, (yesterday.isoformat(),))
                auth_metrics['failed_logins_24h'] = cursor.fetchone()[0]
            except sqlite3.OperationalError:
                pass  # Table might not exist
            
            return auth_metrics
            
        except Exception as e:
            return {'error': str(e)}
        finally:
            conn.close()
    
    async def _get_rate_limit_metrics(self) -> Dict[str, Any]:
        """Get rate limiting metrics"""
        return {
            'requests_blocked_24h': 0,
            'top_blocked_ips': [],
            'rate_limit_violations': 0,
            'current_rate_limits': {
                'per_minute': 60,
                'per_hour': 1000
            }
        }
    
    async def _get_api_health_metrics(self) -> Dict[str, Any]:
        """Get API health metrics"""
        try:
            # Try to get health from the health checker if available
            if 'get_health_checker' in globals():
                health_checker = get_health_checker()
                health_snapshot = await health_checker.run_all_checks()
                
                return {
                    'overall_status': health_snapshot.overall_status.value,
                    'healthy_components': len([c for c in health_snapshot.components if c.status.value == 'healthy']),
                    'total_components': len(health_snapshot.components),
                    'response_time_avg': health_snapshot.response_time_ms,
                    'last_check': health_snapshot.timestamp
                }
            else:
                return {
                    'overall_status': 'unknown',
                    'healthy_components': 0,
                    'total_components': 0,
                    'response_time_avg': 0,
                    'last_check': datetime.now().isoformat()
                }
        except Exception as e:
            return {'error': str(e)}
    
    async def _get_recent_alerts(self) -> List[Dict[str, Any]]:
        """Get recent security alerts"""
        try:
            if 'security_alerting' in globals():
                # Get last 10 alerts
                recent = security_alerting.recent_alerts[-10:]
                return [alert.to_dict() for alert in recent]
            else:
                return []
        except Exception as e:
            return [{'error': str(e)}]
    
    async def _get_system_health(self) -> Dict[str, Any]:
        """Get system health metrics"""
        try:
            if 'get_health_middleware' in globals():
                health_middleware = get_health_middleware()
                stats = health_middleware.get_health_stats()
                return stats
            else:
                return {
                    'uptime_seconds': 0,
                    'total_requests': 0,
                    'total_errors': 0,
                    'error_rate': 0,
                    'requests_per_second': 0
                }
        except Exception as e:
            return {'error': str(e)}
    
    def _calculate_security_score(self, metrics: Dict[str, Any]) -> float:
        """Calculate overall security score (0-100)"""
        score = 100.0
        
        # Deduct points for issues
        auth_metrics = metrics.get('authentication', {})
        if auth_metrics.get('failed_logins_24h', 0) > 10:
            score -= 10
        
        api_health = metrics.get('api_health', {})
        if api_health.get('overall_status') != 'healthy':
            score -= 20
        
        system_health = metrics.get('system_health', {})
        error_rate = system_health.get('error_rate', 0)
        if error_rate > 0.05:  # 5% error rate
            score -= 15
        
        recent_alerts = metrics.get('recent_alerts', [])
        critical_alerts = [a for a in recent_alerts if a.get('severity') == 'critical']
        if critical_alerts:
            score -= len(critical_alerts) * 5
        
        return max(0.0, min(100.0, score))
    
    def format_dashboard_output(self, metrics: Dict[str, Any]) -> str:
        """Format metrics for console output"""
        output = []
        
        # Header
        output.append("=" * 80)
        output.append("🔒 MYTA SECURITY DASHBOARD")
        output.append("=" * 80)
        output.append(f"Generated: {metrics['timestamp']}")
        output.append(f"Security Score: {metrics['security_score']:.1f}/100")
        
        # Security score indicator
        score = metrics['security_score']
        if score >= 90:
            score_indicator = "🟢 EXCELLENT"
        elif score >= 75:
            score_indicator = "🟡 GOOD"
        elif score >= 60:
            score_indicator = "🟠 FAIR"
        else:
            score_indicator = "🔴 POOR"
        
        output.append(f"Status: {score_indicator}")
        output.append("")
        
        # Authentication metrics
        auth = metrics.get('authentication', {})
        output.append("🔐 AUTHENTICATION METRICS")
        output.append("-" * 40)
        output.append(f"Failed logins (24h): {auth.get('failed_logins_24h', 'N/A')}")
        output.append(f"Successful logins (24h): {auth.get('successful_logins_24h', 'N/A')}")
        output.append(f"Unique IPs (24h): {auth.get('unique_ips_24h', 'N/A')}")
        output.append(f"Blocked IPs: {auth.get('blocked_ips', 'N/A')}")
        output.append("")
        
        # API Health
        api_health = metrics.get('api_health', {})
        output.append("🌐 API HEALTH")
        output.append("-" * 40)
        output.append(f"Overall status: {api_health.get('overall_status', 'Unknown')}")
        output.append(f"Healthy components: {api_health.get('healthy_components', 0)}/{api_health.get('total_components', 0)}")
        output.append(f"Avg response time: {api_health.get('response_time_avg', 0):.1f}ms")
        output.append("")
        
        # System Health
        system = metrics.get('system_health', {})
        output.append("⚙️ SYSTEM HEALTH")
        output.append("-" * 40)
        uptime_hours = system.get('uptime_seconds', 0) / 3600
        output.append(f"Uptime: {uptime_hours:.1f} hours")
        output.append(f"Total requests: {system.get('total_requests', 0):,}")
        output.append(f"Error rate: {system.get('error_rate', 0):.2%}")
        output.append(f"Requests/sec: {system.get('requests_per_second', 0):.1f}")
        output.append("")
        
        # Recent Alerts
        alerts = metrics.get('recent_alerts', [])
        output.append("🚨 RECENT ALERTS")
        output.append("-" * 40)
        if alerts:
            for alert in alerts[-5:]:  # Show last 5 alerts
                severity = alert.get('severity', 'unknown').upper()
                alert_type = alert.get('alert_type', 'unknown')
                title = alert.get('title', 'Unknown alert')
                timestamp = alert.get('timestamp', '')
                
                severity_icon = {
                    'LOW': '🟢',
                    'MEDIUM': '🟡',
                    'HIGH': '🟠',
                    'CRITICAL': '🔴'
                }.get(severity, '⚪')
                
                output.append(f"{severity_icon} {severity} - {title}")
                output.append(f"   Type: {alert_type} | Time: {timestamp}")
        else:
            output.append("No recent alerts")
        
        output.append("")
        output.append("=" * 80)
        
        return "\n".join(output)
    
    async def generate_report(self, output_format: str = "console") -> str:
        """Generate security report"""
        metrics = await self.collect_security_metrics()
        
        if output_format == "json":
            return json.dumps(metrics, indent=2)
        elif output_format == "console":
            return self.format_dashboard_output(metrics)
        else:
            raise ValueError(f"Unsupported output format: {output_format}")
    
    async def monitor_continuous(self, interval_seconds: int = 60):
        """Run continuous monitoring"""
        print("Starting continuous security monitoring...")
        print(f"Update interval: {interval_seconds} seconds")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                # Clear screen (works on most terminals)
                os.system('clear' if os.name == 'posix' else 'cls')
                
                # Generate and display report
                report = await self.generate_report("console")
                print(report)
                
                # Wait for next update
                await asyncio.sleep(interval_seconds)
                
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user")


async def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description="MYTA Security Dashboard")
    parser.add_argument('--format', choices=['console', 'json'], default='console',
                       help='Output format')
    parser.add_argument('--monitor', action='store_true',
                       help='Run continuous monitoring')
    parser.add_argument('--interval', type=int, default=60,
                       help='Update interval for monitoring (seconds)')
    parser.add_argument('--db-path', default='Vidalytics.db',
                       help='Path to database file')
    
    args = parser.parse_args()
    
    dashboard = SecurityDashboard(args.db_path)
    
    if args.monitor:
        await dashboard.monitor_continuous(args.interval)
    else:
        report = await dashboard.generate_report(args.format)
        print(report)


if __name__ == "__main__":
    asyncio.run(main())
