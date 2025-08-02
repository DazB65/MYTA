"""
Enhanced Rate Limiting System for Vidalytics
Implements sophisticated rate limiting with multiple strategies and user tiers
"""

import time
import asyncio
import hashlib
import logging
from typing import Dict, Optional, Tuple, List, Any
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta
from collections import defaultdict, deque
import json

logger = logging.getLogger(__name__)

class RateLimitStrategy(Enum):
    """Different rate limiting strategies"""
    TOKEN_BUCKET = "token_bucket"
    SLIDING_WINDOW = "sliding_window"
    FIXED_WINDOW = "fixed_window"
    LEAKY_BUCKET = "leaky_bucket"

class UserTier(Enum):
    """User tier for different rate limits"""
    FREE = "free"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"
    ADMIN = "admin"

@dataclass
class RateLimitConfig:
    """Configuration for rate limiting"""
    requests_per_minute: int = 60
    requests_per_hour: int = 1000
    requests_per_day: int = 10000
    burst_size: int = 10
    strategy: RateLimitStrategy = RateLimitStrategy.TOKEN_BUCKET
    user_tier: UserTier = UserTier.FREE
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class RateLimitResult:
    """Result of rate limit check"""
    allowed: bool
    remaining: int
    reset_time: float
    retry_after: Optional[int] = None
    limit_type: str = "general"
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class TokenBucket:
    """Token bucket rate limiter implementation"""
    
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate  # tokens per second
        self.last_refill = time.time()
    
    def consume(self, tokens: int = 1) -> bool:
        """Try to consume tokens from the bucket"""
        now = time.time()
        
        # Add tokens based on time elapsed
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now
        
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False
    
    def get_remaining(self) -> int:
        """Get remaining tokens"""
        now = time.time()
        elapsed = now - self.last_refill
        current_tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        return int(current_tokens)

class SlidingWindowCounter:
    """Sliding window rate limiter implementation"""
    
    def __init__(self, window_size: int, max_requests: int):
        self.window_size = window_size  # seconds
        self.max_requests = max_requests
        self.requests = deque()
    
    def is_allowed(self) -> Tuple[bool, int]:
        """Check if request is allowed and return remaining count"""
        now = time.time()
        
        # Remove old requests outside the window
        while self.requests and self.requests[0] <= now - self.window_size:
            self.requests.popleft()
        
        # Check if we can allow the request
        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return True, self.max_requests - len(self.requests)
        
        return False, 0
    
    def get_reset_time(self) -> float:
        """Get time when the oldest request will expire"""
        if not self.requests:
            return time.time()
        return self.requests[0] + self.window_size

class EnhancedRateLimiter:
    """Enhanced rate limiter with multiple strategies and user tiers"""
    
    # Tier-based configurations
    TIER_CONFIGS = {
        UserTier.FREE: RateLimitConfig(
            requests_per_minute=30,
            requests_per_hour=500,
            requests_per_day=5000,
            burst_size=5
        ),
        UserTier.PREMIUM: RateLimitConfig(
            requests_per_minute=120,
            requests_per_hour=2000,
            requests_per_day=20000,
            burst_size=20
        ),
        UserTier.ENTERPRISE: RateLimitConfig(
            requests_per_minute=300,
            requests_per_hour=5000,
            requests_per_day=50000,
            burst_size=50
        ),
        UserTier.ADMIN: RateLimitConfig(
            requests_per_minute=1000,
            requests_per_hour=10000,
            requests_per_day=100000,
            burst_size=100
        )
    }
    
    # Agent-specific rate limits
    AGENT_LIMITS = {
        "boss_agent": {"multiplier": 1.0, "burst_multiplier": 1.0},
        "content_analysis": {"multiplier": 0.8, "burst_multiplier": 0.7},
        "audience_insights": {"multiplier": 0.8, "burst_multiplier": 0.7},
        "seo_discoverability": {"multiplier": 0.6, "burst_multiplier": 0.5},
        "competitive_analysis": {"multiplier": 0.5, "burst_multiplier": 0.4},
        "monetization_strategy": {"multiplier": 0.6, "burst_multiplier": 0.5}
    }
    
    def __init__(self):
        # Store rate limiters by user and time window
        self._token_buckets: Dict[str, TokenBucket] = {}
        self._sliding_windows: Dict[str, Dict[str, SlidingWindowCounter]] = defaultdict(dict)
        self._user_tiers: Dict[str, UserTier] = {}
        
        # Track usage statistics
        self._usage_stats: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self._blocked_requests: Dict[str, List[float]] = defaultdict(list)
        
        logger.info("Enhanced rate limiter initialized")
    
    def set_user_tier(self, user_id: str, tier: UserTier):
        """Set user tier for rate limiting"""
        self._user_tiers[user_id] = tier
        # Clear existing limiters to apply new limits
        self._clear_user_limiters(user_id)
        logger.info(f"Set user {user_id} to tier {tier.value}")
    
    def get_user_tier(self, user_id: str) -> UserTier:
        """Get user tier, defaulting to FREE"""
        return self._user_tiers.get(user_id, UserTier.FREE)
    
    def _clear_user_limiters(self, user_id: str):
        """Clear existing limiters for a user"""
        keys_to_remove = [key for key in self._token_buckets.keys() if key.startswith(f"{user_id}:")]
        for key in keys_to_remove:
            del self._token_buckets[key]
        
        if user_id in self._sliding_windows:
            del self._sliding_windows[user_id]
    
    def _get_config_for_agent(self, user_id: str, agent_type: str) -> RateLimitConfig:
        """Get rate limit configuration for specific agent and user"""
        tier = self.get_user_tier(user_id)
        base_config = self.TIER_CONFIGS[tier]
        
        # Apply agent-specific multipliers
        agent_limits = self.AGENT_LIMITS.get(agent_type, {"multiplier": 1.0, "burst_multiplier": 1.0})
        
        return RateLimitConfig(
            requests_per_minute=int(base_config.requests_per_minute * agent_limits["multiplier"]),
            requests_per_hour=int(base_config.requests_per_hour * agent_limits["multiplier"]),
            requests_per_day=int(base_config.requests_per_day * agent_limits["multiplier"]),
            burst_size=int(base_config.burst_size * agent_limits["burst_multiplier"]),
            strategy=base_config.strategy,
            user_tier=tier
        )
    
    def _get_token_bucket(self, user_id: str, agent_type: str) -> TokenBucket:
        """Get or create token bucket for user and agent"""
        key = f"{user_id}:{agent_type}"
        
        if key not in self._token_buckets:
            config = self._get_config_for_agent(user_id, agent_type)
            # Use per-minute limit for token bucket with burst capacity
            self._token_buckets[key] = TokenBucket(
                capacity=config.burst_size,
                refill_rate=config.requests_per_minute / 60.0  # tokens per second
            )
        
        return self._token_buckets[key]
    
    def _get_sliding_window(self, user_id: str, agent_type: str, window_type: str) -> SlidingWindowCounter:
        """Get or create sliding window counter"""
        if window_type not in self._sliding_windows[user_id]:
            config = self._get_config_for_agent(user_id, agent_type)
            
            if window_type == "minute":
                window_size, max_requests = 60, config.requests_per_minute
            elif window_type == "hour":
                window_size, max_requests = 3600, config.requests_per_hour
            elif window_type == "day":
                window_size, max_requests = 86400, config.requests_per_day
            else:
                raise ValueError(f"Unknown window type: {window_type}")
            
            self._sliding_windows[user_id][window_type] = SlidingWindowCounter(window_size, max_requests)
        
        return self._sliding_windows[user_id][window_type]
    
    async def check_rate_limit(self, user_id: str, agent_type: str = "general", 
                              request_weight: int = 1) -> RateLimitResult:
        """
        Check if request is allowed under rate limits
        
        Args:
            user_id: Unique identifier for the user
            agent_type: Type of agent making the request
            request_weight: Weight of the request (default 1)
            
        Returns:
            RateLimitResult with decision and metadata
        """
        try:
            # Check token bucket (for burst protection)
            bucket = self._get_token_bucket(user_id, agent_type)
            bucket_allowed = bucket.consume(request_weight)
            
            if not bucket_allowed:
                self._record_blocked_request(user_id, agent_type, "burst")
                return RateLimitResult(
                    allowed=False,
                    remaining=bucket.get_remaining(),
                    reset_time=time.time() + 60,  # Reset in 1 minute
                    retry_after=60,
                    limit_type="burst"
                )
            
            # Check sliding windows (for sustained rate limiting)
            windows = ["minute", "hour", "day"]
            for window_type in windows:
                window = self._get_sliding_window(user_id, agent_type, window_type)
                allowed, remaining = window.is_allowed()
                
                if not allowed:
                    # Rollback bucket consumption since we're rejecting
                    bucket.tokens = min(bucket.capacity, bucket.tokens + request_weight)
                    
                    self._record_blocked_request(user_id, agent_type, window_type)
                    
                    retry_after = int(window.get_reset_time() - time.time()) + 1
                    return RateLimitResult(
                        allowed=False,
                        remaining=remaining,
                        reset_time=window.get_reset_time(),
                        retry_after=retry_after,
                        limit_type=window_type
                    )
            
            # Request is allowed
            self._record_successful_request(user_id, agent_type)
            
            # Get remaining from the most restrictive limit
            minute_window = self._get_sliding_window(user_id, agent_type, "minute")
            _, remaining = minute_window.is_allowed()
            
            return RateLimitResult(
                allowed=True,
                remaining=remaining,
                reset_time=minute_window.get_reset_time(),
                limit_type="minute"
            )
            
        except Exception as e:
            logger.error(f"Rate limit check failed for {user_id}:{agent_type}: {e}")
            # Fail open - allow the request but log the error
            return RateLimitResult(
                allowed=True,
                remaining=999,
                reset_time=time.time() + 3600,
                limit_type="error"
            )
    
    def _record_successful_request(self, user_id: str, agent_type: str):
        """Record a successful request for statistics"""
        key = f"{user_id}:{agent_type}"
        self._usage_stats[key]["allowed"] += 1
        self._usage_stats[key]["total"] += 1
    
    def _record_blocked_request(self, user_id: str, agent_type: str, limit_type: str):
        """Record a blocked request for statistics"""
        key = f"{user_id}:{agent_type}"
        self._usage_stats[key]["blocked"] += 1
        self._usage_stats[key]["total"] += 1
        self._usage_stats[key][f"blocked_{limit_type}"] += 1
        
        # Track blocked request timestamps for analysis
        self._blocked_requests[key].append(time.time())
        
        # Keep only recent blocked requests (last hour)
        cutoff = time.time() - 3600
        self._blocked_requests[key] = [
            ts for ts in self._blocked_requests[key] if ts > cutoff
        ]
        
        logger.warning(f"Blocked request for {user_id}:{agent_type} due to {limit_type} limit")
    
    def get_usage_stats(self, user_id: str) -> Dict[str, Any]:
        """Get usage statistics for a user"""
        user_stats = {}
        tier = self.get_user_tier(user_id)
        
        for key, stats in self._usage_stats.items():
            if key.startswith(f"{user_id}:"):
                agent_type = key.split(":", 1)[1]
                user_stats[agent_type] = dict(stats)
        
        return {
            "user_id": user_id,
            "tier": tier.value,
            "stats": user_stats,
            "blocked_requests_last_hour": len(self._blocked_requests.get(user_id, []))
        }
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get system-wide rate limiting statistics"""
        total_requests = 0
        total_blocked = 0
        tier_breakdown = defaultdict(int)
        
        for key, stats in self._usage_stats.items():
            total_requests += stats["total"]
            total_blocked += stats["blocked"]
        
        for user_id, tier in self._user_tiers.items():
            tier_breakdown[tier.value] += 1
        
        return {
            "total_requests": total_requests,
            "total_blocked": total_blocked,
            "block_rate": total_blocked / max(total_requests, 1),
            "active_users": len(set(key.split(":")[0] for key in self._usage_stats.keys())),
            "tier_breakdown": dict(tier_breakdown),
            "timestamp": datetime.now().isoformat()
        }
    
    def cleanup_expired_data(self):
        """Clean up expired data to prevent memory leaks"""
        current_time = time.time()
        cutoff_time = current_time - 86400  # Keep data for 24 hours
        
        # Clean up blocked requests tracking
        for key in list(self._blocked_requests.keys()):
            self._blocked_requests[key] = [
                ts for ts in self._blocked_requests[key] if ts > cutoff_time
            ]
            if not self._blocked_requests[key]:
                del self._blocked_requests[key]
        
        logger.debug("Cleaned up expired rate limiting data")

# Global rate limiter instance
_rate_limiter: Optional[EnhancedRateLimiter] = None

def get_rate_limiter() -> EnhancedRateLimiter:
    """Get or create global rate limiter instance"""
    global _rate_limiter
    if _rate_limiter is None:
        _rate_limiter = EnhancedRateLimiter()
    return _rate_limiter

# Decorator for rate limiting
def rate_limit(agent_type: str = "general", weight: int = 1):
    """Decorator to add rate limiting to functions"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Extract user_id from kwargs or args
            user_id = kwargs.get('user_id') or (args[0] if args else "anonymous")
            
            limiter = get_rate_limiter()
            result = await limiter.check_rate_limit(user_id, agent_type, weight)
            
            if not result.allowed:
                from fastapi import HTTPException
                raise HTTPException(
                    status_code=429,
                    detail={
                        "error": "Rate limit exceeded",
                        "limit_type": result.limit_type,
                        "retry_after": result.retry_after,
                        "reset_time": result.reset_time
                    }
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator