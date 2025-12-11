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
        'category_pages': ('0.85', 'weekly'),
        'integrations_index': ('0.8', 'daily'),
        'templates': ('0.7', 'monthly'),
    }
    
    # Add main pages
    main_pages = [
        ('/', 'homepage', today),
        ('/sobre', 'main_pages', today),
        ('/llm', 'main_pages', today),
        ('/guia-automacoes-n8n', 'main_pages', today),
        ('/guia-automacoes-zapier', 'main_pages', today),
        ('/casos-de-uso', 'main_pages', today),
        ('/guia-workflows-crm-whatsapp', 'main_pages', today),
        ('/blog', 'main_pages', today),
        ('/blog/index.html', 'main_pages', today),
        ('/blog/permissoes-openai-n8n.html', 'main_pages', today),
        ('/blog/gerar-api-key-openai-segura.html', 'main_pages', today),
        ('/blog/setup-minimo-n8n-langchain.html', 'main_pages', today),
        ('/blog/azure-openai-vs-openai-n8n.html', 'main_pages', today),
        ('/blog/testar-conexao-openai-n8n.html', 'main_pages', today),
        ('/blog/rotacionar-chaves-openai-automaticamente.html', 'main_pages', today),
        ('/blog/aws-secrets-manager-n8n.html', 'main_pages', today),
        ('/blog/limitar-permissoes-api-key-openai.html', 'main_pages', today),
        ('/blog/auditar-uso-detectar-abuso-chave.html', 'main_pages', today),
        ('/blog/variaveis-ambiente-producao-n8n.html', 'main_pages', today),
        ('/blog/configurar-openai-langchain-n8n.html', 'main_pages', today),
        ('/blog/guia-agentes-ia-n8n.html', 'main_pages', today),
        ('/blog/agentes-ia-autonomos-2026.html', 'main_pages', today),
        ('/blog/benchmark-zapier-make-n8n-2025.html', 'main_pages', today),
        ('/blog/aeo-corrida-ouro-digital-2025.html', 'main_pages', today),
        ('/blog/zapier-hegemonia-2025.html', 'main_pages', today),
        ('/blog/fenomeno-zero-clique-ai-visibility-2025.html', 'main_pages', today),
        ('/blog/softr-backend-ia-n8n.html', 'main_pages', today),
        ('/blog/hyperautomation-rpa-ia-n8n.html', 'main_pages', today),
        ('/blog/tavily-pesquisa-web-agentes-n8n.html', 'main_pages', today),
        ('/blog/physical-ai-iot-robotica-n8n.html', 'main_pages', today),
        ('/blog/queue-mode-scale-n8n.html', 'main_pages', today),
        ('/blog/langgraph-vs-n8n-frameworks.html', 'main_pages', today),
        ('/blog/workflows-startups-leadgen-seo-n8n.html', 'main_pages', today),
        ('/blog/crewai-vs-n8n-multiagents.html', 'main_pages', today),
        ('/blog/autogen-microsoft-agents-n8n.html', 'main_pages', today),
        ('/blog/community-nodes-ia-scraping-n8n.html', 'main_pages', today),
        ('/blog/docker-prod-secrets-redis-n8n.html', 'main_pages', today),
        ('/blog/autogpt-goal-driven-agents-n8n.html', 'main_pages', today),
        ('/blog/mistral-agents-gdpr-n8n.html', 'main_pages', today),
        ('/blog/haystack-rag-enterprise-n8n.html', 'main_pages', today),
        ('/blog/agencias-n8n-contratar-2025.html', 'main_pages', today),
        ('/blog/updates-features-ia-n8n-2025.html', 'main_pages', today),
        ('/blog/langchain-code-node-devs-n8n.html', 'main_pages', today),
        ('/blog/qwen-agent-baixo-custo-n8n.html', 'main_pages', today),
        ('/blog/content-repurposing-video-blog-n8n.html', 'main_pages', today),
        ('/blog/support-triage-ai-n8n.html', 'main_pages', today),
        ('/blog/social-listening-outreach-n8n.html', 'main_pages', today),
        ('/blog/autonomous-ai-agents-2025-n8n.html', 'main_pages', today),
        ('/blog/n8n-zapier-make-comparativo-2026.html', 'main_pages', today),
        ('/blog/ai-agent-frameworks-2025.html', 'main_pages', today),
        ('/blog/automation-trends-agentic-ai-2025.html', 'main_pages', today),
        ('/blog/ai-agent-node-tutorial-iniciantes-n8n.html', 'main_pages', today),
        ('/blog/openai-api-key-security-n8n.html', 'main_pages', today),
        ('/blog/langchain-vs-n8n-2025.html', 'main_pages', today),
        ('/blog/melhores-apps-n8n-2025.html', 'main_pages', today),
        ('/blog/azure-openai-lgpd-compliance-n8n.html', 'main_pages', today),
        ('/blog/instalar-community-nodes-n8n-2025.html', 'main_pages', today),
        ('/blog/deepseek-ai-config-gratuita-n8n.html', 'main_pages', today),
        ('/blog/mcp-nodes-multi-agent-n8n.html', 'main_pages', today),
        ('/blog/elevenlabs-voice-ai-tts-n8n.html', 'main_pages', today),
        ('/blog/perplexity-ai-pesquisa-n8n.html', 'main_pages', today),
        ('/blog/obsidian-rest-api-knowledge-n8n.html', 'main_pages', today),
        ('/blog/github-copilot-code-review-n8n.html', 'main_pages', today),
        ('/blog/brightdata-scraping-web-n8n.html', 'main_pages', today),
        ('/blog/flowise-ai-chatbots-n8n.html', 'main_pages', today),
        ('/blog/kommo-crm-workflows-n8n.html', 'main_pages', today),
        ('/blog/templates-gratuitos-ai-n8n-2025.html', 'main_pages', today),
        ('/blog/n8n-vs-langflow-comparativo.html', 'main_pages', today),
        ('/blog/google-trends-gemini-analise-n8n.html', 'main_pages', today),
        ('/blog/ollama-self-hosted-ai-n8n.html', 'main_pages', today),
        ('/blog/rag-completo-embeddings-pinecone-n8n.html', 'main_pages', today),
        ('/blog/multi-agent-orchestrator-n8n.html', 'main_pages', today),
        ('/blog/youtube-transcripts-automacao-n8n.html', 'main_pages', today),
        ('/blog/vercel-ai-sdk-edge-n8n.html', 'main_pages', today),
        ('/blog/parsera-scraping-ai-n8n.html', 'main_pages', today),
        ('/blog/supabase-backend-ai-apps-n8n.html', 'main_pages', today),
        # Casos de Uso
        ('/casos-de-uso/leads-do-facebook-ads-para-crm.html', 'category_pages', today),
        ('/casos-de-uso/campanha-de-email-drip-automatica.html', 'category_pages', today),
        ('/casos-de-uso/dashboard-de-performance-diario.html', 'category_pages', today),
        ('/casos-de-uso/analise-de-sentimento-com-ia.html', 'category_pages', today),
        ('/casos-de-uso/follow-up-automatico-de-leads-frios.html', 'category_pages', today),
        ('/casos-de-uso/distribuicao-inteligente-de-leads.html', 'category_pages', today),
        ('/casos-de-uso/relatorio-semanal-de-pipeline.html', 'category_pages', today),
        ('/casos-de-uso/fluxo-completo-de-pedido-novo.html', 'category_pages', today),
        ('/casos-de-uso/alerta-de-estoque-baixo.html', 'category_pages', today),
        ('/casos-de-uso/pedido-de-review-automatico.html', 'category_pages', today),
        ('/casos-de-uso/recuperacao-de-carrinho-abandonado.html', 'category_pages', today),
        ('/casos-de-uso/email-ticket-automatico.html', 'category_pages', today),
        ('/casos-de-uso/chatbot-com-ia-chatgpt.html', 'category_pages', today),
        ('/casos-de-uso/feedback-pos-atendimento-nps.html', 'category_pages', today),
        ('/casos-de-uso/onboarding-automatico-de-colaboradores.html', 'category_pages', today),
        ('/casos-de-uso/triagem-de-curriculos-com-ia.html', 'category_pages', today),
        ('/casos-de-uso/aniversarios-e-celebracoes-automaticos.html', 'category_pages', today),
        ('/casos-de-uso/alerta-de-bug-critico.html', 'category_pages', today),
        ('/casos-de-uso/backup-automatico-diario.html', 'category_pages', today),
        ('/casos-de-uso/monitoramento-de-uptime.html', 'category_pages', today),
        ('/integracoes/', 'integrations_index', today),
        ('/integracoes-zapier/', 'integrations_index', today),
        ('/integracoes/index.html', 'integrations_index', today),
        ('/integracoes/crm/', 'category_pages', today),
        ('/integracoes/whatsapp/', 'category_pages', today),
        ('/integracoes/ecommerce/', 'category_pages', today),
        ('/integracoes/marketing/', 'category_pages', today),
        ('/integracoes/suporte/', 'category_pages', today),
    ]
    
    print(f"📄 Adicionando páginas principais...")
    for path, page_type, lastmod in main_pages:
        url = SubElement(urlset, 'url')
        SubElement(url, 'loc').text = f"{base_url}{path}"
        SubElement(url, 'lastmod').text = lastmod
        SubElement(url, 'changefreq').text = priority_map[page_type][1]
        SubElement(url, 'priority').text = priority_map[page_type][0]
    
    # Add template pages from CSV
    print(f"📚 Adicionando templates N8N do CSV...")
    
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
                print(f"   {count} templates N8N adicionados...")
    
    n8n_count = count
    print(f"✅ N8N: {n8n_count} templates")
    
    # Add Zapier template pages from CSV
    zapier_csv = 'automacoes_zapier_db.csv'
    if os.path.exists(zapier_csv):
        print(f"⚡ Adicionando templates Zapier do CSV...")
        
        with open(zapier_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            zapier_count = 0
            
            for row in reader:
                slug = row['slug_url']
                url_path = f"/integracoes-zapier/{slug}.html"
                
                url = SubElement(urlset, 'url')
                SubElement(url, 'loc').text = f"{base_url}{url_path}"
                SubElement(url, 'lastmod').text = today
                SubElement(url, 'changefreq').text = priority_map['templates'][1]
                SubElement(url, 'priority').text = priority_map['templates'][0]
                
                zapier_count += 1
        
        print(f"✅ Zapier: {zapier_count} templates")
        count = n8n_count + zapier_count
    else:
        print(f"⚠️  {zapier_csv} não encontrado, pulando templates Zapier")
    
    print(f"✅ TOTAL: {count + len(main_pages)} URLs")
    
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
Allow: /integracoes-zapier/

# Allow API documentation
Allow: /llm
Allow: /sobre

# Allow CSV data
Allow: /automacoes_db.csv
Allow: /automacoes_zapier_db.csv
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
