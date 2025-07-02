"""
Instagram Creator Advanced - Módulo Principal
Versão 2.0 - Corrigida e Otimizada
"""

__version__ = "2.0.0"
__author__ = "operatortecnick"
__license__ = "MIT"

from .core import InstagramCreatorAdvanced
from .models import AccountData, CreationResult
from .config import ConfigManager
from .utils import (
    generate_random_string,
    validate_email,
    validate_username,
    validate_password
)

__all__ = [
    "InstagramCreatorAdvanced",
    "AccountData", 
    "CreationResult",
    "ConfigManager",
    "generate_random_string",
    "validate_email",
    "validate_username", 
    "validate_password"
]
