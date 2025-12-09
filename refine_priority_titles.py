#!/usr/bin/env python3
"""
Refinamento de títulos e metas para templates prioritários
Foco: CRM, WhatsApp, E-commerce, Marketing (200-500 templates)
"""

import csv
import json
from collections import defaultdict

# Softwares prioritários por categoria
PRIORITY_SOFTWARE = {
    'CRM': ['Pipedrive', 'HubSpot', 'RD Station', 'Salesforce', 'Kommo', 'Zoho CRM'],
    'WhatsApp': ['WhatsApp', 'Chatwoot', 'Kommo', 'Twilio WhatsApp'],
    'E-commerce': ['Shopify', 'WooCommerce', 'Mercado Livre', 'Bling', 'Magento', 'VTEX'],
    'Marketing': ['Facebook', 'Google Ads', 'Instagram', 'LinkedIn', 'Meta Ads', 'TikTok']
}

def categorize_template(software_a, software_b, tags):
    """Identifica categoria do template"""
    combined = f"{software_a} {software_b} {tags}".lower()
    categories = []
    
    for category, softwares in PRIORITY_SOFTWARE.items():
        for software in softwares:
            if software.lower() in combined:
                categories.append(category)
                break
    
    return categories if categories else ['Outros']

def optimize_title(software_a, software_b, tipo_evento):
    """
    Gera título otimizado formato:
    "Como [ação] entre [A] e [B] usando N8N | Automations Cookbook"
    """
    
    actions = {
        'Lead': 'capturar e enviar leads',
        'Venda': 'sincronizar vendas',
        'Formulário': 'processar respostas',
        'Notificação': 'receber alertas',
        'Email': 'automatizar emails',
        'Pedido': 'processar pedidos',
        'Dados': 'sincronizar dados',
        'Pagamento': 'processar pagamentos',
    }
    
    action = actions.get(tipo_evento, 'integrar')
    a_clean = software_a.replace(' (Chatwoot)', '').replace(' (Kommo)', '')
    b_clean = software_b.replace(' (Chatwoot)', '').replace(' (Kommo)', '')
    
    return f"Como {action} entre {a_clean} e {b_clean} usando N8N | Automations Cookbook"

def optimize_meta(software_a, software_b, tipo_evento, caso_uso):
    """
    Meta description 120-160 caracteres
    Linguagem natural focada em benefício
    """
    
    benefits = {
        'Lead': 'Economize tempo e nunca perca uma oportunidade.',
        'Venda': 'Mantenha seu time informado em tempo real.',
        'Formulário': 'Análise de dados eficiente e automática.',
        'Notificação': 'Configure em minutos com template pronto.',
        'Email': 'Economize horas de trabalho manual.',
        'Pedido': 'Reduza erros e acelere sua logística.',
        'Dados': 'Mantenha tudo sincronizado sem esforço.',
        'Pagamento': 'Reduza inadimplência com automação.',
    }
    
    a_clean = software_a.replace(' (Chatwoot)', '').replace(' (Kommo)', '')
    b_clean = software_b.replace(' (Chatwoot)', '').replace(' (Kommo)', '')
    benefit = benefits.get(tipo_evento, 'Template pronto para usar.')
    
    meta = f"Automatize a integração entre {a_clean} e {b_clean}. {benefit} Workflow N8N pronto."
    
    return meta[:160]

def main():
    print("=" * 80)
    print("🎯 Refinamento de Títulos e Metas - Templates Prioritários")
    print("=" * 80)
    print()
    
    priority_templates = []
    stats = defaultdict(int)
    category_templates = defaultdict(list)
    
    with open('automacoes_db.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            software_a = row['software_a']
            software_b = row['software_b']
            tipo_evento = row['tipo_evento']
            tags = row.get('tags', '')
            
            categories = categorize_template(software_a, software_b, tags)
            
            if categories != ['Outros']:
                template = {
                    'slug': row['slug_url'],
                    'software_a': software_a,
                    'software_b': software_b,
                    'tipo_evento': tipo_evento,
                    'categories': categories,
                    'title_old': row['titulo_pagina'],
                    'title_new': optimize_title(software_a, software_b, tipo_evento),
                    'meta_old': row['descricao_curta'],
                    'meta_new': optimize_meta(software_a, software_b, tipo_evento, row['caso_uso_resumido']),
                    'url': f"https://www.automationscookbook.com/integracoes/{row['slug_url']}.html"
                }
                
                priority_templates.append(template)
                
                for cat in categories:
                    stats[cat] += 1
                    category_templates[cat].append(template)
                
                if len(priority_templates) >= 500:
                    break
    
    print(f"✅ Templates prioritários identificados: {len(priority_templates)}\n")
    print("📊 Distribuição por categoria:")
    for cat, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
        print(f"   • {cat}: {count} templates")
    
    # Salvar resultado
    with open('priority_templates_refined.json', 'w', encoding='utf-8') as f:
        json.dump(priority_templates, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Salvo em: priority_templates_refined.json")
    
    # Exemplos
    print("\n" + "=" * 80)
    print("📝 Exemplos de Otimizações")
    print("=" * 80)
    
    for cat in ['CRM', 'WhatsApp', 'E-commerce', 'Marketing']:
        if cat in category_templates and category_templates[cat]:
            example = category_templates[cat][0]
            print(f"\n🔷 Categoria: {cat}")
            print(f"{'─' * 80}")
            print(f"🔗 URL: {example['url']}")
            print(f"\n📌 Título Anterior:")
            print(f"   {example['title_old']}")
            print(f"\n✨ Título Otimizado:")
            print(f"   {example['title_new']}")
            print(f"\n📌 Meta Anterior:")
            print(f"   {example['meta_old']}")
            print(f"\n✨ Meta Otimizada:")
            print(f"   {example['meta_new']}")
    
    print("\n" + "=" * 80)
    print("✅ Processo concluído!")
    print("=" * 80)
    print("\n📋 Próximos passos:")
    print("1. Revisar: priority_templates_refined.json")
    print("2. Aplicar mudanças nos arquivos HTML")
    print("3. Commit e deploy")

if __name__ == '__main__':
    main()
