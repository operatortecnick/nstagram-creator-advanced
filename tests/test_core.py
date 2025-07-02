#!/usr/bin/env python3
"""
Testes Unitários - Instagram Creator Advanced
Testa todas as funcionalidades principais do sistema
"""

import unittest
import asyncio
import tempfile
import os
import configparser
from unittest.mock import Mock, patch, AsyncMock
import sys
from pathlib import Path

# Adicionar diretório pai ao path
sys.path.append(str(Path(__file__).parent.parent))

try:
    from instagram_creator import (
        InstagramCreatorAdvanced, 
        AccountData, 
        CreationResult
    )
except ImportError:
    print("❌ Erro: Não foi possível importar módulos para teste")
    print("💡 Execute os testes a partir do diretório raiz do projeto")
    sys.exit(1)

class TestAccountData(unittest.TestCase):
    """Testa a estrutura de dados AccountData"""
    
    def test_account_data_creation(self):
        """Testa criação de AccountData"""
        account = AccountData(
            username="test_user",
            email="test@example.com",
            password="test123",
            full_name="Test User"
        )
        
        self.assertEqual(account.username, "test_user")
        self.assertEqual(account.email, "test@example.com")
        self.assertEqual(account.password, "test123")
        self.assertEqual(account.full_name, "Test User")
        self.assertIsNone(account.phone)
        self.assertIsNone(account.birth_date)
        self.assertIsNone(account.bio)
    
    def test_account_data_with_optionals(self):
        """Testa AccountData com campos opcionais"""
        account = AccountData(
            username="test_user",
            email="test@example.com", 
            password="test123",
            full_name="Test User",
            phone="123456789",
            birth_date="1990-01-01",
            bio="Test bio"
        )
        
        self.assertEqual(account.phone, "123456789")
        self.assertEqual(account.birth_date, "1990-01-01")
        self.assertEqual(account.bio, "Test bio")

class TestCreationResult(unittest.TestCase):
    """Testa a estrutura CreationResult"""
    
    def test_successful_result(self):
        """Testa resultado bem-sucedido"""
        account = AccountData("user", "email@test.com", "pass", "Name")
        result = CreationResult(
            success=True,
            account_data=account,
            creation_time=5.5
        )
        
        self.assertTrue(result.success)
        self.assertEqual(result.account_data, account)
        self.assertEqual(result.creation_time, 5.5)
        self.assertIsNone(result.error_message)
    
    def test_failed_result(self):
        """Testa resultado com falha"""
        result = CreationResult(
            success=False,
            error_message="Test error"
        )
        
        self.assertFalse(result.success)
        self.assertEqual(result.error_message, "Test error")
        self.assertIsNone(result.account_data)
        self.assertIsNone(result.creation_time)

class TestInstagramCreatorAdvanced(unittest.TestCase):
    """Testa a classe principal InstagramCreatorAdvanced"""
    
    def setUp(self):
        """Configuração para cada teste"""
        # Criar arquivo de configuração temporário
        self.temp_config = tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False)
        self.temp_config.write("""
[BROWSER]
headless = true
window_size = 1280,720
implicitly_wait = 5
page_load_timeout = 15

[DELAYS]
min_delay = 0.1
max_delay = 0.2
typing_delay = 0.01

[SECURITY]
stealth_mode = true
use_proxy = false

[ACCOUNT_GENERATION]
username_prefix = test
email_domain = @test.com
password_length = 8
include_symbols = false

[RETRY]
max_attempts = 2
retry_delay = 1
timeout_seconds = 10
""")
        self.temp_config.close()
        
        self.creator = InstagramCreatorAdvanced(self.temp_config.name)
    
    def tearDown(self):
        """Limpeza após cada teste"""
        # Remover arquivo temporário
        os.unlink(self.temp_config.name)
    
    def test_initialization(self):
        """Testa inicialização do criador"""
        self.assertIsInstance(self.creator.config, configparser.ConfigParser)
        self.assertEqual(self.creator.config_file, self.temp_config.name)
        self.assertIsNone(self.creator.driver)
        self.assertIsNone(self.creator.wait)
    
    def test_load_config(self):
        """Testa carregamento de configuração"""
        config = self.creator._load_config()
        
        self.assertTrue(config.getboolean('BROWSER', 'headless'))
        self.assertEqual(config.get('BROWSER', 'window_size'), '1280,720')
        self.assertEqual(config.get('ACCOUNT_GENERATION', 'username_prefix'), 'test')
    
    def test_create_default_config(self):
        """Testa criação de configuração padrão"""
        temp_file = tempfile.NamedTemporaryFile(suffix='.ini', delete=False)
        temp_file.close()
        os.unlink(temp_file.name)  # Remove para testar criação
        
        creator = InstagramCreatorAdvanced(temp_file.name)
        creator._create_default_config()
        
        self.assertTrue(os.path.exists(temp_file.name))
        
        # Verificar conteúdo
        config = configparser.ConfigParser()
        config.read(temp_file.name)
        
        self.assertTrue(config.has_section('BROWSER'))
        self.assertTrue(config.has_section('DELAYS'))
        self.assertTrue(config.has_section('SECURITY'))
        
        # Limpar
        os.unlink(temp_file.name)
    
    def test_get_updated_selectors(self):
        """Testa seletores atualizados"""
        selectors = self.creator._get_updated_selectors()
        
        required_selectors = [
            'email_input', 'fullname_input', 'username_input',
            'password_input', 'signup_button'
        ]
        
        for selector in required_selectors:
            self.assertIn(selector, selectors)
            self.assertIsInstance(selectors[selector], str)
            self.assertTrue(len(selectors[selector]) > 0)
    
    def test_generate_random_string(self):
        """Testa geração de string aleatória"""
        # Teste comprimento padrão
        random_str = self.creator._generate_random_string()
        self.assertEqual(len(random_str), 8)
        
        # Teste comprimento personalizado
        random_str_custom = self.creator._generate_random_string(12)
        self.assertEqual(len(random_str_custom), 12)
        
        # Teste unicidade
        str1 = self.creator._generate_random_string()
        str2 = self.creator._generate_random_string()
        self.assertNotEqual(str1, str2)
    
    def test_generate_account_data(self):
        """Testa geração de dados da conta"""
        account_data = self.creator._generate_account_data()
        
        self.assertIsInstance(account_data, AccountData)
        self.assertTrue(account_data.username.startswith('test_'))
        self.assertTrue(account_data.email.endswith('@test.com'))
        self.assertEqual(len(account_data.password), 8)
        self.assertTrue(len(account_data.full_name) > 0)
        
        # Teste unicidade
        account_data2 = self.creator._generate_account_data()
        self.assertNotEqual(account_data.username, account_data2.username)
        self.assertNotEqual(account_data.email, account_data2.email)

class TestAsyncMethods(unittest.IsolatedAsyncioTestCase):
    """Testa métodos assíncronos"""
    
    async def asyncSetUp(self):
        """Configuração assíncrona"""
        # Criar configuração de teste
        self.temp_config = tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False)
        self.temp_config.write("""
[BROWSER]
headless = true
[DELAYS]
min_delay = 0.01
max_delay = 0.02
typing_delay = 0.001
[RETRY]
timeout_seconds = 5
""")
        self.temp_config.close()
        
        self.creator = InstagramCreatorAdvanced(self.temp_config.name)
    
    async def asyncTearDown(self):
        """Limpeza assíncrona"""
        # Limpar driver se ainda existir
        if self.creator.driver:
            await self.creator._cleanup_driver()
        
        # Remover arquivo temporário
        os.unlink(self.temp_config.name)
    
    async def test_human_like_delay(self):
        """Testa delays humanizados"""
        import time
        
        start_time = time.time()
        await self.creator._human_like_delay(0.01, 0.02)
        end_time = time.time()
        
        delay_duration = end_time - start_time
        self.assertGreaterEqual(delay_duration, 0.01)
        self.assertLessEqual(delay_duration, 0.05)  # Margem para processamento
    
    @patch('selenium.webdriver.Chrome')
    async def test_setup_driver_mock(self, mock_chrome):
        """Testa configuração do driver (mock)"""
        mock_driver = Mock()
        mock_chrome.return_value = mock_driver
        
        await self.creator._setup_driver()
        
        # Verificar se driver foi configurado
        self.assertIsNotNone(self.creator.driver)
        mock_driver.implicitly_wait.assert_called()
        mock_driver.set_page_load_timeout.assert_called()
    
    async def test_cleanup_driver(self):
        """Testa limpeza do driver"""
        # Simular driver existente
        mock_driver = Mock()
        self.creator.driver = mock_driver
        
        await self.creator._cleanup_driver()
        
        mock_driver.quit.assert_called_once()
        self.assertIsNone(self.creator.driver)
        self.assertIsNone(self.creator.wait)

class TestIntegration(unittest.IsolatedAsyncioTestCase):
    """Testes de integração (simulados)"""
    
    async def asyncSetUp(self):
        """Configuração para testes de integração"""
        self.temp_config = tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False)
        self.temp_config.write("""
[BROWSER]
headless = true
[DELAYS]
min_delay = 0.01
max_delay = 0.02
[ACCOUNT_GENERATION]
username_prefix = integration_test
[RETRY]
max_attempts = 1
timeout_seconds = 2
""")
        self.temp_config.close()
        
        self.creator = InstagramCreatorAdvanced(self.temp_config.name)
    
    async def asyncTearDown(self):
        """Limpeza após testes de integração"""
        if self.creator.driver:
            await self.creator._cleanup_driver()
        os.unlink(self.temp_config.name)
    
    @patch('instagram_creator.InstagramCreatorAdvanced._setup_driver')
    @patch('instagram_creator.InstagramCreatorAdvanced._cleanup_driver') 
    async def test_create_account_workflow_mock(self, mock_cleanup, mock_setup):
        """Testa workflow de criação de conta (mock)"""
        # Mock do driver e elementos
        mock_driver = Mock()
        mock_element = Mock()
        
        # Configurar mocks
        mock_setup.return_value = None
        mock_cleanup.return_value = None
        self.creator.driver = mock_driver
        self.creator.wait = Mock()
        
        # Mock para encontrar elementos
        mock_driver.get.return_value = None
        mock_driver.find_elements.return_value = []  # Sem erros
        self.creator.wait.until.return_value = mock_element
        
        # Dados de teste
        test_account = AccountData(
            username="test_user",
            email="test@example.com",
            password="test123",
            full_name="Test User"
        )
        
        # Executar teste
        result = await self.creator.create_account(test_account)
        
        # Verificações básicas (já que está mockado)
        mock_setup.assert_called_once()
        mock_cleanup.assert_called_once()
        mock_driver.get.assert_called_once()

class TestConfigurationHandling(unittest.TestCase):
    """Testa tratamento de configurações"""
    
    def test_invalid_config_file(self):
        """Testa tratamento de arquivo inválido"""
        # Arquivo que não existe
        creator = InstagramCreatorAdvanced("arquivo_inexistente.ini")
        
        # Deve criar configuração padrão
        self.assertTrue(os.path.exists("arquivo_inexistente.ini"))
        
        # Limpar
        os.unlink("arquivo_inexistente.ini")
    
    def test_malformed_config(self):
        """Testa configuração mal formada"""
        temp_config = tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False)
        temp_config.write("configuracao_invalida_sem_secoes")
        temp_config.close()
        
        try:
            # Deve funcionar mesmo com config inválida
            creator = InstagramCreatorAdvanced(temp_config.name)
            self.assertIsNotNone(creator.config)
        except Exception as e:
            self.fail(f"Falhou ao lidar com config inválida: {e}")
        finally:
            os.unlink(temp_config.name)

def run_all_tests():
    """Executa todos os testes"""
    print("🧪 Executando testes do Instagram Creator Advanced")
    print("=" * 60)
    
    # Criar test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Adicionar todas as classes de teste
    test_classes = [
        TestAccountData,
        TestCreationResult, 
        TestInstagramCreatorAdvanced,
        TestAsyncMethods,
        TestIntegration,
        TestConfigurationHandling
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Executar testes
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Relatório final
    print("\n" + "=" * 60)
    print("📊 RELATÓRIO DE TESTES")
    print("=" * 60)
    print(f"✅ Testes executados: {result.testsRun}")
    print(f"❌ Falhas: {len(result.failures)}")
    print(f"🚫 Erros: {len(result.errors)}")
    print(f"⏭️  Pulados: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.failures:
        print(f"\n❌ FALHAS:")
        for test, traceback in result.failures:
            print(f"   {test}: {traceback.split('\\n')[-2]}")
    
    if result.errors:
        print(f"\n🚫 ERROS:")
        for test, traceback in result.errors:
            print(f"   {test}: {traceback.split('\\n')[-2]}")
    
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun) * 100
    print(f"\n📈 Taxa de sucesso: {success_rate:.1f}%")
    print("=" * 60)
    
    return result.wasSuccessful()

if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"💥 Erro ao executar testes: {e}")
        sys.exit(1)
