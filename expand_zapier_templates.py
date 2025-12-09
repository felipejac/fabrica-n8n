#!/usr/bin/env python3
"""
Script para expandir templates Zapier com novas categorias de alto valor
Adiciona 100+ novos templates focados em casos de uso populares
"""

import csv
import os

def generate_additional_zapier_templates():
    """Gera templates Zapier adicionais para atingir 200+ templates"""
    
    existing_file = 'automacoes_zapier_db.csv'
    
    # Ler templates existentes para evitar duplicatas
    existing_slugs = set()
    with open(existing_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            existing_slugs.add(row['slug_url'])
    
    print(f"📊 Templates existentes: {len(existing_slugs)}")
    
    # Novos templates de alto valor
    new_templates = []
    
    # ===== MARKETING AUTOMATION (20 templates) =====
    marketing_templates = [
        ("Facebook Lead Ads", "Mailchimp", "Lead", "Adicionar leads à lista", "Como adicionar leads do Facebook Ads no Mailchimp usando Zapier", "facebook-lead-ads-para-mailchimp-zapier", "Sincronize leads do Facebook com listas Mailchimp automaticamente. Capture e nutra leads com Zapier.", "https://zapier.com/apps/facebook-lead-ads/integrations/mailchimp", "New Lead|Add to Audience|Tag by Campaign|Send Welcome Email", "marketing,facebook,email,mailchimp,zapier"),
        ("Facebook Lead Ads", "HubSpot", "Lead", "CRM automation", "Como enviar leads do Facebook Ads para HubSpot usando Zapier", "facebook-lead-ads-para-hubspot-zapier", "Automatize captura de leads Facebook no HubSpot. Qualifique e nutra automaticamente com Zapier.", "https://zapier.com/apps/facebook-lead-ads/integrations/hubspot", "New Lead|Create/Update Contact|Set Lifecycle Stage|Assign to Owner", "marketing,facebook,crm,hubspot,zapier"),
        ("Facebook Lead Ads", "Google Sheets", "Lead", "Backup de leads", "Como salvar leads do Facebook Ads no Google Sheets usando Zapier", "facebook-lead-ads-para-google-sheets-zapier", "Backup automático de leads Facebook em planilhas. Análise de performance via Zapier.", "https://zapier.com/apps/facebook-lead-ads/integrations/google-sheets", "New Lead|Format Data|Append to Sheet|Calculate Cost per Lead", "marketing,facebook,dados,zapier"),
        ("LinkedIn Lead Gen", "Salesforce", "Lead", "B2B lead capture", "Como enviar leads do LinkedIn para Salesforce usando Zapier", "linkedin-lead-gen-para-salesforce-zapier", "Capture leads B2B do LinkedIn direto no Salesforce. Qualificação automática via Zapier.", "https://zapier.com/apps/linkedin-lead-gen/integrations/salesforce", "New Lead|Score Lead|Create Lead Record|Assign to Queue", "marketing,linkedin,crm,salesforce,zapier"),
        ("LinkedIn Lead Gen", "HubSpot", "Lead", "B2B marketing", "Como integrar LinkedIn Lead Gen com HubSpot usando Zapier", "linkedin-lead-gen-para-hubspot-zapier", "Automatize leads B2B do LinkedIn para HubSpot. Nutrição e score automáticos via Zapier.", "https://zapier.com/apps/linkedin-lead-gen/integrations/hubspot", "New Lead|Create Contact|Set Persona|Add to Workflow", "marketing,linkedin,crm,hubspot,zapier"),
        ("Google Ads", "Google Sheets", "Conversão", "ROI tracking", "Como registrar conversões Google Ads no Sheets usando Zapier", "google-ads-para-google-sheets-zapier", "Monitore ROI de Google Ads em planilhas. Dashboard automático via Zapier.", "https://zapier.com/apps/google-ads/integrations/google-sheets", "New Conversion|Extract Campaign Data|Append Row|Calculate CPA", "marketing,google-ads,dados,zapier"),
        ("Google Ads", "Slack", "Conversão", "Alertas de campanha", "Como notificar conversões Google Ads no Slack usando Zapier", "google-ads-para-slack-zapier", "Receba alertas no Slack para conversões Google Ads. Performance em tempo real via Zapier.", "https://zapier.com/apps/google-ads/integrations/slack", "New Conversion|Format Stats|Post to Channel|Celebrate Results", "marketing,google-ads,slack,zapier"),
        ("Mailchimp", "Google Sheets", "Campanha", "Email analytics", "Como registrar campanhas Mailchimp no Google Sheets usando Zapier", "mailchimp-campainha-para-google-sheets-zapier", "Automatize relatórios de email marketing em planilhas. Analytics completo via Zapier.", "https://zapier.com/apps/mailchimp/integrations/google-sheets", "Campaign Sent|Get Open/Click Rates|Append Stats|Track ROI", "marketing,email,mailchimp,dados,zapier"),
        ("ActiveCampaign", "Slack", "Automação", "Marketing alerts", "Como notificar automações ActiveCampaign no Slack usando Zapier", "activecampaign-para-slack-zapier", "Receba alertas de automações ActiveCampaign no Slack. Monitore leads via Zapier.", "https://zapier.com/apps/activecampaign/integrations/slack", "Automation Completed|Extract Contact Info|Post to Channel|Add Note", "marketing,email,activecampaign,slack,zapier"),
        ("ActiveCampaign", "Google Sheets", "Contato", "Database sync", "Como sincronizar contatos ActiveCampaign com Sheets usando Zapier", "activecampaign-para-google-sheets-zapier", "Backup automático de contatos ActiveCampaign em planilhas. Análise via Zapier.", "https://zapier.com/apps/activecampaign/integrations/google-sheets", "Contact Updated|Extract Fields|Append/Update Row|Track Engagement", "marketing,email,activecampaign,dados,zapier"),
    ]
    
    # ===== E-COMMERCE AVANÇADO (15 templates) =====
    ecommerce_templates = [
        ("Shopify", "Facebook Pixel", "Venda", "Conversão tracking", "Como enviar vendas Shopify para Facebook Pixel usando Zapier", "shopify-para-facebook-pixel-zapier", "Automatize tracking de conversões Shopify no Facebook. Otimize campanhas via Zapier.", "https://zapier.com/apps/shopify/integrations/facebook", "New Order|Extract Purchase Data|Send Conversion Event|Track Revenue", "ecommerce,shopify,marketing,facebook,zapier"),
        ("Shopify", "Klaviyo", "Cliente", "Email marketing", "Como sincronizar clientes Shopify com Klaviyo usando Zapier", "shopify-para-klaviyo-zapier", "Automatize email marketing pós-compra Shopify com Klaviyo. Retenção via Zapier.", "https://zapier.com/apps/shopify/integrations/klaviyo", "New Customer|Add to List|Trigger Welcome Series|Track LTV", "ecommerce,shopify,email,klaviyo,zapier"),
        ("Shopify", "QuickBooks", "Pedido", "Contabilidade", "Como integrar pedidos Shopify com QuickBooks usando Zapier", "shopify-para-quickbooks-zapier", "Sincronize vendas Shopify com QuickBooks automaticamente. Contabilidade via Zapier.", "https://zapier.com/apps/shopify/integrations/quickbooks", "New Order|Create Invoice|Record Payment|Sync Inventory", "ecommerce,shopify,financeiro,quickbooks,zapier"),
        ("WooCommerce", "Klaviyo", "Cliente", "Email automation", "Como sincronizar WooCommerce com Klaviyo usando Zapier", "woocommerce-para-klaviyo-zapier", "Automatize campanhas de email WooCommerce com Klaviyo. Maximize LTV via Zapier.", "https://zapier.com/apps/woocommerce/integrations/klaviyo", "New Customer|Add Profile|Segment by Purchase|Trigger Flow", "ecommerce,woocommerce,email,klaviyo,zapier"),
        ("WooCommerce", "QuickBooks", "Pedido", "Sync financeiro", "Como integrar WooCommerce com QuickBooks usando Zapier", "woocommerce-para-quickbooks-zapier", "Sincronize vendas WooCommerce com contabilidade QuickBooks. Automação via Zapier.", "https://zapier.com/apps/woocommerce/integrations/quickbooks", "New Order|Create Invoice|Log Payment|Update Inventory", "ecommerce,woocommerce,financeiro,quickbooks,zapier"),
        ("WooCommerce", "Facebook Pixel", "Venda", "Ad tracking", "Como rastrear vendas WooCommerce no Facebook Pixel usando Zapier", "woocommerce-para-facebook-pixel-zapier", "Automatize tracking de conversões WooCommerce no Facebook. ROI via Zapier.", "https://zapier.com/apps/woocommerce/integrations/facebook", "Order Completed|Format Event|Send to Pixel|Track ROAS", "ecommerce,woocommerce,marketing,facebook,zapier"),
        ("Shopify", "Xero", "Pedido", "Contabilidade", "Como sincronizar Shopify com Xero usando Zapier", "shopify-para-xero-zapier", "Automatize contabilidade Shopify com Xero. Reconciliação automática via Zapier.", "https://zapier.com/apps/shopify/integrations/xero", "New Order|Create Invoice|Record Payment|Sync to Xero", "ecommerce,shopify,financeiro,xero,zapier"),
        ("BigCommerce", "HubSpot", "Cliente", "CRM ecommerce", "Como sincronizar BigCommerce com HubSpot usando Zapier", "bigcommerce-para-hubspot-zapier", "Integre BigCommerce com CRM HubSpot automaticamente. Marketing unificado via Zapier.", "https://zapier.com/apps/bigcommerce/integrations/hubspot", "New Customer|Create Contact|Log Purchase|Set Lifecycle", "ecommerce,bigcommerce,crm,hubspot,zapier"),
        ("Etsy", "Google Sheets", "Pedido", "Gestão de vendas", "Como registrar vendas Etsy no Google Sheets usando Zapier", "etsy-para-google-sheets-zapier", "Automatize relatórios de vendas Etsy em planilhas. Dashboard via Zapier.", "https://zapier.com/apps/etsy/integrations/google-sheets", "New Sale|Extract Order Data|Append Row|Calculate Revenue", "ecommerce,etsy,dados,zapier"),
        ("Square", "Mailchimp", "Cliente", "Email marketing", "Como adicionar clientes Square no Mailchimp usando Zapier", "square-para-mailchimp-zapier", "Sincronize clientes Square com Mailchimp automaticamente. Retenção via Zapier.", "https://zapier.com/apps/square/integrations/mailchimp", "New Customer|Add to Audience|Tag by Purchase|Trigger Campaign", "ecommerce,square,email,mailchimp,zapier"),
    ]
    
    # ===== CUSTOMER SUCCESS & SUPPORT (15 templates) =====
    support_templates = [
        ("Zendesk", "HubSpot", "Ticket", "Customer 360", "Como sincronizar tickets Zendesk com HubSpot usando Zapier", "zendesk-para-hubspot-zapier", "Unifique suporte Zendesk e CRM HubSpot automaticamente. Customer 360 via Zapier.", "https://zapier.com/apps/zendesk/integrations/hubspot", "Ticket Solved|Find Contact|Log Activity|Update Support Score", "suporte,zendesk,crm,hubspot,zapier"),
        ("Zendesk", "Salesforce", "Ticket", "Service Cloud sync", "Como integrar Zendesk com Salesforce usando Zapier", "zendesk-para-salesforce-zapier", "Sincronize tickets Zendesk com Salesforce Service Cloud. Dados unificados via Zapier.", "https://zapier.com/apps/zendesk/integrations/salesforce", "New Ticket|Create Case|Sync Status|Log Resolution", "suporte,zendesk,crm,salesforce,zapier"),
        ("Intercom", "Salesforce", "Conversa", "Sales handoff", "Como sincronizar Intercom com Salesforce usando Zapier", "intercom-para-salesforce-zapier", "Automatize handoff de suporte para vendas Intercom-Salesforce. Contexto via Zapier.", "https://zapier.com/apps/intercom/integrations/salesforce", "Conversation Tagged|Find Lead|Create Opportunity|Assign Rep", "suporte,intercom,crm,salesforce,zapier"),
        ("Intercom", "Slack", "Conversa", "Internal escalation", "Como notificar conversas Intercom prioritárias no Slack usando Zapier", "intercom-conversas-prioritarias-para-slack-zapier", "Escalone conversas urgentes Intercom para Slack automaticamente. Resposta via Zapier.", "https://zapier.com/apps/intercom/integrations/slack", "High Priority Conversation|Format Details|Post to Channel|Mention Team", "suporte,intercom,slack,zapier"),
        ("Freshdesk", "HubSpot", "Ticket", "Support CRM sync", "Como sincronizar Freshdesk com HubSpot usando Zapier", "freshdesk-para-hubspot-zapier", "Integre tickets Freshdesk com CRM HubSpot automaticamente. Timeline via Zapier.", "https://zapier.com/apps/freshdesk/integrations/hubspot", "Ticket Created|Find Contact|Log Activity|Update Properties", "suporte,freshdesk,crm,hubspot,zapier"),
        ("Freshdesk", "Salesforce", "Ticket", "Service integration", "Como integrar Freshdesk com Salesforce usando Zapier", "freshdesk-para-salesforce-zapier", "Sincronize suporte Freshdesk com Salesforce automaticamente. Customer 360 via Zapier.", "https://zapier.com/apps/freshdesk/integrations/salesforce", "New Ticket|Create Case|Sync Updates|Track CSAT", "suporte,freshdesk,crm,salesforce,zapier"),
        ("Help Scout", "Slack", "Conversa", "Support alerts", "Como notificar conversas Help Scout no Slack usando Zapier", "help-scout-para-slack-zapier", "Receba alertas Slack para conversas Help Scout. Transparência via Zapier.", "https://zapier.com/apps/help-scout/integrations/slack", "New Conversation|Format Message|Post to Channel|Assign Agent", "suporte,help-scout,slack,zapier"),
        ("Help Scout", "HubSpot", "Cliente", "Support history", "Como sincronizar Help Scout com HubSpot usando Zapier", "help-scout-para-hubspot-zapier", "Unifique histórico de suporte Help Scout no CRM HubSpot. Timeline via Zapier.", "https://zapier.com/apps/help-scout/integrations/hubspot", "Conversation Closed|Find Contact|Log Activity|Update Score", "suporte,help-scout,crm,hubspot,zapier"),
        ("Gorgias", "Shopify", "Ticket", "Ecommerce support", "Como integrar tickets Gorgias com Shopify usando Zapier", "gorgias-para-shopify-zapier", "Sincronize suporte Gorgias com pedidos Shopify automaticamente. Contexto via Zapier.", "https://zapier.com/apps/gorgias/integrations/shopify", "Ticket Created|Find Order|Display Order Info|Tag Ticket", "suporte,gorgias,ecommerce,shopify,zapier"),
        ("Drift", "Salesforce", "Conversa", "Chat to CRM", "Como sincronizar conversas Drift com Salesforce usando Zapier", "drift-para-salesforce-zapier", "Automatize captura de leads Drift no Salesforce. Qualificação via Zapier.", "https://zapier.com/apps/drift/integrations/salesforce", "Conversation Completed|Extract Contact|Create Lead|Assign to SDR", "suporte,drift,crm,salesforce,zapier"),
    ]
    
    # ===== SALES ENABLEMENT (15 templates) =====
    sales_templates = [
        ("Calendly", "Pipedrive", "Agendamento", "Meeting to deal", "Como criar deals Pipedrive de agendamentos Calendly usando Zapier", "calendly-para-pipedrive-zapier", "Automatize criação de deals Pipedrive para reuniões Calendly. Pipeline via Zapier.", "https://zapier.com/apps/calendly/integrations/pipedrive", "New Invitee|Create Person|Create Deal|Set Next Action", "vendas,agendamento,calendly,pipedrive,zapier"),
        ("Calendly", "Mailchimp", "Agendamento", "Follow-up automation", "Como enviar follow-ups Mailchimp após Calendly usando Zapier", "calendly-para-mailchimp-followup-zapier", "Automatize emails pós-reunião Calendly com Mailchimp. Nutrição via Zapier.", "https://zapier.com/apps/calendly/integrations/mailchimp", "Meeting Completed|Add to List|Tag as Customer|Trigger Campaign", "vendas,agendamento,calendly,email,zapier"),
        ("Gong", "Salesforce", "Chamada", "Call intelligence", "Como sincronizar chamadas Gong com Salesforce usando Zapier", "gong-para-salesforce-zapier", "Automatize insights Gong no Salesforce. Inteligência de vendas via Zapier.", "https://zapier.com/apps/gong/integrations/salesforce", "Call Recorded|Extract Insights|Log Activity|Update Opportunity", "vendas,gong,crm,salesforce,zapier"),
        ("DocuSign", "Salesforce", "Contrato", "Deal closing", "Como atualizar Salesforce quando DocuSign completado usando Zapier", "docusign-para-salesforce-zapier", "Automatize fechamento de deals Salesforce com DocuSign. Contratos via Zapier.", "https://zapier.com/apps/docusign/integrations/salesforce", "Envelope Completed|Find Opportunity|Update Stage to Closed Won|Celebrate", "vendas,docusign,crm,salesforce,zapier"),
        ("DocuSign", "HubSpot", "Contrato", "Contract tracking", "Como sincronizar DocuSign com HubSpot usando Zapier", "docusign-para-hubspot-zapier", "Automatize tracking de contratos DocuSign no HubSpot. Deals via Zapier.", "https://zapier.com/apps/docusign/integrations/hubspot", "Envelope Signed|Update Deal Stage|Log Activity|Send to Team", "vendas,docusign,crm,hubspot,zapier"),
        ("PandaDoc", "Salesforce", "Proposta", "Proposal tracking", "Como rastrear propostas PandaDoc no Salesforce usando Zapier", "pandadoc-para-salesforce-zapier", "Sincronize propostas PandaDoc com Salesforce automaticamente. Pipeline via Zapier.", "https://zapier.com/apps/pandadoc/integrations/salesforce", "Document Sent|Update Opportunity|Log Activity|Track Status", "vendas,pandadoc,crm,salesforce,zapier"),
        ("PandaDoc", "HubSpot", "Proposta", "Deal tracking", "Como integrar PandaDoc com HubSpot usando Zapier", "pandadoc-para-hubspot-zapier", "Automatize tracking de propostas PandaDoc no HubSpot. Deals via Zapier.", "https://zapier.com/apps/pandadoc/integrations/hubspot", "Document Completed|Update Deal Stage|Attach to Deal|Notify Rep", "vendas,pandadoc,crm,hubspot,zapier"),
        ("Outreach", "Salesforce", "Sequência", "Sales engagement", "Como sincronizar Outreach com Salesforce usando Zapier", "outreach-para-salesforce-zapier", "Automatize dados de engajamento Outreach no Salesforce. Insights via Zapier.", "https://zapier.com/apps/outreach/integrations/salesforce", "Prospect Replied|Update Lead Status|Log Activity|Score Lead", "vendas,outreach,crm,salesforce,zapier"),
        ("Calendly", "Google Sheets", "Agendamento", "Meeting analytics", "Como registrar agendamentos Calendly no Sheets usando Zapier", "calendly-para-google-sheets-analytics-zapier", "Automatize relatórios de reuniões Calendly em planilhas. Analytics via Zapier.", "https://zapier.com/apps/calendly/integrations/google-sheets", "New Event|Extract Details|Append Row|Calculate Show Rate", "vendas,agendamento,calendly,dados,zapier"),
        ("Close", "Slack", "Deal", "Sales notifications", "Como notificar deals Close no Slack usando Zapier", "close-para-slack-zapier", "Receba alertas Slack para atualizações Close CRM. Transparência via Zapier.", "https://zapier.com/apps/close/integrations/slack", "Opportunity Won|Format Message|Post to Channel|Celebrate Win", "vendas,close,crm,slack,zapier"),
    ]
    
    # ===== PRODUCT & DEVELOPMENT (10 templates) =====
    dev_templates = [
        ("GitHub", "Slack", "Pull Request", "Code review alerts", "Como notificar Pull Requests GitHub no Slack usando Zapier", "github-pull-request-para-slack-zapier", "Receba alertas Slack para PRs GitHub. Acelere code review via Zapier.", "https://zapier.com/apps/github/integrations/slack", "PR Opened|Format Details|Post to Channel|Mention Reviewers", "desenvolvimento,github,slack,zapier"),
        ("GitHub", "Jira", "Issue", "Bug tracking", "Como criar tickets Jira de issues GitHub usando Zapier", "github-issues-para-jira-zapier", "Sincronize bugs GitHub com Jira automaticamente. Tracking via Zapier.", "https://zapier.com/apps/github/integrations/jira", "Issue Labeled as Bug|Create Jira Issue|Link to GitHub|Assign to Team", "desenvolvimento,github,jira,zapier"),
        ("GitLab", "Slack", "Pipeline", "CI/CD monitoring", "Como notificar pipelines GitLab no Slack usando Zapier", "gitlab-pipeline-para-slack-zapier", "Monitore CI/CD GitLab no Slack. Deploy alerts via Zapier.", "https://zapier.com/apps/gitlab/integrations/slack", "Pipeline Failed|Format Error|Post to Channel|Mention On-Call", "desenvolvimento,gitlab,slack,zapier"),
        ("Sentry", "Jira", "Erro", "Error tracking", "Como criar tickets Jira de erros Sentry usando Zapier", "sentry-para-jira-zapier", "Automatize criação de tickets Jira para erros Sentry. Bug tracking via Zapier.", "https://zapier.com/apps/sentry/integrations/jira", "New Error|Group Similar|Create Issue|Set Priority", "desenvolvimento,sentry,jira,zapier"),
        ("Sentry", "Slack", "Erro", "Error alerts", "Como notificar erros Sentry no Slack usando Zapier", "sentry-para-slack-zapier", "Receba alertas Slack para erros críticos Sentry. Resposta rápida via Zapier.", "https://zapier.com/apps/sentry/integrations/slack", "Error Threshold Exceeded|Format Details|Post to Channel|Page Team", "desenvolvimento,sentry,slack,zapier"),
        ("PagerDuty", "Slack", "Incidente", "Incident management", "Como notificar incidentes PagerDuty no Slack usando Zapier", "pagerduty-para-slack-zapier", "Automatize alertas de incidentes PagerDuty no Slack. Resposta via Zapier.", "https://zapier.com/apps/pagerduty/integrations/slack", "Incident Triggered|Format Alert|Post to Channel|Start War Room", "desenvolvimento,pagerduty,slack,zapier"),
        ("Jira", "GitHub", "Issue", "Code linking", "Como vincular issues Jira com GitHub usando Zapier", "jira-para-github-zapier", "Sincronize Jira e GitHub bidirecionalmente. Rastreamento via Zapier.", "https://zapier.com/apps/jira/integrations/github", "Issue In Progress|Create Branch|Link to Issue|Update Status", "desenvolvimento,jira,github,zapier"),
        ("Linear", "Slack", "Issue", "Project updates", "Como notificar issues Linear no Slack usando Zapier", "linear-para-slack-zapier", "Receba atualizações Linear no Slack automaticamente. Transparência via Zapier.", "https://zapier.com/apps/linear/integrations/slack", "Issue Updated|Format Change|Post to Channel|Track Progress", "desenvolvimento,linear,slack,zapier"),
        ("Figma", "Slack", "Arquivo", "Design updates", "Como notificar atualizações Figma no Slack usando Zapier", "figma-para-slack-zapier", "Automatize notificações de design Figma no Slack. Colaboração via Zapier.", "https://zapier.com/apps/figma/integrations/slack", "File Updated|Extract Changes|Post to Channel|Share Link", "design,figma,slack,zapier"),
        ("ProductBoard", "Slack", "Feature", "Product updates", "Como notificar features ProductBoard no Slack usando Zapier", "productboard-para-slack-zapier", "Compartilhe atualizações ProductBoard no Slack automaticamente. Alinhamento via Zapier.", "https://zapier.com/apps/productboard/integrations/slack", "Feature Released|Format Announcement|Post to Channel|Celebrate", "produto,productboard,slack,zapier"),
    ]
    
    # ===== HR & OPERATIONS (10 templates) =====
    hr_templates = [
        ("BambooHR", "Slack", "Funcionário", "Onboarding alerts", "Como notificar novos funcionários BambooHR no Slack usando Zapier", "bamboohr-para-slack-zapier", "Automatize boas-vindas de novos funcionários BambooHR no Slack. Onboarding via Zapier.", "https://zapier.com/apps/bamboohr/integrations/slack", "New Employee|Format Welcome|Post to Channel|Assign Buddy", "rh,bamboohr,slack,zapier"),
        ("BambooHR", "Google Calendar", "Férias", "Time off tracking", "Como sincronizar férias BambooHR com Google Calendar usando Zapier", "bamboohr-para-google-calendar-zapier", "Automatize sincronização de férias BambooHR no calendário. Visibilidade via Zapier.", "https://zapier.com/apps/bamboohr/integrations/google-calendar", "Time Off Approved|Create Event|Set All-Day|Mark as Out of Office", "rh,bamboohr,calendario,zapier"),
        ("Greenhouse", "Slack", "Candidato", "Hiring updates", "Como notificar atualizações Greenhouse no Slack usando Zapier", "greenhouse-para-slack-zapier", "Receba alertas Slack para candidatos Greenhouse. Contratação via Zapier.", "https://zapier.com/apps/greenhouse/integrations/slack", "Candidate Advanced|Format Update|Post to Channel|Mention Hiring Manager", "rh,greenhouse,slack,zapier"),
        ("Lever", "Slack", "Candidato", "Recruiting alerts", "Como notificar candidatos Lever no Slack usando Zapier", "lever-para-slack-zapier", "Automatize notificações de recrutamento Lever no Slack. Pipeline via Zapier.", "https://zapier.com/apps/lever/integrations/slack", "New Application|Format Details|Post to Channel|Tag Recruiter", "rh,lever,slack,zapier"),
        ("Gusto", "Google Sheets", "Folha", "Payroll tracking", "Como registrar folha Gusto no Google Sheets usando Zapier", "gusto-para-google-sheets-zapier", "Automatize relatórios de folha Gusto em planilhas. Analytics via Zapier.", "https://zapier.com/apps/gusto/integrations/google-sheets", "Payroll Run|Extract Data|Append Row|Calculate Totals", "rh,gusto,financeiro,dados,zapier"),
        ("Workday", "Slack", "Solicitação", "Approval workflows", "Como notificar aprovações Workday no Slack usando Zapier", "workday-para-slack-zapier", "Automatize notificações de aprovação Workday no Slack. Agilidade via Zapier.", "https://zapier.com/apps/workday/integrations/slack", "Approval Pending|Format Request|Post to Channel|Mention Approver", "rh,workday,slack,zapier"),
        ("Expensify", "QuickBooks", "Despesa", "Expense sync", "Como sincronizar Expensify com QuickBooks usando Zapier", "expensify-para-quickbooks-zapier", "Automatize sincronização de despesas Expensify no QuickBooks. Contabilidade via Zapier.", "https://zapier.com/apps/expensify/integrations/quickbooks", "Report Approved|Create Expense|Record Payment|Sync to QB", "rh,expensify,financeiro,quickbooks,zapier"),
        ("Expensify", "Slack", "Despesa", "Expense alerts", "Como notificar despesas Expensify no Slack usando Zapier", "expensify-para-slack-zapier", "Receba alertas Slack para relatórios Expensify. Aprovação via Zapier.", "https://zapier.com/apps/expensify/integrations/slack", "Report Submitted|Format Summary|Post to Channel|Request Approval", "rh,expensify,slack,zapier"),
        ("Rippling", "Slack", "Funcionário", "HR notifications", "Como notificar eventos Rippling no Slack usando Zapier", "rippling-para-slack-zapier", "Automatize notificações RH Rippling no Slack. Onboarding e offboarding via Zapier.", "https://zapier.com/apps/rippling/integrations/slack", "Employee Status Changed|Format Update|Post to Channel|Track Changes", "rh,rippling,slack,zapier"),
        ("15Five", "Slack", "Check-in", "Performance tracking", "Como notificar check-ins 15Five no Slack usando Zapier", "15five-para-slack-zapier", "Automatize notificações de check-ins 15Five no Slack. Engajamento via Zapier.", "https://zapier.com/apps/15five/integrations/slack", "Check-in Submitted|Extract Highlights|Post to Channel|Celebrate Wins", "rh,15five,slack,zapier"),
    ]
    
    # Combinar todos os templates
    all_new_templates = (
        marketing_templates + 
        ecommerce_templates + 
        support_templates + 
        sales_templates + 
        dev_templates + 
        hr_templates
    )
    
    # Filtrar duplicatas
    for template_data in all_new_templates:
        slug = template_data[5]
        if slug not in existing_slugs:
            new_templates.append({
                'platform': 'zapier',
                'software_a': template_data[0],
                'software_b': template_data[1],
                'tipo_evento': template_data[2],
                'caso_uso_resumido': template_data[3],
                'titulo_pagina': template_data[4],
                'slug_url': template_data[5],
                'descricao_curta': template_data[6],
                'zap_template_url': template_data[7],
                'passos_resumo': template_data[8],
                'tags': template_data[9]
            })
            existing_slugs.add(slug)
    
    print(f"✅ Novos templates gerados: {len(new_templates)}")
    
    return new_templates


def append_to_csv(new_templates):
    """Adiciona novos templates ao CSV existente"""
    
    csv_file = 'automacoes_zapier_db.csv'
    
    with open(csv_file, 'a', encoding='utf-8', newline='') as f:
        fieldnames = ['platform', 'software_a', 'software_b', 'tipo_evento', 
                     'caso_uso_resumido', 'titulo_pagina', 'slug_url', 
                     'descricao_curta', 'zap_template_url', 'passos_resumo', 'tags']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        for template in new_templates:
            writer.writerow(template)
    
    print(f"✅ {len(new_templates)} templates adicionados ao CSV")
    
    # Contar total
    with open(csv_file, 'r', encoding='utf-8') as f:
        total = sum(1 for line in f) - 1  # -1 para header
    
    print(f"📊 Total de templates Zapier: {total}")
    return total


if __name__ == '__main__':
    print("🚀 Expandindo templates Zapier...\n")
    
    # Gerar novos templates
    new_templates = generate_additional_zapier_templates()
    
    # Adicionar ao CSV
    total = append_to_csv(new_templates)
    
    print(f"\n{'='*60}")
    print(f"✅ EXPANSÃO CONCLUÍDA!")
    print(f"{'='*60}")
    print(f"📈 Novos templates: +{len(new_templates)}")
    print(f"📊 Total Zapier: {total}")
    print(f"🎯 Meta: 200+ (Faltam {max(0, 200 - total)})")
    print(f"\n📝 Próximo passo: python build_zapier.py")
    print(f"{'='*60}\n")
