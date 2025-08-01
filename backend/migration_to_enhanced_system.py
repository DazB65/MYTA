"""
Migration Script for Enhanced Vidalytics System
Helps migrate from the old monolithic system to the new modular architecture
"""

import os
import shutil
import logging
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class SystemMigration:
    """Handles migration to the enhanced system"""
    
    def __init__(self, backup_dir: str = "backup_migration"):
        self.backup_dir = Path(backup_dir)
        self.migration_log = []
        self.success = True
    
    def log_step(self, step: str, success: bool = True, details: str = ""):
        """Log migration step"""
        self.migration_log.append({
            "step": step,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
        
        if success:
            logger.info(f"✅ {step}: {details}")
        else:
            logger.error(f"❌ {step}: {details}")
            self.success = False
    
    def create_backup(self):
        """Create backup of original files before migration"""
        try:
            self.backup_dir.mkdir(exist_ok=True)
            
            # Files to backup
            files_to_backup = [
                "boss_agent.py",
                "database.py", 
                "rate_limiter.py",
                "main.py"
            ]
            
            for file_name in files_to_backup:
                file_path = Path(file_name)
                if file_path.exists():
                    backup_path = self.backup_dir / f"{file_name}.backup"
                    shutil.copy2(file_path, backup_path)
                    self.log_step(f"Backup {file_name}", True, f"Backed up to {backup_path}")
                else:
                    self.log_step(f"Backup {file_name}", False, "File not found")
                    
        except Exception as e:
            self.log_step("Create backup", False, str(e))
    
    def update_imports(self):
        """Update import statements in existing files"""
        try:
            # Update main.py to use new modules
            main_py_updates = [
                ("from boss_agent import", "from boss_agent_core import"),
                ("from database import", "from enhanced_database_manager import"),
                ("from rate_limiter import", "from enhanced_rate_limiter import")
            ]
            
            self._update_file_imports("main.py", main_py_updates)
            self.log_step("Update main.py imports", True, "Updated to use enhanced modules")
            
            # Update agent router imports
            agent_router_updates = [
                ("from boss_agent import", "from boss_agent_core import"),
                ("from standardized_errors import", "from standardized_error_responses import")
            ]
            
            self._update_file_imports("agent_router.py", agent_router_updates)
            self.log_step("Update agent_router.py imports", True, "Updated import statements")
            
        except Exception as e:
            self.log_step("Update imports", False, str(e))
    
    def _update_file_imports(self, file_path: str, updates: List[tuple]):
        """Update imports in a specific file"""
        file_path = Path(file_path)
        if not file_path.exists():
            return
        
        content = file_path.read_text()
        
        for old_import, new_import in updates:
            content = content.replace(old_import, new_import)
        
        file_path.write_text(content)
    
    def setup_enhanced_database(self):
        """Initialize the enhanced database system"""
        try:
            from enhanced_database_manager import get_enhanced_db_manager
            
            db_manager = get_enhanced_db_manager()
            self.log_step("Initialize enhanced database", True, "Database system ready")
            
        except Exception as e:
            self.log_step("Setup enhanced database", False, str(e))
    
    def setup_rate_limiting(self):
        """Initialize the enhanced rate limiting system"""
        try:
            from enhanced_rate_limiter import get_rate_limiter
            
            rate_limiter = get_rate_limiter()
            self.log_step("Initialize rate limiting", True, "Rate limiting system ready")
            
        except Exception as e:
            self.log_step("Setup rate limiting", False, str(e))
    
    def setup_health_checks(self):
        """Initialize the health check system"""
        try:
            from comprehensive_health_checks import get_health_checker
            
            health_checker = get_health_checker()
            self.log_step("Initialize health checks", True, "Health check system ready")
            
        except Exception as e:
            self.log_step("Setup health checks", False, str(e))
    
    def verify_agent_system(self):
        """Verify the new agent system works"""
        try:
            from boss_agent_core import get_boss_agent
            from agent_coordinators import get_agent_coordinators
            from intent_classifier import get_intent_classifier
            
            # Test boss agent initialization
            boss_agent = get_boss_agent()
            self.log_step("Verify boss agent", True, "Boss agent initialized successfully")
            
            # Test coordinators
            coordinators = get_agent_coordinators()
            self.log_step("Verify coordinators", True, f"{len(coordinators)} coordinators available")
            
            # Test intent classifier
            classifier = get_intent_classifier()
            self.log_step("Verify intent classifier", True, "Intent classifier ready")
            
        except Exception as e:
            self.log_step("Verify agent system", False, str(e))
    
    def create_middleware_integration(self):
        """Create middleware to integrate new systems with FastAPI"""
        middleware_code = '''"""
Enhanced Middleware Integration for Vidalytics
Integrates rate limiting, error handling, and health checks with FastAPI
"""

from fastapi import Request, Response
from fastapi.responses import JSONResponse
import time
import logging

from enhanced_rate_limiter import get_rate_limiter
from standardized_error_responses import get_error_handler, CommonErrors
from comprehensive_health_checks import get_health_checker

logger = logging.getLogger(__name__)

async def rate_limiting_middleware(request: Request, call_next):
    """Rate limiting middleware"""
    try:
        # Extract user ID from request (implement based on your auth system)
        user_id = request.headers.get("user-id", "anonymous")
        agent_type = request.url.path.split("/")[-1] if request.url.path else "general"
        
        # Check rate limit
        rate_limiter = get_rate_limiter()
        result = await rate_limiter.check_rate_limit(user_id, agent_type)
        
        if not result.allowed:
            error_response = CommonErrors.rate_limit_exceeded(
                result.limit_type, 
                result.retry_after or 60,
                request.headers.get("request-id")
            )
            return JSONResponse(
                status_code=429,
                content=error_response.to_dict(),
                headers={"Retry-After": str(result.retry_after or 60)}
            )
        
        response = await call_next(request)
        
        # Add rate limit headers
        response.headers["X-RateLimit-Remaining"] = str(result.remaining)
        response.headers["X-RateLimit-Reset"] = str(int(result.reset_time))
        
        return response
        
    except Exception as e:
        logger.error(f"Rate limiting middleware error: {e}")
        return await call_next(request)

async def error_handling_middleware(request: Request, call_next):
    """Global error handling middleware"""
    try:
        return await call_next(request)
        
    except Exception as e:
        error_handler = get_error_handler()
        error_response = error_handler.handle_exception(
            e,
            request.headers.get("request-id"),
            request.url.path.split("/")[-1]
        )
        
        status_code = error_handler.HTTP_STATUS_MAPPING.get(
            error_response.error_category, 500
        )
        
        return JSONResponse(
            status_code=status_code,
            content=error_response.to_dict()
        )

async def health_check_endpoint():
    """Health check endpoint"""
    from comprehensive_health_checks import quick_health_check
    return await quick_health_check()

async def full_health_check_endpoint():
    """Full health check endpoint"""
    from comprehensive_health_checks import full_health_check
    return await full_health_check()
'''
        
        try:
            with open("enhanced_middleware.py", "w") as f:
                f.write(middleware_code)
            self.log_step("Create middleware integration", True, "Middleware file created")
        except Exception as e:
            self.log_step("Create middleware integration", False, str(e))
    
    def generate_migration_report(self):
        """Generate migration report"""
        report = {
            "migration_date": datetime.now().isoformat(),
            "overall_success": self.success,
            "steps_completed": len([step for step in self.migration_log if step["success"]]),
            "total_steps": len(self.migration_log),
            "detailed_log": self.migration_log
        }
        
        try:
            with open("migration_report.json", "w") as f:
                import json
                json.dump(report, f, indent=2)
            
            print("\n" + "="*60)
            print("🚀 MIGRATION REPORT")
            print("="*60)
            print(f"Overall Success: {'✅ YES' if self.success else '❌ NO'}")
            print(f"Steps Completed: {report['steps_completed']}/{report['total_steps']}")
            print(f"Report saved to: migration_report.json")
            print("="*60)
            
            if self.success:
                print("\n🎉 Migration completed successfully!")
                print("\nNext steps:")
                print("1. Update your main.py to use the new middleware")
                print("2. Test the enhanced system")
                print("3. Monitor health checks and error rates")
                print("4. Consider removing old backup files after verification")
            else:
                print("\n⚠️  Migration had some issues. Check the log for details.")
                print("You may need to manually fix some issues.")
            
        except Exception as e:
            logger.error(f"Failed to generate migration report: {e}")
    
    def run_migration(self):
        """Run the complete migration process"""
        print("🔄 Starting Vidalytics Enhanced System Migration...")
        
        # Step 1: Create backups
        self.create_backup()
        
        # Step 2: Setup new systems
        self.setup_enhanced_database()
        self.setup_rate_limiting()
        self.setup_health_checks()
        
        # Step 3: Verify agent system
        self.verify_agent_system()
        
        # Step 4: Update imports
        self.update_imports()
        
        # Step 5: Create middleware integration
        self.create_middleware_integration()
        
        # Step 6: Generate report
        self.generate_migration_report()
        
        return self.success

if __name__ == "__main__":
    # Run the migration
    migration = SystemMigration()
    success = migration.run_migration()
    
    exit(0 if success else 1)