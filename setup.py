#!/usr/bin/env python3
"""Setup script for GALIAS - Terminal-based ImprovMX alias manager."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="galias",
    version="1.0.0",
    author="GazzyCodes",
    author_email="gazzyjuruj1@gmail.com",
    description="Terminal-based ImprovMX alias manager with hacker-chic style",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gazzycodes/galias",
    packages=find_packages(),
    py_modules=[
        "improvctl",
        "config", 
        "api",
        "ui",
        "cli"
    ],
    install_requires=[
        "requests>=2.31.0",
        "rich>=13.0.0", 
        "typer>=0.9.0",
        "python-dotenv>=1.0.0"
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "responses>=0.23.0"
        ]
    },
    entry_points={
        "console_scripts": [
            "galias=improvctl:main"
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators", 
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Communications :: Email",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
        "Environment :: Console"
    ],
    python_requires=">=3.8",
    keywords="email alias improvmx cli terminal hacker",
    project_urls={
        "Bug Reports": "https://github.com/gazzycodes/galias/issues",
        "Source": "https://github.com/gazzycodes/galias",
        "Documentation": "https://github.com/gazzycodes/galias#readme"
    }
)
