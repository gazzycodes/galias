"""UI components and styling for GALIAS CLI."""

from typing import List, Dict, Any, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich import box

from config import DOMAIN, MAX_ALIASES


# Global console instance
console = Console()


def print_banner():
    """Print the GALIAS ASCII banner."""
    banner = """
 ██████╗  █████╗ ██╗     ██╗ █████╗ ███████╗
██╔════╝ ██╔══██╗██║     ██║██╔══██╗██╔════╝
██║  ███╗███████║██║     ██║███████║███████╗
██║   ██║██╔══██║██║     ██║██╔══██║╚════██║
╚██████╔╝██║  ██║███████╗██║██║  ██║███████║
 ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝╚═╝  ╚═╝╚══════╝
"""

    # Print banner in cyan
    console.print(banner, style="bold cyan")
    console.print(f"ImprovMX Alias Manager @ {DOMAIN}", style="dim white", justify="center")
    console.print()


def create_progress_bar(current: int, maximum: int, width: int = 20) -> str:
    """
    Create a visual progress bar for alias count.
    
    Args:
        current: Current number of aliases
        maximum: Maximum number of aliases
        width: Width of the progress bar in characters
        
    Returns:
        Formatted progress bar string
    """
    if maximum <= 0:
        return "[" + "-" * width + "]"
    
    filled = int((current / maximum) * width)
    empty = width - filled
    
    bar = "#" * filled + "-" * empty
    return f"[{bar}]"


def print_alias_count(current: int, maximum: int = None):
    """
    Print the current alias count with a progress bar.

    Args:
        current: Current number of aliases
        maximum: Maximum number of aliases (defaults to config value)
    """
    if maximum is None:
        maximum = MAX_ALIASES
    
    progress_bar = create_progress_bar(current, maximum)
    count_text = f"{current}/{maximum} aliases"
    
    # Color coding based on usage
    if current >= maximum:
        style = "bold red"
        warning = " ⚠️ LIMIT REACHED"
    elif current >= maximum * 0.8:  # 80% or more
        style = "bold yellow"
        warning = f" ⚠️ {maximum - current} slots left"
    else:
        style = "bold green"
        warning = ""
    
    console.print(f"{progress_bar} {count_text}{warning}", style=style)


def print_aliases_table(aliases_data: Dict[str, Any]):
    """
    Print aliases in a formatted table.
    
    Args:
        aliases_data: Response from list_aliases API call
    """
    aliases = aliases_data.get("aliases", [])
    
    if not aliases:
        console.print("No aliases found.", style="dim yellow")
        return
    
    table = Table(title="Current Aliases", box=box.ROUNDED)
    table.add_column("Alias", style="cyan", no_wrap=True)
    table.add_column("Forward To", style="green")
    table.add_column("Status", style="yellow")
    
    for alias in aliases:
        alias_name = alias.get("alias", "")
        forward = alias.get("forward", "")
        active = alias.get("active", True)
        status = "✓ Active" if active else "✗ Inactive"
        
        table.add_row(alias_name, forward, status)
    
    console.print(table)
    console.print()


def print_success(message: str):
    """Print a success message."""
    console.print(f"✓ {message}", style="bold green")


def print_error(message: str):
    """Print an error message."""
    console.print(f"✗ {message}", style="bold red")


def print_warning(message: str):
    """Print a warning message."""
    console.print(f"⚠️ {message}", style="bold yellow")


def print_info(message: str):
    """Print an info message."""
    console.print(f"ℹ️ {message}", style="bold blue")


def prompt_alias() -> str:
    """Prompt user for alias name."""
    return Prompt.ask("❯ Enter new alias", console=console).strip()


def prompt_forward() -> str:
    """Prompt user for forward email address."""
    return Prompt.ask("❯ Forward to", console=console).strip()


def prompt_delete_alias() -> str:
    """Prompt user for alias to delete."""
    return Prompt.ask("❯ Alias to delete", console=console).strip()


def confirm_delete(alias: str) -> bool:
    """Confirm alias deletion."""
    return Confirm.ask(f"❯ Delete alias '{alias}'?", console=console, default=False)


def print_json_output(data: Dict[str, Any]):
    """Print raw JSON output for scripting."""
    import json
    console.print(json.dumps(data, indent=2))


def print_operation_summary(operation: str, alias: str, forward: str = None):
    """
    Print a summary of the completed operation.
    
    Args:
        operation: Type of operation (add, delete, list)
        alias: Alias name
        forward: Forward email (for add operations)
    """
    if operation == "add":
        print_success(f"Added alias: {alias} → {forward}")
    elif operation == "delete":
        print_success(f"Deleted alias: {alias}")
    elif operation == "list":
        print_info("Listed all aliases")


def handle_error_display(error: Exception):
    """
    Display error messages in a user-friendly way.

    Args:
        error: Exception to display
    """
    from api import (
        AuthenticationError, AliasExistsError, AliasNotFoundError,
        LimitReachedError, NetworkError, APIError
    )
    from config import ConfigError
    
    if isinstance(error, ConfigError):
        print_error("Configuration error")
        console.print(str(error), style="dim")
    elif isinstance(error, AuthenticationError):
        print_error("Authentication failed")
        console.print("Please check your API key in the .env file", style="dim")
    elif isinstance(error, AliasExistsError):
        print_error("Alias already exists")
        console.print("Choose a different alias name", style="dim")
    elif isinstance(error, AliasNotFoundError):
        print_error("Alias not found")
        console.print("Check the spelling and try again", style="dim")
    elif isinstance(error, LimitReachedError):
        print_error("Alias limit reached")
        console.print("Delete some aliases before adding new ones", style="dim")
    elif isinstance(error, NetworkError):
        print_error("Network error")
        console.print("Check your internet connection and try again", style="dim")
    else:
        print_error(f"Error: {error}")


def clear_screen():
    """Clear the terminal screen."""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
