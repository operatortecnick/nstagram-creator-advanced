#!/usr/bin/env python3
"""
Exemplo de Uso Avançado - Instagram Creator Advanced
Este exemplo demonstra funcionalidades avançadas e configurações otimizadas
"""

import asyncio
import logging
import json
import time
import random
from pathlib import Path
import sys
from typing import List, Dict, Any

# Adicionar diretório pai ao path
sys.path.append(str(Path(__file__).parent.parent))

from instagram_creator import InstagramCreatorAdvanced, AccountData, CreationResult

# Configurar logging avançado
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('advanced_example.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AdvancedInstagramCreator:
    """Wrapper avançado com funcionalidades extras"""
    
    def __init__(self, config_file: str = "config_default.ini"):
        self.creator = InstagramCreatorAdvanced(config_file)
        self.stats = {
            "total_attempts": 0,
            "successful_creations": 0,
            "failed_creations": 0,
            "start_time": None,
            "end_time": None
        }
    
    async def create_with_retry_strategy(self, max_retries: int = 3) -> CreationResult:
        """Criação com estratégia de retry exponencial"""
        for attempt in range(max_retries):
            try:
                self.stats["total_attempts"] += 1
                
                # Backoff exponencial
                if attempt > 0:
                    delay = min(300, (2 ** attempt) + random.uniform(0, 1))
                    logger.info(f"Retry {attempt}: aguardando {delay:.1f}s")
                    await asyncio.sleep(delay)
                
                result = await self.creator.create_account()
                
                if result.success:
                    self.stats["successful_creations"] += 1
                    return result
                else:
                    self.stats["failed_creations"] += 1
                    logger.warning(f"Tentativa {attempt + 1} falhou: {result.error_message}")
                    
            except Exception as e:
                logger.error(f"Erro na tentativa {attempt + 1}: {e}")
        
        # Todas as tentativas falharam
        return CreationResult(success=False, error_message="Máximo de tentativas excedido")
    
    async def batch_creation_with_monitoring(self, count: int, batch_size: int = 3) -> List[CreationResult]:
        """Criação em lotes com monitoramento"""
        results = []
        self.stats["start_time"] = time.time()
        
        logger.info(f"🚀 Iniciando criação em lotes: {count} contas, lotes de {batch_size}")
        
        for i in range(0, count, batch_size):
            batch_end = min(i + batch_size, count)
            batch_num = (i // batch_size) + 1
            
            logger.info(f"📦 Lote {batch_num}: contas {i+1}-{batch_end}")
            
            # Processar lote
            batch_tasks = []
            for j in range(i, batch_end):
                task = self.create_with_retry_strategy()
                batch_tasks.append(task)
            
            # Aguardar conclusão do lote
            batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
            
            # Processar resultados do lote
            for j, result in enumerate(batch_results):
                if isinstance(result, Exception):
                    logger.error(f"Conta {i+j+1}: Exceção - {result}")
                    results.append(CreationResult(success=False, error_message=str(result)))
                else:
                    results.append(result)
                    status = "✅" if result.success else "❌"
                    logger.info(f"Conta {i+j+1}: {status}")
            
            # Delay entre lotes
            if batch_end < count:
                delay = random.uniform(30, 60)
                logger.info(f"⏳ Aguardando {delay:.1f}s antes do próximo lote...")
                await asyncio.sleep(delay)
        
        self.stats["end_time"] = time.time()
        self._print_statistics()
        
        return results
    
    def _print_statistics(self):
        """Imprime estatísticas detalhadas"""
        duration = self.stats["end_time"] - self.stats["start_time"]
        success_rate = (self.stats["successful_creations"] / self.stats["total_attempts"]) * 100
        
        print("\n" + "="*60)
        print("📊 ESTATÍSTICAS FINAIS")
        print("="*60)
        print(f"⏱️  Duração total: {duration:.2f}s ({duration/60:.1f}min)")
        print(f"🎯 Tentativas totais: {self.stats['total_attempts']}")
        print(f"✅ Criações bem-sucedidas: {self.stats['successful_creations']}")
        print(f"❌ Falhas: {self.stats['failed_creations']}")
        print(f"📈 Taxa de sucesso: {success_rate:.1f}%")
        if self.stats["successful_creations"] > 0:
            avg_time = duration / self.stats["successful_creations"]
            print(f"⚡ Tempo médio por conta: {avg_time:.2f}s")
        print("="*60)

async def exemplo_criacao_em_lotes():
    """Exemplo de criação em lotes otimizada"""
    print("📦 Exemplo: Criação em Lotes Avançada")
    print("=" * 50)
    
    creator = AdvancedInstagramCreator()
    
    # Configurar para criação rápida
    count = 5
    batch_size = 2
    
    print(f"🎯 Objetivo: {count} contas em lotes de {batch_size}")
    
    results = await creator.batch_creation_with_monitoring(count, batch_size)
    
    # Salvar resultados detalhados
    successful_accounts = [r for r in results if r.success]
    
    if successful_accounts:
        data = []
        for result in successful_accounts:
            data.append({
                "username": result.account_data.username,
                "email": result.account_data.email,
                "password": result.account_data.password,
                "full_name": result.account_data.full_name,
                "creation_time": result.creation_time,
                "timestamp": time.time()
            })
        
        with open("batch_results.json", "w") as f:
            json.dump(data, f, indent=2)
        
        print(f"💾 {len(successful_accounts)} contas salvas em batch_results.json")

async def exemplo_configuracao_dinamica():
    """Exemplo com configuração dinâmica baseada no contexto"""
    print("\n⚙️ Exemplo: Configuração Dinâmica")
    print("=" * 50)
    
    import configparser
    
    # Detectar "horário de pico" (simulado)
    hora_atual = time.localtime().tm_hour
    is_peak_hour = 8 <= hora_atual <= 22  # 8h às 22h
    
    # Configuração adaptativa
    config = configparser.ConfigParser()
    
    if is_peak_hour:
        print("🕐 Horário de pico detectado - configuração conservadora")
        config_content = """
[DELAYS]
min_delay = 5
max_delay = 12
typing_delay = 0.2

[SECURITY]
stealth_mode = true
"""
    else:
        print("🌙 Horário de baixo tráfego - configuração rápida")
        config_content = """
[DELAYS]
min_delay = 2
max_delay = 5
typing_delay = 0.1

[SECURITY]
stealth_mode = true
"""
    
    config.read_string(config_content)
    
    # Salvar configuração temporária
    with open("config_dinamica.ini", "w") as f:
        config.write(f)
    
    try:
        creator = InstagramCreatorAdvanced("config_dinamica.ini")
        result = await creator.create_account()
        
        if result.success:
            print("✅ Configuração dinâmica aplicada com sucesso!")
    
    finally:
        import os
        if os.path.exists("config_dinamica.ini"):
            os.remove("config_dinamica.ini")

async def exemplo_monitoramento_performance():
    """Exemplo com monitoramento de performance em tempo real"""
    print("\n📊 Exemplo: Monitoramento de Performance")
    print("=" * 50)
    
    import psutil
    import threading
    
    # Métricas de sistema
    metrics = {
        "cpu_usage": [],
        "memory_usage": [],
        "creation_times": []
    }
    
    def monitor_system():
        """Monitor de sistema em background"""
        while hasattr(monitor_system, 'running'):
            metrics["cpu_usage"].append(psutil.cpu_percent())
            metrics["memory_usage"].append(psutil.virtual_memory().percent)
            time.sleep(1)
    
    # Iniciar monitoramento
    monitor_system.running = True
    monitor_thread = threading.Thread(target=monitor_system)
    monitor_thread.start()
    
    try:
        creator = InstagramCreatorAdvanced()
        
        # Criar algumas contas medindo performance
        for i in range(3):
            start_time = time.time()
            
            result = await creator.create_account()
            
            creation_time = time.time() - start_time
            metrics["creation_times"].append(creation_time)
            
            print(f"Conta {i+1}: {creation_time:.2f}s")
    
    finally:
        # Parar monitoramento
        delattr(monitor_system, 'running')
        monitor_thread.join()
        
        # Exibir métricas
        if metrics["cpu_usage"]:
            print(f"\n📈 CPU média: {sum(metrics['cpu_usage'])/len(metrics['cpu_usage']):.1f}%")
            print(f"🧠 Memória média: {sum(metrics['memory_usage'])/len(metrics['memory_usage']):.1f}%")
        
        if metrics["creation_times"]:
            avg_time = sum(metrics["creation_times"]) / len(metrics["creation_times"])
            print(f"⚡ Tempo médio de criação: {avg_time:.2f}s")

async def exemplo_proxy_rotation():
    """Exemplo com rotação de proxies (simulado)"""
    print("\n🔄 Exemplo: Rotação de Proxies")
    print("=" * 50)
    
    # Lista de proxies (simulada)
    proxy_list = [
        "http://proxy1:8080",
        "http://proxy2:8080", 
        "http://proxy3:8080"
    ]
    
    print(f"🌐 {len(proxy_list)} proxies disponíveis")
    
    # Para cada conta, usar um proxy diferente
    for i, proxy in enumerate(proxy_list[:2]):  # Limitar a 2 para demo
        print(f"\n🔄 Usando proxy {i+1}: {proxy}")
        
        # Em implementação real, configuraria o proxy aqui
        # Por enquanto, apenas simular
        
        creator = InstagramCreatorAdvanced()
        result = await creator.create_account()
        
        if result.success:
            print(f"✅ Conta criada via proxy {i+1}")
        else:
            print(f"❌ Falha com proxy {i+1}")

async def exemplo_data_analysis():
    """Exemplo de análise de dados das contas criadas"""
    print("\n📈 Exemplo: Análise de Dados")
    print("=" * 50)
    
    # Simular criação de algumas contas
    creator = InstagramCreatorAdvanced()
    results = []
    
    print("🔄 Criando contas para análise...")
    for i in range(3):
        result = await creator.create_account()
        results.append(result)
        
        if result.success:
            print(f"  ✅ Conta {i+1} criada")
    
    # Análise dos resultados
    successful = [r for r in results if r.success]
    
    if successful:
        print(f"\n📊 Análise de {len(successful)} contas criadas:")
        
        # Análise de usernames
        username_lengths = [len(r.account_data.username) for r in successful]
        avg_username_length = sum(username_lengths) / len(username_lengths)
        print(f"📏 Comprimento médio do username: {avg_username_length:.1f}")
        
        # Análise de domínios de email
        email_domains = [r.account_data.email.split('@')[1] for r in successful]
        domain_counts = {}
        for domain in email_domains:
            domain_counts[domain] = domain_counts.get(domain, 0) + 1
        
        print("📧 Distribuição de domínios:")
        for domain, count in domain_counts.items():
            print(f"   {domain}: {count} conta(s)")
        
        # Análise de tempos de criação
        if all(r.creation_time for r in successful):
            creation_times = [r.creation_time for r in successful]
            avg_time = sum(creation_times) / len(creation_times)
            min_time = min(creation_times)
            max_time = max(creation_times)
            
            print(f"⏱️  Tempo de criação:")
            print(f"   Média: {avg_time:.2f}s")
            print(f"   Mínimo: {min_time:.2f}s")
            print(f"   Máximo: {max_time:.2f}s")

async def main():
    """Função principal com exemplos avançados"""
    print("🚀 Instagram Creator Advanced - Exemplos Avançados")
    print("=" * 70)
    
    exemplos = [
        ("Criação em Lotes", exemplo_criacao_em_lotes),
        ("Configuração Dinâmica", exemplo_configuracao_dinamica),
        ("Monitoramento de Performance", exemplo_monitoramento_performance),
        ("Rotação de Proxies", exemplo_proxy_rotation),
        ("Análise de Dados", exemplo_data_analysis)
    ]
    
    for nome, funcao in exemplos:
        try:
            print(f"\n🎯 Executando: {nome}")
            await funcao()
            print(f"✅ {nome} concluído")
            
            # Delay entre exemplos
            await asyncio.sleep(2)
            
        except KeyboardInterrupt:
            print(f"\n❌ Interrompido pelo usuário")
            break
        except Exception as e:
            logger.error(f"Erro em {nome}: {e}")
            continue
    
    print("\n🎉 Exemplos avançados concluídos!")
    print("💡 Explore o código para implementar suas próprias funcionalidades")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Finalizado pelo usuário")
    except Exception as e:
        print(f"\n💥 Erro fatal: {e}")
        sys.exit(1)
