#!/usr/bin/env python3
"""
Generate segmented sitemaps from CSV databases and file structure
Usage: python generate_sitemaps.py
"""

import csv
import os
from datetime import datetime
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

BASE_URL = "https://www.automationscookbook.com"
OUTPUT_DIR = Path(__file__).parent

def prettify_xml(elem):
    """Return pretty-printed XML string"""
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ", encoding="UTF-8").decode('utf-8')

def get_last_modified():
    """Get current date in ISO format"""
    return datetime.now().strftime("%Y-%m-%d")

def create_sitemap_index():
    """Create sitemap-index.xml"""
    urlset = Element('sitemapindex', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    
    sitemaps = [
        "sitemap-institucional.xml",
        "sitemap-integracoes-n8n.xml",
        "sitemap-integracoes-zapier.xml",
        "sitemap-blog.xml",
    ]
    
    for sitemap_file in sitemaps:
        sitemap_elem = SubElement(urlset, 'sitemap')
        SubElement(sitemap_elem, 'loc').text = f"{BASE_URL}/{sitemap_file}"
        SubElement(sitemap_elem, 'lastmod').text = get_last_modified()
    
    xml_content = prettify_xml(urlset)
    output_file = OUTPUT_DIR / "sitemap-index.xml"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print(f"✅ Created {output_file}")
    return True

def create_institutional_sitemap():
    """Create sitemap-institucional.xml"""
    urlset = Element('urlset', 
                     xmlns="http://www.sitemaps.org/schemas/sitemap/0.9",
                     attrib={'{http://www.w3.org/1999/xhtml}xhtml': 'http://www.w3.org/1999/xhtml'})
    
    pages = [
        {"url": "/", "priority": "1.0", "changefreq": "daily"},
        {"url": "/sobre", "priority": "0.8", "changefreq": "monthly"},
        {"url": "/llm", "priority": "0.9", "changefreq": "weekly"},
        {"url": "/ai-agents", "priority": "0.9", "changefreq": "monthly"},
        {"url": "/blog", "priority": "0.9", "changefreq": "daily"},
        {"url": "/blog/index.html", "priority": "0.9", "changefreq": "daily"},
        {"url": "/guia-automacoes-n8n", "priority": "0.8", "changefreq": "weekly"},
        {"url": "/guia-automacoes-zapier", "priority": "0.8", "changefreq": "weekly"},
        {"url": "/integracoes", "priority": "0.8", "changefreq": "weekly"},
        {"url": "/integracoes/index.html", "priority": "0.8", "changefreq": "weekly"},
    ]
    
    for page in pages:
        url_elem = SubElement(urlset, 'url')
        SubElement(url_elem, 'loc').text = f"{BASE_URL}{page['url']}"
        SubElement(url_elem, 'lastmod').text = get_last_modified()
        SubElement(url_elem, 'changefreq').text = page['changefreq']
        SubElement(url_elem, 'priority').text = page['priority']
    
    xml_content = prettify_xml(urlset)
    output_file = OUTPUT_DIR / "sitemap-institucional.xml"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print(f"✅ Created {output_file} with {len(pages)} pages")
    return True

def create_n8n_templates_sitemap():
    """Create sitemap-integracoes-n8n.xml from CSV"""
    csv_file = OUTPUT_DIR / "automacoes_db.csv"
    
    if not csv_file.exists():
        print(f"⚠️  CSV not found: {csv_file}")
        return False
    
    urlset = Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        
        for row in reader:
            # Try url_template first, fallback to slug_url
            url_template = row.get('url_template', '').strip()
            if not url_template:
                slug = row.get('slug_url', '').strip()
                if slug:
                    url_template = f"{BASE_URL}/integracoes/{slug}.html"
            
            if not url_template:
                continue
            
            url_elem = SubElement(urlset, 'url')
            SubElement(url_elem, 'loc').text = url_template
            SubElement(url_elem, 'lastmod').text = get_last_modified()
            SubElement(url_elem, 'changefreq').text = "monthly"
            SubElement(url_elem, 'priority').text = "0.7"
            
            count += 1
    
    xml_content = prettify_xml(urlset)
    output_file = OUTPUT_DIR / "sitemap-integracoes-n8n.xml"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print(f"✅ Created {output_file} with {count} N8N template URLs")
    return True

def create_zapier_templates_sitemap():
    """Create sitemap-integracoes-zapier.xml from CSV"""
    csv_file = OUTPUT_DIR / "automacoes_zapier_db.csv"
    
    if not csv_file.exists():
        print(f"⚠️  CSV not found: {csv_file}")
        return False
    
    urlset = Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        
        for row in reader:
            # Try url_template first, fallback to slug_url
            url_template = row.get('url_template', '').strip()
            if not url_template:
                slug = row.get('slug_url', '').strip()
                if slug:
                    url_template = f"{BASE_URL}/integracoes-zapier/{slug}.html"
            
            if not url_template:
                continue
            
            url_elem = SubElement(urlset, 'url')
            SubElement(url_elem, 'loc').text = url_template
            SubElement(url_elem, 'lastmod').text = get_last_modified()
            SubElement(url_elem, 'changefreq').text = "monthly"
            SubElement(url_elem, 'priority').text = "0.7"
            
            count += 1
    
    xml_content = prettify_xml(urlset)
    output_file = OUTPUT_DIR / "sitemap-integracoes-zapier.xml"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print(f"✅ Created {output_file} with {count} Zapier template URLs")
    return True

def create_blog_sitemap():
    """Create sitemap-blog.xml from blog/ directory"""
    blog_dir = OUTPUT_DIR / "blog"
    
    if not blog_dir.exists():
        print(f"⚠️  Blog directory not found: {blog_dir}")
        return False
    
    urlset = Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    
    html_files = list(blog_dir.glob("*.html"))
    # Exclude index.html and template files
    html_files = [f for f in html_files if f.name not in ['index.html', 'template.html', 'template_page.html']]
    
    for html_file in html_files:
        url_elem = SubElement(urlset, 'url')
        SubElement(url_elem, 'loc').text = f"{BASE_URL}/blog/{html_file.name}"
        SubElement(url_elem, 'lastmod').text = get_last_modified()
        SubElement(url_elem, 'changefreq').text = "weekly"
        SubElement(url_elem, 'priority').text = "0.8"
    
    xml_content = prettify_xml(urlset)
    output_file = OUTPUT_DIR / "sitemap-blog.xml"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print(f"✅ Created {output_file} with {len(html_files)} blog articles")
    return True

def main():
    print("🚀 Generating segmented sitemaps...\n")
    
    success = []
    success.append(create_sitemap_index())
    success.append(create_institutional_sitemap())
    success.append(create_n8n_templates_sitemap())
    success.append(create_zapier_templates_sitemap())
    success.append(create_blog_sitemap())
    
    if all(success):
        print("\n✅ All sitemaps generated successfully!")
        print("\n📝 Next steps:")
        print("   1. Submit sitemap-index.xml to Google Search Console")
        print("   2. Update robots.txt with new sitemap URLs")
        print("   3. Test URLs with Google Rich Results Test")
        print("   4. Monitor indexing in Search Console")
    else:
        print("\n⚠️  Some sitemaps failed to generate. Check errors above.")

if __name__ == "__main__":
    main()
