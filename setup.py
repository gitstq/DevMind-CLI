#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DevMind-CLI 安装配置
DevMind-CLI Setup Configuration
"""

from setuptools import setup, find_packages
from pathlib import Path

# 读取README
readme_file = Path(__file__).parent / "README.md"
long_description = ""
if readme_file.exists():
    long_description = readme_file.read_text(encoding="utf-8")

# 读取版本
version_file = Path(__file__).parent / "VERSION"
version = "1.0.0"
if version_file.exists():
    version = version_file.read_text().strip()

setup(
    name="devmind-cli",
    version=version,
    author="gitstq",
    author_email="gitstq@github.com",
    description="🧠 DevMind-CLI - 基于GLM-5.1的开发者智能助手",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitstq/DevMind-CLI",
    project_urls={
        "Bug Reports": "https://github.com/gitstq/DevMind-CLI/issues",
        "Source": "https://github.com/gitstq/DevMind-CLI",
        "Documentation": "https://github.com/gitstq/DevMind-CLI#readme",
    },
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Debuggers",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
    ],
    python_requires=">=3.8",
    install_requires=[
        # 零依赖设计 - 无需安装任何包
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "ui": [
            "rich>=13.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "devmind=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
