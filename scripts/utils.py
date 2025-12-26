#!/usr/bin/env python3
"""
Shared utilities for DriftingMe generators
Input validation, HTTP session management, and common functions
"""

import re
import logging
import time
from typing import Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


def validate_prompt_key(key: str) -> bool:
    """Validate prompt key format - alphanumeric and underscores only"""
    if not isinstance(key, str):
        return False
    return bool(re.match(r'^[a-z0-9_]+$', key))


def validate_seed(seed: Optional[int]) -> Optional[int]:
    """Validate seed range"""
    if seed is None:
        return None
    
    if not isinstance(seed, int):
        raise ValueError(f"Seed must be integer, got {type(seed).__name__}")
    
    if seed < -1 or seed > 2**32 - 1:
        raise ValueError(f"Seed must be -1 or 0 to {2**32-1}, got {seed}")
    
    return seed


def validate_dimensions(width: int, height: int) -> tuple:
    """Validate image dimensions"""
    if not isinstance(width, int) or not isinstance(height, int):
        raise ValueError("Width and height must be integers")
    
    if width < 64 or width > 4096:
        raise ValueError(f"Width must be between 64 and 4096, got {width}")
    
    if height < 64 or height > 4096:
        raise ValueError(f"Height must be between 64 and 4096, got {height}")
    
    # Check total pixels to prevent memory issues
    if width * height > 25_000_000:  # 25 megapixels
        raise ValueError(f"Image dimensions too large: {width}x{height} exceeds 25MP")
    
    return width, height


def create_resilient_session(max_retries: int = 3) -> requests.Session:
    """
    Create HTTP session with automatic retries and connection pooling
    
    Args:
        max_retries: Maximum number of retry attempts
        
    Returns:
        Configured requests.Session object
    """
    session = requests.Session()
    
    retry_strategy = Retry(
        total=max_retries,
        backoff_factor=2,  # 2, 4, 8 seconds between retries
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "POST"],
        raise_on_status=False
    )
    
    adapter = HTTPAdapter(
        max_retries=retry_strategy,
        pool_connections=5,
        pool_maxsize=10
    )
    
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session


class RateLimiter:
    """Simple rate limiter to prevent API abuse"""
    
    def __init__(self, max_calls: int, period: int):
        """
        Args:
            max_calls: Maximum number of calls allowed
            period: Time period in seconds
        """
        self.max_calls = max_calls
        self.period = period
        self.calls = []
    
    def wait_if_needed(self):
        """Wait if rate limit would be exceeded"""
        now = time.time()
        
        # Remove old calls outside the time window
        self.calls = [call_time for call_time in self.calls 
                     if call_time > now - self.period]
        
        # If at limit, wait for the oldest call to expire
        if len(self.calls) >= self.max_calls:
            sleep_time = self.calls[0] + self.period - now
            if sleep_time > 0:
                logger.info(f"Rate limit reached, waiting {sleep_time:.1f}s")
                time.sleep(sleep_time)
                # Recursive call after waiting
                return self.wait_if_needed()
        
        # Record this call
        self.calls.append(now)


# Global rate limiter - 10 requests per minute
api_rate_limiter = RateLimiter(max_calls=10, period=60)


def safe_api_call(session: requests.Session, url: str, payload: dict, 
                  timeout: tuple = (10, 300)) -> requests.Response:
    """
    Make a safe API call with rate limiting and proper timeout
    
    Args:
        session: requests.Session object
        url: API endpoint URL
        payload: Request payload
        timeout: (connect_timeout, read_timeout) in seconds
        
    Returns:
        Response object
        
    Raises:
        requests.exceptions.RequestException on failure
    """
    # Apply rate limiting
    api_rate_limiter.wait_if_needed()
    
    # Make request
    response = session.post(url, json=payload, timeout=timeout)
    
    return response
