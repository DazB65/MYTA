"""
Comprehensive Health Check System for Vidalytics
Monitors system health, dependencies, and performance metrics
"""

import asyncio
import time
import psutil
import sqlite3
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime
import requests

logger = logging.getLogger(__name__)

class HealthStatus(Enum):
    """Health check status levels"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    CRITICAL = "critical"

@dataclass
class HealthCheckResult:
    """Result of a health check"""
    name: str
    status: HealthStatus
    message: str
    response_time_ms: float
    timestamp: str
    details: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class SystemHealthSnapshot:
    """Complete system health snapshot"""
    overall_status: HealthStatus
    checks: List[HealthCheckResult]
    system_metrics: Dict[str, Any]
    timestamp: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "overall_status": self.overall_status.value,
            "checks": [check.to_dict() for check in self.checks],
            "system_metrics": self.system_metrics,
            "timestamp": self.timestamp
        }

class BaseHealthCheck:
    """Base class for health checks"""
    
    def __init__(self, name: str, timeout: float = 10.0):
        self.name = name
        self.timeout = timeout
    
    async def check(self) -> HealthCheckResult:
        """Perform the health check"""
        start_time = time.time()
        
        try:
            async with asyncio.timeout(self.timeout):
                status, message, details = await self._perform_check()
            
            response_time = (time.time() - start_time) * 1000
            
            return HealthCheckResult(
                name=self.name,
                status=status,
                message=message,
                response_time_ms=round(response_time, 2),
                timestamp=datetime.now().isoformat(),
                details=details
            )
            
        except asyncio.TimeoutError:
            response_time = (time.time() - start_time) * 1000
            return HealthCheckResult(
                name=self.name,
                status=HealthStatus.CRITICAL,
                message=f"Health check timed out after {self.timeout}s",
                response_time_ms=round(response_time, 2),
                timestamp=datetime.now().isoformat()
            )
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            logger.error(f"Health check {self.name} failed: {e}")
            return HealthCheckResult(
                name=self.name,
                status=HealthStatus.CRITICAL,
                message=f"Health check failed: {str(e)}",
                response_time_ms=round(response_time, 2),
                timestamp=datetime.now().isoformat(),
                details={"error": str(e)}
            )
    
    async def _perform_check(self) -> tuple[HealthStatus, str, Optional[Dict[str, Any]]]:
        """Override this method in subclasses"""
        raise NotImplementedError

class DatabaseHealthCheck(BaseHealthCheck):
    """Check database connectivity and performance"""
    
    def __init__(self, db_path: str = "Vidalytics.db"):
        super().__init__("database", timeout=5.0)
        self.db_path = db_path
    
    async def _perform_check(self) -> tuple[HealthStatus, str, Optional[Dict[str, Any]]]:
        """Check database health"""
        try:
            # Test connection and basic query
            with sqlite3.connect(self.db_path, timeout=5.0) as conn:
                cursor = conn.cursor()
                
                # Test basic connectivity
                start_time = time.time()
                cursor.execute("SELECT 1")
                query_time = (time.time() - start_time) * 1000
                
                # Check database integrity
                cursor.execute("PRAGMA integrity_check")
                integrity_result = cursor.fetchone()[0]
                
                # Get database stats
                cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
                table_count = cursor.fetchone()[0]
                
                # Check WAL mode
                cursor.execute("PRAGMA journal_mode")
                journal_mode = cursor.fetchone()[0]
                
                # Get database size
                cursor.execute("PRAGMA page_count")
                page_count = cursor.fetchone()[0]
                cursor.execute("PRAGMA page_size")
                page_size = cursor.fetchone()[0]
                db_size_mb = (page_count * page_size) / (1024 * 1024)
                
                details = {
                    "query_time_ms": round(query_time, 2),
                    "integrity_check": integrity_result,
                    "table_count": table_count,
                    "journal_mode": journal_mode,
                    "size_mb": round(db_size_mb, 2)
                }
                
                # Determine status based on performance
                if query_time > 1000:  # > 1 second
                    status = HealthStatus.CRITICAL
                    message = f"Database query time too high ({query_time:.2f}ms)"
                elif query_time > 500:  # > 500ms
                    status = HealthStatus.DEGRADED
                    message = f"Database query time elevated ({query_time:.2f}ms)"
                elif integrity_result != "ok":
                    status = HealthStatus.UNHEALTHY
                    message = f"Database integrity issue: {integrity_result}"
                else:
                    status = HealthStatus.HEALTHY
                    message = f"Database healthy, query time: {query_time:.2f}ms"
                
                return status, message, details
                
        except sqlite3.OperationalError as e:
            return HealthStatus.CRITICAL, f"Database operational error: {str(e)}", {"error": str(e)}
        except Exception as e:
            return HealthStatus.CRITICAL, f"Database connection failed: {str(e)}", {"error": str(e)}

class APIHealthCheck(BaseHealthCheck):
    """Check external API connectivity"""
    
    def __init__(self, api_name: str, url: str, expected_status: int = 200):
        super().__init__(f"api_{api_name}", timeout=10.0)
        self.api_name = api_name
        self.url = url
        self.expected_status = expected_status
    
    async def _perform_check(self) -> tuple[HealthStatus, str, Optional[Dict[str, Any]]]:
        """Check API health"""
        try:
            start_time = time.time()
            response = requests.get(self.url, timeout=self.timeout)
            response_time = (time.time() - start_time) * 1000
            
            details = {
                "status_code": response.status_code,
                "response_time_ms": round(response_time, 2),
                "url": self.url
            }
            
            if response.status_code == self.expected_status:
                if response_time > 5000:  # > 5 seconds
                    status = HealthStatus.DEGRADED
                    message = f"{self.api_name} API slow ({response_time:.2f}ms)"
                else:
                    status = HealthStatus.HEALTHY
                    message = f"{self.api_name} API healthy ({response_time:.2f}ms)"
            else:
                status = HealthStatus.UNHEALTHY
                message = f"{self.api_name} API returned {response.status_code}"
            
            return status, message, details
            
        except requests.exceptions.Timeout:
            return HealthStatus.CRITICAL, f"{self.api_name} API timeout", {"timeout": self.timeout}
        except requests.exceptions.ConnectionError:
            return HealthStatus.CRITICAL, f"{self.api_name} API connection failed", None
        except Exception as e:
            return HealthStatus.CRITICAL, f"{self.api_name} API error: {str(e)}", {"error": str(e)}

class SystemResourceHealthCheck(BaseHealthCheck):
    """Check system resources (CPU, memory, disk)"""
    
    def __init__(self):
        super().__init__("system_resources", timeout=5.0)
    
    async def _perform_check(self) -> tuple[HealthStatus, str, Optional[Dict[str, Any]]]:
        """Check system resource health"""
        try:
            # Get system metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Check system load
            load_avg = psutil.getloadavg()[0] if hasattr(psutil, 'getloadavg') else 0
            cpu_count = psutil.cpu_count()
            
            details = {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_available_gb": round(memory.available / (1024**3), 2),
                "disk_percent": (disk.used / disk.total) * 100,
                "disk_free_gb": round(disk.free / (1024**3), 2),
                "load_average": load_avg,
                "cpu_count": cpu_count
            }
            
            # Determine overall status
            critical_issues = []
            degraded_issues = []
            
            if cpu_percent > 90:
                critical_issues.append(f"CPU usage critical ({cpu_percent:.1f}%)")
            elif cpu_percent > 75:
                degraded_issues.append(f"CPU usage high ({cpu_percent:.1f}%)")
            
            if memory.percent > 90:
                critical_issues.append(f"Memory usage critical ({memory.percent:.1f}%)")
            elif memory.percent > 75:
                degraded_issues.append(f"Memory usage high ({memory.percent:.1f}%)")
            
            disk_percent = (disk.used / disk.total) * 100
            if disk_percent > 95:
                critical_issues.append(f"Disk usage critical ({disk_percent:.1f}%)")
            elif disk_percent > 85:
                degraded_issues.append(f"Disk usage high ({disk_percent:.1f}%)")
            
            if critical_issues:
                return HealthStatus.CRITICAL, "; ".join(critical_issues), details
            elif degraded_issues:
                return HealthStatus.DEGRADED, "; ".join(degraded_issues), details
            else:
                return HealthStatus.HEALTHY, "System resources healthy", details
                
        except Exception as e:
            return HealthStatus.CRITICAL, f"Failed to check system resources: {str(e)}", {"error": str(e)}

class AgentHealthCheck(BaseHealthCheck):
    """Check agent system health"""
    
    def __init__(self):
        super().__init__("agent_system", timeout=5.0)
    
    async def _perform_check(self) -> tuple[HealthStatus, str, Optional[Dict[str, Any]]]:
        """Check agent system health"""
        try:
            # Test boss agent initialization
            from boss_agent_core import get_boss_agent
            
            start_time = time.time()
            boss_agent = get_boss_agent()
            init_time = (time.time() - start_time) * 1000
            
            # Test intent classifier
            from intent_classifier import get_intent_classifier
            classifier = get_intent_classifier()
            
            # Test agent coordinators
            from agent_coordinators import get_agent_coordinators
            coordinators = get_agent_coordinators()
            
            details = {
                "boss_agent_init_time_ms": round(init_time, 2),
                "available_coordinators": list(coordinators.keys()),
                "coordinator_count": len(coordinators)
            }
            
            if init_time > 5000:  # > 5 seconds
                return HealthStatus.DEGRADED, f"Agent initialization slow ({init_time:.2f}ms)", details
            elif len(coordinators) == 0:
                return HealthStatus.CRITICAL, "No agent coordinators available", details
            else:
                return HealthStatus.HEALTHY, f"Agent system healthy ({len(coordinators)} coordinators)", details
                
        except ImportError as e:
            return HealthStatus.CRITICAL, f"Agent module import failed: {str(e)}", {"error": str(e)}
        except Exception as e:
            return HealthStatus.CRITICAL, f"Agent system check failed: {str(e)}", {"error": str(e)}

class CacheHealthCheck(BaseHealthCheck):
    """Check caching system health"""
    
    def __init__(self):
        super().__init__("cache_system", timeout=5.0)
    
    async def _perform_check(self) -> tuple[HealthStatus, str, Optional[Dict[str, Any]]]:
        """Check cache system health"""
        try:
            from backend import get_agent_cache
            
            cache = get_agent_cache()
            
            # Test cache operations
            start_time = time.time()
            test_key = f"health_check_{int(time.time())}"
            test_value = {"test": True, "timestamp": time.time()}
            
            # Test cache set/get
            cache.set(test_key, {}, test_value, "test")
            retrieved = cache.get(test_key, {}, "test")
            
            operation_time = (time.time() - start_time) * 1000
            
            # Get cache stats
            stats = cache.cache_stats
            
            details = {
                "operation_time_ms": round(operation_time, 2),
                "cache_stats": stats,
                "test_successful": retrieved is not None
            }
            
            if not retrieved:
                return HealthStatus.UNHEALTHY, "Cache set/get test failed", details
            elif operation_time > 1000:  # > 1 second
                return HealthStatus.DEGRADED, f"Cache operations slow ({operation_time:.2f}ms)", details
            else:
                hit_rate = stats["hits"] / max(stats["hits"] + stats["misses"], 1)
                return HealthStatus.HEALTHY, f"Cache healthy (hit rate: {hit_rate:.1%})", details
                
        except ImportError:
            return HealthStatus.UNHEALTHY, "Cache module not available", None
        except Exception as e:
            return HealthStatus.CRITICAL, f"Cache system check failed: {str(e)}", {"error": str(e)}

class ComprehensiveHealthChecker:
    """Main health checker that orchestrates all health checks"""
    
    def __init__(self):
        self.checks: List[BaseHealthCheck] = []
        self._initialize_checks()
    
    def _initialize_checks(self):
        """Initialize all health checks"""
        # Core system checks
        self.checks.append(DatabaseHealthCheck())
        self.checks.append(SystemResourceHealthCheck())
        self.checks.append(AgentHealthCheck())
        self.checks.append(CacheHealthCheck())
        
        # External API checks
        self.checks.append(APIHealthCheck("openai", "https://api.openai.com/v1/models"))
        self.checks.append(APIHealthCheck("youtube", "https://www.googleapis.com/youtube/v3/", expected_status=400))  # 400 is expected without API key
        
        logger.info(f"Initialized {len(self.checks)} health checks")
    
    def add_check(self, check: BaseHealthCheck):
        """Add a custom health check"""
        self.checks.append(check)
        logger.info(f"Added custom health check: {check.name}")
    
    async def run_all_checks(self) -> SystemHealthSnapshot:
        """Run all health checks and return system snapshot"""
        logger.info("Running comprehensive health checks")
        
        # Run all checks concurrently
        tasks = [check.check() for check in self.checks]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        check_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                # Handle exceptions from individual checks
                check_results.append(HealthCheckResult(
                    name=self.checks[i].name,
                    status=HealthStatus.CRITICAL,
                    message=f"Health check failed: {str(result)}",
                    response_time_ms=0,
                    timestamp=datetime.now().isoformat(),
                    details={"exception": str(result)}
                ))
            else:
                check_results.append(result)
        
        # Determine overall status
        overall_status = self._determine_overall_status(check_results)
        
        # Get system metrics
        system_metrics = self._get_system_metrics()
        
        return SystemHealthSnapshot(
            overall_status=overall_status,
            checks=check_results,
            system_metrics=system_metrics,
            timestamp=datetime.now().isoformat()
        )
    
    def _determine_overall_status(self, results: List[HealthCheckResult]) -> HealthStatus:
        """Determine overall system status from individual check results"""
        if not results:
            return HealthStatus.CRITICAL
        
        status_counts = {status: 0 for status in HealthStatus}
        for result in results:
            status_counts[result.status] += 1
        
        total_checks = len(results)
        
        # If any critical failures, system is critical
        if status_counts[HealthStatus.CRITICAL] > 0:
            return HealthStatus.CRITICAL
        
        # If more than 50% unhealthy, system is unhealthy
        if status_counts[HealthStatus.UNHEALTHY] > total_checks * 0.5:
            return HealthStatus.UNHEALTHY
        
        # If any unhealthy or more than 25% degraded, system is degraded
        if (status_counts[HealthStatus.UNHEALTHY] > 0 or 
            status_counts[HealthStatus.DEGRADED] > total_checks * 0.25):
            return HealthStatus.DEGRADED
        
        return HealthStatus.HEALTHY
    
    def _get_system_metrics(self) -> Dict[str, Any]:
        """Get additional system metrics"""
        try:
            return {
                "uptime_seconds": time.time() - psutil.boot_time(),
                "python_processes": len([p for p in psutil.process_iter() if 'python' in p.name().lower()]),
                "total_processes": len(list(psutil.process_iter())),
                "system_load": psutil.getloadavg()[0] if hasattr(psutil, 'getloadavg') else 0,
                "network_connections": len(psutil.net_connections()),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get system metrics: {e}")
            return {"error": str(e)}

# Global health checker instance
_health_checker: Optional[ComprehensiveHealthChecker] = None

def get_health_checker() -> ComprehensiveHealthChecker:
    """Get or create global health checker instance"""
    global _health_checker
    if _health_checker is None:
        _health_checker = ComprehensiveHealthChecker()
    return _health_checker

async def quick_health_check() -> Dict[str, Any]:
    """Quick health check for API endpoints"""
    checker = get_health_checker()
    
    # Run only critical checks for quick response
    critical_checks = [
        DatabaseHealthCheck(),
        SystemResourceHealthCheck()
    ]
    
    tasks = [check.check() for check in critical_checks]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    status = HealthStatus.HEALTHY
    for result in results:
        if isinstance(result, HealthCheckResult):
            if result.status in [HealthStatus.CRITICAL, HealthStatus.UNHEALTHY]:
                status = HealthStatus.CRITICAL
                break
            elif result.status == HealthStatus.DEGRADED:
                status = HealthStatus.DEGRADED
    
    return {
        "status": status.value,
        "timestamp": datetime.now().isoformat(),
        "checks_run": len(critical_checks)
    }

async def full_health_check() -> Dict[str, Any]:
    """Full comprehensive health check"""
    checker = get_health_checker()
    snapshot = await checker.run_all_checks()
    return snapshot.to_dict()