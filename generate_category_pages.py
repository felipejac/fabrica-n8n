#!/usr/bin/env python3
"""
Gerador de páginas de índice por categoria
Cria /integracoes/crm/, /integracoes/whatsapp/, etc.
"""

import csv
import os
from collections import defaultdict

CATEGORIES = {
    'crm': {
        'name': 'CRM & Vendas',
        'icon': '📊',
        'description': 'Templates de automação para integrar sistemas de CRM e otimizar processos de vendas.',
        'keywords': ['Pipedrive', 'HubSpot', 'RD Station', 'Salesforce', 'Kommo', 'Zoho CRM', 'Agile CRM'],
        'color': 'indigo'
    },
    'whatsapp': {
        'name': 'WhatsApp & Messaging',
        'icon': '💬',
        'description': 'Automatize conversas e notificações pelo WhatsApp Business e ferramentas de messaging.',
        'keywords': ['WhatsApp', 'Chatwoot', 'Kommo', 'Twilio WhatsApp', 'WhatsApp Business'],
        'color': 'green'
    },
    'ecommerce': {
        'name': 'E-commerce & Varejo',
        'icon': '🛒',
        'description': 'Automatize pedidos, estoque, notas fiscais e toda a operação do seu e-commerce.',
        'keywords': ['Shopify', 'WooCommerce', 'Mercado Livre', 'Bling', 'VTEX', 'Magento'],
        'color': 'purple'
    },
    'marketing': {
        'name': 'Marketing & Ads',
        'icon': '📈',
        'description': 'Templates para campanhas de marketing digital, captura de leads e gestão de anúncios.',
        'keywords': ['Facebook', 'Google Ads', 'Instagram', 'LinkedIn', 'Meta Ads', 'TikTok', 'Twitter'],
        'color': 'pink'
    },
    'suporte': {
        'name': 'Suporte & Customer Success',
        'icon': '🎧',
        'description': 'Automatize atendimento ao cliente, tickets e processos de CS.',
        'keywords': ['Zendesk', 'Freshdesk', 'Help Scout', 'Intercom', 'Jira Service'],
        'color': 'blue'
    }
}

def template_matches_category(software_a, software_b, tags, category_keywords):
    """Verifica se template pertence à categoria"""
    combined = f"{software_a} {software_b} {tags}".lower()
    return any(keyword.lower() in combined for keyword in category_keywords)

def generate_category_page(category_key, category_info, templates):
    """Gera HTML de página de categoria"""
    
    name = category_info['name']
    icon = category_info['icon']
    description = category_info['description']
    color = category_info['color']
    
    html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} - Templates de Automação N8N | Automations Cookbook</title>
    <meta name="description" content="{description} {len(templates)} templates prontos para usar.">
    <meta name="keywords" content="n8n templates, {category_key}, automação, workflow, {', '.join(category_info['keywords'][:5])}">
    
    <!-- Open Graph -->
    <meta property="og:title" content="{name} - Templates de Automação">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://www.automationscookbook.com/integracoes/{category_key}/">
    
    <!-- Schema.org -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "CollectionPage",
      "name": "{name} - Templates de Automação",
      "description": "{description}",
      "url": "https://www.automationscookbook.com/integracoes/{category_key}/",
      "numberOfItems": {len(templates)},
      "about": {{
        "@type": "Thing",
        "name": "{name}"
      }}
    }}
    </script>
    
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-50">

    <!-- Header -->
    <header class="bg-white border-b border-slate-200 sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center py-4">
                <div class="flex items-center gap-2">
                    <span class="text-2xl">🍳</span>
                    <a href="/" class="text-xl font-bold text-slate-900">Automations Cookbook</a>
                </div>
                <nav class="flex gap-6">
                    <a href="/" class="text-slate-600 hover:text-{color}-600">Home</a>
                    <a href="/integracoes/" class="text-{color}-600 font-semibold">Templates</a>
                    <a href="/sobre" class="text-slate-600 hover:text-{color}-600">Sobre</a>
                    <a href="/llm" class="text-slate-600 hover:text-{color}-600">API</a>
                </nav>
            </div>
        </div>
    </header>

    <!-- Hero -->
    <section class="bg-gradient-to-r from-{color}-900 to-{color}-700 text-white py-16">
        <div class="max-w-7xl mx-auto px-4">
            <div class="flex items-center gap-4 mb-4">
                <span class="text-5xl">{icon}</span>
                <div>
                    <h1 class="text-4xl font-extrabold">{name}</h1>
                    <p class="text-{color}-100 mt-2">{len(templates)} templates prontos para usar</p>
                </div>
            </div>
            <p class="text-lg text-{color}-50 max-w-3xl">{description}</p>
        </div>
    </section>

    <!-- Breadcrumb -->
    <div class="max-w-7xl mx-auto px-4 py-4">
        <nav class="flex text-sm text-slate-600">
            <a href="/" class="hover:text-{color}-600">Home</a>
            <span class="mx-2">/</span>
            <a href="/integracoes/" class="hover:text-{color}-600">Templates</a>
            <span class="mx-2">/</span>
            <span class="text-slate-900 font-semibold">{name}</span>
        </nav>
    </div>

    <!-- Templates Grid -->
    <main class="max-w-7xl mx-auto px-4 py-8">
        
        <!-- Filtros rápidos -->
        <div class="mb-8 bg-white rounded-lg p-6 border border-slate-200">
            <h2 class="text-lg font-bold text-slate-900 mb-4">🔍 Softwares mais populares nesta categoria:</h2>
            <div class="flex flex-wrap gap-2">
'''
    
    # Adicionar tags de software
    for keyword in category_info['keywords'][:8]:
        html += f'                <span class="px-4 py-2 bg-{color}-50 text-{color}-700 rounded-full text-sm font-medium border border-{color}-200">{keyword}</span>\n'
    
    html += f'''            </div>
        </div>

        <!-- Lista de Templates -->
        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
'''
    
    # Adicionar cada template
    for template in templates[:100]:  # Limitar a 100 por página
        slug = template['slug']
        software_a = template['software_a']
        software_b = template['software_b']
        titulo = template['titulo']
        descricao = template['descricao'][:120] + '...' if len(template['descricao']) > 120 else template['descricao']
        tipo_evento = template['tipo_evento']
        
        html += f'''            <a href="/integracoes/{slug}.html" class="block bg-white rounded-lg p-6 border-2 border-slate-200 hover:border-{color}-500 hover:shadow-lg transition group">
                <div class="flex items-start justify-between mb-3">
                    <span class="px-3 py-1 bg-{color}-100 text-{color}-700 rounded-full text-xs font-semibold">{tipo_evento}</span>
                    <span class="text-2xl">{icon}</span>
                </div>
                <h3 class="text-lg font-bold text-slate-900 group-hover:text-{color}-600 mb-2 line-clamp-2">{software_a} → {software_b}</h3>
                <p class="text-sm text-slate-600 mb-4 line-clamp-2">{descricao}</p>
                <span class="text-{color}-600 text-sm font-semibold">Ver template →</span>
            </a>
'''
    
    html += f'''        </div>

        <!-- Mostrar mais -->
        {f'<div class="mt-12 text-center text-slate-600"><p>Mostrando 100 de {len(templates)} templates. <a href="/integracoes/" class="text-{color}-600 font-semibold hover:underline">Ver todos os templates →</a></p></div>' if len(templates) > 100 else ''}

        <!-- CTA -->
        <div class="mt-16 bg-gradient-to-r from-{color}-600 to-{color}-500 rounded-2xl p-10 text-center text-white">
            <h2 class="text-3xl font-bold mb-4">Não encontrou o que procurava?</h2>
            <p class="text-xl mb-6 text-{color}-50">Explore todos os 13.269 templates ou confira outras categorias</p>
            <div class="flex gap-4 justify-center">
                <a href="/integracoes/" class="inline-block px-8 py-4 bg-white text-{color}-600 font-bold rounded-lg hover:bg-{color}-50 transition">
                    Ver Todos os Templates
                </a>
                <a href="/sobre" class="inline-block px-8 py-4 bg-{color}-700 text-white font-bold rounded-lg hover:bg-{color}-800 transition border-2 border-white/20">
                    Explorar Categorias
                </a>
            </div>
        </div>

    </main>

    <!-- Footer -->
    <footer class="bg-slate-900 text-slate-400 py-12 mt-20">
        <div class="max-w-7xl mx-auto px-4 text-center">
            <p class="mb-2">🍳 Automations Cookbook</p>
            <p class="text-sm">Open-source library with 13,269+ automation templates</p>
            <p class="text-sm mt-4">
                <a href="https://github.com/felipejac/fabrica-n8n" class="hover:text-white transition">GitHub</a> • 
                <a href="/integracoes/" class="hover:text-white transition">Templates</a> • 
                <a href="/llm" class="hover:text-white transition">API</a>
            </p>
        </div>
    </footer>

</body>
</html>
'''
    
    return html

def main():
    print("=" * 80)
    print("🗂 Gerando Páginas de Índice por Categoria")
    print("=" * 80)
    print()
    
    # Ler todos os templates
    all_templates = []
    with open('automacoes_db.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            all_templates.append({
                'slug': row['slug_url'],
                'software_a': row['software_a'],
                'software_b': row['software_b'],
                'tipo_evento': row['tipo_evento'],
                'titulo': row['titulo_pagina'],
                'descricao': row['descricao_curta'],
                'tags': row.get('tags', '')
            })
    
    print(f"📊 Total de templates carregados: {len(all_templates)}\n")
    
    # Criar diretório se não existir
    os.makedirs('integracoes', exist_ok=True)
    
    # Gerar página para cada categoria
    for category_key, category_info in CATEGORIES.items():
        # Filtrar templates da categoria
        category_templates = [
            t for t in all_templates
            if template_matches_category(t['software_a'], t['software_b'], t['tags'], category_info['keywords'])
        ]
        
        print(f"{category_info['icon']} {category_info['name']}: {len(category_templates)} templates")
        
        # Criar diretório da categoria
        category_dir = f"integracoes/{category_key}"
        os.makedirs(category_dir, exist_ok=True)
        
        # Gerar HTML
        html = generate_category_page(category_key, category_info, category_templates)
        
        # Salvar arquivo
        output_file = f"{category_dir}/index.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"   ✅ Salvo em: {output_file}")
    
    print("\n" + "=" * 80)
    print("✅ Páginas de categoria criadas com sucesso!")
    print("=" * 80)
    print("\nPróximos passos:")
    print("1. Revisar as páginas geradas")
    print("2. Commit e deploy")
    print("3. Atualizar sitemap com as novas URLs")

if __name__ == '__main__':
    main()
