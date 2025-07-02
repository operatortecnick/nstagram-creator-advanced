"""
Modelos de Dados - Instagram Creator Advanced
Define estruturas de dados utilizadas pelo sistema
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class AccountData:
    """Estrutura de dados para informações da conta"""
    username: str
    email: str
    password: str
    full_name: str
    phone: Optional[str] = None
    birth_date: Optional[str] = None
    bio: Optional[str] = None

@dataclass 
class CreationResult:
    """Resultado da criação de conta"""
    success: bool
    account_data: Optional[AccountData] = None
    error_message: Optional[str] = None
    creation_time: Optional[float] = None
