"""Basic functionality tests that don't require complex configuration mocking."""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch
from typer.testing import CliRunner


def test_cli_with_missing_env():
    """Test that CLI shows proper error when .env is missing."""
    # Create a temporary directory without .env
    with tempfile.TemporaryDirectory() as temp_dir:
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            
            # Test the main entry point
            from subprocess import run, PIPE
            result = run(['python', '-c', 'import improvctl'], 
                        capture_output=True, text=True, cwd=original_cwd)
            
            assert result.returncode == 1
            assert "Missing IMPROVMX_API_KEY" in result.stdout
            
        finally:
            os.chdir(original_cwd)


def test_cli_with_valid_env():
    """Test that CLI loads successfully with valid .env."""
    # Create a temporary directory with valid .env
    with tempfile.TemporaryDirectory() as temp_dir:
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            
            # Create valid .env file
            env_file = Path(temp_dir) / ".env"
            env_file.write_text("IMPROVMX_API_KEY=sk_test_key\nDOMAIN=test.com")
            
            # Test the main entry point
            from subprocess import run, PIPE
            result = run(['python', '-c', 'import improvctl; print("SUCCESS")'], 
                        capture_output=True, text=True, cwd=original_cwd)
            
            assert result.returncode == 0
            assert "SUCCESS" in result.stdout
            
        finally:
            os.chdir(original_cwd)


def test_version_command():
    """Test version command with valid config."""
    with tempfile.TemporaryDirectory() as temp_dir:
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            
            # Create valid .env file
            env_file = Path(temp_dir) / ".env"
            env_file.write_text("IMPROVMX_API_KEY=sk_test_key\nDOMAIN=test.com")
            
            # Test version command
            from subprocess import run, PIPE
            result = run(['python', f'{original_cwd}/improvctl.py', '--version'], 
                        capture_output=True, text=True)
            
            assert result.returncode == 0
            assert "GALIAS v1.0.0" in result.stdout
            assert "ImprovMX Alias Manager" in result.stdout
            
        finally:
            os.chdir(original_cwd)


if __name__ == '__main__':
    pytest.main([__file__])
