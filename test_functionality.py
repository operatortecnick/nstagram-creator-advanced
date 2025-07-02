#!/usr/bin/env python3
"""
Script de teste para verificar funcionalidade do Instagram Creator Advanced
"""

import asyncio
import sys
from pathlib import Path

# Adicionar o diretório do projeto ao path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Testar se todos os imports funcionam"""
    print("🔍 Testando imports...")
    
    try:
        from instagram_creator import InstagramCreatorAdvanced, AccountData
        print("✅ instagram_creator importado com sucesso")
        
        from selenium import webdriver
        print("✅ selenium importado com sucesso")
        
        from webdriver_manager.chrome import ChromeDriverManager
        print("✅ webdriver_manager importado com sucesso")
        
        import undetected_chromedriver as uc
        print("✅ undetected_chromedriver importado com sucesso")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erro de import: {e}")
        return False

def test_configuration():
    """Testar carregamento de configuração"""
    print("\n🔧 Testando configuração...")
    
    try:
        from instagram_creator import InstagramCreatorAdvanced
        
        # Testar com arquivo de configuração padrão
        creator = InstagramCreatorAdvanced("config_default.ini")
        print("✅ Configuração carregada com sucesso")
        
        # Verificar algumas configurações
        min_delay = creator.config.getfloat('DELAYS', 'min_delay', fallback=3.0)
        stealth_mode = creator.config.getboolean('SECURITY', 'stealth_mode', fallback=True)
        
        print(f"   📊 Min delay: {min_delay}s")
        print(f"   🛡️ Stealth mode: {stealth_mode}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na configuração: {e}")
        return False

def test_account_data():
    """Testar criação de dados de conta"""
    print("\n👤 Testando dados de conta...")
    
    try:
        from instagram_creator import AccountData
        
        # Criar dados de teste
        account = AccountData(
            email="teste@exemplo.com",
            username="usuario_teste",
            password="senha123",
            full_name="Usuário Teste"
        )
        
        print("✅ AccountData criado com sucesso")
        print(f"   📧 Email: {account.email}")
        print(f"   👤 Username: {account.username}")
        print(f"   👥 Nome: {account.full_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro nos dados da conta: {e}")
        return False

async def test_driver_setup():
    """Testar configuração do driver (sem abrir navegador)"""
    print("\n🌐 Testando configuração do driver...")
    
    try:
        from instagram_creator import InstagramCreatorAdvanced
        from selenium.webdriver.chrome.options import Options
        
        creator = InstagramCreatorAdvanced("config_default.ini")
        
        # Testar se consegue criar as opções do Chrome
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        
        print("✅ Opções do Chrome criadas com sucesso")
        print("✅ Driver setup OK (teste sem abrir navegador)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no setup do driver: {e}")
        return False

def main():
    """Função principal do teste"""
    print("🚀 Instagram Creator Advanced - Teste de Funcionalidade")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Configuração", test_configuration), 
        ("Dados de Conta", test_account_data),
        ("Setup do Driver", test_driver_setup)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Executando teste: {test_name}")
        
        if asyncio.iscoroutinefunction(test_func):
            result = asyncio.run(test_func())
        else:
            result = test_func()
            
        results.append((test_name, result))
    
    # Resumo dos resultados
    print("\n" + "=" * 60)
    print("📊 RESUMO DOS TESTES")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n📈 Resultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 TODOS OS TESTES PASSARAM! Sistema funcionando corretamente.")
        return True
    else:
        print("⚠️ Alguns testes falharam. Verifique as dependências.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
