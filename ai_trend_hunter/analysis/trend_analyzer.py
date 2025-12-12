"""
ANALYSIS LAYER - Inteligência de Dados e Análise de Tendências
Responsável por analisar dados extraídos e segmentar pautas editoriais
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TrendAnalyzer:
    """Analisador de tendências de modelos de IA"""
    
    def __init__(self):
        self.commercial_licenses = ['MIT', 'Apache 2.0', 'BSD', 'Unlicense']
        self.analysis_date = datetime.now()
    
    def analyze_trends(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Analisa tendências e cria métricas de inteligência
        
        Args:
            df: DataFrame com dados de modelos
            
        Returns:
            DataFrame enriquecido com análises
        """
        logger.info("Iniciando análise de tendências...")
        
        df = df.copy()
        
        # 1. HYPE RATIO - Diferencia ferramentas de trabalho de marketing
        df['Hype_Ratio'] = df.apply(self._calculate_hype_ratio, axis=1)
        df['Hype_Category'] = df['Hype_Ratio'].apply(self._categorize_hype)
        
        # 2. SEGURANÇA COMERCIAL
        df['Is_Commercial_Safe'] = df['license_normalized'].apply(
            lambda x: x in self.commercial_licenses
        )
        
        # 3. SAÚDE DO PROJETO
        df['Project_Health'] = df['lastModified'].apply(self._assess_project_health)
        df['Days_Since_Update'] = df['lastModified'].apply(
            lambda x: (self.analysis_date - x.tz_localize(None) if hasattr(x, 'tz') and x.tz is not None else self.analysis_date - x).days if pd.notna(x) else None
        )
        
        # 4. MÉTRICAS ADICIONAIS
        df['Engagement_Score'] = df['likes'] / (df['downloads'] / 1000 + 1)
        df['Popularity_Tier'] = pd.qcut(
            df['downloads'], 
            q=5, 
            labels=['Nicho', 'Emergente', 'Popular', 'Muito Popular', 'Viral'],
            duplicates='drop'
        )
        
        # 5. ANÁLISE DE TAREFAS
        df['Task_Category'] = df['pipeline_tag'].apply(self._categorize_task)
        
        logger.info("✅ Análise de tendências concluída")
        return df
    
    def _calculate_hype_ratio(self, row) -> float:
        """
        Calcula a razão Hype (Downloads / Likes)
        Alta razão = ferramenta de trabalho real
        Baixa razão = muito marketing, pouco uso
        """
        if row['likes'] == 0:
            return row['downloads'] / 1  # Evita divisão por zero
        return row['downloads'] / row['likes']
    
    def _categorize_hype(self, ratio: float) -> str:
        """Categoriza o nível de hype"""
        if ratio > 10000:
            return 'Ferramenta de Produção'
        elif ratio > 1000:
            return 'Uso Profissional'
        elif ratio > 100:
            return 'Uso Moderado'
        else:
            return 'Muito Marketing'
    
    def _assess_project_health(self, last_modified) -> str:
        """Avalia a saúde do projeto baseado na última atualização"""
        if pd.isna(last_modified):
            return 'Desconhecido'
        
        # Converter para timezone-naive se necessário
        if hasattr(last_modified, 'tz') and last_modified.tz is not None:
            last_modified = last_modified.tz_localize(None)
        
        days_ago = (self.analysis_date - last_modified).days
        
        if days_ago <= 30:
            return 'Muito Ativo'
        elif days_ago <= 90:
            return 'Ativo'
        elif days_ago <= 180:
            return 'Moderado'
        elif days_ago <= 365:
            return 'Estagnado'
        else:
            return 'Abandonado'
    
    def _categorize_task(self, pipeline_tag: str) -> str:
        """Categoriza a tarefa do modelo"""
        if not pipeline_tag or pipeline_tag == 'unknown':
            return 'Outros'
        
        categories = {
            'Texto': ['text-generation', 'text-classification', 'translation', 
                     'summarization', 'question-answering', 'fill-mask'],
            'Visão': ['image-classification', 'object-detection', 'image-segmentation',
                     'image-to-text', 'text-to-image'],
            'Áudio': ['automatic-speech-recognition', 'audio-classification', 
                     'text-to-speech', 'audio-to-audio'],
            'Multimodal': ['visual-question-answering', 'image-text-to-text',
                          'document-question-answering'],
            'Código': ['code-generation', 'text-to-code']
        }
        
        for category, tags in categories.items():
            if any(tag in pipeline_tag.lower() for tag in tags):
                return category
        
        return 'Outros'
    
    def segment_editorial_topics(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        Segmenta dados em 5 pautas editoriais estratégicas
        
        Args:
            df: DataFrame analisado
            
        Returns:
            Dicionário com 5 DataFrames segmentados
        """
        logger.info("Segmentando pautas editoriais...")
        
        segments = {}
        
        # 1. MITO VS REALIDADE - Hype alto vs baixo
        production_tools = df[df['Hype_Category'] == 'Ferramenta de Produção'].head(10)
        marketing_hype = df[df['Hype_Category'] == 'Muito Marketing'].head(10)
        
        segments['mito_vs_realidade'] = pd.concat([
            production_tools.assign(Categoria='Ferramenta Real'),
            marketing_hype.assign(Categoria='Marketing Puro')
        ])
        
        # 2. SEGURANÇA JURÍDICA - Safe for Commercial Use
        segments['seguranca_juridica'] = df[
            df['Is_Commercial_Safe'] == True
        ].head(20).copy()
        
        # 3. CEMITÉRIO DE PROJETOS - Famosos mas abandonados
        famous_abandoned = df[
            (df['downloads'] > df['downloads'].quantile(0.75)) &  # Top 25% em downloads
            (df['Project_Health'].isin(['Estagnado', 'Abandonado']))
        ].head(15)
        
        segments['cemiterio_projetos'] = famous_abandoned.copy()
        
        # 4. ALÉM DO CHATGPT - Modelos não-texto
        beyond_text = df[
            df['Task_Category'] != 'Texto'
        ].head(20)
        
        segments['alem_chatgpt'] = beyond_text.copy()
        
        # 5. RELATÓRIO MENSAL - Top modelos gerais
        segments['relatorio_mensal'] = df.head(30).copy()
        
        logger.info(f"✅ {len(segments)} pautas editoriais segmentadas")
        
        return segments
    
    def generate_insights(self, df: pd.DataFrame) -> Dict[str, any]:
        """
        Gera insights estatísticos para o relatório
        
        Args:
            df: DataFrame analisado
            
        Returns:
            Dicionário com insights
        """
        insights = {
            'total_models': len(df),
            'total_downloads': df['downloads'].sum(),
            'total_likes': df['likes'].sum(),
            'avg_hype_ratio': df['Hype_Ratio'].mean(),
            'commercial_safe_pct': (df['Is_Commercial_Safe'].sum() / len(df)) * 100,
            'active_projects_pct': (
                df['Project_Health'].isin(['Muito Ativo', 'Ativo']).sum() / len(df)
            ) * 100,
            'top_task_category': df['Task_Category'].value_counts().index[0],
            'top_license': df['license_normalized'].value_counts().index[0],
            'most_popular_model': df.iloc[0]['modelId'],
            'most_hyped_model': df.nlargest(1, 'Hype_Ratio').iloc[0]['modelId'],
            'newest_update': df['lastModified'].max(),
            'oldest_update': df['lastModified'].min()
        }
        
        return insights


def analyze_trends(df: pd.DataFrame) -> pd.DataFrame:
    """
    Função wrapper para manter compatibilidade com a especificação original
    
    Args:
        df: DataFrame com dados brutos
        
    Returns:
        DataFrame com análises
    """
    analyzer = TrendAnalyzer()
    return analyzer.analyze_trends(df)


if __name__ == "__main__":
    # Teste da análise (requer dados do data layer)
    print("=" * 80)
    print("📊 AI TREND HUNTER - ANALYSIS LAYER TEST")
    print("=" * 80)
    
    # Simular dados para teste
    from data.fetch_market_data import fetch_market_data
    
    print("\n🔍 Buscando dados do Hugging Face...")
    df_raw = fetch_market_data(limit=100)
    
    print("\n📈 Analisando tendências...")
    analyzer = TrendAnalyzer()
    df_analyzed = analyzer.analyze_trends(df_raw)
    
    print("\n✅ ANÁLISE CONCLUÍDA")
    print(f"\nMétricas adicionadas: Hype_Ratio, Project_Health, Is_Commercial_Safe")
    print(f"\nDistribuição de Hype:")
    print(df_analyzed['Hype_Category'].value_counts())
    
    print(f"\nSaúde dos Projetos:")
    print(df_analyzed['Project_Health'].value_counts())
    
    print("\n📝 Segmentando pautas editoriais...")
    segments = analyzer.segment_editorial_topics(df_analyzed)
    
    print(f"\n✅ {len(segments)} pautas criadas:")
    for topic, data in segments.items():
        print(f"  - {topic}: {len(data)} modelos")
    
    print("\n💡 Insights:")
    insights = analyzer.generate_insights(df_analyzed)
    for key, value in insights.items():
        print(f"  - {key}: {value}")
