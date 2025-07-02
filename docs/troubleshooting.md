# 🛠️ Solução de Problemas - Instagram Creator Advanced

## 🚨 Problemas Mais Comuns

### ❌ Erro: `text` is not defined
**Status:** ✅ **CORRIGIDO** na versão 2.0

**Sintoma:**
```
NameError: name 'text' is not defined
```

**Solução:**
- ✅ Já corrigido no código principal
- ✅ Use a versão 2.0+ do repositório

---

### ❌ Erro: Import não encontrado
**Sintomas:**
```
ImportError: No module named 'selenium'
ModuleNotFoundError: No module named 'undetected_chromedriver'
```

**Soluções:**
```bash
# Reinstalar dependências
pip install -r requirements.txt

# Instalar dependências uma por uma
pip install selenium webdriver-manager requests

# Atualizar pip
pip install --upgrade pip
```

---

### ❌ ChromeDriver não funciona
**Sintomas:**
```
selenium.common.exceptions.WebDriverException: 'chromedriver' executable needs to be in PATH
```

**Soluções:**
```bash
# Solução 1: Reinstalar webdriver-manager
pip uninstall webdriver-manager
pip install webdriver-manager

# Solução 2: Download manual
# 1. Verificar versão do Chrome: chrome://version/
# 2. Baixar ChromeDriver compatível
# 3. Adicionar ao PATH do sistema
```

**Código de verificação:**
```python
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

try:
    driver = webdriver.Chrome(ChromeDriverManager().install())
    print("✅ ChromeDriver funcionando")
    driver.quit()
except Exception as e:
    print(f"❌ Erro: {e}")
```

---

### ❌ Instagram detecta automação
**Sintomas:**
- Captcha aparece
- Conta bloqueada imediatamente
- "Suspicious activity" detectado

**Soluções:**
```ini
# Configurar delays maiores
[DELAYS]
min_delay = 5
max_delay = 10

# Ativar modo stealth
[SECURITY]
stealth_mode = true

# Usar proxies
use_proxy = true
proxy_list = proxies.txt
```

**Código adicional:**
```python
# Adicionar mais randomização
import random
import time

async def extra_delay():
    # Delay extra aleatório
    extra = random.uniform(2, 8)
    await asyncio.sleep(extra)
```

---

### ❌ Timeout Errors
**Sintomas:**
```
selenium.common.exceptions.TimeoutException
```

**Soluções:**
```ini
# Aumentar timeouts
[RETRY]
timeout_seconds = 60

[BROWSER]
page_load_timeout = 60
implicitly_wait = 20
```

**Debug:**
```python
# Verificar se elemento existe
try:
    element = driver.find_element(By.CSS_SELECTOR, "input[name='email']")
    print("✅ Elemento encontrado")
except NoSuchElementException:
    print("❌ Elemento não encontrado")
    # Tirar screenshot para debug
    driver.save_screenshot("debug.png")
```

---

### ❌ Seletores desatualizados
**Sintoma:**
```
NoSuchElementException: Unable to locate element
```

**Diagnóstico:**
```python
# Script para verificar seletores
def verificar_seletores():
    selectors = {
        "email": "input[name='emailOrPhone']",
        "username": "input[name='username']",
        "password": "input[name='password']"
    }
    
    for name, selector in selectors.items():
        try:
            element = driver.find_element(By.CSS_SELECTOR, selector)
            print(f"✅ {name}: OK")
        except:
            print(f"❌ {name}: FAILED - {selector}")
```

**Atualizações comuns:**
- Instagram muda seletores frequentemente
- Verificar inspetor de elementos (F12)
- Usar XPath como alternativa

---

### ❌ Resource Leaks / Memory
**Sintomas:**
- Script fica lento
- Muitos processos Chrome
- Erro de memória

**Solução:** ✅ **CORRIGIDO** com context managers
```python
# Uso correto (já implementado)
async with self._browser_context():
    # Operações do navegador
    pass
# Driver é fechado automaticamente
```

**Verificação manual:**
```python
# Sempre fechar driver
try:
    # Operações
    pass
finally:
    if driver:
        driver.quit()
```

---

## 🔧 Debugging Avançado

### 1. Modo Debug Completo
```ini
[LOGGING]
log_level = DEBUG
save_screenshots = true

[BROWSER]
headless = false

[ADVANCED]
auto_cleanup = false
```

### 2. Script de Debug
```python
import logging
import asyncio
from instagram_creator import InstagramCreatorAdvanced

# Configurar logging detalhado
logging.basicConfig(level=logging.DEBUG)

async def debug_test():
    creator = InstagramCreatorAdvanced()
    
    # Teste apenas setup do driver
    try:
        await creator._setup_driver()
        print("✅ Driver OK")
        
        # Navegar para Instagram
        creator.driver.get("https://www.instagram.com")
        print("✅ Navegação OK")
        
        # Tirar screenshot
        creator.driver.save_screenshot("debug_instagram.png")
        print("✅ Screenshot salva")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        await creator._cleanup_driver()

asyncio.run(debug_test())
```

### 3. Verificação de Dependências
```python
import sys
import pkg_resources

def verificar_versoes():
    dependencias = [
        'selenium',
        'webdriver-manager', 
        'requests',
        'undetected-chromedriver'
    ]
    
    print(f"Python: {sys.version}")
    print("-" * 40)
    
    for dep in dependencias:
        try:
            version = pkg_resources.get_distribution(dep).version
            print(f"✅ {dep}: {version}")
        except pkg_resources.DistributionNotFound:
            print(f"❌ {dep}: NÃO INSTALADO")

verificar_versoes()
```

## 🌐 Problemas de Rede

### Conexão Lenta
```ini
[BROWSER]
page_load_timeout = 90
implicitly_wait = 30

[DELAYS]
min_delay = 5
max_delay = 12
```

### Proxy Issues
```python
# Testar proxy
import requests

def testar_proxy(proxy_url):
    try:
        response = requests.get(
            "http://httpbin.org/ip", 
            proxies={"http": proxy_url},
            timeout=10
        )
        print(f"✅ Proxy OK: {response.json()}")
    except Exception as e:
        print(f"❌ Proxy falhou: {e}")

# Teste
testar_proxy("http://proxy:port")
```

## 🔒 Problemas de Segurança

### Captcha Frequente
**Soluções:**
1. Diminuir velocidade
2. Usar proxies rotativos
3. Intervalos maiores entre contas
4. User agents variados

### Rate Limiting
```python
# Implementar backoff exponencial
import time

async def backoff_delay(attempt):
    delay = min(300, (2 ** attempt) + random.uniform(0, 1))
    await asyncio.sleep(delay)
```

## 📋 Checklist de Troubleshooting

### Antes de Reportar Bug
- [ ] Python 3.8+ instalado
- [ ] Dependências atualizadas
- [ ] Chrome/ChromeDriver funcionando
- [ ] Configuração válida
- [ ] Logs coletados
- [ ] Screenshots (se relevante)

### Informações para Bug Report
1. **Versão do Python:** `python --version`
2. **Sistema operacional:** Windows/macOS/Linux
3. **Versões das dependências:** `pip list`
4. **Configuração usada:** `config.ini`
5. **Logs completos:** `instagram_creator.log`
6. **Passos para reproduzir**

## 🆘 Ainda com Problemas?

### Recursos Adicionais
- 📖 [Documentação Selenium](https://selenium-python.readthedocs.io/)
- 🌐 [ChromeDriver Downloads](https://chromedriver.chromium.org/)
- 💬 [Stack Overflow](https://stackoverflow.com/questions/tagged/selenium)

### Contato
- 📧 Abrir issue no GitHub com detalhes completos
- 💬 Usar GitHub Discussions para dúvidas
- 📝 Incluir logs e configuração

---

**💡 Dica:** A maioria dos problemas são resolvidos com dependências atualizadas e configuração adequada!
