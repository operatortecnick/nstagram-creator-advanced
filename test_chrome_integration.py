#!/usr/bin/env python3
"""
Teste de integração do Chrome e WebDriver
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

def test_chrome_installation():
    """Verificar se o Chrome está instalado"""
    print("🌐 Verificando instalação do Chrome...")
    
    import subprocess
    import os
    
    # Possíveis locais do Chrome no Windows
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
    ]
    
    for path in chrome_paths:
        if os.path.exists(path):
            print(f"✅ Chrome encontrado em: {path}")
            
            # Verificar versão
            try:
                result = subprocess.run([path, "--version"], capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    version = result.stdout.strip()
                    print(f"   📊 Versão: {version}")
                    return True, path
            except Exception as e:
                print(f"   ⚠️ Erro ao verificar versão: {e}")
                
    print("❌ Chrome não encontrado")
    return False, None

def test_webdriver_manager():
    """Testar o WebDriverManager"""
    print("\n🛠️ Testando WebDriverManager...")
    
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        
        print("   📥 Baixando/verificando ChromeDriver...")
        driver_path = ChromeDriverManager().install()
        print(f"   ✅ ChromeDriver disponível em: {driver_path}")
        
        # Verificar se o arquivo existe
        import os
        if os.path.exists(driver_path):
            print(f"   📁 Arquivo confirmado: {os.path.getsize(driver_path)} bytes")
            return True, driver_path
        else:
            print("   ❌ Arquivo do driver não encontrado")
            return False, None
            
    except Exception as e:
        print(f"   ❌ Erro no WebDriverManager: {e}")
        return False, None

def test_selenium_basic():
    """Teste básico do Selenium"""
    print("\n🤖 Testando Selenium básico...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        
        # Configurar opções do Chrome
        options = Options()
        options.add_argument('--headless')  # Modo headless para teste
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--window-size=1920,1080')
        
        print("   ✅ Opções do Chrome configuradas")
        
        # Criar serviço
        service = Service(ChromeDriverManager().install())
        print("   ✅ Serviço do ChromeDriver criado")
        
        # Inicializar driver
        print("   🚀 Inicializando driver do Chrome...")
        driver = webdriver.Chrome(service=service, options=options)
        print("   ✅ Driver inicializado com sucesso!")
        
        # Teste básico de navegação
        print("   🌐 Testando navegação...")
        driver.get("https://www.google.com")
        title = driver.title
        print(f"   📄 Título da página: {title}")
        
        # Verificar se conseguiu carregar
        if "Google" in title:
            print("   ✅ Navegação funcionando!")
            result = True
        else:
            print("   ❌ Problema na navegação")
            result = False
        
        # Fechar driver
        driver.quit()
        print("   🧹 Driver fechado com sucesso")
        
        return result
        
    except Exception as e:
        print(f"   ❌ Erro no teste do Selenium: {e}")
        return False

def test_undetected_chrome():
    """Testar undetected_chromedriver"""
    print("\n🕵️ Testando undetected_chromedriver...")
    
    try:
        import undetected_chromedriver as uc
        
        print("   🚀 Inicializando undetected_chromedriver...")
        
        # Configurar opções
        options = uc.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        # Inicializar driver
        driver = uc.Chrome(options=options)
        print("   ✅ Undetected Chrome inicializado!")
        
        # Teste rápido
        driver.get("https://www.google.com")
        title = driver.title
        print(f"   📄 Título: {title}")
        
        # Fechar
        driver.quit()
        print("   🧹 Driver fechado")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erro no undetected_chromedriver: {e}")
        print("   💡 Isso é normal se for a primeira execução")
        return False

def main():
    """Função principal do teste de integração"""
    print("🔍 TESTE DE INTEGRAÇÃO - Chrome + WebDriver")
    print("=" * 60)
    
    tests = [
        ("Instalação do Chrome", test_chrome_installation),
        ("WebDriverManager", test_webdriver_manager),
        ("Selenium Básico", test_selenium_basic),
        ("Undetected Chrome", test_undetected_chrome)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}")
        print("-" * 40)
        
        try:
            result = test_func()
            if isinstance(result, tuple):
                result = result[0]  # Pegar apenas o status
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Exceção no teste: {e}")
            results.append((test_name, False))
    
    # Resumo
    print("\n" + "=" * 60)
    print("📊 RESUMO FINAL")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n📈 Resultado: {passed}/{total} testes passaram")
    
    if passed >= 3:  # Pelo menos 3 de 4 testes
        print("🎉 SISTEMA PRONTO PARA USO!")
        print("💡 Você pode usar o Instagram Creator Advanced")
    elif passed >= 2:
        print("⚠️ SISTEMA PARCIALMENTE FUNCIONAL")
        print("💡 Algumas funcionalidades podem não funcionar")
    else:
        print("❌ SISTEMA NÃO FUNCIONAL")
        print("💡 Verifique a instalação do Chrome e dependências")

if __name__ == "__main__":
    main()
