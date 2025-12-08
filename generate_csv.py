#!/usr/bin/env python3
"""
📊 Gerador de CSV para Expansão de Integrações
Cria centenas de combinações de integrações para demonstrar escalabilidade
"""

import csv
import os
from itertools import combinations

# ==================== CONFIGURAÇÕES ====================

# Softwares disponíveis
SOFTWARE_LIST = [
    "Facebook Ads",
    "Google Sheets",
    "WhatsApp",
    "Slack",
    "Typeform",
    "RD Station",
    "Shopify",
    "Stripe",
    "Gmail",
    "Telegram",
    "Twitter",
    "Instagram",
    "LinkedIn",
    "TikTok",
    "Discord",
    "Notion",
    "Airtable",
    "Zapier",
    "Pipedrive",
    "HubSpot",
    "Trello",
    "Jira",
    "GitHub",
    "GitLab",
    "Twilio",
    "SendGrid",
    "Mailchimp",
    "WooCommerce",
    "Wix",
    "Webflow",
]

TIPO_EVENTO = ["Lead", "Formulário", "Venda", "Evento", "Notificação", "Backup", "Sincronização"]

TAGS_LIST = [
    "marketing",
    "vendas",
    "dados",
    "crm",
    "automação",
    "chat",
    "email",
    "notificação",
    "ia",
    "financeiro",
    "e-commerce",
    "blog",
    "redes sociais",
    "backup",
    "api",
]

CASOS_USO = [
    "Automação de leads",
    "Sincronização de dados",
    "Alertas em tempo real",
    "Backup automático",
    "Integração CRM",
    "Coleta de respostas",
    "Gestão de vendas",
    "Notificações personalizadas",
    "Processamento com IA",
    "Consolidação de dados",
]

# ==================== FUNÇÕES ====================

def slugify(text):
    """Converte texto para slug URL-safe"""
    return text.lower().replace(" ", "-").replace("(", "").replace(")", "").replace(".", "")

def generate_csv(num_combinations=100, output_file="automacoes_db_expanded.csv"):
    """Gera CSV com múltiplas combinações de integrações"""
    
    print(f"🔄 Gerando {num_combinations} combinações de integrações...")
    
    integrations = []
    
    # Gerar combinações únicas
    for i, (software_a, software_b) in enumerate(combinations(SOFTWARE_LIST, 2)):
        if i >= num_combinations:
            break
        
        tipo = TIPO_EVENTO[i % len(TIPO_EVENTO)]
        caso_uso = CASOS_USO[i % len(CASOS_USO)]
        tags = ",".join([TAGS_LIST[(i + j) % len(TAGS_LIST)] for j in range(2)])
        
        slug = f"{slugify(software_a)}-para-{slugify(software_b)}-n8n"
        titulo = f"Como integrar {software_a} com {software_b} usando N8N"
        descricao = f"Automação completa entre {software_a} e {software_b}. {caso_uso} sem limites."
        
        integrations.append({
            "software_a": software_a,
            "software_b": software_b,
            "tipo_evento": tipo,
            "caso_uso_resumido": caso_uso,
            "titulo_pagina": titulo,
            "slug_url": slug,
            "descricao_curta": descricao,
            "json_n8n_url": "https://n8n.io/workflows/1000",
            "passos_resumo": "Conectar origem|Mapear dados|Validar|Enviar para destino|Registrar log",
            "tags": tags,
        })
    
    # Salvar CSV
    if integrations:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                "software_a", "software_b", "tipo_evento", "caso_uso_resumido",
                "titulo_pagina", "slug_url", "descricao_curta", "json_n8n_url",
                "passos_resumo", "tags"
            ])
            writer.writeheader()
            writer.writerows(integrations)
        
        print(f"✅ CSV gerado: {output_file}")
        print(f"📊 Total de linhas: {len(integrations)}")
        return output_file
    else:
        print("❌ Nenhuma combinação gerada!")
        return None

def merge_csv_files(original="automacoes_db.csv", expanded="automacoes_db_expanded.csv", output="automacoes_db_merged.csv"):
    """Mescla CSV original com expandido, removendo duplicatas"""
    
    print(f"🔀 Mesclando {original} com {expanded}...")
    
    all_rows = []
    seen_slugs = set()
    
    # Ler original
    try:
        with open(original, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                slug = row.get('slug_url', '')
                if slug not in seen_slugs:
                    all_rows.append(row)
                    seen_slugs.add(slug)
    except FileNotFoundError:
        print(f"⚠️  {original} não encontrado, iniciando com expandido...")
    
    # Ler expandido
    try:
        with open(expanded, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                slug = row.get('slug_url', '')
                if slug not in seen_slugs:
                    all_rows.append(row)
                    seen_slugs.add(slug)
    except FileNotFoundError:
        print(f"❌ {expanded} não encontrado!")
        return None
    
    # Salvar mesclado
    if all_rows:
        with open(output, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=all_rows[0].keys())
            writer.writeheader()
            writer.writerows(all_rows)
        
        print(f"✅ CSV mesclado: {output}")
        print(f"📊 Total de integrações: {len(all_rows)}")
        print(f"   - Sem duplicatas: {len(all_rows)} linhas únicas")
        return output
    else:
        print("❌ Nenhuma linha para mesclar!")
        return None

# ==================== MAIN ====================

if __name__ == "__main__":
    import sys
    
    print("=" * 60)
    print("📊 Gerador de CSV para Expansão de Integrações")
    print("=" * 60)
    print()
    
    # Verificar argumentos
    if len(sys.argv) > 1:
        num_combinations = int(sys.argv[1])
    else:
        num_combinations = 100
    
    # Gerar CSV expandido
    expanded_file = generate_csv(num_combinations)
    
    if expanded_file:
        print()
        
        # Opção 1: Usar arquivo expandido diretamente
        print(f"📌 Opção 1: Usar {expanded_file} diretamente com build.py")
        print(f"   python build.py")
        print()
        
        # Opção 2: Mesclar com original
        print(f"📌 Opção 2: Mesclar com original e usar mesclado")
        merged_file = merge_csv_files(expanded=expanded_file)
        
        if merged_file:
            print()
            print("=" * 60)
            print(f"✨ Agora execute:")
            print(f"   cp {merged_file} automacoes_db.csv")
            print(f"   python build.py")
            print("=" * 60)
    
    print()
