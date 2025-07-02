#!/usr/bin/env python3
"""
Exemplo de Uso Básico - Instagram Creator Advanced
Este exemplo demonstra o uso básico e seguro do sistema
"""

import asyncio
import logging
from pathlib import Path
import sys

# Adicionar diretório pai ao path para importar o módulo
sys.path.append(str(Path(__file__).parent.parent))

from instagram_creator import InstagramCreatorAdvanced, AccountData

# Configurar logging para o exemplo
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def exemplo_criacao_simples():
    """Exemplo de criação de uma única conta"""
    print("🤖 Exemplo: Criação Simples de Conta")
    print("=" * 50)
    
    try:
        # Inicializar o criador
        creator = InstagramCreatorAdvanced("config_default.ini")
        
        # Criar uma conta com dados aleatórios
        print("🚀 Criando conta com dados aleatórios...")
        result = await creator.create_account()
        
        if result.success:
            print("✅ Sucesso! Conta criada:")
            print(f"   👤 Username: {result.account_data.username}")
            print(f"   📧 Email: {result.account_data.email}")
            print(f"   🔑 Password: {result.account_data.password}")
            print(f"   👥 Nome: {result.account_data.full_name}")
            print(f"   ⏱️  Tempo: {result.creation_time:.2f}s")
        else:
            print(f"❌ Falha na criação: {result.error_message}")
            
    except Exception as e:
        logger.error(f"Erro no exemplo: {e}")

async def exemplo_dados_customizados():
    """Exemplo com dados personalizados"""
    print("\n🎯 Exemplo: Dados Personalizados")
    print("=" * 50)
    
    try:
        creator = InstagramCreatorAdvanced()
        
        # Criar dados personalizados
        dados_customizados = AccountData(
            username="meuusuario123",
            email="meuusuario123@gmail.com",
            password="MinhaSenh@123",
            full_name="João Silva",
            bio="Desenvolvedor Python"
        )
        
        print("🎨 Criando conta com dados personalizados...")
        result = await creator.create_account(dados_customizados)
        
        if result.success:
            print("✅ Conta personalizada criada com sucesso!")
        else:
            print(f"❌ Erro: {result.error_message}")
            
    except Exception as e:
        logger.error(f"Erro no exemplo: {e}")

async def exemplo_com_validacao():
    """Exemplo com validação de dados"""
    print("\n🔍 Exemplo: Com Validação")
    print("=" * 50)
    
    def validar_resultado(result):
        """Valida resultado da criação"""
        if not result.success:
            return False, f"Criação falhou: {result.error_message}"
        
        if not result.account_data:
            return False, "Dados da conta não encontrados"
        
        # Validações básicas
        if len(result.account_data.username) < 3:
            return False, "Username muito curto"
        
        if "@" not in result.account_data.email:
            return False, "Email inválido"
        
        if len(result.account_data.password) < 8:
            return False, "Senha muito simples"
        
        return True, "Validação bem-sucedida"
    
    try:
        creator = InstagramCreatorAdvanced()
        
        print("🔄 Criando e validando conta...")
        result = await creator.create_account()
        
        # Validar resultado
        valido, mensagem = validar_resultado(result)
        
        if valido:
            print(f"✅ {mensagem}")
            print(f"   📊 Dados válidos para: {result.account_data.username}")
        else:
            print(f"❌ {mensagem}")
            
    except Exception as e:
        logger.error(f"Erro no exemplo: {e}")

async def exemplo_tratamento_erros():
    """Exemplo de tratamento robusto de erros"""
    print("\n🛡️  Exemplo: Tratamento de Erros")
    print("=" * 50)
    
    creator = InstagramCreatorAdvanced()
    max_tentativas = 3
    
    for tentativa in range(1, max_tentativas + 1):
        print(f"🔄 Tentativa {tentativa}/{max_tentativas}")
        
        try:
            result = await creator.create_account()
            
            if result.success:
                print("✅ Sucesso na criação!")
                break
            else:
                print(f"⚠️  Falha: {result.error_message}")
                
                if tentativa < max_tentativas:
                    print("⏳ Aguardando antes da próxima tentativa...")
                    await asyncio.sleep(5)
                    
        except Exception as e:
            print(f"❌ Erro crítico: {e}")
            
            if tentativa < max_tentativas:
                print("🔄 Tentando novamente...")
                await asyncio.sleep(10)
    else:
        print("❌ Todas as tentativas falharam")

async def exemplo_configuracao_personalizada():
    """Exemplo com configuração personalizada"""
    print("\n⚙️ Exemplo: Configuração Personalizada")
    print("=" * 50)
    
    import configparser
    
    # Criar configuração personalizada
    config = configparser.ConfigParser()
    config.read_string("""
[BROWSER]
headless = true
window_size = 1366,768

[DELAYS]
min_delay = 1
max_delay = 3
typing_delay = 0.05

[ACCOUNT_GENERATION]
username_prefix = exemplo
email_domain = @teste.com
password_length = 10
""")
    
    # Salvar configuração temporária
    with open("config_exemplo.ini", "w") as f:
        config.write(f)
    
    try:
        # Usar configuração personalizada
        creator = InstagramCreatorAdvanced("config_exemplo.ini")
        
        print("⚡ Criando conta com configuração rápida...")
        result = await creator.create_account()
        
        if result.success:
            print("✅ Configuração personalizada funcionou!")
            print(f"   Username gerado: {result.account_data.username}")
        
    finally:
        # Limpar arquivo temporário
        import os
        if os.path.exists("config_exemplo.ini"):
            os.remove("config_exemplo.ini")

async def main():
    """Função principal que executa todos os exemplos"""
    print("📚 Instagram Creator Advanced - Exemplos Básicos")
    print("=" * 70)
    
    exemplos = [
        ("Criação Simples", exemplo_criacao_simples),
        ("Dados Customizados", exemplo_dados_customizados),
        ("Com Validação", exemplo_com_validacao),
        ("Tratamento de Erros", exemplo_tratamento_erros),
        ("Configuração Personalizada", exemplo_configuracao_personalizada)
    ]
    
    for nome, funcao in exemplos:
        try:
            print(f"\n🎯 Executando: {nome}")
            await funcao()
            print(f"✅ {nome} concluído")
        except KeyboardInterrupt:
            print(f"\n❌ Interrompido pelo usuário")
            break
        except Exception as e:
            print(f"❌ Erro em {nome}: {e}")
            continue
    
    print("\n🎉 Exemplos básicos concluídos!")
    print("💡 Próximo passo: Explore os exemplos avançados")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Finalizado pelo usuário")
    except Exception as e:
        print(f"\n💥 Erro fatal: {e}")
        sys.exit(1)
