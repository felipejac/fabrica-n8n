"""
OUTPUT LAYER - Gestão de Saída e Metadados SEO
Responsável por salvar posts com frontmatter otimizado e Schema.org
"""

import os
import json
from datetime import datetime
from typing import Dict, List
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SEOPostManager:
    """Gerenciador de posts com metadados SEO e Schema.org"""
    
    def __init__(self, output_dir: str = 'posts'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def save_post_markdown(self, content: str, topic_type: str, 
                          custom_title: str = None, tags: List[str] = None) -> str:
        """
        Salva post em Markdown com frontmatter completo para SEO
        
        Args:
            content: Conteúdo do artigo em Markdown
            topic_type: Tipo de pauta editorial
            custom_title: Título customizado (opcional)
            tags: Lista de tags (opcional)
            
        Returns:
            Caminho do arquivo salvo
        """
        logger.info(f"Salvando post: {topic_type}")
        
        # Extrair título do conteúdo (primeira linha H1)
        title = custom_title or self._extract_title(content)
        
        # Gerar nome do arquivo
        date_str = datetime.now().strftime('%Y-%m-%d')
        filename = f"{date_str}_{topic_type}.md"
        filepath = os.path.join(self.output_dir, filename)
        
        # Gerar metadados SEO
        frontmatter = self._generate_frontmatter(
            title=title,
            topic_type=topic_type,
            content=content,
            tags=tags
        )
        
        # Gerar Schema.org JSON-LD
        schema_org = self._generate_schema_org(
            title=title,
            content=content,
            filepath=filename
        )
        
        # Montar conteúdo final
        full_content = f"{frontmatter}\n\n{content}\n\n{schema_org}"
        
        # Salvar arquivo
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        logger.info(f"✅ Post salvo: {filepath}")
        return filepath
    
    def _extract_title(self, content: str) -> str:
        """Extrai título do conteúdo (primeira linha H1)"""
        for line in content.split('\n'):
            if line.startswith('# '):
                return line.replace('# ', '').strip()
        return 'Artigo Sem Título'
    
    def _generate_frontmatter(self, title: str, topic_type: str, 
                             content: str, tags: List[str] = None) -> str:
        """
        Gera frontmatter YAML otimizado para CMS e SEO
        
        Args:
            title: Título do artigo
            topic_type: Tipo de pauta
            content: Conteúdo completo
            tags: Tags customizadas
            
        Returns:
            Frontmatter formatado em YAML
        """
        # Gerar descrição SEO (primeiro parágrafo não-título)
        seo_description = self._generate_seo_description(content)
        
        # Tags padrão por tipo de tópico
        default_tags = self._get_default_tags(topic_type)
        final_tags = tags if tags else default_tags
        
        # Gerar slug (URL-friendly)
        slug = self._generate_slug(title)
        
        # Data e hora atuais
        now = datetime.now()
        date_iso = now.isoformat()
        date_readable = now.strftime('%Y-%m-%d')
        
        # Categorias
        category = self._get_category(topic_type)
        
        # Autor (pode ser configurável)
        author = "AI Trend Hunter Bot"
        author_twitter = "@aitrendhunter"
        
        frontmatter = f"""---
# SEO METADATA
title: "{title}"
description: "{seo_description}"
slug: "{slug}"
date: {date_iso}
lastmod: {date_iso}

# CLASSIFICATION
category: "{category}"
tags:
{self._format_yaml_list(final_tags)}
topic_type: "{topic_type}"

# AUTHORSHIP
author: "{author}"
author_twitter: "{author_twitter}"

# SEO OPTIMIZATION
featured_image: ""
featured_image_alt: "{title}"
keywords: "{', '.join(final_tags[:10])}"

# SCHEMA.ORG
article_type: "TechArticle"
word_count: {self._count_words(content)}
reading_time: "{self._estimate_reading_time(content)} min"

# PUBLICATION STATUS
published: true
featured: {self._is_featured(topic_type)}
draft: false

# SOCIAL SHARING
og_title: "{title}"
og_description: "{seo_description}"
og_type: "article"
twitter_card: "summary_large_image"
twitter_title: "{title}"
twitter_description: "{seo_description}"

# INDEXING
robots: "index, follow"
canonical_url: ""

# AEO OPTIMIZATION
answer_engine_optimized: true
direct_answer_provided: true
structured_data: true
---"""
        
        return frontmatter
    
    def _generate_seo_description(self, content: str, max_length: int = 155) -> str:
        """
        Gera descrição SEO (meta description) otimizada
        Busca no conteúdo por "Resposta Direta" ou primeiro parágrafo
        """
        # Procurar por seção "Resposta Direta"
        lines = content.split('\n')
        in_direct_answer = False
        
        for i, line in enumerate(lines):
            if '## 📊 Resposta Direta' in line or '## Resposta Direta' in line:
                in_direct_answer = True
                continue
            
            if in_direct_answer and line.strip() and not line.startswith('#'):
                description = line.strip()
                # Truncar se necessário
                if len(description) > max_length:
                    description = description[:max_length-3] + '...'
                return description
        
        # Fallback: primeiro parágrafo após título
        for line in lines:
            if line.strip() and not line.startswith('#') and len(line) > 50:
                description = line.strip()
                if len(description) > max_length:
                    description = description[:max_length-3] + '...'
                return description
        
        return "Análise de tendências em Inteligência Artificial baseada em dados reais do Hugging Face."
    
    def _generate_slug(self, title: str) -> str:
        """Gera slug URL-friendly"""
        import re
        
        slug = title.lower()
        slug = re.sub(r'[àáâãäå]', 'a', slug)
        slug = re.sub(r'[èéêë]', 'e', slug)
        slug = re.sub(r'[ìíîï]', 'i', slug)
        slug = re.sub(r'[òóôõö]', 'o', slug)
        slug = re.sub(r'[ùúûü]', 'u', slug)
        slug = re.sub(r'[ç]', 'c', slug)
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'\s+', '-', slug)
        slug = re.sub(r'-+', '-', slug)
        slug = slug.strip('-')
        
        return slug[:100]  # Limitar tamanho
    
    def _get_default_tags(self, topic_type: str) -> List[str]:
        """Tags padrão por tipo de tópico"""
        tag_mapping = {
            'mito_vs_realidade': [
                'inteligência artificial', 'machine learning', 'análise de dados',
                'hype vs realidade', 'modelos de IA', 'produção', 'data science'
            ],
            'seguranca_juridica': [
                'licenças open source', 'uso comercial', 'MIT', 'Apache 2.0',
                'direito digital', 'compliance', 'segurança jurídica'
            ],
            'cemiterio_projetos': [
                'projetos abandonados', 'manutenção de software', 'open source',
                'sustentabilidade', 'dívida técnica', 'gestão de projetos'
            ],
            'alem_chatgpt': [
                'visão computacional', 'processamento de áudio', 'multimodalidade',
                'computer vision', 'deep learning', 'IA não-texto'
            ],
            'relatorio_mensal': [
                'relatório de mercado', 'análise de tendências', 'hugging face',
                'inteligência artificial', 'panorama de IA', 'data science'
            ]
        }
        
        return tag_mapping.get(topic_type, ['inteligência artificial', 'machine learning'])
    
    def _get_category(self, topic_type: str) -> str:
        """Categoria principal por tipo de tópico"""
        category_mapping = {
            'mito_vs_realidade': 'Análise de Mercado',
            'seguranca_juridica': 'Aspectos Legais',
            'cemiterio_projetos': 'Gestão de Projetos',
            'alem_chatgpt': 'Tecnologias Emergentes',
            'relatorio_mensal': 'Relatórios'
        }
        
        return category_mapping.get(topic_type, 'Tecnologia')
    
    def _format_yaml_list(self, items: List[str]) -> str:
        """Formata lista para YAML"""
        return '\n'.join([f'  - "{item}"' for item in items])
    
    def _count_words(self, content: str) -> int:
        """Conta palavras no conteúdo"""
        import re
        text = re.sub(r'[#*`\[\](){}]', '', content)
        words = text.split()
        return len(words)
    
    def _estimate_reading_time(self, content: str) -> int:
        """Estima tempo de leitura (200 palavras/min)"""
        word_count = self._count_words(content)
        return max(1, round(word_count / 200))
    
    def _is_featured(self, topic_type: str) -> bool:
        """Define se o post é featured (destaque)"""
        # Relatórios mensais sempre são featured
        return topic_type == 'relatorio_mensal'
    
    def _generate_schema_org(self, title: str, content: str, filepath: str) -> str:
        """
        Gera Schema.org JSON-LD para TechArticle
        
        Args:
            title: Título do artigo
            content: Conteúdo completo
            filepath: Nome do arquivo
            
        Returns:
            Schema.org formatado em HTML
        """
        now = datetime.now()
        
        # Extrair primeiro parágrafo como abstract
        abstract = self._generate_seo_description(content, max_length=300)
        
        schema = {
            "@context": "https://schema.org",
            "@type": "TechArticle",
            "headline": title,
            "abstract": abstract,
            "author": {
                "@type": "Organization",
                "name": "AI Trend Hunter",
                "url": "https://aitrendhunter.com"
            },
            "publisher": {
                "@type": "Organization",
                "name": "AI Trend Hunter",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://aitrendhunter.com/logo.png"
                }
            },
            "datePublished": now.isoformat(),
            "dateModified": now.isoformat(),
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": f"https://aitrendhunter.com/blog/{self._generate_slug(title)}"
            },
            "image": f"https://aitrendhunter.com/images/{self._generate_slug(title)}.png",
            "articleBody": content[:500] + "...",
            "wordCount": self._count_words(content),
            "keywords": ", ".join(self._get_default_tags(
                filepath.split('_')[1].replace('.md', '')
            )),
            "inLanguage": "pt-BR",
            "about": {
                "@type": "Thing",
                "name": "Inteligência Artificial",
                "sameAs": "https://www.wikidata.org/wiki/Q11660"
            }
        }
        
        # Formatar como HTML comment com JSON-LD
        schema_html = f"""
<!-- Schema.org JSON-LD -->
<script type="application/ld+json">
{json.dumps(schema, ensure_ascii=False, indent=2)}
</script>
"""
        
        return schema_html
    
    def generate_index(self) -> str:
        """
        Gera arquivo index.md listando todos os posts
        
        Returns:
            Caminho do arquivo index
        """
        logger.info("Gerando índice de posts...")
        
        # Listar todos os posts
        posts = []
        for filename in sorted(os.listdir(self.output_dir), reverse=True):
            if filename.endswith('.md') and filename != 'index.md':
                filepath = os.path.join(self.output_dir, filename)
                
                # Extrair metadados
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    title = self._extract_title(content)
                    date = filename.split('_')[0]
                    
                    posts.append({
                        'filename': filename,
                        'title': title,
                        'date': date
                    })
        
        # Gerar conteúdo do índice
        index_content = f"""# AI Trend Hunter - Índice de Artigos

**Última atualização:** {datetime.now().strftime('%d de %B de %Y')}

Total de artigos: **{len(posts)}**

---

"""
        
        for post in posts:
            index_content += f"## [{post['title']}]({post['filename']})\n"
            index_content += f"**Data:** {post['date']}\n\n"
        
        # Salvar índice
        index_path = os.path.join(self.output_dir, 'index.md')
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_content)
        
        logger.info(f"✅ Índice gerado: {index_path}")
        return index_path


def save_post_markdown(content: str, topic_type: str, output_dir: str = 'posts') -> str:
    """
    Função wrapper para manter compatibilidade com a especificação original
    
    Args:
        content: Conteúdo do post
        topic_type: Tipo de pauta
        output_dir: Diretório de saída
        
    Returns:
        Caminho do arquivo salvo
    """
    manager = SEOPostManager(output_dir=output_dir)
    return manager.save_post_markdown(content, topic_type)


if __name__ == "__main__":
    # Teste da camada de output
    print("=" * 80)
    print("💾 AI TREND HUNTER - OUTPUT LAYER TEST")
    print("=" * 80)
    
    # Criar conteúdo de exemplo
    sample_content = """# Teste de Post com SEO Otimizado

## 📊 Resposta Direta

Este é um post de exemplo para testar a geração de metadados SEO e Schema.org completos.

## Conteúdo Principal

Aqui temos o conteúdo principal do artigo, com várias seções e informações relevantes.

### Seção de Exemplo

- Item 1
- Item 2
- Item 3

---

**Tags:** teste, seo, schema.org, markdown
"""
    
    manager = SEOPostManager(output_dir='posts')
    
    print("\n📝 Salvando post de exemplo...")
    filepath = manager.save_post_markdown(
        content=sample_content,
        topic_type='relatorio_mensal'
    )
    
    print(f"\n✅ Post salvo: {filepath}")
    print(f"\n📄 Visualize o arquivo para ver:")
    print("   - Frontmatter YAML completo")
    print("   - Metadados SEO (title, description, tags)")
    print("   - Open Graph e Twitter Cards")
    print("   - Schema.org JSON-LD")
    
    print(f"\n📑 Gerando índice...")
    index_path = manager.generate_index()
    print(f"✅ Índice criado: {index_path}")
