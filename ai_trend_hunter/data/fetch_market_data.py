"""
DATA LAYER - Extração de Dados do Hugging Face
Responsável por buscar e normalizar dados de modelos de IA
"""

import os
import pandas as pd
from huggingface_hub import HfApi
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class HuggingFaceDataFetcher:
    """Extrator de dados do Hugging Face Hub"""
    
    def __init__(self):
        self.api = HfApi()
        self.license_mapping = {
            'mit': 'MIT',
            'apache': 'Apache 2.0',
            'apache-2.0': 'Apache 2.0',
            'openrail': 'OpenRAIL',
            'openrail++': 'OpenRAIL++',
            'cc-by': 'CC-BY',
            'cc-by-nc': 'CC-BY-NC',
            'gpl': 'GPL',
            'bsd': 'BSD',
            'unlicense': 'Unlicense',
            'other': 'Other'
        }
    
    def fetch_market_data(self, limit: int = 200) -> pd.DataFrame:
        """
        Busca os top modelos do Hugging Face ordenados por downloads
        
        Args:
            limit: Número de modelos a buscar (default: 200)
            
        Returns:
            DataFrame com dados normalizados dos modelos
        """
        logger.info(f"Iniciando busca dos top {limit} modelos no Hugging Face...")
        
        try:
            # Buscar modelos ordenados por downloads
            models = self.api.list_models(
                sort='downloads',
                direction=-1,
                limit=limit,
                full=True  # Buscar dados completos
            )
            
            # Extrair dados relevantes
            data = []
            for model in models:
                try:
                    model_data = {
                        'modelId': model.modelId,
                        'downloads': getattr(model, 'downloads', 0) or 0,
                        'likes': getattr(model, 'likes', 0) or 0,
                        'pipeline_tag': getattr(model, 'pipeline_tag', 'unknown'),
                        'lastModified': getattr(model, 'lastModified', None),
                        'tags': getattr(model, 'tags', []),
                        'author': model.modelId.split('/')[0] if '/' in model.modelId else 'unknown',
                        'model_name': model.modelId.split('/')[-1] if '/' in model.modelId else model.modelId,
                        'library_name': getattr(model, 'library_name', 'unknown'),
                        'created_at': getattr(model, 'created_at', None)
                    }
                    data.append(model_data)
                except Exception as e:
                    logger.warning(f"Erro ao processar modelo {model.modelId}: {e}")
                    continue
            
            logger.info(f"✅ {len(data)} modelos extraídos com sucesso")
            
            # Criar DataFrame
            df = pd.DataFrame(data)
            
            # Normalizar dados
            df = self._normalize_data(df)
            
            return df
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar dados do Hugging Face: {e}")
            raise
    
    def _normalize_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Normaliza e limpa os dados extraídos
        
        Args:
            df: DataFrame bruto
            
        Returns:
            DataFrame normalizado
        """
        logger.info("Normalizando dados...")
        
        # Converter datas para datetime
        if 'lastModified' in df.columns:
            df['lastModified'] = pd.to_datetime(df['lastModified'], errors='coerce')
        
        if 'created_at' in df.columns:
            df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
        
        # Normalizar licenças
        df['license'] = df['tags'].apply(self._extract_license)
        df['license_normalized'] = df['license'].apply(self._normalize_license)
        
        # Garantir valores numéricos
        df['downloads'] = pd.to_numeric(df['downloads'], errors='coerce').fillna(0).astype(int)
        df['likes'] = pd.to_numeric(df['likes'], errors='coerce').fillna(0).astype(int)
        
        # Extrair categorias de tags
        df['is_multilingual'] = df['tags'].apply(lambda x: any('multilingual' in str(tag).lower() for tag in x))
        df['is_quantized'] = df['tags'].apply(lambda x: any('quantized' in str(tag).lower() or 'gguf' in str(tag).lower() for tag in x))
        df['languages'] = df['tags'].apply(self._extract_languages)
        
        # Ordenar por downloads
        df = df.sort_values('downloads', ascending=False).reset_index(drop=True)
        df['rank'] = df.index + 1
        
        logger.info(f"✅ Dados normalizados: {len(df)} modelos")
        
        return df
    
    def _extract_license(self, tags: List[str]) -> str:
        """Extrai licença das tags"""
        if not isinstance(tags, list):
            return 'unknown'
        
        for tag in tags:
            tag_lower = str(tag).lower()
            if 'license:' in tag_lower:
                return tag.split(':')[1].strip()
        
        return 'unknown'
    
    def _normalize_license(self, license_str: str) -> str:
        """Normaliza nome da licença"""
        if not license_str or license_str == 'unknown':
            return 'Unknown'
        
        license_lower = license_str.lower()
        
        for key, value in self.license_mapping.items():
            if key in license_lower:
                return value
        
        return license_str.title()
    
    def _extract_languages(self, tags: List[str]) -> List[str]:
        """Extrai idiomas das tags"""
        if not isinstance(tags, list):
            return []
        
        languages = []
        language_tags = ['en', 'pt', 'es', 'fr', 'de', 'zh', 'ja', 'ko', 'ru', 'ar']
        
        for tag in tags:
            tag_lower = str(tag).lower()
            if 'language:' in tag_lower:
                lang = tag.split(':')[1].strip()
                languages.append(lang)
            elif any(lang in tag_lower for lang in language_tags):
                for lang in language_tags:
                    if lang in tag_lower:
                        languages.append(lang)
        
        return list(set(languages))
    
    def save_raw_data(self, df: pd.DataFrame, filepath: str = None) -> str:
        """
        Salva dados brutos em CSV para análise posterior
        
        Args:
            df: DataFrame a salvar
            filepath: Caminho do arquivo (opcional)
            
        Returns:
            Caminho do arquivo salvo
        """
        if filepath is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filepath = f'data/raw_data_{timestamp}.csv'
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        df.to_csv(filepath, index=False, encoding='utf-8')
        
        logger.info(f"✅ Dados salvos em: {filepath}")
        return filepath


def fetch_market_data(limit: int = 200) -> pd.DataFrame:
    """
    Função wrapper para manter compatibilidade com a especificação original
    
    Args:
        limit: Número de modelos a buscar
        
    Returns:
        DataFrame com dados do mercado
    """
    fetcher = HuggingFaceDataFetcher()
    return fetcher.fetch_market_data(limit=limit)


if __name__ == "__main__":
    # Teste da extração
    print("=" * 80)
    print("🔍 AI TREND HUNTER - DATA LAYER TEST")
    print("=" * 80)
    
    fetcher = HuggingFaceDataFetcher()
    df = fetcher.fetch_market_data(limit=50)
    
    print("\n📊 RESUMO DOS DADOS EXTRAÍDOS:")
    print(f"Total de modelos: {len(df)}")
    print(f"\nTop 10 modelos por downloads:")
    print(df[['rank', 'modelId', 'downloads', 'likes', 'pipeline_tag']].head(10).to_string(index=False))
    
    print(f"\n📁 Salvando dados...")
    filepath = fetcher.save_raw_data(df)
    print(f"✅ Arquivo salvo: {filepath}")
