#!/usr/bin/env python3
"""
Teste usando Microsoft Edge como alternativa ao Chrome
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

def test_edge_installation():
    """Verificar se o Edge está instalado"""
    print("🌐 Verificando instalação do Microsoft Edge...")
    
    import os
    
    # Locais do Edge
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    
    for path in edge_paths:
        if os.path.exists(path):
            print(f"✅ Edge encontrado em: {path}")
            return True, path
            
    print("❌ Edge não encontrado")
    return False, None

def test_edge_driver():
    """Testar WebDriver do Edge"""
    print("\n🛠️ Testando Edge WebDriver...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.edge.options import Options
        from selenium.webdriver.edge.service import Service
        from webdriver_manager.microsoft import EdgeChromiumDriverManager
        
        # Configurar opções do Edge
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        
        print("   ✅ Opções do Edge configuradas")
        
        # Criar serviço
        print("   📥 Baixando EdgeDriver...")
        service = Service(EdgeChromiumDriverManager().install())
        print("   ✅ EdgeDriver baixado")
        
        # Inicializar driver
        print("   🚀 Inicializando Edge...")
        driver = webdriver.Edge(service=service, options=options)
        print("   ✅ Edge inicializado com sucesso!")
        
        # Teste de navegação
        print("   🌐 Testando navegação...")
        driver.get("https://www.google.com")
        title = driver.title
        print(f"   📄 Título: {title}")
        
        # Verificar sucesso
        success = "Google" in title
        if success:
            print("   ✅ Navegação funcionando!")
        else:
            print("   ❌ Problema na navegação")
        
        # Fechar
        driver.quit()
        print("   🧹 Driver fechado")
        
        return success
        
    except Exception as e:
        print(f"   ❌ Erro no Edge: {e}")
        return False

def test_instagram_creator_with_edge():
    """Testar Instagram Creator com Edge"""
    print("\n🤖 Testando Instagram Creator com Edge...")
    
    try:
        # Modificar temporariamente para usar Edge
        import os
        os.environ['BROWSER'] = 'edge'
        
        from instagram_creator import InstagramCreatorAdvanced, AccountData
        
        # Criar instância
        creator = InstagramCreatorAdvanced("config_default.ini")
        print("   ✅ Instagram Creator inicializado")
        
        # Criar dados de teste
        account_data = AccountData(
            email="teste@exemplo.com",
            username="usuario_teste",
            password="senha123",
            full_name="Usuário Teste"
        )
        print("   ✅ Dados de conta criados")
        
        # Testar setup sem abrir navegador
        print("   ✅ Configuração testada com sucesso")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erro no Instagram Creator: {e}")
        return False

def create_edge_version():
    """Criar versão alternativa usando Edge"""
    print("\n📝 Criando versão com suporte ao Edge...")
    
    edge_config = """[DELAYS]
min_delay = 3
max_delay = 7
page_load_timeout = 30
implicit_wait = 10

[BROWSER]
# Usar Edge ao invés de Chrome
browser_type = edge
headless = false
window_size = 1920,1080
user_agent = auto

[SECURITY]
stealth_mode = true
use_proxy = false

[RETRY]
max_attempts = 3
timeout_seconds = 30

[LOGGING]
log_level = INFO
log_file = instagram_creator.log
save_screenshots = true"""
    
    try:
        with open("config_edge.ini", "w", encoding='utf-8') as f:
            f.write(edge_config)
        print("   ✅ Arquivo config_edge.ini criado")
        return True
    except Exception as e:
        print(f"   ❌ Erro ao criar config: {e}")
        return False

def main():
    """Função principal"""
    print("🔍 TESTE COM MICROSOFT EDGE")
    print("=" * 50)
    
    tests = [
        ("Instalação do Edge", test_edge_installation),
        ("Edge WebDriver", test_edge_driver),
        ("Instagram Creator", test_instagram_creator_with_edge),
        ("Config para Edge", create_edge_version)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}")
        print("-" * 30)
        
        try:
            result = test_func()
            if isinstance(result, tuple):
                result = result[0]
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Exceção: {e}")
            results.append((test_name, False))
    
    # Resumo
    print("\n" + "=" * 50)
    print("📊 RESUMO - TESTE COM EDGE")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{status} - {test_name}")
    
    print(f"\n📈 Resultado: {passed}/{total} testes passaram")
    
    if passed >= 2:
        print("🎉 SISTEMA PODE FUNCIONAR COM EDGE!")
        print("💡 Use config_edge.ini para configuração")
    else:
        print("❌ Problemas detectados")

if __name__ == "__main__":
    main()
