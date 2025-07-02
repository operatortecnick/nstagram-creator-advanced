# ⚙️ Referência de Configuração - Instagram Creator Advanced

## 📋 Visão Geral

O arquivo `config.ini` controla todos os aspectos do comportamento do Instagram Creator. Esta referência documenta todas as opções disponíveis.

## 🌐 [BROWSER] - Configurações do Navegador

### `headless`
- **Tipo:** boolean
- **Padrão:** `false`
- **Descrição:** Executa navegador em modo invisível
```ini
headless = false  # Mostra janela do navegador
headless = true   # Modo invisível
```

### `window_size`
- **Tipo:** string
- **Padrão:** `1920,1080`
- **Descrição:** Tamanho da janela do navegador
```ini
window_size = 1920,1080  # Full HD
window_size = 1366,768   # Laptop padrão
window_size = 1280,720   # HD
```

### `user_agent`
- **Tipo:** string
- **Padrão:** (vazio - usa aleatório)
- **Descrição:** User agent personalizado
```ini
user_agent =  # Usa aleatório
user_agent = Mozilla/5.0 (Windows NT 10.0; Win64; x64)...  # Fixo
```

### `implicitly_wait`
- **Tipo:** integer
- **Padrão:** `10`
- **Descrição:** Tempo de espera implícita (segundos)
```ini
implicitly_wait = 10  # Espera padrão
implicitly_wait = 5   # Mais rápido
implicitly_wait = 20  # Mais tolerante
```

### `page_load_timeout`
- **Tipo:** integer
- **Padrão:** `30`
- **Descrição:** Timeout para carregamento de páginas
```ini
page_load_timeout = 30  # Padrão
page_load_timeout = 60  # Para conexões lentas
```

## ⏱️ [DELAYS] - Configurações de Timing

### `min_delay` / `max_delay`
- **Tipo:** float
- **Padrão:** `2` / `5`
- **Descrição:** Range de delays entre ações
```ini
min_delay = 2    # Mínimo 2 segundos
max_delay = 5    # Máximo 5 segundos

# Para ser mais rápido (CUIDADO!)
min_delay = 1
max_delay = 3

# Para ser mais cauteloso
min_delay = 3
max_delay = 8
```

### `typing_delay`
- **Tipo:** float
- **Padrão:** `0.1`
- **Descrição:** Delay entre teclas digitadas
```ini
typing_delay = 0.1   # Digitação normal
typing_delay = 0.05  # Mais rápida
typing_delay = 0.2   # Mais lenta/humana
```

### `form_submission_delay`
- **Tipo:** float
- **Padrão:** `3`
- **Descrição:** Delay antes de enviar formulários
```ini
form_submission_delay = 3  # Padrão
form_submission_delay = 5  # Mais cauteloso
```

## 🛡️ [SECURITY] - Configurações de Segurança

### `stealth_mode`
- **Tipo:** boolean
- **Padrão:** `true`
- **Descrição:** Ativa modo stealth anti-detecção
```ini
stealth_mode = true   # Recomendado
stealth_mode = false  # Apenas para debug
```

### `use_proxy`
- **Tipo:** boolean
- **Padrão:** `false`
- **Descrição:** Ativa uso de proxies
```ini
use_proxy = false  # Sem proxy
use_proxy = true   # Com proxy (configurar proxy_list)
```

### `proxy_list`
- **Tipo:** string (path)
- **Padrão:** (vazio)
- **Descrição:** Arquivo com lista de proxies
```ini
proxy_list = proxies.txt
# Formato do arquivo:
# http://proxy1:port
# http://user:pass@proxy2:port
# socks5://proxy3:port
```

### `rotation_enabled`
- **Tipo:** boolean
- **Padrão:** `false`
- **Descrição:** Rotaciona proxies automaticamente
```ini
rotation_enabled = false  # Usa mesmo proxy
rotation_enabled = true   # Rotaciona a cada conta
```

## 👤 [ACCOUNT_GENERATION] - Geração de Contas

### `username_prefix`
- **Tipo:** string
- **Padrão:** `user`
- **Descrição:** Prefixo para usernames gerados
```ini
username_prefix = user      # user_abc123
username_prefix = mybot     # mybot_abc123
username_prefix = test      # test_abc123
```

### `email_domain`
- **Tipo:** string
- **Padrão:** `@gmail.com`
- **Descrição:** Domínio para emails gerados
```ini
email_domain = @gmail.com     # Gmail
email_domain = @yahoo.com     # Yahoo
email_domain = @outlook.com   # Outlook
email_domain = @tempmail.org  # Temporário
```

### `password_length`
- **Tipo:** integer
- **Padrão:** `12`
- **Descrição:** Comprimento das senhas geradas
```ini
password_length = 12  # Padrão seguro
password_length = 8   # Mínimo
password_length = 16  # Extra seguro
```

### `include_symbols`
- **Tipo:** boolean
- **Padrão:** `true`
- **Descrição:** Inclui símbolos nas senhas
```ini
include_symbols = true   # Abc123!@#
include_symbols = false  # Abc123456
```

## 🔄 [RETRY] - Configurações de Retry

### `max_attempts`
- **Tipo:** integer
- **Padrão:** `3`
- **Descrição:** Tentativas máximas por operação
```ini
max_attempts = 3  # Padrão
max_attempts = 1  # Sem retry
max_attempts = 5  # Mais persistente
```

### `retry_delay`
- **Tipo:** integer
- **Padrão:** `5`
- **Descrição:** Delay entre tentativas (segundos)
```ini
retry_delay = 5   # Padrão
retry_delay = 10  # Mais conservador
retry_delay = 2   # Mais rápido
```

### `timeout_seconds`
- **Tipo:** integer
- **Padrão:** `30`
- **Descrição:** Timeout para WebDriverWait
```ini
timeout_seconds = 30  # Padrão
timeout_seconds = 60  # Para sites lentos
timeout_seconds = 15  # Para testes rápidos
```

## 📝 [LOGGING] - Configurações de Log

### `log_level`
- **Tipo:** string
- **Padrão:** `INFO`
- **Descrição:** Nível de log
```ini
log_level = INFO     # Informações gerais
log_level = DEBUG    # Detalhes completos
log_level = WARNING  # Apenas avisos
log_level = ERROR    # Apenas erros
```

### `log_file`
- **Tipo:** string
- **Padrão:** `instagram_creator.log`
- **Descrição:** Arquivo de log
```ini
log_file = instagram_creator.log
log_file = logs/app.log
log_file = /var/log/instagram.log
```

### `console_output`
- **Tipo:** boolean
- **Padrão:** `true`
- **Descrição:** Mostra logs no console
```ini
console_output = true   # Mostra no terminal
console_output = false  # Apenas arquivo
```

## 🔬 [ADVANCED] - Configurações Avançadas

### `batch_size`
- **Tipo:** integer
- **Padrão:** `1`
- **Descrição:** Contas processadas por vez
```ini
batch_size = 1   # Uma por vez (recomendado)
batch_size = 5   # Cinco por vez (cuidado!)
```

### `concurrent_sessions`
- **Tipo:** integer
- **Padrão:** `1`
- **Descrição:** Sessões simultâneas do navegador
```ini
concurrent_sessions = 1  # Recomendado
concurrent_sessions = 2  # Experimental
```

### `save_screenshots`
- **Tipo:** boolean
- **Padrão:** `false`
- **Descrição:** Salva screenshots para debug
```ini
save_screenshots = false  # Normal
save_screenshots = true   # Para debugging
```

### `auto_cleanup`
- **Tipo:** boolean
- **Padrão:** `true`
- **Descrição:** Limpeza automática de recursos
```ini
auto_cleanup = true   # Recomendado
auto_cleanup = false  # Manual (debug)
```

## 📋 Exemplos de Configuração

### Configuração Rápida
```ini
[DELAYS]
min_delay = 1
max_delay = 2
typing_delay = 0.05

[BROWSER]
headless = true
```

### Configuração Stealth
```ini
[SECURITY]
stealth_mode = true
use_proxy = true
proxy_list = proxies.txt

[DELAYS]
min_delay = 3
max_delay = 8
```

### Configuração Debug
```ini
[LOGGING]
log_level = DEBUG
save_screenshots = true

[BROWSER]
headless = false

[ADVANCED]
auto_cleanup = false
```

## ⚠️ Recomendações

### Para Produção
- ✅ `stealth_mode = true`
- ✅ `headless = true`
- ✅ `use_proxy = true`
- ✅ `min_delay >= 2`

### Para Desenvolvimento
- ✅ `headless = false`
- ✅ `log_level = DEBUG`
- ✅ `save_screenshots = true`
- ✅ `auto_cleanup = false`

### Para Performance
- ⚠️ `min_delay = 1` (cuidado)
- ✅ `headless = true`
- ✅ `concurrent_sessions = 1`
- ✅ `batch_size = 1`
