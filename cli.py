"""CLI commands for GALIAS."""

import typer
from typing import Optional
import sys

from api import get_api, APIError
from ui import (
    print_banner, print_aliases_table, print_alias_count,
    print_success, print_error, print_json_output,
    prompt_alias, prompt_forward, prompt_delete_alias,
    confirm_delete, handle_error_display, print_operation_summary
)
from config import DOMAIN, MAX_ALIASES
from pathlib import Path


app = typer.Typer(
    name="galias",
    help="GALIAS - Terminal-based ImprovMX alias manager",
    add_completion=False
)





def show_banner_and_count(skip_banner: bool = False):
    """Show banner and current alias count."""
    if not skip_banner:
        print_banner()
    
    try:
        api = get_api()
        count = api.get_alias_count()
        print_alias_count(count)
        print()
        return count
    except Exception as e:
        handle_error_display(e)
        return None


@app.command()
def list(
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON for scripting"),
    no_color: bool = typer.Option(False, "--no-color", help="Disable colored output"),
    quiet: bool = typer.Option(False, "-q", "--quiet", help="Skip banner and just show aliases")
):
    """List all aliases and show current count."""
    try:
        # Set up console for no-color mode
        if no_color:
            from ui import console
            console._color_system = None
        
        api = get_api()
        aliases_data = api.list_aliases()
        
        if json_output:
            print_json_output(aliases_data)
            return
        
        if not quiet:
            show_banner_and_count()
        
        print_aliases_table(aliases_data)
        
        if not quiet:
            count = len(aliases_data.get("aliases", []))
            print_alias_count(count)
        
    except Exception as e:
        handle_error_display(e)
        sys.exit(1)


@app.command()
def add(
    alias: Optional[str] = typer.Argument(None, help="Alias name (without domain)"),
    forward: Optional[str] = typer.Argument(None, help="Email address to forward to"),
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON for scripting"),
    no_color: bool = typer.Option(False, "--no-color", help="Disable colored output"),
    quiet: bool = typer.Option(False, "-q", "--quiet", help="Skip banner and progress display")
):
    """Add a new alias."""
    try:
        # Set up console for no-color mode
        if no_color:
            from ui import console
            console._color_system = None
        
        if not quiet:
            show_banner_and_count()
        
        # Interactive prompts if arguments not provided
        if alias is None:
            alias = prompt_alias()
        
        if forward is None:
            forward = prompt_forward()
        
        # Validate inputs
        if not alias or not forward:
            print_error("Both alias and forward email are required")
            sys.exit(1)
        
        # Validate email format (basic check)
        if "@" not in forward or "." not in forward:
            print_error("Invalid email format for forward address")
            sys.exit(1)
        
        api = get_api()
        result = api.add_alias(alias, forward)
        
        if json_output:
            print_json_output(result)
            return
        
        print_operation_summary("add", alias, forward)
        
        # Show updated count
        if not quiet:
            print()
            count = api.get_alias_count()
            print_alias_count(count)
        
    except Exception as e:
        handle_error_display(e)
        sys.exit(1)


@app.command()
def delete(
    alias: Optional[str] = typer.Argument(None, help="Alias name to delete"),
    force: bool = typer.Option(False, "-f", "--force", help="Skip confirmation prompt"),
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON for scripting"),
    no_color: bool = typer.Option(False, "--no-color", help="Disable colored output"),
    quiet: bool = typer.Option(False, "-q", "--quiet", help="Skip banner and progress display")
):
    """Delete an existing alias."""
    try:
        # Set up console for no-color mode
        if no_color:
            from ui import console
            console._color_system = None
        
        if not quiet:
            show_banner_and_count()
        
        # Interactive prompt if alias not provided
        if alias is None:
            alias = prompt_delete_alias()
        
        if not alias:
            print_error("Alias name is required")
            sys.exit(1)
        
        # Confirmation prompt (unless forced or in JSON mode)
        if not force and not json_output:
            if not confirm_delete(alias):
                print("Operation cancelled.")
                return
        
        api = get_api()
        result = api.delete_alias(alias)
        
        if json_output:
            print_json_output(result)
            return
        
        print_operation_summary("delete", alias)
        
        # Show updated count
        if not quiet:
            print()
            count = api.get_alias_count()
            print_alias_count(count)
        
    except Exception as e:
        handle_error_display(e)
        sys.exit(1)


@app.command()
def status(
    json_output: bool = typer.Option(False, "--json", help="Output raw JSON for scripting"),
    no_color: bool = typer.Option(False, "--no-color", help="Disable colored output")
):
    """Show current alias count and status."""
    try:
        # Set up console for no-color mode
        if no_color:
            from ui import console
            console._color_system = None
        
        api = get_api()
        count = api.get_alias_count()
        
        if json_output:
            status_data = {
                "current_aliases": count,
                "max_aliases": MAX_ALIASES,
                "domain": DOMAIN,
                "usage_percentage": round((count / MAX_ALIASES) * 100, 1)
            }
            print_json_output(status_data)
            return
        
        print_banner()
        print_alias_count(count)
        
    except Exception as e:
        handle_error_display(e)
        sys.exit(1)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", help="Show version information")
):
    """GALIAS - Terminal-based ImprovMX alias manager."""
    if version:
        typer.echo("GALIAS v1.0.0")
        typer.echo("ImprovMX Alias Manager")
        raise typer.Exit()

    if ctx.invoked_subcommand is None:
        typer.echo("GALIAS - Terminal-based ImprovMX alias manager")
        typer.echo("Use --help for more information.")


if __name__ == "__main__":
    app()
