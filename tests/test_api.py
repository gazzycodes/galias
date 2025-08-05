"""Tests for API module."""

import pytest
import responses
from unittest.mock import patch, MagicMock

from api import (
    ImprovMXAPI, get_api, APIError, AuthenticationError,
    AliasExistsError, AliasNotFoundError, LimitReachedError, NetworkError
)


class TestImprovMXAPI:
    """Test cases for ImprovMXAPI class."""
    
    @patch('api.IMPROVMX_API_KEY', 'sk_test_key')
    @patch('api.DOMAIN', 'test.com')
    @patch('api.API_URL', 'https://api.improvmx.com/v3/domains/test.com')
    @patch('api.MAX_ALIASES', 25)
    def setup_method(self, method):
        """Set up test fixtures."""
        self.api = ImprovMXAPI()
    
    @responses.activate
    def test_list_aliases_success(self):
        """Test successful alias listing."""
        mock_response = {
            "aliases": [
                {"alias": "test", "forward": "test@example.com", "active": True}
            ]
        }
        
        responses.add(
            responses.GET,
            'https://api.improvmx.com/v3/domains/test.com/aliases',
            json=mock_response,
            status=200
        )
        
        result = self.api.list_aliases()
        assert result == mock_response
        assert len(responses.calls) == 1
    
    @responses.activate
    def test_add_alias_success(self):
        """Test successful alias creation."""
        mock_response = {
            "alias": "new",
            "forward": "new@example.com",
            "active": True
        }
        
        responses.add(
            responses.POST,
            'https://api.improvmx.com/v3/domains/test.com/aliases',
            json=mock_response,
            status=201
        )
        
        result = self.api.add_alias("new", "new@example.com")
        assert result == mock_response
        
        # Check request body
        request_body = responses.calls[0].request.body
        assert b'"alias": "new"' in request_body
        assert b'"forward": "new@example.com"' in request_body
    
    @responses.activate
    def test_delete_alias_success(self):
        """Test successful alias deletion."""
        mock_response = {"message": "Alias deleted successfully"}
        
        responses.add(
            responses.DELETE,
            'https://api.improvmx.com/v3/domains/test.com/aliases/test',
            json=mock_response,
            status=200
        )
        
        result = self.api.delete_alias("test")
        assert result == mock_response
    
    @responses.activate
    def test_authentication_error(self):
        """Test authentication error handling."""
        responses.add(
            responses.GET,
            'https://api.improvmx.com/v3/domains/test.com/aliases',
            status=401
        )
        
        with pytest.raises(AuthenticationError, match="Invalid API key"):
            self.api.list_aliases()
    
    @responses.activate
    def test_alias_not_found_error(self):
        """Test alias not found error handling."""
        responses.add(
            responses.DELETE,
            'https://api.improvmx.com/v3/domains/test.com/aliases/nonexistent',
            status=404
        )
        
        with pytest.raises(AliasNotFoundError, match="Alias not found"):
            self.api.delete_alias("nonexistent")
    
    @responses.activate
    def test_alias_exists_error(self):
        """Test alias already exists error handling."""
        responses.add(
            responses.POST,
            'https://api.improvmx.com/v3/domains/test.com/aliases',
            status=409
        )
        
        with pytest.raises(AliasExistsError, match="Alias already exists"):
            self.api.add_alias("existing", "test@example.com")
    
    @responses.activate
    def test_limit_reached_error(self):
        """Test limit reached error handling."""
        responses.add(
            responses.POST,
            'https://api.improvmx.com/v3/domains/test.com/aliases',
            json={"message": "Alias limit reached"},
            status=400
        )
        
        with pytest.raises(LimitReachedError, match="Alias limit reached"):
            self.api.add_alias("new", "test@example.com")
    
    @responses.activate
    def test_generic_400_error(self):
        """Test generic 400 error handling."""
        responses.add(
            responses.POST,
            'https://api.improvmx.com/v3/domains/test.com/aliases',
            json={"message": "Invalid request"},
            status=400
        )
        
        with pytest.raises(APIError, match="Bad request"):
            self.api.add_alias("new", "test@example.com")
    
    @responses.activate
    def test_network_error(self):
        """Test network error handling."""
        responses.add(
            responses.GET,
            'https://api.improvmx.com/v3/domains/test.com/aliases',
            body=responses.ConnectionError("Connection failed")
        )
        
        with pytest.raises(NetworkError, match="Network connection error"):
            self.api.list_aliases()
    
    @responses.activate
    def test_get_alias_count(self):
        """Test getting alias count."""
        mock_response = {
            "aliases": [
                {"alias": "test1", "forward": "test1@example.com"},
                {"alias": "test2", "forward": "test2@example.com"},
                {"alias": "test3", "forward": "test3@example.com"}
            ]
        }
        
        responses.add(
            responses.GET,
            'https://api.improvmx.com/v3/domains/test.com/aliases',
            json=mock_response,
            status=200
        )
        
        count = self.api.get_alias_count()
        assert count == 3
    
    @responses.activate
    def test_invalid_json_response(self):
        """Test handling of invalid JSON response."""
        responses.add(
            responses.GET,
            'https://api.improvmx.com/v3/domains/test.com/aliases',
            body="Invalid JSON",
            status=200
        )
        
        with pytest.raises(APIError, match="Invalid JSON response"):
            self.api.list_aliases()
    
    def test_request_headers(self):
        """Test that proper headers are set."""
        assert self.api.session.headers['Content-Type'] == 'application/json'
        assert self.api.session.headers['User-Agent'] == 'GALIAS-CLI/1.0'
        assert self.api.session.auth.username == 'api'
        assert self.api.session.auth.password == 'sk_test_key'


class TestGlobalAPI:
    """Test cases for global API functions."""
    
    @patch('api.ImprovMXAPI')
    def test_get_api_singleton(self, mock_api_class):
        """Test that get_api returns the same instance."""
        mock_instance = MagicMock()
        mock_api_class.return_value = mock_instance
        
        api1 = get_api()
        api2 = get_api()
        
        assert api1 is api2
        mock_api_class.assert_called_once()


if __name__ == '__main__':
    pytest.main([__file__])
