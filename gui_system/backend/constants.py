"""Constants used throughout the GUI backend.

Centralized location for all magic numbers and configuration constants.
"""

# Cache Configuration
STOCK_DATA_CACHE_TTL_SECONDS = 300  # 5 minutes
PRICE_HISTORY_CACHE_TTL_SECONDS = 60  # 1 minute
CACHE_CLEANUP_INTERVAL_SECONDS = 300  # 5 minutes

# Data Service Configuration
YFINANCE_TIMEOUT_SECONDS = 10  # Request timeout for yfinance API calls
YFINANCE_MAX_RETRIES = 3  # Number of retries for failed requests
YFINANCE_BACKOFF_FACTOR = 1  # Exponential backoff factor

# Validation Constants
MIN_MODEL_NAME_LENGTH = 3  # Minimum length for LLM model name
FLOAT_EQUALITY_THRESHOLD = 0.01  # Threshold for float equality comparison
MIN_TICKER_LENGTH = 1  # Minimum ticker symbol length
MAX_TICKER_LENGTH = 5  # Maximum ticker symbol length

# Analysis Constants
DEFAULT_CONFIDENCE = 0.5  # Default confidence for neutral signals
ERROR_CONFIDENCE = 0.0  # Confidence value for error signals
NEUTRAL_DIRECTION = 'neutral'  # Default signal direction

# Logging
DEFAULT_LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Health Check
HEALTH_CHECK_TIMEOUT_SECONDS = 5  # Timeout for individual health checks
