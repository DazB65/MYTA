"""
API Startup and Initialization for CreatorMate Multi-Agent System
Handles system initialization, health checks, and startup validation
"""

import os
import asyncio
import logging
from typing import Dict, Any, List
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)

class CreatorMateStartup:
    """Handles startup initialization for the CreatorMate API"""
    
    def __init__(self):
        self.startup_time = datetime.now()
        self.initialization_status = {}
        self.required_env_vars = [
            "OPENAI_API_KEY",
            "YOUTUBE_API_KEY"
        ]
        self.optional_env_vars = [
            "ANTHROPIC_API_KEY",
            "GOOGLE_API_KEY", 
            "BOSS_AGENT_SECRET_KEY"
        ]
    
    async def initialize_system(self) -> Dict[str, Any]:
        """Initialize all system components"""
        logger.info("Starting CreatorMate Multi-Agent System initialization...")
        
        initialization_results = {
            "startup_time": self.startup_time.isoformat(),
            "environment_check": await self._check_environment(),
            "model_integrations": await self._initialize_model_integrations(),
            "youtube_api": await self._initialize_youtube_api(),
            "agent_system": await self._initialize_agent_system(),
            "cache_system": await self._initialize_cache_system(),
            "data_pipeline": await self._initialize_data_pipeline(),
            "authentication": await self._initialize_authentication(),
            "overall_status": "pending"
        }
        
        # Determine overall status
        critical_systems = ["environment_check", "model_integrations", "agent_system"]
        all_critical_ok = all(
            initialization_results[system]["status"] == "success" 
            for system in critical_systems
        )
        
        if all_critical_ok:
            initialization_results["overall_status"] = "success"
            logger.info("✅ CreatorMate system initialization successful")
        else:
            initialization_results["overall_status"] = "partial"
            logger.warning("⚠️ CreatorMate system initialization completed with warnings")
        
        self.initialization_status = initialization_results
        return initialization_results
    
    async def _check_environment(self) -> Dict[str, Any]:
        """Check environment variables and configuration"""
        logger.info("Checking environment configuration...")
        
        missing_required = []
        missing_optional = []
        configured_vars = []
        
        # Check required environment variables
        for var in self.required_env_vars:
            if os.getenv(var):
                configured_vars.append(var)
            else:
                missing_required.append(var)
        
        # Check optional environment variables
        for var in self.optional_env_vars:
            if os.getenv(var):
                configured_vars.append(var)
            else:
                missing_optional.append(var)
        
        status = "success" if not missing_required else "error"
        
        result = {
            "status": status,
            "configured_vars": configured_vars,
            "missing_required": missing_required,
            "missing_optional": missing_optional,
            "recommendations": []
        }
        
        # Add recommendations
        if missing_required:
            result["recommendations"].append(
                f"Set required environment variables: {', '.join(missing_required)}"
            )
        
        if missing_optional:
            result["recommendations"].append(
                f"Consider setting optional variables for full functionality: {', '.join(missing_optional)}"
            )
        
        if status == "success":
            logger.info("✅ Environment configuration check passed")
        else:
            logger.error(f"❌ Environment check failed: missing {missing_required}")
        
        return result
    
    async def _initialize_model_integrations(self) -> Dict[str, Any]:
        """Initialize AI model integrations"""
        logger.info("Initializing AI model integrations...")
        
        try:
            from model_integrations import get_model_integration
            
            integration = get_model_integration()
            model_status = integration.get_model_status()
            available_models = integration.get_available_models()
            
            # Count active integrations
            active_count = sum(1 for status in model_status.values() if status["available"])
            total_count = len(model_status)
            
            status = "success" if active_count > 0 else "error"
            
            result = {
                "status": status,
                "active_integrations": active_count,
                "total_integrations": total_count,
                "model_status": model_status,
                "available_models": available_models,
                "recommendations": []
            }
            
            # Add recommendations
            if active_count == 0:
                result["recommendations"].append("No AI model integrations available. Check API keys.")
            elif active_count < total_count:
                result["recommendations"].append("Some model integrations unavailable. Check optional API keys for full functionality.")
            
            logger.info(f"✅ Model integrations initialized: {active_count}/{total_count} active")
            return result
            
        except Exception as e:
            logger.error(f"❌ Model integration initialization failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "recommendations": ["Check model integration configuration and API keys"]
            }
    
    async def _initialize_youtube_api(self) -> Dict[str, Any]:
        """Initialize YouTube API integration"""
        logger.info("Initializing YouTube API integration...")
        
        try:
            from youtube_api_integration import get_youtube_integration
            
            integration = get_youtube_integration()
            api_status = integration.get_api_status()
            
            status = "success" if api_status["api_available"] else "error"
            
            result = {
                "status": status,
                "api_status": api_status,
                "recommendations": []
            }
            
            if not api_status["api_available"]:
                result["recommendations"].append("YouTube API not available. Check YOUTUBE_API_KEY.")
            
            logger.info(f"✅ YouTube API initialized: {api_status['api_available']}")
            return result
            
        except Exception as e:
            logger.error(f"❌ YouTube API initialization failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "recommendations": ["Check YouTube API configuration"]
            }
    
    async def _initialize_agent_system(self) -> Dict[str, Any]:
        """Initialize multi-agent system"""
        logger.info("Initializing multi-agent system...")
        
        try:
            # Test boss agent import
            from boss_agent import get_boss_agent
            boss_agent = get_boss_agent()
            
            # Test specialized agent imports
            agent_imports = {
                "content_analysis": "content_analysis_agent",
                "audience_insights": "audience_insights_agent", 
                "seo_discoverability": "seo_discoverability_agent",
                "competitive_analysis": "competitive_analysis_agent",
                "monetization_strategy": "monetization_strategy_agent"
            }
            
            available_agents = []
            failed_agents = []
            
            for agent_name, module_name in agent_imports.items():
                try:
                    __import__(module_name)
                    available_agents.append(agent_name)
                except Exception as e:
                    failed_agents.append(f"{agent_name}: {e}")
            
            status = "success" if len(available_agents) >= 3 else "error"  # Need at least 3 agents
            
            result = {
                "status": status,
                "boss_agent_available": True,
                "available_agents": available_agents,
                "failed_agents": failed_agents,
                "total_agents": len(available_agents),
                "recommendations": []
            }
            
            if failed_agents:
                result["recommendations"].append(f"Some agents failed to load: {failed_agents}")
            
            logger.info(f"✅ Agent system initialized: {len(available_agents)}/5 agents available")
            return result
            
        except Exception as e:
            logger.error(f"❌ Agent system initialization failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "recommendations": ["Check agent system configuration and dependencies"]
            }
    
    async def _initialize_cache_system(self) -> Dict[str, Any]:
        """Initialize caching system"""
        logger.info("Initializing cache system...")
        
        try:
            from agent_cache import get_agent_cache
            
            cache = get_agent_cache()
            cache_stats = cache.get_stats()
            
            result = {
                "status": "success",
                "cache_stats": cache_stats,
                "recommendations": []
            }
            
            logger.info("✅ Cache system initialized")
            return result
            
        except Exception as e:
            logger.error(f"❌ Cache system initialization failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "recommendations": ["Check cache system configuration"]
            }
    
    async def _initialize_data_pipeline(self) -> Dict[str, Any]:
        """Initialize real-time data pipeline"""
        logger.info("Initializing real-time data pipeline...")
        
        try:
            from realtime_data_pipeline import get_data_pipeline
            from enhanced_user_context import get_enhanced_context_manager
            from analytics_service import get_analytics_service
            
            # Initialize data pipeline
            data_pipeline = get_data_pipeline()
            
            # Initialize enhanced context manager
            context_manager = get_enhanced_context_manager()
            
            # Initialize analytics service
            analytics_service = get_analytics_service()
            
            # Start background monitoring if available
            try:
                # Start background monitoring tasks
                await data_pipeline.start_background_monitoring()
                monitoring_status = "active"
            except Exception as e:
                logger.warning(f"Background monitoring not started: {e}")
                monitoring_status = "disabled"
            
            result = {
                "status": "success",
                "pipeline_status": "initialized",
                "context_manager": "ready",
                "analytics_service": "ready", 
                "background_monitoring": monitoring_status,
                "recommendations": []
            }
            
            if monitoring_status == "disabled":
                result["recommendations"].append("Background monitoring disabled - some real-time features may be limited")
            
            logger.info("✅ Real-time data pipeline initialized")
            return result
            
        except Exception as e:
            logger.error(f"❌ Data pipeline initialization failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "recommendations": [
                    "Check data pipeline dependencies",
                    "Verify OAuth and analytics service configuration"
                ]
            }
    
    async def _initialize_authentication(self) -> Dict[str, Any]:
        """Initialize authentication system"""
        logger.info("Initializing authentication system...")
        
        try:
            from boss_agent_auth import get_boss_agent_authenticator
            
            authenticator = get_boss_agent_authenticator()
            
            # Test token generation
            test_token = authenticator.generate_boss_agent_token("test_request")
            validation_result = authenticator.validate_boss_agent_token(test_token, "test_request")
            
            status = "success" if validation_result.is_valid else "error"
            
            result = {
                "status": status,
                "jwt_authentication": validation_result.is_valid,
                "secret_configured": bool(os.getenv("BOSS_AGENT_SECRET_KEY")),
                "recommendations": []
            }
            
            if not result["secret_configured"]:
                result["recommendations"].append("Consider setting BOSS_AGENT_SECRET_KEY for persistent authentication")
            
            logger.info(f"✅ Authentication system initialized: JWT working={validation_result.is_valid}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Authentication system initialization failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "recommendations": ["Check authentication system configuration"]
            }
    
    def get_startup_summary(self) -> Dict[str, Any]:
        """Get a summary of the startup status"""
        if not self.initialization_status:
            return {"status": "not_initialized", "message": "System not yet initialized"}
        
        # Count successful vs failed systems
        successful_systems = 0
        total_systems = 0
        warnings = []
        
        for system_name, system_status in self.initialization_status.items():
            if system_name in ["startup_time", "overall_status"]:
                continue
                
            total_systems += 1
            if isinstance(system_status, dict) and system_status.get("status") == "success":
                successful_systems += 1
            elif isinstance(system_status, dict) and system_status.get("recommendations"):
                warnings.extend(system_status["recommendations"])
        
        return {
            "overall_status": self.initialization_status["overall_status"],
            "successful_systems": successful_systems,
            "total_systems": total_systems,
            "success_rate": (successful_systems / total_systems * 100) if total_systems > 0 else 0,
            "warnings": warnings,
            "startup_time": self.initialization_status["startup_time"],
            "ready_for_requests": self.initialization_status["overall_status"] in ["success", "partial"]
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform a quick health check"""
        try:
            # Quick checks for critical systems
            health_status = {
                "timestamp": datetime.now().isoformat(),
                "uptime_seconds": (datetime.now() - self.startup_time).total_seconds(),
                "status": "healthy"
            }
            
            # Check if core systems are still working
            try:
                from model_integrations import get_model_integration
                model_integration = get_model_integration()
                health_status["model_integrations"] = "available"
            except:
                health_status["model_integrations"] = "unavailable"
                health_status["status"] = "degraded"
            
            try:
                from agent_cache import get_agent_cache
                cache = get_agent_cache()
                cache.get_stats()  # Test cache access
                health_status["cache_system"] = "available"
            except:
                health_status["cache_system"] = "unavailable"
                health_status["status"] = "degraded"
            
            return health_status
            
        except Exception as e:
            return {
                "timestamp": datetime.now().isoformat(),
                "status": "unhealthy",
                "error": str(e)
            }

# Global startup instance
_startup_manager = None

def get_startup_manager() -> CreatorMateStartup:
    """Get or create global startup manager"""
    global _startup_manager
    if _startup_manager is None:
        _startup_manager = CreatorMateStartup()
    return _startup_manager

async def initialize_creatormate_system():
    """Initialize the CreatorMate system"""
    startup_manager = get_startup_manager()
    return await startup_manager.initialize_system()

def get_system_status():
    """Get current system status"""
    startup_manager = get_startup_manager()
    return startup_manager.get_startup_summary()