#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generator de 10.000+ Templates N8N
Expande automacoes_db.csv para 10.000 linhas mantendo qualidade e sem duplicatas
"""

import csv
import os
from datetime import datetime
from urllib.parse import quote

# 80+ softwares de integração
SOFTWARES = [
    "Salesforce", "HubSpot", "Pipedrive", "RD Station", "Active Campaign", "Keap", "Close.io",
    "Mailchimp", "Klaviyo", "ConvertKit", "GetResponse", "Brevo", "SendGrid", "Constant Contact",
    "Shopify", "WooCommerce", "Magento", "BigCommerce", "Wix", "Squarespace", "OpenCart",
    "WhatsApp", "Telegram", "Slack", "Teams", "Discord", "Twilio", "Zendesk", "Intercom",
    "Google Sheets", "Excel", "Airtable", "Notion", "Asana", "Monday.com", "ClickUp", "Trello",
    "Stripe", "PayPal", "Square", "Razorpay", "2Checkout", "PagSeguro", "Hotmart",
    "Gmail", "Outlook", "Yahoo Mail", "Google Drive", "OneDrive", "Dropbox", "AWS S3",
    "GitHub", "GitLab", "BitBucket", "Jira", "Confluence", "Azure DevOps",
    "Google Analytics", "Mixpanel", "Amplitude", "Segment", "Hotjar", "Clarity",
    "Zapier", "IFTTT", "Make.com", "n8n", "Workflow", "Automation.io",
    "Instagram", "Facebook", "TikTok", "Twitter", "LinkedIn", "Pinterest", "YouTube",
    "Google Calendar", "Outlook Calendar", "Calendly", "Zoom", "Meet", "Teams Call",
    "Canva", "Figma", "Adobe XD", "Sketch", "Framer"
]

# 50+ tipos de eventos/triggers
TIPOS_EVENTOS = [
    "lead", "venda", "notificação", "formulário", "contato", "pedido", "pagamento",
    "reembolso", "cancelamento", "atualização", "criação", "remoção", "deleção",
    "webhook", "agendado", "comentário", "resposta", "revisão", "aprovação", "rejeição",
    "filtro", "validação", "transformação", "sincronização", "backup", "recuperação",
    "importação", "exportação", "integração", "migração", "consolidação", "relatório",
    "alerta", "ativação", "desativação", "atividade", "interação", "evento", "transação",
    "confirmação", "verificação", "autenticação", "autorização", "permissão", "acesso",
    "envio", "recebimento", "processamento", "conclusão", "progresso", "ciclo"
]

# 50+ casos de uso
CASOS_USO = [
    "lead qualification", "venda automática", "notificação em tempo real", 
    "formulário automático", "contato sincronizado", "pedido rastreado", "pagamento processado",
    "reembolso automático", "cancelamento notificado", "atualização em cascata",
    "criação de registro", "remoção de duplicatas", "backup automático",
    "webhook confiável", "agendamento inteligente", "comentário moderado",
    "resposta automática", "revisão aprovada", "aprovação multi-nível", "rejeição notificada",
    "filtro inteligente", "validação de dados", "transformação de formato",
    "sincronização bidirecional", "backup seguro", "recuperação de dados",
    "importação em massa", "exportação agendada", "integração profunda", "migração segura",
    "consolidação de dados", "relatório personalizado", "alerta crítico",
    "ativação de campanha", "desativação automática", "rastreamento de atividade",
    "análise de interação", "captura de evento", "processamento de transação",
    "confirmação de entrega", "verificação de identidade", "autenticação OAuth2",
    "autorização granular", "gerencimento de permissões", "controle de acesso",
    "envio em batch", "recebimento com retry", "processamento assíncrono",
    "conclusão de workflow", "monitoramento de progresso", "ciclo de vida"
]

# 60+ tags
TAGS = [
    "automação", "integração", "sincronização", "workflow", "crm", "marketing", "vendas",
    "ecommerce", "comunicação", "produtividade", "pagamento", "email", "redes-sociais",
    "armazenamento", "desenvolvimento", "analytics", "backup", "recuperação",
    "notificação", "relatório", "validação", "transformação", "importação", "exportação",
    "webhook", "api", "oauth2", "autenticação", "permissões", "acesso",
    "performance", "segurança", "escalabilidade", "confiabilidade", "disponibilidade",
    "monitoramento", "logging", "rastreamento", "auditoria", "conformidade",
    "crm-automation", "sales-enablement", "marketing-automation", "lead-generation",
    "customer-retention", "revenue-growth", "cost-reduction", "time-savings",
    "data-quality", "data-governance", "data-security", "gdpr-compliance",
    "realtime", "batch-processing", "streaming", "event-driven", "scheduled",
    "trigger-based", "rule-based", "ai-powered", "ml-enabled", "intelligent"
]

print("\n" + "="*80)
print("🚀 GERADOR DE 10.000+ TEMPLATES N8N")
print("="*80 + "\n")

# Ler CSV existente
existing_entries = set()
existing_list = []

if os.path.exists("automacoes_db.csv"):
    print("📖 Lendo CSV existente...")
    with open("automacoes_db.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row["software_a"], row["software_b"], row["tipo_evento"])
            existing_entries.add(key)
            existing_list.append(row)
    print(f"   ✓ {len(existing_list)} templates existentes carregados")
else:
    print("⚠️  CSV não encontrado, iniciando do zero")

# Gerar combinações inteligentes
print("\n📝 Gerando 10.000+ templates únicos...")
new_entries = []
target = 10000
progress_step = 500

# Estratégia: Combinar softwares × eventos × casos de uso
for i, software_a in enumerate(SOFTWARES):
    for software_b in SOFTWARES:
        if software_a == software_b:
            continue
        
        for evento in TIPOS_EVENTOS:
            # Usar diferentes casos de uso e tags
            caso_idx = (len(new_entries) % len(CASOS_USO))
            tags_idx = (len(new_entries) % (len(TAGS) - 4))
            
            caso_uso = CASOS_USO[caso_idx]
            tags = ", ".join(TAGS[tags_idx:tags_idx+4])
            
            # Evitar duplicatas
            key = (software_a, software_b, evento)
            if key in existing_entries:
                continue
            
            # Gerar slug
            slug_base = f"{software_a.lower()}-para-{software_b.lower()}-n8n-{evento}"
            slug = quote(slug_base.replace(" ", "-"), safe="-").lower()
            
            # Título
            titulo = f"{software_a} para {software_b} | Automação de {evento.title()} com n8n"
            
            # Descrição
            descricao = f"Integre {software_a} com {software_b} para automatizar {caso_uso} de forma inteligente e confiável"
            
            # URL JSON simulada
            json_url = f"https://n8n.io/workflows/{slug}"
            
            # Passos
            passos = f"1. Conectar {software_a}\n2. Configurar gatilho de {evento}\n3. Mapear dados\n4. Sincronizar com {software_b}\n5. Testar workflow"
            
            entry = {
                "software_a": software_a,
                "software_b": software_b,
                "tipo_evento": evento,
                "caso_uso_resumido": caso_uso,
                "titulo_pagina": titulo,
                "slug_url": slug,
                "descricao_curta": descricao,
                "json_n8n_url": json_url,
                "passos_resumo": passos,
                "tags": tags
            }
            
            new_entries.append(entry)
            existing_entries.add(key)
            
            if len(new_entries) % progress_step == 0:
                print(f"   → {len(new_entries)} templates gerados...")
            
            if len(new_entries) >= target:
                break
        
        if len(new_entries) >= target:
            break
    
    if len(new_entries) >= target:
        break

print(f"\n✅ Gerados {len(new_entries)} novos templates únicos\n")

# Mesclar e salvar
print("📊 Mesclando com existentes...")
all_entries = existing_list + new_entries
print(f"   Total: {len(existing_list)} existentes + {len(new_entries)} novos = {len(all_entries)}")

# Salvar CSVs
fieldnames = [
    "software_a", "software_b", "tipo_evento", "caso_uso_resumido",
    "titulo_pagina", "slug_url", "descricao_curta", "json_n8n_url",
    "passos_resumo", "tags"
]

print("\n💾 Salvando arquivos CSV...")

for filename in ["automacoes_db.csv", "automacoes_db_merged.csv"]:
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_entries)
    
    size_mb = os.path.getsize(filename) / (1024 * 1024)
    print(f"   ✅ {filename:30} → {len(all_entries):5} linhas ({size_mb:.1f} MB)")

print("\n" + "="*80)
print("✅ ESCALADO PARA 10.000+ TEMPLATES!")
print("="*80)
print(f"""
📊 Estatísticas Finais:
   • Total de templates: {len(all_entries)}
   • Softwares únicos: {len(SOFTWARES)}
   • Tipos de eventos: {len(TIPOS_EVENTOS)}
   • Casos de uso: {len(CASOS_USO)}
   • Tags disponíveis: {len(TAGS)}
   • Arquivo size: {size_mb:.1f} MB cada

🎯 Próximo passo:
   python build.py  # Regenerar ~10.000 páginas HTML
""")
print("="*80 + "\n")
