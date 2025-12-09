#!/usr/bin/env python3
"""
Gerador automático de sitemap.xml otimizado para SEO e LLMs
Cria sitemap com todas as 13.269+ páginas de templates
"""

import csv
import os
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

def generate_sitemap(
    csv_file='automacoes_db.csv',
    base_url='https://www.automationscookbook.com',
    output_file='sitemap.xml'
):
    """
    Gera sitemap.xml completo do site
    """
    
    print(f"🗺️  Gerando sitemap.xml...")
    print(f"📖 Lendo {csv_file}...")
    
    # Root element
    urlset = Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    urlset.set('xmlns:xhtml', 'http://www.w3.org/1999/xhtml')
    
    # Get current date for lastmod
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Priority and changefreq mapping
    priority_map = {
        'homepage': ('1.0', 'weekly'),
        'main_pages': ('0.9', 'weekly'),
        'integrations_index': ('0.8', 'daily'),
        'templates': ('0.7', 'monthly'),
    }
    
    # Add main pages
    main_pages = [
        ('/', 'homepage', today),
        ('/sobre', 'main_pages', today),
        ('/llm', 'main_pages', today),
        ('/guia-automacoes-n8n', 'main_pages', today),
        ('/casos-de-uso', 'main_pages', today),
        ('/integracoes/', 'integrations_index', today),
        ('/integracoes/index.html', 'integrations_index', today),
    ]
    
    print(f"📄 Adicionando páginas principais...")
    for path, page_type, lastmod in main_pages:
        url = SubElement(urlset, 'url')
        SubElement(url, 'loc').text = f"{base_url}{path}"
        SubElement(url, 'lastmod').text = lastmod
        SubElement(url, 'changefreq').text = priority_map[page_type][1]
        SubElement(url, 'priority').text = priority_map[page_type][0]
    
    # Add template pages from CSV
    print(f"📚 Adicionando templates do CSV...")
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        
        for row in reader:
            slug = row['slug_url']
            url_path = f"/integracoes/{slug}.html"
            
            url = SubElement(urlset, 'url')
            SubElement(url, 'loc').text = f"{base_url}{url_path}"
            SubElement(url, 'lastmod').text = today
            SubElement(url, 'changefreq').text = priority_map['templates'][1]
            SubElement(url, 'priority').text = priority_map['templates'][0]
            
            count += 1
            
            if count % 1000 == 0:
                print(f"   {count} templates adicionados...")
    
    print(f"✅ Total: {count + len(main_pages)} URLs")
    
    # Pretty print XML
    xml_str = minidom.parseString(tostring(urlset)).toprettyxml(indent="  ")
    
    # Remove empty lines
    xml_lines = [line for line in xml_str.split('\n') if line.strip()]
    xml_str = '\n'.join(xml_lines)
    
    # Save sitemap
    print(f"💾 Salvando {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_str)
    
    # Calculate size
    size_kb = os.path.getsize(output_file) / 1024
    print(f"✅ Sitemap gerado: {size_kb:.1f} KB")
    
    # Generate sitemap index if needed (>50k URLs)
    if count > 50000:
        print(f"⚠️  Aviso: {count} URLs excedem limite de 50k")
        print(f"   Considere criar sitemap index")
    
    return output_file

def generate_robots_txt(
    base_url='https://www.automationscookbook.com',
    sitemap_path='sitemap.xml',
    output_file='robots.txt'
):
    """
    Gera robots.txt otimizado
    """
    
    print(f"🤖 Gerando {output_file}...")
    
    robots_content = f"""# Automations Cookbook - Robots.txt
# Website: {base_url}
# Open-source automation templates library

User-agent: *
Allow: /

# Sitemap
Sitemap: {base_url}/{sitemap_path}

# LLM & AI Crawlers - Welcome!
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: Claude-Web
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: CCBot
Allow: /

User-agent: PerplexityBot
Allow: /

# Specific optimizations
Crawl-delay: 0

# Disallow admin/private areas (if any)
# Disallow: /admin/
# Disallow: /private/

# Allow all integrations
Allow: /integracoes/

# Allow API documentation
Allow: /llm
Allow: /sobre

# Allow CSV data
Allow: /automacoes_db.csv
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(robots_content.strip() + '\n')
    
    print(f"✅ {output_file} criado")
    return output_file

if __name__ == '__main__':
    # Generate sitemap
    sitemap_file = generate_sitemap()
    
    print()
    
    # Generate robots.txt
    robots_file = generate_robots_txt()
    
    print()
    print("=" * 60)
    print("✅ SEO optimization concluída!")
    print(f"   - {sitemap_file}")
    print(f"   - {robots_file}")
    print()
    print("📊 Próximo passo: commit e deploy")
    print("=" * 60)
