#!/usr/bin/env python3
"""
AI TREND HUNTER - ORQUESTRADOR PRINCIPAL
Sistema automatizado de análise de tendências em IA e geração de conteúdo otimizado

Autor: AI Trend Hunter Bot
Data: 2025-12-12
Versão: 1.0.0

PIPELINE COMPLETO:
1. DATA LAYER: Extração de dados do Hugging Face
2. ANALYSIS LAYER: Análise de tendências e segmentação editorial
3. CONTENT LAYER: Geração de conteúdo AEO (Answer Engine Optimization)
4. OUTPUT LAYER: Salvamento com metadados SEO e Schema.org
"""

import sys
import os
import logging
from datetime import datetime
from typing import List, Dict

# Adicionar diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar módulos do projeto
from data.fetch_market_data import HuggingFaceDataFetcher
from analysis.trend_analyzer import TrendAnalyzer
from content.aeo_generator import AEOContentGenerator
from output.seo_manager import SEOPostManager
from config import (
    HUGGINGFACE_CONFIG, ANALYSIS_CONFIG, CONTENT_CONFIG, 
    OUTPUT_CONFIG, EXECUTION_CONFIG
)

# Configurar logging
logging.basicConfig(
    level=logging.INFO if EXECUTION_CONFIG['verbose'] else logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('ai_trend_hunter.log')
    ]
)
logger = logging.getLogger(__name__)


class AITrendHunter:
    """Orquestrador principal do sistema AI Trend Hunter"""
    
    def __init__(self):
        """Inicializa todos os componentes do pipeline"""
        logger.info("🚀 Inicializando AI Trend Hunter...")
        
        # Inicializar componentes
        self.data_fetcher = HuggingFaceDataFetcher()
        self.analyzer = TrendAnalyzer()
        self.content_generator = AEOContentGenerator()
        self.seo_manager = SEOPostManager(
            output_dir=OUTPUT_CONFIG['posts_directory']
        )
        
        # Estado
        self.raw_data = None
        self.analyzed_data = None
        self.segments = None
        self.insights = None
        self.generated_posts = []
        
        logger.info("✅ AI Trend Hunter inicializado com sucesso")
    
    def run(self, topics: List[str] = None) -> Dict[str, any]:
        """
        Executa o pipeline completo de análise e geração de conteúdo
        
        Args:
            topics: Lista de tópicos a gerar (None = todos)
            
        Returns:
            Dicionário com resultados da execução
        """
        start_time = datetime.now()
        logger.info("=" * 80)
        logger.info("🎯 INICIANDO EXECUÇÃO DO AI TREND HUNTER")
        logger.info("=" * 80)
        
        try:
            # ETAPA 1: Extração de Dados
            logger.info("\n📥 ETAPA 1/4: EXTRAÇÃO DE DADOS")
            self._execute_data_extraction()
            
            # ETAPA 2: Análise de Tendências
            logger.info("\n📊 ETAPA 2/4: ANÁLISE DE TENDÊNCIAS")
            self._execute_trend_analysis()
            
            # ETAPA 3: Geração de Conteúdo
            logger.info("\n📝 ETAPA 3/4: GERAÇÃO DE CONTEÚDO")
            self._execute_content_generation(topics)
            
            # ETAPA 4: Pós-processamento
            logger.info("\n💾 ETAPA 4/4: PÓS-PROCESSAMENTO")
            self._execute_post_processing()
            
            # Calcular duração
            duration = (datetime.now() - start_time).total_seconds()
            
            # Resultado
            result = {
                'success': True,
                'duration_seconds': duration,
                'models_analyzed': len(self.raw_data) if self.raw_data is not None else 0,
                'posts_generated': len(self.generated_posts),
                'post_files': self.generated_posts,
                'execution_date': datetime.now().isoformat()
            }
            
            logger.info("\n" + "=" * 80)
            logger.info("✅ EXECUÇÃO CONCLUÍDA COM SUCESSO")
            logger.info("=" * 80)
            logger.info(f"⏱️  Duração: {duration:.2f} segundos")
            logger.info(f"📊 Modelos analisados: {result['models_analyzed']}")
            logger.info(f"📝 Posts gerados: {result['posts_generated']}")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ ERRO NA EXECUÇÃO: {e}", exc_info=True)
            return {
                'success': False,
                'error': str(e),
                'execution_date': datetime.now().isoformat()
            }
    
    def _execute_data_extraction(self):
        """ETAPA 1: Extrai dados do Hugging Face"""
        logger.info("🔍 Buscando dados do Hugging Face...")
        
        # Determinar limite baseado no modo
        limit = (
            EXECUTION_CONFIG['test_mode_limit'] 
            if EXECUTION_CONFIG['mode'] == 'test' 
            else HUGGINGFACE_CONFIG['model_limit']
        )
        
        # Buscar dados
        self.raw_data = self.data_fetcher.fetch_market_data(limit=limit)
        
        logger.info(f"✅ {len(self.raw_data)} modelos extraídos")
        
        # Salvar dados brutos se configurado
        if EXECUTION_CONFIG['save_raw_data']:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filepath = f"{OUTPUT_CONFIG['data_directory']}/raw_data_{timestamp}.csv"
            self.data_fetcher.save_raw_data(self.raw_data, filepath)
            logger.info(f"💾 Dados brutos salvos: {filepath}")
    
    def _execute_trend_analysis(self):
        """ETAPA 2: Analisa tendências e segmenta pautas"""
        logger.info("📈 Analisando tendências...")
        
        # Analisar dados
        self.analyzed_data = self.analyzer.analyze_trends(self.raw_data)
        
        logger.info(f"✅ Análise concluída: {len(self.analyzed_data)} modelos analisados")
        
        # Segmentar pautas editoriais
        logger.info("📋 Segmentando pautas editoriais...")
        self.segments = self.analyzer.segment_editorial_topics(self.analyzed_data)
        
        logger.info(f"✅ {len(self.segments)} pautas segmentadas:")
        for topic, data in self.segments.items():
            logger.info(f"   - {topic}: {len(data)} modelos")
        
        # Gerar insights
        self.insights = self.analyzer.generate_insights(self.analyzed_data)
        logger.info("✅ Insights estatísticos gerados")
    
    def _execute_content_generation(self, topics: List[str] = None):
        """ETAPA 3: Gera conteúdo para cada pauta"""
        # Determinar quais tópicos gerar
        if topics:
            topics_to_generate = topics
        elif EXECUTION_CONFIG.get('generation_strategy') == 'daily_rotation':
            # Rotação automática baseada no dia da semana
            topics_to_generate = self._get_daily_topics()
        elif EXECUTION_CONFIG.get('topics_to_generate'):
            topics_to_generate = EXECUTION_CONFIG['topics_to_generate']
        else:
            topics_to_generate = CONTENT_CONFIG['editorial_topics']
        
        logger.info(f"📝 Gerando conteúdo para {len(topics_to_generate)} tópicos...")
        
        for topic in topics_to_generate:
            if topic not in self.segments:
                logger.warning(f"⚠️  Tópico '{topic}' não encontrado, pulando...")
                continue
            
            logger.info(f"   Gerando: {topic}...")
            
            try:
                # Gerar conteúdo
                content = self.content_generator.generate_blog_post(
                    topic_type=topic,
                    data_segment=self.segments[topic],
                    insights=self.insights
                )
                
                # Salvar post
                filepath = self.seo_manager.save_post_markdown(
                    content=content,
                    topic_type=topic
                )
                
                self.generated_posts.append(filepath)
                logger.info(f"   ✅ Post salvo: {filepath}")
                
            except Exception as e:
                logger.error(f"   ❌ Erro ao gerar '{topic}': {e}")
        
        logger.info(f"✅ {len(self.generated_posts)} posts gerados com sucesso")
    
    def _get_daily_topics(self) -> List[str]:
        """
        Retorna os tópicos a gerar baseado no dia da semana
        
        Returns:
            Lista de tópicos para o dia atual
        """
        if not EXECUTION_CONFIG.get('use_weekly_rotation'):
            # Fallback: pegar os N primeiros tópicos
            count = CONTENT_CONFIG.get('daily_posts_count', 2)
            return CONTENT_CONFIG['editorial_topics'][:count]
        
        from datetime import datetime
        
        # Dia da semana (0=segunda, 6=domingo)
        weekday = datetime.now().weekday()
        
        # Buscar tópicos do dia
        daily_topics = CONTENT_CONFIG.get('weekly_rotation', {}).get(weekday, [])
        
        if not daily_topics:
            # Se não houver tópicos definidos para hoje (fim de semana)
            logger.info(f"⏸️  Sem artigos programados para hoje ({['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'][weekday]})")
            return []
        
        logger.info(f"📅 Dia da semana: {['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'][weekday]}")
        logger.info(f"📋 Tópicos do dia: {', '.join(daily_topics)}")
        
        return daily_topics
    
    def _execute_post_processing(self):
        """ETAPA 4: Pós-processamento (índice, etc)"""
        # Gerar índice se configurado
        if EXECUTION_CONFIG['auto_generate_index']:
            logger.info("📑 Gerando índice de posts...")
            index_path = self.seo_manager.generate_index()
            logger.info(f"✅ Índice criado: {index_path}")
        
        logger.info("✅ Pós-processamento concluído")


def main():
    """Função principal de execução"""
    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                          AI TREND HUNTER v1.0.0                           ║
║                  Sistema Automatizado de Análise de IA                    ║
╚═══════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Criar e executar orquestrador
    hunter = AITrendHunter()
    result = hunter.run()
    
    # Exibir resumo final
    if result['success']:
        print("\n" + "=" * 80)
        print("🎉 EXECUÇÃO FINALIZADA COM SUCESSO")
        print("=" * 80)
        print(f"\n📊 ESTATÍSTICAS:")
        print(f"   • Modelos analisados: {result['models_analyzed']}")
        print(f"   • Posts gerados: {result['posts_generated']}")
        print(f"   • Tempo de execução: {result['duration_seconds']:.2f}s")
        print(f"\n📁 ARQUIVOS GERADOS:")
        for filepath in result['post_files']:
            print(f"   • {filepath}")
        print("\n✅ Todos os posts estão prontos para publicação!")
        print("   Verifique a pasta 'posts/' para os arquivos Markdown")
        print("\n" + "=" * 80)
        
        return 0
    else:
        print("\n" + "=" * 80)
        print("❌ ERRO NA EXECUÇÃO")
        print("=" * 80)
        print(f"\n⚠️  {result.get('error', 'Erro desconhecido')}")
        print("\n📝 Verifique o arquivo 'ai_trend_hunter.log' para mais detalhes")
        print("=" * 80)
        
        return 1


if __name__ == "__main__":
    sys.exit(main())
