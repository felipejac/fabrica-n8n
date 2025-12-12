# 📊 Google Analytics 4 - Guia de Integração

**Data:** 12 de Dezembro de 2025  
**Site:** automationscookbook.com  
**Status:** Pronto para integração

---

## 🎯 Objetivo

Integrar Google Analytics 4 (GA4) para monitorar:
- Tráfego orgânico (SEO)
- Comportamento do usuário
- Conversões (downloads de templates)
- Engajamento (scroll, tempo na página, FAQ)
- Navegação interna

---

## 🚀 Passo 1: Criar Propriedade GA4

### 1.1 Acessar Google Analytics
```
https://analytics.google.com
```

### 1.2 Criar Conta (se necessário)
1. Clique em **"Administrador"** (⚙️)
2. Clique em **"Criar conta"**
3. Nome da conta: `Automations Cookbook`
4. Configurar compartilhamento de dados (opcional)
5. Clicar em **"Avançar"**

### 1.3 Criar Propriedade
1. Nome da propriedade: `Automations Cookbook - Website`
2. Fuso horário: `(GMT-03:00) Brasília` (ou seu fuso)
3. Moeda: `BRL - Real brasileiro`
4. Clicar em **"Avançar"**

### 1.4 Detalhes da Empresa
1. Setor: **Software e Tecnologia**
2. Tamanho da empresa: **Pequeno (1-10 funcionários)**
3. Clicar em **"Criar"**

### 1.5 Aceitar Termos
1. Ler e aceitar os Termos de Serviço
2. Clicar em **"Aceito"**

---

## 🔑 Passo 2: Obter Measurement ID

### 2.1 Configurar Fluxo de Dados
1. Selecionar plataforma: **Web**
2. URL do site: `https://www.automationscookbook.com`
3. Nome do fluxo: `Automations Cookbook - Main Site`
4. Clicar em **"Criar fluxo"**

### 2.2 Copiar Measurement ID
```
Formato: G-XXXXXXXXXX
Exemplo: G-ABC1234567
```

**IMPORTANTE:** Salve este ID, você precisará dele no próximo passo.

---

## 💻 Passo 3: Integrar no Site

### 3.1 Executar Script de Integração

**Dry-run (simular, sem salvar):**
```bash
cd /workspaces/fabrica-n8n
python integrate_google_analytics.py --measurement-id G-XXXXXXXXXX --dry-run
```

**Produção (aplicar mudanças):**
```bash
cd /workspaces/fabrica-n8n
python integrate_google_analytics.py --measurement-id G-XXXXXXXXXX
```

### 3.2 Verificar Integração
O script irá:
- ✅ Adicionar tag GA4 em todas as páginas HTML
- ✅ Configurar eventos personalizados
- ✅ Preservar páginas que já possuem GA4

**Output esperado:**
```
================================================================================
📊 RESUMO DA INTEGRAÇÃO
================================================================================
Arquivos processados: 12,700+
Arquivos atualizados: 12,700+
Arquivos pulados (já tinham GA4): 0
```

---

## 📊 Passo 4: Configurar Eventos Personalizados

### Eventos Automáticos (já configurados pelo script)

#### 1. Download de Template
**Trigger:** Clique em botão/link de download  
**Nome do evento:** `template_download`  
**Parâmetros:**
- `event_category`: engagement
- `event_label`: URL da página
- `value`: 1

#### 2. Scroll 75%
**Trigger:** Usuário rola 75% da página  
**Nome do evento:** `scroll`  
**Parâmetros:**
- `event_category`: engagement
- `event_label`: 75_percent
- `value`: 75

#### 3. Tempo na Página (2+ minutos)
**Trigger:** Usuário permanece 2 minutos na página  
**Nome do evento:** `time_on_page`  
**Parâmetros:**
- `event_category`: engagement
- `event_label`: 2_minutes
- `value`: 120

#### 4. Navegação Interna
**Trigger:** Clique em links internos  
**Nome do evento:** `internal_navigation`  
**Parâmetros:**
- `event_category`: navigation
- `event_label`: URL do link
- `value`: 1

#### 5. Expansão de FAQ
**Trigger:** Usuário expande item de FAQ  
**Nome do evento:** `faq_expansion`  
**Parâmetros:**
- `event_category`: engagement
- `event_label`: faq_item_X
- `value`: 1

#### 6. Interação com Prompt LLM
**Trigger:** Clique na seção de prompt LLM  
**Nome do evento:** `llm_prompt_interaction`  
**Parâmetros:**
- `event_category`: engagement
- `event_label`: prompt_clicked
- `value`: 1

---

## 🎯 Passo 5: Configurar Conversões

### 5.1 Acessar Conversões
1. No GA4, ir em: **Configuração** → **Eventos**
2. Aguardar 24-48h para eventos aparecerem
3. Clicar em **"Marcar como conversão"** nos eventos:
   - `template_download` (principal conversão)
   - `time_on_page` (engajamento)
   - `scroll` (engajamento)

### 5.2 Definir Valores de Conversão (opcional)
```
template_download: R$ 50,00 (economia de tempo estimada)
time_on_page: R$ 5,00 (engajamento valioso)
scroll: R$ 2,00 (interesse no conteúdo)
```

---

## 📈 Passo 6: Verificar Instalação

### 6.1 Google Analytics Real-Time
1. Acessar: **Relatórios** → **Tempo real**
2. Abrir o site em outra aba: https://www.automationscookbook.com
3. Navegar por algumas páginas
4. Verificar:
   - ✓ Usuário aparece em "Tempo real"
   - ✓ Páginas visitadas aparecem
   - ✓ Eventos são registrados

### 6.2 Google Tag Assistant (extensão Chrome)
```
https://chrome.google.com/webstore/detail/tag-assistant-legacy-by-g/kejbdjndbnbjgmefkgdddjlbokphdefk
```

1. Instalar extensão
2. Abrir o site
3. Clicar no ícone da extensão
4. Verificar: ✓ Google Analytics tag detectada

### 6.3 Console do Navegador
```javascript
// Abrir DevTools (F12)
// Console → executar:
dataLayer

// Deve retornar array com eventos
```

---

## 🔧 Passo 7: Configurações Avançadas

### 7.1 Enhanced Measurement (Recomendado)
**GA4 → Configuração → Fluxos de dados → Seu site → Enhanced measurement**

Ativar:
- ✅ Visualizações de página
- ✅ Rolagens (scrolls)
- ✅ Cliques externos (outbound clicks)
- ✅ Pesquisa no site (se aplicável)
- ✅ Interações com vídeo (se aplicável)
- ✅ Download de arquivos

### 7.2 Filtros Internos (Opcional)
Excluir tráfego interno:
1. **Configuração** → **Fluxos de dados** → **Configurar**
2. **Definir filtros de IP interno**
3. Adicionar IP do escritório/desenvolvimento

### 7.3 User-ID Tracking (Futuro)
Se implementar login de usuários:
```javascript
gtag('config', 'G-XXXXXXXXXX', {
    'user_id': 'USER_ID_HERE'
});
```

---

## 📊 Passo 8: Criar Relatórios Personalizados

### 8.1 Dashboard Principal
**Explorar** → **Criar novo relatório**

**Métricas:**
- Usuários
- Sessões
- Taxa de engajamento
- Conversões (template_download)
- Tempo médio de engajamento

**Dimensões:**
- Fonte/meio de tráfego
- Página de destino
- País
- Dispositivo

### 8.2 Relatório de SEO
**Dimensões:**
- Fonte/meio = `google / organic`
- Query de pesquisa (requer Search Console)

**Métricas:**
- Usuários orgânicos
- Taxa de conversão orgânica
- Páginas mais visitadas via SEO

### 8.3 Relatório de Conversão
**Funil:**
1. Visualização de página (landing)
2. Scroll 75%
3. Tempo na página >2min
4. Download de template

---

## 🔗 Passo 9: Integrar com Google Search Console

### 9.1 Vincular Propriedades
1. GA4 → **Configuração** → **Vínculos do produto**
2. Clicar em **"Vincular Search Console"**
3. Selecionar propriedade: `automationscookbook.com`
4. Confirmar vínculo

### 9.2 Benefícios
- ✅ Queries de busca orgânica no GA4
- ✅ Análise de landing pages
- ✅ CTR e posições médias
- ✅ Correlação de SEO + conversões

---

## 📋 Checklist de Verificação

### Integração Técnica
- [ ] Propriedade GA4 criada
- [ ] Measurement ID copiado
- [ ] Script `integrate_google_analytics.py` executado
- [ ] 12,700+ arquivos HTML atualizados
- [ ] Tag GA4 aparece em "Ver código-fonte"

### Validação
- [ ] Real-Time mostra usuários ativos
- [ ] Eventos personalizados funcionando
- [ ] Tag Assistant detecta GA4
- [ ] dataLayer retorna eventos no console

### Configuração
- [ ] Enhanced Measurement ativado
- [ ] Conversões marcadas (template_download)
- [ ] Filtros de IP configurados (opcional)
- [ ] Search Console vinculado

### Relatórios
- [ ] Dashboard principal criado
- [ ] Relatório de SEO configurado
- [ ] Funil de conversão definido
- [ ] Alertas configurados (quedas de tráfego)

---

## 🎯 Metas de Analytics (30 dias)

### KPIs Primários
- **Usuários únicos:** 10k+/mês
- **Taxa de engajamento:** >60%
- **Conversões (downloads):** 200+/mês
- **Tempo médio de engajamento:** 2:00+

### KPIs de SEO (com GSC vinculado)
- **Tráfego orgânico:** +30% vs baseline
- **CTR orgânico:** 6.5%+
- **Landing pages indexadas:** 12,500+
- **Queries de cauda longa:** 1,000+

---

## 🚨 Troubleshooting

### GA4 não aparece no Real-Time
1. Verificar Measurement ID está correto
2. Limpar cache do navegador
3. Abrir site em modo anônimo
4. Aguardar 5-10 minutos

### Eventos não disparam
1. Abrir DevTools (F12) → Console
2. Verificar erros JavaScript
3. Testar manualmente: `gtag('event', 'test')`
4. Verificar seletores CSS estão corretos

### Múltiplas tags GA4 (duplicação)
```bash
# Remover duplicatas
grep -r "gtag/js?id=" . --include="*.html" | wc -l

# Se >12,700, tem duplicação
# Re-executar script com verificação de duplicatas
```

---

## 📞 Suporte

### Recursos Oficiais
- [GA4 Documentation](https://support.google.com/analytics/answer/9304153)
- [GA4 Events Guide](https://support.google.com/analytics/answer/9267735)
- [GA4 Conversion Setup](https://support.google.com/analytics/answer/9267568)

### Ferramentas de Debug
- Google Tag Assistant
- GA Debugger (extensão Chrome)
- Analytics Debug Mode: `?debug_mode=1`

---

## 🎉 Próximos Passos (Após 7 dias)

### Análise Inicial
1. ☐ Revisar primeiras métricas
2. ☐ Identificar páginas mais visitadas
3. ☐ Analisar fontes de tráfego
4. ☐ Verificar taxa de conversão

### Otimizações
1. ☐ A/B test de CTAs (botões download)
2. ☐ Otimizar landing pages com baixo engajamento
3. ☐ Criar conteúdo para queries populares
4. ☐ Melhorar funil de conversão

---

**Última Atualização:** 12/12/2025, 02:30 UTC  
**Status:** ⏳ Aguardando Measurement ID  
**Próximo Passo:** Criar propriedade GA4 e executar script
