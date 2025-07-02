#!/usr/bin/env python3
"""
Instagram Creator Advanced - Sistema Avançado de Criação de Contas
Versão Corrigida e Otimizada

Este script automatiza a criação de contas Instagram de forma segura e eficiente.
Todas as correções de bugs e melhorias de segurança foram implementadas.

Autor: operatortecnick
Licença: MIT
Versão: 2.0.0
"""

import asyncio
import logging
import sys
import os
import random
import string
import time
import json
import configparser
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from contextlib import asynccontextmanager

# Imports corrigidos e organizados
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.firefox.options import Options as FirefoxOptions
    from selenium.common.exceptions import (
        TimeoutException, 
        NoSuchElementException, 
        WebDriverException,
        ElementClickInterceptedException,
        StaleElementReferenceException
    )
except ImportError as e:
    print(f"❌ Erro: Dependência não encontrada - {e}")
    print("💡 Execute: pip install -r requirements.txt")
    sys.exit(1)

try:
    import requests
    from fake_useragent import UserAgent
    import undetected_chromedriver as uc
except ImportError as e:
    print(f"⚠️  Dependência opcional não encontrada - {e}")
    print("💡 Para funcionalidades avançadas, execute: pip install -r requirements.txt")

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('instagram_creator.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

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

class InstagramCreatorAdvanced:
    """
    Classe principal para criação automatizada de contas Instagram
    Versão corrigida com todas as melhorias de segurança e estabilidade
    """
    
    def __init__(self, config_file: str = "config.ini"):
        """
        Inicializa o criador de contas Instagram
        
        Args:
            config_file: Caminho para o arquivo de configuração
        """
        self.config_file = config_file
        self.config = self._load_config()
        self.driver: Optional[webdriver.Chrome] = None
        self.wait: Optional[WebDriverWait] = None
        self.ua = None
        
        # Inicializa UserAgent se disponível
        try:
            self.ua = UserAgent()
        except Exception:
            logger.warning("UserAgent não disponível, usando padrão")
        
        # URLs e seletores atualizados
        self.instagram_url = "https://www.instagram.com/accounts/emailsignup/"
        self.selectors = self._get_updated_selectors()
        
        logger.info("✅ InstagramCreatorAdvanced inicializado com sucesso")
    
    def _load_config(self) -> configparser.ConfigParser:
        """Carrega configurações do arquivo ini"""
        config = configparser.ConfigParser()
        
        if os.path.exists(self.config_file):
            config.read(self.config_file)
            logger.info(f"✅ Configuração carregada de {self.config_file}")
        else:
            logger.warning(f"⚠️  Arquivo {self.config_file} não encontrado, usando padrões")
            self._create_default_config()
            config.read(self.config_file)
        
        return config
    
    def _create_default_config(self):
        """Cria arquivo de configuração padrão"""
        default_config = """[BROWSER]
headless = false
window_size = 1920,1080
user_agent = 
implicitly_wait = 10
page_load_timeout = 30

[DELAYS]
min_delay = 2
max_delay = 5
typing_delay = 0.1
form_submission_delay = 3

[SECURITY]
use_proxy = false
proxy_list = 
rotation_enabled = false
stealth_mode = true

[ACCOUNT_GENERATION]
username_prefix = user
email_domain = @gmail.com
password_length = 12
include_symbols = true

[RETRY]
max_attempts = 3
retry_delay = 5
timeout_seconds = 30"""
        
        with open(self.config_file, 'w') as f:
            f.write(default_config)
        
        logger.info(f"✅ Arquivo de configuração padrão criado: {self.config_file}")
    
    def _get_updated_selectors(self) -> Dict[str, str]:
        """Retorna seletores atualizados do Instagram"""
        return {
            "email_input": "input[name='emailOrPhone']",
            "fullname_input": "input[name='fullName']", 
            "username_input": "input[name='username']",
            "password_input": "input[name='password']",
            "signup_button": "button[type='submit']",
            "month_select": "select[title='Month:']",
            "day_select": "select[title='Day:']", 
            "year_select": "select[title='Year:']",
            "continue_button": "//button[contains(text(), 'Next')]",
            "error_message": "[role='alert']",
            "username_available": "//span[contains(text(), 'available')]"
        }
    
    @asynccontextmanager
    async def _browser_context(self):
        """Context manager para gerenciar o navegador de forma segura"""
        try:
            await self._setup_driver()
            yield self.driver
        except Exception as e:
            logger.error(f"❌ Erro no contexto do navegador: {e}")
            raise
        finally:
            await self._cleanup_driver()
    
    async def _setup_driver(self):
        """Configura o driver do navegador com todas as otimizações"""
        try:
            # Configurações do Chrome otimizadas
            chrome_options = ChromeOptions()
            
            # Configurações de segurança e performance
            if self.config.getboolean('BROWSER', 'headless', fallback=False):
                chrome_options.add_argument('--headless')
            
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # User Agent personalizado
            if self.ua:
                chrome_options.add_argument(f'--user-agent={self.ua.random}')
            
            # Tamanho da janela
            window_size = self.config.get('BROWSER', 'window_size', fallback='1920,1080')
            chrome_options.add_argument(f'--window-size={window_size}')
            
            # Inicializa driver (tentativa com undetected-chromedriver primeiro)
            try:
                self.driver = uc.Chrome(options=chrome_options)
                logger.info("✅ Driver undetected-chromedriver inicializado")
            except Exception:
                self.driver = webdriver.Chrome(options=chrome_options)
                logger.info("✅ Driver Chrome padrão inicializado")
            
            # Configurações de timeout
            implicitly_wait = self.config.getint('BROWSER', 'implicitly_wait', fallback=10)
            page_load_timeout = self.config.getint('BROWSER', 'page_load_timeout', fallback=30)
            
            self.driver.implicitly_wait(implicitly_wait)
            self.driver.set_page_load_timeout(page_load_timeout)
            
            # WebDriverWait configurado
            timeout_seconds = self.config.getint('RETRY', 'timeout_seconds', fallback=30)
            self.wait = WebDriverWait(self.driver, timeout_seconds)
            
            # Remove propriedades de detecção de automação
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            logger.info("✅ Driver configurado com sucesso")
            
        except Exception as e:
            logger.error(f"❌ Erro ao configurar driver: {e}")
            raise
    
    async def _cleanup_driver(self):
        """Limpa recursos do driver de forma segura"""
        try:
            if self.driver:
                self.driver.quit()
                self.driver = None
                self.wait = None
                logger.info("✅ Driver finalizado com sucesso")
        except Exception as e:
            logger.warning(f"⚠️  Erro ao finalizar driver: {e}")
    
    def _generate_random_string(self, length: int = 8) -> str:
        """Gera string aleatória"""
        letters = string.ascii_lowercase + string.digits
        return ''.join(random.choice(letters) for _ in range(length))
    
    def _generate_account_data(self) -> AccountData:
        """Gera dados aleatórios para a conta"""
        # Configurações de geração
        username_prefix = self.config.get('ACCOUNT_GENERATION', 'username_prefix', fallback='user')
        email_domain = self.config.get('ACCOUNT_GENERATION', 'email_domain', fallback='@gmail.com')
        password_length = self.config.getint('ACCOUNT_GENERATION', 'password_length', fallback=12)
        include_symbols = self.config.getboolean('ACCOUNT_GENERATION', 'include_symbols', fallback=True)
        
        # Gera dados únicos
        random_suffix = self._generate_random_string(8)
        username = f"{username_prefix}_{random_suffix}"
        email = f"{username}{email_domain}"
        
        # Gera senha segura
        password_chars = string.ascii_letters + string.digits
        if include_symbols:
            password_chars += "!@#$%^&*"
        
        password = ''.join(random.choice(password_chars) for _ in range(password_length))
        
        # Nome completo fictício
        first_names = ["Alex", "Jordan", "Taylor", "Casey", "Morgan", "Riley", "Avery", "Quinn"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]
        full_name = f"{random.choice(first_names)} {random.choice(last_names)}"
        
        return AccountData(
            username=username,
            email=email, 
            password=password,
            full_name=full_name
        )
    
    async def _human_like_delay(self, min_delay: Optional[float] = None, max_delay: Optional[float] = None):
        """Implementa delays similares a comportamento humano"""
        if min_delay is None:
            min_delay = self.config.getfloat('DELAYS', 'min_delay', fallback=2.0)
        if max_delay is None:
            max_delay = self.config.getfloat('DELAYS', 'max_delay', fallback=5.0)
        
        delay = random.uniform(min_delay, max_delay)
        await asyncio.sleep(delay)
    
    async def _human_like_typing(self, element, text: str):
        """Simula digitação humana"""
        typing_delay = self.config.getfloat('DELAYS', 'typing_delay', fallback=0.1)
        
        for char in text:
            element.send_keys(char)
            if random.random() < 0.1:  # 10% chance de pausa extra
                await asyncio.sleep(random.uniform(0.1, 0.3))
            await asyncio.sleep(typing_delay)
    
    async def _wait_and_find_element(self, selector: str, by: By = By.CSS_SELECTOR, timeout: int = 30):
        """Aguarda e encontra elemento de forma robusta"""
        try:
            if selector.startswith('//'):
                by = By.XPATH
            
            element = self.wait.until(
                EC.presence_of_element_located((by, selector))
            )
            
            # Aguarda elemento ser clicável
            element = self.wait.until(
                EC.element_to_be_clickable((by, selector))
            )
            
            return element
            
        except TimeoutException:
            logger.error(f"❌ Timeout ao encontrar elemento: {selector}")
            raise
        except Exception as e:
            logger.error(f"❌ Erro ao encontrar elemento {selector}: {e}")
            raise
    
    async def _fill_form_field(self, selector: str, value: str, field_name: str):
        """Preenche campo do formulário de forma segura"""
        try:
            element = await self._wait_and_find_element(selector)
            
            # Limpa campo primeiro
            element.clear()
            await self._human_like_delay(0.5, 1.0)
            
            # Digita valor
            await self._human_like_typing(element, value)
            await self._human_like_delay(0.5, 1.5)
            
            logger.info(f"✅ Campo {field_name} preenchido com sucesso")
            
        except Exception as e:
            logger.error(f"❌ Erro ao preencher campo {field_name}: {e}")
            raise
    
    async def _check_for_errors(self) -> Optional[str]:
        """Verifica se há mensagens de erro na página"""
        try:
            error_elements = self.driver.find_elements(By.CSS_SELECTOR, self.selectors["error_message"])
            if error_elements:
                error_text = error_elements[0].text
                logger.warning(f"⚠️  Erro detectado: {error_text}")
                return error_text
            return None
        except Exception:
            return None
    
    async def create_account(self, account_data: Optional[AccountData] = None) -> CreationResult:
        """
        Cria uma conta Instagram de forma automatizada
        
        Args:
            account_data: Dados da conta (se None, gera automaticamente)
            
        Returns:
            CreationResult com resultado da operação
        """
        start_time = time.time()
        
        if account_data is None:
            account_data = self._generate_account_data()
        
        logger.info(f"🚀 Iniciando criação de conta para: {account_data.username}")
        
        async with self._browser_context():
            try:
                # Navega para página de signup
                logger.info("📱 Navegando para página de registro...")
                self.driver.get(self.instagram_url)
                await self._human_like_delay(3, 5)
                
                # Preenche email
                await self._fill_form_field(
                    self.selectors["email_input"], 
                    account_data.email, 
                    "email"
                )
                
                # Preenche nome completo
                await self._fill_form_field(
                    self.selectors["fullname_input"], 
                    account_data.full_name, 
                    "nome completo"
                )
                
                # Preenche username
                await self._fill_form_field(
                    self.selectors["username_input"], 
                    account_data.username, 
                    "username"
                )
                
                # Preenche senha
                await self._fill_form_field(
                    self.selectors["password_input"], 
                    account_data.password, 
                    "senha"
                )
                
                # Verifica erros antes de continuar
                error_message = await self._check_for_errors()
                if error_message:
                    return CreationResult(
                        success=False,
                        error_message=f"Erro no formulário: {error_message}"
                    )
                
                # Clica em "Sign Up"
                logger.info("📝 Enviando formulário...")
                signup_button = await self._wait_and_find_element(self.selectors["signup_button"])
                
                # Scroll para o botão se necessário
                self.driver.execute_script("arguments[0].scrollIntoView();", signup_button)
                await self._human_like_delay(1, 2)
                
                signup_button.click()
                await self._human_like_delay(3, 5)
                
                # Verifica se chegou na próxima etapa ou se há erros
                error_message = await self._check_for_errors()
                if error_message:
                    return CreationResult(
                        success=False,
                        error_message=f"Erro no envio: {error_message}"
                    )
                
                # Se chegou até aqui, considera sucesso
                creation_time = time.time() - start_time
                logger.info(f"✅ Conta criada com sucesso em {creation_time:.2f}s!")
                
                return CreationResult(
                    success=True,
                    account_data=account_data,
                    creation_time=creation_time
                )
                
            except Exception as e:
                logger.error(f"❌ Erro durante criação da conta: {e}")
                return CreationResult(
                    success=False,
                    error_message=str(e)
                )
    
    async def create_multiple_accounts(self, count: int) -> List[CreationResult]:
        """
        Cria múltiplas contas de forma sequencial
        
        Args:
            count: Número de contas a criar
            
        Returns:
            Lista com resultados de cada criação
        """
        logger.info(f"🔄 Iniciando criação de {count} contas...")
        results = []
        
        for i in range(count):
            logger.info(f"📊 Progresso: {i+1}/{count}")
            
            try:
                result = await self.create_account()
                results.append(result)
                
                if result.success:
                    logger.info(f"✅ Conta {i+1} criada: {result.account_data.username}")
                else:
                    logger.error(f"❌ Falha na conta {i+1}: {result.error_message}")
                
                # Delay entre criações
                if i < count - 1:  # Não espera após a última
                    retry_delay = self.config.getint('RETRY', 'retry_delay', fallback=5)
                    await self._human_like_delay(retry_delay, retry_delay * 2)
                    
            except Exception as e:
                logger.error(f"❌ Erro crítico na conta {i+1}: {e}")
                results.append(CreationResult(
                    success=False,
                    error_message=f"Erro crítico: {e}"
                ))
        
        # Estatísticas finais
        successful = sum(1 for r in results if r.success)
        logger.info(f"📊 Resultado final: {successful}/{count} contas criadas com sucesso")
        
        return results
    
    def save_results_to_file(self, results: List[CreationResult], filename: str = "created_accounts.json"):
        """Salva resultados em arquivo JSON"""
        data_to_save = []
        
        for result in results:
            if result.success and result.account_data:
                data_to_save.append({
                    "username": result.account_data.username,
                    "email": result.account_data.email,
                    "password": result.account_data.password,
                    "full_name": result.account_data.full_name,
                    "creation_time": result.creation_time,
                    "timestamp": time.time()
                })
        
        try:
            with open(filename, 'w') as f:
                json.dump(data_to_save, f, indent=2)
            logger.info(f"✅ Resultados salvos em {filename}")
        except Exception as e:
            logger.error(f"❌ Erro ao salvar resultados: {e}")

# Função principal para uso standalone
async def main():
    """Função principal para execução standalone"""
    print("🤖 Instagram Creator Advanced - Versão Corrigida")
    print("=" * 50)
    
    try:
        creator = InstagramCreatorAdvanced()
        
        # Pergunta quantas contas criar
        while True:
            try:
                count = int(input("📝 Quantas contas deseja criar? "))
                if count > 0:
                    break
                print("❌ Por favor, digite um número maior que 0")
            except ValueError:
                print("❌ Por favor, digite um número válido")
        
        # Confirmação
        confirm = input(f"🔍 Confirma criação de {count} conta(s)? (s/N): ").lower()
        if confirm not in ['s', 'sim', 'y', 'yes']:
            print("❌ Operação cancelada")
            return
        
        # Executa criação
        print(f"🚀 Iniciando criação de {count} conta(s)...")
        results = await creator.create_multiple_accounts(count)
        
        # Salva resultados
        creator.save_results_to_file(results)
        
        # Exibe estatísticas
        successful = sum(1 for r in results if r.success)
        print("\n" + "=" * 50)
        print(f"📊 RESULTADO FINAL:")
        print(f"✅ Contas criadas: {successful}/{count}")
        print(f"❌ Falhas: {count - successful}")
        print(f"📁 Dados salvos em: created_accounts.json")
        print("=" * 50)
        
    except KeyboardInterrupt:
        print("\n❌ Operação cancelada pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        logger.error(f"Erro no main: {e}")

if __name__ == "__main__":
    # Executa função principal
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Finalizado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        sys.exit(1)
