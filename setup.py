"""Setup configuration for Math Operations CLI."""
from setuptools import setup, find_packages

setup(
    name="math-operations-cli",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.1.7",
        "httpx>=0.25.1",
        "tabulate>=0.9.0",
    ],
    entry_points={
        "console_scripts": [
            "math-cli=cli.commands:cli",
        ],
    },
    author="Teodor Leahu",
    author_email="teodor.leahu@endava.com",
    description="CLI for Math Operations Microservice",
    python_requires=">=3.8",
)