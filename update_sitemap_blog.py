#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Atualiza sitemap-blog.xml com os novos 30 artigos
"""

import xml.etree.ElementTree as ET
from datetime import datetime

# Novos slugs dos artigos
new_articles = [
    "self-reflecting-agents-n8n-reflexion",
    "plan-and-solve-hierarchical-planning-agents-n8n",
    "human-in-the-loop-slack-block-kit-n8n",
    "memoria-semantica-episodica-redis-qdrant-n8n",
    "swarm-intelligence-scraping-massivo-n8n",
    "graphrag-neo4j-knowledge-graph-n8n",
    "hybrid-search-bm25-vetores-n8n",
    "reranking-models-cohere-precisao-rag-n8n",
    "rag-multimodal-gpt4o-vision-pdfs-n8n",
    "contextual-compression-otimizacao-tokens-rag-n8n",
    "automated-evals-deepeval-testes-alucinacoes-n8n",
    "git-backed-workflows-github-actions-n8n",
    "guardrails-ai-seguranca-prompt-injection-n8n",
    "finops-monitoramento-custos-openai-grafana-n8n",
    "error-handling-dead-letter-queue-n8n",
    "groq-agentes-voz-baixa-latencia-n8n",
    "browser-use-vs-puppeteer-navegacao-autonoma-n8n",
    "cursor-composer-code-nodes-javascript-n8n",
    "vapi-ai-chamadas-telefonicas-ia-n8n",
    "firecrawl-scraping-markdown-llms-n8n",
    "legal-tech-analise-contratos-claude-sonnet-n8n",
    "ai-sdr-enriquecimento-leads-waterfall-n8n",
    "financeiro-reconciliacao-bancaria-vision-ai-n8n",
    "devrel-ops-agente-github-discord-n8n",
    "hr-tech-triagem-curriculos-blind-screening-n8n",
    "localai-openai-alternative-air-gapped-n8n",
    "phi-3-raspberry-pi-edge-ai-n8n",
    "whisper-turbo-transcricao-local-privacidade-n8n",
    "llama-3-2-vision-cameras-seguranca-n8n",
    "private-rag-qdrant-huggingface-embeddings-n8n",
    "gemini-1-5-pro-video-analysis-multimodal-n8n"
]

def update_sitemap():
    sitemap_path = "/workspaces/fabrica-n8n/sitemap-blog.xml"
    
    # Parse o XML existente
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    
    # Namespace para sitemap
    ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    
    # Get existing URLs
    existing_locs = {url.find('sm:loc', ns).text for url in root.findall('sm:url', ns)}
    
    # Data atual
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Adicionar novos artigos
    added = 0
    for slug in new_articles:
        url = f"https://www.automationscookbook.com/blog/{slug}.html"
        
        if url not in existing_locs:
            url_elem = ET.SubElement(root, 'url')
            
            loc = ET.SubElement(url_elem, 'loc')
            loc.text = url
            
            lastmod = ET.SubElement(url_elem, 'lastmod')
            lastmod.text = today
            
            changefreq = ET.SubElement(url_elem, 'changefreq')
            changefreq.text = 'weekly'
            
            priority = ET.SubElement(url_elem, 'priority')
            priority.text = '0.8'
            
            added += 1
            print(f"✅ Adicionado: {slug}")
    
    # Salvar XML atualizado
    tree.write(sitemap_path, encoding='UTF-8', xml_declaration=True)
    
    print(f"\n🎉 Sitemap atualizado!")
    print(f"📊 {added} novos artigos adicionados")
    print(f"📄 Total de URLs no sitemap: {len(root.findall('url', ns))}")

if __name__ == "__main__":
    update_sitemap()
