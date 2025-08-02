"""
Circuit Breaker Pattern Implementation for Vidalytics
Provides fault tolerance for external API calls
"""

import asyncio
import time
from enum import Enum
from typing import Callable, Any, Dict, Optional, Union
from dataclasses import dataclass
from functools import wraps
import logging

from exceptions import ExternalAPIError, SystemError


logger = logging.getLogger(__name__)


class CircuitState(Enum):
    """Circuit breaker states"""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"         # Failing, reject calls
    HALF_OPEN = "half_open"  # Testing if service recovered


@dataclass
class CircuitBreakerConfig:
    """Circuit breaker configuration"""
    failure_threshold: int = 5          # Failures before opening
    recovery_timeout: int = 60          # Seconds before trying half-open
    success_threshold: int = 3          # Successes needed to close from half-open
    timeout: int = 30                   # Request timeout in seconds
    expected_exception: type = Exception  # Exception type that counts as failure


class CircuitBreakerStats:
    """Circuit breaker statistics"""
    
    def __init__(self):
        self.failure_count = 0
        self.success_count = 0
        self.total_requests = 0
        self.last_failure_time = None
        self.state_changes = []
    
    def record_success(self):
        """Record a successful call"""
        self.success_count += 1
        self.total_requests += 1
    
    def record_failure(self):
        """Record a failed call"""
        self.failure_count += 1
        self.total_requests += 1
        self.last_failure_time = time.time()
    
    def record_state_change(self, old_state: CircuitState, new_state: CircuitState):
        """Record state transition"""
        self.state_changes.append({
            "timestamp": time.time(),
            "from_state": old_state.value,
            "to_state": new_state.value
        })
    
    def get_failure_rate(self) -> float:
        """Calculate failure rate"""
        if self.total_requests == 0:
            return 0.0
        return self.failure_count / self.total_requests
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert stats to dictionary"""
        return {
            "failure_count": self.failure_count,
            "success_count": self.success_count,
            "total_requests": self.total_requests,
            "failure_rate": self.get_failure_rate(),
            "last_failure_time": self.last_failure_time,
            "state_changes": self.state_changes[-10:]  # Last 10 state changes
        }


class CircuitBreaker:
    """Circuit breaker implementation"""
    
    def __init__(self, name: str, config: CircuitBreakerConfig):
        self.name = name
        self.config = config
        self.state = CircuitState.CLOSED
        self.stats = CircuitBreakerStats()
        self._lock = asyncio.Lock()
    
    async def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with circuit breaker protection"""
        async with self._lock:
            # Check if we should allow the call
            if not self._should_allow_request():
                raise SystemError(
                    message=f"Circuit breaker {self.name} is OPEN",
                    component=self.name,
                    error_code="CIRCUIT_BREAKER_OPEN",
                    details=self.stats.to_dict()
                )
        
        try:
            # Set timeout for the call
            if asyncio.iscoroutinefunction(func):
                result = await asyncio.wait_for(
                    func(*args, **kwargs),
                    timeout=self.config.timeout
                )
            else:
                result = func(*args, **kwargs)
            
            # Record success and potentially close circuit
            await self._on_success()
            return result
            
        except asyncio.TimeoutError:
            await self._on_failure()
            raise ExternalAPIError(
                service=self.name,
                message=f"Request timed out after {self.config.timeout} seconds",
                error_code="REQUEST_TIMEOUT"
            )
        except self.config.expected_exception as e:
            await self._on_failure()
            raise
        except Exception as e:
            # Unexpected exceptions don't count as failures
            logger.warning(f"Unexpected exception in circuit breaker {self.name}: {e}")
            raise
    
    def _should_allow_request(self) -> bool:
        """Check if request should be allowed based on current state"""
        if self.state == CircuitState.CLOSED:
            return True
        elif self.state == CircuitState.OPEN:
            # Check if we should transition to half-open
            if self._should_attempt_reset():
                self._transition_to_half_open()
                return True
            return False
        elif self.state == CircuitState.HALF_OPEN:
            return True
        return False
    
    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset"""
        if self.stats.last_failure_time is None:
            return True
        return (time.time() - self.stats.last_failure_time) >= self.config.recovery_timeout
    
    async def _on_success(self):
        """Handle successful call"""
        async with self._lock:
            self.stats.record_success()
            
            if self.state == CircuitState.HALF_OPEN:
                # Check if we have enough successes to close
                recent_successes = self._get_recent_success_count()
                if recent_successes >= self.config.success_threshold:
                    self._transition_to_closed()
    
    async def _on_failure(self):
        """Handle failed call"""
        async with self._lock:
            self.stats.record_failure()
            
            if self.state == CircuitState.CLOSED:
                # Check if we should open the circuit
                if self.stats.failure_count >= self.config.failure_threshold:
                    self._transition_to_open()
            elif self.state == CircuitState.HALF_OPEN:
                # Go back to open on any failure
                self._transition_to_open()
    
    def _get_recent_success_count(self) -> int:
        """Get count of recent successes (simplified - in production use time window)"""
        return self.stats.success_count
    
    def _transition_to_open(self):
        """Transition to OPEN state"""
        old_state = self.state
        self.state = CircuitState.OPEN
        self.stats.record_state_change(old_state, self.state)
        logger.warning(f"Circuit breaker {self.name} opened due to failures")
    
    def _transition_to_half_open(self):
        """Transition to HALF_OPEN state"""
        old_state = self.state
        self.state = CircuitState.HALF_OPEN
        self.stats.record_state_change(old_state, self.state)
        logger.info(f"Circuit breaker {self.name} transitioning to half-open")
    
    def _transition_to_closed(self):
        """Transition to CLOSED state"""
        old_state = self.state
        self.state = CircuitState.CLOSED
        # Reset failure count when closing
        self.stats.failure_count = 0
        self.stats.record_state_change(old_state, self.state)
        logger.info(f"Circuit breaker {self.name} closed - service recovered")
    
    def get_state(self) -> CircuitState:
        """Get current circuit state"""
        return self.state
    
    def get_stats(self) -> Dict[str, Any]:
        """Get circuit breaker statistics"""
        return {
            "name": self.name,
            "state": self.state.value,
            "config": {
                "failure_threshold": self.config.failure_threshold,
                "recovery_timeout": self.config.recovery_timeout,
                "success_threshold": self.config.success_threshold,
                "timeout": self.config.timeout
            },
            "stats": self.stats.to_dict()
        }
    
    def reset(self):
        """Manually reset circuit breaker"""
        self.state = CircuitState.CLOSED
        self.stats = CircuitBreakerStats()
        logger.info(f"Circuit breaker {self.name} manually reset")


class CircuitBreakerManager:
    """Manages multiple circuit breakers"""
    
    def __init__(self):
        self.breakers: Dict[str, CircuitBreaker] = {}
        self.default_configs = {
            "youtube_api": CircuitBreakerConfig(
                failure_threshold=5,
                recovery_timeout=60,
                success_threshold=3,
                timeout=30,
                expected_exception=ExternalAPIError
            ),
            "openai_api": CircuitBreakerConfig(
                failure_threshold=3,
                recovery_timeout=30,
                success_threshold=2,
                timeout=60,
                expected_exception=ExternalAPIError
            ),
            "google_ai_api": CircuitBreakerConfig(
                failure_threshold=3,
                recovery_timeout=30,
                success_threshold=2,
                timeout=45,
                expected_exception=ExternalAPIError
            ),
            "database": CircuitBreakerConfig(
                failure_threshold=10,
                recovery_timeout=10,
                success_threshold=5,
                timeout=5,
                expected_exception=Exception
            ),
            "redis": CircuitBreakerConfig(
                failure_threshold=5,
                recovery_timeout=15,
                success_threshold=3,
                timeout=5,
                expected_exception=Exception
            )
        }
    
    def get_breaker(self, name: str, config: Optional[CircuitBreakerConfig] = None) -> CircuitBreaker:
        """Get or create circuit breaker"""
        if name not in self.breakers:
            breaker_config = config or self.default_configs.get(name, CircuitBreakerConfig())
            self.breakers[name] = CircuitBreaker(name, breaker_config)
        return self.breakers[name]
    
    def get_all_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get statistics for all circuit breakers"""
        return {name: breaker.get_stats() for name, breaker in self.breakers.items()}
    
    def reset_all(self):
        """Reset all circuit breakers"""
        for breaker in self.breakers.values():
            breaker.reset()
    
    def reset_breaker(self, name: str):
        """Reset specific circuit breaker"""
        if name in self.breakers:
            self.breakers[name].reset()


# Global circuit breaker manager
_circuit_breaker_manager = CircuitBreakerManager()


def get_circuit_breaker_manager() -> CircuitBreakerManager:
    """Get global circuit breaker manager"""
    return _circuit_breaker_manager


def circuit_breaker(name: str, config: Optional[CircuitBreakerConfig] = None):
    """Decorator for applying circuit breaker to functions"""
    def decorator(func: Callable):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            breaker = get_circuit_breaker_manager().get_breaker(name, config)
            return await breaker.call(func, *args, **kwargs)
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            breaker = get_circuit_breaker_manager().get_breaker(name, config)
            # Convert sync call to async for circuit breaker
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(breaker.call(func, *args, **kwargs))
            finally:
                loop.close()
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator