import csv
import os
import json
from datetime import datetime
import hashlib

# ==================== CONFIGURAÇÕES ====================
CSV_FILE = 'automacoes_zapier_db.csv'
TEMPLATE_FILE = 'template_page_zapier.html'
OUTPUT_DIR = 'integracoes-zapier'
MAIN_INDEX = 'index.html'

# Emoji map para categorias
EMOJI_MAP = {
    'marketing': '📢',
    'vendas': '💼',
    'dados': '📊',
    'crm': '🎯',
    'automação': '⚙️',
    'chat': '💬',
    'email': '📧',
    'notificação': '🔔',
    'ia': '🤖',
    'financeiro': '💰',
    'ecommerce': '🛒',
    'e-commerce': '🛒',
    'blog': '📝',
    'social-media': '📱',
    'redes sociais': '📱',
    'backup': '💾',
    'api': '🔌',
    'zapier': '⚡',
    'agendamento': '📅',
    'comunicacao': '💬',
    'whatsapp': '💚',
    'formularios': '📝',
    'pagamentos': '💳',
    'gestao': '📋',
    'suporte': '🎧',
    'arquivos': '📁',
    'desenvolvimento': '💻',
}

# Garante que a pasta de saída existe
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# ==================== FUNÇÕES UTILITÁRIAS ====================

def get_emoji(tags_str):
    """Retorna emoji baseado nas tags"""
    if not tags_str:
        return '⚡'
    for tag in tags_str.split(','):
        tag = tag.strip().lower()
        if tag in EMOJI_MAP:
            return EMOJI_MAP[tag]
    return '⚡'

def create_tags_html(tags_str):
    """Cria HTML de tags com badge"""
    if not tags_str:
        return ""
    tags = tags_str.split(',')
    html = ""
    for tag in tags:
        tag = tag.strip()
        if tag and tag.lower() != 'zapier':  # Não exibir tag "zapier" redundante
            html += f'<span class="px-2 py-1 bg-orange-50 text-orange-700 text-xs rounded-full font-medium hover:bg-orange-100 transition-colors">{tag}</span>'
    return html

def create_steps_html(steps_str):
    """Cria lista de passos em HTML"""
    if not steps_str:
        return "<li>Conecte as contas no Zapier e configure o Zap.</li>"
    steps = steps_str.split('|')
    html = ""
    for i, step in enumerate(steps, 1):
        step = step.strip()
        if step:
            html += f'<li class="mb-3 flex gap-3"><span class="flex-shrink-0 flex items-center justify-center h-6 w-6 rounded-full bg-orange-100 text-orange-700 text-sm font-bold">{i}</span><span>{step}</span></li>'
    return html

def create_json_steps(steps_str):
    """Gera steps para Schema.org JSON-LD"""
    if not steps_str:
        return ""
    steps = steps_str.split('|')
    json_steps = []
    for step in steps:
        step = step.strip()
        if step:
            # Escapar aspas para JSON
            step_escaped = step.replace('"', '\\"')
            json_steps.append(f'{{"@type": "HowToStep", "text": "{step_escaped}"}}')
    return ",\n".join(json_steps)

def slugify(text):
    """Cria slug a partir de texto"""
    return text.lower().replace(' ', '-').replace('_', '-')

def sanitize_html(text):
    """Remove caracteres perigosos"""
    return text.replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

# ==================== GERAÇÃO DE ÍNDICE ====================

def generate_index_page(templates):
    """Gera index.html otimizado com busca e filtros"""
    
    # Criar dados para filtro JavaScript
    templates_json = json.dumps(templates)
    
    index_content = f'''<!DOCTYPE html>
<html lang="pt-BR" itemscope itemtype="http://schema.org/CollectionPage">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- SEO -->
    <title>Templates de Automação Zapier | {len(templates)}+ Zaps Prontos | Automations Cookbook</title>
    <meta name="description" content="{len(templates)}+ templates prontos de automação Zapier. Conecte suas ferramentas favoritas em minutos com Zaps pré-configurados. Guias passo a passo gratuitos.">
    <meta name="keywords" content="zapier, automação, zaps, templates, integração, workflow, tutorial">
    <meta name="author" content="Automations Cookbook">
    <link rel="canonical" href="https://www.automationscookbook.com/integracoes-zapier/">
    
    <!-- Open Graph -->
    <meta property="og:title" content="Templates de Automação Zapier | {len(templates)}+ Zaps Prontos">
    <meta property="og:description" content="{len(templates)}+ templates prontos de automação Zapier. Conecte suas ferramentas favoritas em minutos.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://www.automationscookbook.com/integracoes-zapier/">
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    
    <style>
        body {{ font-family: 'Inter', sans-serif; }}
        .integration-card {{ transition: all 0.3s ease; }}
        .integration-card:hover {{ transform: translateY(-4px); }}
    </style>

    <!-- Schema.org CollectionPage -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Templates de Automação Zapier",
        "description": "{len(templates)}+ templates prontos de automação Zapier com guias passo a passo",
        "url": "https://www.automationscookbook.com/integracoes-zapier/",
        "numberOfItems": {len(templates)},
        "about": {{
            "@type": "SoftwareApplication",
            "name": "Zapier",
            "applicationCategory": "BusinessApplication",
            "operatingSystem": "Web"
        }}
    }}
    </script>
</head>
<body class="bg-slate-50 text-slate-800">
    <!-- Header / Navegação -->
    <header class="bg-white border-b border-slate-200 sticky top-0 z-50 shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-16">
                <a href="../index.html" class="font-bold text-xl text-orange-600 flex items-center gap-2 hover:opacity-80 transition-opacity">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                    Automations Cookbook
                </a>
                <nav class="flex items-center gap-4">
                    <a href="../integracoes/" class="text-sm text-slate-600 hover:text-indigo-600 transition-colors">N8N Templates</a>
                    <span class="text-slate-300">|</span>
                    <a href="../index.html" class="text-sm text-slate-600 hover:text-orange-600 transition-colors">← Início</a>
                    <span class="text-slate-300">|</span>
                    <span class="text-sm font-medium text-orange-600">Zapier ({len(templates)})</span>
                </nav>
            </div>
        </div>
    </header>

    <!-- Hero Section -->
    <div class="bg-gradient-to-r from-orange-600 to-orange-500 text-white py-12">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h1 class="text-4xl font-bold mb-4">⚡ Templates de Automação Zapier</h1>
            <p class="text-lg text-orange-100 max-w-2xl mx-auto mb-6">
                {len(templates)}+ Zaps prontos para conectar suas ferramentas favoritas em minutos. Sem código, 100% visual.
            </p>
            <div class="flex items-center justify-center gap-4 text-sm flex-wrap">
                <span class="bg-white/20 text-white px-3 py-1 rounded-full">⚡ {len(templates)}+ Zaps</span>
                <span class="bg-white/20 text-white px-3 py-1 rounded-full">✅ Sem Código</span>
                <span class="bg-white/20 text-white px-3 py-1 rounded-full">🎯 Prontos para Usar</span>
                <span class="bg-white/20 text-white px-3 py-1 rounded-full">📚 Guias Detalhados</span>
            </div>
        </div>
    </div>

    <!-- Buscador -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="max-w-md mx-auto">
            <input 
                type="text" 
                id="searchInput" 
                onkeyup="filterCards()" 
                placeholder="Buscar Zap (ex: Shopify, Gmail, Slack)..." 
                class="w-full px-4 py-3 rounded-lg border border-slate-300 focus:ring-2 focus:ring-orange-500 focus:outline-none shadow-sm"
            >
        </div>
    </div>

    <!-- Grid de Integrações -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-12">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6" id="integrationsGrid">
'''
    
    # Adicionar cards
    for t in templates:
        emoji = get_emoji(t['tags'])
        index_content += f'''            <a href="{t['slug']}" class="integration-card block bg-white p-6 rounded-xl shadow-sm border border-slate-200 hover:shadow-lg hover:border-orange-300 transition-all group">
                <div class="text-xs uppercase font-bold text-orange-600 mb-2">{emoji} {t['software_a']} → {t['software_b']}</div>
                <h2 class="font-bold text-slate-900 mb-2 group-hover:text-orange-600 transition-colors line-clamp-2">{sanitize_html(t['titulo'])}</h2>
                <p class="text-sm text-slate-600 line-clamp-2">{sanitize_html(t['desc'])}</p>
                <div class="mt-3 flex items-center gap-2">
                    <span class="text-xs text-orange-600 font-medium">⚡ Zapier</span>
                </div>
            </a>
'''
    
    index_content += '''        </div>

        <div id="noResults" class="hidden text-center py-12">
            <p class="text-slate-500 text-lg">Nenhum Zap encontrado para sua busca.</p>
            <p class="text-slate-400 text-sm mt-2">Tente outros termos ou <a href="../integracoes/" class="text-indigo-600 hover:underline">veja os templates N8N</a>.</p>
        </div>
    </main>

    <!-- CTA Section -->
    <section class="bg-gradient-to-r from-orange-50 to-orange-100 py-12 mt-12">
        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 class="text-2xl font-bold text-slate-900 mb-4">Prefere automação open-source?</h2>
            <p class="text-slate-600 mb-6">Explore nossos <strong>{len(templates)}+ templates N8N</strong> gratuitos com controle total e sem limites.</p>
            <a href="../integracoes/" class="inline-block bg-indigo-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-indigo-700 transition-colors shadow-md">
                Ver Templates N8N →
            </a>
        </div>
    </section>

    <!-- Footer -->
    <footer class="bg-white border-t border-slate-200 mt-12 py-8">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-sm text-slate-600">
            <p class="mb-2">© 2024 <strong>Automations Cookbook</strong></p>
            <p class="space-x-4">
                <a href="../index.html" class="text-orange-600 hover:text-orange-700 font-medium">← Início</a>
                <span class="text-slate-300">|</span>
                <a href="../integracoes/" class="text-indigo-600 hover:text-indigo-700 font-medium">Templates N8N</a>
                <span class="text-slate-300">|</span>
                <a href="../llm.html" class="text-slate-600 hover:text-slate-900">API para LLMs</a>
            </p>
        </div>
    </footer>

    <script>
        // Dados das integrações para filtro
        const integrations = [
'''
    
    # Adicionar dados para busca
    for t in templates:
        keywords = ','.join([tag.strip() for tag in t['tags'].split(',')] + [t['software_a'].lower(), t['software_b'].lower()])
        index_content += f'''            {{
                name: '{sanitize_html(t["titulo"])}',
                file: '{t["slug"]}',
                keywords: ['{keywords.replace(",", "','")}']
            }},
'''
    
    index_content += '''        ];

        // Função de filtro
        function filterCards() {
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            const cards = document.querySelectorAll('.integration-card');
            let visibleCount = 0;

            cards.forEach((card, index) => {
                const integration = integrations[index];
                const matchesSearch = integration.name.toLowerCase().includes(searchTerm) ||
                    integration.keywords.some(kw => kw.includes(searchTerm));

                if (matchesSearch || searchTerm === '') {
                    card.style.display = 'block';
                    visibleCount++;
                } else {
                    card.style.display = 'none';
                }
            });

            document.getElementById('noResults').classList.toggle('hidden', visibleCount > 0);
        }

        window.filterCards = filterCards;
    </script>
</body>
</html>
'''
    
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_content)
    print(f"✅ Índice Zapier gerado: {len(templates)} templates indexados")


def generate():
    """Função principal de geração"""
    print(f"⚡ Iniciando geração de templates Zapier...")
    print(f"📂 Pasta de saída: {OUTPUT_DIR}/")
    
    # 1. Verificar se template existe, senão usar template inline
    template_content = get_zapier_template()

    # 2. Ler CSV e Gerar Páginas
    generated_templates = []
    count = 0
    start_time = datetime.now()
    
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                # Dados básicos
                page = template_content
                slug = row.get('slug_url', '').strip()
                
                if not slug:
                    continue

                # ===== SUBSTITUIÇÕES SIMPLES =====
                for key, value in row.items():
                    placeholder = f"{{{{ {key} }}}}"
                    page = page.replace(placeholder, value)

                # ===== SUBSTITUIÇÕES COMPLEXAS =====
                tags_html = create_tags_html(row.get('tags', ''))
                page = page.replace('{{ tags_html }}', tags_html)

                steps_html = create_steps_html(row.get('passos_resumo', ''))
                page = page.replace('{{ lista_passos }}', steps_html)
                
                json_steps = create_json_steps(row.get('passos_resumo', ''))
                page = page.replace('{{ json_steps }}', json_steps)

                # Ajustar vocabulário para Zapier
                page = page.replace('workflow n8n', 'Zap')
                page = page.replace('Workflow n8n', 'Zap')
                page = page.replace('N8N', 'Zapier')
                page = page.replace('n8n', 'Zapier')

                # ===== SALVAR ARQUIVO =====
                filename = f"{slug}.html"
                filepath = os.path.join(OUTPUT_DIR, filename)
                
                with open(filepath, 'w', encoding='utf-8') as out:
                    out.write(page)
                
                # Guardar info para o índice
                generated_templates.append({
                    'slug': filename,
                    'titulo': row.get('titulo_pagina', 'Sem Título'),
                    'desc': row.get('descricao_curta', ''),
                    'software_a': row.get('software_a', ''),
                    'software_b': row.get('software_b', ''),
                    'tags': row.get('tags', ''),
                })
                
                print(f"⚡ Gerado: {filename}")
                count += 1

    except FileNotFoundError:
        print(f"❌ Erro: '{CSV_FILE}' não encontrado.")
        return

    # 3. Gerar Índice do diretório
    generate_index_page(generated_templates)

    # ===== ESTATÍSTICAS =====
    elapsed_time = (datetime.now() - start_time).total_seconds()
    avg_time = (elapsed_time / count * 1000) if count > 0 else 0
    
    print(f"\n{'='*60}")
    print(f"✅ GERAÇÃO ZAPIER CONCLUÍDA COM SUCESSO!")
    print(f"{'='*60}")
    print(f"📊 Estatísticas:")
    print(f"   • Zaps gerados: {count}")
    print(f"   • Tempo total: {elapsed_time:.2f}s")
    print(f"   • Tempo por Zap: {avg_time:.2f}ms")
    print(f"   • Taxa: {count/elapsed_time:.0f} páginas/segundo")
    print(f"   • Pasta: {OUTPUT_DIR}/")
    print(f"{'='*60}\n")


def get_zapier_template():
    """Retorna template para páginas Zapier"""
    
    # Tentar ler template customizado
    if os.path.exists(TEMPLATE_FILE):
        with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
            return f.read()
    
    # Template inline otimizado para Zapier
    return '''<!DOCTYPE html>
<html lang="pt-BR" itemscope itemtype="http://schema.org/HowTo">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- SEO -->
    <title>{{ titulo_pagina }} | Automations Cookbook</title>
    <meta name="description" content="{{ descricao_curta }}">
    <meta name="keywords" content="zapier,automação,{{ software_a }},{{ software_b }},{{ tags }}">
    <link rel="canonical" href="https://www.automationscookbook.com/integracoes-zapier/{{ slug_url }}.html">
    
    <!-- Open Graph -->
    <meta property="og:title" content="{{ titulo_pagina }}">
    <meta property="og:description" content="{{ descricao_curta }}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://www.automationscookbook.com/integracoes-zapier/{{ slug_url }}.html">
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    
    <style>
        body { font-family: 'Inter', sans-serif; }
    </style>

    <!-- Schema.org HowTo -->
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": "{{ titulo_pagina }}",
        "description": "{{ descricao_curta }}",
        "tool": ["Zapier", "{{ software_a }}", "{{ software_b }}"],
        "step": [
            {{ json_steps }}
        ]
    }
    </script>
</head>
<body class="bg-slate-50 text-slate-800">
    <!-- Header -->
    <header class="bg-white border-b border-slate-200 sticky top-0 z-50 shadow-sm">
        <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-16">
                <a href="../index.html" class="font-bold text-xl text-orange-600 flex items-center gap-2 hover:opacity-80 transition-opacity">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                    Automations Cookbook
                </a>
                <nav class="flex items-center gap-3 text-sm">
                    <a href="index.html" class="text-slate-600 hover:text-orange-600 transition-colors">← Todos os Zaps</a>
                </nav>
            </div>
        </div>
    </header>

    <!-- Conteúdo Principal -->
    <main class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <!-- Breadcrumb -->
        <nav class="text-sm text-slate-500 mb-6">
            <a href="../index.html" class="hover:text-orange-600">Início</a> / 
            <a href="index.html" class="hover:text-orange-600">Zapier</a> / 
            <span class="text-slate-700">{{ software_a }} para {{ software_b }}</span>
        </nav>

        <!-- Hero -->
        <div class="bg-gradient-to-r from-orange-500 to-orange-600 text-white rounded-2xl p-8 mb-8">
            <div class="flex items-center gap-2 mb-3">
                <span class="bg-white/20 px-3 py-1 rounded-full text-sm font-medium">⚡ Zapier</span>
                <span class="bg-white/20 px-3 py-1 rounded-full text-sm font-medium">{{ tipo_evento }}</span>
            </div>
            <h1 class="text-3xl md:text-4xl font-bold mb-4">{{ titulo_pagina }}</h1>
            <p class="text-lg text-orange-100">{{ descricao_curta }}</p>
        </div>

        <!-- Info Box -->
        <div class="bg-white rounded-xl border border-slate-200 p-6 mb-8">
            <div class="grid md:grid-cols-3 gap-6">
                <div>
                    <div class="text-xs uppercase text-slate-500 font-semibold mb-1">Trigger</div>
                    <div class="font-bold text-slate-900">{{ software_a }}</div>
                </div>
                <div>
                    <div class="text-xs uppercase text-slate-500 font-semibold mb-1">Action</div>
                    <div class="font-bold text-slate-900">{{ software_b }}</div>
                </div>
                <div>
                    <div class="text-xs uppercase text-slate-500 font-semibold mb-1">Caso de Uso</div>
                    <div class="font-bold text-slate-900">{{ caso_uso_resumido }}</div>
                </div>
            </div>
        </div>

        <!-- Passos -->
        <section class="bg-white rounded-xl border border-slate-200 p-8 mb-8">
            <h2 class="text-2xl font-bold text-slate-900 mb-6">📋 Passo a Passo</h2>
            <ol class="space-y-3 list-none">
                {{ lista_passos }}
            </ol>
        </section>

        <!-- Tags -->
        <div class="flex flex-wrap gap-2 mb-8">
            {{ tags_html }}
        </div>

        <!-- CTA -->
        <div class="bg-orange-50 border border-orange-200 rounded-xl p-6 text-center">
            <h3 class="font-bold text-xl text-slate-900 mb-2">Pronto para Automatizar?</h3>
            <p class="text-slate-600 mb-4">Use este template no Zapier ou adapte para N8N (open-source).</p>
            <div class="flex gap-3 justify-center flex-wrap">
                <a href="{{ zap_template_url }}" target="_blank" rel="noopener" class="inline-block bg-orange-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-orange-700 transition-colors shadow-md">
                    ⚡ Abrir no Zapier
                </a>
                <a href="../integracoes/" class="inline-block bg-indigo-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-indigo-700 transition-colors shadow-md">
                    Ver versão N8N
                </a>
            </div>
        </div>
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-slate-200 mt-12 py-8">
        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-sm text-slate-600">
            <p class="mb-2">© 2024 <strong>Automations Cookbook</strong></p>
            <p class="space-x-4">
                <a href="../index.html" class="text-orange-600 hover:text-orange-700 font-medium">Início</a>
                <span class="text-slate-300">|</span>
                <a href="index.html" class="text-orange-600 hover:text-orange-700 font-medium">Todos os Zaps</a>
                <span class="text-slate-300">|</span>
                <a href="../integracoes/" class="text-indigo-600 hover:text-indigo-700 font-medium">Templates N8N</a>
            </p>
        </div>
    </footer>
</body>
</html>'''


if __name__ == "__main__":
    generate()
