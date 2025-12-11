#!/usr/bin/env python3
"""
Script para atualizar automaticamente os filtros de categoria do blog
Analisa os badges dos posts e cria botões de filtro dinamicamente
"""

import re
from bs4 import BeautifulSoup
from collections import Counter

def extract_categories():
    """Extrai todas as categorias dos posts"""
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    articles = soup.find_all('article')
    
    categories = []
    for article in articles:
        badge = article.find('span', class_=lambda x: x and 'bg-' in x and 'px-2' in x)
        if badge:
            category = badge.get_text().strip()
            categories.append(category)
    
    return Counter(categories)

def generate_filter_buttons(category_count, min_posts=2):
    """Gera HTML dos botões de filtro baseado nas categorias"""
    
    # Categorias principais (com pelo menos min_posts)
    main_categories = {cat: count for cat, count in category_count.items() if count >= min_posts}
    
    # Mapear categorias similares
    category_map = {
        'Comparação': ['Comparação'],
        'DevOps': ['DevOps', 'Cloud'],
        'Segurança': ['Segurança', 'Compliance'],
        'Tutorial': ['Tutorial', 'Setup'],
        'Automação': ['Automação', 'Integração'],
        'IA': ['IA', 'Agentes', 'RAG', 'Local AI', 'Voice AI'],
        'Desenvolvimento': ['Desenvolvimento', 'Plugins', 'Frontend', 'Backend', 'Frameworks'],
        'Marketing': ['Marketing', 'Growth', 'Marketing Digital', 'Conteúdo'],
        'Análise': ['Economia', 'Análise de Mercado', 'Tendências', 'Negócios'],
        'Ferramentas': ['Scraping', 'Templates', 'Chatbots', 'CRM']
    }
    
    # Calcular posts por categoria agrupada
    grouped_categories = {}
    for group_name, keywords in category_map.items():
        count = sum(category_count.get(kw, 0) for kw in keywords)
        if count > 0:
            grouped_categories[group_name] = count
    
    # Ordenar por quantidade (desc)
    sorted_categories = sorted(grouped_categories.items(), key=lambda x: x[1], reverse=True)
    
    # Gerar HTML dos botões
    buttons_html = '                <button class="filter-btn px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold text-sm" data-filter="all">Todos</button>\n'
    
    for category, count in sorted_categories[:8]:  # Top 8 categorias + Todos
        cat_lower = category.lower()
        buttons_html += f'                <button class="filter-btn px-4 py-2 bg-gray-200 text-gray-700 rounded-lg font-semibold text-sm hover:bg-gray-300 transition" data-filter="{cat_lower}">{category}</button>\n'
    
    return buttons_html.rstrip('\n'), category_map

def generate_filter_script(category_map):
    """Gera o script JavaScript para os filtros"""
    
    # Criar mapeamento de filtros para keywords
    filter_mapping = {}
    for group_name, keywords in category_map.items():
        filter_mapping[group_name.lower()] = [k.lower() for k in keywords]
    
    script = """    <!-- Filter Functionality -->
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const filterButtons = document.querySelectorAll('.filter-btn');
            const articles = document.querySelectorAll('article');
            
            // Mapeamento de filtros para categorias
            const filterMap = """ + str(filter_mapping).replace("'", '"') + """;
            
            filterButtons.forEach(button => {
                button.addEventListener('click', function() {
                    const filter = this.getAttribute('data-filter').toLowerCase();
                    
                    // Update active button style
                    filterButtons.forEach(btn => {
                        btn.classList.remove('bg-blue-600', 'text-white');
                        btn.classList.add('bg-gray-200', 'text-gray-700');
                    });
                    this.classList.remove('bg-gray-200', 'text-gray-700');
                    this.classList.add('bg-blue-600', 'text-white');
                    
                    // Filter articles
                    let visibleCount = 0;
                    articles.forEach(article => {
                        if (filter === 'all') {
                            article.style.display = 'block';
                            visibleCount++;
                        } else {
                            const categoryBadge = article.querySelector('span[class*="bg-"][class*="px-2"]');
                            
                            if (categoryBadge) {
                                const categoryText = categoryBadge.textContent.toLowerCase().trim();
                                const keywords = filterMap[filter] || [];
                                
                                const shouldShow = keywords.some(keyword => 
                                    categoryText.includes(keyword.toLowerCase())
                                );
                                
                                article.style.display = shouldShow ? 'block' : 'none';
                                if (shouldShow) visibleCount++;
                            } else {
                                article.style.display = 'none';
                            }
                        }
                    });
                    
                    console.log(`🔍 Filtro "${filter}": ${visibleCount} posts exibidos`);
                });
            });
        });
    </script>"""
    
    return script

def update_index_html():
    """Atualiza o index.html com novos filtros"""
    
    print("🔄 Analisando categorias...")
    category_count = extract_categories()
    
    print(f"✅ Encontradas {len(category_count)} categorias únicas")
    print(f"📊 Total de posts: {sum(category_count.values())}\n")
    
    print("📋 Top 10 categorias:")
    for cat, count in category_count.most_common(10):
        print(f"   • {cat}: {count} posts")
    
    print("\n🔧 Gerando botões de filtro...")
    buttons_html, category_map = generate_filter_buttons(category_count)
    
    print("📝 Gerando script de filtro...")
    filter_script = generate_filter_script(category_map)
    
    # Ler arquivo atual
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Substituir botões de filtro
    pattern = r'(<div class="flex gap-2" id="filter-buttons">)(.*?)(</div>)'
    replacement = r'\1\n' + buttons_html + '\n            \3'
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Substituir script de filtro
    pattern = r'(<!-- Filter Functionality -->)(.*?)(</script>)'
    replacement = filter_script
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Salvar arquivo atualizado
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("\n✅ index.html atualizado com sucesso!")
    print(f"🎯 Criados {len(category_map)} grupos de filtros")
    
    return category_map

if __name__ == "__main__":
    category_map = update_index_html()
    
    print("\n📊 GRUPOS DE FILTRO CRIADOS:")
    print("=" * 50)
    for group, keywords in sorted(category_map.items()):
        print(f"{group}:")
        print(f"  Keywords: {', '.join(keywords)}")
    print("=" * 50)
