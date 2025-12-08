import csv
import os
import json
from datetime import datetime
import hashlib

# ==================== CONFIGURAÇÕES ====================
CSV_FILE = 'automacoes_db.csv'
TEMPLATE_FILE = 'template_page.html'
OUTPUT_DIR = 'integracoes'
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
    'e-commerce': '🛒',
    'blog': '📝',
    'redes sociais': '📱',
    'backup': '💾',
    'api': '🔌',
}

# Garante que a pasta de saída existe
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# ==================== FUNÇÕES UTILITÁRIAS ====================

def get_emoji(tags_str):
    """Retorna emoji baseado nas tags"""
    if not tags_str:
        return '🔗'
    for tag in tags_str.split(','):
        tag = tag.strip().lower()
        if tag in EMOJI_MAP:
            return EMOJI_MAP[tag]
    return '🔗'

def create_tags_html(tags_str):
    """Cria HTML de tags com badge"""
    if not tags_str:
        return ""
    tags = tags_str.split(',')
    html = ""
    for tag in tags:
        tag = tag.strip()
        if tag:
            html += f'<span class="px-2 py-1 bg-indigo-50 text-indigo-700 text-xs rounded-full font-medium hover:bg-indigo-100 transition-colors">{tag}</span>'
    return html

def create_steps_html(steps_str):
    """Cria lista de passos em HTML"""
    if not steps_str:
        return "<li>Importe o JSON e configure as credenciais.</li>"
    steps = steps_str.split('|')
    html = ""
    for i, step in enumerate(steps, 1):
        step = step.strip()
        if step:
            html += f'<li class="mb-3 flex gap-3"><span class="flex-shrink-0 flex items-center justify-center h-6 w-6 rounded-full bg-indigo-100 text-indigo-700 text-sm font-bold">{i}</span><span>{step}</span></li>'
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
    <title>Guias Completos de Integrações N8N | {len(templates)}+ Tutoriais Passo a Passo | AI Factory</title>
    <meta name="description" content="{len(templates)}+ guias passo a passo sobre como integrar ferramentas populares com N8N. Tutoriais com exemplos práticos e templates JSON.">
    <meta name="keywords" content="n8n, integrações, automação, workflow, tutorial, guia">
    <meta name="author" content="AI Factory">
    <link rel="canonical" href="https://felipejac.github.io/fabrica-n8n/integracoes/">
    
    <!-- Open Graph -->
    <meta property="og:title" content="Guias Completos de Integrações N8N">
    <meta property="og:description" content="{len(templates)}+ guias passo a passo sobre como integrar ferramentas populares com N8N.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://felipejac.github.io/fabrica-n8n/integracoes/">
    
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    
    <style>
        body {{ font-family: 'Inter', sans-serif; }}
        .integration-card {{ transition: all 0.3s ease; }}
        .integration-card:hover {{ transform: translateY(-4px); }}
    </style>
</head>
<body class="bg-slate-50 text-slate-800">
    <!-- Header / Navegação -->
    <header class="bg-white border-b border-slate-200 sticky top-0 z-50 shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-16">
                <a href="../index.html" class="font-bold text-xl text-indigo-600 flex items-center gap-2 hover:opacity-80 transition-opacity">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                    </svg>
                    AI Factory
                </a>
                <nav class="flex items-center gap-4">
                    <a href="../index.html" class="text-sm text-slate-600 hover:text-indigo-600 transition-colors">← Voltar</a>
                    <span class="text-slate-300">|</span>
                    <span class="text-sm font-medium text-indigo-600">Integrações ({len(templates)})</span>
                </nav>
            </div>
        </div>
    </header>

    <!-- Hero Section -->
    <div class="bg-gradient-to-r from-slate-900 to-slate-800 text-white py-12">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h1 class="text-4xl font-bold mb-4">Guias de Integrações N8N</h1>
            <p class="text-lg text-slate-300 max-w-2xl mx-auto mb-6">
                {len(templates)}+ tutoriais passo a passo para conectar suas ferramentas favoritas.
            </p>
            <div class="flex items-center justify-center gap-4 text-sm">
                <span class="bg-indigo-600/20 text-indigo-200 px-3 py-1 rounded-full">📚 {len(templates)}+ Guias</span>
                <span class="bg-green-600/20 text-green-200 px-3 py-1 rounded-full">✅ 100% Gratuito</span>
                <span class="bg-purple-600/20 text-purple-200 px-3 py-1 rounded-full">🎯 Passo a Passo</span>
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
                placeholder="Buscar integração (ex: WordPress, Shopify)..." 
                class="w-full px-4 py-3 rounded-lg border border-slate-300 focus:ring-2 focus:ring-indigo-500 focus:outline-none shadow-sm"
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
        index_content += f'''            <a href="{t['slug']}" class="integration-card block bg-white p-6 rounded-xl shadow-sm border border-slate-200 hover:shadow-lg hover:border-indigo-300 transition-all group">
                <div class="text-xs uppercase font-bold text-indigo-600 mb-2">{emoji} {t['software_a']} → {t['software_b']}</div>
                <h2 class="font-bold text-slate-900 mb-2 group-hover:text-indigo-600 transition-colors line-clamp-2">{sanitize_html(t['titulo'])}</h2>
                <p class="text-sm text-slate-600 line-clamp-2">{sanitize_html(t['desc'])}</p>
            </a>
'''
    
    index_content += '''        </div>

        <div id="noResults" class="hidden text-center py-12">
            <p class="text-slate-500 text-lg">Nenhuma integração encontrada para sua busca.</p>
        </div>
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-slate-200 mt-12 py-8">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-sm text-slate-600">
            <p class="mb-2">© 2024 <strong>AI Factory</strong></p>
            <p><a href="../index.html" class="text-indigo-600 hover:text-indigo-700 font-medium">← Voltar ao AI Factory</a></p>
        </div>
    </footer>

    <script>
        // Dados das integrações para filtro
        const integrations = '''
    
    # Adicionar dados para busca
    for t in templates:
        keywords = ','.join([tag.strip() for tag in t['tags'].split(',')] + [t['software_a'].lower(), t['software_b'].lower()])
        index_content += f'''{{
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
    print(f"✅ Índice do diretório gerado: {len(templates)} integrações indexadas")


def generate():
    """Função principal de geração"""
    print(f"🚀 Iniciando a fábrica de integrações otimizada...")
    print(f"📂 Pasta de saída: {OUTPUT_DIR}/")
    
    # 1. Ler Template
    try:
        with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
            template_content = f.read()
    except FileNotFoundError:
        print(f"❌ Erro: '{TEMPLATE_FILE}' não encontrado.")
        return

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
                
                print(f"📄 Gerado: {filename}")
                count += 1

    except FileNotFoundError:
        print(f"❌ Erro: '{CSV_FILE}' não encontrado.")
        return

    # 3. Gerar Índice do diretório
    generate_index_page(generated_templates)

    # 4. Atualizar menu do index.html principal (OPCIONAL)
    update_main_index(generated_templates)

    # ===== ESTATÍSTICAS =====
    elapsed_time = (datetime.now() - start_time).total_seconds()
    avg_time = (elapsed_time / count * 1000) if count > 0 else 0
    
    print(f"\n{'='*60}")
    print(f"✅ GERAÇÃO CONCLUÍDA COM SUCESSO!")
    print(f"{'='*60}")
    print(f"📊 Estatísticas:")
    print(f"   • Páginas geradas: {count}")
    print(f"   • Tempo total: {elapsed_time:.2f}s")
    print(f"   • Tempo por página: {avg_time:.2f}ms")
    print(f"   • Taxa: {count/elapsed_time:.0f} páginas/segundo")
    print(f"   • Pasta: {OUTPUT_DIR}/")
    print(f"{'='*60}\n")

def update_main_index(templates):
    """Atualiza o menu de integrações no index.html principal"""
    try:
        with open(MAIN_INDEX, 'r', encoding='utf-8') as f:
            main_content = f.read()
        
        # Contar integrações atuais
        if f'<!-- INTEGRATIONS_COUNT: {len(templates)} -->' not in main_content:
            # Adicionar comentário com contagem
            main_content = main_content.replace(
                '<button onclick="switchView(\'integrations\')" id="nav-integrations"',
                f'<!-- INTEGRATIONS_COUNT: {len(templates)} -->\n                <button onclick="switchView(\'integrations\')" id="nav-integrations"'
            )
            
            with open(MAIN_INDEX, 'w', encoding='utf-8') as f:
                f.write(main_content)
            
            print(f"✅ Index.html principal atualizado com {len(templates)} integrações")
    except Exception as e:
        print(f"⚠️  Aviso ao atualizar index.html: {e}")

if __name__ == "__main__":
    generate()
