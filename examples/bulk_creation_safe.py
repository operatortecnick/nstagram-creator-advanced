#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instagram Creator Advanced - Exemplo de Criação em Lote
Versão: 2.0.0

Este exemplo demonstra como criar múltiplas contas de forma eficiente e segura.
"""

import asyncio
import sys
import os
import json
import csv
from datetime import datetime
from typing import List, Dict

# Adicionar caminho do projeto ao PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from instagram_creator_advanced import (
    InstagramCreatorAdvanced,
    validate_account_data,
    generate_username,
    generate_email
)


class BulkAccountCreator:
    """
    Classe para criação em lote de contas Instagram.
    """
    
    def __init__(self, config_file: str = "config.ini"):
        self.config_file = config_file
        self.results = []
        self.session_start = datetime.now()
        
    def load_accounts_from_csv(self, csv_file: str) -> List[Dict[str, str]]:
        """
        Carrega dados de contas de um arquivo CSV.
        
        CSV deve ter colunas: email,full_name,username,password
        """
        accounts = []
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    accounts.append({
                        'email': row['email'],
                        'full_name': row['full_name'],
                        'username': row['username'],
                        'password': row['password']
                    })
            
            print(f"📁 Carregadas {len(accounts)} contas de {csv_file}")
            return accounts
            
        except Exception as e:
            print(f"❌ Erro ao carregar CSV: {e}")
            return []
    
    def generate_bulk_accounts(self, count: int, base_name: str = "bulk_user") -> List[Dict[str, str]]:
        """
        Gera dados para múltiplas contas automaticamente.
        """
        accounts = []
        
        print(f"🔄 Gerando {count} contas automaticamente...")
        
        for i in range(count):
            # Gerar dados únicos
            username = f"{base_name}_{i+1}_{datetime.now().strftime('%m%d')}"
            email = f"{username}@tempmail.com"
            full_name = f"User {i+1}"
            password = f"Password{i+1}@2025"
            
            account_data = {
                'email': email,
                'full_name': full_name,
                'username': username,
                'password': password
            }
            
            accounts.append(account_data)
            print(f"  📝 {i+1}. {username}")
        
        return accounts
    
    def validate_all_accounts(self, accounts: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Valida todos os dados antes de criar as contas.
        """
        valid_accounts = []
        
        print("✅ Validando todas as contas...")
        
        for i, account_data in enumerate(accounts):
            is_valid, errors = validate_account_data(account_data)
            
            if is_valid:
                valid_accounts.append(account_data)
                print(f"  ✅ {i+1}. {account_data['username']}")
            else:
                print(f"  ❌ {i+1}. {account_data['username']}: {', '.join(errors)}")
        
        print(f"📊 {len(valid_accounts)}/{len(accounts)} contas válidas")
        return valid_accounts
    
    async def create_accounts_batch(self, accounts: List[Dict[str, str]], 
                                  delay_between: int = 60) -> Dict[str, bool]:
        """
        Cria contas em lote com delay entre elas.
        
        Args:
            accounts: Lista de dados das contas
            delay_between: Delay em segundos entre cada conta
            
        Returns:
            Dicionário com resultados
        """
        results = {}
        total = len(accounts)
        
        print(f"🚀 Iniciando criação de {total} contas...")
        print(f"⏱️  Delay entre contas: {delay_between}s")
        print(f"🕐 Tempo estimado: {(total * delay_between) / 60:.1f} minutos")
        
        for i, account_data in enumerate(accounts):
            username = account_data['username']
            
            print(f"\n📋 Conta {i+1}/{total}: {username}")
            print(f"⏱️  {datetime.now().strftime('%H:%M:%S')}")
            
            try:
                # Criar instância do Instagram Creator
                creator = InstagramCreatorAdvanced(self.config_file)
                
                # Tentar criar conta
                success = await creator.create_account(account_data)
                
                # Registrar resultado
                result_data = {
                    'username': username,
                    'email': account_data['email'],
                    'success': success,
                    'timestamp': datetime.now().isoformat(),
                    'order': i + 1
                }
                
                results[username] = success
                self.results.append(result_data)
                
                if success:
                    print(f"✅ {username} - SUCESSO!")
                else:
                    print(f"❌ {username} - FALHA")
                
                # Salvar dados da sessão
                creator.save_session_data(f"session_{username}.json")
                
            except Exception as e:
                print(f"❌ {username} - ERRO: {e}")
                results[username] = False
                
                # Registrar erro
                error_data = {
                    'username': username,
                    'email': account_data['email'],
                    'success': False,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat(),
                    'order': i + 1
                }
                self.results.append(error_data)
            
            # Delay entre contas (exceto na última)
            if i < total - 1:
                print(f"⏱️  Aguardando {delay_between}s...")
                await asyncio.sleep(delay_between)
        
        # Relatório final
        successful = sum(1 for success in results.values() if success)
        print(f"\n📊 RELATÓRIO FINAL:")
        print(f"  ✅ Sucessos: {successful}/{total}")
        print(f"  ❌ Falhas: {total - successful}/{total}")
        print(f"  📈 Taxa de sucesso: {(successful/total)*100:.1f}%")
        
        return results
    
    def save_results_report(self, filename: str = None):
        """
        Salva relatório detalhado dos resultados.
        """
        if filename is None:
            timestamp = self.session_start.strftime("%Y%m%d_%H%M%S")
            filename = f"bulk_creation_report_{timestamp}.json"
        
        report = {
            'session_info': {
                'start_time': self.session_start.isoformat(),
                'end_time': datetime.now().isoformat(),
                'total_accounts': len(self.results),
                'successful_accounts': sum(1 for r in self.results if r.get('success', False)),
                'config_file': self.config_file
            },
            'results': self.results
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            
            print(f"📄 Relatório salvo: {filename}")
            
        except Exception as e:
            print(f"❌ Erro ao salvar relatório: {e}")
    
    def save_successful_accounts_csv(self, filename: str = None):
        """
        Salva apenas as contas criadas com sucesso em CSV.
        """
        if filename is None:
            timestamp = self.session_start.strftime("%Y%m%d_%H%M%S")
            filename = f"successful_accounts_{timestamp}.csv"
        
        successful_accounts = [r for r in self.results if r.get('success', False)]
        
        if not successful_accounts:
            print("⚠️  Nenhuma conta criada com sucesso para salvar")
            return
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                fieldnames = ['username', 'email', 'timestamp', 'order']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                
                writer.writeheader()
                for account in successful_accounts:
                    writer.writerow({
                        'username': account['username'],
                        'email': account['email'],
                        'timestamp': account['timestamp'],
                        'order': account['order']
                    })
            
            print(f"📊 Contas bem-sucedidas salvas: {filename}")
            
        except Exception as e:
            print(f"❌ Erro ao salvar CSV: {e}")


async def exemplo_bulk_automatico():
    """
    Exemplo de criação em lote automática.
    """
    print("🤖 Exemplo: Criação em Lote Automática")
    print("=" * 50)
    
    creator = BulkAccountCreator()
    
    # Gerar contas automaticamente
    num_accounts = 3  # Pequeno número para demo
    accounts = creator.generate_bulk_accounts(num_accounts, "demo_bulk")
    
    # Validar todas as contas
    valid_accounts = creator.validate_all_accounts(accounts)
    
    if not valid_accounts:
        print("❌ Nenhuma conta válida para criar")
        return
    
    try:
        # Criar contas (delay pequeno para demo)
        print("\n⚠️  DEMO MODE: Usando delay de 10s entre contas")
        results = await creator.create_accounts_batch(valid_accounts, delay_between=10)
        
        # Salvar relatórios
        creator.save_results_report()
        creator.save_successful_accounts_csv()
        
    except KeyboardInterrupt:
        print("\n⚠️  Criação interrompida pelo usuário")
        creator.save_results_report("interrupted_session.json")


async def exemplo_bulk_csv():
    """
    Exemplo de criação em lote a partir de CSV.
    """
    print("\n📁 Exemplo: Criação em Lote via CSV")
    print("=" * 50)
    
    # Criar arquivo CSV de exemplo
    csv_filename = "accounts_example.csv"
    sample_data = [
        ['email', 'full_name', 'username', 'password'],
        ['user1@tempmail.com', 'João Silva', 'joao_csv_2025', 'senha123456'],
        ['user2@tempmail.com', 'Maria Santos', 'maria_csv_2025', 'senha123456'],
        ['user3@tempmail.com', 'Pedro Lima', 'pedro_csv_2025', 'senha123456']
    ]
    
    with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(sample_data)
    
    print(f"📄 Arquivo CSV de exemplo criado: {csv_filename}")
    
    creator = BulkAccountCreator()
    
    try:
        # Carregar contas do CSV
        accounts = creator.load_accounts_from_csv(csv_filename)
        
        if not accounts:
            print("❌ Nenhuma conta carregada do CSV")
            return
        
        # Validar contas
        valid_accounts = creator.validate_all_accounts(accounts)
        
        if valid_accounts:
            print(f"\n✅ {len(valid_accounts)} contas prontas para criação")
            print("💡 Para criar as contas, descomente a linha abaixo:")
            print("# results = await creator.create_accounts_batch(valid_accounts)")
            
            # Em produção, descomente:
            # results = await creator.create_accounts_batch(valid_accounts, delay_between=60)
            # creator.save_results_report()
            # creator.save_successful_accounts_csv()
        
    finally:
        # Limpar arquivo de exemplo
        if os.path.exists(csv_filename):
            os.remove(csv_filename)
            print(f"🧹 Arquivo de exemplo removido: {csv_filename}")


def exemplo_configuracao_bulk():
    """
    Exemplo de configuração otimizada para criação em lote.
    """
    print("\n⚙️  Exemplo: Configuração para Bulk Creation")
    print("=" * 50)
    
    import configparser
    
    # Configuração otimizada para bulk
    config = configparser.ConfigParser()
    
    config['BROWSER'] = {
        'headless': 'true',  # Headless para velocidade
        'page_load_timeout': '45'
    }
    
    config['DELAYS'] = {
        'min_delay': '8',  # Delays maiores para segurança
        'max_delay': '15',
        'typing_delay': '0.2'
    }
    
    config['BATCH_PROCESSING'] = {
        'account_creation_delay': '120',  # 2 min entre contas
        'max_accounts_per_session': '5',
        'session_delay': '600'  # 10 min entre sessões
    }
    
    config['LOGGING'] = {
        'log_level': 'INFO',
        'save_screenshots': 'true'  # Para debug
    }
    
    config['ERROR_HANDLING'] = {
        'continue_on_error': 'true',
        'auto_retry_on_error': 'true',
        'screenshot_on_error': 'true'
    }
    
    # Salvar configuração
    config_filename = "config_bulk.ini"
    with open(config_filename, 'w', encoding='utf-8') as f:
        config.write(f)
    
    print(f"⚙️  Configuração para bulk criada: {config_filename}")
    print("\n📋 Configurações otimizadas:")
    print("  🔧 Headless mode ativado")
    print("  ⏱️  Delays maiores para segurança")
    print("  🔄 Auto-retry em caso de erro")
    print("  📸 Screenshots automáticas")
    print("  📝 Logging detalhado")
    
    print(f"\n💡 Para usar: BulkAccountCreator('{config_filename}')")


def main():
    """
    Menu principal dos exemplos de criação em lote.
    """
    print("📦 Instagram Creator Advanced - Criação em Lote")
    print("Versão: 2.0.0")
    print("=" * 60)
    
    print("\nEscolha um exemplo:")
    print("1. 🤖 Criação automática (geração de dados)")
    print("2. 📁 Criação via CSV")
    print("3. ⚙️  Configuração otimizada para bulk")
    print("4. 📊 Executar exemplo automático")
    print("0. ❌ Sair")
    
    try:
        escolha = input("\n📝 Digite sua escolha (0-4): ").strip()
        
        if escolha == "1":
            print("\n📖 Exemplo de criação automática:")
            print("Ver código em: examples/bulk_creation.py - exemplo_bulk_automatico()")
            
        elif escolha == "2":
            asyncio.run(exemplo_bulk_csv())
            
        elif escolha == "3":
            exemplo_configuracao_bulk()
            
        elif escolha == "4":
            print("\n🚀 Executando exemplo automático...")
            print("⚠️  Este é apenas uma demonstração!")
            
            continuar = input("Continuar? (s/N): ").lower().strip()
            if continuar in ['s', 'sim', 'y', 'yes']:
                asyncio.run(exemplo_bulk_automatico())
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
