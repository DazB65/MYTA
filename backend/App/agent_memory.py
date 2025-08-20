"""
Agent Memory & Context System for MYTA
Handles conversation memory, context awareness, and agent switching
"""

import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

from backend.App.redis_service import get_redis_service
from backend.App.supabase_client import get_supabase_service
from backend.App.agent_personalities import get_agent_personality
from backend.logging_config import get_logger, LogCategory

logger = get_logger(__name__, LogCategory.AGENT)

class AgentMemory:
    """Manages agent memory and conversation context"""
    
    def __init__(self):
        self.redis_service = get_redis_service()
        self.supabase = get_supabase_service()
        
        # Memory configuration
        self.max_context_messages = 20  # Maximum messages to keep in context
        self.memory_ttl = 86400 * 7  # 7 days memory retention
        self.summary_threshold = 50  # Summarize after 50 messages
    
    async def get_conversation_context(self, user_id: str, session_id: str, agent_id: str) -> Dict[str, Any]:
        """Get conversation context for an agent"""
        try:
            # Get conversation history from database
            history = await self._get_conversation_history(user_id, session_id)
            
            # Get agent-specific memory
            agent_memory = await self._get_agent_memory(user_id, agent_id)
            
            # Get user preferences and context
            user_context = await self._get_user_context(user_id)
            
            # Build context
            context = {
                "conversation_history": history,
                "agent_memory": agent_memory,
                "user_context": user_context,
                "session_info": {
                    "session_id": session_id,
                    "agent_id": agent_id,
                    "message_count": len(history),
                    "last_interaction": datetime.utcnow().isoformat()
                }
            }
            
            return context
        
        except Exception as e:
            logger.error(f"Error getting conversation context: {e}")
            return {"conversation_history": [], "agent_memory": {}, "user_context": {}}
    
    async def _get_conversation_history(self, user_id: str, session_id: str) -> List[Dict]:
        """Get recent conversation history"""
        try:
            result = self.supabase.select("chat_messages", "*", {
                "user_id": user_id,
                "session_id": session_id
            })
            
            if result["success"]:
                # Sort by timestamp and get recent messages
                messages = sorted(result["data"], key=lambda x: x["created_at"])
                recent_messages = messages[-self.max_context_messages:]
                
                # Format for AI context
                formatted_messages = []
                for msg in recent_messages:
                    formatted_messages.append({
                        "role": msg["role"],
                        "content": msg["content"],
                        "timestamp": msg["created_at"],
                        "agent_id": msg.get("agent_id"),
                        "metadata": msg.get("metadata", {})
                    })
                
                return formatted_messages
            
            return []
        
        except Exception as e:
            logger.error(f"Error getting conversation history: {e}")
            return []
    
    async def _get_agent_memory(self, user_id: str, agent_id: str) -> Dict[str, Any]:
        """Get agent-specific memory for user"""
        try:
            if not self.redis_service.is_available():
                return {}
            
            memory_key = f"agent_memory:{user_id}:{agent_id}"
            memory_data = self.redis_service.get(memory_key)
            
            if memory_data:
                return memory_data
            
            # Initialize empty memory
            empty_memory = {
                "user_preferences": {},
                "conversation_topics": [],
                "user_goals": [],
                "interaction_history": [],
                "last_updated": datetime.utcnow().isoformat()
            }
            
            self.redis_service.set(memory_key, empty_memory, self.memory_ttl)
            return empty_memory
        
        except Exception as e:
            logger.error(f"Error getting agent memory: {e}")
            return {}
    
    async def _get_user_context(self, user_id: str) -> Dict[str, Any]:
        """Get user context and preferences"""
        try:
            # Get user settings
            settings_result = self.supabase.select("user_settings", "*", {"user_id": user_id})
            
            # Get user tasks/goals for context
            tasks_result = self.supabase.select("tasks", "*", {"user_id": user_id})
            goals_result = self.supabase.select("goals", "*", {"user_id": user_id})
            
            context = {
                "settings": settings_result["data"][0] if settings_result["success"] and settings_result["data"] else {},
                "active_tasks": [task for task in tasks_result["data"] if task.get("status") == "in_progress"] if tasks_result["success"] else [],
                "active_goals": [goal for goal in goals_result["data"] if goal.get("status") == "active"] if goals_result["success"] else [],
                "preferences": {}
            }
            
            return context
        
        except Exception as e:
            logger.error(f"Error getting user context: {e}")
            return {}
    
    async def update_agent_memory(self, user_id: str, agent_id: str, interaction_data: Dict[str, Any]):
        """Update agent memory with new interaction"""
        try:
            if not self.redis_service.is_available():
                return
            
            memory_key = f"agent_memory:{user_id}:{agent_id}"
            current_memory = await self._get_agent_memory(user_id, agent_id)
            
            # Update interaction history
            interaction = {
                "timestamp": datetime.utcnow().isoformat(),
                "user_message": interaction_data.get("user_message", ""),
                "agent_response": interaction_data.get("agent_response", ""),
                "topics": interaction_data.get("topics", []),
                "sentiment": interaction_data.get("sentiment", "neutral"),
                "satisfaction": interaction_data.get("satisfaction")
            }
            
            current_memory["interaction_history"].append(interaction)
            
            # Keep only recent interactions
            if len(current_memory["interaction_history"]) > 100:
                current_memory["interaction_history"] = current_memory["interaction_history"][-100:]
            
            # Update conversation topics
            topics = interaction_data.get("topics", [])
            for topic in topics:
                if topic not in current_memory["conversation_topics"]:
                    current_memory["conversation_topics"].append(topic)
            
            # Update user preferences if provided
            if "preferences" in interaction_data:
                current_memory["user_preferences"].update(interaction_data["preferences"])
            
            # Update user goals if mentioned
            if "goals" in interaction_data:
                for goal in interaction_data["goals"]:
                    if goal not in current_memory["user_goals"]:
                        current_memory["user_goals"].append(goal)
            
            current_memory["last_updated"] = datetime.utcnow().isoformat()
            
            # Save updated memory
            self.redis_service.set(memory_key, current_memory, self.memory_ttl)
            
            logger.debug(f"Updated agent memory for user {user_id}, agent {agent_id}")
        
        except Exception as e:
            logger.error(f"Error updating agent memory: {e}")
    
    async def handle_agent_switch(self, user_id: str, session_id: str, old_agent_id: str, new_agent_id: str) -> Dict[str, Any]:
        """Handle switching between agents with context transfer"""
        try:
            # Get context from old agent
            old_context = await self.get_conversation_context(user_id, session_id, old_agent_id)
            
            # Get new agent personality
            new_agent = get_agent_personality(new_agent_id)
            old_agent = get_agent_personality(old_agent_id)
            
            # Create handoff summary
            handoff_summary = {
                "from_agent": {
                    "id": old_agent_id,
                    "name": old_agent["name"],
                    "role": old_agent["role"]
                },
                "to_agent": {
                    "id": new_agent_id,
                    "name": new_agent["name"],
                    "role": new_agent["role"]
                },
                "conversation_summary": await self._summarize_conversation(old_context["conversation_history"]),
                "user_context": old_context["user_context"],
                "timestamp": datetime.utcnow().isoformat()
            }
            
            # Store handoff in new agent's memory
            await self.update_agent_memory(user_id, new_agent_id, {
                "agent_handoff": handoff_summary,
                "topics": self._extract_topics_from_history(old_context["conversation_history"])
            })
            
            # Generate handoff message
            handoff_message = self._generate_handoff_message(old_agent, new_agent, handoff_summary)
            
            return {
                "success": True,
                "handoff_summary": handoff_summary,
                "handoff_message": handoff_message
            }
        
        except Exception as e:
            logger.error(f"Error handling agent switch: {e}")
            return {"success": False, "error": str(e)}
    
    async def _summarize_conversation(self, conversation_history: List[Dict]) -> str:
        """Create a summary of the conversation"""
        try:
            if not conversation_history:
                return "No previous conversation."
            
            # Simple summarization - in production, could use AI for better summaries
            recent_messages = conversation_history[-10:]
            topics = self._extract_topics_from_history(recent_messages)
            
            user_messages = [msg for msg in recent_messages if msg["role"] == "user"]
            
            summary = f"Recent conversation covered {len(topics)} topics: {', '.join(topics[:5])}. "
            summary += f"User asked {len(user_messages)} questions. "
            
            if recent_messages:
                summary += f"Last interaction was about: {recent_messages[-1]['content'][:100]}..."
            
            return summary
        
        except Exception as e:
            logger.error(f"Error summarizing conversation: {e}")
            return "Unable to summarize conversation."
    
    def _extract_topics_from_history(self, conversation_history: List[Dict]) -> List[str]:
        """Extract topics from conversation history"""
        try:
            topics = []
            
            # Simple keyword extraction - could be enhanced with NLP
            keywords = [
                "analytics", "content", "engagement", "growth", "seo", "optimization",
                "youtube", "video", "thumbnail", "title", "description", "tags",
                "audience", "subscribers", "views", "monetization", "revenue"
            ]
            
            for message in conversation_history:
                content = message["content"].lower()
                for keyword in keywords:
                    if keyword in content and keyword not in topics:
                        topics.append(keyword)
            
            return topics[:10]  # Return top 10 topics
        
        except Exception as e:
            logger.error(f"Error extracting topics: {e}")
            return []
    
    def _generate_handoff_message(self, old_agent: Dict, new_agent: Dict, handoff_summary: Dict) -> str:
        """Generate a handoff message for agent switching"""
        try:
            message = f"Hi! I'm {new_agent['name']}, your {new_agent['role']}. "
            message += f"{old_agent['name']} has filled me in on your conversation. "
            
            if handoff_summary.get("conversation_summary"):
                message += f"I understand you've been discussing {handoff_summary['conversation_summary'][:100]}... "
            
            message += f"I'm here to help with {new_agent['expertise']}. How can I assist you?"
            
            return message
        
        except Exception as e:
            logger.error(f"Error generating handoff message: {e}")
            return f"Hi! I'm {new_agent['name']}, your {new_agent['role']}. How can I help you today?"
    
    async def get_memory_stats(self, user_id: str) -> Dict[str, Any]:
        """Get memory statistics for a user"""
        try:
            stats = {
                "total_agents_interacted": 0,
                "total_interactions": 0,
                "favorite_topics": [],
                "agent_usage": {},
                "memory_size": 0
            }
            
            if not self.redis_service.is_available():
                return stats
            
            # Check memory for each agent
            for agent_id in ["1", "2", "3", "4", "5"]:
                memory_key = f"agent_memory:{user_id}:{agent_id}"
                memory_data = self.redis_service.get(memory_key)
                
                if memory_data:
                    stats["total_agents_interacted"] += 1
                    interactions = len(memory_data.get("interaction_history", []))
                    stats["total_interactions"] += interactions
                    stats["agent_usage"][agent_id] = interactions
                    
                    # Add topics
                    topics = memory_data.get("conversation_topics", [])
                    stats["favorite_topics"].extend(topics)
            
            # Get unique topics and sort by frequency
            topic_counts = {}
            for topic in stats["favorite_topics"]:
                topic_counts[topic] = topic_counts.get(topic, 0) + 1
            
            stats["favorite_topics"] = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            
            return stats
        
        except Exception as e:
            logger.error(f"Error getting memory stats: {e}")
            return {"error": str(e)}

# Global agent memory instance
_agent_memory: Optional[AgentMemory] = None

def get_agent_memory() -> AgentMemory:
    """Get or create global agent memory instance"""
    global _agent_memory
    if _agent_memory is None:
        _agent_memory = AgentMemory()
    return _agent_memory
