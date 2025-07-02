#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instagram Creator Advanced - Setup Script
Versão: 2.0.0
Autor: operatortecnick
"""

from setuptools import setup, find_packages
import os

# Ler README para descrição longa
def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

# Ler requirements
def read_requirements():
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        # Filtrar comentários e linhas vazias
        return [line.strip() for line in lines 
                if line.strip() and not line.startswith('#')]

setup(
    name="instagram-creator-advanced",
    version="2.0.0",
    author="operatortecnick",
    author_email="operatortecnick@example.com",
    description="Sistema avançado de criação de contas Instagram com todas as correções aplicadas",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/operatortecnick/nstagram-creator-advanced",
    
    packages=find_packages(),
    
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9", 
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    
    python_requires=">=3.8",
    
    install_requires=read_requirements(),
    
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.1",
            "black>=23.12.0",
            "flake8>=6.1.0",
            "mypy>=1.7.1",
        ],
        "full": [
            "rich>=13.7.0",
            "click>=8.1.7",
            "pandas>=2.1.4",
            "openpyxl>=3.1.2",
            "aiohttp>=3.9.1",
            "aiofiles>=23.2.1",
        ]
    },
    
    entry_points={
        "console_scripts": [
            "instagram-creator=instagram_creator_advanced:main",
        ],
    },
    
    include_package_data=True,
    
    package_data={
        "": [
            "*.md",
            "*.txt", 
            "*.ini",
            "docs/*",
            "examples/*",
            "tests/*",
        ],
    },
    
    keywords=[
        "instagram", 
        "automation", 
        "selenium", 
        "account-creation",
        "social-media",
        "bot",
        "web-scraping"
    ],
    
    project_urls={
        "Bug Reports": "https://github.com/operatortecnick/nstagram-creator-advanced/issues",
        "Source": "https://github.com/operatortecnick/nstagram-creator-advanced",
        "Documentation": "https://github.com/operatortecnick/nstagram-creator-advanced/docs",
    },
)
