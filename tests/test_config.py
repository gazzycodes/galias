"""Tests for config module."""

import os
import pytest
from unittest.mock import patch
from pathlib import Path


class TestConfigValidation:
    """Test cases for configuration validation."""

    @patch('config.load_dotenv')
    @patch.dict(os.environ, {
        'IMPROVMX_API_KEY': 'sk_test_key_123',
        'DOMAIN': 'test.com'
    })
    def test_valid_config_loads(self, mock_load_dotenv):
        """Test that valid configuration loads without error."""
        # This test validates that importing config with valid env vars works
        import importlib
        import config
        importlib.reload(config)

        assert config.IMPROVMX_API_KEY == 'sk_test_key_123'
        assert config.DOMAIN == 'test.com'
        assert config.API_URL == 'https://api.improvmx.com/v3/domains/test.com'
        assert config.MAX_ALIASES == 25

    @patch('config.load_dotenv')
    @patch.dict(os.environ, {
        'IMPROVMX_API_KEY': 'sk_custom_key',
        'DOMAIN': 'custom.com',
        'IMPROVMX_API_BASE_URL': 'https://custom.api.com',
        'MAX_ALIASES': '50'
    })
    def test_custom_config_values(self, mock_load_dotenv):
        """Test configuration with custom values."""
        import importlib
        import config
        importlib.reload(config)

        assert config.IMPROVMX_API_BASE_URL == 'https://custom.api.com'
        assert config.MAX_ALIASES == 50
        assert config.API_URL == 'https://custom.api.com/v3/domains/custom.com'

    @patch('config.sys.exit')
    @patch('config.load_dotenv')
    @patch.dict(os.environ, {}, clear=True)
    def test_missing_api_key_exits(self, mock_load_dotenv, mock_exit):
        """Test that missing API key causes system exit."""
        import importlib
        import config
        importlib.reload(config)

        mock_exit.assert_called_with(1)

    @patch('config.sys.exit')
    @patch('config.load_dotenv')
    @patch.dict(os.environ, {
        'IMPROVMX_API_KEY': 'sk_test'
    }, clear=True)
    def test_missing_domain_exits(self, mock_load_dotenv, mock_exit):
        """Test that missing domain causes system exit."""
        import importlib
        import config
        importlib.reload(config)

        mock_exit.assert_called_with(1)

    @patch('config.sys.exit')
    @patch('config.load_dotenv')
    @patch.dict(os.environ, {
        'IMPROVMX_API_KEY': 'invalid_key',
        'DOMAIN': 'test.com'
    })
    def test_invalid_api_key_format_exits(self, mock_load_dotenv, mock_exit):
        """Test that invalid API key format causes system exit."""
        import importlib
        import config
        importlib.reload(config)

        mock_exit.assert_called_with(1)

    @patch('config.sys.exit')
    @patch('config.load_dotenv')
    @patch.dict(os.environ, {
        'IMPROVMX_API_KEY': 'sk_test',
        'DOMAIN': 'invalid'
    })
    def test_invalid_domain_format_exits(self, mock_load_dotenv, mock_exit):
        """Test that invalid domain format causes system exit."""
        import importlib
        import config
        importlib.reload(config)

        mock_exit.assert_called_with(1)


if __name__ == '__main__':
    pytest.main([__file__])
