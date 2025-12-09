# ✅ Checklist: Registro e Monitoramento em Search Engines

## 📊 Google Search Console (GSC)

### 1. Adicionar Propriedade

**Acesse:** https://search.google.com/search-console

#### Opção A: Domínio (Recomendado)
- ✅ Escolher "Domínio"
- ✅ Digite: `automationscookbook.com`
- ✅ Verificação via **DNS TXT record**
  - Copie o código TXT fornecido
  - Acesse seu provedor de DNS (Cloudflare, GoDaddy, etc.)
  - Adicione registro TXT em `automationscookbook.com`
  - Aguarde 10-60 min (propagação DNS)
  - Volte ao GSC e clique "Verificar"

#### Opção B: Prefixo do URL (Alternativa)
- ✅ Escolher "Prefixo do URL"
- ✅ Digite: `https://www.automationscookbook.com`
- ✅ Verificação via **Tag HTML**
  - Copie o meta tag fornecido
  - Adicione no `<head>` do `index.html`
  - Faça commit e push
  - Aguarde ~2 min (deploy)
  - Volte ao GSC e clique "Verificar"

---

### 2. Submeter Sitemap

**Status atual:** ✅ Sitemap acessível em `https://www.automationscookbook.com/sitemap.xml`  
**Total de URLs:** 13.276

**Passos:**
1. ✅ No menu lateral do GSC, clique em **"Sitemaps"**
2. ✅ Na seção "Adicionar um novo sitemap", digite:
   ```
   sitemap.xml
   ```
   ou
   ```
   https://www.automationscookbook.com/sitemap.xml
   ```
3. ✅ Clique em **"Enviar"**
4. ✅ Aguarde 10-30 min e verifique status:
   - 🟡 **"Buscado"** → Em processamento
   - 🟢 **"Sucesso"** → Aceito
   - 🔴 **"Erro"** → Verificar logs

---

### 3. Solicitar Indexação Prioritária

**Limite:** 10 URLs/dia por propriedade

**URLs prioritárias para solicitar:**
1. `https://www.automationscookbook.com/`
2. `https://www.automationscookbook.com/sobre`
3. `https://www.automationscookbook.com/llm`
4. `https://www.automationscookbook.com/guia-automacoes-n8n`
5. `https://www.automationscookbook.com/casos-de-uso`
6. `https://www.automationscookbook.com/integracoes/`
7. `https://www.automationscookbook.com/integracoes/crm/`
8. `https://www.automationscookbook.com/integracoes/whatsapp/`
9. `https://www.automationscookbook.com/integracoes/marketing/`
10. `https://www.automationscookbook.com/guia-workflows-crm-whatsapp`

**Passos:**
1. ✅ No menu lateral, clique em **"Inspeção de URL"**
2. ✅ Cole cada URL acima
3. ✅ Clique em **"Solicitar indexação"**
4. ✅ Aguarde ~1-2 min por URL
5. ✅ Repita para as próximas URLs

---

### 4. Monitorar Cobertura (Page Indexing)

**Timeline esperada:**
- **24-48h:** Primeiras páginas indexadas
- **7-14 dias:** Indexação completa
- **Meta:** 10.000+ páginas indexadas (de 13.276)

**Monitoramento:**

#### A. Cobertura / Páginas
- Menu: **"Páginas"** ou **"Cobertura"**
- Verificar:
  - ✅ **Páginas indexadas:** Quantas foram aceitas
  - ⚠️ **Excluídas:** Motivo da exclusão (duplicate, noindex, etc.)
  - ❌ **Erro:** Problemas técnicos

#### B. Desempenho (3-7 dias após indexação)
- Menu: **"Desempenho"**
- Métricas:
  - 📊 **Impressões:** Vezes que apareceu nos resultados
  - 👆 **Cliques:** Acessos vindos do Google
  - 📈 **CTR:** Taxa de clique (cliques/impressões)
  - 📍 **Posição média:** Ranking médio

#### C. Consultas principais
- Aba **"Consultas"** dentro de Desempenho
- Exemplos esperados:
  - "automação n8n"
  - "integração shopify n8n"
  - "webhook para notion n8n"
  - "templates n8n grátis"
  - "como integrar crm whatsapp"

---

### 5. Relatórios Importantes

| Relatório | O que verificar | Frequência |
|-----------|----------------|------------|
| **Páginas** | Indexação, erros, cobertura | Semanal |
| **Desempenho** | CTR, impressões, posição | Semanal |
| **Core Web Vitals** | LCP, FID, CLS | Mensal |
| **Usabilidade em dispositivos móveis** | Erros mobile | Mensal |
| **Links** | Backlinks externos | Mensal |
| **Experiência da página** | HTTPS, mobile-friendly | Trimestral |

---

## 🔷 Bing Webmaster Tools

### 1. Adicionar Site

**Acesse:** https://www.bing.com/webmasters

**Passos:**
1. ✅ Login com conta Microsoft
2. ✅ Clique em **"Adicionar site"**
3. ✅ Digite: `https://www.automationscookbook.com`
4. ✅ Escolha método de verificação:
   - **Opção A:** Meta tag (adicione no `<head>`)
   - **Opção B:** Arquivo XML (faça upload via FTP/deploy)
   - **Opção C:** DNS TXT (igual ao GSC)

---

### 2. Submeter Sitemap

**Passos:**
1. ✅ Menu lateral: **"Sitemaps"**
2. ✅ Digite: `https://www.automationscookbook.com/sitemap.xml`
3. ✅ Clique em **"Submeter"**
4. ✅ Aguarde 24-48h para processamento

---

### 3. Monitorar Indexação

**Relatórios importantes:**

| Relatório | O que verificar |
|-----------|----------------|
| **Páginas Indexadas** | Quantas páginas estão no índice |
| **Rastreamento** | Erros de crawl, páginas bloqueadas |
| **Tráfego de Pesquisa** | Cliques, impressões, CTR |
| **Links de Entrada** | Backlinks descobertos |

---

## 📈 KPIs de Sucesso (30 dias)

| Métrica | Meta |
|---------|------|
| **Páginas indexadas (Google)** | 10.000+ (de 13.276) |
| **Páginas indexadas (Bing)** | 5.000+ (de 13.276) |
| **Impressões/mês (Google)** | 5.000+ |
| **Cliques/mês (Google)** | 100+ |
| **Posição média (top queries)** | < 50 |
| **Queries rankeando** | 50+ |
| **Backlinks externos** | 3+ |

---

## 🔧 Checklist de Manutenção

### Semanal
- [ ] Verificar relatório de indexação no GSC
- [ ] Checar novos erros em "Páginas"
- [ ] Revisar top 10 queries e CTR
- [ ] Solicitar indexação de novas páginas prioritárias

### Mensal
- [ ] Analisar Core Web Vitals
- [ ] Revisar backlinks e menções
- [ ] Atualizar sitemap (se houver novos templates)
- [ ] Comparar desempenho Google vs Bing

### Trimestral
- [ ] Auditoria completa de SEO técnico
- [ ] Revisar conteúdo das páginas pilares
- [ ] Atualizar guias com novos templates
- [ ] Planejar novas categorias/páginas

---

## 🚨 Alertas e Problemas Comuns

### Sitemap rejeitado
**Causa:** URLs inválidas, formato incorreto, sitemap inacessível  
**Solução:** Validar XML, checar HTTP 200, testar no https://validator.w3.org/

### Páginas não indexadas
**Causa:** Noindex, canonical errado, conteúdo duplicado, baixa qualidade  
**Solução:** Inspecionar URL no GSC, revisar meta tags, melhorar conteúdo

### Queda de impressões
**Causa:** Mudança de algoritmo, perda de rankings, sazonalidade  
**Solução:** Analisar queries perdidas, fortalecer backlinks, criar conteúdo

### Erros de rastreamento
**Causa:** Links quebrados, timeout, bloqueio em robots.txt  
**Solução:** Corrigir 404s, otimizar performance, revisar robots.txt

---

## 📚 Recursos Úteis

- **Google Search Central:** https://developers.google.com/search/docs
- **Bing Webmaster Guidelines:** https://www.bing.com/webmasters/help/webmasters-guidelines-30fba23a
- **Schema.org Validator:** https://validator.schema.org/
- **Rich Results Test:** https://search.google.com/test/rich-results
- **Mobile-Friendly Test:** https://search.google.com/test/mobile-friendly
