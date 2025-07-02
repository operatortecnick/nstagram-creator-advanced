#!/usr/bin/env python3
"""
Exemplo de Criação em Lote - Instagram Creator Advanced
Este exemplo demonstra criação automatizada de múltiplas contas em larga escala
"""

import asyncio
import json
import csv
import time
import logging
from datetime import datetime
from pathlib import Path
import sys
from typing import List, Dict

# Adicionar diretório pai ao path
sys.path.append(str(Path(__file__).parent.parent))

from instagram_creator import InstagramCreatorAdvanced, CreationResult

# Configurar logging para operações em lote
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'bulk_creation_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BulkAccountCreator:
    """Classe especializada para criação em lote de contas"""
    
    def __init__(self, config_file: str = "config_default.ini"):
        self.creator = InstagramCreatorAdvanced(config_file)
        self.results: List[CreationResult] = []
        self.stats = {
            "start_time": None,
            "end_time": None,
            "total_requested": 0,
            "successful": 0,
            "failed": 0,
            "errors": {}
        }
    
    async def create_accounts_batch(self, 
                                  total_accounts: int,
                                  batch_size: int = 5,
                                  delay_between_batches: float = 60.0) -> List[CreationResult]:
        """
        Cria contas em lotes para otimizar performance e evitar detecção
        
        Args:
            total_accounts: Total de contas a criar
            batch_size: Tamanho de cada lote
            delay_between_batches: Delay entre lotes (segundos)
        """
        self.stats["start_time"] = time.time()
        self.stats["total_requested"] = total_accounts
        
        logger.info(f"🚀 Iniciando criação em lote: {total_accounts} contas")
        logger.info(f"📦 Configuração: lotes de {batch_size}, delay {delay_between_batches}s")
        
        all_results = []
        
        for batch_num in range(0, total_accounts, batch_size):
            batch_end = min(batch_num + batch_size, total_accounts)
            current_batch_size = batch_end - batch_num
            
            logger.info(f"\n📦 Lote {(batch_num//batch_size)+1}: contas {batch_num+1}-{batch_end}")
            
            # Processar lote atual
            batch_results = await self._process_batch(current_batch_size, batch_num + 1)
            all_results.extend(batch_results)
            
            # Atualizar estatísticas
            for result in batch_results:
                if result.success:
                    self.stats["successful"] += 1
                else:
                    self.stats["failed"] += 1
                    error_type = type(result.error_message).__name__ if result.error_message else "Unknown"
                    self.stats["errors"][error_type] = self.stats["errors"].get(error_type, 0) + 1
            
            # Progresso
            progress = ((batch_num + current_batch_size) / total_accounts) * 100
            logger.info(f"📊 Progresso: {progress:.1f}% ({self.stats['successful']} sucessos, {self.stats['failed']} falhas)")
            
            # Delay entre lotes (exceto no último)
            if batch_end < total_accounts:
                logger.info(f"⏳ Aguardando {delay_between_batches}s antes do próximo lote...")
                await asyncio.sleep(delay_between_batches)
        
        self.stats["end_time"] = time.time()
        self.results = all_results
        
        # Relatório final
        self._generate_final_report()
        
        return all_results
    
    async def _process_batch(self, batch_size: int, start_num: int) -> List[CreationResult]:
        """Processa um lote de contas"""
        tasks = []
        
        # Criar tasks para execução paralela limitada
        for i in range(batch_size):
            account_num = start_num + i - 1
            task = self._create_single_account_with_retry(account_num)
            tasks.append(task)
        
        # Executar com limite de concorrência
        semaphore = asyncio.Semaphore(3)  # Máximo 3 simultâneas
        
        async def limited_create(task):
            async with semaphore:
                return await task
        
        results = await asyncio.gather(*[limited_create(task) for task in tasks])
        return results
    
    async def _create_single_account_with_retry(self, account_num: int, max_retries: int = 3) -> CreationResult:
        """Cria uma conta com retry automático"""
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    delay = min(60, 2 ** attempt)
                    logger.info(f"   🔄 Conta {account_num}: tentativa {attempt + 1}, aguardando {delay}s")
                    await asyncio.sleep(delay)
                
                result = await self.creator.create_account()
                
                if result.success:
                    logger.info(f"   ✅ Conta {account_num}: {result.account_data.username}")
                    return result
                else:
                    logger.warning(f"   ⚠️  Conta {account_num}: {result.error_message}")
                    
            except Exception as e:
                logger.error(f"   ❌ Conta {account_num}: Erro - {e}")
        
        return CreationResult(success=False, error_message="Máximo de tentativas excedido")
    
    def _generate_final_report(self):
        """Gera relatório final detalhado"""
        duration = self.stats["end_time"] - self.stats["start_time"]
        success_rate = (self.stats["successful"] / self.stats["total_requested"]) * 100
        
        print("\n" + "="*80)
        print("📊 RELATÓRIO FINAL DE CRIAÇÃO EM LOTE")
        print("="*80)
        print(f"🎯 Total solicitado: {self.stats['total_requested']} contas")
        print(f"✅ Criadas com sucesso: {self.stats['successful']}")
        print(f"❌ Falhas: {self.stats['failed']}")
        print(f"📈 Taxa de sucesso: {success_rate:.1f}%")
        print(f"⏱️  Tempo total: {duration:.2f}s ({duration/60:.1f} minutos)")
        
        if self.stats["successful"] > 0:
            avg_time = duration / self.stats["successful"]
            accounts_per_hour = 3600 / avg_time if avg_time > 0 else 0
            print(f"⚡ Tempo médio por conta: {avg_time:.2f}s")
            print(f"🚀 Taxa estimada: {accounts_per_hour:.1f} contas/hora")
        
        if self.stats["errors"]:
            print(f"\n🐛 Tipos de erro encontrados:")
            for error_type, count in self.stats["errors"].items():
                print(f"   {error_type}: {count} ocorrência(s)")
        
        print("="*80)
    
    def save_results_json(self, filename: str = None):
        """Salva resultados em formato JSON"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"bulk_accounts_{timestamp}.json"
        
        successful_accounts = [r for r in self.results if r.success and r.account_data]
        
        data = {
            "metadata": {
                "creation_date": datetime.now().isoformat(),
                "total_created": len(successful_accounts),
                "statistics": self.stats
            },
            "accounts": []
        }
        
        for result in successful_accounts:
            data["accounts"].append({
                "username": result.account_data.username,
                "email": result.account_data.email,
                "password": result.account_data.password,
                "full_name": result.account_data.full_name,
                "creation_time": result.creation_time
            })
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Resultados salvos em: {filename}")
        return filename
    
    def save_results_csv(self, filename: str = None):
        """Salva resultados em formato CSV"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"bulk_accounts_{timestamp}.csv"
        
        successful_accounts = [r for r in self.results if r.success and r.account_data]
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Cabeçalho
            writer.writerow(['Username', 'Email', 'Password', 'Full Name', 'Creation Time'])
            
            # Dados
            for result in successful_accounts:
                writer.writerow([
                    result.account_data.username,
                    result.account_data.email,
                    result.account_data.password,
                    result.account_data.full_name,
                    result.creation_time
                ])
        
        logger.info(f"📊 CSV salvo em: {filename}")
        return filename

async def exemplo_criacao_pequena():
    """Exemplo de criação em pequena escala"""
    print("📦 Exemplo: Criação Pequena (5 contas)")
    print("=" * 50)
    
    creator = BulkAccountCreator()
    
    results = await creator.create_accounts_batch(
        total_accounts=5,
        batch_size=2,
        delay_between_batches=30
    )
    
    # Salvar resultados
    json_file = creator.save_results_json()
    csv_file = creator.save_results_csv()
    
    print(f"\n💾 Arquivos gerados:")
    print(f"   📄 JSON: {json_file}")
    print(f"   📊 CSV: {csv_file}")

async def exemplo_criacao_media():
    """Exemplo de criação em escala média"""
    print("\n📦 Exemplo: Criação Média (20 contas)")
    print("=" * 50)
    
    creator = BulkAccountCreator()
    
    # Configuração mais conservadora para escala média
    results = await creator.create_accounts_batch(
        total_accounts=20,
        batch_size=3,
        delay_between_batches=90  # 1.5 minutos entre lotes
    )
    
    creator.save_results_json("medium_batch_accounts.json")
    creator.save_results_csv("medium_batch_accounts.csv")

async def exemplo_criacao_com_monitoramento():
    """Exemplo com monitoramento de sistema"""
    print("\n📊 Exemplo: Criação com Monitoramento")
    print("=" * 50)
    
    import psutil
    import threading
    
    # Monitor de recursos
    system_stats = {"cpu": [], "memory": [], "running": True}
    
    def monitor_resources():
        while system_stats["running"]:
            system_stats["cpu"].append(psutil.cpu_percent())
            system_stats["memory"].append(psutil.virtual_memory().percent)
            time.sleep(5)
    
    # Iniciar monitoramento
    monitor_thread = threading.Thread(target=monitor_resources)
    monitor_thread.start()
    
    try:
        creator = BulkAccountCreator()
        
        results = await creator.create_accounts_batch(
            total_accounts=10,
            batch_size=2,
            delay_between_batches=45
        )
        
        # Parar monitoramento
        system_stats["running"] = False
        monitor_thread.join()
        
        # Relatório do sistema
        if system_stats["cpu"]:
            avg_cpu = sum(system_stats["cpu"]) / len(system_stats["cpu"])
            avg_memory = sum(system_stats["memory"]) / len(system_stats["memory"])
            
            print(f"\n🖥️  Uso médio do sistema durante criação:")
            print(f"   💻 CPU: {avg_cpu:.1f}%")
            print(f"   🧠 Memória: {avg_memory:.1f}%")
        
        creator.save_results_json("monitored_accounts.json")
        
    except Exception as e:
        system_stats["running"] = False
        logger.error(f"Erro durante criação monitorada: {e}")

async def exemplo_configuracao_adaptativa():
    """Exemplo com configuração que se adapta aos resultados"""
    print("\n⚙️ Exemplo: Configuração Adaptativa")
    print("=" * 50)
    
    creator = BulkAccountCreator()
    
    # Começar com configuração rápida
    batch_size = 3
    delay = 30
    
    total_to_create = 15
    created_so_far = 0
    
    while created_so_far < total_to_create:
        remaining = min(batch_size * 2, total_to_create - created_so_far)
        
        logger.info(f"🎯 Criando {remaining} contas com delay de {delay}s")
        
        batch_results = await creator.create_accounts_batch(
            total_accounts=remaining,
            batch_size=batch_size,
            delay_between_batches=delay
        )
        
        # Analisar resultado e adaptar configuração
        recent_successes = sum(1 for r in batch_results if r.success)
        success_rate = (recent_successes / remaining) * 100
        
        logger.info(f"📊 Taxa de sucesso do lote: {success_rate:.1f}%")
        
        if success_rate < 50:
            # Taxa baixa - ser mais conservador
            delay = min(delay * 1.5, 300)  # Máximo 5 minutos
            batch_size = max(batch_size - 1, 1)
            logger.info(f"⚠️  Adaptando: delay={delay}s, batch_size={batch_size}")
        elif success_rate > 80:
            # Taxa alta - pode acelerar um pouco
            delay = max(delay * 0.8, 15)  # Mínimo 15 segundos
            batch_size = min(batch_size + 1, 5)
            logger.info(f"⚡ Adaptando: delay={delay}s, batch_size={batch_size}")
        
        created_so_far += remaining
        
        if created_so_far < total_to_create:
            await asyncio.sleep(delay)
    
    creator.save_results_json("adaptive_accounts.json")

async def main():
    """Função principal com exemplos de criação em lote"""
    print("📦 Instagram Creator Advanced - Criação em Lote")
    print("=" * 70)
    
    exemplos = [
        ("Criação Pequena", exemplo_criacao_pequena),
        ("Criação Média", exemplo_criacao_media),
        ("Com Monitoramento", exemplo_criacao_com_monitoramento),
        ("Configuração Adaptativa", exemplo_configuracao_adaptativa)
    ]
    
    for nome, funcao in exemplos:
        try:
            print(f"\n🎯 Executando: {nome}")
            await funcao()
            print(f"✅ {nome} concluído")
            
            # Pausa entre exemplos
            print("⏳ Pausa entre exemplos...")
            await asyncio.sleep(5)
            
        except KeyboardInterrupt:
            print(f"\n❌ Interrompido pelo usuário")
            break
        except Exception as e:
            logger.error(f"Erro em {nome}: {e}")
            continue
    
    print("\n🎉 Exemplos de criação em lote concluídos!")
    print("💡 Use estes padrões para implementar sua própria solução em larga escala")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Finalizado pelo usuário")
    except Exception as e:
        print(f"\n💥 Erro fatal: {e}")
        sys.exit(1)
