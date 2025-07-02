# 📖 Guia de Instalação - Instagram Creator Advanced

## 🎯 Requisitos do Sistema

### Requisitos Mínimos
- **Python:** 3.8 ou superior
- **RAM:** 4GB (recomendado 8GB+)
- **Espaço em disco:** 500MB
- **Conexão:** Internet estável

### Sistemas Operacionais Suportados
- ✅ Windows 10/11
- ✅ macOS 10.15+
- ✅ Linux Ubuntu 18.04+
- ✅ Linux Debian 10+

## 🔧 Instalação Detalhada

### Passo 1: Verificar Python
```bash
# Verificar versão do Python
python --version
# ou
python3 --version

# Deve retornar Python 3.8.0 ou superior
```

### Passo 2: Clonar Repositório
```bash
# Via HTTPS
git clone https://github.com/operatortecnick/nstagram-creator-advanced.git

# Via SSH (se configurado)
git clone git@github.com:operatortecnick/nstagram-creator-advanced.git

# Entrar no diretório
cd nstagram-creator-advanced
```

### Passo 3: Ambiente Virtual (Recomendado)
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Passo 4: Instalar Dependências
```bash
# Instalação básica
pip install -r requirements.txt

# Instalação com extras (desenvolvimento)
pip install -e .[dev]

# Instalação completa
pip install -e .[dev,gui,data]
```

## 🌐 Configuração do Navegador

### Chrome (Recomendado)
O sistema tentará usar o Chrome automaticamente.

**Downloads:**
- [Chrome](https://www.google.com/chrome/)
- [ChromeDriver](https://chromedriver.chromium.org/) (gerenciado automaticamente)

### Firefox (Alternativo)
```python
# Em instagram_creator.py, modifique:
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# Usar FirefoxOptions ao invés de ChromeOptions
```

## ⚙️ Configuração Inicial

### Passo 1: Copiar Configuração
```bash
# Copiar arquivo de configuração padrão
cp config_default.ini config.ini
```

### Passo 2: Editar Configuração
```ini
# Abrir config.ini e ajustar conforme necessário
[BROWSER]
headless = false  # true para modo invisível

[DELAYS]
min_delay = 2     # Ajustar para velocidade desejada
max_delay = 5

[ACCOUNT_GENERATION]
username_prefix = meuuser  # Personalizar prefixo
```

## 🚀 Primeira Execução

### Teste Básico
```bash
# Executar o script principal
python instagram_creator.py

# Seguir as instruções na tela
```

### Teste com Configuração
```python
# Criar arquivo test.py
import asyncio
from instagram_creator import InstagramCreatorAdvanced

async def teste():
    creator = InstagramCreatorAdvanced("config.ini")
    result = await creator.create_account()
    print(f"Resultado: {result.success}")

asyncio.run(teste())
```

## 🔍 Verificação da Instalação

### Script de Verificação
```python
# verificar_instalacao.py
import sys
import importlib

def verificar_dependencias():
    dependencias = [
        'selenium',
        'webdriver_manager',
        'requests',
        'undetected_chromedriver',
        'fake_useragent'
    ]
    
    for dep in dependencias:
        try:
            importlib.import_module(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep} - FALTANDO")

if __name__ == "__main__":
    print(f"Python: {sys.version}")
    print("Verificando dependências:")
    verificar_dependencias()
```

## 🐛 Problemas Comuns

### Erro: ChromeDriver
```bash
# Solução 1: Reinstalar webdriver-manager
pip uninstall webdriver-manager
pip install webdriver-manager

# Solução 2: Download manual
# Baixar ChromeDriver e colocar no PATH
```

### Erro: Selenium
```bash
# Atualizar Selenium
pip install --upgrade selenium
```

### Erro: Permissões
```bash
# Linux/macOS - ajustar permissões
chmod +x instagram_creator.py
```

### Erro: SSL/TLS
```bash
# Atualizar certificados
pip install --upgrade certifi
```

## 📋 Checklist Final

- [ ] Python 3.8+ instalado
- [ ] Repositório clonado
- [ ] Dependências instaladas
- [ ] Chrome/Firefox disponível
- [ ] Configuração criada
- [ ] Teste básico executado
- [ ] Sem erros na verificação

## 💡 Próximos Passos

1. ✅ Ler [Configuração](configuration.md)
2. ✅ Explorar [Exemplos](../examples/)
3. ✅ Consultar [Troubleshooting](troubleshooting.md)

## 🆘 Precisa de Ajuda?

- 📧 Abrir issue no GitHub
- 💬 Consultar discussões
- 📖 Ler documentação completa
