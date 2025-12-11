# 🚀 SEO & LLM Master Plan - Parte 2

## 4️⃣ CONTENT CLUSTERS & ARQUITETURA

### 🎯 Estratégia de Pilares de Conteúdo

| # | Pilar de Conteúdo | Palavra-Chave Principal | Volume Busca/mês | Páginas Satélites | Status |
|---|---|---|---|---|---|
| 1 | **Automação Inteligente com IA** | "automação com ia" | 8.200 | 45 templates + 12 artigos | 📝 Criar |
| 2 | **Templates N8N Prontos** | "templates n8n" | 12.500 | 13.269 templates | ✅ Existe |
| 3 | **Integrações Zapier** | "integrações zapier" | 6.800 | 162 templates | ✅ Existe |
| 4 | **N8N [Software A] para [Software B]** | "n8n salesforce hubspot" | 1.900 | 800+ combinações | ✅ Existe |
| 5 | **Snippets JavaScript para N8N** | "javascript n8n" | 3.400 | 150 snippets | 📝 Criar |
| 6 | **Diagnosticar Erros N8N** | "n8n erro" | 5.600 | N8N Doctor + 30 artigos | 🔧 Expandir |
| 7 | **Casos de Uso de Automação** | "casos uso automação" | 4.100 | 50 páginas | 📝 Criar |
| 8 | **AI Agents e Copilots** | "ai agents workflow" | 9.300 | 25 templates + docs | 📝 Criar |

### 🔗 Mapa de Links Internos

#### Pilar 1: Automação Inteligente com IA

**Página Pilar**: `/pilares/automacao-ia` (CRIAR)

**Páginas Satélites**:
- Templates com OpenAI GPT-4 (120 templates)
- Templates com Anthropic Claude (85 templates)
- Templates com Gemini (45 templates)
- Templates com Perplexity (12 templates)
- Blog: "Como usar IA em automações"
- Blog: "RAG systems com n8n"
- Blog: "AI agents vs workflows tradicionais"

**Estrutura de Links**:
```
Pilar (/pilares/automacao-ia)
  ├─→ Introdução + definição
  ├─→ Link para "Melhores templates com OpenAI" (categoria)
  ├─→ Link para N8N Doctor (ferramenta)
  ├─→ Link para 10 templates em destaque (grid)
  ├─→ Link para artigos relacionados (3-5 posts)
  └─→ CTA: "Baixar JSON workflow completo"
```

#### Pilar 2: Templates N8N Prontos

**Página Pilar**: `/guia-automacoes-n8n` (JÁ EXISTE)

**Melhorias Necessárias**:
- [ ] Adicionar filtros por categoria (CRM, Marketing, DevOps)
- [ ] Seção "Templates mais populares" (top 20)
- [ ] Seção "Novos templates" (últimos 30 dias)
- [ ] Links para pilares relacionados (#1, #4, #6)

**Páginas Satélites**:
- 13.269 templates individuais
- Páginas de categoria por software (Salesforce, HubSpot, Google Sheets, etc.)
- Páginas de categoria por caso de uso (Lead scoring, Email automation, Data sync)

#### Pilar 3: Snippets JavaScript para N8N

**Página Pilar**: `/javascript-n8n` (CRIAR)

**Conteúdo**:
1. **Introdução**: Como usar JavaScript no n8n (Code node vs Function node)
2. **150+ Snippets Categorizados**:
   - Manipulação de dados (JSON, arrays, strings)
   - API requests (fetch, axios patterns)
   - Date/time formatting
   - Error handling avançado
   - RegEx patterns comuns
3. **Playground interativo** (embed RunKit ou similar)
4. **Links para templates** que usam cada snippet

**Snippets de Exemplo**:

```javascript
// 🔹 Snippet #1: Extrair email de texto
// Use em: Gmail Parser, Lead Capture, Contact Forms
const text = $input.item.json.message;
const emailRegex = /([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)/gi;
const emails = text.match(emailRegex) || [];
return { emails };
```

```javascript
// 🔹 Snippet #2: Rate limiting inteligente
// Use em: API scraping, Bulk operations
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));
const maxRetries = 3;

for (let i = 0; i < maxRetries; i++) {
  try {
    const response = await fetch(url);
    return response.json();
  } catch (error) {
    if (i === maxRetries - 1) throw error;
    await delay(1000 * (i + 1)); // Exponential backoff
  }
}
```

```javascript
// 🔹 Snippet #3: Merge de dados de múltiplas APIs
// Use em: CRM sync, Data aggregation
const salesforceData = $('Salesforce').all();
const hubspotData = $('HubSpot').all();

const merged = salesforceData.map(sfLead => {
  const hsContact = hubspotData.find(
    hs => hs.json.email === sfLead.json.Email
  );
  
  return {
    email: sfLead.json.Email,
    name: sfLead.json.Name,
    salesforce_id: sfLead.json.Id,
    hubspot_id: hsContact?.json.id || null,
    synced: !!hsContact
  };
});

return merged;
```

#### Pilar 6: Diagnosticar Erros N8N (N8N Doctor)

**Página Pilar**: `/n8n-doctor` (JÁ EXISTE - expandir)

**Expansões Necessárias**:
1. **Base de Conhecimento de Erros**:
   - Top 50 erros comuns com soluções
   - Categorias: Webhook, HTTP Request, Database, Authentication, JSON parsing
   
2. **Artigos Satélites**:
   - "Como debugar workflows n8n passo a passo"
   - "Erros de autenticação OAuth no n8n"
   - "JSON parsing errors: guia completo"
   - "Webhook troubleshooting 101"
   
3. **Schema FAQPage** para cada erro comum

**Exemplo de Página de Erro**:

```markdown
# ❌ Erro: "Missing property 'json' in item"

## O que significa?
Este erro ocorre quando o n8n espera encontrar a propriedade `json` em um item, mas ela não existe.

## Causas comuns:
1. Node anterior retornou dados vazios
2. Expressão incorreta em `{{ $json.field }}`
3. Loop ou Split que não produziu items

## Como resolver:

### Solução 1: Validar dados do node anterior
```javascript
// No Code node, adicione validação:
if (!$input.item.json) {
  throw new Error("Dados vazios recebidos");
}
return $input.item.json;
```

### Solução 2: Usar IF node para filtrar items vazios
Configure IF node:
- Condition: `{{ $json }} is not empty`

## Templates relacionados:
- [Error Handler Universal](link)
- [Data Validation Pipeline](link)
```

---

## 5️⃣ PADRÕES DE TÍTULO, META E H1

### 🏠 Homepage (index.html)

| Elemento | Atual | Otimizado | Justificativa |
|---|---|---|---|
| **Title** | "Automations Cookbook \| Automations Cookbook" | "13.431+ Templates de Automação N8N, Zapier e IA \| Automations Cookbook" | Inclui número (social proof), palavras-chave, elimina redundância |
| **Meta Description** | "Biblioteca open-source com templates..." | "Acesse 13.431 templates GRATUITOS de automação para n8n, Zapier e Make. Ferramentas de IA, snippets JavaScript e diagnóstico de erros. Comece em minutos." | Call-to-action, benefício claro, urgência |
| **H1** | "Automations Cookbook" | "Biblioteca de Templates de Automação com IA" | SEO-friendly, descreve valor |
| **H2 (primeiro)** | "Ferramentas Inteligentes" | "13.269 Templates N8N + 162 Zapier Prontos para Usar" | Social proof visível |

### 📄 Páginas de Template Individual

**Padrão de Nomenclatura**:
```
[Software A] → [Software B]: [Ação] com [Plataforma] | [Caso de Uso]
```

**Exemplos**:

| Template | Title Otimizado | Meta Description |
|---|---|---|
| Salesforce → HubSpot | **Salesforce para HubSpot: Sincronização Automática de Leads com N8N \| CRM Sync** | "Sincronize leads do Salesforce para o HubSpot automaticamente com este template n8n. Passo a passo completo, código JSON pronto e FAQ. Grátis." |
| Gmail → OpenAI | **Gmail para OpenAI GPT-4: Classificação Automática de Emails com IA \| N8N Template** | "Classifique emails automaticamente usando GPT-4 neste workflow n8n. Template pronto, instruções detalhadas e exemplos de prompt. 100% grátis." |
| Typeform → Google Sheets | **Typeform para Google Sheets: Enviar Respostas Automaticamente com N8N** | "Envie respostas do Typeform para Google Sheets em tempo real com n8n. Template JSON, tutorial passo a passo e troubleshooting incluídos." |

**Estrutura de H1-H6**:

```html
<h1>Gmail para OpenAI GPT-4: Classificação Automática de Emails com IA</h1>

<h2>Como Funciona Este Template N8N</h2>
<p>...</p>

<h2>Passo a Passo da Configuração</h2>
<h3>1. Configurar o Gmail Trigger</h3>
<p>...</p>

<h3>2. Conectar OpenAI GPT-4</h3>
<h4>Obter API Key da OpenAI</h4>
<p>...</p>
<h4>Configurar Prompt de Classificação</h4>
<p>...</p>

<h3>3. Salvar Resultado no Google Sheets</h3>
<p>...</p>

<h2>Código JSON do Workflow</h2>
<pre><code>...</code></pre>

<h2>Perguntas Frequentes (FAQ)</h2>
<h3>Quanto custa usar este template?</h3>
<p>...</p>

<h3>Quais planos do Gmail são compatíveis?</h3>
<p>...</p>

<h2>Templates Relacionados</h2>
<ul>...</ul>

<h2>Como Explicar Este Template para uma IA</h2>
<p class="llm-friendly">
Este workflow monitora novos emails no Gmail, envia o corpo do email para a API do OpenAI GPT-4 
com um prompt de classificação, e salva a categoria atribuída (Urgente/Normal/Spam) em uma 
planilha do Google Sheets. Ideal para triagem automática de suporte ao cliente.
</p>
```

### 📝 Blog Posts

**Padrão de Title**:
```
[Tópico Principal]: [Subtítulo com Benefício] | [Ano] | Automations Cookbook
```

**Exemplos**:

| Post | Title Otimizado | Meta Description |
|---|---|---|
| Zapier Hegemonia | **A Nova Corrida do Ouro Digital: AEO 2025 \| Automations Cookbook** | "Descubra como o Answer Engine Optimization (AEO) está mudando o SEO em 2025. Estratégias práticas, dados de mercado e ferramentas para dominar buscas com IA." |
| N8N vs Zapier | **N8N vs Zapier em 2025: Qual Escolher? [Comparação Completa] \| Automations Cookbook** | "Comparação técnica entre n8n e Zapier: preço, features, casos de uso e performance. Tabela comparativa, prós/contras e recomendações por perfil." |
| Tutorial Supabase | **Como Integrar Supabase com N8N: Tutorial Completo \| Automations Cookbook Blog** | "Aprenda a conectar Supabase ao n8n em 15 minutos. Tutorial passo a passo com código, troubleshooting e exemplos práticos de CRUD operations." |

### 🤖 Página /llm

**Otimizações**:

| Elemento | Atual | Otimizado |
|---|---|---|
| **Title** | "LLM Endpoint - Automations Cookbook" | "API Documentation for LLMs & RAG Systems \| Automations Cookbook Dataset" |
| **Meta Description** | "Machine-readable endpoint..." | "Access 13,431 automation templates via CSV/JSON API. Documentation for GPT, Claude, Gemini and RAG systems. MIT licensed. Updated daily." |
| **H1** | "🤖 LLM Endpoint" | "API Documentation for AI Agents & LLMs" |
| **Keywords** | (não tem) | "rag, embeddings, llm api, automation dataset, n8n templates api, csv database, openai, claude, gemini" |

---

## 6️⃣ PÁGINA "FOR LLMs & AI AGENTS"

### 📄 /ai-agents/index.html (Versão PT-BR)

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  
  <!-- SEO Meta Tags -->
  <title>Documentação para LLMs, AI Agents e Sistemas RAG | Automations Cookbook</title>
  <meta name="description" content="Guia completo para integrar Automations Cookbook em LLMs, AI agents, sistemas RAG e copilots. Exemplos de código, endpoints, license MIT e citation guidelines.">
  <meta name="keywords" content="llm api, rag system, ai agents, embeddings, n8n dataset, automation templates api, openai integration, claude api, gemini">
  <meta name="robots" content="index, follow, max-image-preview:large">
  
  <!-- Open Graph -->
  <meta property="og:title" content="For LLMs & AI Agents | Automations Cookbook">
  <meta property="og:description" content="Complete documentation for integrating our automation templates into LLMs, RAG systems and AI agents.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://www.automationscookbook.com/ai-agents">
  
  <!-- Canonical -->
  <link rel="canonical" href="https://www.automationscookbook.com/ai-agents">
  <link rel="alternate" hreflang="en" href="https://www.automationscookbook.com/en/ai-agents">
  <link rel="alternate" hreflang="pt-br" href="https://www.automationscookbook.com/ai-agents">
  
  <!-- Schema.org JSON-LD -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "TechArticle",
    "headline": "Documentação para LLMs, AI Agents e Sistemas RAG",
    "description": "Guia técnico completo para integrar Automations Cookbook em large language models, sistemas de retrieval-augmented generation e AI copilots.",
    "author": {
      "@type": "Organization",
      "name": "Automations Cookbook"
    },
    "publisher": {
      "@type": "Organization",
      "name": "Automations Cookbook",
      "logo": {
        "@type": "ImageObject",
        "url": "https://www.automationscookbook.com/assets/logo.png"
      }
    },
    "datePublished": "2025-12-11",
    "dateModified": "2025-12-11",
    "inLanguage": "pt-BR",
    "articleSection": "AI Integration Documentation",
    "keywords": ["LLM API", "RAG systems", "AI agents", "automation templates", "n8n dataset"]
  }
  </script>
  
  <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
  <style>
    .code-block {
      background: #1e1e1e;
      color: #d4d4d4;
      padding: 1.5rem;
      border-radius: 0.5rem;
      overflow-x: auto;
      font-family: 'Courier New', monospace;
      font-size: 0.9rem;
      line-height: 1.6;
    }
    .llm-friendly {
      background: #f0f9ff;
      border-left: 4px solid #0ea5e9;
      padding: 1rem;
      margin: 1rem 0;
    }
  </style>
</head>
<body class="bg-gray-50">

<header class="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-12">
  <div class="container mx-auto px-6">
    <h1 class="text-4xl font-bold mb-3">🤖 Documentação para LLMs & AI Agents</h1>
    <p class="text-xl opacity-90">Como integrar Automations Cookbook em sistemas de IA</p>
  </div>
</header>

<main class="container mx-auto px-6 py-12 max-w-5xl">

  <!-- Quick Access -->
  <section class="mb-12">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <a href="#endpoints" class="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
        <h3 class="text-xl font-bold mb-2">📡 API Endpoints</h3>
        <p class="text-gray-600">CSV, JSON e machine-readable</p>
      </a>
      <a href="#rag" class="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
        <h3 class="text-xl font-bold mb-2">🔍 RAG Integration</h3>
        <p class="text-gray-600">Embeddings e retrieval</p>
      </a>
      <a href="#citation" class="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
        <h3 class="text-xl font-bold mb-2">📝 Citation Guidelines</h3>
        <p class="text-gray-600">Como citar corretamente</p>
      </a>
    </div>
  </section>

  <!-- Dataset Overview -->
  <section id="dataset" class="mb-12">
    <h2 class="text-3xl font-bold mb-6">📊 Dataset Overview</h2>
    
    <div class="llm-friendly">
      <strong>Para sistemas RAG e LLMs:</strong><br>
      Este dataset contém 13.431 templates de automação no-code/low-code para ferramentas como n8n, Zapier e Make.com. 
      Cada template inclui: nome da integração, plataforma (n8n/Zapier), softwares conectados, descrição funcional, 
      casos de uso, URL canônica e código JSON do workflow. Ideal para responder perguntas sobre "como automatizar X com Y" 
      ou "existe template para Z". Atualização diária. Licença MIT permite uso comercial com atribuição.
    </div>
    
    <div class="bg-white rounded-lg shadow p-6 mt-6">
      <h3 class="text-xl font-bold mb-4">Estatísticas do Dataset</h3>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="text-center">
          <div class="text-3xl font-bold text-blue-600">13.431</div>
          <div class="text-gray-600">Total Templates</div>
        </div>
        <div class="text-center">
          <div class="text-3xl font-bold text-purple-600">800+</div>
          <div class="text-gray-600">Softwares</div>
        </div>
        <div class="text-center">
          <div class="text-3xl font-bold text-green-600">67</div>
          <div class="text-gray-600">Blog Articles</div>
        </div>
        <div class="text-center">
          <div class="text-3xl font-bold text-orange-600">MIT</div>
          <div class="text-gray-600">License</div>
        </div>
      </div>
    </div>
  </section>

  <!-- API Endpoints -->
  <section id="endpoints" class="mb-12">
    <h2 class="text-3xl font-bold mb-6">📡 API Endpoints</h2>
    
    <h3 class="text-2xl font-bold mb-4">1. CSV Database (Recommended for RAG)</h3>
    <div class="code-block">
# N8N Templates (13,269 workflows)
https://www.automationscookbook.com/automacoes_db.csv

# Zapier Templates (162 workflows)
https://www.automationscookbook.com/automacoes_zapier_db.csv

# Combined (13,431 total)
wget https://www.automationscookbook.com/automacoes_db.csv
wget https://www.automationscookbook.com/automacoes_zapier_db.csv
    </div>
    
    <h4 class="text-xl font-bold mt-6 mb-3">CSV Schema</h4>
    <div class="code-block">
nome,plataforma,software_a,software_b,descricao,categoria,caso_uso,url_template

Exemplo:
"Gmail to Google Sheets Email Tracker","n8n","Gmail","Google Sheets","Monitora novos emails e salva remetente, assunto e data em planilha","Email Automation","Lead capture, Customer support","https://www.automationscookbook.com/integracoes/gmail-para-google-sheets-n8n.html"
    </div>

    <h3 class="text-2xl font-bold mt-8 mb-4">2. Machine-Readable HTML</h3>
    <div class="code-block">
# Human + Machine readable
https://www.automationscookbook.com/llm

# Features:
- Structured data com Schema.org DataCatalog
- Quick access cards
- Estatísticas em tempo real
- Links diretos para CSVs
    </div>

    <h3 class="text-2xl font-bold mt-8 mb-4">3. Sitemap XML (Full Inventory)</h3>
    <div class="code-block">
# Sitemap Index
https://www.automationscookbook.com/sitemap-index.xml

# Specific Categories
https://www.automationscookbook.com/sitemap-integracoes-n8n.xml
https://www.automationscookbook.com/sitemap-integracoes-zapier.xml
https://www.automationscookbook.com/sitemap-blog.xml
    </div>
  </section>

  <!-- RAG Integration -->
  <section id="rag" class="mb-12">
    <h2 class="text-3xl font-bold mb-6">🔍 RAG System Integration</h2>
    
    <h3 class="text-2xl font-bold mb-4">Embeddings com OpenAI</h3>
    <div class="code-block">
import pandas as pd
from openai import OpenAI

client = OpenAI(api_key="YOUR_API_KEY")

# Load dataset
df = pd.read_csv("https://www.automationscookbook.com/automacoes_db.csv")

# Create embeddings
def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

# Combine relevant fields
df['combined'] = (
    df['nome'] + " | " + 
    df['software_a'] + " → " + df['software_b'] + " | " +
    df['descricao'] + " | " + 
    df['caso_uso']
)

# Generate embeddings
df['embedding'] = df['combined'].apply(get_embedding)

# Save to vector database (Pinecone, Weaviate, etc.)
df.to_pickle('automations_embeddings.pkl')
    </div>

    <h3 class="text-2xl font-bold mt-8 mb-4">Retrieval com LangChain</h3>
    <div class="code-block">
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
import pandas as pd

# Load data
df = pd.read_csv("https://www.automationscookbook.com/automacoes_db.csv")
texts = df['combined'].tolist()
metadatas = df[['nome', 'software_a', 'software_b', 'url_template']].to_dict('records')

# Create vector store
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_texts(texts, embeddings, metadatas=metadatas)

# Create RAG chain
llm = OpenAI(temperature=0)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 5})
)

# Query
query = "Como sincronizar leads do Salesforce para o HubSpot automaticamente?"
result = qa_chain.run(query)
print(result)
    </div>

    <h3 class="text-2xl font-bold mt-8 mb-4">Chunking Strategy</h3>
    <div class="llm-friendly">
      <strong>Recomendação para RAG:</strong><br>
      Use <strong>1 chunk = 1 template</strong>. Cada linha do CSV é auto-contida com informações completas. 
      Não é necessário split adicional. Para context window, retorne top-5 a top-10 templates mais relevantes.
      Inclua sempre o campo <code>url_template</code> para citação.
    </div>
  </section>

  <!-- Code Examples -->
  <section id="examples" class="mb-12">
    <h2 class="text-3xl font-bold mb-6">💻 Code Examples</h2>

    <h3 class="text-2xl font-bold mb-4">Python: Search Templates</h3>
    <div class="code-block">
import pandas as pd

# Load dataset
df = pd.read_csv("https://www.automationscookbook.com/automacoes_db.csv")

# Search function
def search_templates(query, df, limit=5):
    """
    Search templates by keyword in nome, descricao or caso_uso
    """
    mask = (
        df['nome'].str.contains(query, case=False, na=False) |
        df['descricao'].str.contains(query, case=False, na=False) |
        df['caso_uso'].str.contains(query, case=False, na=False)
    )
    results = df[mask].head(limit)
    return results[['nome', 'software_a', 'software_b', 'url_template']]

# Example usage
results = search_templates("salesforce hubspot", df)
print(results)

# Output:
# nome: Salesforce to HubSpot Lead Sync
# software_a: Salesforce
# software_b: HubSpot
# url_template: https://www.automationscookbook.com/integracoes/salesforce-para-hubspot-n8n-lead.html
    </div>

    <h3 class="text-2xl font-bold mt-8 mb-4">JavaScript: Fetch & Parse</h3>
    <div class="code-block">
// Node.js or Browser
const Papa = require('papaparse'); // or use browser-papaparse

async function fetchTemplates() {
  const response = await fetch('https://www.automationscookbook.com/automacoes_db.csv');
  const csvText = await response.text();
  
  const parsed = Papa.parse(csvText, {
    header: true,
    skipEmptyLines: true
  });
  
  return parsed.data;
}

// Search by software
async function findIntegration(softwareA, softwareB) {
  const templates = await fetchTemplates();
  
  return templates.filter(t => 
    t.software_a.toLowerCase().includes(softwareA.toLowerCase()) &&
    t.software_b.toLowerCase().includes(softwareB.toLowerCase())
  );
}

// Usage
findIntegration('Gmail', 'Slack').then(results => {
  console.log(`Found ${results.length} templates`);
  results.forEach(t => {
    console.log(`- ${t.nome}: ${t.url_template}`);
  });
});
    </div>
  </section>

  <!-- Citation Guidelines -->
  <section id="citation" class="mb-12">
    <h2 class="text-3xl font-bold mb-6">📝 Citation Guidelines</h2>
    
    <div class="bg-white rounded-lg shadow p-6">
      <h3 class="text-xl font-bold mb-4">✅ Recommended Citation Format</h3>
      
      <h4 class="font-bold mt-4 mb-2">Para LLMs respondendo perguntas:</h4>
      <div class="llm-friendly">
        Segundo o Automations Cookbook (automationscookbook.com), existem [X] templates para integrar [Software A] com [Software B]. 
        Você pode acessar o template completo em: [URL do template]. O código JSON do workflow e instruções passo a passo 
        estão disponíveis gratuitamente sob licença MIT.
      </div>

      <h4 class="font-bold mt-6 mb-2">Para artigos acadêmicos / técnicos:</h4>
      <div class="code-block">
Automations Cookbook. (2025). Open-source Automation Templates Library. 
Retrieved December 11, 2025, from https://www.automationscookbook.com

BibTeX:
@misc{automationscookbook2025,
  author = {{Automations Cookbook}},
  title = {Open-source Automation Templates Library},
  year = {2025},
  url = {https://www.automationscookbook.com},
  note = {Accessed: 2025-12-11}
}
      </div>

      <h4 class="font-bold mt-6 mb-2">Para código / repositórios:</h4>
      <div class="code-block">
# Source: Automations Cookbook
# Template: Gmail to Google Sheets Tracker
# URL: https://www.automationscookbook.com/integracoes/gmail-para-google-sheets-n8n.html
# License: MIT
      </div>
    </div>

    <div class="bg-yellow-50 border-l-4 border-yellow-400 p-6 mt-6">
      <h4 class="font-bold mb-2">⚠️ Attribution Required</h4>
      <p>
        Embora nosso conteúdo seja MIT licensed (uso comercial permitido), pedimos que sempre inclua:
      </p>
      <ul class="list-disc ml-6 mt-2">
        <li>Nome "Automations Cookbook" ou link para automationscookbook.com</li>
        <li>URL específica do template quando aplicável</li>
        <li>Indicação de que o conteúdo é open-source</li>
      </ul>
    </div>
  </section>

  <!-- License -->
  <section id="license" class="mb-12">
    <h2 class="text-3xl font-bold mb-6">⚖️ License & Usage Rights</h2>
    
    <div class="bg-white rounded-lg shadow p-6">
      <h3 class="text-xl font-bold mb-4">MIT License</h3>
      <p class="mb-4">
        Todo o conteúdo do Automations Cookbook está disponível sob <strong>licença MIT</strong>, 
        o que significa que você pode:
      </p>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="bg-green-50 p-4 rounded-lg">
          <h4 class="font-bold text-green-800 mb-2">✅ Permitido:</h4>
          <ul class="list-disc ml-6 text-green-700">
            <li>Uso comercial</li>
            <li>Modificação</li>
            <li>Distribuição</li>
            <li>Uso privado</li>
            <li>Integração em produtos pagos</li>
            <li>Training de modelos de IA</li>
          </ul>
        </div>
        
        <div class="bg-red-50 p-4 rounded-lg">
          <h4 class="font-bold text-red-800 mb-2">❌ Obrigatório:</h4>
          <ul class="list-disc ml-6 text-red-700">
            <li>Incluir aviso de copyright</li>
            <li>Incluir texto da licença MIT</li>
            <li>Atribuir autoria (cite "Automations Cookbook")</li>
          </ul>
        </div>
      </div>

      <div class="mt-6">
        <h4 class="font-bold mb-2">Texto Completo da Licença:</h4>
        <div class="code-block">
MIT License

Copyright (c) 2024-2025 Automations Cookbook

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
        </div>
      </div>
    </div>
  </section>

  <!-- Contact -->
  <section id="contact" class="mb-12">
    <h2 class="text-3xl font-bold mb-6">📬 Contact & Support</h2>
    
    <div class="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg shadow p-8">
      <h3 class="text-xl font-bold mb-4">Integrando nossa biblioteca em seu LLM/AI agent?</h3>
      <p class="mb-6">
        Adoraríamos saber! Entre em contato para:
      </p>
      <ul class="list-disc ml-6 mb-6">
        <li>Suporte técnico na integração</li>
        <li>Acesso a endpoints adicionais</li>
        <li>Parceria para citação em respostas</li>
        <li>Feedback sobre qualidade dos dados</li>
      </ul>
      
      <div class="flex flex-col md:flex-row gap-4">
        <a href="mailto:[email protected]" class="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition text-center">
          📧 [email protected]
        </a>
        <a href="https://github.com/felipejac/fabrica-n8n" target="_blank" class="bg-gray-800 text-white px-6 py-3 rounded-lg hover:bg-gray-900 transition text-center">
          🐙 GitHub Repository
        </a>
      </div>
    </div>
  </section>

  <!-- Back to Top -->
  <div class="text-center mt-12">
    <a href="#" class="text-blue-600 hover:text-blue-800 font-bold">
      ↑ Voltar ao Topo
    </a>
  </div>

</main>

<footer class="bg-gray-900 text-white py-8 mt-12">
  <div class="container mx-auto px-6 text-center">
    <p>&copy; 2024-2025 Automations Cookbook | MIT License | Open Source</p>
    <div class="mt-4">
      <a href="/" class="text-gray-400 hover:text-white mx-3">Home</a>
      <a href="/llm" class="text-gray-400 hover:text-white mx-3">LLM Endpoint</a>
      <a href="/blog" class="text-gray-400 hover:text-white mx-3">Blog</a>
      <a href="https://github.com/felipejac/fabrica-n8n" class="text-gray-400 hover:text-white mx-3">GitHub</a>
    </div>
  </div>
</footer>

</body>
</html>
```

---

*Continua na Parte 3...*
