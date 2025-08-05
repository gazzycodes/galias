"""Configuration management for GALIAS CLI."""

from pathlib import Path
from dotenv import load_dotenv
import os, sys

# Load .env from current working directory
env_path = Path(".env")
load_dotenv(dotenv_path=env_path)

IMPROVMX_API_KEY = os.getenv("IMPROVMX_API_KEY")
DOMAIN           = os.getenv("DOMAIN")

if not IMPROVMX_API_KEY:
    print("X Missing IMPROVMX_API_KEY in .env - please add your sk_xxx key.")
    sys.exit(1)
if not DOMAIN:
    print("X Missing DOMAIN in .env - set yourdomain.com.")
    sys.exit(1)

# Optional configuration
IMPROVMX_API_BASE_URL = os.getenv("IMPROVMX_API_BASE_URL", "https://api.improvmx.com")
MAX_ALIASES = int(os.getenv("MAX_ALIASES", "25"))

# Validate API key format
if not IMPROVMX_API_KEY.startswith("sk_"):
    print("X Invalid API key format. ImprovMX API keys should start with 'sk_'")
    sys.exit(1)

# Validate domain format
if not DOMAIN or "." not in DOMAIN:
    print("X Invalid domain format. Please provide a valid domain name.")
    sys.exit(1)

# Derived configuration
API_URL = f"{IMPROVMX_API_BASE_URL}/v3/domains/{DOMAIN}"


class ConfigError(Exception):
    """Raised when configuration is invalid or missing."""
    pass
