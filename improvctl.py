#!/usr/bin/env python3
"""
GALIAS - Terminal-based ImprovMX alias manager

A hacker-chic CLI tool for managing ImprovMX email aliases.
"""

import sys
import os
from pathlib import Path

# Add current directory to Python path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    # Import config first to validate environment
    import config
    from cli import app
    from ui import print_error, console
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure all required dependencies are installed:")
    print("pip install -r requirements.txt")
    sys.exit(1)


def main():
    """Main entry point for GALIAS CLI."""
    try:
        # Run the CLI app (config is already validated at import time)
        app()

    except KeyboardInterrupt:
        console.print("\n\nOperation cancelled by user", style="dim yellow")
        sys.exit(0)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        console.print("Please report this issue if it persists", style="dim")
        sys.exit(1)


if __name__ == "__main__":
    main()
