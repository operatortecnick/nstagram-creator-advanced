#!/usr/bin/env python3
"""
Setup script para Instagram Creator Advanced
Instala e configura o ambiente de forma automatizada
"""

from setuptools import setup, find_packages
import os
import sys

# Lê o README para descrição longa
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Sistema avançado de criação de contas Instagram"

# Lê os requirements
def read_requirements():
    req_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    requirements = []
    if os.path.exists(req_path):
        with open(req_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Remove comentários inline
                    if ';' in line:
                        line = line.split(';')[0].strip()
                    requirements.append(line)
    return requirements

setup(
    name="instagram-creator-advanced",
    version="2.0.0",
    author="operatortecnick",
    author_email="",
    description="Sistema avançado de criação de contas Instagram - Versão corrigida",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/operatortecnick/nstagram-creator-advanced",
    packages=find_packages(),
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
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.1",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
        "gui": [
            "tkinter",
        ],
        "data": [
            "pandas>=2.1.0",
            "openpyxl>=3.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "instagram-creator=instagram_creator:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.ini", "*.md", "*.txt"],
    },
)

# Script de instalação personalizada
if __name__ == "__main__":
    print("🚀 Instagram Creator Advanced - Setup")
    print("=" * 50)
    
    # Verifica versão do Python
    if sys.version_info < (3, 8):
        print("❌ Erro: Python 3.8+ é necessário")
        sys.exit(1)
    
    print("✅ Versão do Python compatível")
    
    # Executa setup
    try:
        setup()
        print("✅ Instalação concluída com sucesso!")
        print("\n💡 Próximos passos:")
        print("1. Configure o arquivo config_default.ini")
        print("2. Execute: python instagram_creator.py")
        print("3. Ou use: instagram-creator (se instalado globalmente)")
        
    except Exception as e:
        print(f"❌ Erro durante instalação: {e}")
        sys.exit(1)
