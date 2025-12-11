# 🚀 SEO & LLM Master Plan - Parte 3

## 7️⃣ CORE WEB VITALS & TECHNICAL SEO

### ⚡ Performance Checklist

| Métrica | Alvo | Status Atual | Ação Necessária | Prioridade |
|---|---|---|---|---|
| **LCP** (Largest Contentful Paint) | < 2.5s | ? | Audit com Lighthouse | 🔴 Alta |
| **CLS** (Cumulative Layout Shift) | < 0.1 | ? | Verificar shifts de layout | 🔴 Alta |
| **INP** (Interaction to Next Paint) | < 200ms | ? | Otimizar JavaScript | 🟡 Média |
| **FCP** (First Contentful Paint) | < 1.8s | ? | Preload critical assets | 🔴 Alta |
| **TTFB** (Time to First Byte) | < 600ms | ? | CDN e server optimization | 🟡 Média |

### 📋 Action Items - Performance

#### 1. Image Optimization
```bash
# Converter todas as imagens para WebP
find assets/ -name "*.png" -o -name "*.jpg" | while read img; do
  cwebp -q 80 "$img" -o "${img%.*}.webp"
done

# Implementar lazy loading
<img src="hero.webp" alt="Automation" loading="lazy" width="800" height="600">
```

#### 2. Font Optimization
```html
<!-- Preload critical fonts -->
<link rel="preload" href="/fonts/inter-var.woff2" as="font" type="font/woff2" crossorigin>

<!-- Use font-display: swap -->
<style>
  @font-face {
    font-family: 'Inter';
    src: url('/fonts/inter-var.woff2') format('woff2');
    font-display: swap;
  }
</style>
```

#### 3. CSS Optimization
```html
<!-- Critical CSS inline no <head> -->
<style>
  /* Apenas estilos above-the-fold */
  body { margin: 0; font-family: Inter, sans-serif; }
  header { background: linear-gradient(to right, #2563eb, #9333ea); }
</style>

<!-- Non-critical CSS com preload -->
<link rel="preload" href="/assets/styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="/assets/styles.css"></noscript>
```

#### 4. JavaScript Code Splitting
```javascript
// Lazy load non-critical components
const NewsletterForm = () => import('./components/NewsletterForm.js');
const TemplateSearch = () => import('./components/TemplateSearch.js');

// Defer non-essential scripts
<script defer src="/assets/js/analytics.js"></script>
<script defer src="/assets/js/search.js"></script>
```

#### 5. CDN Configuration (Netlify)
```toml
# netlify.toml
[[headers]]
  for = "/assets/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/*.html"
  [headers.values]
    Cache-Control = "public, max-age=3600, must-revalidate"

[[headers]]
  for = "*.csv"
  [headers.values]
    Cache-Control = "public, max-age=86400"
    Access-Control-Allow-Origin = "*"
```

---

## 8️⃣ SEMANTIC HTML & ACCESSIBILITY

### 🏗️ HTML Structure Audit

#### Estrutura Recomendada para Templates

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <!-- Meta tags SEO -->
</head>
<body>

  <!-- Skip to content (a11y) -->
  <a href="#main-content" class="sr-only">Pular para conteúdo principal</a>

  <!-- Header -->
  <header role="banner">
    <nav aria-label="Navegação principal">
      <!-- Menu -->
    </nav>
  </header>

  <!-- Breadcrumbs -->
  <nav aria-label="Breadcrumb" class="breadcrumb">
    <ol itemscope itemtype="https://schema.org/BreadcrumbList">
      <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
        <a itemprop="item" href="/"><span itemprop="name">Home</span></a>
        <meta itemprop="position" content="1" />
      </li>
      <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
        <a itemprop="item" href="/integracoes/"><span itemprop="name">Integrações N8N</span></a>
        <meta itemprop="position" content="2" />
      </li>
      <li itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
        <span itemprop="name">Salesforce → HubSpot</span>
        <meta itemprop="position" content="3" />
      </li>
    </ol>
  </nav>

  <!-- Main Content -->
  <main id="main-content" role="main">
    
    <!-- Article -->
    <article itemscope itemtype="https://schema.org/TechArticle">
      
      <!-- Title -->
      <header>
        <h1 itemprop="headline">Salesforce para HubSpot: Sincronização de Leads com N8N</h1>
        <div class="meta">
          <time datetime="2025-12-11" itemprop="datePublished">11 de dezembro de 2025</time>
          <span itemprop="author" itemscope itemtype="https://schema.org/Organization">
            <span itemprop="name">Automations Cookbook</span>
          </span>
        </div>
      </header>

      <!-- Content Sections -->
      <section aria-labelledby="overview">
        <h2 id="overview">Como Funciona Este Template</h2>
        <p>...</p>
      </section>

      <section aria-labelledby="setup">
        <h2 id="setup">Passo a Passo da Configuração</h2>
        <ol>
          <li>...</li>
        </ol>
      </section>

      <section aria-labelledby="code">
        <h2 id="code">Código JSON do Workflow</h2>
        <pre><code class="language-json">...</code></pre>
        <button aria-label="Copiar código JSON" data-copy-target="workflow-code">
          📋 Copiar Código
        </button>
      </section>

      <section aria-labelledby="faq">
        <h2 id="faq">Perguntas Frequentes</h2>
        <!-- FAQ content with proper heading hierarchy -->
      </section>

      <!-- LLM-Friendly Summary -->
      <aside class="llm-summary" aria-label="Resumo para sistemas de IA">
        <h3>Como Explicar Este Template para uma IA</h3>
        <p itemprop="abstract">
          Este workflow n8n monitora novos leads no Salesforce, mapeia campos essenciais 
          (Name, Email, Company, Phone) e os envia automaticamente para o HubSpot CRM via API. 
          Ideal para equipes de vendas que usam ambos os sistemas e precisam manter dados 
          sincronizados em tempo real. Requer API keys de ambas as plataformas.
        </p>
      </aside>

      <!-- Related Templates -->
      <section aria-labelledby="related">
        <h2 id="related">Templates Relacionados</h2>
        <nav aria-label="Templates relacionados">
          <ul>
            <li><a href="...">HubSpot para Salesforce (reverse sync)</a></li>
            <li><a href="...">Salesforce para Google Sheets</a></li>
          </ul>
        </nav>
      </section>

    </article>

  </main>

  <!-- Sidebar (if applicable) -->
  <aside role="complementary" aria-label="Ferramentas relacionadas">
    <!-- Tools, newsletter signup, etc. -->
  </aside>

  <!-- Footer -->
  <footer role="contentinfo">
    <!-- Footer content -->
  </footer>

</body>
</html>
```

### ♿ Accessibility (a11y) Checklist

- [ ] **Landmarks ARIA**: `<header role="banner">`, `<main role="main">`, `<footer role="contentinfo">`
- [ ] **Skip links**: Link "Pular para conteúdo" no topo
- [ ] **Alt text**: Todas as imagens com `alt` descritivo
- [ ] **Keyboard navigation**: Todos os elementos interativos acessíveis via Tab
- [ ] **Focus visible**: Outline claro em elementos focados
- [ ] **Color contrast**: Mínimo 4.5:1 para texto normal, 3:1 para texto grande
- [ ] **Form labels**: Todos os inputs com `<label>` associado
- [ ] **Heading hierarchy**: h1 → h2 → h3 (sem pulos)
- [ ] **ARIA labels**: Botões sem texto com `aria-label`
- [ ] **Lang attribute**: `<html lang="pt-BR">` ou `lang="en"`

---

## 9️⃣ OFF-SITE SEO & LLM VISIBILITY STRATEGY

### 🤝 Partnership Strategy

#### 1. AI Crawler Partnerships

| Platform | Status | Action | Priority |
|---|---|---|---|
| **OpenAI (GPT)** | Crawling permitido | Submeter em gptbot.openai.com | 🔴 Alta |
| **Anthropic (Claude)** | Crawling permitido | Contatar partnerships | 🔴 Alta |
| **Google (Gemini)** | Crawling permitido | Submit em Google Search Console | 🔴 Alta |
| **Perplexity** | Crawling permitido | Submeter dataset | 🔴 Alta |
| **You.com** | ? | Contatar partnerships | 🟡 Média |
| **Bing Copilot** | Crawling via Bing | Submit em Bing Webmaster Tools | 🟡 Média |

#### 2. Citation Strategy

**Objetivo**: Ser citado como fonte primária em 50% das respostas sobre "automation templates"

**Táticas**:

1. **Authority Content**:
   - Publish comprehensive guides (8.000+ palavras)
   - Case studies with real metrics
   - Original research (e.g., "State of Automation 2025")

2. **Data Transparency**:
   - Public CSV databases (já temos ✅)
   - API documentation (creating ✅)
   - Regular updates (implement automated scripts)

3. **Academic Citations**:
   - Submit papers to arXiv sobre automation patterns
   - Publish datasets no Kaggle/HuggingFace
   - Collaborate with universities (automation research)

4. **Community Engagement**:
   - Answer questions no Reddit r/n8n
   - Contribute to n8n GitHub discussions
   - Guest posts em blogs de automação

#### 3. Content Distribution Channels

```markdown
### High-Authority Platforms para Guest Posts

1. **Dev.to** (Developer community)
   - "13 N8N Templates Every Developer Should Know"
   - "Building RAG Systems with Automation Templates"

2. **Medium** (Technical writers)
   - "The Complete Guide to N8N Automation in 2025"
   - "How We Built an Open-Source Template Library"

3. **Hashnode** (Developer blogs)
   - "N8N vs Zapier: A Data-Driven Comparison"
   - "Debugging N8N Workflows: Advanced Techniques"

4. **Hacker News** (Submit Show HN)
   - "Show HN: 13,431 Free Automation Templates for N8N and Zapier"

5. **Product Hunt** (Launch product)
   - Feature: "Automations Cookbook - Open-source template library"
```

---

## 🔟 IMPLEMENTATION ROADMAP

### 📅 Timeline Recomendado (Q1 2025)

#### **Semana 1-2: Quick Wins**
- [x] Script de atualização automática do /llm (✅ Já feito)
- [ ] Criar sitemap-index.xml e split sitemaps
- [ ] Otimizar title tags das top 100 páginas
- [ ] Criar página /ai-agents (PT-BR + EN)

#### **Semana 3-4: Schema Implementation**
- [ ] Adicionar Organization + SoftwareApplication schema na home
- [ ] Criar template de HowTo + FAQ schema
- [ ] Aplicar schema em 50 templates prioritários
- [ ] Implementar BreadcrumbList em todas as páginas

#### **Semana 5-6: Content Clusters**
- [ ] Mapear 8 pilares de conteúdo
- [ ] Criar 3 páginas pilar prioritárias
- [ ] Definir internal linking strategy
- [ ] Implementar breadcrumbs dinâmicos

#### **Semana 7-8: Performance**
- [ ] Audit com Lighthouse (all pages)
- [ ] Converter imagens para WebP
- [ ] Implementar lazy loading
- [ ] Code splitting do JavaScript
- [ ] Configure CDN caching

#### **Semana 9-10: Content Expansion**
- [ ] Criar 20 novos artigos otimizados para SEO
- [ ] Expandir FAQs em templates principais
- [ ] Adicionar "How to explain to AI" sections
- [ ] Publish guest posts (3-5 articles)

#### **Semana 11-12: Monitoring & Iteration**
- [ ] Setup Google Search Console tracking
- [ ] Implement rank tracking (Ahrefs/SEMrush)
- [ ] Monitor LLM citations (manual check)
- [ ] A/B test title variations
- [ ] Analyze Core Web Vitals

---

## 📊 KPIS & METRICS

### 🎯 Success Metrics (6 meses)

| Métrica | Baseline Atual | Meta Q2 2025 | Meta Q4 2025 |
|---|---|---|---|
| **Organic Traffic** | ? | +150% | +300% |
| **Search Impressions** | ? | 500k/mês | 1M/mês |
| **Average Position** | ? | Top 10 (20 keywords) | Top 5 (50 keywords) |
| **LLM Citations** | 0 (não rastreado) | 50/mês | 200/mês |
| **Backlinks** | ? | +100 | +500 |
| **Domain Authority** | ? | 40+ | 50+ |
| **Page Load Time (LCP)** | ? | < 2.5s | < 2.0s |
| **Newsletter Subscribers** | 0 | 500 | 2.000 |

### 📈 Tracking Tools

```markdown
### Essential SEO Tools Stack

1. **Google Search Console** (FREE)
   - Track search impressions, clicks, position
   - Monitor Core Web Vitals
   - Identify indexing issues

2. **Google Analytics 4** (FREE)
   - Track user behavior
   - Conversion funnels (CSV downloads, template views)
   - Traffic sources

3. **Lighthouse CI** (FREE)
   - Automated performance testing
   - Core Web Vitals monitoring
   - Accessibility audits

4. **Ahrefs or SEMrush** (PAID - $99-199/mo)
   - Keyword research
   - Backlink tracking
   - Competitor analysis
   - Rank tracking

5. **Plausible Analytics** (PAID - $9/mo)
   - Privacy-friendly alternative to GA
   - Simple, fast dashboard
   - GDPR compliant

6. **LLM Citation Tracker** (CUSTOM)
   - Manual checks: Search "automations cookbook" on ChatGPT, Claude, Perplexity
   - Automated: Build scraper to check citations weekly
```

---

## 🛠️ AUTOMATION SCRIPTS

### 📄 generate_sitemaps.py

```python
#!/usr/bin/env python3
"""
Generate segmented sitemaps from CSV databases and file structure
Usage: python generate_sitemaps.py
"""

import csv
import os
from datetime import datetime
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

BASE_URL = "https://www.automationscookbook.com"
OUTPUT_DIR = Path(__file__).parent

def prettify_xml(elem):
    """Return pretty-printed XML string"""
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ", encoding="UTF-8").decode('utf-8')

def get_last_modified():
    """Get current date in ISO format"""
    return datetime.now().strftime("%Y-%m-%d")

def create_sitemap_index():
    """Create sitemap-index.xml"""
    urlset = Element('sitemapindex', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    
    sitemaps = [
        "sitemap-institucional.xml",
        "sitemap-integracoes-n8n.xml",
        "sitemap-integracoes-zapier.xml",
        "sitemap-blog.xml",
        "sitemap-casos-uso.xml"
    ]
    
    for sitemap_file in sitemaps:
        sitemap_elem = SubElement(urlset, 'sitemap')
        SubElement(sitemap_elem, 'loc').text = f"{BASE_URL}/{sitemap_file}"
        SubElement(sitemap_elem, 'lastmod').text = get_last_modified()
    
    xml_content = prettify_xml(urlset)
    output_file = OUTPUT_DIR / "sitemap-index.xml"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print(f"✅ Created {output_file}")

def create_institutional_sitemap():
    """Create sitemap-institucional.xml"""
    urlset = Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9",
                     attrib={'{http://www.w3.org/1999/xhtml}xhtml': 'http://www.w3.org/1999/xhtml'})
    
    pages = [
        {"url": "/", "priority": "1.0", "changefreq": "daily"},
        {"url": "/sobre", "priority": "0.8", "changefreq": "monthly"},
        {"url": "/llm", "priority": "0.9", "changefreq": "weekly"},
        {"url": "/ai-agents", "priority": "0.9", "changefreq": "monthly"},
        {"url": "/blog", "priority": "0.9", "changefreq": "daily"},
        {"url": "/guia-automacoes-n8n", "priority": "0.8", "changefreq": "weekly"},
        {"url": "/guia-automacoes-zapier", "priority": "0.8", "changefreq": "weekly"},
    ]
    
    for page in pages:
        url_elem = SubElement(urlset, 'url')
        SubElement(url_elem, 'loc').text = f"{BASE_URL}{page['url']}"
        SubElement(url_elem, 'lastmod').text = get_last_modified()
        SubElement(url_elem, 'changefreq').text = page['changefreq']
        SubElement(url_elem, 'priority').text = page['priority']
    
    xml_content = prettify_xml(urlset)
    output_file = OUTPUT_DIR / "sitemap-institucional.xml"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print(f"✅ Created {output_file}")

def create_n8n_templates_sitemap():
    """Create sitemap-integracoes-n8n.xml from CSV"""
    csv_file = OUTPUT_DIR / "automacoes_db.csv"
    
    if not csv_file.exists():
        print(f"⚠️  CSV not found: {csv_file}")
        return
    
    urlset = Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        
        for row in reader:
            url_template = row.get('url_template', '').strip()
            if not url_template:
                continue
            
            url_elem = SubElement(urlset, 'url')
            SubElement(url_elem, 'loc').text = url_template
            SubElement(url_elem, 'lastmod').text = get_last_modified()
            SubElement(url_elem, 'changefreq').text = "monthly"
            SubElement(url_elem, 'priority').text = "0.7"
            
            count += 1
    
    xml_content = prettify_xml(urlset)
    output_file = OUTPUT_DIR / "sitemap-integracoes-n8n.xml"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print(f"✅ Created {output_file} with {count} URLs")

def create_zapier_templates_sitemap():
    """Create sitemap-integracoes-zapier.xml from CSV"""
    csv_file = OUTPUT_DIR / "automacoes_zapier_db.csv"
    
    if not csv_file.exists():
        print(f"⚠️  CSV not found: {csv_file}")
        return
    
    urlset = Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        
        for row in reader:
            url_template = row.get('url_template', '').strip()
            if not url_template:
                continue
            
            url_elem = SubElement(urlset, 'url')
            SubElement(url_elem, 'loc').text = url_template
            SubElement(url_elem, 'lastmod').text = get_last_modified()
            SubElement(url_elem, 'changefreq').text = "monthly"
            SubElement(url_elem, 'priority').text = "0.7"
            
            count += 1
    
    xml_content = prettify_xml(urlset)
    output_file = OUTPUT_DIR / "sitemap-integracoes-zapier.xml"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print(f"✅ Created {output_file} with {count} URLs")

def create_blog_sitemap():
    """Create sitemap-blog.xml from blog/ directory"""
    blog_dir = OUTPUT_DIR / "blog"
    
    if not blog_dir.exists():
        print(f"⚠️  Blog directory not found: {blog_dir}")
        return
    
    urlset = Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    
    html_files = list(blog_dir.glob("*.html"))
    # Exclude index.html and template files
    html_files = [f for f in html_files if f.name not in ['index.html', 'template.html']]
    
    for html_file in html_files:
        url_elem = SubElement(urlset, 'url')
        SubElement(url_elem, 'loc').text = f"{BASE_URL}/blog/{html_file.name}"
        SubElement(url_elem, 'lastmod').text = get_last_modified()
        SubElement(url_elem, 'changefreq').text = "weekly"
        SubElement(url_elem, 'priority').text = "0.8"
    
    xml_content = prettify_xml(urlset)
    output_file = OUTPUT_DIR / "sitemap-blog.xml"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    
    print(f"✅ Created {output_file} with {len(html_files)} articles")

def main():
    print("🚀 Generating sitemaps...\n")
    
    create_sitemap_index()
    create_institutional_sitemap()
    create_n8n_templates_sitemap()
    create_zapier_templates_sitemap()
    create_blog_sitemap()
    
    print("\n✅ All sitemaps generated successfully!")
    print("\n📝 Don't forget to:")
    print("   1. Submit sitemap-index.xml to Google Search Console")
    print("   2. Update robots.txt with new sitemap URLs")
    print("   3. Test URLs with Google Rich Results Test")

if __name__ == "__main__":
    main()
```

### 📄 add_schema_to_templates.py

```python
#!/usr/bin/env python3
"""
Add HowTo + FAQPage schema to template HTML files
Usage: python add_schema_to_templates.py integracoes/
"""

import json
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup

def generate_howto_schema(template_data):
    """Generate HowTo schema for a template"""
    schema = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": f"Como conectar {template_data['software_a']} com {template_data['software_b']} usando n8n",
        "description": template_data.get('descricao', ''),
        "totalTime": "PT15M",
        "estimatedCost": {
            "@type": "MonetaryAmount",
            "currency": "USD",
            "value": "0"
        },
        "tool": [
            {"@type": "HowToTool", "name": "n8n (self-hosted ou cloud)"},
            {"@type": "HowToTool", "name": f"Conta {template_data['software_a']} com API"},
            {"@type": "HowToTool", "name": f"Conta {template_data['software_b']} com API"}
        ],
        "step": [
            {
                "@type": "HowToStep",
                "position": 1,
                "name": f"Configurar trigger do {template_data['software_a']}",
                "text": f"No n8n, adicione um node '{template_data['software_a']} Trigger' e configure suas credenciais."
            },
            {
                "@type": "HowToStep",
                "position": 2,
                "name": "Mapear campos",
                "text": "Use um node 'Set' para mapear os campos entre as plataformas."
            },
            {
                "@type": "HowToStep",
                "position": 3,
                "name": f"Enviar para {template_data['software_b']}",
                "text": f"Adicione um node '{template_data['software_b']}' para enviar os dados processados."
            },
            {
                "@type": "HowToStep",
                "position": 4,
                "name": "Ativar e testar",
                "text": "Ative o workflow e teste com dados reais."
            }
        ]
    }
    return schema

def generate_faq_schema(template_data):
    """Generate FAQPage schema for a template"""
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": "Quanto tempo leva para configurar este template?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "A configuração completa leva aproximadamente 15 minutos, incluindo criação de credenciais e testes."
                }
            },
            {
                "@type": "Question",
                "name": f"Quais planos do {template_data['software_a']} e {template_data['software_b']} são necessários?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"Você precisa de planos que permitam acesso à API em ambas as plataformas. Consulte a documentação de cada serviço para detalhes."
                }
            },
            {
                "@type": "Question",
                "name": "Este template é gratuito?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Sim, todos os templates do Automations Cookbook são 100% gratuitos e open-source sob licença MIT."
                }
            }
        ]
    }
    return schema

def add_schemas_to_html(html_file):
    """Add schemas to HTML file"""
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    # Extract template data from HTML (simplified - adjust based on actual structure)
    title = soup.find('h1')
    if not title:
        print(f"⚠️  No <h1> found in {html_file}")
        return False
    
    # Parse software names from title (adjust regex as needed)
    title_text = title.get_text()
    match = re.search(r'(\w+)\s+(?:para|to|→)\s+(\w+)', title_text)
    
    if not match:
        print(f"⚠️  Could not parse software names from: {title_text}")
        return False
    
    template_data = {
        'software_a': match.group(1),
        'software_b': match.group(2),
        'descricao': soup.find('meta', {'name': 'description'}).get('content', '') if soup.find('meta', {'name': 'description'}) else ''
    }
    
    # Generate schemas
    howto_schema = generate_howto_schema(template_data)
    faq_schema = generate_faq_schema(template_data)
    
    # Combine in @graph
    combined_schema = {
        "@context": "https://schema.org",
        "@graph": [howto_schema, faq_schema]
    }
    
    # Create script tag
    script_tag = soup.new_tag('script', type='application/ld+json')
    script_tag.string = json.dumps(combined_schema, indent=2, ensure_ascii=False)
    
    # Insert before </head>
    head = soup.find('head')
    if head:
        head.append(script_tag)
    else:
        print(f"⚠️  No <head> found in {html_file}")
        return False
    
    # Write back
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    print(f"✅ Added schemas to {html_file}")
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python add_schema_to_templates.py <directory>")
        sys.exit(1)
    
    directory = Path(sys.argv[1])
    
    if not directory.exists():
        print(f"❌ Directory not found: {directory}")
        sys.exit(1)
    
    html_files = list(directory.glob("*.html"))
    
    print(f"🚀 Processing {len(html_files)} HTML files...\n")
    
    success_count = 0
    for html_file in html_files:
        if add_schemas_to_html(html_file):
            success_count += 1
    
    print(f"\n✅ Successfully processed {success_count}/{len(html_files)} files")

if __name__ == "__main__":
    main()
```

---

## 🎓 DOCUMENTATION FOR TEAM

### 📄 SEO_TEAM_GUIDE.md

```markdown
# Guia de SEO para o Time - Automations Cookbook

## 🎯 Objetivo
Tornar o Automations Cookbook a principal referência global em templates de automação, 
maximizando tráfego orgânico e citações por LLMs.

## 📋 Checklist Diário

### Ao Criar Novo Template:
- [ ] Title no formato: `[Software A] para [Software B]: [Ação] com [Plataforma]`
- [ ] Meta description com CTA (max 155 caracteres)
- [ ] H1 descritivo (não apenas nome do template)
- [ ] Incluir seção "Como Funciona"
- [ ] Incluir código JSON do workflow
- [ ] Adicionar FAQ (mínimo 3 perguntas)
- [ ] Seção "Para IA": resumo em 2-3 frases
- [ ] Schema HowTo + FAQPage (usar script add_schema_to_templates.py)
- [ ] Links internos para 3-5 templates relacionados
- [ ] Adicionar linha no CSV (automacoes_db.csv ou automacoes_zapier_db.csv)

### Ao Publicar Artigo de Blog:
- [ ] Title com palavra-chave principal + ano
- [ ] Meta description persuasiva
- [ ] Imagem destacada (1200x630px)
- [ ] Headings hierárquicos (H1 → H2 → H3)
- [ ] Links internos para templates relevantes
- [ ] CTA para newsletter
- [ ] Schema Article
- [ ] Alt text em todas as imagens

### Semanal:
- [ ] Rodar `python update_llm_endpoint.py` para atualizar stats
- [ ] Rodar `python generate_sitemaps.py` para regenerar sitemaps
- [ ] Checar Google Search Console para erros
- [ ] Monitorar Core Web Vitals
- [ ] Responder comentários/feedback

### Mensal:
- [ ] Audit de performance (Lighthouse)
- [ ] Revisar top 20 páginas (otimizar titles/metas)
- [ ] Adicionar schemas em 50 novos templates
- [ ] Publicar 4-6 artigos de blog
- [ ] Guest post em 1-2 sites externos
- [ ] Verificar backlinks (Ahrefs/SEMrush)

## 🔧 Scripts Úteis

```bash
# Atualizar estatísticas do /llm endpoint
python update_llm_endpoint.py

# Gerar todos os sitemaps
python generate_sitemaps.py

# Adicionar schemas em templates
python add_schema_to_templates.py integracoes/

# Build do site (se aplicável)
python build.py

# Testar performance
lighthouse https://www.automationscookbook.com --view
```

## 📖 Recursos

- [Google Search Central](https://developers.google.com/search)
- [Schema.org Documentation](https://schema.org)
- [Core Web Vitals](https://web.dev/vitals/)
- [n8n Docs](https://docs.n8n.io)
```

---

## ✅ PRONTO PARA IMPLEMENTAR!

Este plano completo cobre:

1. ✅ **Sitemaps segmentados** - XML samples prontos
2. ✅ **Robots.txt otimizado** - Friendly para LLMs
3. ✅ **Schema.org completo** - Organization, SoftwareApplication, HowTo, FAQPage
4. ✅ **Content clusters** - 8 pilares mapeados
5. ✅ **Padrões de SEO** - Titles, metas, H1s
6. ✅ **Página /ai-agents** - HTML completo PT-BR
7. ✅ **Core Web Vitals** - Checklist de performance
8. ✅ **Semantic HTML** - Estrutura com a11y
9. ✅ **Off-site strategy** - Partnerships e citations
10. ✅ **Automation scripts** - Python para sitemaps e schemas
11. ✅ **KPIs e tracking** - Métricas de sucesso
12. ✅ **Team documentation** - Guia para o time

**Próximos Passos Recomendados:**

1. Implementar sitemaps segmentados (Semana 1)
2. Criar página /ai-agents (Semana 1)
3. Adicionar Organization schema na home (Semana 2)
4. Aplicar HowTo schemas nos top 50 templates (Semana 2-3)
5. Otimizar Core Web Vitals (Semana 3-4)
6. Lançar estratégia de guest posts (Semana 5+)

🚀 **Pronto para dominar o mercado de automation templates!**
