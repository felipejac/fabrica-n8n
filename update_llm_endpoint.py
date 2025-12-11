#!/usr/bin/env python3
"""
Script para atualizar o endpoint /llm com estatísticas atualizadas
Conta templates N8N, Zapier e artigos do blog automaticamente
"""

import os
import csv
import re
from pathlib import Path

def count_n8n_templates():
    """Conta templates N8N no CSV"""
    csv_file = 'automacoes_db.csv'
    if not os.path.exists(csv_file):
        return 0
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return sum(1 for row in reader)

def count_zapier_templates():
    """Conta templates Zapier no CSV"""
    csv_file = 'automacoes_zapier_db.csv'
    if not os.path.exists(csv_file):
        return 0
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return sum(1 for row in reader)

def count_blog_articles():
    """Conta artigos do blog"""
    blog_dir = Path('blog')
    if not blog_dir.exists():
        return 0
    
    # Excluir templates e arquivos especiais
    exclude_files = {'email_template_welcome.html', 'template_page.html', 'index.html'}
    
    html_files = [
        f for f in blog_dir.glob('*.html')
        if f.name not in exclude_files
    ]
    
    return len(html_files)

def update_llm_html():
    """Atualiza llm.html com estatísticas corretas"""
    llm_file = 'llm.html'
    
    if not os.path.exists(llm_file):
        print(f"❌ Arquivo {llm_file} não encontrado")
        return False
    
    # Contar recursos
    n8n_count = count_n8n_templates()
    zapier_count = count_zapier_templates()
    blog_count = count_blog_articles()
    total_count = n8n_count + zapier_count
    
    print(f"\n📊 Estatísticas Atuais:")
    print(f"  N8N Templates: {n8n_count:,}")
    print(f"  Zapier Templates: {zapier_count:,}")
    print(f"  Total Templates: {total_count:,}")
    print(f"  Artigos do Blog: {blog_count}")
    
    # Ler conteúdo do arquivo
    with open(llm_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Atualizar números no conteúdo
    replacements = [
        # Meta description
        (r'(\d+[\d,]*)\+ automation templates', f'{total_count:,}+ automation templates'),
        
        # Intro section - total templates
        (r'database of <strong>(\d+[\d,]*)\+ automation templates</strong>', 
         f'database of <strong>{total_count:,}+ automation templates</strong>'),
        
        # N8N badge
        (r'🔷 (\d+[\d,]*) N8N templates', f'🔷 {n8n_count:,} N8N templates'),
        
        # Zapier badge
        (r'⚡ (\d+[\d,]*) Zapier templates', f'⚡ {zapier_count:,} Zapier templates'),
        
        # N8N Quick Access
        (r'Full dataset of (\d+[\d,]*) N8N templates', 
         f'Full dataset of {n8n_count:,} N8N templates'),
        
        # Zapier Quick Access
        (r'Dataset of (\d+[\d,]*) Zapier templates', 
         f'Dataset of {zapier_count:,} Zapier templates'),
        
        # N8N HTML pages
        (r'(\d+[\d,]*) individual template pages with Schema', 
         f'{n8n_count:,} individual template pages with Schema'),
        
        # Data structure section
        (r'<strong>(\d+[\d,]*) records</strong> following this schema', 
         f'<strong>{n8n_count:,} records</strong> following this schema'),
        
        # Coverage - Total
        (r'<div class="text-4xl font-bold text-purple-600 mb-2">(\d+[\d,]*)</div>\s*<p class="text-slate-600">Total Templates</p>',
         f'<div class="text-4xl font-bold text-purple-600 mb-2">{total_count:,}</div>\n                    <p class="text-slate-600">Total Templates</p>'),
        
        # Coverage - N8N
        (r'<div class="text-4xl font-bold text-indigo-600 mb-2">(\d+[\d,]*)</div>\s*<p class="text-slate-600">N8N Templates</p>',
         f'<div class="text-4xl font-bold text-indigo-600 mb-2">{n8n_count:,}</div>\n                    <p class="text-slate-600">N8N Templates</p>'),
        
        # Coverage - Zapier
        (r'<div class="text-4xl font-bold text-orange-600 mb-2">(\d+[\d,]*)</div>\s*<p class="text-slate-600">Zapier Templates</p>',
         f'<div class="text-4xl font-bold text-orange-600 mb-2">{zapier_count:,}</div>\n                    <p class="text-slate-600">Zapier Templates</p>'),
    ]
    
    # Aplicar substituições
    modified = False
    for pattern, replacement in replacements:
        new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        if new_content != content:
            modified = True
            content = new_content
    
    # Adicionar seção do Blog se ainda não existir
    if 'Blog Articles' not in content and blog_count > 0:
        # Encontrar a seção de Zapier HTML Pages e adicionar blog após
        blog_section = f'''                <a href="/blog" class="block p-6 bg-white border border-green-200 rounded-lg hover:shadow-lg transition">
                    <div class="flex items-center gap-3 mb-2">
                        <span class="text-3xl">📝</span>
                        <h3 class="text-xl font-bold">Blog Articles</h3>
                    </div>
                    <p class="text-slate-600 mb-3">{blog_count} in-depth articles about automation, AI agents, and no-code tools</p>
                    <code class="text-sm bg-slate-100 px-2 py-1 rounded">/blog/*.html</code>
                </a>'''
        
        # Inserir após a seção de Zapier HTML Pages
        zapier_section_end = content.find('</code>\n                </a>\n            </div>\n        </section>', 
                                          content.find('Zapier HTML Pages'))
        
        if zapier_section_end != -1:
            # Encontrar o final da última tag </a> antes de </div>
            insert_pos = content.find('</a>', zapier_section_end) + 4
            content = content[:insert_pos] + '\n' + blog_section + content[insert_pos:]
            modified = True
            print(f"\n✅ Adicionada seção do Blog com {blog_count} artigos")
    
    # Salvar se modificado
    if modified:
        with open(llm_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\n✅ Arquivo {llm_file} atualizado com sucesso!")
        return True
    else:
        print(f"\n ℹ️  Nenhuma atualização necessária em {llm_file}")
        return False

def main():
    """Função principal"""
    print("🔄 Atualizando endpoint /llm...")
    
    success = update_llm_html()
    
    if success:
        print("\n🎉 Endpoint /llm atualizado!")
        print("\n💡 Dica: Execute este script sempre que:")
        print("   - Adicionar novos templates N8N ou Zapier")
        print("   - Publicar novos artigos no blog")
        print("   - Antes de fazer deploy para produção")
    else:
        print("\n⚠️  Verifique se os arquivos CSV existem e se há artigos no blog")
    
    return success

if __name__ == '__main__':
    main()
