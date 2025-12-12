#!/usr/bin/env python3
"""
Publicador Automático de Posts do AI Trend Hunter para Blog HTML
Converte artigos .md para HTML e publica automaticamente
"""

import os
import re
import yaml
from datetime import datetime
from pathlib import Path

# Configurações
POSTS_DIR = Path(__file__).parent / "ai_trend_hunter" / "posts"
BLOG_DIR = Path(__file__).parent.parent / "blog"
SITEMAP_PATH = Path(__file__).parent.parent / "sitemap-blog.xml"
BLOG_INDEX_PATH = BLOG_DIR / "index.html"

# Mapeamento de emojis por categoria
EMOJI_MAP = {
    'Análise de Mercado': '📊',
    'Relatórios': '📈',
    'Segurança': '🔒',
    'Análise Técnica': '🔧',
    'Tendências': '🚀',
    'Default': '🤖'
}

def parse_markdown_post(md_path):
    """Parse arquivo markdown e extrai frontmatter + conteúdo"""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extrair frontmatter YAML
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = yaml.safe_load(parts[1])
            markdown_content = parts[2].strip()
            return frontmatter, markdown_content
    
    return {}, content

def markdown_to_html(markdown_text):
    """Converte markdown simples para HTML"""
    html = markdown_text
    
    # Headers
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    
    # Bold e Italic
    html = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', html)
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    
    # Links
    html = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2" target="_blank" rel="noopener">\1</a>', html)
    
    # Listas
    html = re.sub(r'^\- (.+?)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'(<li>.*?</li>)', r'<ul>\1</ul>', html, flags=re.DOTALL)
    
    # Code blocks
    html = re.sub(r'```(\w+)?\n(.*?)\n```', r'<pre><code class="language-\1">\2</code></pre>', html, flags=re.DOTALL)
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    
    # Parágrafos
    paragraphs = html.split('\n\n')
    formatted_paragraphs = []
    for p in paragraphs:
        p = p.strip()
        if p and not p.startswith('<'):
            formatted_paragraphs.append(f'<p>{p}</p>')
        else:
            formatted_paragraphs.append(p)
    
    return '\n'.join(formatted_paragraphs)

def generate_blog_html(frontmatter, content_html, slug):
    """Gera HTML completo do artigo no formato do blog"""
    
    title = frontmatter.get('title', 'Sem título')
    description = frontmatter.get('description', '')[:150]
    date = frontmatter.get('date', datetime.now().isoformat())
    category = frontmatter.get('category', 'Tecnologia')
    tags = frontmatter.get('tags', [])[:4]
    keywords = frontmatter.get('keywords', '')
    reading_time = frontmatter.get('reading_time', '3 min')
    emoji = EMOJI_MAP.get(category, EMOJI_MAP['Default'])
    
    # Formatar data
    if isinstance(date, str):
        try:
            date_obj = datetime.fromisoformat(date.replace('Z', '+00:00'))
            date_formatted = date_obj.strftime('%d de %B de %Y')
        except:
            date_formatted = datetime.now().strftime('%d de %B de %Y')
    else:
        date_formatted = date.strftime('%d de %B de %Y')
    
    # Traduzir mês para português
    months_pt = {
        'January': 'Janeiro', 'February': 'Fevereiro', 'March': 'Março',
        'April': 'Abril', 'May': 'Maio', 'June': 'Junho',
        'July': 'Julho', 'August': 'Agosto', 'September': 'Setembro',
        'October': 'Outubro', 'November': 'Novembro', 'December': 'Dezembro'
    }
    for en, pt in months_pt.items():
        date_formatted = date_formatted.replace(en, pt)
    
    # Gerar tags HTML
    tags_html = '\n'.join([
        f'                            <span class="inline-block bg-gradient-to-r from-purple-100 to-pink-100 text-purple-700 px-3 py-1 rounded-full text-sm font-medium">{tag}</span>'
        for tag in tags[:4]
    ])
    
    html_template = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <!-- Meta Tags Essenciais -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Automations Cookbook</title>
    <meta name="description" content="{description}">
    <meta name="keywords" content="{keywords}">
    <meta name="author" content="{frontmatter.get('author', 'AI Trend Hunter Bot')}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://www.automationscookbook.com/blog/{slug}.html">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://www.automationscookbook.com/blog/{slug}.html">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:image" content="https://www.automationscookbook.com/assets/images/og-blog.jpg">
    <meta property="og:locale" content="pt_BR">
    
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:url" content="https://www.automationscookbook.com/blog/{slug}.html">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:image" content="https://www.automationscookbook.com/assets/images/og-blog.jpg">
    
    <!-- Schema.org JSON-LD -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": "{title}",
        "description": "{description}",
        "author": {{
            "@type": "Person",
            "name": "{frontmatter.get('author', 'AI Trend Hunter Bot')}"
        }},
        "datePublished": "{date}",
        "dateModified": "{frontmatter.get('lastmod', date)}",
        "publisher": {{
            "@type": "Organization",
            "name": "Automations Cookbook",
            "logo": {{
                "@type": "ImageObject",
                "url": "https://www.automationscookbook.com/assets/images/logo.png"
            }}
        }},
        "mainEntityOfPage": {{
            "@type": "WebPage",
            "@id": "https://www.automationscookbook.com/blog/{slug}.html"
        }},
        "keywords": "{keywords}"
    }}
    </script>
    
    <!-- Breadcrumb Schema -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {{
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": "https://www.automationscookbook.com/"
            }},
            {{
                "@type": "ListItem",
                "position": 2,
                "name": "Blog",
                "item": "https://www.automationscookbook.com/blog/"
            }},
            {{
                "@type": "ListItem",
                "position": 3,
                "name": "{title}",
                "item": "https://www.automationscookbook.com/blog/{slug}.html"
            }}
        ]
    }}
    </script>
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    
    <!-- Google Analytics 4 -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-CEYC26V1T3"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());
        gtag('config', 'G-CEYC26V1T3');
    </script>
    
    <!-- Google Tag Manager -->
    <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
    new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    }})(window,document,'script','dataLayer','GTM-KVTHGKJR');</script>
    
    <style>
        body {{
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
        }}
        .prose {{
            max-width: 65ch;
        }}
        .prose h2 {{
            margin-top: 2rem;
            margin-bottom: 1rem;
            font-size: 1.875rem;
            font-weight: 700;
            color: #1a202c;
        }}
        .prose h3 {{
            margin-top: 1.5rem;
            margin-bottom: 0.75rem;
            font-size: 1.5rem;
            font-weight: 600;
            color: #2d3748;
        }}
        .prose p {{
            margin-bottom: 1.25rem;
            line-height: 1.75;
            color: #4a5568;
        }}
        .prose ul {{
            margin: 1.25rem 0;
            padding-left: 1.5rem;
        }}
        .prose li {{
            margin-bottom: 0.5rem;
            line-height: 1.75;
            color: #4a5568;
        }}
        .prose code {{
            background: #f7fafc;
            padding: 0.2rem 0.4rem;
            border-radius: 0.25rem;
            font-size: 0.875rem;
            color: #d53f8c;
        }}
        .prose pre {{
            background: #2d3748;
            color: #e2e8f0;
            padding: 1.25rem;
            border-radius: 0.5rem;
            overflow-x: auto;
            margin: 1.5rem 0;
        }}
        .prose strong {{
            color: #2d3748;
            font-weight: 600;
        }}
    </style>
</head>
<body class="bg-gradient-to-br from-gray-50 via-white to-purple-50 min-h-screen">
    <!-- Google Tag Manager (noscript) -->
    <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-KVTHGKJR"
    height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>

    <!-- Header -->
    <header class="bg-white shadow-sm sticky top-0 z-50 border-b border-gray-100">
        <nav class="container mx-auto px-4 py-4">
            <div class="flex items-center justify-between">
                <a href="../index.html" class="text-2xl font-bold bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
                    🤖 Automations Cookbook
                </a>
                <div class="flex items-center space-x-6">
                    <a href="../index.html" class="text-gray-600 hover:text-indigo-600 transition">Home</a>
                    <a href="../integracoes/" class="text-gray-600 hover:text-indigo-600 transition">Integrações</a>
                    <a href="index.html" class="text-indigo-600 font-semibold">Blog</a>
                    <a href="../sobre.html" class="text-gray-600 hover:text-indigo-600 transition">Sobre</a>
                </div>
            </div>
        </nav>
    </header>

    <!-- Breadcrumb -->
    <div class="container mx-auto px-4 py-4">
        <nav class="flex items-center space-x-2 text-sm text-gray-600">
            <a href="../index.html" class="hover:text-indigo-600 transition">Home</a>
            <span>/</span>
            <a href="index.html" class="hover:text-indigo-600 transition">Blog</a>
            <span>/</span>
            <span class="text-gray-900 font-medium">{title[:50]}...</span>
        </nav>
    </div>

    <!-- Main Content -->
    <main class="container mx-auto px-4 py-12 max-w-4xl">
        <!-- Article Header -->
        <article class="bg-white rounded-2xl shadow-xl overflow-hidden">
            <!-- Header colorido com gradiente -->
            <div class="bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-600 p-8 text-white">
                <div class="flex items-center space-x-3 mb-4">
                    <span class="text-5xl">{emoji}</span>
                    <span class="bg-white/20 backdrop-blur-sm px-4 py-1 rounded-full text-sm font-semibold">
                        {category}
                    </span>
                </div>
            </div>

            <!-- Tags e Metadata -->
            <div class="px-8 pt-6 pb-4 border-b border-gray-100">
                <div class="flex flex-wrap gap-2 mb-4">
{tags_html}
                </div>
                
                <h1 class="text-4xl font-bold text-gray-900 mb-4 leading-tight">
                    {title}
                </h1>
                
                <div class="flex items-center space-x-6 text-sm text-gray-600">
                    <div class="flex items-center space-x-2">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                        </svg>
                        <span>{frontmatter.get('author', 'AI Trend Hunter Bot')}</span>
                    </div>
                    <div class="flex items-center space-x-2">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                        </svg>
                        <span>{date_formatted}</span>
                    </div>
                    <div class="flex items-center space-x-2">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                        </svg>
                        <span>{reading_time}</span>
                    </div>
                </div>
            </div>

            <!-- Article Content -->
            <div class="px-8 py-8 prose max-w-none">
                {content_html}
            </div>
        </article>

        <!-- CTA Section -->
        <div class="mt-12 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-600 rounded-2xl shadow-xl p-8 text-white text-center">
            <h2 class="text-3xl font-bold mb-4">
                Pronto para Automatizar com IA?
            </h2>
            <p class="text-lg mb-6 opacity-90">
                Explore mais de 12.700 templates de automação n8n prontos para uso
            </p>
            <a href="../integracoes/" class="inline-block bg-white text-indigo-600 px-8 py-4 rounded-full font-bold text-lg hover:bg-gray-100 transition transform hover:scale-105 shadow-lg">
                Ver Templates →
            </a>
        </div>

        <!-- Author Bio -->
        <div class="mt-12 bg-white rounded-2xl shadow-xl p-8">
            <div class="flex items-start space-x-4">
                <div class="flex-shrink-0">
                    <div class="w-16 h-16 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full flex items-center justify-center text-white text-2xl font-bold">
                        🤖
                    </div>
                </div>
                <div>
                    <h3 class="text-xl font-bold text-gray-900 mb-2">
                        {frontmatter.get('author', 'AI Trend Hunter Bot')}
                    </h3>
                    <p class="text-gray-600 leading-relaxed">
                        Sistema automatizado de análise de tendências em IA, monitorando continuamente o Hugging Face 
                        e gerando insights sobre os modelos mais relevantes do mercado. Atualizado diariamente com dados frescos.
                    </p>
                </div>
            </div>
        </div>
    </main>

    <!-- Footer -->
    <footer class="bg-gray-900 text-white mt-20 py-12">
        <div class="container mx-auto px-4">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
                <div>
                    <h3 class="text-xl font-bold mb-4 bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
                        Automations Cookbook
                    </h3>
                    <p class="text-gray-400 text-sm">
                        Templates e tutoriais de automação para n8n, Make, Zapier e mais.
                    </p>
                </div>
                <div>
                    <h4 class="font-semibold mb-4">Links Rápidos</h4>
                    <ul class="space-y-2 text-sm text-gray-400">
                        <li><a href="../index.html" class="hover:text-white transition">Home</a></li>
                        <li><a href="../integracoes/" class="hover:text-white transition">Integrações</a></li>
                        <li><a href="index.html" class="hover:text-white transition">Blog</a></li>
                        <li><a href="../sobre.html" class="hover:text-white transition">Sobre</a></li>
                    </ul>
                </div>
                <div>
                    <h4 class="font-semibold mb-4">Categorias</h4>
                    <ul class="space-y-2 text-sm text-gray-400">
                        <li><a href="index.html?category=ia" class="hover:text-white transition">Inteligência Artificial</a></li>
                        <li><a href="index.html?category=automacao" class="hover:text-white transition">Automação</a></li>
                        <li><a href="index.html?category=n8n" class="hover:text-white transition">n8n</a></li>
                        <li><a href="index.html?category=tutoriais" class="hover:text-white transition">Tutoriais</a></li>
                    </ul>
                </div>
                <div>
                    <h4 class="font-semibold mb-4">Recursos</h4>
                    <ul class="space-y-2 text-sm text-gray-400">
                        <li><a href="../integracoes/" class="hover:text-white transition">12.700+ Templates</a></li>
                        <li><a href="index.html" class="hover:text-white transition">Artigos Técnicos</a></li>
                        <li><a href="../sitemap-blog.xml" class="hover:text-white transition">Sitemap</a></li>
                    </ul>
                </div>
            </div>
            <div class="border-t border-gray-800 mt-8 pt-8 text-center text-sm text-gray-400">
                <p>&copy; 2025 Automations Cookbook. Todos os direitos reservados.</p>
            </div>
        </div>
    </footer>
</body>
</html>'''
    
    return html_template

def publish_post(md_file):
    """Publica um post markdown no blog"""
    
    # Parse markdown
    frontmatter, markdown_content = parse_markdown_post(md_file)
    
    # Gerar slug do filename ou do frontmatter
    slug = frontmatter.get('slug')
    if not slug:
        slug = md_file.stem
    
    # Converter markdown para HTML
    content_html = markdown_to_html(markdown_content)
    
    # Gerar HTML completo
    html_content = generate_blog_html(frontmatter, content_html, slug)
    
    # Salvar arquivo HTML
    html_filename = f"{slug}.html"
    html_path = BLOG_DIR / html_filename
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Post publicado: {html_path}")
    
    return {
        'slug': slug,
        'title': frontmatter.get('title', 'Sem título'),
        'url': f"/blog/{html_filename}",
        'date': frontmatter.get('date', datetime.now().isoformat()),
        'category': frontmatter.get('category', 'Tecnologia'),
        'tags': frontmatter.get('tags', [])[:4]
    }

def update_sitemap(posts_info):
    """Atualiza sitemap-blog.xml com novos posts"""
    
    import xml.etree.ElementTree as ET
    
    # Parse sitemap existente
    tree = ET.parse(SITEMAP_PATH)
    root = tree.getroot()
    
    # Namespace
    ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    
    # URLs já existentes
    existing_urls = {url.find('ns:loc', ns).text for url in root.findall('ns:url', ns)}
    
    # Adicionar novos posts
    added_count = 0
    for post in posts_info:
        url = f"https://www.automationscookbook.com{post['url']}"
        
        if url not in existing_urls:
            url_elem = ET.SubElement(root, 'url')
            
            loc = ET.SubElement(url_elem, 'loc')
            loc.text = url
            
            lastmod = ET.SubElement(url_elem, 'lastmod')
            try:
                date_obj = datetime.fromisoformat(post['date'].replace('Z', '+00:00'))
                lastmod.text = date_obj.strftime('%Y-%m-%d')
            except:
                lastmod.text = datetime.now().strftime('%Y-%m-%d')
            
            changefreq = ET.SubElement(url_elem, 'changefreq')
            changefreq.text = 'weekly'
            
            priority = ET.SubElement(url_elem, 'priority')
            priority.text = '0.8'
            
            added_count += 1
    
    # Salvar sitemap atualizado
    tree.write(SITEMAP_PATH, encoding='utf-8', xml_declaration=True)
    
    print(f"✅ Sitemap atualizado: {added_count} novos URLs")

def update_blog_index(posts_info):
    """Atualiza blog/index.html com cards dos novos posts"""
    
    with open(BLOG_INDEX_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Gerar cards HTML
    cards_html = []
    for post in posts_info:
        emoji = EMOJI_MAP.get(post['category'], EMOJI_MAP['Default'])
        
        # Formatar tags
        tags_html = ' '.join([
            f'<span class="text-xs bg-purple-100 text-purple-700 px-2 py-1 rounded">{tag}</span>'
            for tag in post['tags'][:3]
        ])
        
        card = f'''
                    <!-- Card: {post['title'][:50]} -->
                    <div class="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2">
                        <div class="bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-600 p-6 text-white">
                            <div class="flex items-center space-x-3 mb-3">
                                <span class="text-4xl">{emoji}</span>
                                <span class="bg-white/20 backdrop-blur-sm px-3 py-1 rounded-full text-xs font-semibold">
                                    {post['category']}
                                </span>
                            </div>
                        </div>
                        <div class="p-6">
                            <div class="flex flex-wrap gap-2 mb-3">
                                {tags_html}
                            </div>
                            <h3 class="text-xl font-bold text-gray-900 mb-3 line-clamp-2 hover:text-indigo-600 transition">
                                <a href="{post['slug']}.html">{post['title']}</a>
                            </h3>
                            <p class="text-gray-600 mb-4 line-clamp-3">
                                Análise automática de tendências em IA, com dados atualizados do Hugging Face.
                            </p>
                            <a href="{post['slug']}.html" class="inline-flex items-center space-x-2 text-indigo-600 font-semibold hover:text-indigo-700 transition group">
                                <span>Ler artigo</span>
                                <svg class="w-5 h-5 transform group-hover:translate-x-1 transition" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
                                </svg>
                            </a>
                        </div>
                    </div>'''
        
        cards_html.append(card)
    
    # Encontrar ponto de inserção
    marker = '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8" id="articles-grid">'
    
    if marker in content:
        new_cards = '\n'.join(cards_html)
        new_content = content.replace(marker, f'{marker}\n{new_cards}\n')
        
        with open(BLOG_INDEX_PATH, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ Blog index atualizado: {len(posts_info)} novos cards")
    else:
        print("⚠️ Marcador não encontrado em blog/index.html")

def main():
    """Função principal - publica todos os posts novos do AI Trend Hunter"""
    
    print("🚀 Iniciando publicação automática do AI Trend Hunter...\n")
    
    # Encontrar posts markdown do dia
    today = datetime.now().strftime('%Y-%m-%d')
    md_files = list(POSTS_DIR.glob(f'{today}_*.md'))
    
    if not md_files:
        print(f"⚠️ Nenhum post encontrado para hoje ({today})")
        print(f"   Buscando em: {POSTS_DIR}")
        # Buscar qualquer arquivo .md disponível
        md_files = [f for f in POSTS_DIR.glob('*.md') if f.name != 'index.md']
        if md_files:
            print(f"📝 Encontrados {len(md_files)} posts disponíveis")
        else:
            print("❌ Nenhum post markdown encontrado")
            return
    
    # Publicar cada post
    posts_info = []
    for md_file in md_files:
        print(f"\n📝 Processando: {md_file.name}")
        try:
            post_info = publish_post(md_file)
            posts_info.append(post_info)
        except Exception as e:
            print(f"❌ Erro ao publicar {md_file.name}: {e}")
            import traceback
            traceback.print_exc()
    
    if not posts_info:
        print("\n❌ Nenhum post foi publicado com sucesso")
        return
    
    # Atualizar sitemap
    print(f"\n📊 Atualizando sitemap...")
    try:
        update_sitemap(posts_info)
    except Exception as e:
        print(f"❌ Erro ao atualizar sitemap: {e}")
    
    # Atualizar blog index
    print(f"\n🏠 Atualizando blog/index.html...")
    try:
        update_blog_index(posts_info)
    except Exception as e:
        print(f"❌ Erro ao atualizar blog index: {e}")
    
    print(f"\n✅ Publicação concluída!")
    print(f"📊 Total de posts publicados: {len(posts_info)}")
    print(f"\nURLs geradas:")
    for post in posts_info:
        print(f"  - https://www.automationscookbook.com{post['url']}")

if __name__ == '__main__':
    main()
