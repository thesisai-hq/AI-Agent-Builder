"""In-memory cache for stock data with TTL and comprehensive management.

Reduces API calls to yfinance and improves response time.
Supports multiple cache instances for different data types.
"""

import logging
from typing import Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from threading import Lock
from .constants import STOCK_DATA_CACHE_TTL_SECONDS, PRICE_HISTORY_CACHE_TTL_SECONDS

logger = logging.getLogger(__name__)


class DataCache:
    """Thread-safe in-memory cache with time-to-live."""
    
    def __init__(self, ttl_seconds: int = 300):
        """Initialize cache.
        
        Args:
            ttl_seconds: Time to live in seconds (default 5 minutes)
        """
        self.cache: Dict[str, Tuple[Any, datetime]] = {}
        self.ttl = timedelta(seconds=ttl_seconds)
        self.lock = Lock()
    
    def get(self, key: str) -> Optional[Any]:
        """Get cached data if available and not expired.
        
        Args:
            key: Cache key (typically ticker symbol)
            
        Returns:
            Cached data or None if not found/expired
        """
        with self.lock:
            if key not in self.cache:
                return None
            
            data, timestamp = self.cache[key]
            
            # Check if expired
            if datetime.now() - timestamp > self.ttl:
                del self.cache[key]
                return None
            
            return data
    
    def set(self, key: str, data: Any) -> None:
        """Store data in cache.
        
        Args:
            key: Cache key
            data: Data to cache
        """
        with self.lock:
            self.cache[key] = (data, datetime.now())
    
    def invalidate(self, key: str) -> bool:
        """Remove specific key from cache.
        
        Args:
            key: Cache key to remove
            
        Returns:
            True if key was removed, False if not found
        """
        with self.lock:
            if key in self.cache:
                del self.cache[key]
                return True
            return False
    
    def clear(self, key: Optional[str] = None) -> None:
        """Clear cache.
        
        Args:
            key: Specific key to clear, or None to clear all
        """
        with self.lock:
            if key:
                self.cache.pop(key, None)
            else:
                self.cache.clear()
    
    def clear_prefix(self, prefix: str) -> int:
        """Clear all keys starting with prefix.
        
        Args:
            prefix: Key prefix to match
            
        Returns:
            Number of entries removed
        """
        with self.lock:
            keys_to_remove = [k for k in self.cache.keys() if k.startswith(prefix)]
            for key in keys_to_remove:
                del self.cache[key]
            return len(keys_to_remove)
    
    def size(self) -> int:
        """Get number of cached items."""
        with self.lock:
            return len(self.cache)
    
    def cleanup_expired(self) -> int:
        """Remove all expired entries.
        
        Returns:
            Number of entries removed
        """
        with self.lock:
            now = datetime.now()
            expired_keys = [
                key for key, (_, timestamp) in self.cache.items()
                if now - timestamp > self.ttl
            ]
            
            for key in expired_keys:
                del self.cache[key]
            
            return len(expired_keys)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics.
        
        Returns:
            Cache statistics
        """
        with self.lock:
            now = datetime.now()
            valid_entries = sum(
                1 for _, timestamp in self.cache.values()
                if now - timestamp <= self.ttl
            )
            
            return {
                "total_entries": len(self.cache),
                "valid_entries": valid_entries,
                "expired_entries": len(self.cache) - valid_entries,
                "ttl_seconds": self.ttl.total_seconds()
            }


# Global cache instances
# Stock fundamental data: 5 minute TTL
data_cache = DataCache(ttl_seconds=STOCK_DATA_CACHE_TTL_SECONDS)

# Price history data: 1 minute TTL (more frequent for technical analysis)
price_history_cache = DataCache(ttl_seconds=PRICE_HISTORY_CACHE_TTL_SECONDS)
