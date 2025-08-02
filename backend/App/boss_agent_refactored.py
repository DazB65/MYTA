"""
Boss Agent Orchestration System for Vidalytics - Refactored Version
This is the new modular implementation - the original boss_agent.py will be deprecated
"""

# Import all functionality from the new modular structure
from boss_agent_core import BossAgent, get_boss_agent, process_user_message
from backend.App.agent_models import QueryType, Priority, Context, TokenBudget, AgentRequest, AgentResponse
from intent_classifier import IntentClassifier, get_intent_classifier  
from voice_analyzer import VoiceAnalyzer, get_voice_analyzer
from agent_coordinators import get_agent_coordinators

# Re-export everything for backward compatibility
__all__ = [
    'BossAgent',
    'get_boss_agent', 
    'process_user_message',
    'QueryType',
    'Priority',
    'Context',
    'TokenBudget',
    'AgentRequest', 
    'AgentResponse',
    'IntentClassifier',
    'get_intent_classifier',
    'VoiceAnalyzer',
    'get_voice_analyzer',
    'get_agent_coordinators'
]

# Maintain backward compatibility with existing imports
def get_boss_agent_instance():
    """Legacy function name for backward compatibility"""
    return get_boss_agent()

async def process_message(message: str, context: dict):
    """Legacy function name for backward compatibility"""  
    return await process_user_message(message, context)