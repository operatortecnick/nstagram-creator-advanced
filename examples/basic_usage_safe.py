#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instagram Creator Advanced - Exemplo de Uso Básico e Seguro
Versão: 2.0.0

Este exemplo demonstra como usar o Instagram Creator de forma básica e segura.
"""

import asyncio
import sys
import os

# Adicionar caminho do projeto ao PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from instagram_creator_advanced import InstagramCreatorAdvanced, validate_account_data


async def exemplo_basico():
    """
    Exemplo básico de criação de uma conta Instagram.
    """
    print("🚀 Instagram Creator Advanced - Exemplo Básico")
    print("=" * 50)
    
    # 1. Dados da conta
    print("📝 Configurando dados da conta...")
    account_data = {
        'email': 'exemplo2025@tempmail.com',
        'full_name': 'João da Silva',
        'username': 'joao_silva_2025_demo',
        'password': 'MinhaSenga123!'
    }
    
    # 2. Validar dados
    print("✅ Validando dados...")
    is_valid, errors = validate_account_data(account_data)
    
    if not is_valid:
        print("❌ Dados inválidos:")
        for error in errors:
            print(f"  - {error}")
        return
    
    print("✅ Dados válidos!")
    
    # 3. Criar instância do Instagram Creator
    print("⚙️  Inicializando Instagram Creator...")
    creator = InstagramCreatorAdvanced(config_file="config.ini")
    
    try:
        # 4. Criar conta
        print(f"👤 Criando conta: {account_data['username']}")
        print("⏱️  Isso pode levar alguns minutos...")
        
        success = await creator.create_account(account_data)
        
        if success:
            print("🎉 SUCESSO! Conta criada com sucesso!")
            print(f"📧 Email: {account_data['email']}")
            print(f"👤 Username: {account_data['username']}")
            
            # Salvar dados da sessão
            creator.save_session_data("conta_criada.json")
            print("💾 Dados salvos em: conta_criada.json")
            
        else:
            print("❌ FALHA ao criar conta")
            print("🔍 Verifique os logs para mais detalhes: instagram_creator.log")
            
    except KeyboardInterrupt:
        print("\n⚠️  Operação cancelada pelo usuário")
        
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        print("🔍 Verifique os logs para mais detalhes: instagram_creator.log")
        
    finally:
        print("🧹 Limpeza concluída")


def exemplo_validacao():
    """
    Exemplo de como validar dados antes de criar conta.
    """
    print("\n" + "=" * 50)
    print("✅ Exemplo de Validação de Dados")
    print("=" * 50)
    
    # Dados válidos
    dados_validos = {
        'email': 'usuario@exemplo.com',
        'full_name': 'Nome Completo',
        'username': 'usuario_valido_123',
        'password': 'senha123456'
    }
    
    # Dados inválidos
    dados_invalidos = {
        'email': 'email_invalido',  # Sem @
        'full_name': '',  # Vazio
        'username': 'ab',  # Muito curto
        'password': '123'  # Muito curta
    }
    
    print("📋 Testando dados válidos:")
    is_valid, errors = validate_account_data(dados_validos)
    print(f"  Resultado: {'✅ VÁLIDO' if is_valid else '❌ INVÁLIDO'}")
    
    print("\n📋 Testando dados inválidos:")
    is_valid, errors = validate_account_data(dados_invalidos)
    print(f"  Resultado: {'✅ VÁLIDO' if is_valid else '❌ INVÁLIDO'}")
    
    if errors:
        print("  Erros encontrados:")
        for error in errors:
            print(f"    - {error}")


def dicas_de_uso():
    """
    Dicas importantes para usar o sistema.
    """
    print("\n" + "=" * 50)
    print("💡 DICAS IMPORTANTES")
    print("=" * 50)
    
    dicas = [
        "🔐 Use senhas fortes (mín. 8 caracteres, números e símbolos)",
        "📧 Use emails temporários válidos (10minutemail, tempmail, etc.)",
        "⏱️  Aguarde entre criações (Instagram detecta atividade suspeita)",
        "🥷 Mantenha stealth_mode=true para evitar detecção",
        "📸 Screenshots são salvas automaticamente para debug",
        "📝 Logs detalhados estão em instagram_creator.log",
        "🔄 Configure proxies se criar muitas contas",
        "⚙️  Teste configurações com headless=false primeiro"
    ]
    
    for dica in dicas:
        print(f"  {dica}")
    
    print("\n⚠️  AVISO LEGAL:")
    print("  Este software é apenas para fins educacionais.")
    print("  Respeite os Termos de Serviço do Instagram.")
    print("  Use com responsabilidade!")


def main():
    """
    Função principal com menu de exemplos.
    """
    print("🤖 Instagram Creator Advanced - Exemplos de Uso")
    print("Versão: 2.0.0")
    print("=" * 60)
    
    print("\nEscolha um exemplo:")
    print("1. 🚀 Uso básico (recomendado)")
    print("2. ✅ Validação de dados")
    print("3. 💡 Dicas de uso")
    print("4. 🏃 Executar exemplo básico agora")
    print("0. ❌ Sair")
    
    try:
        escolha = input("\n📝 Digite sua escolha (0-4): ").strip()
        
        if escolha == "1":
            print("\n📖 Exemplo de uso básico:")
            print("Ver código em: examples/basic_usage_safe.py")
            dicas_de_uso()
            
        elif escolha == "2":
            exemplo_validacao()
            
        elif escolha == "3":
            dicas_de_uso()
            
        elif escolha == "4":
            print("\n🚀 Executando exemplo básico...")
            print("⚠️  CERTIFIQUE-SE de ter configurado o config.ini corretamente!")
            
            continuar = input("Continuar? (s/N): ").lower().strip()
            if continuar in ['s', 'sim', 'y', 'yes']:
                asyncio.run(exemplo_basico())
            else:
                print("❌ Cancelado pelo usuário")
                
        elif escolha == "0":
            print("👋 Até logo!")
            
        else:
            print("❌ Opção inválida!")
            
    except KeyboardInterrupt:
        print("\n👋 Até logo!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")


if __name__ == "__main__":
    main()
