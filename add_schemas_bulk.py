#!/usr/bin/env python3
"""
Add HowTo + FAQPage schemas to N8N template HTML files in bulk
Usage: python add_schemas_bulk.py [--limit N] [--dry-run]
"""

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup

BASE_URL = "https://www.automationscookbook.com"
WORKSPACE_DIR = Path(__file__).parent

def extract_software_names(title):
    """Extract software A and B from title"""
    # Try pattern: "Software A para Software B"
    match = re.search(r'([A-Za-z0-9\s]+)\s+para\s+([A-Za-z0-9\s]+)', title, re.IGNORECASE)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    
    # Try pattern: "Software A → Software B" or "Software A to Software B"
    match = re.search(r'([A-Za-z0-9\s]+)\s+(?:→|to)\s+([A-Za-z0-9\s]+)', title, re.IGNORECASE)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    
    return None, None

def generate_howto_schema(template_data, html_url):
    """Generate HowTo schema for a template"""
    software_a = template_data.get('software_a', 'Software A')
    software_b = template_data.get('software_b', 'Software B')
    title = template_data.get('titulo_pagina', '')
    description = template_data.get('descricao_curta', '')
    steps = template_data.get('passos_resumo', '').split('|')
    
    schema = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "@id": f"{html_url}#howto",
        "name": title,
        "description": description,
        "image": f"{BASE_URL}/assets/integrations/{software_a.lower()}-{software_b.lower()}.png",
        "totalTime": "PT15M",
        "estimatedCost": {
            "@type": "MonetaryAmount",
            "currency": "BRL",
            "value": "0"
        },
        "tool": [
            {"@type": "HowToTool", "name": "n8n (self-hosted ou cloud)"},
            {"@type": "HowToTool", "name": f"Conta {software_a} com API"},
            {"@type": "HowToTool", "name": f"Conta {software_b} com API"}
        ],
        "supply": [
            {"@type": "HowToSupply", "name": f"Credenciais de API do {software_a}"},
            {"@type": "HowToSupply", "name": f"API key do {software_b}"}
        ],
        "step": []
    }
    
    # Add steps
    for i, step_text in enumerate(steps, 1):
        if step_text.strip():
            schema["step"].append({
                "@type": "HowToStep",
                "position": i,
                "name": step_text.strip(),
                "text": f"No n8n, configure o node '{step_text.strip()}' seguindo as instruções da documentação oficial.",
                "url": f"{html_url}#step{i}"
            })
    
    return schema

def generate_faq_schema(template_data, html_url):
    """Generate FAQPage schema for a template"""
    software_a = template_data.get('software_a', 'Software A')
    software_b = template_data.get('software_b', 'Software B')
    
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "@id": f"{html_url}#faq",
        "mainEntity": [
            {
                "@type": "Question",
                "name": "Quanto tempo leva para configurar esta integração?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"A configuração completa da integração entre {software_a} e {software_b} no n8n leva aproximadamente 15 minutos, incluindo criação de credenciais de API e testes iniciais."
                }
            },
            {
                "@type": "Question",
                "name": f"Quais planos do {software_a} e {software_b} são necessários?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"Você precisa de planos que permitam acesso à API em ambas as plataformas. Verifique a documentação oficial de {software_a} e {software_b} para requisitos específicos de API."
                }
            },
            {
                "@type": "Question",
                "name": "Este template é gratuito?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Sim, todos os templates do Automations Cookbook são 100% gratuitos e open-source sob licença MIT. Você pode usar, modificar e distribuir livremente."
                }
            },
            {
                "@type": "Question",
                "name": "Preciso ter conhecimentos de programação?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Não é necessário. O n8n é uma plataforma no-code/low-code. Este template já vem pronto para importar e usar. Conhecimentos básicos de APIs ajudam, mas não são obrigatórios."
                }
            },
            {
                "@type": "Question",
                "name": "Como faço para personalizar este workflow?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Após importar o template JSON no n8n, você pode adicionar ou remover nodes, ajustar lógicas com nodes IF/Switch, e personalizar mensagens e dados usando expressões do n8n."
                }
            },
            {
                "@type": "Question",
                "name": "O workflow funciona em tempo real?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"Sim! Quando configurado com triggers (webhooks ou polling), o n8n processa dados em tempo real entre {software_a} e {software_b}, geralmente em menos de 5 segundos."
                }
            }
        ]
    }
    
    return schema

def generate_breadcrumb_schema(template_data, html_url):
    """Generate BreadcrumbList schema"""
    slug = template_data.get('slug_url', '')
    title = template_data.get('titulo_pagina', '')
    
    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "@id": f"{html_url}#breadcrumb",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Home",
                "item": BASE_URL
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": "Integrações N8N",
                "item": f"{BASE_URL}/integracoes/"
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": title,
                "item": html_url
            }
        ]
    }
    
    return schema

def has_existing_schema(soup):
    """Check if HTML already has schema.org structured data"""
    scripts = soup.find_all('script', {'type': 'application/ld+json'})
    for script in scripts:
        try:
            data = json.loads(script.string)
            if isinstance(data, dict):
                if data.get('@type') in ['HowTo', 'FAQPage'] or '@graph' in data:
                    return True
        except:
            continue
    return False

def add_schemas_to_html(html_path, template_data, dry_run=False):
    """Add schemas to HTML file"""
    
    if not html_path.exists():
        print(f"  ⚠️  File not found: {html_path}")
        return False
    
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Check if already has schemas
        if has_existing_schema(soup):
            print(f"  ℹ️  Already has schema, skipping: {html_path.name}")
            return False
        
        # Generate URL
        slug = template_data.get('slug_url', '')
        html_url = f"{BASE_URL}/integracoes/{slug}.html"
        
        # Generate schemas
        howto_schema = generate_howto_schema(template_data, html_url)
        faq_schema = generate_faq_schema(template_data, html_url)
        breadcrumb_schema = generate_breadcrumb_schema(template_data, html_url)
        
        # Combine in @graph
        combined_schema = {
            "@context": "https://schema.org",
            "@graph": [howto_schema, faq_schema, breadcrumb_schema]
        }
        
        # Create script tag
        schema_json = json.dumps(combined_schema, indent=2, ensure_ascii=False)
        
        # Find head tag
        head = soup.find('head')
        if not head:
            print(f"  ⚠️  No <head> tag found: {html_path.name}")
            return False
        
        # Insert schema script (replace existing if any)
        existing_schema = head.find('script', {'type': 'application/ld+json'})
        if existing_schema:
            existing_schema.extract()
        
        # Add comment before schema
        schema_comment = soup.new_tag('comment')
        schema_comment.string = ' Enhanced Schema.org (HowTo + FAQPage + BreadcrumbList) '
        
        new_script = soup.new_tag('script', type='application/ld+json')
        new_script.string = f"\n{schema_json}\n    "
        
        # Insert before </head>
        head.append(soup.new_string('\n    '))
        head.append(schema_comment)
        head.append(soup.new_string('\n    '))
        head.append(new_script)
        head.append(soup.new_string('\n    '))
        
        if dry_run:
            print(f"  🔍 [DRY RUN] Would add schemas to: {html_path.name}")
            return True
        
        # Write back
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        print(f"  ✅ Added schemas to: {html_path.name}")
        return True
        
    except Exception as e:
        print(f"  ❌ Error processing {html_path.name}: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Add Schema.org to N8N templates in bulk')
    parser.add_argument('--limit', type=int, default=20, help='Number of templates to process (default: 20)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    parser.add_argument('--skip', type=int, default=0, help='Skip first N templates')
    args = parser.parse_args()
    
    print("🚀 Adding Schema.org to N8N Templates\n")
    
    # Read CSV
    csv_file = WORKSPACE_DIR / "automacoes_db.csv"
    if not csv_file.exists():
        print(f"❌ CSV not found: {csv_file}")
        sys.exit(1)
    
    templates = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            templates.append(row)
    
    print(f"📊 Found {len(templates)} templates in CSV\n")
    
    # Apply skip and limit
    templates_to_process = templates[args.skip:args.skip + args.limit]
    
    print(f"🎯 Processing {len(templates_to_process)} templates (skip: {args.skip}, limit: {args.limit})\n")
    if args.dry_run:
        print("🔍 DRY RUN MODE - No files will be modified\n")
    
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for i, template in enumerate(templates_to_process, 1):
        slug = template.get('slug_url', '')
        title = template.get('titulo_pagina', '')
        
        print(f"[{i}/{len(templates_to_process)}] {title}")
        
        if not slug:
            print(f"  ⚠️  No slug found, skipping")
            skip_count += 1
            continue
        
        html_path = WORKSPACE_DIR / "integracoes" / f"{slug}.html"
        
        result = add_schemas_to_html(html_path, template, args.dry_run)
        if result:
            success_count += 1
        elif result is False:
            skip_count += 1
        else:
            error_count += 1
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Success: {success_count}")
    print(f"ℹ️  Skipped: {skip_count} (already have schemas or not found)")
    print(f"❌ Errors:  {error_count}")
    print(f"📝 Total:   {len(templates_to_process)}")
    
    if args.dry_run:
        print(f"\n🔍 This was a DRY RUN - no files were modified")
        print(f"   Remove --dry-run to apply changes")
    else:
        print(f"\n✅ Schema.org successfully added to {success_count} templates!")
        print(f"\n📝 Next steps:")
        print(f"   1. Test with Google Rich Results Test")
        print(f"   2. Commit changes to git")
        print(f"   3. Run again with --skip {args.skip + args.limit} to process next batch")

if __name__ == "__main__":
    main()
