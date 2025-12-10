#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador de Páginas de Casos de Uso - Automations Cookbook
Gera 20 páginas HTML otimizadas para SEO baseadas no template
"""

import os
import re
from pathlib import Path

# Dados dos 20 casos de uso
CASOS_DE_USO = [
    {
        "categoria": "📥 Geração e Nutrição de Leads",
        "nome": "Leads do Facebook Ads para CRM",
        "descricao": "Integra os leads do Facebook Ads com HubSpot/RD Station e notifica o time no Slack em tempo real.",
        "icon": "📥",
        "tools": ["Facebook Ads", "HubSpot", "RD Station", "Slack"],
        "complexity": "Fácil",
        "setup_time": "30-45 minutos",
        "roi": "300% em 3 meses",
        "workflow": "Facebook Lead Ad → Webhook N8N → HubSpot/RD Station (criar contato) → Slack (notificação)",
        "benefits": [
            {"title": "Resposta Imediata", "desc": "Leads entram no CRM em menos de 2 minutos após o cadastro"},
            {"title": "Zero Leads Perdidos", "desc": "100% dos leads são capturados automaticamente"},
            {"title": "Time Notificado", "desc": "Vendedores recebem alerta instantâneo no Slack"}
        ],
        "expert_tip": "Configure um campo de 'Origem' no CRM para rastrear quais campanhas geram mais conversões. Isso permite otimizar o investimento em ads.",
        "success_story": "Uma empresa de educação online implementou este workflow e reduziu o tempo de resposta ao lead de 4 horas para 2 minutos, aumentando a taxa de conversão em 45%.",
        "search_query": "facebook+leads+crm"
    },
    {
        "categoria": "📥 Geração e Nutrição de Leads",
        "nome": "Campanha de Email Drip Automática",
        "descricao": "Cria sequência de e-mails automáticos para nutrir leads e acompanhar aberturas e cliques.",
        "icon": "📧",
        "tools": ["Gmail", "SendGrid", "Google Sheets", "Mailchimp"],
        "complexity": "Médio",
        "setup_time": "1-2 horas",
        "roi": "250% em 6 meses",
        "workflow": "Novo contato → Aguardar 1 dia → Email 1 → Aguardar 3 dias → Email 2 → Aguardar 7 dias → Email 3",
        "benefits": [
            {"title": "Nutrição Automática", "desc": "Leads recebem conteúdo relevante no timing perfeito"},
            {"title": "Personalização em Escala", "desc": "Segmente por interesse, comportamento ou estágio do funil"},
            {"title": "Métricas Precisas", "desc": "Tracking completo de abertura, clique e conversão"}
        ],
        "expert_tip": "Use variáveis dinâmicas como {{nome}} e {{empresa}} para aumentar a taxa de abertura em até 26%. Teste diferentes horários de envio para cada segmento.",
        "success_story": "Uma SaaS B2B automatizou sua sequência de onboarding e viu a ativação de usuários aumentar de 35% para 68% em 2 meses.",
        "search_query": "email+drip+automation"
    },
    {
        "categoria": "📥 Geração e Nutrição de Leads",
        "nome": "Dashboard de Performance Diário",
        "descricao": "Consolida dados de Google Analytics e Facebook Ads em Sheets e envia relatórios por e-mail diariamente.",
        "icon": "📈",
        "tools": ["Google Analytics", "Facebook Ads", "Google Sheets", "Gmail"],
        "complexity": "Médio",
        "setup_time": "2-3 horas",
        "roi": "150% em economia de tempo",
        "workflow": "Todo dia 9h → Google Analytics (métricas) → Facebook Ads (campanhas) → Google Sheets (consolidar) → Gmail (enviar relatório)",
        "benefits": [
            {"title": "Dados Centralizados", "desc": "Todas as métricas em um único dashboard atualizado automaticamente"},
            {"title": "Decisões Rápidas", "desc": "Time recebe dados frescos todo dia no mesmo horário"},
            {"title": "Zero Trabalho Manual", "desc": "Economize 5-10 horas por semana em coleta de dados"}
        ],
        "expert_tip": "Adicione alertas condicionais: se o CPA aumentar mais de 20%, envie um email urgente para o time. Isso permite reação rápida a problemas.",
        "success_story": "Uma agência de marketing reduziu de 8 horas para 0 o tempo gasto semanalmente em relatórios, permitindo que analistas focassem em otimização.",
        "search_query": "dashboard+analytics+automation"
    },
    {
        "categoria": "📥 Geração e Nutrição de Leads",
        "nome": "Análise de Sentimento com IA",
        "descricao": "Analisa menções nas redes sociais com ChatGPT e envia alertas no Slack para menções negativas.",
        "icon": "🤖",
        "tools": ["Twitter", "Instagram", "OpenAI", "Slack"],
        "complexity": "Avançado",
        "setup_time": "3-4 horas",
        "roi": "400% em gestão de crise",
        "workflow": "Menção na rede social → Capturar texto → ChatGPT (analisar sentimento) → Se negativo → Slack (alerta urgente)",
        "benefits": [
            {"title": "Detecção Instantânea", "desc": "Identifique crises de reputação em tempo real"},
            {"title": "Priorização Inteligente", "desc": "IA classifica menções por urgência e sentimento"},
            {"title": "Resposta Rápida", "desc": "Time de CS notificado em segundos para agir"}
        ],
        "expert_tip": "Configure diferentes níveis de alerta: amarelo para neutro, laranja para levemente negativo, vermelho para muito negativo. Escale apenas os críticos.",
        "success_story": "Uma marca de cosméticos detectou uma crise viral 45 minutos antes de viralizar, conseguindo reverter a narrativa e evitar danos à marca.",
        "search_query": "sentiment+analysis+ai"
    },
    {
        "categoria": "💰 Vendas & CRM",
        "nome": "Follow-up Automático de Leads Frios",
        "descricao": "Envia e-mails automáticos para reengajar leads inativos e atualiza o status no CRM conforme resposta.",
        "icon": "🔔",
        "tools": ["Salesforce", "Pipedrive", "Gmail", "HubSpot"],
        "complexity": "Fácil",
        "setup_time": "45 minutos",
        "roi": "350% em recuperação",
        "workflow": "Lead sem interação 7 dias → Email de reengajamento → Se responder → Mover para 'Quente' | Senão → Aguardar 14 dias → Email 2",
        "benefits": [
            {"title": "Reativar Leads Esquecidos", "desc": "30% dos leads frios voltam a engajar"},
            {"title": "Aumento de Conversão", "desc": "Até 25% mais vendas sem custo adicional de aquisição"},
            {"title": "Automático e Escalável", "desc": "Funciona 24/7 sem intervenção humana"}
        ],
        "expert_tip": "Use o 'Zeigarnik Effect': mencione algo que o lead começou mas não terminou (ex: 'Você iniciou o cadastro mas não finalizou'). Aumenta taxa de resposta em 35%.",
        "success_story": "Uma empresa de software B2B recuperou 23% de leads frios em 3 meses, gerando R$ 180k em receita adicional sem investir em novos leads.",
        "search_query": "follow+up+automation+crm"
    },
    {
        "categoria": "💰 Vendas & CRM",
        "nome": "Distribuição Inteligente de Leads",
        "descricao": "Distribui automaticamente novos leads para vendedores adequados com base em região e segmento.",
        "icon": "📞",
        "tools": ["HubSpot", "Salesforce", "Slack", "Google Sheets"],
        "complexity": "Médio",
        "setup_time": "1-2 horas",
        "roi": "200% em eficiência",
        "workflow": "Novo lead → Analisar região + segmento → Regras de atribuição → Atribuir ao vendedor certo → Slack (notificar)",
        "benefits": [
            {"title": "Round-Robin Balanceado", "desc": "Distribuição justa baseada em carga de trabalho atual"},
            {"title": "Especialização", "desc": "Leads de tecnologia vão para vendedores tech, por exemplo"},
            {"title": "50% Mais Rápido", "desc": "Redução drástica no tempo entre lead e primeiro contato"}
        ],
        "expert_tip": "Implemente 'lead scoring' antes da distribuição: leads com score > 80 vão para vendedores seniores. Isso maximiza taxa de conversão dos melhores leads.",
        "success_story": "Uma empresa de telecom aumentou conversão em 38% ao rotear leads premium para vendedores especializados, enquanto SDRs focavam em volume.",
        "search_query": "lead+distribution+automation"
    },
    {
        "categoria": "💰 Vendas & CRM",
        "nome": "Relatório Semanal de Pipeline",
        "descricao": "Extrai métricas do CRM e envia relatório semanal de performance para a gerência.",
        "icon": "📊",
        "tools": ["Pipedrive", "Salesforce", "Google Sheets", "Looker"],
        "complexity": "Fácil",
        "setup_time": "1 hora",
        "roi": "180% em visibilidade",
        "workflow": "Segunda-feira 8h → Extrair dados do CRM → Calcular métricas (conversão, ticket médio, ciclo) → Email para gerência",
        "benefits": [
            {"title": "Visibilidade Total", "desc": "Gerência vê gargalos e oportunidades toda semana"},
            {"title": "Decisões Data-Driven", "desc": "Métricas objetivas para coaching e estratégia"},
            {"title": "Previsão Precisa", "desc": "Forecast de vendas atualizado automaticamente"}
        ],
        "expert_tip": "Inclua 'health score' de cada negócio: verde (saudável), amarelo (em risco), vermelho (perdido provável). Permite ação preventiva antes de perder deals.",
        "success_story": "Uma empresa SaaS identificou que deals > 45 dias no funil tinham 80% de chance de perder. Implementaram ações preventivas e aumentaram fechamento em 22%.",
        "search_query": "sales+pipeline+report"
    },
    {
        "categoria": "🛒 E-commerce & Retail",
        "nome": "Fluxo Completo de Pedido Novo",
        "descricao": "Automatiza o processo de pedido: criação no ERP, emissão de NF, atualização de estoque e notificação ao cliente.",
        "icon": "📦",
        "tools": ["Shopify", "WooCommerce", "Bling", "Gmail"],
        "complexity": "Médio",
        "setup_time": "2-3 horas",
        "roi": "500% em eficiência",
        "workflow": "Pedido Shopify → ERP (criar pedido) → Emitir NF-e → Atualizar estoque → Email cliente (confirmação + tracking)",
        "benefits": [
            {"title": "Processamento em 2 Minutos", "desc": "Do checkout à NF emitida automaticamente"},
            {"title": "Zero Erro Manual", "desc": "Elimina digitação incorreta de dados"},
            {"title": "Cliente Informado", "desc": "Recebe confirmação e código de rastreio instantaneamente"}
        ],
        "expert_tip": "Configure webhooks bidirecionais: quando o status muda no ERP (ex: 'enviado'), atualize automaticamente a loja e envie email ao cliente. Reduz tickets de suporte em 60%.",
        "success_story": "Um e-commerce de moda processava 50 pedidos/dia manualmente (4h de trabalho). Com automação, passou a processar 500 pedidos/dia com zero intervenção.",
        "search_query": "ecommerce+order+automation"
    },
    {
        "categoria": "🛒 E-commerce & Retail",
        "nome": "Alerta de Estoque Baixo",
        "descricao": "Monitora nível de estoque e envia alerta via Slack ou SMS quando o número de unidades cai abaixo do limite.",
        "icon": "⚠️",
        "tools": ["WooCommerce", "Shopify", "Slack", "SMS API"],
        "complexity": "Fácil",
        "setup_time": "30 minutos",
        "roi": "250% em prevenção",
        "workflow": "A cada hora → Verificar estoque → Se < 10 unidades → Notificar equipe de compras → Criar tarefa no Trello",
        "benefits": [
            {"title": "Evitar Ruptura", "desc": "Nunca perca vendas por falta de estoque"},
            {"title": "Reposição Proativa", "desc": "Compras iniciadas antes do estoque zerar"},
            {"title": "Otimização de Capital", "desc": "Compre apenas quando necessário"}
        ],
        "expert_tip": "Configure limites diferentes por categoria: produtos de alta rotação com alerta em 20 unidades, baixa rotação em 5. Isso evita capital parado.",
        "success_story": "Uma loja de eletrônicos reduziu rupturas de estoque de 15% para 2%, aumentando receita em R$ 85k/mês ao não perder vendas.",
        "search_query": "inventory+alert+automation"
    },
    {
        "categoria": "🛒 E-commerce & Retail",
        "nome": "Pedido de Review Automático",
        "descricao": "Dispara automaticamente um e-mail pedindo avaliação alguns dias após a entrega do pedido.",
        "icon": "⭐",
        "tools": ["Shopify", "Trustpilot", "Gmail", "Google Reviews"],
        "complexity": "Fácil",
        "setup_time": "45 minutos",
        "roi": "400% em social proof",
        "workflow": "Pedido entregue → Aguardar 3 dias → Email pedindo review → Se responder → Salvar no banco → Publicar",
        "benefits": [
            {"title": "5x Mais Reviews", "desc": "De 2% para 10% de clientes deixando avaliação"},
            {"title": "Timing Perfeito", "desc": "Pedir review quando cliente já usou o produto"},
            {"title": "Social Proof Automático", "desc": "Reviews aumentam conversão em 15-30%"}
        ],
        "expert_tip": "Ofereça um pequeno incentivo (ex: cupom de 5% na próxima compra) apenas para quem deixar review. Isso dobra a taxa de resposta sem comprometer autenticidade.",
        "success_story": "Uma loja de cosméticos passou de 50 reviews para 1.200 em 6 meses, aumentando taxa de conversão de 2.1% para 3.2% (52% de aumento).",
        "search_query": "review+request+automation"
    },
    {
        "categoria": "🛒 E-commerce & Retail",
        "nome": "Recuperação de Carrinho Abandonado",
        "descricao": "Envia e-mails com lembretes e cupons para clientes que deixaram o carrinho sem finalizar a compra.",
        "icon": "🔄",
        "tools": ["Shopify", "Klaviyo", "Stripe", "Gmail"],
        "complexity": "Médio",
        "setup_time": "1-2 horas",
        "roi": "600% em recuperação",
        "workflow": "Carrinho abandonado → Aguardar 1h → Email 1 (lembrete) → Aguardar 24h → Email 2 (cupom 10%) → Aguardar 48h → Email 3 (urgência)",
        "benefits": [
            {"title": "Recuperar 15% dos Carrinhos", "desc": "Em média, 69% dos carrinhos são abandonados"},
            {"title": "Aumento Direto em Receita", "desc": "Cada 1% recuperado = milhares em receita"},
            {"title": "Segmentação por Valor", "desc": "Ofertas maiores para carrinhos de alto valor"}
        ],
        "expert_tip": "No primeiro email, não ofereça desconto ainda. Use apenas lembrete com senso de urgência ('Seu carrinho expira em 24h'). Reserve desconto para o segundo email.",
        "success_story": "Um e-commerce de moda recuperou R$ 340k em 3 meses de carrinhos abandonados, com investimento zero além da automação.",
        "search_query": "abandoned+cart+recovery"
    },
    {
        "categoria": "💬 Atendimento & Suporte",
        "nome": "Email → Ticket Automático",
        "descricao": "Converte e-mails recebidos em tickets no Zendesk e os atribui ao time responsável.",
        "icon": "🎫",
        "tools": ["Gmail", "Zendesk", "Freshdesk", "Slack"],
        "complexity": "Fácil",
        "setup_time": "30 minutos",
        "roi": "300% em organização",
        "workflow": "Email recebido → Extrair assunto + corpo → Criar ticket Zendesk → Categorizar (técnico/comercial/financeiro) → Atribuir time",
        "benefits": [
            {"title": "Zero Email Perdido", "desc": "100% das mensagens viram tickets rastreáveis"},
            {"title": "Categorização Automática", "desc": "IA identifica tipo de demanda e roteia corretamente"},
            {"title": "SLA desde o Início", "desc": "Contagem de tempo começa automaticamente"}
        ],
        "expert_tip": "Use palavras-chave no assunto para priorização: emails com 'URGENTE' ou 'BUG' vão para fila prioritária automaticamente.",
        "success_story": "Uma empresa de SaaS reduziu tempo médio de primeira resposta de 6 horas para 45 minutos ao eliminar triagem manual.",
        "search_query": "email+ticket+automation"
    },
    {
        "categoria": "💬 Atendimento & Suporte",
        "nome": "Chatbot com IA (ChatGPT)",
        "descricao": "Gerencia conversas no WhatsApp via ChatGPT, resolvendo dúvidas automaticamente ou escalando para humanos.",
        "icon": "🤖",
        "tools": ["WhatsApp", "OpenAI", "Chatwoot", "Dialogflow"],
        "complexity": "Avançado",
        "setup_time": "4-6 horas",
        "roi": "500% em economia",
        "workflow": "Mensagem WhatsApp → ChatGPT (gerar resposta) → Se resolver → Fechar | Se não resolver → Escalar para humano",
        "benefits": [
            {"title": "70% de Resolução Automática", "desc": "Maioria das dúvidas resolvidas sem humano"},
            {"title": "Atendimento 24/7", "desc": "Clientes atendidos mesmo fora do horário comercial"},
            {"title": "Redução de 50% em Custos", "desc": "Menos atendentes necessários para mesmo volume"}
        ],
        "expert_tip": "Treine a IA com suas FAQs e histórico de tickets reais. Quanto mais contexto você der, melhor a qualidade das respostas. Use 'temperature' baixa (0.3) para respostas consistentes.",
        "success_story": "Uma fintech implementou chatbot IA e reduziu tempo médio de atendimento de 8 minutos para 2 minutos, enquanto satisfação subiu de 7.2 para 8.9.",
        "search_query": "chatbot+ai+whatsapp"
    },
    {
        "categoria": "💬 Atendimento & Suporte",
        "nome": "Feedback Pós-Atendimento (NPS)",
        "descricao": "Envia pesquisa de satisfação após atendimento e alerta o gerente se a nota for baixa.",
        "icon": "📞",
        "tools": ["Zendesk", "Typeform", "Google Forms", "Slack"],
        "complexity": "Fácil",
        "setup_time": "45 minutos",
        "roi": "250% em qualidade",
        "workflow": "Ticket fechado → Aguardar 1h → Enviar pesquisa NPS → Salvar resposta → Se NPS < 7 → Alertar gerente + criar tarefa",
        "benefits": [
            {"title": "Medir Qualidade Real", "desc": "Feedback direto do cliente sobre cada atendimento"},
            {"title": "Identificar Problemas Rápido", "desc": "Gerente notificado imediatamente de NPS baixo"},
            {"title": "Melhoria Contínua", "desc": "Dados para coaching e treinamento do time"}
        ],
        "expert_tip": "Além do NPS, pergunte 'O que poderíamos ter feito melhor?'. Respostas qualitativas são ouro para melhorar processos.",
        "success_story": "Uma empresa de telecom identificou que 80% dos NPSs baixos vinham de um tipo específico de problema. Criaram automação para resolver e NPS subiu de 42 para 68.",
        "search_query": "nps+feedback+automation"
    },
    {
        "categoria": "👥 RH & People Ops",
        "nome": "Onboarding Automático de Colaboradores",
        "descricao": "Cria contas, envia mensagens de boas-vindas e tarefas no Trello para novos funcionários.",
        "icon": "🎉",
        "tools": ["Google Workspace", "Slack", "Trello", "BambooHR"],
        "complexity": "Médio",
        "setup_time": "2-3 horas",
        "roi": "400% em experiência",
        "workflow": "Novo contrato → Criar email @empresa → Adicionar ao Slack → Enviar boas-vindas → Criar board Trello → Agendar reuniões",
        "benefits": [
            {"title": "Experiência Consistente", "desc": "Todo novo funcionário tem o mesmo processo de excelência"},
            {"title": "Zero Esquecimento", "desc": "Nenhuma etapa crítica é esquecida"},
            {"title": "80% Menos Tempo", "desc": "RH economiza 6-8 horas por onboarding"}
        ],
        "expert_tip": "Crie uma 'welcome page' personalizada com foto, bio e links úteis do novo colaborador. Envie para o time antes do primeiro dia. Aumenta engajamento inicial.",
        "success_story": "Uma startup de 80 pessoas reduziu onboarding de 2 dias para 2 horas, melhorando satisfação dos novos contratados de 7.8 para 9.2.",
        "search_query": "onboarding+automation+hr"
    },
    {
        "categoria": "👥 RH & People Ops",
        "nome": "Triagem de Currículos com IA",
        "descricao": "Analisa currículos com ChatGPT, agenda entrevistas para perfis qualificados e envia e-mails de rejeição.",
        "icon": "📝",
        "tools": ["Gmail", "OpenAI", "Google Calendar", "Greenhouse"],
        "complexity": "Avançado",
        "setup_time": "3-4 horas",
        "roi": "600% em produtividade",
        "workflow": "Candidato aplica → ChatGPT analisa CV + descrição da vaga → Se match > 80% → Agendar entrevista | Senão → Email educado de rejeição",
        "benefits": [
            {"title": "Processar 100+ CVs em Minutos", "desc": "IA analisa em segundos o que humano levaria horas"},
            {"title": "Reduzir Viés", "desc": "Análise objetiva baseada em skills, não em nome/foto"},
            {"title": "Focar no que Importa", "desc": "Recrutadores entrevistam apenas perfis qualificados"}
        ],
        "expert_tip": "Use 'few-shot learning': dê exemplos de 3 CVs bons e 3 ruins para a IA. Isso melhora drasticamente a precisão da triagem.",
        "success_story": "Uma empresa de tech reduziu tempo de triagem de 40 horas/semana para 2 horas, permitindo que RH focasse em cultura fit e experiência do candidato.",
        "search_query": "resume+screening+ai"
    },
    {
        "categoria": "👥 RH & People Ops",
        "nome": "Aniversários e Celebrações Automáticos",
        "descricao": "Verifica aniversários diários e envia mensagens personalizadas e cartões via Slack e Canva API.",
        "icon": "🎂",
        "tools": ["Google Sheets", "Slack", "Canva API", "Gmail"],
        "complexity": "Fácil",
        "setup_time": "1 hora",
        "roi": "200% em cultura",
        "workflow": "Todo dia 8h → Verificar planilha de aniversários → Se hoje → Gerar cartão no Canva → Postar no Slack → Email personalizado",
        "benefits": [
            {"title": "Cultura de Reconhecimento", "desc": "Colaboradores se sentem valorizados e lembrados"},
            {"title": "Engajamento do Time", "desc": "Canal de celebrações aumenta conexão entre pessoas"},
            {"title": "Zero Esquecimento", "desc": "Ninguém fica sem parabenização"}
        ],
        "expert_tip": "Além de aniversários, automatize outras celebrações: aniversário de empresa (tempo de casa), conquistas (promoção, meta batida). Reconhecimento frequente aumenta retenção.",
        "success_story": "Uma empresa de 200 pessoas implementou automação de celebrações e viu o eNPS (employee Net Promoter Score) subir de 45 para 72 em 6 meses.",
        "search_query": "birthday+celebration+automation"
    },
    {
        "categoria": "💻 TI & DevOps",
        "nome": "Alerta de Bug Crítico",
        "descricao": "Notifica equipe via Slack, SMS e PagerDuty quando um bug crítico é identificado no Jira.",
        "icon": "🚨",
        "tools": ["Jira", "Slack", "PagerDuty", "SMS API"],
        "complexity": "Médio",
        "setup_time": "1-2 horas",
        "roi": "500% em uptime",
        "workflow": "Jira (bug priority = Critical) → Notificar Slack (#incidents) → SMS para on-call → Criar incidente PagerDuty → Abrir war room",
        "benefits": [
            {"title": "Resposta < 5 Minutos", "desc": "Time mobilizado instantaneamente"},
            {"title": "Escalonamento Automático", "desc": "Se on-call não responder em 10min, escala para manager"},
            {"title": "Redução de Downtime", "desc": "Bugs críticos resolvidos 3x mais rápido"}
        ],
        "expert_tip": "Configure 'runbooks' automáticos: quando um tipo específico de bug ocorre, a automação já envia o guia de troubleshooting junto com o alerta. Reduz tempo de diagnóstico.",
        "success_story": "Uma plataforma de pagamentos reduziu MTTR (Mean Time To Recovery) de 45 minutos para 12 minutos, evitando perdas de R$ 150k/mês em transações.",
        "search_query": "critical+bug+alert"
    },
    {
        "categoria": "💻 TI & DevOps",
        "nome": "Backup Automático Diário",
        "descricao": "Faz backup do banco PostgreSQL, compacta, salva no Google Drive e confirma no Slack.",
        "icon": "📊",
        "tools": ["PostgreSQL", "Google Drive", "Slack", "AWS S3"],
        "complexity": "Médio",
        "setup_time": "2-3 horas",
        "roi": "999% em segurança",
        "workflow": "Todo dia 3h → Dump PostgreSQL → Compactar (gzip) → Upload Google Drive + S3 → Slack (confirmação) → Se falhar → Alertar urgente",
        "benefits": [
            {"title": "Proteção Garantida", "desc": "Dados salvos automaticamente todo dia"},
            {"title": "Histórico de 30 Dias", "desc": "Múltiplos pontos de restauração"},
            {"title": "Alertas de Falha", "desc": "Notificação imediata se backup falhar"}
        ],
        "expert_tip": "Implemente '3-2-1 rule': 3 cópias dos dados, 2 mídias diferentes (Drive + S3), 1 off-site. E teste restauração mensalmente - backup não testado não é backup.",
        "success_story": "Uma empresa evitou perda total de dados após ransomware porque tinha backups automáticos. Restauração completa em 4 horas, evitando prejuízo de R$ 2M.",
        "search_query": "database+backup+automation"
    },
    {
        "categoria": "💻 TI & DevOps",
        "nome": "Monitoramento de Uptime",
        "descricao": "Executa pings regulares em servidores, alerta a equipe e tenta reiniciar automaticamente em caso de falha.",
        "icon": "🔧",
        "tools": ["Webhook", "AWS", "Telegram", "UptimeRobot"],
        "complexity": "Avançado",
        "setup_time": "3-4 horas",
        "roi": "800% em disponibilidade",
        "workflow": "A cada 5 min → Ping servidor → Se offline > 2 min → Alertar equipe → Tentar restart automático → Se persistir → Escalar",
        "benefits": [
            {"title": "Detectar Antes do Cliente", "desc": "Problemas identificados antes de reclamações"},
            {"title": "Auto-Healing", "desc": "80% dos problemas resolvidos automaticamente"},
            {"title": "99.9% de Uptime", "desc": "SLA garantido com monitoramento ativo"}
        ],
        "expert_tip": "Monitore não só 'server is up', mas também 'health checks': latência de API, uso de CPU/RAM, taxa de erro. Isso permite identificar degradação antes de falha total.",
        "success_story": "Um e-commerce identificou degradação de performance às 14h (horário de pico) e escalou recursos automaticamente, evitando R$ 80k em vendas perdidas.",
        "search_query": "uptime+monitoring+automation"
    }
]

def slugify(text):
    """Converte texto em slug URL-friendly"""
    text = text.lower()
    text = re.sub(r'[àáâãäå]', 'a', text)
    text = re.sub(r'[èéêë]', 'e', text)
    text = re.sub(r'[ìíîï]', 'i', text)
    text = re.sub(r'[òóôõö]', 'o', text)
    text = re.sub(r'[ùúûü]', 'u', text)
    text = re.sub(r'[ç]', 'c', text)
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text

def generate_page(caso):
    """Gera HTML para um caso de uso"""
    
    # Ler template
    with open('template_caso_uso.html', 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Criar slug
    slug = slugify(caso['nome'])
    
    # Gerar HTML dos benefícios
    benefits_html = ""
    for benefit in caso['benefits']:
        benefits_html += f'''                        <div class="benefit-card">
                            <h4>{benefit['title']}</h4>
                            <p>{benefit['desc']}</p>
                        </div>
'''
    
    # Gerar HTML das ferramentas
    tools_html = ""
    for tool in caso['tools']:
        tools_html += f'                        <span class="tool-tag">{tool}</span>\n'
    
    # Gerar workflow steps com arrows
    workflow_steps = caso['workflow'].replace(' → ', ' <span class="arrow">→</span> ')
    
    # Meta description otimizada
    meta_desc = f"{caso['descricao']} Guia completo de implementação com N8N, ferramentas necessárias e casos de sucesso reais."
    
    # Keywords
    keywords = f"n8n, automação, {caso['nome'].lower()}, {', '.join([t.lower() for t in caso['tools'][:3]])}, workflow automation"
    
    # Search query para CTA
    search_query = caso['search_query']
    
    # Passos de implementação (genéricos mas personalizáveis)
    step_1 = f"Instale o N8N (self-hosted ou cloud) e crie um novo workflow. Conecte-se às APIs necessárias: {', '.join(caso['tools'][:2])}. Teste as credenciais para garantir que a conexão está funcionando."
    
    step_2 = f"Configure os nodes de integração no N8N para {', '.join(caso['tools'])}. Defina os triggers (eventos que iniciam o workflow) e autentique cada serviço com suas credenciais."
    
    step_3 = f"Monte o fluxo seguindo a lógica: {caso['workflow']}. Use nodes de função para transformar dados entre diferentes formatos quando necessário."
    
    step_4 = f"Execute o workflow em modo de teste com dados fictícios. Verifique logs para identificar erros. Ajuste mapeamentos de campos e condições lógicas conforme necessário."
    
    step_5 = f"Ative o workflow em produção. Configure alertas para falhas no N8N. Monitore execuções nas primeiras 48h para garantir estabilidade. Documente o processo para o time."
    
    # Casos relacionados (3 da mesma categoria)
    related_html = ""
    related_cases = [c for c in CASOS_DE_USO if c['categoria'] == caso['categoria'] and c['nome'] != caso['nome']][:3]
    for related in related_cases:
        related_slug = slugify(related['nome'])
        related_html += f'''                        <a href="{related_slug}.html" class="related-card">
                            <h4>{related['icon']} {related['nome']}</h4>
                            <p style="font-size: 0.9rem; color: #666;">{related['descricao'][:80]}...</p>
                        </a>
'''
    
    # Substituir placeholders
    html = template.replace('{{TITLE}}', caso['nome'])
    html = html.replace('{{META_DESCRIPTION}}', meta_desc)
    html = html.replace('{{KEYWORDS}}', keywords)
    html = html.replace('{{SLUG}}', slug)
    html = html.replace('{{CATEGORY}}', caso['categoria'])
    html = html.replace('{{ICON}}', caso['icon'])
    html = html.replace('{{DESCRIPTION}}', caso['descricao'])
    html = html.replace('{{COMPLEXITY}}', caso['complexity'])
    html = html.replace('{{WORKFLOW_STEPS}}', workflow_steps)
    html = html.replace('{{BENEFITS_HTML}}', benefits_html)
    html = html.replace('{{TOOLS_HTML}}', tools_html)
    html = html.replace('{{STEP_1}}', step_1)
    html = html.replace('{{STEP_2}}', step_2)
    html = html.replace('{{STEP_3}}', step_3)
    html = html.replace('{{STEP_4}}', step_4)
    html = html.replace('{{STEP_5}}', step_5)
    html = html.replace('{{EXPERT_TIP}}', caso['expert_tip'])
    html = html.replace('{{SUCCESS_STORY}}', caso['success_story'])
    html = html.replace('{{SEARCH_QUERY}}', search_query)
    html = html.replace('{{RELATED_CASES_HTML}}', related_html)
    html = html.replace('{{SETUP_TIME}}', caso['setup_time'])
    html = html.replace('{{ROI}}', caso['roi'])
    
    return slug, html

def main():
    """Gera todas as páginas"""
    
    # Criar diretório
    output_dir = Path('casos-de-uso')
    output_dir.mkdir(exist_ok=True)
    
    print("🚀 Gerando páginas de casos de uso...\n")
    
    slugs = []
    
    for i, caso in enumerate(CASOS_DE_USO, 1):
        slug, html = generate_page(caso)
        
        # Salvar arquivo
        output_path = output_dir / f'{slug}.html'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        slugs.append({
            'slug': slug,
            'nome': caso['nome'],
            'categoria': caso['categoria'],
            'icon': caso['icon']
        })
        
        print(f"✅ [{i}/20] {caso['nome']}")
        print(f"    📄 casos-de-uso/{slug}.html")
    
    print(f"\n🎉 {len(CASOS_DE_USO)} páginas geradas com sucesso!")
    print(f"\n📋 Lista de slugs para atualizar casos-de-uso.html:")
    print("="*60)
    for item in slugs:
        print(f"{item['icon']} {item['nome']}")
        print(f"   Link: /casos-de-uso/{item['slug']}.html")
    
    # Salvar mapeamento para sitemap
    print(f"\n💾 Salvando mapeamento casos_de_uso_slugs.txt...")
    with open('casos_de_uso_slugs.txt', 'w', encoding='utf-8') as f:
        for item in slugs:
            f.write(f"/casos-de-uso/{item['slug']}.html\n")
    
    print("\n✅ Processo concluído!")
    print("\n📌 Próximos passos:")
    print("1. Atualizar casos-de-uso.html com links para as novas páginas")
    print("2. Atualizar sitemap.xml com as 20 novas URLs")
    print("3. Testar páginas no navegador")
    print("4. Commit e push para GitHub")

if __name__ == '__main__':
    main()
