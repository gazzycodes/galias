"""ImprovMX API wrapper for GALIAS CLI."""

import requests
from typing import Dict, List, Any
from requests.auth import HTTPBasicAuth

from config import IMPROVMX_API_KEY, DOMAIN, API_URL, MAX_ALIASES


class APIError(Exception):
    """Base exception for API-related errors."""
    pass


class AuthenticationError(APIError):
    """Raised when API authentication fails."""
    pass


class AliasExistsError(APIError):
    """Raised when trying to create an alias that already exists."""
    pass


class AliasNotFoundError(APIError):
    """Raised when trying to delete a non-existent alias."""
    pass


class LimitReachedError(APIError):
    """Raised when the alias limit is reached."""
    pass


class NetworkError(APIError):
    """Raised when network/connection issues occur."""
    pass


class ImprovMXAPI:
    """Wrapper for ImprovMX API operations."""

    def __init__(self):
        """Initialize API client with configuration."""
        self.auth = HTTPBasicAuth("api", IMPROVMX_API_KEY)
        self.session = requests.Session()
        self.session.auth = self.auth
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "GALIAS-CLI/1.0"
        })
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request with error handling."""
        url = f"{API_URL}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.request(method, url, **kwargs)
            
            # Handle specific HTTP status codes
            if response.status_code == 401:
                raise AuthenticationError(
                    "Invalid API key. Please check your IMPROVMX_API_KEY in .env file."
                )
            elif response.status_code == 404:
                raise AliasNotFoundError("Alias not found.")
            elif response.status_code == 409:
                raise AliasExistsError("Alias already exists.")
            elif response.status_code == 400:
                # Check if it's a limit error
                try:
                    error_data = response.json()
                    if "limit" in error_data.get("message", "").lower():
                        raise LimitReachedError(
                            f"Alias limit reached ({MAX_ALIASES} aliases max)."
                        )
                except ValueError:
                    pass
                raise APIError(f"Bad request: {response.text}")
            elif not response.ok:
                raise APIError(f"API error ({response.status_code}): {response.text}")
            
            return response.json()
            
        except requests.exceptions.ConnectionError:
            raise NetworkError("Network connection error. Please check your internet connection.")
        except requests.exceptions.Timeout:
            raise NetworkError("Request timeout. Please try again.")
        except requests.exceptions.JSONDecodeError as e:
            raise APIError(f"Invalid JSON response: {e}")
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Network error: {e}")
        except ValueError as e:
            raise APIError(f"Invalid JSON response: {e}")
    
    def list_aliases(self) -> Dict[str, Any]:
        """
        Get list of all aliases for the configured domain.
        
        Returns:
            Dict containing aliases data and metadata
        """
        return self._make_request("GET", "aliases")
    
    def add_alias(self, alias: str, forward: str) -> Dict[str, Any]:
        """
        Create a new alias.
        
        Args:
            alias: The alias name (without domain)
            forward: Email address to forward to
            
        Returns:
            Dict containing the created alias data
        """
        data = {
            "alias": alias,
            "forward": forward
        }
        return self._make_request("POST", "aliases", json=data)
    
    def delete_alias(self, alias: str) -> Dict[str, Any]:
        """
        Delete an existing alias.
        
        Args:
            alias: The alias name to delete
            
        Returns:
            Dict containing deletion confirmation
        """
        return self._make_request("DELETE", f"aliases/{alias}")
    
    def get_alias_count(self) -> int:
        """
        Get the current number of aliases.
        
        Returns:
            Number of active aliases
        """
        data = self.list_aliases()
        aliases = data.get("aliases", [])
        return len(aliases)


# Global API instance
_api_instance = None


def get_api() -> ImprovMXAPI:
    """Get the global API instance."""
    global _api_instance
    if _api_instance is None:
        _api_instance = ImprovMXAPI()
    return _api_instance
