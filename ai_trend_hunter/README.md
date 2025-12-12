# AI Trend Hunter 🤖📈

**Sistema automatizado de análise de tendências em Inteligência Artificial e geração de conteúdo otimizado para SEO/AEO.**

## 🎯 Objetivo

Criar um blog de tecnologia focado em Data Science e IA que:
- Busca dados reais do Hugging Face diariamente
- Analisa tendências de mercado automaticamente
- Gera artigos otimizados para Google (SEO) e Answer Engines como ChatGPT/Perplexity (AEO)

## 🏗️ Arquitetura do Sistema

### Pipeline de 4 Camadas

```
┌─────────────────────────────────────────────────────────────┐
│                    1. DATA LAYER                            │
│  Extração de dados do Hugging Face (top 200 modelos)       │
│  • Downloads, Likes, Licenças, Tags, Última Atualização    │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                  2. ANALYSIS LAYER                          │
│  Análise de tendências e inteligência de dados             │
│  • Hype Ratio (Downloads/Likes)                            │
│  • Segurança Comercial (Licenças)                          │
│  • Saúde do Projeto (Atualização)                          │
│  • 5 Segmentos Editoriais                                  │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                  3. CONTENT LAYER                           │
│  Geração de conteúdo otimizado para AEO                    │
│  • Estrutura de Answer Engine Optimization                 │
│  • Respostas diretas para snippets                         │
│  • Tabelas comparativas                                    │
│  • Listas e bullets                                        │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                  4. OUTPUT LAYER                            │
│  Salvamento com metadados SEO completos                    │
│  • Frontmatter YAML (title, description, tags)             │
│  • Schema.org JSON-LD (TechArticle)                        │
│  • Open Graph e Twitter Cards                              │
│  • Canonical URLs                                          │
└─────────────────────────────────────────────────────────────┘
```

## 📦 Estrutura do Projeto

```
ai_trend_hunter/
├── main.py                    # Orquestrador principal
├── config.py                  # Configurações centralizadas
├── requirements.txt           # Dependências Python
├── README.md                  # Este arquivo
│
├── data/                      # DATA LAYER
│   ├── fetch_market_data.py   # Extração do Hugging Face
│   └── raw_data_*.csv         # Dados brutos salvos
│
├── analysis/                  # ANALYSIS LAYER
│   └── trend_analyzer.py      # Análise de tendências
│
├── content/                   # CONTENT LAYER
│   └── aeo_generator.py       # Geração de conteúdo AEO
│
├── output/                    # OUTPUT LAYER
│   └── seo_manager.py         # Gestão de metadados SEO
│
└── posts/                     # Artigos gerados
    ├── 2025-12-12_relatorio_mensal.md
    ├── 2025-12-12_mito_vs_realidade.md
    └── index.md               # Índice de todos os posts
```

## 🚀 Instalação e Uso

### 1. Instalar Dependências

```bash
cd ai_trend_hunter
pip install -r requirements.txt
```

### 2. Executar o Sistema

```bash
python main.py
```

### 3. Resultado

O sistema irá:
1. ✅ Buscar os top 200 modelos do Hugging Face
2. ✅ Analisar tendências e segmentar pautas
3. ✅ Gerar 5 artigos otimizados em Markdown
4. ✅ Salvar na pasta `posts/` com metadados SEO completos

## 📝 Tipos de Artigos Gerados

### 1. **Mito vs Realidade** (`mito_vs_realidade`)
- Compara modelos com alto Hype Ratio vs baixo
- Identifica ferramentas de produção real vs marketing puro
- Foco: Ajudar empresas a escolher modelos confiáveis

### 2. **Segurança Jurídica** (`seguranca_juridica`)
- Lista modelos com licenças comerciais seguras (MIT, Apache 2.0)
- Explica riscos de licenças restritivas (GPL, CC-BY-NC)
- Foco: Compliance e uso corporativo

### 3. **Cemitério de Projetos** (`cemiterio_projetos`)
- Identifica modelos populares mas abandonados (> 1 ano sem update)
- Analisa causas de abandono
- Sugere alternativas mantidas
- Foco: Gestão de risco técnico

### 4. **Além do ChatGPT** (`alem_chatgpt`)
- Explora modelos de visão, áudio e multimodalidade
- Foca em aplicações práticas (não só chatbots)
- Foco: Diversificação de IA

### 5. **Relatório Mensal** (`relatorio_mensal`)
- Panorama completo do mercado de IA
- Top 30 modelos com estatísticas
- Análise de tendências e previsões
- Foco: Visão estratégica de mercado

## 🎯 Otimizações SEO/AEO

### Answer Engine Optimization (AEO)

Cada artigo é estruturado para ser facilmente compreendido por IAs:

1. **Resposta Direta** no início (para featured snippets)
2. **Estrutura de Listas** (bullets e numeradas)
3. **Tabelas Comparativas** (dados estruturados)
4. **Títulos Descritivos** (H1, H2, H3 hierárquicos)
5. **Linguagem Clara** (evita jargões desnecessários)

### Search Engine Optimization (SEO)

Metadados completos em cada arquivo `.md`:

```yaml
---
title: "Título otimizado para SEO"
description: "Meta description de 155 caracteres"
slug: "url-amigavel"
date: 2025-12-12T10:30:00
tags: ["ai", "machine learning", "data science"]
category: "Análise de Mercado"
keywords: "inteligência artificial, modelos de IA, hugging face"
robots: "index, follow"
og_title: "Título para Open Graph"
og_description: "Descrição para redes sociais"
twitter_card: "summary_large_image"
---
```

### Schema.org JSON-LD

Cada artigo inclui `TechArticle` structured data:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "TechArticle",
  "headline": "Título do Artigo",
  "author": {
    "@type": "Organization",
    "name": "AI Trend Hunter"
  },
  "datePublished": "2025-12-12T10:30:00",
  "wordCount": 2500,
  "keywords": "inteligência artificial, machine learning"
}
</script>
```

## ⚙️ Configuração Avançada

### Arquivo `config.py`

Personalize o comportamento do sistema:

```python
# Número de modelos a buscar
HUGGINGFACE_CONFIG['model_limit'] = 200

# Dias para considerar projeto ativo
ANALYSIS_CONFIG['active_threshold_days'] = 90

# Tópicos a gerar (None = todos)
EXECUTION_CONFIG['topics_to_generate'] = ['relatorio_mensal']

# Modo de execução
EXECUTION_CONFIG['mode'] = 'production'  # ou 'test'
```

### Variáveis de Ambiente (Opcional)

Para funcionalidades futuras (geração com LLM, publicação automática):

```bash
# Hugging Face (para APIs privadas)
export HUGGINGFACE_TOKEN="seu_token_aqui"

# OpenAI (para geração com GPT - futuro)
export OPENAI_API_KEY="sk-..."

# WordPress (para publicação automática - futuro)
export WORDPRESS_URL="https://seublog.com"
export WORDPRESS_USERNAME="admin"
export WORDPRESS_PASSWORD="senha"
```

## 📊 Análise de Dados

### Métricas Calculadas

1. **Hype Ratio** = Downloads / Likes
   - Alto (> 10.000): Ferramenta de produção
   - Baixo (< 100): Marketing forte, pouco uso real

2. **Project Health** (Saúde do Projeto)
   - Muito Ativo: < 30 dias desde update
   - Ativo: 30-90 dias
   - Moderado: 90-180 dias
   - Estagnado: 180-365 dias
   - Abandonado: > 365 dias

3. **Commercial Safety** (Segurança Comercial)
   - Seguro: MIT, Apache 2.0, BSD, Unlicense
   - Restrito: GPL, CC-BY-NC, OpenRAIL
   - Desconhecido: Licença não especificada

## 🔮 Roadmap Futuro

### Fase 2: Geração com LLM
- [ ] Integração com OpenAI GPT-4
- [ ] Integração com Anthropic Claude
- [ ] Prompts especializados por tipo de pauta
- [ ] Geração de imagens com DALL-E/Midjourney

### Fase 3: Publicação Automática
- [ ] Integração com WordPress API
- [ ] Publicação em GitHub Pages
- [ ] Agendamento de posts
- [ ] Sistema de revisão humana

### Fase 4: Analytics e Feedback
- [ ] Tracking de performance (Google Analytics)
- [ ] Análise de CTR e impressões
- [ ] A/B testing de títulos
- [ ] Feedback loop para melhorar geração

### Fase 5: Multicanal
- [ ] Posts para LinkedIn
- [ ] Threads para Twitter/X
- [ ] Newsletter por email
- [ ] Podcast com Text-to-Speech

## 🛠️ Desenvolvimento

### Estrutura Modular

Cada camada é **independente e testável**:

```bash
# Testar DATA LAYER isoladamente
python -m data.fetch_market_data

# Testar ANALYSIS LAYER
python -m analysis.trend_analyzer

# Testar CONTENT LAYER
python -m content.aeo_generator

# Testar OUTPUT LAYER
python -m output.seo_manager
```

### Logs

Logs detalhados salvos em `ai_trend_hunter.log`:

```bash
tail -f ai_trend_hunter.log
```

## 📄 Licença

MIT License - Uso livre para projetos comerciais e open source.

## 🤝 Contribuindo

Pull requests são bem-vindos! Para mudanças maiores:

1. Abra uma issue primeiro
2. Discuta a mudança proposta
3. Fork o repositório
4. Crie sua feature branch
5. Commit suas mudanças
6. Push para a branch
7. Abra um Pull Request

## 📞 Suporte

- 📧 Email: contato@aitrendhunter.com
- 🐦 Twitter: [@aitrendhunter](https://twitter.com/aitrendhunter)
- 💬 Issues: [GitHub Issues](https://github.com/usuario/ai-trend-hunter/issues)

---

**Criado com ❤️ por AI Trend Hunter Bot**

*Última atualização: 12 de Dezembro de 2025*
