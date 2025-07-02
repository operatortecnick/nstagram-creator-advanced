#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instagram Creator Advanced - Testes Unitários Core
Versão: 2.0.0

Testes para verificar funcionamento de todas as funcionalidades principais.
"""

import pytest
import asyncio
import sys
import os
from unittest.mock import Mock, patch, AsyncMock
import configparser

# Adicionar caminho do projeto ao PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from instagram_creator_advanced import (
    InstagramCreatorAdvanced,
    validate_account_data,
    generate_username,
    generate_email
)


class TestInstagramCreatorAdvanced:
    """
    Testes para a classe principal InstagramCreatorAdvanced.
    """
    
    def setup_method(self):
        """Configuração antes de cada teste."""
        self.creator = InstagramCreatorAdvanced()
        self.sample_account_data = {
            'email': 'test@example.com',
            'full_name': 'Test User',
            'username': 'test_user_123',
            'password': 'password123'
        }
    
    def test_init(self):
        """Testa inicialização da classe."""
        assert self.creator is not None
        assert self.creator.config is not None
        assert self.creator.logger is not None
        assert self.creator.driver is None
        assert isinstance(self.creator.session_data, dict)
    
    def test_create_default_config(self):
        """Testa criação de configuração padrão."""
        config = self.creator._create_default_config()
        
        assert isinstance(config, configparser.ConfigParser)
        assert 'BROWSER' in config
        assert 'SECURITY' in config
        assert 'DELAYS' in config
        assert 'RETRY' in config
        assert 'LOGGING' in config
        
        # Verificar valores padrão
        assert config.get('BROWSER', 'headless') == 'false'
        assert config.get('SECURITY', 'stealth_mode') == 'true'
        assert config.get('DELAYS', 'min_delay') == '3'
    
    def test_selectors_updated(self):
        """Testa se os seletores estão atualizados."""
        expected_selectors = {
            "email_input": "input[name='emailOrPhone']",
            "fullname_input": "input[name='fullName']",
            "username_input": "input[name='username']", 
            "password_input": "input[name='password']",
            "signup_button": "button[type='submit']"
        }
        
        for key, expected_value in expected_selectors.items():
            assert self.creator.selectors[key] == expected_value


class TestValidationFunctions:
    """
    Testes para funções de validação.
    """
    
    def test_validate_account_data_valid(self):
        """Testa validação com dados válidos."""
        valid_data = {
            'email': 'user@example.com',
            'full_name': 'John Doe',
            'username': 'john_doe_123',
            'password': 'password123'
        }
        
        is_valid, errors = validate_account_data(valid_data)
        
        assert is_valid is True
        assert len(errors) == 0
    
    def test_validate_account_data_missing_fields(self):
        """Testa validação com campos obrigatórios ausentes."""
        invalid_data = {
            'email': 'user@example.com',
            # 'full_name' ausente
            'username': 'user123',
            'password': 'pass123'
        }
        
        is_valid, errors = validate_account_data(invalid_data)
        
        assert is_valid is False
        assert len(errors) > 0
        assert any("full_name" in error for error in errors)
    
    def test_validate_account_data_invalid_email(self):
        """Testa validação com email inválido."""
        invalid_data = {
            'email': 'invalid_email',  # Sem @
            'full_name': 'John Doe',
            'username': 'john_doe',
            'password': 'password123'
        }
        
        is_valid, errors = validate_account_data(invalid_data)
        
        assert is_valid is False
        assert any("Email inválido" in error for error in errors)


class TestUtilityFunctions:
    """
    Testes para funções utilitárias.
    """
    
    def test_generate_username(self):
        """Testa geração de username."""
        base_name = "test_user"
        username = generate_username(base_name)
        
        assert username.startswith(base_name)
        assert "_" in username
        assert len(username) > len(base_name)
        
        # Verificar se sufixo é numérico
        suffix = username.split("_")[-1]
        assert suffix.isdigit()
        assert 1000 <= int(suffix) <= 9999
    
    def test_generate_email(self):
        """Testa geração de email."""
        username = "test_user_123"
        email = generate_email(username)
        
        assert email.startswith(username)
        assert "@" in email
        assert email.endswith("tempmail.com")


def test_imports():
    """Testa se todas as importações estão funcionando."""
    try:
        from instagram_creator_advanced import (
            InstagramCreatorAdvanced,
            validate_account_data,
            generate_username,
            generate_email
        )
        assert True
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")


def test_version_compatibility():
    """Testa compatibilidade de versões."""
    import sys
    
    # Python 3.8+
    assert sys.version_info >= (3, 8)


if __name__ == "__main__":
    print("🧪 Instagram Creator Advanced - Testes Core")
    print("=" * 50)
    
    try:
        import pytest
        print("✅ Pytest encontrado")
        exit_code = pytest.main([__file__, "-v"])
        
        if exit_code == 0:
            print("\n🎉 Todos os testes passaram!")
        else:
            print("\n❌ Alguns testes falharam")
            
    except ImportError:
        print("❌ Pytest não instalado")
        print("📦 Instale com: pip install pytest pytest-asyncio")
        
        # Testes básicos
        print("\n🔧 Executando testes básicos...")
        
        try:
            from instagram_creator_advanced import InstagramCreatorAdvanced
            print("✅ Import básico OK")
            
            creator = InstagramCreatorAdvanced()
            print("✅ Inicialização OK")
            
            from instagram_creator_advanced import validate_account_data
            test_data = {
                'email': 'test@example.com',
                'full_name': 'Test',
                'username': 'test123',
                'password': 'password123'
            }
            is_valid, errors = validate_account_data(test_data)
            if is_valid:
                print("✅ Validação OK")
            else:
                print(f"❌ Validação falhou: {errors}")
                
            print("\n🎉 Testes básicos concluídos!")
            
        except Exception as e:
            print(f"❌ Erro: {e}")
