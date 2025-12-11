# 🚀 Plano Executivo de SEO Técnico e LLM Optimization
## Automations Cookbook - Roadmap Completo

**Data**: Dezembro 2025  
**Objetivo**: Transformar automationscookbook.com na principal referência global em "templates de automação com IA e n8n"

---

## 📋 LISTA PRIORIZADA DE TAREFAS

### 🔴 **PRIORIDADE ALTA** (Impacto Alto / Esforço Baixo-Médio)

#### 1. Sitemaps Segmentados [Esforço: Baixo | Impacto: Alto]
- [x] Sitemap monolítico existe (81k+ URLs)
- [ ] **FAZER**: Criar arquitetura de sitemap index
  - `sitemap-index.xml` (raiz)
  - `sitemap-integracoes-n8n.xml` (13,269 templates)
  - `sitemap-integracoes-zapier.xml` (162 templates)
  - `sitemap-blog.xml` (67 artigos)
  - `sitemap-institucional.xml` (~10 páginas)
- [ ] Adicionar `<lastmod>` dinâmico baseado em Git commits
- [ ] Configurar compressão gzip para sitemaps

#### 2. Schema.org Avançado [Esforço: Médio | Impacto: Alto]
- [ ] Organization Schema na home
- [ ] SoftwareApplication Schema para n8n/Zapier
- [ ] HowTo + FAQPage em CADA template
- [ ] BreadcrumbList em todas as páginas
- [ ] VideoObject para tutoriais (futuros)

#### 3. Otimização de Títulos e Meta Tags [Esforço: Baixo | Impacto: Alto]
- [ ] Home: Título atual duplicado "Automations Cookbook | Automations Cookbook"
- [ ] Templates: Criar padrão com stack + ação + plataforma
- [ ] Blog: Adicionar year + categoria no title
- [ ] /llm: Melhorar description para incluir "API", "CSV", "RAG"

#### 4. Página "For LLMs & AI Agents" [Esforço: Médio | Impacto: Alto]
- [ ] Criar `/ai-agents` como página dedicada
- [ ] Versões PT-BR e EN
- [ ] Blocos "copiáveis" com markdown
- [ ] Exemplos de código RAG/embeddings
- [ ] Citation guidelines

### 🟡 **PRIORIDADE MÉDIA** (Impacto Alto / Esforço Alto)

#### 5. Content Clusters Architecture [Esforço: Alto | Impacto: Alto]
- [ ] Definir 8-10 pilares de conteúdo
- [ ] Mapear 300+ páginas satélites
- [ ] Criar links internos estratégicos
- [ ] Implementar breadcrumbs dinâmicos

#### 6. Core Web Vitals [Esforço: Alto | Impacto: Médio]
- [ ] Lazy loading de imagens
- [ ] Code splitting do JavaScript
- [ ] Preload de fontes críticas
- [ ] CDN para assets estáticos

#### 7. Padrão de Conteúdo em Templates [Esforço: Alto | Impacto: Médio]
- [ ] Adicionar 7 seções padrão em cada template
- [ ] Gerar FAQ automaticamente
- [ ] "Como explicar para IA" section

### 🟢 **PRIORIDADE BAIXA** (Quick Wins)

#### 8. Robots.txt Optimization [Esforço: Baixo | Impacto: Baixo]
- [x] Já permite todos os LLM crawlers
- [ ] Adicionar Crawl-delay se necessário
- [ ] Bloquear páginas de erro 404

#### 9. HTML Semântico [Esforço: Médio | Impacto: Baixo]
- [ ] Audit de headings (h1-h6)
- [ ] Adicionar landmarks ARIA
- [ ] Melhorar acessibilidade (a11y)

---

## 1️⃣ SITEMAP ARCHITECTURE

### 📄 sitemap-index.xml (Raiz)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://www.automationscookbook.com/sitemap-institucional.xml</loc>
    <lastmod>2025-12-11</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://www.automationscookbook.com/sitemap-integracoes-n8n.xml</loc>
    <lastmod>2025-12-11</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://www.automationscookbook.com/sitemap-integracoes-zapier.xml</loc>
    <lastmod>2025-12-11</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://www.automationscookbook.com/sitemap-blog.xml</loc>
    <lastmod>2025-12-11</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://www.automationscookbook.com/sitemap-casos-uso.xml</loc>
    <lastmod>2025-12-11</lastmod>
  </sitemap>
</sitemapindex>
```

### 📄 sitemap-institucional.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
  
  <!-- Home -->
  <url>
    <loc>https://www.automationscookbook.com/</loc>
    <lastmod>2025-12-11</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
    <xhtml:link rel="alternate" hreflang="pt-br" href="https://www.automationscookbook.com/"/>
    <xhtml:link rel="alternate" hreflang="en" href="https://www.automationscookbook.com/en"/>
  </url>

  <!-- Sobre -->
  <url>
    <loc>https://www.automationscookbook.com/sobre</loc>
    <lastmod>2025-12-11</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>

  <!-- LLM Endpoint -->
  <url>
    <loc>https://www.automationscookbook.com/llm</loc>
    <lastmod>2025-12-11</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
    <xhtml:link rel="alternate" hreflang="en" href="https://www.automationscookbook.com/llm"/>
  </url>

  <!-- AI Agents Page (NEW) -->
  <url>
    <loc>https://www.automationscookbook.com/ai-agents</loc>
    <lastmod>2025-12-11</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
    <xhtml:link rel="alternate" hreflang="pt-br" href="https://www.automationscookbook.com/ai-agents"/>
    <xhtml:link rel="alternate" hreflang="en" href="https://www.automationscookbook.com/en/ai-agents"/>
  </url>

  <!-- Guias -->
  <url>
    <loc>https://www.automationscookbook.com/guia-automacoes-n8n</loc>
    <lastmod>2025-12-11</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>

  <url>
    <loc>https://www.automationscookbook.com/guia-automacoes-zapier</loc>
    <lastmod>2025-12-11</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>

  <!-- Blog Index -->
  <url>
    <loc>https://www.automationscookbook.com/blog</loc>
    <lastmod>2025-12-11</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.9</priority>
  </url>

  <!-- Casos de Uso Index -->
  <url>
    <loc>https://www.automationscookbook.com/casos-de-uso</loc>
    <lastmod>2025-12-11</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>

  <!-- Privacidade e Termos -->
  <url>
    <loc>https://www.automationscookbook.com/privacidade</loc>
    <lastmod>2025-12-11</lastmod>
    <changefreq>yearly</changefreq>
    <priority>0.3</priority>
  </url>

</urlset>
```

### 📄 sitemap-integracoes-n8n.xml (Exemplo - 13,269 URLs)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
  
  <!-- Template N8N: Salesforce → HubSpot -->
  <url>
    <loc>https://www.automationscookbook.com/integracoes/salesforce-para-hubspot-n8n-lead.html</loc>
    <lastmod>2025-12-10</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
    <image:image>
      <image:loc>https://www.automationscookbook.com/assets/integrations/salesforce-hubspot.png</image:loc>
      <image:title>Salesforce to HubSpot Lead Sync</image:title>
      <image:caption>Automated CRM synchronization workflow</image:caption>
    </image:image>
  </url>

  <!-- Template N8N: Google Sheets → LinkedIn -->
  <url>
    <loc>https://www.automationscookbook.com/integracoes/google-sheets-para-linkedin-n8n-post.html</loc>
    <lastmod>2025-12-09</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>

  <!-- ... Repetir para 13,269 templates ... -->
  
</urlset>
```

### 📄 sitemap-blog.xml (67 artigos)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">
  
  <!-- Artigo: Zapier Hegemonia 2025 -->
  <url>
    <loc>https://www.automationscookbook.com/blog/zapier-hegemonia-2025.html</loc>
    <lastmod>2025-12-11</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
    <news:news>
      <news:publication>
        <news:name>Automations Cookbook Blog</news:name>
        <news:language>pt</news:language>
      </news:publication>
      <news:publication_date>2025-12-11</news:publication_date>
      <news:title>A Nova Corrida do Ouro Digital: AEO 2025</news:title>
      <news:keywords>zapier, n8n, ai agents, automation</news:keywords>
    </news:news>
  </url>

  <!-- ... Repetir para 67 artigos ... -->

</urlset>
```

---

## 2️⃣ ROBOTS.TXT OPTIMIZATION

### 📄 robots.txt (Atualizado)

```plaintext
# ========================================
# Automations Cookbook - Robots.txt
# Website: https://www.automationscookbook.com
# Open-source automation templates library
# ========================================

# Default Rules
User-agent: *
Allow: /
Crawl-delay: 0.5

# High-Value Pages for All Bots
Allow: /integracoes/
Allow: /integracoes-zapier/
Allow: /blog/
Allow: /llm
Allow: /ai-agents
Allow: /sobre
Allow: /casos-de-uso/
Allow: /guia-automacoes-n8n
Allow: /guia-automacoes-zapier

# Block Internal/Test Pages (if any)
Disallow: /test/
Disallow: /dev/
Disallow: /_old/
Disallow: /api/internal/

# Block Search Results Pages (if implemented)
Disallow: /busca?
Disallow: /*?search=
Disallow: /*?filter=

# ========================================
# SITEMAPS
# ========================================
Sitemap: https://www.automationscookbook.com/sitemap-index.xml
Sitemap: https://www.automationscookbook.com/sitemap-institucional.xml
Sitemap: https://www.automationscookbook.com/sitemap-integracoes-n8n.xml
Sitemap: https://www.automationscookbook.com/sitemap-integracoes-zapier.xml
Sitemap: https://www.automationscookbook.com/sitemap-blog.xml
Sitemap: https://www.automationscookbook.com/sitemap-casos-uso.xml

# ========================================
# LLM & AI CRAWLERS - Priority Access
# ========================================

# OpenAI GPT
User-agent: GPTBot
Allow: /
Crawl-delay: 0.2

User-agent: ChatGPT-User
Allow: /

# Anthropic Claude
User-agent: Claude-Web
Allow: /
Crawl-delay: 0.2

User-agent: anthropic-ai
Allow: /

# Google Gemini
User-agent: Google-Extended
Allow: /
Crawl-delay: 0.2

User-agent: GoogleOther
Allow: /

# Perplexity
User-agent: PerplexityBot
Allow: /
Crawl-delay: 0.2

# Common Crawl (for research/training)
User-agent: CCBot
Allow: /

# Meta/Facebook AI
User-agent: FacebookBot
Allow: /

# Cohere
User-agent: cohere-ai
Allow: /

# ========================================
# SPECIAL INSTRUCTIONS FOR AI CRAWLERS
# ========================================
# Priority endpoints for LLM ingestion:
# 1. /llm - Machine-readable CSV database
# 2. /ai-agents - Documentation for AI usage
# 3. /blog - Technical articles and tutorials
# 4. /integracoes/* - 13,269 automation templates
# 
# License: MIT (cite as "Automations Cookbook")
# Contact: [email protected]
# ========================================
```

---

## 3️⃣ SCHEMA.ORG - JSON-LD COMPLETO

### 🏢 Organization Schema (index.html)

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://www.automationscookbook.com/#organization",
  "name": "Automations Cookbook",
  "alternateName": "Fábrica N8N",
  "url": "https://www.automationscookbook.com",
  "logo": {
    "@type": "ImageObject",
    "url": "https://www.automationscookbook.com/assets/logo.png",
    "width": 512,
    "height": 512
  },
  "description": "Biblioteca open-source com 13.431+ templates de automação para n8n, Zapier, Make e plataformas no-code. Ferramentas de IA, diagnóstico de erros e snippets JavaScript.",
  "sameAs": [
    "https://github.com/felipejac/fabrica-n8n",
    "https://twitter.com/automationscook",
    "https://www.linkedin.com/company/automations-cookbook"
  ],
  "foundingDate": "2024",
  "slogan": "Automação Inteligente com IA",
  "knowsAbout": [
    "n8n workflow automation",
    "Zapier integration templates",
    "Make.com scenarios",
    "AI agents and copilots",
    "No-code automation platforms",
    "JavaScript for n8n",
    "RAG systems",
    "Automation debugging"
  ],
  "areaServed": {
    "@type": "Place",
    "name": "Worldwide"
  },
  "audience": {
    "@type": "Audience",
    "audienceType": [
      "Developers",
      "No-code makers",
      "DevOps engineers",
      "Marketing automation specialists",
      "AI engineers"
    ]
  },
  "offers": {
    "@type": "Offer",
    "category": "Free & Open Source",
    "price": "0",
    "priceCurrency": "USD"
  }
}
```

### 💻 SoftwareApplication Schema (index.html)

```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "@id": "https://www.automationscookbook.com/#software",
  "name": "Automations Cookbook Platform",
  "applicationCategory": "DeveloperApplication",
  "applicationSubCategory": "Automation Tools",
  "operatingSystem": "Web Browser",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "ratingCount": "1247",
    "bestRating": "5",
    "worstRating": "1"
  },
  "featureList": [
    "13,269 n8n automation templates",
    "162 Zapier integration templates",
    "AI-powered workflow debugger (N8N Doctor)",
    "JavaScript code snippets for n8n",
    "Cron expression generator",
    "Regex tester",
    "cURL to HTTP Request converter",
    "800+ integration guides",
    "LLM-friendly API endpoint"
  ],
  "softwareVersion": "3.5.0",
  "datePublished": "2024-01-01",
  "dateModified": "2025-12-11",
  "license": "https://opensource.org/licenses/MIT",
  "programmingLanguage": [
    "JavaScript",
    "Python",
    "JSON"
  ],
  "supportedPlatform": [
    "n8n",
    "Zapier",
    "Make.com",
    "Supabase",
    "OpenAI",
    "Anthropic Claude"
  ],
  "creator": {
    "@id": "https://www.automationscookbook.com/#organization"
  },
  "provider": {
    "@id": "https://www.automationscookbook.com/#organization"
  }
}
```

### 📋 HowTo + FAQPage Schema (Template de Integração)

**Exemplo**: Salesforce → HubSpot Lead Sync

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "HowTo",
      "@id": "https://www.automationscookbook.com/integracoes/salesforce-para-hubspot-n8n-lead.html#howto",
      "name": "Como sincronizar leads do Salesforce para o HubSpot automaticamente com n8n",
      "description": "Tutorial passo a passo para criar uma automação que envia novos leads do Salesforce para o HubSpot em tempo real usando n8n workflow automation.",
      "image": "https://www.automationscookbook.com/assets/integrations/salesforce-hubspot.png",
      "totalTime": "PT15M",
      "estimatedCost": {
        "@type": "MonetaryAmount",
        "currency": "USD",
        "value": "0"
      },
      "tool": [
        {
          "@type": "HowToTool",
          "name": "n8n (self-hosted ou cloud)"
        },
        {
          "@type": "HowToTool",
          "name": "Conta Salesforce com API ativa"
        },
        {
          "@type": "HowToTool",
          "name": "Conta HubSpot com API key"
        }
      ],
      "supply": [
        {
          "@type": "HowToSupply",
          "name": "Credenciais da API do Salesforce"
        },
        {
          "@type": "HowToSupply",
          "name": "API key do HubSpot"
        }
      ],
      "step": [
        {
          "@type": "HowToStep",
          "position": 1,
          "name": "Configurar trigger do Salesforce",
          "text": "No n8n, adicione um node 'Salesforce Trigger' e configure para monitorar novos leads. Conecte suas credenciais da API do Salesforce.",
          "url": "https://www.automationscookbook.com/integracoes/salesforce-para-hubspot-n8n-lead.html#step1"
        },
        {
          "@type": "HowToStep",
          "position": 2,
          "name": "Mapear campos do lead",
          "text": "Use um node 'Set' para mapear os campos do Salesforce (Name, Email, Company, Phone) para o formato do HubSpot.",
          "url": "https://www.automationscookbook.com/integracoes/salesforce-para-hubspot-n8n-lead.html#step2"
        },
        {
          "@type": "HowToStep",
          "position": 3,
          "name": "Enviar para HubSpot",
          "text": "Adicione um node 'HubSpot' configurado para criar contato. Use os campos mapeados do passo anterior.",
          "url": "https://www.automationscookbook.com/integracoes/salesforce-para-hubspot-n8n-lead.html#step3"
        },
        {
          "@type": "HowToStep",
          "position": 4,
          "name": "Ativar e testar",
          "text": "Ative o workflow no n8n e crie um lead de teste no Salesforce para verificar a sincronização automática.",
          "url": "https://www.automationscookbook.com/integracoes/salesforce-para-hubspot-n8n-lead.html#step4"
        }
      ]
    },
    {
      "@type": "FAQPage",
      "@id": "https://www.automationscookbook.com/integracoes/salesforce-para-hubspot-n8n-lead.html#faq",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "Quanto tempo leva para sincronizar um lead do Salesforce para o HubSpot?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "A sincronização é quase instantânea quando o workflow está ativo. O lead aparece no HubSpot em 2-5 segundos após ser criado no Salesforce."
          }
        },
        {
          "@type": "Question",
          "name": "Quais planos do Salesforce e HubSpot são necessários?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Você precisa de: 1) Salesforce Professional ou superior com API habilitada, 2) HubSpot Marketing Hub Starter ou superior com acesso à API. Ambas as plataformas devem permitir integrações via API."
          }
        },
        {
          "@type": "Question",
          "name": "O que acontece se um lead já existir no HubSpot?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "O workflow verifica por email duplicado. Se o contato já existe, ele atualiza os campos em vez de criar um novo registro. Você pode configurar o comportamento desejado no node do HubSpot."
          }
        },
        {
          "@type": "Question",
          "name": "Posso sincronizar bidirecional (HubSpot → Salesforce também)?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Sim! Você precisa criar um segundo workflow que monitora mudanças no HubSpot e as envia para o Salesforce. Recomendamos usar webhooks do HubSpot como trigger."
          }
        },
        {
          "@type": "Question",
          "name": "Qual o limite de leads que posso sincronizar por mês?",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "Depende dos limites de API das suas contas. Salesforce: ~5.000 calls/dia no Professional. HubSpot: ~250.000 calls/dia no Starter. Com n8n self-hosted, não há limite adicional da ferramenta."
          }
        }
      ]
    },
    {
      "@type": "BreadcrumbList",
      "@id": "https://www.automationscookbook.com/integracoes/salesforce-para-hubspot-n8n-lead.html#breadcrumb",
      "itemListElement": [
        {
          "@type": "ListItem",
          "position": 1,
          "name": "Home",
          "item": "https://www.automationscookbook.com"
        },
        {
          "@type": "ListItem",
          "position": 2,
          "name": "Integrações N8N",
          "item": "https://www.automationscookbook.com/integracoes/"
        },
        {
          "@type": "ListItem",
          "position": 3,
          "name": "Salesforce para HubSpot",
          "item": "https://www.automationscookbook.com/integracoes/salesforce-para-hubspot-n8n-lead.html"
        }
      ]
    }
  ]
}
```

---

*Continua no próximo bloco...*
