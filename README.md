# 🤖 Instagram Creator Advanced

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Stable-brightgreen.svg)

## 📋 Descrição

**Sistema avançado de criação de contas Instagram** - Versão 2.0 corrigida e otimizada com todas as melhorias de segurança, estabilidade e performance.

### 🎯 **Principais Correções Implementadas:**

- ✅ **Bug `text` undefined** → **CORRIGIDO**
- ✅ **Imports organizados** → **Dependências gerenciadas adequadamente**
- ✅ **Async/await padronizado** → **Fluxo assíncrono consistente**
- ✅ **Resource leaks eliminados** → **Cleanup automático de recursos**
- ✅ **Error handling robusto** → **Tratamento de erros abrangente**
- ✅ **Configurações seguras** → **Padrões seguros por padrão**

## 🚀 Funcionalidades

- 🔧 **Criação automatizada** de contas Instagram
- 🛡️ **Modo stealth** com undetected-chromedriver
- 🎭 **User agents aleatórios** para evitar detecção
- ⏱️ **Delays humanizados** para simular comportamento real
- 📊 **Criação em lote** com relatórios detalhados
- 🔐 **Configurações seguras** por padrão
- 📝 **Logs detalhados** para debugging
- 🔄 **Sistema de retry** inteligente
- 💾 **Salvamento automático** de resultados

## 📦 Instalação

### Método 1: Instalação Rápida
```bash
# Clone o repositório
git clone https://github.com/operatortecnick/nstagram-creator-advanced.git
cd nstagram-creator-advanced

# Instale dependências
pip install -r requirements.txt

# Execute
python instagram_creator.py
```

### Método 2: Instalação Completa
```bash
# Instalação do pacote
python setup.py install

# Ou usando pip
pip install -e .

# Execute via command line
instagram-creator
```

## ⚡ Uso Rápido

### Uso Básico
```python
import asyncio
from instagram_creator import InstagramCreatorAdvanced

async def exemplo_basico():
    creator = InstagramCreatorAdvanced()
    
    # Cria uma conta
    result = await creator.create_account()
    
    if result.success:
        print(f"✅ Conta criada: {result.account_data.username}")
    else:
        print(f"❌ Erro: {result.error_message}")

asyncio.run(exemplo_basico())
```

### Criação em Lote
```python
async def exemplo_lote():
    creator = InstagramCreatorAdvanced()
    
    # Cria 5 contas
    results = await creator.create_multiple_accounts(5)
    
    # Salva resultados
    creator.save_results_to_file(results, "minhas_contas.json")

asyncio.run(exemplo_lote())
```

## 🔧 Configuração

O arquivo `config_default.ini` contém todas as configurações:

```ini
[BROWSER]
headless = false
window_size = 1920,1080

[DELAYS]
min_delay = 2
max_delay = 5
typing_delay = 0.1

[SECURITY]
stealth_mode = true
use_proxy = false

[ACCOUNT_GENERATION]
username_prefix = user
email_domain = @gmail.com
password_length = 12
```

## 📚 Documentação Completa

- 📖 [Guia de Instalação](docs/installation.md)
- ⚙️ [Referência de Configuração](docs/configuration.md)
- 🛠️ [Solução de Problemas](docs/troubleshooting.md)
- 💡 [Exemplos Avançados](examples/)

## 🔒 Segurança

Este projeto implementa várias camadas de segurança:

- 🛡️ **Stealth mode** por padrão
- 🎭 **User agents rotativos**
- ⏱️ **Delays humanizados**
- 🚫 **Anti-detecção** avançada
- 🔐 **Configurações seguras**

## ⚠️ Avisos Importantes

1. **Use responsavelmente** - Respeite os termos de uso do Instagram
2. **Para fins educacionais** - Não use para spam ou atividades maliciosas
3. **Rate limiting** - O Instagram pode detectar automação excessiva
4. **Proxies recomendados** - Para uso em escala

## 🐛 Problemas Conhecidos e Soluções

### ❌ Erro: `text` is not defined
**Status:** ✅ **CORRIGIDO** na versão 2.0

### ❌ Imports inconsistentes
**Status:** ✅ **CORRIGIDO** - Todos os imports organizados

### ❌ Resource leaks
**Status:** ✅ **CORRIGIDO** - Context managers implementados

## 🤝 Contribuição

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).

## 📞 Suporte

- 📧 **Issues:** [GitHub Issues](https://github.com/operatortecnick/nstagram-creator-advanced/issues)
- 💬 **Discussões:** [GitHub Discussions](https://github.com/operatortecnick/nstagram-creator-advanced/discussions)

## 🙏 Agradecimentos

- Comunidade Selenium
- Desenvolvedores do undetected-chromedriver
- Contribuidores do projeto

---

⭐ **Se este projeto foi útil, deixe uma estrela!** ⭐nstagram-creator-advanced
Sistema avançado de criação de contas Instagram - Versão corrigida e otimizada
