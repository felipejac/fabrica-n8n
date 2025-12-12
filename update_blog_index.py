#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adiciona os novos 30 artigos ao blog/index.html
"""

import re

# Dados dos novos artigos
new_articles_data = [
    {
        "slug": "self-reflecting-agents-n8n-reflexion",
        "title": "Self-Reflecting Agents: Como criar IAs que corrigem o próprio código no n8n",
        "description": "Implemente o padrão 'Reflexion' no n8n. Agentes que detectam seus próprios erros e tentam novamente automaticamente aumentam taxa de sucesso de 60% para 90%.",
        "date": "2025-12-05",
        "tags": ["Agentic AI", "n8n", "Reflexion", "Error Handling"]
    },
    {
        "slug": "plan-and-solve-hierarchical-planning-agents-n8n",
        "title": "Plan-and-Solve: Implementando Agentes de Planejamento Hierárquico (HPA)",
        "description": "Dividir para conquistar. Arquitetura onde um Agente Arquiteto planeja e Agentes Operários executam no n8n para tarefas complexas.",
        "date": "2025-12-05",
        "tags": ["Planning Agents", "n8n", "HPA", "Arquitetura"]
    },
    {
        "slug": "human-in-the-loop-slack-block-kit-n8n",
        "title": "Human-in-the-Loop 2.0: Interfaces de Aprovação via Slack Block Kit",
        "description": "Vá além dos botões 'Sim/Não'. Crie formulários de aprovação interativos no Slack para controlar seus agentes de IA.",
        "date": "2025-12-05",
        "tags": ["Slack", "HITL", "n8n", "UX"]
    },
    {
        "slug": "memoria-semantica-episodica-redis-qdrant-n8n",
        "title": "Memória Semântica vs. Episódica: Redis e Qdrant no n8n",
        "description": "Agentes inteligentes precisam lembrar. Arquitetura de memória dupla para conversas complexas usando Redis e Qdrant.",
        "date": "2025-12-05",
        "tags": ["Memória IA", "Redis", "Qdrant", "RAG"]
    },
    {
        "slug": "swarm-intelligence-scraping-massivo-n8n",
        "title": "Swarm Intelligence: Coordenando 50+ Mini-Agentes para Scraping",
        "description": "Processe dados em escala massiva usando o padrão Map-Reduce no n8n para coordenar um enxame de agentes.",
        "date": "2025-12-05",
        "tags": ["Swarm", "Scraping", "Map-Reduce", "n8n"]
    },
    {
        "slug": "graphrag-neo4j-knowledge-graph-n8n",
        "title": "GraphRAG Tutorial: Integrando Neo4j e n8n para Buscas Contextuais",
        "description": "Vá além da similaridade vetorial. Implemente GraphRAG no n8n para conectar pontos e entender relacionamentos complexos.",
        "date": "2025-12-05",
        "tags": ["GraphRAG", "Neo4j", "Knowledge Graph", "n8n"]
    },
    {
        "slug": "hybrid-search-bm25-vetores-n8n",
        "title": "Hybrid Search no n8n: Combinando Keyword Search (BM25) com Vetores",
        "description": "Vetores não resolvem tudo. Implemente Busca Híbrida no n8n para encontrar SKUs exatos e conceitos semânticos simultaneamente.",
        "date": "2025-12-05",
        "tags": ["Hybrid Search", "BM25", "RAG", "n8n"]
    },
    {
        "slug": "reranking-models-cohere-precisao-rag-n8n",
        "title": "Reranking Models: Melhorando a Precisão do Retrieval com Cohere",
        "description": "Pare de alimentar seu LLM com lixo. Use Reranking no n8n para filtrar documentos e aumentar a precisão do seu RAG.",
        "date": "2025-12-05",
        "tags": ["Cohere", "Rerank", "RAG", "Precisão"]
    },
    {
        "slug": "rag-multimodal-gpt4o-vision-pdfs-n8n",
        "title": "RAG Multimodal: Processando Gráficos e Tabelas de PDFs com GPT-4o",
        "description": "Texto não é tudo. Extraia e entenda gráficos, tabelas e imagens de PDFs para criar um RAG verdadeiramente completo.",
        "date": "2025-12-05",
        "tags": ["RAG Multimodal", "GPT-4o Vision", "OCR", "n8n"]
    },
    {
        "slug": "contextual-compression-otimizacao-tokens-rag-n8n",
        "title": "Contextual Compression: Otimizando Tokens em Pipelines RAG",
        "description": "Não envie documentos inteiros para o LLM. Comprima o contexto dinamicamente no n8n para economizar dinheiro e melhorar respostas.",
        "date": "2025-12-05",
        "tags": ["Otimização", "Tokens", "RAG", "Custos"]
    },
    {
        "slug": "automated-evals-deepeval-testes-alucinacoes-n8n",
        "title": "Automated Evals: Usando DeepEval no n8n para Testar Alucinações",
        "description": "Não confie, verifique. Implemente uma esteira de testes automatizados no n8n para garantir que seu agente não está alucinando.",
        "date": "2025-12-05",
        "tags": ["LLMOps", "DeepEval", "Testes", "QA"]
    },
    {
        "slug": "git-backed-workflows-github-actions-n8n",
        "title": "Git-backed Workflows: Versionamento Real de n8n com GitHub Actions",
        "description": "Trate seus workflows como código. Faça backup, versione e restaure seus fluxos do n8n automaticamente usando Git.",
        "date": "2025-12-05",
        "tags": ["Git", "DevOps", "GitHub Actions", "n8n"]
    },
    {
        "slug": "guardrails-ai-seguranca-prompt-injection-n8n",
        "title": "Segurança de Agentes: Implementando Guardrails AI contra Prompt Injection",
        "description": "Proteja seus agentes. Como implementar camadas de defesa (Input/Output Rails) no n8n para bloquear ataques de injeção de prompt.",
        "date": "2025-12-05",
        "tags": ["Segurança", "Guardrails", "Prompt Injection", "n8n"]
    },
    {
        "slug": "finops-monitoramento-custos-openai-grafana-n8n",
        "title": "Monitoramento de Custos: Dashboard de FinOps para OpenAI com Grafana",
        "description": "Quem está gastando seus tokens? Rastreie, logge e visualize custos de IA por departamento ou workflow no n8n.",
        "date": "2025-12-05",
        "tags": ["FinOps", "Grafana", "Monitoramento", "Custos"]
    },
    {
        "slug": "error-handling-dead-letter-queue-n8n",
        "title": "Error Handling Robusto: Padrões de 'Dead Letter Queue' no n8n",
        "description": "O que acontece quando sua automação falha? Não perca dados. Implemente o padrão Dead Letter Queue (DLQ) para reprocessamento.",
        "date": "2025-12-05",
        "tags": ["Error Handling", "DLQ", "Confiabilidade", "n8n"]
    },
    {
        "slug": "groq-agentes-voz-baixa-latencia-n8n",
        "title": "n8n + Groq: Construindo Agentes de Voz com Latência <500ms",
        "description": "A velocidade é a nova inteligência. Use a Groq no n8n para criar experiências de IA conversacional instantâneas.",
        "date": "2025-12-05",
        "tags": ["Groq", "Voice AI", "Baixa Latência", "n8n"]
    },
    {
        "slug": "browser-use-vs-puppeteer-navegacao-autonoma-n8n",
        "title": "Browser-Use vs Puppeteer: A Nova Era da Navegação Autônoma no n8n",
        "description": "Adeus seletores CSS quebrados. Conheça o 'browser-use', que permite agentes navegarem na web visualmente como humanos.",
        "date": "2025-12-05",
        "tags": ["Browser-Use", "Puppeteer", "Vision AI", "Scraping"]
    },
    {
        "slug": "cursor-composer-code-nodes-javascript-n8n",
        "title": "Cursor Composer + n8n: Gerando Nodes de Código Javascript com Contexto",
        "description": "Pare de sofrer com sintaxe. Use o Cursor Composer para escrever Code Nodes complexos para o n8n em segundos.",
        "date": "2025-12-05",
        "tags": ["Cursor", "IDE AI", "JavaScript", "Produtividade"]
    },
    {
        "slug": "vapi-ai-chamadas-telefonicas-ia-n8n",
        "title": "Vapi.ai + n8n: Orquestrando Chamadas Telefônicas de IA",
        "description": "Crie atendentes telefônicos inteligentes. Use o n8n como o cérebro lógico por trás da infraestrutura de voz da Vapi.ai.",
        "date": "2025-12-05",
        "tags": ["Vapi.ai", "Voice Agents", "Telefonia", "Function Calling"]
    },
    {
        "slug": "firecrawl-scraping-markdown-llms-n8n",
        "title": "Firecrawl Integration: Transformando Sites em Markdown Limpo para LLMs",
        "description": "Alimente seus agentes com dados da web de alta qualidade. Use Firecrawl no n8n para converter sites complexos em Markdown.",
        "date": "2025-12-05",
        "tags": ["Firecrawl", "Scraping", "Markdown", "RAG"]
    },
    {
        "slug": "legal-tech-analise-contratos-claude-sonnet-n8n",
        "title": "Legal Tech Automation: Analisador de Contratos com Claude 3.5 Sonnet",
        "description": "Automatize a revisão de minutas. Use a precisão do Claude 3.5 Sonnet no n8n para identificar cláusulas de risco em contratos.",
        "date": "2025-12-05",
        "tags": ["Legal Tech", "Claude 3.5", "Contratos", "Análise de Risco"]
    },
    {
        "slug": "ai-sdr-enriquecimento-leads-waterfall-n8n",
        "title": "AI SDR: Enriquecimento de Leads com Waterfall (Apollo -> Clay -> n8n)",
        "description": "Recrie a lógica do Clay.com dentro do n8n. Faça enriquecimento de dados em cascata para economizar custos de API.",
        "date": "2025-12-05",
        "tags": ["AI SDR", "Vendas", "Waterfall", "Leads"]
    },
    {
        "slug": "financeiro-reconciliacao-bancaria-vision-ai-n8n",
        "title": "Financeiro: Reconciliação Bancária Inteligente com Vision AI (OCR)",
        "description": "O fim da digitação manual. Use GPT-4o Vision no n8n para ler comprovantes (fotos) e cruzar com o extrato bancário.",
        "date": "2025-12-05",
        "tags": ["Financeiro", "Vision AI", "OCR", "Fintech"]
    },
    {
        "slug": "devrel-ops-agente-github-discord-n8n",
        "title": "DevRel Ops: Agente que Responde Issues do GitHub e Discord Automaticamente",
        "description": "Escale seu suporte à comunidade. Crie um agente que lê sua documentação e responde dúvidas técnicas no GitHub e Discord.",
        "date": "2025-12-05",
        "tags": ["DevRel", "GitHub", "Discord", "Comunidade"]
    },
    {
        "slug": "hr-tech-triagem-curriculos-blind-screening-n8n",
        "title": "HR Tech: Triagem de Currículos Cega (Blind Screening) com IA Ética",
        "description": "Elimine vieses inconscientes na contratação. Crie um pipeline no n8n que anonimiza currículos e avalia skills objetivamente.",
        "date": "2025-12-05",
        "tags": ["RH", "Recrutamento", "IA Ética", "Blind Screening"]
    },
    {
        "slug": "localai-openai-alternative-air-gapped-n8n",
        "title": "LocalAI + n8n: Substituindo 100% das APIs da OpenAI em Ambiente Air-Gapped",
        "description": "Crie uma infraestrutura de IA totalmente offline. Use o LocalAI para emular a API da OpenAI dentro do n8n.",
        "date": "2025-12-05",
        "tags": ["LocalAI", "OpenAI Alternative", "Air-Gapped", "Privacidade"]
    },
    {
        "slug": "phi-3-raspberry-pi-edge-ai-n8n",
        "title": "Phi-3.5 on Edge: Rodando Small Language Models em Raspberry Pi com n8n",
        "description": "IA poderosa que cabe no bolso. Rode o modelo Phi-3.5 da Microsoft em um Raspberry Pi 5 orquestrado pelo n8n.",
        "date": "2025-12-05",
        "tags": ["Raspberry Pi", "Edge AI", "Phi-3", "IoT"]
    },
    {
        "slug": "whisper-turbo-transcricao-local-privacidade-n8n",
        "title": "Whisper Turbo Local: Transcrição de Reuniões Privadas sem API Externa",
        "description": "Transcreva áudios confidenciais (médicos, jurídicos) sem enviá-los para a OpenAI. Tutorial de setup do Faster-Whisper com n8n.",
        "date": "2025-12-05",
        "tags": ["Whisper", "Transcrição", "Privacidade", "Local"]
    },
    {
        "slug": "llama-3-2-vision-cameras-seguranca-n8n",
        "title": "Llama 3.2 Vision Local: Analisando Câmeras de Segurança com n8n",
        "description": "Transforme câmeras 'burras' em inteligentes. Use n8n e Llama 3.2 Vision para detectar eventos em vídeo RTSP localmente.",
        "date": "2025-12-05",
        "tags": ["Llama 3.2", "Vision AI", "CCTV", "Segurança"]
    },
    {
        "slug": "private-rag-qdrant-huggingface-embeddings-n8n",
        "title": "Private RAG: Qdrant Local + Embeddings HuggingFace no n8n",
        "description": "RAG sem OpenAI. Construa uma base de conhecimento completa usando Qdrant e modelos de Embedding open-source dentro do n8n.",
        "date": "2025-12-05",
        "tags": ["RAG Local", "Qdrant", "HuggingFace", "Privacidade"]
    },
    {
        "slug": "gemini-1-5-pro-video-analysis-multimodal-n8n",
        "title": "Multi-Modal Agents com Gemini 1.5 Pro: Analisando Vídeos Longos (1h+)",
        "description": "Encontre uma agulha num palheiro de vídeo. Use a janela de contexto de 1 milhão de tokens do Gemini para analisar horas de vídeo no n8n.",
        "date": "2025-12-05",
        "tags": ["Gemini", "Video Analysis", "Multimodal", "Google"]
    }
]

def generate_article_card_html(article):
    """Gera o HTML de um card de artigo"""
    tags_html = "".join([f'<span class="bg-blue-100 text-blue-700 px-2 py-1 rounded font-semibold mr-2">{tag}</span>' for tag in article["tags"]])
    
    # Emoji baseado na primeira tag
    emoji_map = {
        "Agentic AI": "🤖", "Planning Agents": "🧠", "Slack": "💬", "Memória IA": "🧩",
        "Swarm": "🐝", "GraphRAG": "🕸️", "Hybrid Search": "🔍", "Cohere": "📊",
        "RAG Multimodal": "👁️", "Otimização": "⚡", "LLMOps": "🔬", "Git": "📝",
        "Segurança": "🔒", "FinOps": "💰", "Error Handling": "🛡️", "Groq": "⚡",
        "Browser-Use": "🌐", "Cursor": "✨", "Vapi.ai": "📞", "Firecrawl": "🕷️",
        "Legal Tech": "⚖️", "AI SDR": "🎯", "Financeiro": "💳", "DevRel": "👥",
        "RH": "📋", "LocalAI": "🏠", "Raspberry Pi": "🍓", "Whisper": "🎙️",
        "Llama 3.2": "🦙", "RAG Local": "🔐", "Gemini": "✨"
    }
    emoji = emoji_map.get(article["tags"][0], "🚀")
    
    return f'''
            <!-- Artigo {article['slug']} -->
            <article class="bg-white rounded-xl shadow-md overflow-hidden card-hover">
                <div class="h-48 bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-600 relative flex items-center justify-center">
                    <div class="flex items-center gap-3">
                        <div class="text-white text-center">
                            <div class="text-6xl mb-2">{emoji}</div>
                            <div class="text-sm font-bold opacity-90">{article["tags"][0]}</div>
                        </div>
                    </div>
                </div>
                <div class="p-6">
                    <div class="flex items-center gap-2 text-xs text-gray-500 mb-3">
                        {tags_html}
                        <span>•</span>
                        <time datetime="{article['date']}">05 Dez 2025</time>
                    </div>
                    <h3 class="text-xl font-bold text-gray-900 mb-3 leading-tight hover:text-blue-600 transition">
                        <a href="/blog/{article['slug']}.html">
                            {article['title']}
                        </a>
                    </h3>
                    <p class="text-gray-600 mb-4 text-sm leading-relaxed">
                        {article['description']}
                    </p>
                    <a href="/blog/{article['slug']}.html" class="inline-flex items-center text-blue-600 hover:text-blue-700 font-semibold text-sm transition group">
                        Ler artigo
                        <svg class="w-4 h-4 ml-1 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                        </svg>
                    </a>
                </div>
            </article>'''

def update_blog_index():
    index_path = "/workspaces/fabrica-n8n/blog/index.html"
    
    # Ler o arquivo existente
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Gerar HTML de todos os novos artigos
    new_articles_html = "\n".join([generate_article_card_html(article) for article in new_articles_data])
    
    # Encontrar a seção de artigos e adicionar os novos
    # Procura pelo grid de artigos - id="articles-grid"
    marker = '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8" id="articles-grid">'
    
    if marker in content:
        # Insere os novos artigos logo após a abertura do grid
        new_content = content.replace(
            marker,
            f'{marker}\n{new_articles_html}\n'
        )
        
        # Salvar arquivo atualizado
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("✅ blog/index.html atualizado com sucesso!")
        print(f"📊 {len(new_articles_data)} novos artigos adicionados ao topo da lista")
    else:
        print("❌ Não foi possível encontrar a seção de artigos no index.html")

if __name__ == "__main__":
    update_blog_index()
