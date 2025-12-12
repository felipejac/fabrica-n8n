"""
Arquivo de configuração central do AI Trend Hunter
"""

import os
from typing import Dict, Any

# ============================================================================
# CONFIGURAÇÕES DO HUGGING FACE
# ============================================================================

HUGGINGFACE_CONFIG = {
    # Número de modelos a buscar do Hugging Face
    'model_limit': 200,
    
    # Critério de ordenação
    'sort_by': 'downloads',
    
    # Direção da ordenação (-1 = descendente)
    'sort_direction': -1,
    
    # Token de autenticação (opcional - para APIs privadas)
    'hf_token': os.getenv('HUGGINGFACE_TOKEN', None)
}


# ============================================================================
# CONFIGURAÇÕES DE ANÁLISE
# ============================================================================

ANALYSIS_CONFIG = {
    # Licenças consideradas seguras para uso comercial
    'commercial_safe_licenses': ['MIT', 'Apache 2.0', 'BSD', 'Unlicense'],
    
    # Dias desde última atualização para considerar projeto ativo
    'active_threshold_days': 90,
    
    # Dias para considerar projeto estagnado
    'stagnant_threshold_days': 180,
    
    # Dias para considerar projeto abandonado
    'abandoned_threshold_days': 365,
    
    # Limites para categorização de Hype Ratio
    'hype_ratio_thresholds': {
        'production_tool': 10000,
        'professional_use': 1000,
        'moderate_use': 100
    }
}


# ============================================================================
# CONFIGURAÇÕES DE CONTEÚDO
# ============================================================================

CONTENT_CONFIG = {
    # Tipos de pautas editoriais disponíveis
    'editorial_topics': [
        'mito_vs_realidade',
        'seguranca_juridica',
        'cemiterio_projetos',
        'alem_chatgpt',
        'relatorio_mensal'
    ],
    
    # CONFIGURAÇÃO DE PUBLICAÇÃO DIÁRIA
    'daily_posts_count': 2,  # Quantos artigos gerar por dia
    
    # Rotação semanal (2 artigos/dia = 10 artigos/semana útil)
    'weekly_rotation': {
        0: ['mito_vs_realidade', 'alem_chatgpt'],        # Segunda
        1: ['seguranca_juridica', 'cemiterio_projetos'], # Terça
        2: ['mito_vs_realidade', 'seguranca_juridica'],  # Quarta
        3: ['alem_chatgpt', 'cemiterio_projetos'],       # Quinta
        4: ['relatorio_mensal', 'mito_vs_realidade'],    # Sexta (+ relatório semanal)
        5: [],  # Sábado (pausa)
        6: []   # Domingo (pausa)
    },
    
    # Número de modelos por segmento editorial
    'models_per_segment': {
        'mito_vs_realidade': 20,  # 10 reais + 10 hype
        'seguranca_juridica': 20,
        'cemiterio_projetos': 15,
        'alem_chatgpt': 20,
        'relatorio_mensal': 30
    },
    
    # Palavras por minuto para cálculo de tempo de leitura
    'reading_speed_wpm': 200,
    
    # Comprimento máximo da descrição SEO
    'seo_description_max_length': 155
}


# ============================================================================
# CONFIGURAÇÕES DE OUTPUT
# ============================================================================

OUTPUT_CONFIG = {
    # Diretório para salvar posts gerados
    'posts_directory': 'ai_trend_hunter/posts',
    
    # Diretório para salvar dados brutos (CSV)
    'data_directory': 'ai_trend_hunter/data',
    
    # Formato do nome dos arquivos
    'filename_format': '{date}_{topic_type}.md',
    
    # Data format para nomes de arquivo
    'date_format': '%Y-%m-%d',
    
    # Informações do autor
    'author': {
        'name': 'AI Trend Hunter Bot',
        'twitter': '@aitrendhunter',
        'website': 'https://aitrendhunter.com',
        'logo_url': 'https://aitrendhunter.com/logo.png'
    }
}


# ============================================================================
# CONFIGURAÇÕES DE SEO
# ============================================================================

SEO_CONFIG = {
    # URL base do site (para canonical e Schema.org)
    'site_url': 'https://aitrendhunter.com',
    
    # Nome do site
    'site_name': 'AI Trend Hunter',
    
    # Robots meta tag padrão
    'robots_default': 'index, follow',
    
    # Open Graph type padrão
    'og_type': 'article',
    
    # Twitter card type padrão
    'twitter_card': 'summary_large_image',
    
    # Schema.org type padrão
    'schema_type': 'TechArticle',
    
    # Idioma do conteúdo
    'content_language': 'pt-BR'
}


# ============================================================================
# CONFIGURAÇÕES DE EXECUÇÃO
# ============================================================================

EXECUTION_CONFIG = {
    # Modo de execução
    'mode': 'production',  # 'production' ou 'test'
    
    # Limite de modelos em modo teste
    'test_mode_limit': 50,
    
    # Verbose logging
    'verbose': True,
    
    # Salvar dados brutos em CSV
    'save_raw_data': True,
    
    # Gerar índice de posts automaticamente
    'auto_generate_index': True,
    
    # ESTRATÉGIA DE GERAÇÃO
    'generation_strategy': 'daily_rotation',  # 'all', 'daily_rotation', ou 'custom'
    
    # Tópicos a gerar (usado apenas se generation_strategy = 'custom')
    'topics_to_generate': None,  # ou lista: ['relatorio_mensal', 'mito_vs_realidade']
    
    # Usar rotação semanal automática
    'use_weekly_rotation': True,  # Se True, usa CONTENT_CONFIG['weekly_rotation']
}


# ============================================================================
# CONFIGURAÇÕES DE INTEGRAÇÃO (FUTURAS)
# ============================================================================

INTEGRATION_CONFIG = {
    # OpenAI API (para geração de conteúdo com LLM - futuro)
    'openai_api_key': os.getenv('OPENAI_API_KEY', None),
    'openai_model': 'gpt-4',
    
    # Anthropic Claude API (alternativa - futuro)
    'anthropic_api_key': os.getenv('ANTHROPIC_API_KEY', None),
    'anthropic_model': 'claude-3-opus-20240229',
    
    # WordPress API (para publicação automática - futuro)
    'wordpress_url': os.getenv('WORDPRESS_URL', None),
    'wordpress_username': os.getenv('WORDPRESS_USERNAME', None),
    'wordpress_password': os.getenv('WORDPRESS_PASSWORD', None),
    
    # GitHub Pages (para publicação - futuro)
    'github_token': os.getenv('GITHUB_TOKEN', None),
    'github_repo': os.getenv('GITHUB_REPO', None)
}


# ============================================================================
# FUNÇÃO HELPER PARA OBTER CONFIGURAÇÕES
# ============================================================================

def get_config(section: str = None) -> Dict[str, Any]:
    """
    Retorna configurações por seção ou todas
    
    Args:
        section: Nome da seção (opcional)
        
    Returns:
        Dicionário com configurações
    """
    all_configs = {
        'huggingface': HUGGINGFACE_CONFIG,
        'analysis': ANALYSIS_CONFIG,
        'content': CONTENT_CONFIG,
        'output': OUTPUT_CONFIG,
        'seo': SEO_CONFIG,
        'execution': EXECUTION_CONFIG,
        'integration': INTEGRATION_CONFIG
    }
    
    if section:
        return all_configs.get(section, {})
    
    return all_configs


if __name__ == "__main__":
    # Exibir todas as configurações
    import json
    
    print("=" * 80)
    print("⚙️  AI TREND HUNTER - CONFIGURAÇÕES")
    print("=" * 80)
    
    all_configs = get_config()
    
    for section_name, section_config in all_configs.items():
        print(f"\n📁 {section_name.upper()}")
        print("-" * 80)
        print(json.dumps(section_config, indent=2, ensure_ascii=False))
