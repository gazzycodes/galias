# Changelog

All notable changes to GALIAS will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-05

### Added
- Initial release of GALIAS CLI
- Terminal-based ImprovMX alias management
- Hacker-chic ASCII banner and styled output
- Real-time alias count with progress bars
- Interactive prompts for user-friendly operation
- JSON output support for scripting
- Comprehensive error handling with helpful messages
- Support for list, add, delete, and status commands
- Configuration via .env file with validation
- Complete test suite with 57+ tests
- Installable package with `pip install`
- Console script entry point (`galias` command)

### Features
- **Commands**: `list`, `add`, `delete`, `status`
- **Options**: `--json`, `--no-color`, `--quiet`, `--force`
- **Interactive mode**: Prompts for alias and forward email
- **Progress tracking**: Visual progress bars showing alias usage
- **Error handling**: Clear, actionable error messages
- **Validation**: API key format and domain validation
- **Styling**: Rich terminal output with colors and tables

### Technical
- Python 3.8+ support
- Dependencies: requests, rich, typer, python-dotenv
- Comprehensive test coverage
- Modern Python packaging (setup.py + pyproject.toml)
- MIT License
