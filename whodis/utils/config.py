"""Configuration constants for WHODIS."""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
CACHE_DIR = PROJECT_ROOT / "cache"
DATA_DIR = PROJECT_ROOT / "whodis" / "data"

# Ensure cache directory exists
CACHE_DIR.mkdir(exist_ok=True)

# Timeout settings
DEFAULT_TIMEOUT = 10
REQUEST_TIMEOUT = 15

# User agents for anti-bot
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1.1 Safari/605.1.15",
]

# Sources list
SOURCES_LIST = [
    "validator",
    "truecaller",
    "getcontact",
    "whatsapp",
    "telegram",
    "instagram",
    "facebook",
    "linkedin",
    "twitter",
    "breach",
    "virtual",
    "spam",
    "forum",
]

# Color codes
COLORS = {
    "RED": "\033[91m",
    "DARK_RED": "\033[31m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "BLUE": "\033[94m",
    "CYAN": "\033[96m",
    "WHITE": "\033[97m",
    "RESET": "\033[0m",
    "BOLD": "\033[1m",
}

# Emojis
EMOJIS = {
    "PHONE": "📞",
    "CHECK": "✅",
    "CROSS": "❌",
    "SEARCH": "🔍",
    "ROCKET": "🚀",
    "WAVE": "🌊",
    "CLOCK": "⏳",
    "BAR": "📊",
    "RADIO": "📡",
    "USER": "👤",
    "LINK": "🔗",
    "WARNING": "⚠️",
    "INFO": "ℹ️",
}

VERSION = "0.1"
