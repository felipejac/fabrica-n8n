#!/usr/bin/env python3
"""
Script para gerar 3200+ templates únicos de automação N8N
Sem duplicatas, mantendo o formato CSV correto
"""

import csv
import os
from datetime import datetime
from itertools import combinations, permutations
from collections import OrderedDict

# Software populares para integrações
SOFTWARES = [
    # CRM & Sales
    "Salesforce", "HubSpot", "Pipedrive", "RD Station", "Active Campaign", "Keap", "Close.io",
    # Marketing
    "Mailchimp", "Klaviyo", "ConvertKit", "ActiveCampaign", "GetResponse", "Brevo", "SendGrid",
    # E-commerce
    "Shopify", "WooCommerce", "Magento", "BigCommerce", "Wix", "Squarespace", "OpenCart",
    # Communication
    "WhatsApp", "Telegram", "Slack", "Microsoft Teams", "Discord", "Twilio", "Zendesk Chat",
    # Productivity
    "Google Sheets", "Excel", "Airtable", "Notion", "Asana", "Monday.com", "ClickUp", "Trello",
    # Forms & Surveys
    "Typeform", "Google Forms", "JotForm", "Formstack", "SurveyMonkey", "Qualtrics",
    # Social Media
    "Facebook", "Instagram", "Twitter", "TikTok", "LinkedIn", "YouTube", "Pinterest",
    # Analytics
    "Google Analytics", "Mixpanel", "Amplitude", "Segment", "Hotjar",
    # Project Management
    "Jira", "GitHub", "GitLab", "Asana", "Monday", "Basecamp",
    # Payment
    "Stripe", "PayPal", "Square", "Razorpay", "2Checkout", "Pagseguro",
    # Storage & Cloud
    "Google Drive", "Dropbox", "OneDrive", "AWS S3", "Cloudinary",
    # Database
    "PostgreSQL", "MySQL", "MongoDB", "Firebase", "Supabase",
    # Calendar & Time
    "Google Calendar", "Calendly", "Zoom", "Teams", "Meet",
    # Documentation
    "Confluence", "Wiki", "Notion", "Evernote",
    # Support
    "Zendesk", "Freshdesk", "Intercom", "Help Scout",
    # Booking
    "Calendly", "Acuity Scheduling", "Setmore",
    # Accounting
    "QuickBooks", "Xero", "FreshBooks", "Wave",
    # HR
    "BambooHR", "Workday", "Gupy", "Cia de Talentos",
    # Email
    "Gmail", "Outlook", "Office 365",
    # AI & Automation
    "ChatGPT", "OpenAI", "Google Gemini", "Claude",
    # Webhooks & API
    "HTTP Request", "REST API", "Webhook",
    # Other Popular
    "Chatwoot", "Kommo", "Bling", "Mercado Livre", "Amazon", "eBay", "Aliexpress",
]

# Tipos de eventos/gatilhos
TIPOS_EVENTOS = [
    "Lead",
    "Venda",
    "Notificação",
    "Formulário",
    "Contato",
    "Pedido",
    "Pagamento",
    "Evento",
    "Chat",
    "Comentário",
    "Post",
    "Agendamento",
    "Email",
    "Webhook",
    "API Call",
    "Atualização",
    "Criação",
    "Exclusão",
    "Backup",
    "Sincronização",
    "Relatório",
    "Alerta",
    "Importação",
    "Exportação",
    "Transformação",
    "Filtro",
    "Validação",
]

# Casos de uso resumidos (diversos)
CASOS_USO = [
    "Captura e processamento automático de dados",
    "Sincronização em tempo real entre plataformas",
    "Notificação e alerta de eventos importantes",
    "Backup e armazenamento seguro de informações",
    "Geração de relatórios automatizados",
    "Fluxo de trabalho com aprovações",
    "Integração de pagamentos e financeiro",
    "Gerenciamento de relacionamento com clientes",
    "Marketing automation e segmentação",
    "Controle de inventário e estoque",
    "Atendimento ao cliente 24/7",
    "Análise de dados e inteligência",
    "Automação de email marketing",
    "Criação de leads qualificados",
    "Acompanhamento de vendas",
    "Organização de eventos e agendamentos",
    "Gerenciamento de projetos",
    "Controle de qualidade",
    "Centralização de dados empresariais",
    "Otimização de processos",
    "Redução de tarefas repetitivas",
    "Melhoria de experiência do cliente",
    "Integração com redes sociais",
    "Automação de conteúdo",
    "Gestão de tickets e suporte",
    "Verificação de dados duplicados",
    "Enriquecimento de contatos",
    "Priorização de leads",
    "Notificação para equipes",
    "Auditoria de ações",
    "Conformidade e segurança",
    "Escalabilidade de processos",
    "Redução de custos operacionais",
    "Aumento de produtividade",
    "Melhor rastreabilidade",
]

# Tags/categorias
TAGS = [
    "marketing", "vendas", "crm", "ecommerce", "dados", "formularios",
    "notificacao", "automacao", "integracao", "api", "webhook", "sync",
    "email", "whatsapp", "chat", "social", "analytics", "finance",
    "hr", "project-management", "customer-support", "booking", "accounting",
    "inventory", "payment", "security", "backup", "reporting", "export",
    "import", "validation", "filter", "transform", "schedule", "trigger",
    "b2b", "b2c", "saas", "enterprise", "startup", "sme", "cultura",
    "otimizacao", "performance", "growth", "retention", "acquisition",
]

def read_existing_csv(filename):
    """Lê o CSV existente para evitar duplicatas"""
    existing = set()
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Cria chave única: software_a + software_b + tipo_evento
                key = (row['software_a'].lower(), row['software_b'].lower(), row['tipo_evento'].lower())
                existing.add(key)
    return existing

def create_slug(software_a, software_b):
    """Cria URL slug a partir dos softwares"""
    s_a = software_a.lower().replace(" ", "-").replace("(", "").replace(")", "")
    s_b = software_b.lower().replace(" ", "-").replace("(", "").replace(")", "")
    return f"{s_a}-para-{s_b}-n8n"

def generate_unique_templates(target_count=3200):
    """Gera templates únicos sem duplicatas"""
    existing = read_existing_csv('/workspaces/fabrica-n8n/automacoes_db.csv')
    
    templates = []
    used_keys = set(existing)  # Começa com as existentes
    
    # Passo 1: Gera combinações de 2 softwares
    print("Gerando combinações de softwares...")
    total_softwares = len(SOFTWARES)
    combinations_count = 0
    
    for i, software_a in enumerate(SOFTWARES):
        for software_b in SOFTWARES[i+1:]:
            if software_a.lower() == software_b.lower():
                continue
                
            # Para cada combinação, cria multiplos templates com tipos diferentes
            for tipo_evento in TIPOS_EVENTOS:
                key = (software_a.lower(), software_b.lower(), tipo_evento.lower())
                
                if key not in used_keys:
                    # Pega caso de uso e tags aleatorios
                    import random
                    caso_uso = random.choice(CASOS_USO)
                    tags_sample = ",".join(random.sample(TAGS, min(3, len(TAGS))))
                    
                    # Cria título descritivo
                    titulo = f"Como integrar {software_a} com {software_b} para {tipo_evento.lower()} usando N8N"
                    slug = create_slug(software_a, software_b) + f"-{tipo_evento.lower()}"
                    
                    # Descrição
                    descricao = f"Automatize {tipo_evento.lower()} integrando {software_a} e {software_b} com N8N. {caso_uso}."
                    
                    # Passos (exemplo genérico)
                    passos = f"Conectar Trigger {software_a}|Validar dados|Formatar para {software_b}|Enviar/Criar no {software_b}|Registrar resultado"
                    
                    # URL JSON (simulada)
                    json_url = f"https://n8n.io/workflows/{2000 + len(templates)}"
                    
                    template = {
                        'software_a': software_a,
                        'software_b': software_b,
                        'tipo_evento': tipo_evento,
                        'caso_uso_resumido': caso_uso,
                        'titulo_pagina': titulo,
                        'slug_url': slug,
                        'descricao_curta': descricao,
                        'json_n8n_url': json_url,
                        'passos_resumo': passos,
                        'tags': tags_sample,
                    }
                    
                    templates.append(template)
                    used_keys.add(key)
                    combinations_count += 1
                    
                    if len(templates) >= target_count:
                        print(f"✅ Atingido alvo de {target_count} templates")
                        return templates
    
    print(f"✅ Gerados {len(templates)} templates únicos")
    return templates

def merge_with_existing(new_templates):
    """Mescla novos templates com os existentes"""
    existing = []
    
    # Lê existentes
    with open('/workspaces/fabrica-n8n/automacoes_db.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        existing = list(reader)
    
    print(f"Existentes: {len(existing)}")
    print(f"Novos: {len(new_templates)}")
    
    # Mescla
    all_templates = existing + new_templates
    
    print(f"Total: {len(all_templates)}")
    return all_templates

def save_csv(templates, filename):
    """Salva templates em CSV"""
    if not templates:
        print(f"⚠️  Nenhum template para salvar em {filename}")
        return
    
    fieldnames = list(templates[0].keys())
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(templates)
    
    print(f"✅ Salvos {len(templates)} templates em {filename}")

def main():
    print("=" * 70)
    print("🚀 GERADOR DE 3200+ TEMPLATES N8N")
    print("=" * 70)
    print()
    
    # Gera novos templates
    print("📝 Gerando novos templates...")
    new_templates = generate_unique_templates(3200)
    
    # Mescla com existentes
    print("\n📊 Mesclando com existentes...")
    all_templates = merge_with_existing(new_templates)
    
    # Remove duplicatas (por segurança)
    print("\n🔍 Removendo duplicatas...")
    unique_templates = []
    seen_keys = set()
    
    for template in all_templates:
        key = (template['software_a'].lower(), template['software_b'].lower(), template['tipo_evento'].lower())
        if key not in seen_keys:
            unique_templates.append(template)
            seen_keys.add(key)
    
    print(f"✅ {len(unique_templates)} templates únicos")
    
    # Salva arquivos
    print("\n💾 Salvando arquivos...")
    save_csv(unique_templates, '/workspaces/fabrica-n8n/automacoes_db.csv')
    save_csv(unique_templates, '/workspaces/fabrica-n8n/automacoes_db_merged.csv')
    
    print("\n" + "=" * 70)
    print(f"✅ CONCLUÍDO!")
    print(f"   • Total de templates: {len(unique_templates)}")
    print(f"   • Softwares únicos: {len(set(t['software_a'] for t in unique_templates))}")
    print(f"   • Tipos de eventos: {len(set(t['tipo_evento'] for t in unique_templates))}")
    print("=" * 70)

if __name__ == '__main__':
    main()
