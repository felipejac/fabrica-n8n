# 🤖 Endpoint /llm - Machine-Readable API

## 📍 O que é?

O endpoint `/llm` (https://www.automationscookbook.com/llm) fornece acesso **machine-readable** ao banco de dados completo de templates de automação, otimizado para:

- 🤖 Large Language Models (LLMs)
- 🔍 Sistemas RAG (Retrieval-Augmented Generation)
- 💬 Chatbots e AI Assistants
- 🛠️ Automation Copilots
- 📚 Knowledge Bases

## 📊 Dados Disponíveis

### Templates
- **13,269 templates N8N** → `automacoes_db.csv`
- **162 templates Zapier** → `automacoes_zapier_db.csv`
- **13,431 templates totais**

### Blog
- **67 artigos** sobre automação, IA e no-code
- Tutoriais técnicos
- Análises de mercado
- Guias de ferramentas

## 🔄 Atualização Automática

### Script: `update_llm_endpoint.py`

O script Python atualiza automaticamente as estatísticas no `llm.html`:

```bash
python3 update_llm_endpoint.py
```

**O que ele faz:**
1. ✅ Conta templates N8N em `automacoes_db.csv`
2. ✅ Conta templates Zapier em `automacoes_zapier_db.csv`
3. ✅ Conta artigos do blog em `blog/*.html`
4. ✅ Atualiza todos os números no `llm.html`
5. ✅ Adiciona seção do blog se não existir

### Quando executar?

Execute **sempre que**:
- 📝 Publicar novos artigos no blog
- 🔌 Adicionar templates N8N ou Zapier
- 🚀 Antes de fazer deploy para produção
- 📊 Para verificar estatísticas atuais

## 🛠️ Como Integrar no Workflow

### 1. Manual (Desenvolvimento)

```bash
# Após adicionar templates ou artigos
python3 update_llm_endpoint.py
git add llm.html
git commit -m "chore: atualizar estatísticas do endpoint /llm"
git push
```

### 2. Automatizado (CI/CD)

Adicione ao seu workflow de build:

```yaml
# .github/workflows/deploy.yml
- name: Update LLM Endpoint
  run: python3 update_llm_endpoint.py

- name: Commit changes
  run: |
    git config --local user.email "action@github.com"
    git config --local user.name "GitHub Action"
    git add llm.html
    git diff --staged --quiet || git commit -m "chore: auto-update LLM endpoint stats"
```

### 3. Hook Pre-Commit (Local)

Crie `.git/hooks/pre-commit`:

```bash
#!/bin/bash
python3 update_llm_endpoint.py
git add llm.html
```

## 📈 Estatísticas Atuais

Execute para ver os números atuais:

```bash
python3 update_llm_endpoint.py
```

Output:
```
📊 Estatísticas Atuais:
  N8N Templates: 13,269
  Zapier Templates: 162
  Total Templates: 13,431
  Artigos do Blog: 67
```

## 🔍 O que é Atualizado

O script atualiza os seguintes elementos no `llm.html`:

### Meta Tags
- `<meta name="description">` - Total de templates
- `<meta property="og:description">` - Total de templates

### Seção Intro
- Badge com count de N8N templates
- Badge com count de Zapier templates
- Texto principal com total de templates

### Quick Access Cards
- N8N Database (CSV) - count
- Zapier Database (CSV) - count
- N8N HTML Pages - count
- **Blog Articles (NEW)** - count e link

### Coverage Section
- Total Templates
- N8N Templates
- Zapier Templates
- Software Platforms (87+)

## 🎯 Estrutura de Dados

### Templates (CSV)

```csv
id,software_a,software_b,tipo_evento,caso_de_uso,titulo_pagina,descricao_curta,tags,url
salesforce-para-hubspot-n8n-lead,Salesforce,HubSpot,lead,Sincronização de CRM,...
```

### Blog Articles (HTML)

```
blog/
├── index.html (página principal)
├── artigo-1.html
├── artigo-2.html
└── ... (67 artigos)
```

## 🚀 Casos de Uso

### 1. RAG System

```python
import pandas as pd

# Carregar templates
df = pd.read_csv('https://www.automationscookbook.com/automacoes_db.csv')

# Buscar por software
hubspot_templates = df[
    (df['software_a'].str.contains('HubSpot', case=False)) | 
    (df['software_b'].str.contains('HubSpot', case=False))
]

# Usar em prompt para LLM
context = hubspot_templates.to_json()
```

### 2. AI Assistant

```javascript
// Fetch templates para contexto
const response = await fetch('https://www.automationscookbook.com/automacoes_db.csv');
const templates = await response.text();

// Usar em chatbot
const prompt = `
Based on these automation templates:
${templates}

User question: "How do I sync Salesforce to HubSpot?"
`;
```

### 3. Knowledge Base

```python
# Indexar em vector database (Pinecone, Weaviate, etc)
from langchain.document_loaders import CSVLoader

loader = CSVLoader('automacoes_db.csv')
documents = loader.load()

# Criar embeddings e indexar
# ...
```

## 📝 Manutenção

### Verificar Integridade

```bash
# Contar arquivos manualmente
echo "N8N Templates: $(wc -l < automacoes_db.csv)"
echo "Zapier Templates: $(wc -l < automacoes_zapier_db.csv)"
echo "Blog Articles: $(find blog -name '*.html' ! -name 'email_template_welcome.html' ! -name 'template_page.html' ! -name 'index.html' | wc -l)"
```

### Validar Atualização

Após executar o script, verifique:

```bash
# Ver mudanças
git diff llm.html

# Confirmar números
grep -o '\d\+,\?\d* N8N templates' llm.html
grep -o '\d\+,\?\d* Zapier templates' llm.html
```

## 🔗 Links Úteis

- **Endpoint Live**: https://www.automationscookbook.com/llm
- **N8N Templates**: https://www.automationscookbook.com/integracoes/
- **Zapier Templates**: https://www.automationscookbook.com/integracoes-zapier/
- **Blog**: https://www.automationscookbook.com/blog

## 🆘 Troubleshooting

### Script não encontra CSV

```bash
# Verificar se os arquivos existem
ls -la automacoes_db.csv automacoes_zapier_db.csv
```

### Contagem errada de blog posts

```bash
# Listar arquivos HTML no blog
find blog -name '*.html' -type f ! -name 'email_template_welcome.html' ! -name 'template_page.html'
```

### llm.html não atualizado

```bash
# Verificar permissões
ls -la llm.html

# Executar com verbose
python3 -v update_llm_endpoint.py
```

---

**Última Atualização**: Dezembro 2025  
**Mantido por**: Automations Cookbook Team 🚀
