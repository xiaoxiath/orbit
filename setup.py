#!/usr/bin/env python3
"""Minimal setup.py for building orbit-macos package."""

from setuptools import setup, find_packages

# Read pyproject.toml for metadata
import re
with open('pyproject.toml', 'r') as f:
    content = f.read()
    name = re.search(r'name = "(.*?)"', content).group(1)
    version = re.search(r'version = "(.*?)"', content).group(1)
    description = re.search(r'description = "(.*?)"', content).group(1)

setup(
    name=name,
    version=version,
    description=description,
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'jinja2>=3.0.0',
        'click>=8.0.0',
    ],
    python_requires='>=3.10',
    entry_points={
        'console_scripts': [
            'orbit=orbit.cli:cli',
        ],
    },
)
