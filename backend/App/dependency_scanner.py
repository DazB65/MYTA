"""
Automated Dependency Vulnerability Scanner
Monitors dependencies for security vulnerabilities and provides alerts
"""

import subprocess
import json
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import asyncio
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class Vulnerability:
    """Vulnerability information"""
    package_name: str
    current_version: str
    vulnerability_id: str
    severity: str
    advisory: str
    cve: Optional[str]
    fixed_versions: List[str]
    more_info_url: str

@dataclass
class ScanResult:
    """Dependency scan result"""
    timestamp: datetime
    total_packages: int
    vulnerabilities_found: int
    vulnerabilities: List[Vulnerability]
    scan_duration: float
    status: str  # 'success', 'error', 'warning'

class DependencyScanner:
    """Automated dependency vulnerability scanner"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.requirements_file = self.project_root / "requirements.txt"
        self.scan_history = []
        self.last_scan = None
        
        # Vulnerability thresholds
        self.severity_weights = {
            'critical': 10,
            'high': 7,
            'medium': 4,
            'low': 1
        }
    
    async def scan_dependencies(self) -> ScanResult:
        """Scan dependencies for vulnerabilities"""
        start_time = datetime.now()
        
        try:
            logger.info("Starting dependency vulnerability scan...")
            
            # Run safety check
            safety_result = await self._run_safety_check()
            
            # Parse results
            vulnerabilities = self._parse_safety_results(safety_result)
            
            # Calculate scan duration
            scan_duration = (datetime.now() - start_time).total_seconds()
            
            # Determine status
            status = self._determine_scan_status(vulnerabilities)
            
            # Create scan result
            scan_result = ScanResult(
                timestamp=start_time,
                total_packages=await self._count_packages(),
                vulnerabilities_found=len(vulnerabilities),
                vulnerabilities=vulnerabilities,
                scan_duration=scan_duration,
                status=status
            )
            
            # Store scan result
            self.scan_history.append(scan_result)
            self.last_scan = scan_result
            
            # Keep only last 50 scans
            if len(self.scan_history) > 50:
                self.scan_history = self.scan_history[-50:]
            
            logger.info(f"Dependency scan completed: {len(vulnerabilities)} vulnerabilities found")
            return scan_result
            
        except Exception as e:
            logger.error(f"Dependency scan failed: {e}")
            return ScanResult(
                timestamp=start_time,
                total_packages=0,
                vulnerabilities_found=0,
                vulnerabilities=[],
                scan_duration=(datetime.now() - start_time).total_seconds(),
                status='error'
            )
    
    async def _run_safety_check(self) -> Dict[str, Any]:
        """Run safety check and return results"""
        try:
            # Run safety check with JSON output
            process = await asyncio.create_subprocess_exec(
                'safety', 'check', '--json',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.project_root
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                # No vulnerabilities found
                return {"vulnerabilities": []}
            elif process.returncode == 64:
                # Vulnerabilities found
                return json.loads(stdout.decode())
            else:
                # Error occurred
                logger.error(f"Safety check error: {stderr.decode()}")
                return {"vulnerabilities": []}
                
        except FileNotFoundError:
            logger.warning("Safety tool not found. Install with: pip install safety")
            return {"vulnerabilities": []}
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse safety output: {e}")
            return {"vulnerabilities": []}
        except Exception as e:
            logger.error(f"Safety check failed: {e}")
            return {"vulnerabilities": []}
    
    def _parse_safety_results(self, safety_data: Dict[str, Any]) -> List[Vulnerability]:
        """Parse safety check results into vulnerability objects"""
        vulnerabilities = []
        
        for vuln_data in safety_data.get("vulnerabilities", []):
            try:
                vulnerability = Vulnerability(
                    package_name=vuln_data.get("package_name", "unknown"),
                    current_version=vuln_data.get("analyzed_version", "unknown"),
                    vulnerability_id=vuln_data.get("vulnerability_id", "unknown"),
                    severity=vuln_data.get("severity", "unknown").lower(),
                    advisory=vuln_data.get("advisory", "No advisory available"),
                    cve=vuln_data.get("CVE"),
                    fixed_versions=vuln_data.get("fixed_versions", []),
                    more_info_url=vuln_data.get("more_info_url", "")
                )
                vulnerabilities.append(vulnerability)
            except Exception as e:
                logger.error(f"Failed to parse vulnerability data: {e}")
                continue
        
        return vulnerabilities
    
    async def _count_packages(self) -> int:
        """Count total number of installed packages"""
        try:
            if self.requirements_file.exists():
                with open(self.requirements_file, 'r') as f:
                    lines = f.readlines()
                    # Count non-empty, non-comment lines
                    return len([line for line in lines if line.strip() and not line.strip().startswith('#')])
            else:
                # Fallback: count installed packages
                process = await asyncio.create_subprocess_exec(
                    'pip', 'list', '--format=json',
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, _ = await process.communicate()
                packages = json.loads(stdout.decode())
                return len(packages)
        except Exception as e:
            logger.error(f"Failed to count packages: {e}")
            return 0
    
    def _determine_scan_status(self, vulnerabilities: List[Vulnerability]) -> str:
        """Determine overall scan status based on vulnerabilities"""
        if not vulnerabilities:
            return 'success'
        
        # Calculate risk score
        risk_score = sum(
            self.severity_weights.get(vuln.severity, 1) 
            for vuln in vulnerabilities
        )
        
        if risk_score >= 50:
            return 'critical'
        elif risk_score >= 20:
            return 'warning'
        else:
            return 'info'
    
    def get_vulnerability_summary(self) -> Dict[str, Any]:
        """Get summary of current vulnerabilities"""
        if not self.last_scan:
            return {
                "status": "no_scan",
                "message": "No dependency scan has been performed yet"
            }
        
        vulnerabilities = self.last_scan.vulnerabilities
        
        # Group by severity
        severity_counts = {}
        for vuln in vulnerabilities:
            severity = vuln.severity
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        # Group by package
        package_counts = {}
        for vuln in vulnerabilities:
            package = vuln.package_name
            package_counts[package] = package_counts.get(package, 0) + 1
        
        # Get most critical vulnerabilities
        critical_vulns = [
            vuln for vuln in vulnerabilities 
            if vuln.severity in ['critical', 'high']
        ]
        
        return {
            "last_scan": self.last_scan.timestamp.isoformat(),
            "total_packages": self.last_scan.total_packages,
            "vulnerabilities_found": self.last_scan.vulnerabilities_found,
            "status": self.last_scan.status,
            "severity_breakdown": severity_counts,
            "affected_packages": len(package_counts),
            "package_breakdown": package_counts,
            "critical_vulnerabilities": [
                {
                    "package": vuln.package_name,
                    "version": vuln.current_version,
                    "severity": vuln.severity,
                    "cve": vuln.cve,
                    "advisory": vuln.advisory[:200] + "..." if len(vuln.advisory) > 200 else vuln.advisory
                }
                for vuln in critical_vulns[:5]  # Top 5 critical
            ],
            "recommendations": self._generate_recommendations(vulnerabilities)
        }
    
    def _generate_recommendations(self, vulnerabilities: List[Vulnerability]) -> List[str]:
        """Generate recommendations based on vulnerabilities"""
        recommendations = []
        
        if not vulnerabilities:
            recommendations.append("✅ No vulnerabilities found. Keep dependencies updated.")
            return recommendations
        
        # Count by severity
        critical_count = len([v for v in vulnerabilities if v.severity == 'critical'])
        high_count = len([v for v in vulnerabilities if v.severity == 'high'])
        
        if critical_count > 0:
            recommendations.append(f"🚨 {critical_count} critical vulnerabilities require immediate attention")
        
        if high_count > 0:
            recommendations.append(f"⚠️ {high_count} high-severity vulnerabilities should be addressed soon")
        
        # Package-specific recommendations
        package_counts = {}
        for vuln in vulnerabilities:
            package_counts[vuln.package_name] = package_counts.get(vuln.package_name, 0) + 1
        
        # Find packages with multiple vulnerabilities
        multi_vuln_packages = [pkg for pkg, count in package_counts.items() if count > 1]
        if multi_vuln_packages:
            recommendations.append(f"📦 Consider updating these packages with multiple vulnerabilities: {', '.join(multi_vuln_packages[:3])}")
        
        # General recommendations
        recommendations.append("🔄 Run 'pip install --upgrade' for affected packages")
        recommendations.append("📅 Schedule regular dependency scans (weekly recommended)")
        
        return recommendations
    
    def get_scan_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent scan history"""
        recent_scans = self.scan_history[-limit:] if self.scan_history else []
        
        return [
            {
                "timestamp": scan.timestamp.isoformat(),
                "vulnerabilities_found": scan.vulnerabilities_found,
                "total_packages": scan.total_packages,
                "status": scan.status,
                "scan_duration": round(scan.scan_duration, 2)
            }
            for scan in reversed(recent_scans)
        ]

# Global scanner instance
dependency_scanner = DependencyScanner()

async def run_scheduled_scan():
    """Run a scheduled dependency scan"""
    try:
        result = await dependency_scanner.scan_dependencies()
        
        # Log results
        if result.vulnerabilities_found > 0:
            logger.warning(f"Dependency scan found {result.vulnerabilities_found} vulnerabilities")
        else:
            logger.info("Dependency scan completed - no vulnerabilities found")
        
        return result
    except Exception as e:
        logger.error(f"Scheduled dependency scan failed: {e}")
        return None

async def get_dependency_status() -> Dict[str, Any]:
    """Get current dependency security status"""
    return dependency_scanner.get_vulnerability_summary()
