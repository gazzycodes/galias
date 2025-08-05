"""Tests for UI module."""

import pytest
from unittest.mock import patch, MagicMock
from io import StringIO

from ui import (
    create_progress_bar, print_alias_count, print_aliases_table,
    print_success, print_error, print_warning, print_info,
    handle_error_display
)


class TestProgressBar:
    """Test cases for progress bar functionality."""
    
    def test_create_progress_bar_empty(self):
        """Test progress bar with zero current value."""
        bar = create_progress_bar(0, 25, 20)
        assert bar == "[--------------------]"
    
    def test_create_progress_bar_full(self):
        """Test progress bar with maximum value."""
        bar = create_progress_bar(25, 25, 20)
        assert bar == "[####################]"
    
    def test_create_progress_bar_half(self):
        """Test progress bar with half value."""
        bar = create_progress_bar(12, 25, 20)
        # 12/25 = 0.48, so 0.48 * 20 = 9.6 -> 9 filled
        assert bar == "[#########-----------]"
    
    def test_create_progress_bar_custom_width(self):
        """Test progress bar with custom width."""
        bar = create_progress_bar(5, 10, 10)
        assert bar == "[#####-----]"
        assert len(bar) == 12  # 10 chars + 2 brackets
    
    def test_create_progress_bar_zero_maximum(self):
        """Test progress bar with zero maximum."""
        bar = create_progress_bar(5, 0, 10)
        assert bar == "[----------]"


class TestPrintFunctions:
    """Test cases for print functions."""
    
    @patch('ui.console')
    def test_print_success(self, mock_console):
        """Test success message printing."""
        print_success("Operation completed")
        mock_console.print.assert_called_once_with("✓ Operation completed", style="bold green")
    
    @patch('ui.console')
    def test_print_error(self, mock_console):
        """Test error message printing."""
        print_error("Something went wrong")
        mock_console.print.assert_called_once_with("✗ Something went wrong", style="bold red")
    
    @patch('ui.console')
    def test_print_warning(self, mock_console):
        """Test warning message printing."""
        print_warning("Be careful")
        mock_console.print.assert_called_once_with("⚠️ Be careful", style="bold yellow")
    
    @patch('ui.console')
    def test_print_info(self, mock_console):
        """Test info message printing."""
        print_info("Here's some info")
        mock_console.print.assert_called_once_with("ℹ️ Here's some info", style="bold blue")


class TestAliasDisplay:
    """Test cases for alias display functions."""
    
    @patch('ui.console')
    @patch('ui.MAX_ALIASES', 25)
    def test_print_alias_count_normal(self, mock_console):
        """Test alias count display in normal range."""
        print_alias_count(10)

        # Should be called with green style for normal usage
        calls = mock_console.print.call_args_list
        assert len(calls) == 1
        assert "10/25 aliases" in calls[0][0][0]
        assert calls[0][1]['style'] == "bold green"

    @patch('ui.console')
    @patch('ui.MAX_ALIASES', 25)
    def test_print_alias_count_warning(self, mock_console):
        """Test alias count display in warning range."""
        print_alias_count(22)  # 88% usage, should trigger warning

        calls = mock_console.print.call_args_list
        assert len(calls) == 1
        assert "22/25 aliases" in calls[0][0][0]
        assert "3 slots left" in calls[0][0][0]
        assert calls[0][1]['style'] == "bold yellow"

    @patch('ui.console')
    @patch('ui.MAX_ALIASES', 25)
    def test_print_alias_count_limit_reached(self, mock_console):
        """Test alias count display at limit."""
        print_alias_count(25)

        calls = mock_console.print.call_args_list
        assert len(calls) == 1
        assert "25/25 aliases" in calls[0][0][0]
        assert "LIMIT REACHED" in calls[0][0][0]
        assert calls[0][1]['style'] == "bold red"
    
    @patch('ui.console')
    def test_print_aliases_table_empty(self, mock_console):
        """Test aliases table with no aliases."""
        aliases_data = {"aliases": []}
        
        print_aliases_table(aliases_data)
        
        mock_console.print.assert_called_with("No aliases found.", style="dim yellow")
    
    @patch('ui.console')
    def test_print_aliases_table_with_data(self, mock_console):
        """Test aliases table with alias data."""
        aliases_data = {
            "aliases": [
                {"alias": "test", "forward": "test@example.com", "active": True},
                {"alias": "info", "forward": "info@example.com", "active": False}
            ]
        }
        
        print_aliases_table(aliases_data)
        
        # Should print table and empty line
        assert mock_console.print.call_count == 2


class TestErrorHandling:
    """Test cases for error handling display."""
    
    @patch('ui.print_error')
    @patch('ui.console')
    def test_handle_authentication_error(self, mock_console, mock_print_error):
        """Test authentication error display."""
        from api import AuthenticationError
        
        error = AuthenticationError("Auth failed")
        handle_error_display(error)
        
        mock_print_error.assert_called_once_with("Authentication failed")
        mock_console.print.assert_called_with(
            "Please check your API key in the .env file", style="dim"
        )
    
    @patch('ui.print_error')
    @patch('ui.console')
    def test_handle_alias_exists_error(self, mock_console, mock_print_error):
        """Test alias exists error display."""
        from api import AliasExistsError
        
        error = AliasExistsError("Alias exists")
        handle_error_display(error)
        
        mock_print_error.assert_called_once_with("Alias already exists")
        mock_console.print.assert_called_with(
            "Choose a different alias name", style="dim"
        )
    
    @patch('ui.print_error')
    @patch('ui.console')
    def test_handle_alias_not_found_error(self, mock_console, mock_print_error):
        """Test alias not found error display."""
        from api import AliasNotFoundError
        
        error = AliasNotFoundError("Not found")
        handle_error_display(error)
        
        mock_print_error.assert_called_once_with("Alias not found")
        mock_console.print.assert_called_with(
            "Check the spelling and try again", style="dim"
        )
    
    @patch('ui.print_error')
    @patch('ui.console')
    def test_handle_limit_reached_error(self, mock_console, mock_print_error):
        """Test limit reached error display."""
        from api import LimitReachedError
        
        error = LimitReachedError("Limit reached")
        handle_error_display(error)
        
        mock_print_error.assert_called_once_with("Alias limit reached")
        mock_console.print.assert_called_with(
            "Delete some aliases before adding new ones", style="dim"
        )
    
    @patch('ui.print_error')
    @patch('ui.console')
    def test_handle_network_error(self, mock_console, mock_print_error):
        """Test network error display."""
        from api import NetworkError
        
        error = NetworkError("Network failed")
        handle_error_display(error)
        
        mock_print_error.assert_called_once_with("Network error")
        mock_console.print.assert_called_with(
            "Check your internet connection and try again", style="dim"
        )
    
    @patch('ui.print_error')
    def test_handle_generic_error(self, mock_print_error):
        """Test generic error display."""
        error = Exception("Generic error")
        handle_error_display(error)
        
        mock_print_error.assert_called_once_with("Error: Generic error")


if __name__ == '__main__':
    pytest.main([__file__])
