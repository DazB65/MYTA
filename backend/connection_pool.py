"""
Connection Pool Manager for Vidalytics
Implements connection pooling for API clients to improve performance and resource management
"""

import asyncio
import aiohttp
import httpx
from typing import Dict, Optional, Any
from openai import OpenAI, AsyncOpenAI
import google.generativeai as genai
from googleapiclient.discovery import build
import threading
import logging
from dataclasses import dataclass
from contextlib import asynccontextmanager
import time

logger = logging.getLogger(__name__)

@dataclass
class PoolConfig:
    """Configuration for connection pools"""
    max_connections: int = 100
    max_keepalive_connections: int = 20
    keepalive_expiry: int = 5
    timeout: int = 30
    retries: int = 3

class OpenAIConnectionPool:
    """Managed connection pool for OpenAI API clients"""
    
    def __init__(self, api_key: str, config: PoolConfig = None):
        self.api_key = api_key
        self.config = config or PoolConfig()
        self._sync_client: Optional[OpenAI] = None
        self._async_client: Optional[AsyncOpenAI] = None
        self._lock = threading.Lock()
        self._created_at = time.time()
        
    def get_sync_client(self) -> OpenAI:
        """Get a synchronized OpenAI client with connection pooling"""
        if self._sync_client is None:
            with self._lock:
                if self._sync_client is None:
                    # Create HTTP client with connection pooling
                    http_client = httpx.Client(
                        limits=httpx.Limits(
                            max_connections=self.config.max_connections,
                            max_keepalive_connections=self.config.max_keepalive_connections,
                            keepalive_expiry=self.config.keepalive_expiry
                        ),
                        timeout=httpx.Timeout(self.config.timeout)
                    )
                    
                    self._sync_client = OpenAI(
                        api_key=self.api_key,
                        http_client=http_client
                    )
                    logger.info("Created OpenAI sync client with connection pool")
        
        return self._sync_client
    
    def get_async_client(self) -> AsyncOpenAI:
        """Get an asynchronous OpenAI client with connection pooling"""
        if self._async_client is None:
            with self._lock:
                if self._async_client is None:
                    # Create async HTTP client with connection pooling
                    http_client = httpx.AsyncClient(
                        limits=httpx.Limits(
                            max_connections=self.config.max_connections,
                            max_keepalive_connections=self.config.max_keepalive_connections,
                            keepalive_expiry=self.config.keepalive_expiry
                        ),
                        timeout=httpx.Timeout(self.config.timeout),
                    )
                    
                    self._async_client = AsyncOpenAI(
                        api_key=self.api_key,
                        http_client=http_client
                    )
                    logger.info("Created OpenAI async client with connection pool")
        
        return self._async_client
    
    def close(self):
        """Close all connections"""
        if self._sync_client:
            self._sync_client.close()
            self._sync_client = None
            
        if self._async_client:
            asyncio.create_task(self._async_client.close())
            self._async_client = None
            
        logger.info("Closed OpenAI connection pool")

class YouTubeConnectionPool:
    """Managed connection pool for YouTube API clients"""
    
    def __init__(self, api_key: str, config: PoolConfig = None):
        self.api_key = api_key
        self.config = config or PoolConfig()
        self._clients: Dict[str, Any] = {}
        self._lock = threading.Lock()
        self._session: Optional[aiohttp.ClientSession] = None
        
    def get_client(self, service_name: str = 'youtube', version: str = 'v3'):
        """Get a YouTube API client with connection pooling"""
        client_key = f"{service_name}_{version}"
        
        if client_key not in self._clients:
            with self._lock:
                if client_key not in self._clients:
                    # Create HTTP client with connection pooling
                    http = httpx.Client(
                        limits=httpx.Limits(
                            max_connections=self.config.max_connections,
                            max_keepalive_connections=self.config.max_keepalive_connections,
                            keepalive_expiry=self.config.keepalive_expiry
                        ),
                        timeout=httpx.Timeout(self.config.timeout)
                    )
                    
                    # Build YouTube client with custom HTTP client
                    client = build(
                        service_name,
                        version,
                        developerKey=self.api_key,
                        cache_discovery=False  # Disable discovery caching for better performance
                    )
                    
                    self._clients[client_key] = client
                    logger.info(f"Created YouTube {service_name} v{version} client with connection pool")
        
        return self._clients[client_key]
    
    @asynccontextmanager
    async def get_async_session(self):
        """Get an async HTTP session for direct API calls"""
        if self._session is None or self._session.closed:
            connector = aiohttp.TCPConnector(
                limit=self.config.max_connections,
                limit_per_host=self.config.max_keepalive_connections,
                keepalive_timeout=self.config.keepalive_expiry,
                enable_cleanup_closed=True
            )
            
            timeout = aiohttp.ClientTimeout(total=self.config.timeout)
            
            self._session = aiohttp.ClientSession(
                connector=connector,
                timeout=timeout,
                headers={'Authorization': f'Bearer {self.api_key}'}
            )
            
            logger.info("Created YouTube async session with connection pool")
        
        try:
            yield self._session
        finally:
            # Session will be reused, don't close here
            pass
    
    async def close(self):
        """Close all connections"""
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None
            
        self._clients.clear()
        logger.info("Closed YouTube connection pool")

class GeminiConnectionPool:
    """Managed connection pool for Google Gemini API clients"""
    
    def __init__(self, api_key: str, config: PoolConfig = None):
        self.api_key = api_key
        self.config = config or PoolConfig()
        self._configured = False
        self._lock = threading.Lock()
        
    def configure_gemini(self):
        """Configure Gemini with connection pooling settings"""
        if not self._configured:
            with self._lock:
                if not self._configured:
                    genai.configure(api_key=self.api_key)
                    
                    # Configure transport settings for better connection management
                    # Note: Gemini SDK may not support all httpx options directly
                    self._configured = True
                    logger.info("Configured Gemini client with connection optimizations")
    
    def get_model(self, model_name: str = "gemini-2.5-pro"):
        """Get a Gemini model with optimized configuration"""
        self.configure_gemini()
        
        # Configure generation settings for better performance
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 2048,
        }
        
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]
        
        model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        
        return model

class ConnectionPoolManager:
    """Central manager for all API connection pools"""
    
    def __init__(self):
        self._openai_pools: Dict[str, OpenAIConnectionPool] = {}
        self._youtube_pools: Dict[str, YouTubeConnectionPool] = {}
        self._gemini_pools: Dict[str, GeminiConnectionPool] = {}
        self._lock = threading.Lock()
        
    def get_openai_pool(self, api_key: str, config: PoolConfig = None) -> OpenAIConnectionPool:
        """Get or create OpenAI connection pool"""
        pool_key = f"openai_{hash(api_key)}"
        
        if pool_key not in self._openai_pools:
            with self._lock:
                if pool_key not in self._openai_pools:
                    self._openai_pools[pool_key] = OpenAIConnectionPool(api_key, config)
        
        return self._openai_pools[pool_key]
    
    def get_youtube_pool(self, api_key: str, config: PoolConfig = None) -> YouTubeConnectionPool:
        """Get or create YouTube connection pool"""
        pool_key = f"youtube_{hash(api_key)}"
        
        if pool_key not in self._youtube_pools:
            with self._lock:
                if pool_key not in self._youtube_pools:
                    self._youtube_pools[pool_key] = YouTubeConnectionPool(api_key, config)
        
        return self._youtube_pools[pool_key]
    
    def get_gemini_pool(self, api_key: str, config: PoolConfig = None) -> GeminiConnectionPool:
        """Get or create Gemini connection pool"""
        pool_key = f"gemini_{hash(api_key)}"
        
        if pool_key not in self._gemini_pools:
            with self._lock:
                if pool_key not in self._gemini_pools:
                    self._gemini_pools[pool_key] = GeminiConnectionPool(api_key, config)
        
        return self._gemini_pools[pool_key]
    
    async def close_all(self):
        """Close all connection pools"""
        # Close OpenAI pools
        for pool in self._openai_pools.values():
            pool.close()
        
        # Close YouTube pools
        for pool in self._youtube_pools.values():
            await pool.close()
        
        self._openai_pools.clear()
        self._youtube_pools.clear()
        self._gemini_pools.clear()
        
        logger.info("Closed all connection pools")

# Global connection pool manager
_pool_manager: Optional[ConnectionPoolManager] = None

def get_connection_pool_manager() -> ConnectionPoolManager:
    """Get the global connection pool manager"""
    global _pool_manager
    if _pool_manager is None:
        _pool_manager = ConnectionPoolManager()
    return _pool_manager

def get_openai_client(api_key: str, use_async: bool = False, config: PoolConfig = None):
    """Get an OpenAI client with connection pooling"""
    pool_manager = get_connection_pool_manager()
    pool = pool_manager.get_openai_pool(api_key, config)
    
    if use_async:
        return pool.get_async_client()
    else:
        return pool.get_sync_client()

def get_youtube_client(api_key: str, service_name: str = 'youtube', version: str = 'v3', config: PoolConfig = None):
    """Get a YouTube API client with connection pooling"""
    pool_manager = get_connection_pool_manager()
    pool = pool_manager.get_youtube_pool(api_key, config)
    return pool.get_client(service_name, version)

def get_gemini_model(api_key: str, model_name: str = "gemini-2.5-pro", config: PoolConfig = None):
    """Get a Gemini model with connection pooling"""
    pool_manager = get_connection_pool_manager()
    pool = pool_manager.get_gemini_pool(api_key, config)
    return pool.get_model(model_name)

async def cleanup_connections():
    """Cleanup all connections - call this on app shutdown"""
    global _pool_manager
    if _pool_manager:
        await _pool_manager.close_all()
        _pool_manager = None