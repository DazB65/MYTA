"""
Comprehensive Health Check System for CreatorMate
Provides detailed health monitoring for all system components
"""

import asyncio
import time
import sys
import os
import psutil
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import redis
import sqlite3
import httpx

from config import get_settings
from logging_config import get_logger, LogCategory


class HealthStatus(Enum):
    """Health status enumeration"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass
class ComponentHealth:
    """Health status for a system component"""
    name: str
    status: HealthStatus
    response_time_ms: float
    message: str
    details: Dict[str, Any]
    last_check: datetime
    error: Optional[str] = None


@dataclass
class SystemHealth:
    """Overall system health status"""
    status: HealthStatus
    overall_score: float
    components: List[ComponentHealth]
    system_info: Dict[str, Any]
    timestamp: datetime
    uptime_seconds: int


class HealthChecker:
    """Comprehensive health checking system"""
    
    def __init__(self):
        self.settings = get_settings()
        self.logger = get_logger(__name__, LogCategory.SYSTEM)
        self.start_time = datetime.now(timezone.utc)
        
        # Health check configuration
        self.timeout_seconds = 10
        self.critical_thresholds = {
            'cpu_percent': 90.0,
            'memory_percent': 90.0,
            'disk_percent': 95.0,
            'response_time_ms': 5000
        }
        self.warning_thresholds = {
            'cpu_percent': 70.0,
            'memory_percent': 75.0,
            'disk_percent': 85.0,
            'response_time_ms': 2000
        }
    
    async def check_system_health(self) -> SystemHealth:
        """Perform comprehensive system health check"""
        start_time = time.time()
        
        self.logger.info("Starting comprehensive system health check")
        
        # Run all component checks concurrently
        component_checks = [
            self._check_redis_health(),
            self._check_database_health(),
            self._check_ai_services_health(),
            self._check_youtube_api_health(),
            self._check_system_resources_health(),
            self._check_disk_health(),
            self._check_network_health(),
            self._check_backup_health()
        ]
        
        try:
            components = await asyncio.gather(*component_checks, return_exceptions=True)
            
            # Handle any exceptions from component checks
            healthy_components = []
            for i, component in enumerate(components):
                if isinstance(component, Exception):
                    self.logger.error(f"Component check {i} failed: {component}")
                    healthy_components.append(ComponentHealth(
                        name=f"component_{i}",
                        status=HealthStatus.UNHEALTHY,
                        response_time_ms=0,
                        message="Check failed with exception",
                        details={},
                        last_check=datetime.now(timezone.utc),
                        error=str(component)
                    ))
                else:
                    healthy_components.append(component)
            
            # Calculate overall health score
            overall_score = self._calculate_overall_score(healthy_components)
            overall_status = self._determine_overall_status(overall_score)
            
            # Get system information
            system_info = self._get_system_info()
            
            # Calculate uptime
            uptime_seconds = int((datetime.now(timezone.utc) - self.start_time).total_seconds())
            
            health_result = SystemHealth(
                status=overall_status,
                overall_score=overall_score,
                components=healthy_components,
                system_info=system_info,
                timestamp=datetime.now(timezone.utc),
                uptime_seconds=uptime_seconds
            )
            
            duration_ms = (time.time() - start_time) * 1000
            self.logger.info(
                f"System health check completed in {duration_ms:.2f}ms",
                extra={
                    'category': LogCategory.SYSTEM.value,
                    'metadata': {
                        'overall_status': overall_status.value,
                        'overall_score': overall_score,
                        'duration_ms': duration_ms,
                        'components_checked': len(healthy_components)
                    }
                }
            )
            
            return health_result
            
        except Exception as e:
            self.logger.error(
                "System health check failed",
                extra={
                    'category': LogCategory.ERROR.value,
                    'metadata': {
                        'error_type': type(e).__name__,
                        'error_message': str(e)
                    }
                },
                exc_info=True
            )
            
            # Return unhealthy system status
            return SystemHealth(
                status=HealthStatus.UNHEALTHY,
                overall_score=0.0,
                components=[],
                system_info=self._get_system_info(),
                timestamp=datetime.now(timezone.utc),
                uptime_seconds=0
            )
    
    async def _check_redis_health(self) -> ComponentHealth:
        """Check Redis health and performance"""
        start_time = time.time()
        
        try:
            # Create Redis connection
            redis_client = redis.Redis(
                host=getattr(self.settings, 'redis_host', 'localhost'),
                port=getattr(self.settings, 'redis_port', 6379),
                db=getattr(self.settings, 'redis_db', 0),
                password=getattr(self.settings, 'redis_password', None),
                decode_responses=True,
                socket_timeout=5,
                socket_connect_timeout=5
            )
            
            # Test basic operations
            test_key = "health_check_test"
            test_value = f"test_{int(time.time())}"
            
            # Ping test
            redis_client.ping()
            
            # Write test
            redis_client.set(test_key, test_value, ex=60)
            
            # Read test
            retrieved_value = redis_client.get(test_key)
            
            # Delete test
            redis_client.delete(test_key)
            
            # Get Redis info
            redis_info = redis_client.info()
            
            response_time_ms = (time.time() - start_time) * 1000
            
            # Analyze Redis health
            used_memory_percent = (redis_info.get('used_memory', 0) / 
                                 redis_info.get('maxmemory', sys.maxsize)) * 100
            
            connected_clients = redis_info.get('connected_clients', 0)
            
            # Determine status
            if response_time_ms > self.critical_thresholds['response_time_ms']:
                status = HealthStatus.UNHEALTHY
                message = f"Redis response time critical: {response_time_ms:.2f}ms"
            elif used_memory_percent > 90:
                status = HealthStatus.DEGRADED
                message = f"Redis memory usage high: {used_memory_percent:.1f}%"
            elif response_time_ms > self.warning_thresholds['response_time_ms']:
                status = HealthStatus.DEGRADED
                message = f"Redis response time elevated: {response_time_ms:.2f}ms"
            else:
                status = HealthStatus.HEALTHY
                message = "Redis is functioning normally"
            
            return ComponentHealth(
                name="redis",
                status=status,
                response_time_ms=response_time_ms,
                message=message,
                details={
                    "redis_version": redis_info.get('redis_version', 'unknown'),
                    "connected_clients": connected_clients,
                    "used_memory_human": redis_info.get('used_memory_human', 'unknown'),
                    "used_memory_percent": round(used_memory_percent, 2),
                    "uptime_seconds": redis_info.get('uptime_in_seconds', 0),
                    "keyspace_hits": redis_info.get('keyspace_hits', 0),
                    "keyspace_misses": redis_info.get('keyspace_misses', 0),
                    "test_successful": retrieved_value == test_value
                },
                last_check=datetime.now(timezone.utc)
            )
            
        except redis.ConnectionError as e:
            return ComponentHealth(
                name="redis",
                status=HealthStatus.UNHEALTHY,
                response_time_ms=(time.time() - start_time) * 1000,
                message="Redis connection failed",
                details={"connection_error": str(e)},
                last_check=datetime.now(timezone.utc),
                error=str(e)
            )
        except Exception as e:
            return ComponentHealth(
                name="redis",
                status=HealthStatus.UNHEALTHY,
                response_time_ms=(time.time() - start_time) * 1000,
                message="Redis health check failed",
                details={"error_type": type(e).__name__},
                last_check=datetime.now(timezone.utc),
                error=str(e)
            )
    
    async def _check_database_health(self) -> ComponentHealth:
        """Check SQLite database health"""
        start_time = time.time()
        
        try:
            # Get database path
            db_path = getattr(self.settings, 'database_path', 'creatormate.db')
            if not os.path.isabs(db_path):
                db_path = os.path.join(os.getcwd(), db_path)
            
            # Check if database file exists
            if not os.path.exists(db_path):
                return ComponentHealth(
                    name="database",
                    status=HealthStatus.UNHEALTHY,
                    response_time_ms=(time.time() - start_time) * 1000,
                    message="Database file not found",
                    details={"db_path": db_path},
                    last_check=datetime.now(timezone.utc),
                    error="Database file does not exist"
                )
            
            # Test database connection and operations
            with sqlite3.connect(db_path, timeout=5.0) as conn:
                cursor = conn.cursor()
                
                # Test basic query
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                
                # Check database integrity
                cursor.execute("PRAGMA integrity_check")
                integrity_result = cursor.fetchone()[0]
                
                # Get database statistics
                cursor.execute("PRAGMA page_count")
                page_count = cursor.fetchone()[0]
                
                cursor.execute("PRAGMA page_size")
                page_size = cursor.fetchone()[0]
                
                # Get table count
                cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
                table_count = cursor.fetchone()[0]
                
                db_size_bytes = page_count * page_size
                db_size_mb = db_size_bytes / (1024 * 1024)
                
                response_time_ms = (time.time() - start_time) * 1000
                
                # Determine status
                if integrity_result != "ok":
                    status = HealthStatus.UNHEALTHY
                    message = f"Database integrity check failed: {integrity_result}"
                elif response_time_ms > self.critical_thresholds['response_time_ms']:
                    status = HealthStatus.DEGRADED
                    message = f"Database response time critical: {response_time_ms:.2f}ms"
                elif response_time_ms > self.warning_thresholds['response_time_ms']:
                    status = HealthStatus.DEGRADED
                    message = f"Database response time elevated: {response_time_ms:.2f}ms"
                else:
                    status = HealthStatus.HEALTHY
                    message = "Database is functioning normally"
                
                return ComponentHealth(
                    name="database",
                    status=status,
                    response_time_ms=response_time_ms,
                    message=message,
                    details={
                        "db_path": db_path,
                        "db_size_mb": round(db_size_mb, 2),
                        "table_count": table_count,
                        "page_count": page_count,
                        "page_size": page_size,
                        "integrity_check": integrity_result,
                        "test_query_successful": result[0] == 1
                    },
                    last_check=datetime.now(timezone.utc)
                )
                
        except sqlite3.Error as e:
            return ComponentHealth(
                name="database",
                status=HealthStatus.UNHEALTHY,
                response_time_ms=(time.time() - start_time) * 1000,
                message="Database error occurred",
                details={"sqlite_error": str(e)},
                last_check=datetime.now(timezone.utc),
                error=str(e)
            )
        except Exception as e:
            return ComponentHealth(
                name="database",
                status=HealthStatus.UNHEALTHY,
                response_time_ms=(time.time() - start_time) * 1000,
                message="Database health check failed",
                details={"error_type": type(e).__name__},
                last_check=datetime.now(timezone.utc),
                error=str(e)
            )
    
    async def _check_ai_services_health(self) -> ComponentHealth:
        """Check AI services (OpenAI, Google) health"""
        start_time = time.time()
        
        try:
            health_details = {}
            service_statuses = []
            
            # Check OpenAI API
            if hasattr(self.settings, 'openai_api_key') and self.settings.openai_api_key:
                try:
                    import openai
                    openai.api_key = self.settings.openai_api_key
                    
                    # Test OpenAI API with a simple request
                    # Note: This would make an actual API call, so we'll simulate
                    health_details["openai"] = {
                        "status": "configured",
                        "api_key_present": True,
                        "test_call": "skipped"  # Skip actual call to avoid costs
                    }
                    service_statuses.append(HealthStatus.HEALTHY)
                    
                except ImportError:
                    health_details["openai"] = {
                        "status": "library_missing",
                        "error": "OpenAI library not installed"
                    }
                    service_statuses.append(HealthStatus.DEGRADED)
                except Exception as e:
                    health_details["openai"] = {
                        "status": "error",
                        "error": str(e)
                    }
                    service_statuses.append(HealthStatus.UNHEALTHY)
            else:
                health_details["openai"] = {
                    "status": "not_configured",
                    "api_key_present": False
                }
                service_statuses.append(HealthStatus.DEGRADED)
            
            # Check Google API
            if hasattr(self.settings, 'google_api_key') and self.settings.google_api_key:
                try:
                    import google.generativeai as genai
                    genai.configure(api_key=self.settings.google_api_key)
                    
                    health_details["google"] = {
                        "status": "configured",
                        "api_key_present": True,
                        "test_call": "skipped"  # Skip actual call to avoid costs
                    }
                    service_statuses.append(HealthStatus.HEALTHY)
                    
                except ImportError:
                    health_details["google"] = {
                        "status": "library_missing",
                        "error": "Google Generative AI library not installed"
                    }
                    service_statuses.append(HealthStatus.DEGRADED)
                except Exception as e:
                    health_details["google"] = {
                        "status": "error",
                        "error": str(e)
                    }
                    service_statuses.append(HealthStatus.UNHEALTHY)
            else:
                health_details["google"] = {
                    "status": "not_configured",
                    "api_key_present": False
                }
                service_statuses.append(HealthStatus.DEGRADED)
            
            response_time_ms = (time.time() - start_time) * 1000
            
            # Determine overall AI services status
            if any(status == HealthStatus.UNHEALTHY for status in service_statuses):
                overall_status = HealthStatus.UNHEALTHY
                message = "One or more AI services are unhealthy"
            elif any(status == HealthStatus.DEGRADED for status in service_statuses):
                overall_status = HealthStatus.DEGRADED
                message = "Some AI services are not configured or degraded"
            else:
                overall_status = HealthStatus.HEALTHY
                message = "AI services are configured and ready"
            
            return ComponentHealth(
                name="ai_services",
                status=overall_status,
                response_time_ms=response_time_ms,
                message=message,
                details=health_details,
                last_check=datetime.now(timezone.utc)
            )
            
        except Exception as e:
            return ComponentHealth(
                name="ai_services",
                status=HealthStatus.UNHEALTHY,
                response_time_ms=(time.time() - start_time) * 1000,
                message="AI services health check failed",
                details={"error_type": type(e).__name__},
                last_check=datetime.now(timezone.utc),
                error=str(e)
            )
    
    async def _check_youtube_api_health(self) -> ComponentHealth:
        """Check YouTube API health"""
        start_time = time.time()
        
        try:
            if not hasattr(self.settings, 'youtube_api_key') or not self.settings.youtube_api_key:
                return ComponentHealth(
                    name="youtube_api",
                    status=HealthStatus.DEGRADED,
                    response_time_ms=(time.time() - start_time) * 1000,
                    message="YouTube API key not configured",
                    details={"api_key_present": False},
                    last_check=datetime.now(timezone.utc)
                )
            
            # Test YouTube API connectivity (without making actual requests)
            youtube_api_url = "https://www.googleapis.com/youtube/v3"
            
            async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
                # Test basic connectivity to YouTube API
                response = await client.get(f"{youtube_api_url}/videos", params={
                    "part": "id",
                    "id": "invalid_test_id",  # This will fail but tests connectivity
                    "key": self.settings.youtube_api_key
                })
                
                response_time_ms = (time.time() - start_time) * 1000
                
                # YouTube API returns 400 for invalid video ID, which means it's working
                if response.status_code in [200, 400]:
                    status = HealthStatus.HEALTHY
                    message = "YouTube API is accessible"
                elif response.status_code == 403:
                    status = HealthStatus.DEGRADED
                    message = "YouTube API quota exceeded or key invalid"
                else:
                    status = HealthStatus.DEGRADED
                    message = f"YouTube API returned status {response.status_code}"
                
                return ComponentHealth(
                    name="youtube_api",
                    status=status,
                    response_time_ms=response_time_ms,
                    message=message,
                    details={
                        "api_key_present": True,
                        "status_code": response.status_code,
                        "api_url": youtube_api_url
                    },
                    last_check=datetime.now(timezone.utc)
                )
                
        except httpx.TimeoutException:
            return ComponentHealth(
                name="youtube_api",
                status=HealthStatus.UNHEALTHY,
                response_time_ms=(time.time() - start_time) * 1000,
                message="YouTube API request timed out",
                details={"timeout_seconds": self.timeout_seconds},
                last_check=datetime.now(timezone.utc),
                error="Request timeout"
            )
        except Exception as e:
            return ComponentHealth(
                name="youtube_api",
                status=HealthStatus.UNHEALTHY,
                response_time_ms=(time.time() - start_time) * 1000,
                message="YouTube API health check failed",
                details={"error_type": type(e).__name__},
                last_check=datetime.now(timezone.utc),
                error=str(e)
            )
    
    async def _check_system_resources_health(self) -> ComponentHealth:
        """Check system resource usage"""
        start_time = time.time()
        
        try:
            # Get CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Get memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Get disk usage
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            
            # Get load average (Unix-like systems)
            if hasattr(os, 'getloadavg'):
                load_avg = os.getloadavg()
            else:
                load_avg = (0, 0, 0)  # Windows fallback
            
            # Get process info
            process = psutil.Process()
            process_memory = process.memory_info()
            process_cpu = process.cpu_percent()
            
            response_time_ms = (time.time() - start_time) * 1000
            
            # Determine status based on resource usage
            critical_issues = []
            warnings = []
            
            if cpu_percent > self.critical_thresholds['cpu_percent']:
                critical_issues.append(f"CPU usage critical: {cpu_percent:.1f}%")
            elif cpu_percent > self.warning_thresholds['cpu_percent']:
                warnings.append(f"CPU usage high: {cpu_percent:.1f}%")
            
            if memory_percent > self.critical_thresholds['memory_percent']:
                critical_issues.append(f"Memory usage critical: {memory_percent:.1f}%")
            elif memory_percent > self.warning_thresholds['memory_percent']:
                warnings.append(f"Memory usage high: {memory_percent:.1f}%")
            
            if disk_percent > self.critical_thresholds['disk_percent']:
                critical_issues.append(f"Disk usage critical: {disk_percent:.1f}%")
            elif disk_percent > self.warning_thresholds['disk_percent']:
                warnings.append(f"Disk usage high: {disk_percent:.1f}%")
            
            # Determine overall status
            if critical_issues:
                status = HealthStatus.UNHEALTHY
                message = f"Critical resource issues: {'; '.join(critical_issues)}"
            elif warnings:
                status = HealthStatus.DEGRADED
                message = f"Resource warnings: {'; '.join(warnings)}"
            else:
                status = HealthStatus.HEALTHY
                message = "System resources are within normal ranges"
            
            return ComponentHealth(
                name="system_resources",
                status=status,
                response_time_ms=response_time_ms,
                message=message,
                details={
                    "cpu_percent": round(cpu_percent, 2),
                    "memory_percent": round(memory_percent, 2),
                    "memory_available_gb": round(memory.available / (1024**3), 2),
                    "memory_total_gb": round(memory.total / (1024**3), 2),
                    "disk_percent": round(disk_percent, 2),
                    "disk_free_gb": round(disk.free / (1024**3), 2),
                    "disk_total_gb": round(disk.total / (1024**3), 2),
                    "load_average": {
                        "1min": round(load_avg[0], 2),
                        "5min": round(load_avg[1], 2),
                        "15min": round(load_avg[2], 2)
                    },
                    "process": {
                        "cpu_percent": round(process_cpu, 2),
                        "memory_mb": round(process_memory.rss / (1024**2), 2),
                        "threads": process.num_threads()
                    }
                },
                last_check=datetime.now(timezone.utc)
            )
            
        except Exception as e:
            return ComponentHealth(
                name="system_resources",
                status=HealthStatus.UNHEALTHY,
                response_time_ms=(time.time() - start_time) * 1000,
                message="System resources health check failed",
                details={"error_type": type(e).__name__},
                last_check=datetime.now(timezone.utc),
                error=str(e)
            )
    
    async def _check_disk_health(self) -> ComponentHealth:
        """Check disk health and I/O performance"""
        start_time = time.time()
        
        try:
            # Test disk I/O performance
            test_file = "/tmp/health_check_io_test.txt"
            test_data = "health_check_test_data" * 1000  # ~24KB
            
            # Write test
            write_start = time.time()
            with open(test_file, 'w') as f:
                f.write(test_data)
                f.flush()
                os.fsync(f.fileno())  # Force write to disk
            write_time_ms = (time.time() - write_start) * 1000
            
            # Read test
            read_start = time.time()
            with open(test_file, 'r') as f:
                read_data = f.read()
            read_time_ms = (time.time() - read_start) * 1000
            
            # Cleanup
            os.remove(test_file)
            
            # Get disk stats
            disk_io = psutil.disk_io_counters()
            
            response_time_ms = (time.time() - start_time) * 1000
            
            # Determine status based on I/O performance
            if write_time_ms > 1000 or read_time_ms > 1000:  # > 1 second is critical
                status = HealthStatus.UNHEALTHY
                message = f"Disk I/O performance critical (write: {write_time_ms:.2f}ms, read: {read_time_ms:.2f}ms)"
            elif write_time_ms > 500 or read_time_ms > 500:  # > 500ms is degraded
                status = HealthStatus.DEGRADED
                message = f"Disk I/O performance degraded (write: {write_time_ms:.2f}ms, read: {read_time_ms:.2f}ms)"
            else:
                status = HealthStatus.HEALTHY
                message = "Disk I/O performance is normal"
            
            return ComponentHealth(
                name="disk_io",
                status=status,
                response_time_ms=response_time_ms,
                message=message,
                details={
                    "write_time_ms": round(write_time_ms, 2),
                    "read_time_ms": round(read_time_ms, 2),
                    "test_data_size_bytes": len(test_data),
                    "test_successful": read_data == test_data,
                    "disk_io_counters": {
                        "read_count": disk_io.read_count if disk_io else 0,
                        "write_count": disk_io.write_count if disk_io else 0,
                        "read_bytes": disk_io.read_bytes if disk_io else 0,
                        "write_bytes": disk_io.write_bytes if disk_io else 0
                    } if disk_io else None
                },
                last_check=datetime.now(timezone.utc)
            )
            
        except Exception as e:
            # Cleanup test file if it exists
            try:
                if os.path.exists(test_file):
                    os.remove(test_file)
            except:
                pass
            
            return ComponentHealth(
                name="disk_io",
                status=HealthStatus.UNHEALTHY,
                response_time_ms=(time.time() - start_time) * 1000,
                message="Disk I/O health check failed",
                details={"error_type": type(e).__name__},
                last_check=datetime.now(timezone.utc),
                error=str(e)
            )
    
    async def _check_network_health(self) -> ComponentHealth:
        """Check network connectivity and performance"""
        start_time = time.time()
        
        try:
            # Test external connectivity
            test_urls = [
                "https://www.google.com",
                "https://api.openai.com",
                "https://www.googleapis.com"
            ]
            
            connectivity_results = []
            
            async with httpx.AsyncClient(timeout=5.0) as client:
                for url in test_urls:
                    try:
                        url_start = time.time()
                        response = await client.head(url)
                        url_time_ms = (time.time() - url_start) * 1000
                        
                        connectivity_results.append({
                            "url": url,
                            "status_code": response.status_code,
                            "response_time_ms": round(url_time_ms, 2),
                            "success": response.status_code < 400
                        })
                    except Exception as e:
                        connectivity_results.append({
                            "url": url,
                            "status_code": 0,
                            "response_time_ms": 0,
                            "success": False,
                            "error": str(e)
                        })
            
            response_time_ms = (time.time() - start_time) * 1000
            
            # Analyze connectivity results
            successful_connections = sum(1 for result in connectivity_results if result["success"])
            avg_response_time = sum(result["response_time_ms"] for result in connectivity_results 
                                  if result["success"]) / max(successful_connections, 1)
            
            # Determine status
            if successful_connections == 0:
                status = HealthStatus.UNHEALTHY
                message = "No external connectivity available"
            elif successful_connections < len(test_urls) / 2:
                status = HealthStatus.DEGRADED
                message = f"Limited connectivity: {successful_connections}/{len(test_urls)} services reachable"
            elif avg_response_time > 3000:  # > 3 seconds average
                status = HealthStatus.DEGRADED
                message = f"Network performance degraded: {avg_response_time:.2f}ms average"
            else:
                status = HealthStatus.HEALTHY
                message = f"Network connectivity healthy: {successful_connections}/{len(test_urls)} services reachable"
            
            return ComponentHealth(
                name="network",
                status=status,
                response_time_ms=response_time_ms,
                message=message,
                details={
                    "connectivity_tests": connectivity_results,
                    "successful_connections": successful_connections,
                    "total_tests": len(test_urls),
                    "average_response_time_ms": round(avg_response_time, 2)
                },
                last_check=datetime.now(timezone.utc)
            )
            
        except Exception as e:
            return ComponentHealth(
                name="network",
                status=HealthStatus.UNHEALTHY,
                response_time_ms=(time.time() - start_time) * 1000,
                message="Network health check failed",
                details={"error_type": type(e).__name__},
                last_check=datetime.now(timezone.utc),
                error=str(e)
            )
    
    def _calculate_overall_score(self, components: List[ComponentHealth]) -> float:
        """Calculate overall health score from component scores"""
        if not components:
            return 0.0
        
        # Component weights (sum should equal 1.0)
        weights = {
            "redis": 0.22,
            "database": 0.18,
            "backup_system": 0.15,
            "ai_services": 0.15,
            "youtube_api": 0.10,
            "system_resources": 0.12,
            "disk_io": 0.06,
            "network": 0.02
        }
        
        total_score = 0.0
        total_weight = 0.0
        
        for component in components:
            weight = weights.get(component.name, 0.05)  # Default weight for unknown components
            
            # Convert status to score
            if component.status == HealthStatus.HEALTHY:
                score = 1.0
            elif component.status == HealthStatus.DEGRADED:
                score = 0.6
            elif component.status == HealthStatus.UNHEALTHY:
                score = 0.2
            else:  # UNKNOWN
                score = 0.3
            
            total_score += score * weight
            total_weight += weight
        
        return total_score / total_weight if total_weight > 0 else 0.0
    
    def _determine_overall_status(self, score: float) -> HealthStatus:
        """Determine overall system status from score"""
        if score >= 0.8:
            return HealthStatus.HEALTHY
        elif score >= 0.5:
            return HealthStatus.DEGRADED
        else:
            return HealthStatus.UNHEALTHY
    
    async def _check_backup_health(self) -> ComponentHealth:
        """Check backup system health"""
        start_time = time.time()
        
        try:
            from backup_service import get_backup_service, BackupHealthChecker
            
            # Get database path from settings
            db_path = self.settings.database_url.replace("sqlite:///", "").replace("./", "")
            
            # Initialize health checker and backup service
            backup_health_checker = BackupHealthChecker(db_path)
            backup_service = get_backup_service()
            
            # Run comprehensive backup health check
            health_report = backup_health_checker.run_health_check()
            backup_status = backup_service.get_service_status()
            
            response_time_ms = (time.time() - start_time) * 1000
            
            # Determine component status based on health report
            if health_report["overall_status"] == "healthy":
                status = HealthStatus.HEALTHY
                message = "Backup system is healthy"
            elif health_report["overall_status"] == "degraded":
                status = HealthStatus.DEGRADED
                message = f"Backup system degraded: {len(health_report.get('failed_checks', []))} checks failed"
            else:
                status = HealthStatus.UNHEALTHY
                message = f"Backup system unhealthy: {health_report.get('error', 'Multiple issues detected')}"
            
            # Compile detailed information
            details = {
                "service_running": backup_status["running"],
                "schedule": backup_status["schedule"],
                "alerts": backup_status["alerts"],
                "health_checks": health_report["checks"],
                "overall_health_status": health_report["overall_status"],
                "failed_checks": health_report.get("failed_checks", [])
            }
            
            return ComponentHealth(
                name="backup_system",
                status=status,
                response_time_ms=response_time_ms,
                message=message,
                details=details,
                last_check=datetime.now(timezone.utc)
            )
            
        except Exception as e:
            return ComponentHealth(
                name="backup_system",
                status=HealthStatus.UNHEALTHY,
                response_time_ms=(time.time() - start_time) * 1000,
                message="Backup system health check failed",
                details={"error_type": type(e).__name__},
                last_check=datetime.now(timezone.utc),
                error=str(e)
            )
    
    def _get_system_info(self) -> Dict[str, Any]:
        """Get general system information"""
        try:
            return {
                "platform": sys.platform,
                "python_version": sys.version,
                "cpu_count": psutil.cpu_count(),
                "boot_time": datetime.fromtimestamp(psutil.boot_time(), tz=timezone.utc).isoformat(),
                "hostname": os.uname().nodename if hasattr(os, 'uname') else 'unknown',
                "architecture": os.uname().machine if hasattr(os, 'uname') else 'unknown',
                "environment": getattr(self.settings, 'environment', 'unknown')
            }
        except Exception:
            return {"error": "Could not retrieve system information"}


# Global health checker instance
_health_checker: Optional[HealthChecker] = None


def get_health_checker() -> HealthChecker:
    """Get or create global health checker instance"""
    global _health_checker
    if _health_checker is None:
        _health_checker = HealthChecker()
    return _health_checker


async def perform_health_check() -> Dict[str, Any]:
    """Perform comprehensive health check and return results"""
    health_checker = get_health_checker()
    system_health = await health_checker.check_system_health()
    
    # Convert to dictionary format for API response
    return {
        "status": system_health.status.value,
        "overall_score": system_health.overall_score,
        "timestamp": system_health.timestamp.isoformat(),
        "uptime_seconds": system_health.uptime_seconds,
        "system_info": system_health.system_info,
        "components": {
            component.name: {
                "status": component.status.value,
                "response_time_ms": component.response_time_ms,
                "message": component.message,
                "details": component.details,
                "last_check": component.last_check.isoformat(),
                "error": component.error
            }
            for component in system_health.components
        }
    }