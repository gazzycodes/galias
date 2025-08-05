"""Integration tests for GALIAS CLI."""

import pytest
import os
import tempfile
from pathlib import Path
from unittest.mock import patch
from typer.testing import CliRunner


class TestCLIIntegration:
    """Integration tests for CLI commands."""

    def setup_method(self):
        """Set up test environment."""
        self.runner = CliRunner()

        # Reset global state
        import api
        api._api_instance = None
    
    def teardown_method(self):
        """Clean up test environment."""
        pass
    
    @patch('config.IMPROVMX_API_KEY', 'sk_test_key_123')
    @patch('config.DOMAIN', 'test.com')
    @patch('config.API_URL', 'https://api.improvmx.com/v3/domains/test.com')
    @patch('config.MAX_ALIASES', 25)
    @patch('api.ImprovMXAPI._make_request')
    def test_list_command_success(self, mock_request, mock_max_aliases, mock_api_url, mock_domain, mock_api_key):
        """Test successful list command."""
        from cli import app

        mock_response = {
            "aliases": [
                {"alias": "test", "forward": "test@example.com", "active": True}
            ]
        }
        mock_request.return_value = mock_response

        result = self.runner.invoke(app, ["list", "--quiet"])

        assert result.exit_code == 0
        assert "test" in result.stdout
        assert "test@example.com" in result.stdout
    
    @patch('api.ImprovMXAPI._make_request')
    def test_list_command_json(self, mock_request):
        """Test list command with JSON output."""
        mock_response = {
            "aliases": [
                {"alias": "test", "forward": "test@example.com", "active": True}
            ]
        }
        mock_request.return_value = mock_response

        result = self.runner.invoke(app, ["list", "--json", "--no-color"])

        assert result.exit_code == 0
        assert '"alias": "test"' in result.stdout
        assert '"forward": "test@example.com"' in result.stdout
    
    @patch('api.ImprovMXAPI._make_request')
    def test_add_command_success(self, mock_request):
        """Test successful add command."""
        # Mock both the add request and the count request
        mock_request.side_effect = [
            {"alias": "new", "forward": "new@example.com", "active": True},  # add response
            {"aliases": [{"alias": "new", "forward": "new@example.com"}]}     # count response
        ]
        
        result = self.runner.invoke(app, ["add", "new", "new@example.com", "--quiet"])
        
        assert result.exit_code == 0
        assert "Added alias: new → new@example.com" in result.stdout
    
    @patch('api.ImprovMXAPI._make_request')
    def test_delete_command_success(self, mock_request):
        """Test successful delete command."""
        # Mock both the delete request and the count request
        mock_request.side_effect = [
            {"message": "Alias deleted"},  # delete response
            {"aliases": []}                # count response
        ]
        
        result = self.runner.invoke(app, ["delete", "test", "--force", "--quiet"])
        
        assert result.exit_code == 0
        assert "Deleted alias: test" in result.stdout
    
    @patch('api.ImprovMXAPI._make_request')
    def test_status_command_success(self, mock_request):
        """Test successful status command."""
        mock_request.return_value = {
            "aliases": [
                {"alias": "test1", "forward": "test1@example.com"},
                {"alias": "test2", "forward": "test2@example.com"}
            ]
        }
        
        result = self.runner.invoke(app, ["status"])
        
        assert result.exit_code == 0
        assert "2/25 aliases" in result.stdout
    
    @patch('api.ImprovMXAPI._make_request')
    def test_status_command_json(self, mock_request):
        """Test status command with JSON output."""
        mock_request.return_value = {
            "aliases": [
                {"alias": "test1", "forward": "test1@example.com"},
                {"alias": "test2", "forward": "test2@example.com"}
            ]
        }

        result = self.runner.invoke(app, ["status", "--json", "--no-color"])

        assert result.exit_code == 0
        assert '"current_aliases": 2' in result.stdout
        assert '"max_aliases": 25' in result.stdout
        assert '"domain": "test.com"' in result.stdout
    
    def test_version_flag(self):
        """Test version flag."""
        result = self.runner.invoke(app, ["--version"])
        
        assert result.exit_code == 0
        assert "GALIAS v1.0.0" in result.stdout
    
    def test_help_command(self):
        """Test help command."""
        result = self.runner.invoke(app, ["--help"])
        
        assert result.exit_code == 0
        assert "GALIAS - Terminal-based ImprovMX alias manager" in result.stdout
    
    @patch('api.ImprovMXAPI._make_request')
    def test_add_command_validation_error(self, mock_request):
        """Test add command with validation error."""
        result = self.runner.invoke(app, ["add", "test", "invalid-email", "--quiet"])
        
        assert result.exit_code == 1
        assert "Invalid email format" in result.stdout
    
    @patch('api.ImprovMXAPI._make_request')
    def test_add_command_missing_args(self, mock_request):
        """Test add command with missing arguments."""
        # Simulate user canceling interactive input
        result = self.runner.invoke(app, ["add", "--quiet"], input="\n\n")
        
        assert result.exit_code == 1
        assert "required" in result.stdout.lower()


class TestCLIErrorHandling:
    """Test CLI error handling scenarios."""
    
    def setup_method(self):
        """Set up test environment."""
        self.runner = CliRunner()

        # Create temporary directory without .env file
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)

        # Reset global state
        import api
        api._api_instance = None
    
    def teardown_method(self):
        """Clean up test environment."""
        os.chdir(self.original_cwd)
        import shutil
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)
    
    def test_missing_env_file(self):
        """Test behavior when .env file is missing."""
        result = self.runner.invoke(app, ["list"])
        
        assert result.exit_code == 1
        assert "No .env file found" in result.stdout
    
    def test_config_error_handling(self):
        """Test configuration error handling."""
        # Create .env file with invalid API key format to trigger validation error
        env_file = Path(self.temp_dir) / ".env"
        env_file.write_text("IMPROVMX_API_KEY=invalid_key_format\nDOMAIN=test.com")

        result = self.runner.invoke(app, ["list"])

        assert result.exit_code == 1
        # Either configuration error or authentication error is acceptable
        # since both indicate the API key is invalid
        assert any(msg in result.stdout for msg in [
            "Configuration error",
            "Invalid API key format",
            "Authentication failed"
        ])


if __name__ == '__main__':
    pytest.main([__file__])
