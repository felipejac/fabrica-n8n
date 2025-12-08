import csv
import os
import json

# Configurações
CSV_FILE = 'automacoes_db.csv'
TEMPLATE_FILE = 'template_page.html'
OUTPUT_DIR = 'integracoes' # Pasta onde os HTMLs serão salvos

# Garante que a pasta de saída existe
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def create_tags_html(tags_str):
    if not tags_str: return ""
    tags = tags_str.split(',')
    html = ""
    for tag in tags:
        tag = tag.strip()
        html += f'<span class="px-2 py-1 bg-slate-100 text-slate-600 text-xs rounded hover:bg-slate-200 transition-colors cursor-default">{tag}</span>'
    return html

def create_steps_html(steps_str):
    if not steps_str: return "<li>Importe o JSON e configure as credenciais.</li>"
    steps = steps_str.split('|') # Usando pipe | como separador no CSV
    html = ""
    for step in steps:
        step = step.strip()
        if step:
            html += f'<li class="mb-2">{step}</li>'
    return html

def create_json_steps(steps_str):
    # Gera steps para o Schema.org JSON-LD
    if not steps_str: return ""
    steps = steps_str.split('|')
    json_steps = []
    for step in steps:
        step = step.strip()
        if step:
            json_steps.append(f'{{ "@type": "HowToStep", "text": "{step}" }}')
    return ",\n".join(json_steps)

def generate_index_page(templates):
    # Gera a página index.html do diretório /integracoes/
    index_content = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Diretório de Integrações N8N | N8N Factory</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-50 text-slate-800">
        <header class="bg-white border-b p-4 mb-8">
            <div class="max-w-6xl mx-auto flex justify-between items-center">
                <a href="../index.html" class="font-bold text-xl text-indigo-600 flex items-center gap-2">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" /></svg>
                    N8N Factory
                </a>
                <h1 class="text-lg text-slate-500">Diretório de Integrações</h1>
            </div>
        </header>
        <main class="max-w-6xl mx-auto px-4 pb-12">
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    """
    
    for t in templates:
        index_content += f"""
        <a href="{t['slug']}" class="block bg-white p-6 rounded-xl shadow-sm border hover:shadow-md transition-all group">
            <div class="text-xs uppercase font-bold text-indigo-600 mb-2 flex items-center gap-1">
                {t['software_a']} <span class="text-slate-300">→</span> {t['software_b']}
            </div>
            <h2 class="font-bold text-slate-900 mb-2 group-hover:text-indigo-600 transition-colors">{t['titulo']}</h2>
            <p class="text-sm text-slate-600 line-clamp-2">{t['desc']}</p>
        </a>
        """
    
    index_content += """
            </div>
        </main>
        <footer class="bg-white border-t border-slate-200 mt-auto py-8 text-center text-sm text-slate-500">
            <p>© 2024 N8N Factory.</p>
        </footer>
    </body>
    </html>
    """
    
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_content)
    print("✅ Índice do diretório gerado: index.html")

def generate():
    print(f"🚀 Iniciando a fábrica pSEO em '{OUTPUT_DIR}'...")
    
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
    
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                # Dados básicos
                page = template_content
                slug = row.get('slug_url', 'sem-slug').strip()
                
                if not slug: continue

                # Substituições Simples
                for key, value in row.items():
                    placeholder = f"{{{{ {key} }}}}"
                    page = page.replace(placeholder, value)

                # Substituições Complexas (HTML & JSON)
                tags_html = create_tags_html(row.get('tags', ''))
                page = page.replace('{{ tags_html }}', tags_html)

                steps_html = create_steps_html(row.get('passos_resumo', ''))
                page = page.replace('{{ lista_passos }}', steps_html)
                
                json_steps = create_json_steps(row.get('passos_resumo', ''))
                page = page.replace('{{ json_steps }}', json_steps)

                # Salvar Arquivo
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
                    'software_b': row.get('software_b', '')
                })
                
                print(f"📄 Gerado: {filename}")
                count += 1

    except FileNotFoundError:
        print(f"❌ Erro: '{CSV_FILE}' não encontrado.")
        return

    # 3. Gerar Índice
    generate_index_page(generated_templates)

    print(f"\n🎉 Concluído! {count} páginas de integração geradas.")

if __name__ == "__main__":
    generate()
