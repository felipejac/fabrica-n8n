
# A/B Testing - Instruções de Implementação

## 📋 Setup

### 1. Adicionar script ao template
Incluir no `template_page.html` (seção Zapier) antes do `</body>`:

```html
<!-- A/B Testing -->
<script src="/assets/js/ab_testing.js"></script>
```

### 2. Configurar Google Analytics 4
No GA4, criar Custom Dimensions:
- **dimension1**: test_id
- **dimension2**: variant
- **dimension3**: template_slug
- **dimension4**: platform

### 3. Atualizar GA ID
Editar `ab_testing_config.json` e substituir:
```json
"analytics_property": "G-XXXXXXXXXX"
```
Com o ID real do Google Analytics.

## 🧪 Testes Implementados

### Teste 1: CTA Button Text
**Objetivo:** Descobrir qual texto gera mais cliques

**Variações:**
- A (33%): "⚡ Abrir no Zapier" + "Configure em 2 minutos"
- B (33%): "⚡ Usar este Zap" + "Começar automação"
- C (34%): "⚡ Começar Agora" + "Economize tempo hoje"

**Métrica primária:** Taxa de cliques no CTA
**Duração:** 14 dias
**Amostra mínima:** 1,000 visualizações

### Teste 2: Platform Comparison Visibility
**Objetivo:** Avaliar impacto de mostrar link para N8N

**Variações:**
- A (33%): Banner amarelo no topo "💡 Prefere código aberto? Veja N8N"
- B (33%): Link sutil no footer "Versão N8N disponível"
- C (34%): Sem cross-link para N8N

**Métrica primária:** Taxa de cliques no CTA Zapier (não N8N)
**Duração:** 21 dias
**Amostra mínima:** 2,000 visualizações

## 📊 Análise de Resultados

### Google Analytics 4
1. **Explorar → Análise de segmento**
2. Filtrar por `test_id` = `cta_button_text`
3. Segmentar por `variant`
4. Comparar evento `zapier_cta_click`

### Fórmula de Significância Estatística
Usar calculadora: https://abtestguide.com/calc/

Exemplo:
- Variant A: 50 cliques / 1000 views = 5% CTR
- Variant B: 65 cliques / 1000 views = 6.5% CTR
- Variant C: 70 cliques / 1000 views = 7% CTR

Se p-value < 0.05 → Diferença é estatisticamente significante

## 🚀 Deployment

### Regenerar páginas com A/B testing
```bash
python build_zapier.py
```

### Verificar implementação
1. Abrir página Zapier no navegador
2. Abrir DevTools → Console
3. Verificar mensagem: "✅ A/B tests initialized"
4. Inspecionar cookies: `ab_test_variant_cta_button_text`

### Monitorar eventos no GA4
1. GA4 → Relatórios → Eventos
2. Buscar eventos: `ab_test_view`, `zapier_cta_click`, `n8n_comparison_click`
3. Aguardar 24-48h para dados aparecerem

## ⚠️ Troubleshooting

### Teste não aparece
- Verificar se script `ab_testing.js` está carregando (Network tab)
- Verificar console por erros JavaScript
- Limpar cookies e tentar novamente

### Eventos não aparecem no GA4
- Verificar se GA4 ID está correto
- Verificar se custom dimensions foram criadas
- Usar GA4 DebugView para real-time testing

### Variações não estão balanceadas
- Aguardar amostra maior (> 100 usuários)
- Verificar se há cache agressivo (Cloudflare)
- Confirmar que cookies estão sendo setados

## 📈 Próximos Passos

Após 14-21 dias:
1. Analisar resultados no GA4
2. Identificar variante vencedora
3. Implementar variante vencedora permanentemente
4. Desabilitar teste em `ab_testing_config.json`
5. Criar novo teste (e.g., guide_layout)

---

**Criado:** 2024
**Revisão:** Semanal durante testes ativos
