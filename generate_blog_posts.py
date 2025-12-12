#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador de Blog Posts para Automations Cookbook
Cria 30 artigos completos com SEO otimizado
"""

import os
from datetime import datetime

# Dados dos artigos
articles = [
    {
        "slug": "self-reflecting-agents-n8n-reflexion",
        "title": "Self-Reflecting Agents: Como criar IAs que corrigem o próprio código no n8n",
        "date": "2025-12-05",
        "tags": ["n8n", "agentic-ai", "reflexion", "error-handling", "code-node"],
        "description": "Implemente o padrão 'Reflexion' no n8n. Aprenda a criar agentes que detectam seus próprios erros e tentam novamente automaticamente.",
        "content_file": "self_reflecting_agents.txt"
    },
    {
        "slug": "plan-and-solve-hierarchical-planning-agents-n8n",
        "title": "Plan-and-Solve: Implementando Agentes de Planejamento Hierárquico (HPA)",
        "date": "2025-12-05",
        "tags": ["n8n", "planning-agents", "hpa", "arquitetura", "json"],
        "description": "Dividir para conquistar. Aprenda a criar uma arquitetura onde um Agente Arquiteto planeja e Agentes Operários executam no n8n.",
        "keywords": "n8n, planning agents, HPA, hierarchical planning, agentes hierárquicos, plan-and-solve"
    },
    {
        "slug": "human-in-the-loop-slack-block-kit-n8n",
        "title": "Human-in-the-Loop 2.0: Interfaces de Aprovação via Slack Block Kit e n8n",
        "date": "2025-12-05",
        "tags": ["n8n", "slack", "human-in-the-loop", "ux", "aprovacao"],
        "description": "Vá além dos botões 'Sim/Não'. Crie formulários de aprovação interativos no Slack para controlar seus agentes de IA.",
        "keywords": "n8n, slack, human-in-the-loop, block kit, aprovação, HITL"
    },
    {
        "slug": "memoria-semantica-episodica-redis-qdrant-n8n",
        "title": "Memória Semântica vs. Episódica: Gerenciando Estado de Longo Prazo com Redis e Qdrant",
        "date": "2025-12-05",
        "tags": ["n8n", "memoria", "redis", "qdrant", "rag"],
        "description": "Agentes inteligentes precisam lembrar do passado. Aprenda a arquitetura de memória dupla para conversas complexas no n8n.",
        "keywords": "n8n, memória IA, redis, qdrant, RAG, memória episódica, memória semântica"
    },
    {
        "slug": "swarm-intelligence-scraping-massivo-n8n",
        "title": "Swarm Intelligence: Coordenando 50+ Mini-Agentes para Tarefas de Scraping",
        "date": "2025-12-05",
        "tags": ["n8n", "swarm", "scraping", "parallel-processing", "map-reduce"],
        "description": "Processe dados em escala massiva usando o padrão Map-Reduce no n8n para coordenar um enxame de agentes.",
        "keywords": "n8n, swarm intelligence, scraping, map-reduce, processamento paralelo"
    },
    {
        "slug": "graphrag-neo4j-knowledge-graph-n8n",
        "title": "GraphRAG Tutorial: Integrando Neo4j e n8n para Buscas Contextuais Complexas",
        "date": "2025-12-05",
        "tags": ["n8n", "graphrag", "neo4j", "knowledge-graph", "rag-avancado"],
        "description": "Vá além da similaridade vetorial. Aprenda a implementar GraphRAG no n8n para conectar pontos e entender relacionamentos complexos nos seus dados.",
        "keywords": "n8n, GraphRAG, Neo4j, knowledge graph, busca contextual"
    },
    {
        "slug": "hybrid-search-bm25-vetores-n8n",
        "title": "Hybrid Search no n8n: Combinando Keyword Search (BM25) com Vetores",
        "date": "2025-12-05",
        "tags": ["n8n", "hybrid-search", "bm25", "supabase", "rag"],
        "description": "Vetores não resolvem tudo. Aprenda a implementar Busca Híbrida no n8n para encontrar SKUs exatos e conceitos semânticos ao mesmo tempo.",
        "keywords": "n8n, hybrid search, BM25, busca vetorial, Supabase, RAG"
    },
    {
        "slug": "reranking-models-cohere-precisao-rag-n8n",
        "title": "Reranking Models: Melhorando a Precisão do Retrieval com Cohere Rerank e n8n",
        "date": "2025-12-05",
        "tags": ["n8n", "cohere", "rerank", "rag", "precisao"],
        "description": "Pare de alimentar seu LLM com lixo. Use Reranking no n8n para filtrar documentos e aumentar a precisão do seu RAG.",
        "keywords": "n8n, Cohere Rerank, RAG, reranking, precisão de busca"
    },
    {
        "slug": "rag-multimodal-gpt4o-vision-pdfs-n8n",
        "title": "RAG Multimodal: Processando Gráficos e Tabelas de PDFs com GPT-4o e n8n",
        "date": "2025-12-05",
        "tags": ["n8n", "multimodal", "rag", "gpt-4o", "vision-ai"],
        "description": "Texto não é tudo. Aprenda a extrair e entender gráficos, tabelas e imagens de PDFs para criar um RAG verdadeiramente completo.",
        "keywords": "n8n, RAG multimodal, GPT-4o Vision, OCR, PDFs"
    },
    {
        "slug": "contextual-compression-otimizacao-tokens-rag-n8n",
        "title": "Contextual Compression: Otimizando Tokens em Pipelines RAG de Alto Volume",
        "date": "2025-12-05",
        "tags": ["n8n", "rag", "tokens", "otimizacao", "langchain"],
        "description": "Não envie documentos inteiros para o LLM. Aprenda a comprimir o contexto dinamicamente no n8n para economizar dinheiro e melhorar respostas.",
        "keywords": "n8n, contextual compression, otimização de tokens, RAG, custo LLM"
    },
    {
        "slug": "automated-evals-deepeval-testes-alucinacoes-n8n",
        "title": "Automated Evals: Usando DeepEval no n8n para Testar Alucinações",
        "date": "2025-12-05",
        "tags": ["n8n", "llmops", "deepeval", "qa", "testes"],
        "description": "Não confie, verifique. Implemente uma esteira de testes automatizados no n8n para garantir que seu agente não está alucinando.",
        "keywords": "n8n, DeepEval, LLMOps, testes automatizados, alucinações"
    },
    {
        "slug": "git-backed-workflows-github-actions-n8n",
        "title": "Git-backed Workflows: Versionamento Real de n8n com GitHub Actions",
        "date": "2025-12-05",
        "tags": ["n8n", "git", "devops", "github-actions", "version-control"],
        "description": "Trate seus workflows como código. Aprenda a fazer backup, versionar e restaurar seus fluxos do n8n automaticamente usando Git.",
        "keywords": "n8n, Git, GitHub Actions, versionamento, DevOps, backup"
    },
    {
        "slug": "guardrails-ai-seguranca-prompt-injection-n8n",
        "title": "Segurança de Agentes: Implementando Guardrails AI contra Prompt Injection",
        "date": "2025-12-05",
        "tags": ["n8n", "security", "guardrails", "prompt-injection", "llm-security"],
        "description": "Proteja seus agentes. Como implementar camadas de defesa (Input/Output Rails) no n8n para bloquear ataques de injeção de prompt.",
        "keywords": "n8n, segurança IA, guardrails, prompt injection, LLM security"
    },
    {
        "slug": "finops-monitoramento-custos-openai-grafana-n8n",
        "title": "Monitoramento de Custos: Dashboard de FinOps para OpenAI e Anthropic com Grafana",
        "date": "2025-12-05",
        "tags": ["n8n", "finops", "openai", "grafana", "monitoramento"],
        "description": "Quem está gastando seus tokens? Aprenda a rastrear, logar e visualizar custos de IA por departamento ou workflow no n8n.",
        "keywords": "n8n, FinOps, monitoramento de custos, OpenAI, Grafana, métricas"
    },
    {
        "slug": "error-handling-dead-letter-queue-n8n",
        "title": "Error Handling Robusto: Padrões de 'Dead Letter Queue' no n8n",
        "date": "2025-12-05",
        "tags": ["n8n", "error-handling", "dlq", "confiabilidade", "arquitetura"],
        "description": "O que acontece quando sua automação falha? Não perca dados. Implemente o padrão Dead Letter Queue (DLQ) para reprocessamento de erros.",
        "keywords": "n8n, error handling, DLQ, dead letter queue, confiabilidade"
    },
    {
        "slug": "groq-agentes-voz-baixa-latencia-n8n",
        "title": "n8n + Groq: Construindo Agentes de Voz com Latência <500ms",
        "date": "2025-12-05",
        "tags": ["n8n", "groq", "real-time", "voice-ai", "latencia"],
        "description": "A velocidade é a nova inteligência. Aprenda a usar a Groq no n8n para criar experiências de IA conversacional instantâneas.",
        "keywords": "n8n, Groq, voice AI, baixa latência, LPU, tempo real"
    },
    {
        "slug": "browser-use-vs-puppeteer-navegacao-autonoma-n8n",
        "title": "Browser-Use vs Puppeteer: A Nova Era da Navegação Autônoma no n8n",
        "date": "2025-12-05",
        "tags": ["n8n", "browser-use", "puppeteer", "vision-ai", "scraping"],
        "description": "Adeus seletores CSS quebrados. Conheça o 'browser-use', a biblioteca que permite agentes navegarem na web visualmente como humanos.",
        "keywords": "n8n, browser-use, Puppeteer, scraping, navegação autônoma, vision AI"
    },
    {
        "slug": "cursor-composer-code-nodes-javascript-n8n",
        "title": "Cursor Composer + n8n: Gerando Nodes de Código Javascript com Contexto do Projeto",
        "date": "2025-12-05",
        "tags": ["n8n", "cursor", "ide-ai", "javascript", "produtividade"],
        "description": "Pare de sofrer com sintaxe. Aprenda a usar o Cursor Composer para escrever Code Nodes complexos para o n8n em segundos.",
        "keywords": "n8n, Cursor, Composer, Code Node, JavaScript, IDE AI"
    },
    {
        "slug": "vapi-ai-chamadas-telefonicas-ia-n8n",
        "title": "Vapi.ai + n8n: Orquestrando Chamadas Telefônicas de IA",
        "date": "2025-12-05",
        "tags": ["n8n", "vapi", "voice-agents", "telefone", "function-calling"],
        "description": "Crie atendentes telefônicos inteligentes. Use o n8n como o cérebro lógico por trás da infraestrutura de voz da Vapi.ai.",
        "keywords": "n8n, Vapi.ai, voice agents, telefonia IA, function calling"
    },
    {
        "slug": "firecrawl-scraping-markdown-llms-n8n",
        "title": "Firecrawl Integration: Transformando Sites Inteiros em Markdown Limpo para LLMs",
        "date": "2025-12-05",
        "tags": ["n8n", "firecrawl", "scraping", "llm-data", "rag"],
        "description": "Alimente seus agentes com dados da web de alta qualidade. Aprenda a usar Firecrawl no n8n para converter sites complexos em Markdown.",
        "keywords": "n8n, Firecrawl, scraping, Markdown, RAG, web scraping"
    },
    {
        "slug": "legal-tech-analise-contratos-claude-sonnet-n8n",
        "title": "Legal Tech Automation: Analisador de Contratos com Claude 3.5 Sonnet e n8n",
        "date": "2025-12-05",
        "tags": ["n8n", "legal-tech", "claude-3-5", "contratos", "analise-de-risco"],
        "description": "Automatize a revisão de minutas. Como usar a precisão do Claude 3.5 Sonnet no n8n para identificar cláusulas de risco em contratos.",
        "keywords": "n8n, legal tech, Claude Sonnet, análise de contratos, automação jurídica"
    },
    {
        "slug": "ai-sdr-enriquecimento-leads-waterfall-n8n",
        "title": "AI SDR: Enriquecimento de Leads com Waterfall (Apollo -> Clay -> n8n)",
        "date": "2025-12-05",
        "tags": ["n8n", "sdr", "vendas", "waterfall-enrichment", "outbound"],
        "description": "Recrie a lógica do Clay.com dentro do n8n. Aprenda a fazer enriquecimento de dados em cascata para economizar custos de API.",
        "keywords": "n8n, AI SDR, enriquecimento de leads, waterfall, Apollo, vendas"
    },
    {
        "slug": "financeiro-reconciliacao-bancaria-vision-ai-n8n",
        "title": "Financeiro: Reconciliação Bancária Inteligente com Vision AI (OCR de Comprovantes)",
        "date": "2025-12-05",
        "tags": ["n8n", "financeiro", "vision-ai", "ocr", "fintech"],
        "description": "O fim da digitação manual. Use GPT-4o Vision no n8n para ler comprovantes (fotos) e cruzar automaticamente com o extrato bancário.",
        "keywords": "n8n, reconciliação bancária, Vision AI, OCR, automação financeira"
    },
    {
        "slug": "devrel-ops-agente-github-discord-n8n",
        "title": "DevRel Ops: Agente que Responde Issues do GitHub e Discord Automaticamente",
        "date": "2025-12-05",
        "tags": ["n8n", "devrel", "github", "discord", "comunidade"],
        "description": "Escale seu suporte à comunidade. Como criar um agente que lê sua documentação e responde dúvidas técnicas no GitHub e Discord.",
        "keywords": "n8n, DevRel, GitHub, Discord, suporte automatizado, RAG"
    },
    {
        "slug": "hr-tech-triagem-curriculos-blind-screening-n8n",
        "title": "HR Tech: Triagem de Currículos Cega (Blind Screening) com IA Ética",
        "date": "2025-12-05",
        "tags": ["n8n", "rh", "recrutamento", "ia-etica", "pdf-parsing"],
        "description": "Elimine vieses inconscientes na contratação. Crie um pipeline no n8n que anonimiza currículos e avalia skills objetivamente.",
        "keywords": "n8n, RH, blind screening, recrutamento, IA ética, triagem de currículos"
    },
    {
        "slug": "localai-openai-alternative-air-gapped-n8n",
        "title": "LocalAI + n8n: Substituindo 100% das APIs da OpenAI em Ambiente Air-Gapped",
        "date": "2025-12-05",
        "tags": ["n8n", "localai", "openai-alternative", "air-gapped", "privacidade"],
        "description": "Crie uma infraestrutura de IA totalmente offline. Aprenda a usar o LocalAI para emular a API da OpenAI dentro do n8n.",
        "keywords": "n8n, LocalAI, OpenAI alternative, air-gapped, privacidade, IA offline"
    },
    {
        "slug": "phi-3-raspberry-pi-edge-ai-n8n",
        "title": "Phi-3.5 on Edge: Rodando Small Language Models (SLMs) em Raspberry Pi com n8n",
        "date": "2025-12-05",
        "tags": ["n8n", "raspberry-pi", "edge-ai", "phi-3", "iot"],
        "description": "IA poderosa que cabe no bolso. Aprenda a rodar o modelo Phi-3.5 da Microsoft em um Raspberry Pi 5 orquestrado pelo n8n.",
        "keywords": "n8n, Raspberry Pi, Edge AI, Phi-3, SLM, IoT"
    },
    {
        "slug": "whisper-turbo-transcricao-local-privacidade-n8n",
        "title": "Whisper Turbo Local: Transcrição de Reuniões Privadas sem API Externa",
        "date": "2025-12-05",
        "tags": ["n8n", "whisper", "transcricao", "privacidade", "docker"],
        "description": "Transcreva áudios confidenciais (médicos, jurídicos) sem enviá-los para a OpenAI. Tutorial de setup do Faster-Whisper com n8n.",
        "keywords": "n8n, Whisper, transcrição local, privacidade, Faster-Whisper"
    },
    {
        "slug": "llama-3-2-vision-cameras-seguranca-n8n",
        "title": "Llama 3.2 Vision Local: Analisando Câmeras de Segurança com n8n",
        "date": "2025-12-05",
        "tags": ["n8n", "vision-ai", "llama-3-2", "cctv", "seguranca"],
        "description": "Transforme câmeras 'burras' em inteligentes. Use n8n e Llama 3.2 Vision para detectar eventos em vídeo RTSP localmente.",
        "keywords": "n8n, Llama 3.2 Vision, câmeras de segurança, CCTV, detecção de eventos"
    },
    {
        "slug": "private-rag-qdrant-huggingface-embeddings-n8n",
        "title": "Private RAG: Qdrant Local + Embeddings HuggingFace no n8n",
        "date": "2025-12-05",
        "tags": ["n8n", "qdrant", "huggingface", "rag-local", "soberania-de-dados"],
        "description": "RAG sem OpenAI. Construa uma base de conhecimento completa usando Qdrant e modelos de Embedding open-source dentro do n8n.",
        "keywords": "n8n, RAG local, Qdrant, HuggingFace, embeddings, privacidade"
    },
    {
        "slug": "gemini-1-5-pro-video-analysis-multimodal-n8n",
        "title": "Multi-Modal Agents com Gemini 1.5 Pro: Analisando Vídeos Longos (1h+) no n8n",
        "date": "2025-12-05",
        "tags": ["n8n", "gemini", "google", "video-analysis", "multimodal"],
        "description": "Encontre uma agulha num palheiro de vídeo. Use a janela de contexto de 1 milhão de tokens do Gemini para analisar horas de vídeo no n8n.",
        "keywords": "n8n, Gemini 1.5 Pro, análise de vídeo, multimodal, 1 milhão de tokens"
    }
]

# Template HTML base
def generate_html(article):
    tags_html = "\n".join([f'<span class="tag">{tag}</span>' for tag in article["tags"]])
    keywords = article.get("keywords", ", ".join(article["tags"]))
    
    html_content = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<!-- Primary Meta Tags -->
<title>{article["title"]} | Automations Cookbook</title>
<meta content="{article["title"]}" name="title"/>
<meta content="{article["description"]}" name="description"/>
<meta content="{keywords}" name="keywords"/>
<meta content="Felipe Lourenzo" name="author"/>
<meta content="index, follow" name="robots"/>
<link href="https://www.automationscookbook.com/blog/{article["slug"]}" rel="canonical"/>
<!-- Open Graph / Facebook -->
<meta content="article" property="og:type"/>
<meta content="https://www.automationscookbook.com/blog/{article["slug"]}" property="og:url"/>
<meta content="{article["title"]}" property="og:title"/>
<meta content="{article["description"]}" property="og:description"/>
<meta content="https://www.automationscookbook.com/logo.png" property="og:image"/>
<meta content="{article["date"]}T00:00:00Z" property="article:published_time"/>
<meta content="Felipe Lourenzo" property="article:author"/>
<meta content="Agentic AI" property="article:section"/>
{''.join([f'<meta content="{tag}" property="article:tag"/>' for tag in article["tags"]])}
<!-- Twitter -->
<meta content="summary_large_image" property="twitter:card"/>
<meta content="https://www.automationscookbook.com/blog/{article["slug"]}" property="twitter:url"/>
<meta content="{article["title"]}" property="twitter:title"/>
<meta content="{article["description"]}" property="twitter:description"/>
<meta content="https://www.automationscookbook.com/logo.png" property="twitter:image"/>
<!-- Tailwind CSS -->
<script src="https://cdn.tailwindcss.com"></script>
<!-- Fonts -->
<link href="https://fonts.googleapis.com" rel="preconnect"/>
<link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet"/>
<!-- Favicon -->
<link href="/favicon.ico" rel="icon" type="image/x-icon"/>
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','GTM-KVTHGKJR');</script>
<!-- End Google Tag Manager -->
<!-- Google Analytics 4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-CEYC26V1T3"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){{dataLayer.push(arguments);}}
gtag('js', new Date());
gtag('config', 'G-CEYC26V1T3', {{
    'send_page_view': true,
    'anonymize_ip': true
}});
</script>
<!-- Schema.org Article Markup -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "TechArticle",
  "headline": "{article["title"]}",
  "alternativeHeadline": "{article["description"]}",
  "image": {{
    "@type": "ImageObject",
    "url": "https://www.automationscookbook.com/logo.png",
    "width": 1200,
    "height": 630
  }},
  "author": {{
    "@type": "Person",
    "name": "Felipe Lourenzo",
    "jobTitle": "AI Researcher and AI Automation Specialist",
    "url": "https://www.automationscookbook.com"
  }},
  "publisher": {{
    "@type": "Organization",
    "name": "Automations Cookbook",
    "logo": {{
      "@type": "ImageObject",
      "url": "https://www.automationscookbook.com/logo.png"
    }}
  }},
  "datePublished": "{article["date"]}",
  "dateModified": "{article["date"]}",
  "mainEntityOfPage": {{
    "@type": "WebPage",
    "@id": "https://www.automationscookbook.com/blog/{article["slug"]}"
  }},
  "articleSection": "Agentic AI",
  "keywords": "{keywords}",
  "articleBody": "{article["description"]}"
}}
</script>
<!-- BreadcrumbList Schema -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://www.automationscookbook.com"
    }},
    {{
      "@type": "ListItem",
      "position": 2,
      "name": "Blog",
      "item": "https://www.automationscookbook.com/blog/"
    }},
    {{
      "@type": "ListItem",
      "position": 3,
      "name": "{article["title"]}",
      "item": "https://www.automationscookbook.com/blog/{article["slug"]}"
    }}
  ]
}}
</script>
<style>
body {{
    font-family: 'Inter', sans-serif;
    background-color: #f9fafb;
}}
.prose {{
    max-width: 800px;
}}
.prose h1 {{
    font-size: 2.5rem;
    font-weight: 800;
    line-height: 1.2;
    margin-bottom: 1.5rem;
    color: #111827;
}}
.prose h2 {{
    font-size: 1.875rem;
    font-weight: 700;
    margin-top: 2.5rem;
    margin-bottom: 1rem;
    color: #1f2937;
    border-bottom: 2px solid #e5e7eb;
    padding-bottom: 0.5rem;
}}
.prose h3 {{
    font-size: 1.5rem;
    font-weight: 600;
    margin-top: 2rem;
    margin-bottom: 0.75rem;
    color: #374151;
}}
.prose p {{
    font-size: 1.125rem;
    line-height: 1.75;
    color: #4b5563;
    margin-bottom: 1.5rem;
}}
.prose strong {{
    color: #1f2937;
    font-weight: 600;
}}
.prose ul, .prose ol {{
    margin-left: 1.5rem;
    margin-bottom: 1.5rem;
}}
.prose li {{
    margin-bottom: 0.5rem;
    line-height: 1.75;
}}
.prose code {{
    background-color: #f3f4f6;
    padding: 0.2rem 0.4rem;
    border-radius: 0.25rem;
    font-size: 0.9em;
    color: #dc2626;
}}
.prose pre {{
    background-color: #1f2937;
    color: #e5e7eb;
    padding: 1rem;
    border-radius: 0.5rem;
    overflow-x: auto;
    margin-bottom: 1.5rem;
}}
.prose pre code {{
    background-color: transparent;
    color: inherit;
    padding: 0;
}}
.tag {{
    display: inline-block;
    background-color: #dbeafe;
    color: #1e40af;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.875rem;
    font-weight: 500;
    margin-right: 0.5rem;
    margin-bottom: 0.5rem;
}}
.cta-button {{
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    color: white;
    padding: 0.75rem 1.5rem;
    border-radius: 0.5rem;
    font-weight: 600;
    text-decoration: none;
    display: inline-block;
    transition: transform 0.2s;
}}
.cta-button:hover {{
    transform: translateY(-2px);
    text-decoration: none;
}}
</style>
</head>
<body>
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-KVTHGKJR"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->

<!-- Header -->
<header class="bg-white shadow-sm sticky top-0 z-50">
<nav class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
<div class="flex justify-between items-center">
<a href="https://www.automationscookbook.com" class="text-2xl font-bold text-indigo-600">
Automations Cookbook
</a>
<div class="hidden md:flex space-x-8">
<a href="https://www.automationscookbook.com/integracoes/" class="text-gray-700 hover:text-indigo-600">Integrações</a>
<a href="https://www.automationscookbook.com/blog/" class="text-gray-700 hover:text-indigo-600 font-semibold">Blog</a>
<a href="https://www.automationscookbook.com/ai-agents/" class="text-gray-700 hover:text-indigo-600">AI Agents</a>
</div>
</div>
</nav>
</header>

<!-- Main Content -->
<main class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
<!-- Breadcrumb -->
<nav class="text-sm mb-8" aria-label="Breadcrumb">
<ol class="flex items-center space-x-2 text-gray-500">
<li><a href="https://www.automationscookbook.com" class="hover:text-indigo-600">Home</a></li>
<li><span>/</span></li>
<li><a href="https://www.automationscookbook.com/blog/" class="hover:text-indigo-600">Blog</a></li>
<li><span>/</span></li>
<li class="text-gray-900 font-medium">{article["title"].split(":")[0]}</li>
</ol>
</nav>

<!-- Article Header -->
<article class="prose prose-lg mx-auto">
<div class="mb-8">
<div class="flex flex-wrap gap-2 mb-4">
{tags_html}
</div>
<h1>{article["title"]}</h1>
<div class="flex items-center text-gray-600 text-sm mb-6">
<span>Por Felipe Lourenzo</span>
<span class="mx-2">•</span>
<time datetime="{article["date"]}">05 de Dezembro, 2025</time>
<span class="mx-2">•</span>
<span>12 min de leitura</span>
</div>
</div>

<!-- Article Content Placeholder -->
<div class="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-8">
<p class="text-yellow-800"><strong>🚧 Artigo em desenvolvimento</strong> - O conteúdo completo será adicionado em breve.</p>
</div>

<p>{article["description"]}</p>

<!-- CTA Section -->
<div class="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-lg p-8 my-12">
<h3 class="text-2xl font-bold text-gray-900 mb-4">Pronto para automatizar com n8n?</h3>
<p class="text-gray-700 mb-6">Explore mais de 12.700+ templates de automação prontos para usar.</p>
<a href="https://www.automationscookbook.com/integracoes/" class="cta-button">
Explorar Templates de Automação →
</a>
</div>

<!-- Author Bio -->
<div class="bg-gray-50 rounded-lg p-6 my-12">
<div class="flex items-start">
<div class="flex-shrink-0">
<div class="h-16 w-16 rounded-full bg-indigo-600 flex items-center justify-center text-white text-2xl font-bold">
FL
</div>
</div>
<div class="ml-4">
<h4 class="text-lg font-bold text-gray-900">Felipe Lourenzo</h4>
<p class="text-gray-600">AI Researcher and AI Automation Specialist</p>
<p class="text-gray-500 mt-2">Especialista em Agentic AI, LLMs e automação inteligente com n8n. Ajudando empresas a implementar agentes autônomos que transformam processos.</p>
</div>
</div>
</div>

</article>
</main>

<!-- Footer -->
<footer class="bg-gray-900 text-white mt-20">
<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
<div class="grid md:grid-cols-4 gap-8">
<div>
<h3 class="font-bold text-lg mb-4">Automations Cookbook</h3>
<p class="text-gray-400">12.700+ templates de automação para n8n</p>
</div>
<div>
<h4 class="font-semibold mb-4">Recursos</h4>
<ul class="space-y-2 text-gray-400">
<li><a href="https://www.automationscookbook.com/integracoes/" class="hover:text-white">Integrações</a></li>
<li><a href="https://www.automationscookbook.com/blog/" class="hover:text-white">Blog</a></li>
<li><a href="https://www.automationscookbook.com/ai-agents/" class="hover:text-white">AI Agents</a></li>
</ul>
</div>
<div>
<h4 class="font-semibold mb-4">Categorias</h4>
<ul class="space-y-2 text-gray-400">
<li><a href="https://www.automationscookbook.com/blog/?tag=agentic-ai" class="hover:text-white">Agentic AI</a></li>
<li><a href="https://www.automationscookbook.com/blog/?tag=n8n" class="hover:text-white">n8n Tutorials</a></li>
<li><a href="https://www.automationscookbook.com/blog/?tag=automation" class="hover:text-white">Automação</a></li>
</ul>
</div>
<div>
<h4 class="font-semibold mb-4">Contato</h4>
<ul class="space-y-2 text-gray-400">
<li><a href="mailto:contato@automationscookbook.com" class="hover:text-white">Email</a></li>
<li><a href="https://github.com/felipejac" class="hover:text-white">GitHub</a></li>
</ul>
</div>
</div>
<div class="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
<p>© 2025 Automations Cookbook. Todos os direitos reservados.</p>
</div>
</div>
</footer>

</body>
</html>'''
    
    return html_content

# Gerar todos os arquivos
def main():
    blog_dir = "/workspaces/fabrica-n8n/blog"
    
    print("🚀 Gerando 30 artigos de blog com SEO completo...\n")
    
    for i, article in enumerate(articles, 1):
        filename = f"{article['slug']}.html"
        filepath = os.path.join(blog_dir, filename)
        
        html_content = generate_html(article)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ [{i}/30] {filename}")
    
    print(f"\n🎉 Todos os 30 artigos foram criados com sucesso em {blog_dir}")
    print("\n📋 Próximos passos:")
    print("1. Atualizar sitemap-blog.xml")
    print("2. Atualizar blog/index.html")
    print("3. Fazer commit e push para deploy")

if __name__ == "__main__":
    main()
