#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instagram Creator Advanced - Versão 2.0
Sistema avançado de criação de contas Instagram com todas as correções aplicadas.

CORREÇÕES PRINCIPAIS:
- ✅ Bug 'text' undefined corrigido
- ✅ Imports organizados
- ✅ Async/await padronizado  
- ✅ Resource leaks eliminados
- ✅ Error handling robusto
- ✅ Configurações seguras por padrão

Autor: operatortecnick
Versão: 2.0.0
Data: 2025-07-02
"""

import asyncio
import random
import time
import logging
import configparser
import json
import os
import sys
from typing import Dict, List, Optional, Tuple, Any
from contextlib import asynccontextmanager
from pathlib import Path

# Selenium imports
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.common.exceptions import (
        TimeoutException, 
        NoSuchElementException, 
        WebDriverException,
        ElementClickInterceptedException
    )
except ImportError as e:
    print(f"❌ Erro de import Selenium: {e}")
    print("📦 Instale com: pip install selenium")
    sys.exit(1)

# WebDriver Manager
try:
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError as e:
    print(f"❌ Erro de import WebDriver Manager: {e}")
    print("📦 Instale com: pip install webdriver-manager")
    sys.exit(1)

# Undetected Chrome (opcional)
try:
    import undetected_chromedriver as uc
    UNDETECTED_AVAILABLE = True
except ImportError:
    UNDETECTED_AVAILABLE = False
    print("⚠️  undetected-chromedriver não instalado (opcional)")

# Requests
try:
    import requests
except ImportError as e:
    print(f"❌ Erro de import Requests: {e}")
    print("📦 Instale com: pip install requests")
    sys.exit(1)


class InstagramCreatorAdvanced:
    """
    Classe principal para criação automatizada de contas Instagram.
    
    Features:
    - ✅ Detecção anti-bot avançada
    - ✅ Rotação de proxies
    - ✅ Randomização de delays
    - ✅ Limpeza automática de recursos
    - ✅ Logging detalhado
    - ✅ Configuração flexível
    """
    
    def __init__(self, config_file: str = "config.ini"):
        """
        Inicializa o Instagram Creator.
        
        Args:
            config_file (str): Caminho para arquivo de configuração
        """
        self.config_file = config_file
        self.driver: Optional[webdriver.Chrome] = None
        self.logger = self._setup_logging()
        self.config = self._load_config()
        self.session_data = {}
        
        # URLs do Instagram
        self.instagram_url = "https://www.instagram.com"
        self.signup_url = f"{self.instagram_url}/accounts/emailsignup/"
        
        # Seletores atualizados (2025)
        self.selectors = {
            "email_input": "input[name='emailOrPhone']",
            "fullname_input": "input[name='fullName']",
            "username_input": "input[name='username']", 
            "password_input": "input[name='password']",
            "signup_button": "button[type='submit']",
            "next_button": "//button[contains(text(), 'Next')]",
            "skip_button": "//button[contains(text(), 'Skip')]",
            "not_now_button": "//button[contains(text(), 'Not Now')]"
        }
        
        self.logger.info("🚀 Instagram Creator Advanced v2.0 inicializado")
    
    def _setup_logging(self) -> logging.Logger:
        """Configura sistema de logging."""
        logger = logging.getLogger('InstagramCreator')
        logger.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # File handler
        file_handler = logging.FileHandler('instagram_creator.log', encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        return logger
    
    def _load_config(self) -> configparser.ConfigParser:
        """Carrega configuração do arquivo."""
        config = configparser.ConfigParser()
        
        if not os.path.exists(self.config_file):
            self.logger.warning(f"⚠️  Arquivo {self.config_file} não encontrado. Usando padrões.")
            return self._create_default_config()
        
        try:
            config.read(self.config_file, encoding='utf-8')
            self.logger.info(f"✅ Configuração carregada: {self.config_file}")
            return config
        except Exception as e:
            self.logger.error(f"❌ Erro ao carregar config: {e}")
            return self._create_default_config()
    
    def _create_default_config(self) -> configparser.ConfigParser:
        """Cria configuração padrão segura."""
        config = configparser.ConfigParser()
        
        # Configurações seguras por padrão
        config['BROWSER'] = {
            'headless': 'false',
            'user_agent': 'auto',
            'window_size': '1366x768',
            'page_load_timeout': '30',
            'implicitly_wait': '10'
        }
        
        config['SECURITY'] = {
            'stealth_mode': 'true',
            'use_proxy': 'false',
            'proxy_rotation': 'false'
        }
        
        config['DELAYS'] = {
            'min_delay': '3',
            'max_delay': '7',
            'typing_delay': '0.1'
        }
        
        config['RETRY'] = {
            'max_retries': '3',
            'timeout_seconds': '30'
        }
        
        config['LOGGING'] = {
            'log_level': 'INFO',
            'save_screenshots': 'true'
        }
        
        return config
    
    async def _random_delay(self, min_delay: Optional[float] = None, max_delay: Optional[float] = None):
        """
        Aplica delay aleatório para simular comportamento humano.
        
        Args:
            min_delay: Delay mínimo (segundos)
            max_delay: Delay máximo (segundos)
        """
        if min_delay is None:
            min_delay = float(self.config.get('DELAYS', 'min_delay', fallback='3'))
        if max_delay is None:
            max_delay = float(self.config.get('DELAYS', 'max_delay', fallback='7'))
        
        delay = random.uniform(min_delay, max_delay)
        self.logger.debug(f"⏱️  Aguardando {delay:.2f}s...")
        await asyncio.sleep(delay)
    
    def _get_chrome_options(self) -> Options:
        """Configura opções do Chrome para evitar detecção."""
        options = Options()
        
        # Configurações anti-detecção
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Disable logging
        options.add_argument("--disable-logging")
        options.add_argument("--log-level=3")
        options.add_argument("--disable-extensions")
        
        # Performance
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-software-rasterizer")
        
        # User agent
        user_agent = self.config.get('BROWSER', 'user_agent', fallback='auto')
        if user_agent != 'auto':
            options.add_argument(f"--user-agent={user_agent}")
        
        # Headless mode
        if self.config.getboolean('BROWSER', 'headless', fallback=False):
            options.add_argument("--headless")
        
        # Window size
        window_size = self.config.get('BROWSER', 'window_size', fallback='1366x768')
        options.add_argument(f"--window-size={window_size}")
        
        # Proxy (se configurado)
        if self.config.getboolean('SECURITY', 'use_proxy', fallback=False):
            proxy = self._get_proxy()
            if proxy:
                options.add_argument(f"--proxy-server={proxy}")
        
        return options
    
    def _get_proxy(self) -> Optional[str]:
        """Obtém proxy da lista configurada."""
        try:
            proxy_file = self.config.get('SECURITY', 'proxy_list', fallback='proxies.txt')
            if os.path.exists(proxy_file):
                with open(proxy_file, 'r') as f:
                    proxies = [line.strip() for line in f if line.strip()]
                if proxies:
                    return random.choice(proxies)
        except Exception as e:
            self.logger.warning(f"⚠️  Erro ao carregar proxy: {e}")
        return None
    
    async def _setup_driver(self):
        """Configura e inicializa o driver do Chrome."""
        try:
            options = self._get_chrome_options()
            
            # Tenta usar undetected-chromedriver se disponível
            if UNDETECTED_AVAILABLE and self.config.getboolean('SECURITY', 'stealth_mode', fallback=True):
                self.logger.info("🥷 Usando undetected-chromedriver")
                self.driver = uc.Chrome(options=options)
            else:
                # WebDriver padrão
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=options)
            
            # Configurações de timeout
            page_timeout = int(self.config.get('BROWSER', 'page_load_timeout', fallback='30'))
            implicit_wait = int(self.config.get('BROWSER', 'implicitly_wait', fallback='10'))
            
            self.driver.set_page_load_timeout(page_timeout)
            self.driver.implicitly_wait(implicit_wait)
            
            # Remove automation flags
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.logger.info("✅ Driver configurado com sucesso")
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao configurar driver: {e}")
            raise
    
    async def _cleanup_driver(self):
        """Limpa recursos do driver."""
        if self.driver:
            try:
                self.driver.quit()
                self.logger.info("🧹 Driver encerrado com sucesso")
            except Exception as e:
                self.logger.warning(f"⚠️  Erro ao encerrar driver: {e}")
            finally:
                self.driver = None
    
    @asynccontextmanager
    async def _browser_context(self):
        """Context manager para garantir limpeza do browser."""
        try:
            await self._setup_driver()
            yield self.driver
        finally:
            await self._cleanup_driver()
    
    async def _type_like_human(self, element, text: str):
        """
        Digita texto simulando comportamento humano.
        
        Args:
            element: Elemento do Selenium
            text: Texto para digitar
        """
        typing_delay = float(self.config.get('DELAYS', 'typing_delay', fallback='0.1'))
        
        for char in text:
            element.send_keys(char)
            if random.random() < 0.1:  # 10% chance de pausa extra
                await asyncio.sleep(random.uniform(0.1, 0.3))
            await asyncio.sleep(typing_delay)
    
    async def _safe_find_element(self, by: By, selector: str, timeout: int = 10) -> Optional[Any]:
        """
        Encontra elemento de forma segura com retry.
        
        Args:
            by: Tipo de seletor (By.CSS_SELECTOR, By.XPATH, etc.)
            selector: Seletor do elemento
            timeout: Timeout em segundos
            
        Returns:
            Elemento encontrado ou None
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.presence_of_element_located((by, selector)))
            return element
        except TimeoutException:
            self.logger.warning(f"⚠️  Elemento não encontrado: {selector}")
            return None
        except Exception as e:
            self.logger.error(f"❌ Erro ao buscar elemento {selector}: {e}")
            return None
    
    async def _safe_click(self, element) -> bool:
        """
        Clica em elemento de forma segura.
        
        Args:
            element: Elemento para clicar
            
        Returns:
            True se clicou com sucesso, False caso contrário
        """
        try:
            # Scroll para elemento
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            await asyncio.sleep(0.5)
            
            # Tenta click normal
            element.click()
            return True
            
        except ElementClickInterceptedException:
            try:
                # Tenta JavaScript click
                self.driver.execute_script("arguments[0].click();", element)
                return True
            except Exception as e:
                self.logger.error(f"❌ Erro ao clicar: {e}")
                return False
        except Exception as e:
            self.logger.error(f"❌ Erro ao clicar: {e}")
            return False
    
    async def _take_screenshot(self, filename: str):
        """Tira screenshot para debug."""
        if self.config.getboolean('LOGGING', 'save_screenshots', fallback=True):
            try:
                screenshot_path = f"screenshots/{filename}"
                os.makedirs("screenshots", exist_ok=True)
                self.driver.save_screenshot(screenshot_path)
                self.logger.info(f"📸 Screenshot salva: {screenshot_path}")
            except Exception as e:
                self.logger.warning(f"⚠️  Erro ao salvar screenshot: {e}")
    
    async def navigate_to_signup(self) -> bool:
        """
        Navega para página de cadastro do Instagram.
        
        Returns:
            True se navegou com sucesso, False caso contrário
        """
        try:
            self.logger.info("🌐 Navegando para página de cadastro...")
            self.driver.get(self.signup_url)
            await self._random_delay(2, 4)
            
            # Verifica se carregou corretamente
            if "instagram.com" in self.driver.current_url:
                self.logger.info("✅ Página de cadastro carregada")
                await self._take_screenshot("signup_page.png")
                return True
            else:
                self.logger.error("❌ Falha ao carregar página de cadastro")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao navegar para cadastro: {e}")
            return False
    
    async def create_account(self, account_data: Dict[str, str]) -> bool:
        """
        Cria uma conta do Instagram.
        
        Args:
            account_data: Dicionário com dados da conta:
                {
                    'email': 'email@exemplo.com',
                    'full_name': 'Nome Completo', 
                    'username': 'usuario123',
                    'password': 'senha123'
                }
        
        Returns:
            True se criou com sucesso, False caso contrário
        """
        # Validação dos dados
        required_fields = ['email', 'full_name', 'username', 'password']
        for field in required_fields:
            if field not in account_data or not account_data[field]:
                self.logger.error(f"❌ Campo obrigatório ausente: {field}")
                return False
        
        self.logger.info(f"👤 Iniciando criação da conta: {account_data['username']}")
        
        async with self._browser_context():
            try:
                # Navegar para página de cadastro
                if not await self.navigate_to_signup():
                    return False
                
                # Preencher email
                email_input = await self._safe_find_element(By.CSS_SELECTOR, self.selectors['email_input'])
                if not email_input:
                    self.logger.error("❌ Campo email não encontrado")
                    return False
                
                await self._type_like_human(email_input, account_data['email'])
                await self._random_delay(1, 2)
                
                # Preencher nome completo  
                fullname_input = await self._safe_find_element(By.CSS_SELECTOR, self.selectors['fullname_input'])
                if not fullname_input:
                    self.logger.error("❌ Campo nome completo não encontrado")
                    return False
                
                await self._type_like_human(fullname_input, account_data['full_name'])
                await self._random_delay(1, 2)
                
                # Preencher username
                username_input = await self._safe_find_element(By.CSS_SELECTOR, self.selectors['username_input'])
                if not username_input:
                    self.logger.error("❌ Campo username não encontrado")
                    return False
                
                await self._type_like_human(username_input, account_data['username'])
                await self._random_delay(1, 2)
                
                # Preencher senha
                password_input = await self._safe_find_element(By.CSS_SELECTOR, self.selectors['password_input'])
                if not password_input:
                    self.logger.error("❌ Campo senha não encontrado")
                    return False
                
                await self._type_like_human(password_input, account_data['password'])
                await self._random_delay(2, 4)
                
                # Screenshot antes de submeter
                await self._take_screenshot("before_submit.png")
                
                # Clicar no botão de cadastro
                signup_button = await self._safe_find_element(By.CSS_SELECTOR, self.selectors['signup_button'])
                if not signup_button:
                    self.logger.error("❌ Botão de cadastro não encontrado")
                    return False
                
                if not await self._safe_click(signup_button):
                    self.logger.error("❌ Falha ao clicar no botão de cadastro")
                    return False
                
                self.logger.info("✅ Formulário submetido")
                await self._random_delay(3, 6)
                
                # Verificar se cadastro foi bem-sucedido
                current_url = self.driver.current_url
                if "challenge" in current_url or "accounts/emailsignup" not in current_url:
                    self.logger.info("✅ Cadastro realizado com sucesso!")
                    await self._take_screenshot("signup_success.png")
                    
                    # Salvar dados da sessão
                    self.session_data = {
                        'username': account_data['username'],
                        'email': account_data['email'],
                        'created_at': time.time(),
                        'status': 'created'
                    }
                    
                    return True
                else:
                    self.logger.warning("⚠️  Possível erro no cadastro ou captcha")
                    await self._take_screenshot("signup_error.png")
                    return False
                
            except Exception as e:
                self.logger.error(f"❌ Erro durante criação da conta: {e}")
                await self._take_screenshot("error_during_creation.png")
                return False
    
    async def create_multiple_accounts(self, accounts_data: List[Dict[str, str]]) -> Dict[str, bool]:
        """
        Cria múltiplas contas.
        
        Args:
            accounts_data: Lista de dados das contas
            
        Returns:
            Dicionário com resultado para cada conta
        """
        results = {}
        
        for i, account_data in enumerate(accounts_data):
            username = account_data.get('username', f'conta_{i}')
            self.logger.info(f"📋 Processando conta {i+1}/{len(accounts_data)}: {username}")
            
            try:
                result = await self.create_account(account_data)
                results[username] = result
                
                if result:
                    self.logger.info(f"✅ Conta {username} criada com sucesso!")
                else:
                    self.logger.error(f"❌ Falha ao criar conta {username}")
                
                # Delay entre contas
                if i < len(accounts_data) - 1:  # Não delay na última conta
                    delay = random.uniform(30, 60)  # 30-60s entre contas
                    self.logger.info(f"⏱️  Aguardando {delay:.1f}s antes da próxima conta...")
                    await asyncio.sleep(delay)
                    
            except Exception as e:
                self.logger.error(f"❌ Erro ao processar conta {username}: {e}")
                results[username] = False
        
        # Relatório final
        successful = sum(1 for result in results.values() if result)
        total = len(results)
        self.logger.info(f"📊 Relatório final: {successful}/{total} contas criadas com sucesso")
        
        return results
    
    def save_session_data(self, filename: str = "session_data.json"):
        """Salva dados da sessão."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.session_data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"💾 Dados da sessão salvos: {filename}")
        except Exception as e:
            self.logger.error(f"❌ Erro ao salvar dados da sessão: {e}")


# Funções utilitárias
def generate_username(base_name: str) -> str:
    """Gera username único com números aleatórios."""
    suffix = random.randint(1000, 9999)
    return f"{base_name}_{suffix}"

def generate_email(username: str, domain: str = "tempmail.com") -> str:
    """Gera email baseado no username."""
    return f"{username}@{domain}"

def validate_account_data(account_data: Dict[str, str]) -> Tuple[bool, List[str]]:
    """
    Valida dados da conta.
    
    Returns:
        (is_valid, error_messages)
    """
    errors = []
    
    # Verificar campos obrigatórios
    required_fields = ['email', 'full_name', 'username', 'password']
    for field in required_fields:
        if field not in account_data or not account_data[field]:
            errors.append(f"Campo '{field}' é obrigatório")
    
    # Validar email
    email = account_data.get('email', '')
    if email and '@' not in email:
        errors.append("Email inválido")
    
    # Validar username
    username = account_data.get('username', '')
    if username and (len(username) < 3 or len(username) > 30):
        errors.append("Username deve ter entre 3 e 30 caracteres")
    
    # Validar senha
    password = account_data.get('password', '')
    if password and len(password) < 6:
        errors.append("Senha deve ter pelo menos 6 caracteres")
    
    return len(errors) == 0, errors


# Exemplo de uso
async def main():
    """Exemplo de uso da classe."""
    # Dados da conta de exemplo
    account_data = {
        'email': 'exemplo@tempmail.com',
        'full_name': 'João Silva',
        'username': 'joao_silva_2025',
        'password': 'senha123456'
    }
    
    # Validar dados
    is_valid, errors = validate_account_data(account_data)
    if not is_valid:
        print("❌ Dados inválidos:")
        for error in errors:
            print(f"  - {error}")
        return
    
    # Criar instância
    creator = InstagramCreatorAdvanced()
    
    try:
        # Criar conta
        success = await creator.create_account(account_data)
        
        if success:
            print("🎉 Conta criada com sucesso!")
            creator.save_session_data()
        else:
            print("❌ Falha ao criar conta")
            
    except KeyboardInterrupt:
        print("\n⚠️  Operação cancelada pelo usuário")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")


if __name__ == "__main__":
    # Executar exemplo
    asyncio.run(main())
