#!/usr/bin/env python3
"""
A/B Testing Configuration Generator
Gera variações de páginas Zapier para testes A/B

Testes implementados:
1. CTA Button Text (3 variações)
2. Platform Comparison Visibility (3 variações)
3. Guide Page Layout (3 variações)
"""

import json
import csv
import os

def generate_ab_config():
    """Gera configuração de testes A/B para templates Zapier"""
    
    config = {
        "version": "1.0",
        "enabled": True,
        "tests": [
            {
                "test_id": "cta_button_text",
                "name": "CTA Button Text Optimization",
                "description": "Testar qual texto de CTA gera mais cliques",
                "enabled": True,
                "allocation": {
                    "variant_a": 33,  # 33% tráfego
                    "variant_b": 33,  # 33% tráfego
                    "variant_c": 34   # 34% tráfego
                },
                "variants": {
                    "variant_a": {
                        "name": "Ação Direta",
                        "cta_text": "⚡ Abrir no Zapier",
                        "cta_subtext": "Configure em 2 minutos"
                    },
                    "variant_b": {
                        "name": "Propriedade",
                        "cta_text": "⚡ Usar este Zap",
                        "cta_subtext": "Começar automação"
                    },
                    "variant_c": {
                        "name": "Urgência",
                        "cta_text": "⚡ Começar Agora",
                        "cta_subtext": "Economize tempo hoje"
                    }
                },
                "metrics": {
                    "primary": "cta_click_rate",
                    "secondary": ["time_on_page", "bounce_rate"]
                },
                "duration_days": 14,
                "min_sample_size": 1000
            },
            {
                "test_id": "platform_comparison",
                "name": "Platform Comparison Visibility",
                "description": "Testar visibilidade de links para N8N",
                "enabled": True,
                "allocation": {
                    "variant_a": 33,
                    "variant_b": 33,
                    "variant_c": 34
                },
                "variants": {
                    "variant_a": {
                        "name": "Proeminente",
                        "n8n_link_position": "top",
                        "n8n_banner": True,
                        "banner_text": "💡 Prefere código aberto? Veja a versão N8N",
                        "banner_color": "#FEF3C7"  # Yellow-100
                    },
                    "variant_b": {
                        "name": "Sutil",
                        "n8n_link_position": "footer",
                        "n8n_banner": False,
                        "footer_text": "Versão N8N disponível"
                    },
                    "variant_c": {
                        "name": "Sem Cross-Link",
                        "n8n_link_position": None,
                        "n8n_banner": False
                    }
                },
                "metrics": {
                    "primary": "cta_click_rate",  # CTA principal Zapier
                    "secondary": ["n8n_link_clicks", "conversion_rate"]
                },
                "duration_days": 21,
                "min_sample_size": 2000
            },
            {
                "test_id": "guide_layout",
                "name": "Guide Page Layout",
                "description": "Testar estrutura da página guia Zapier",
                "enabled": False,  # Desabilitado por padrão (requer mudanças maiores)
                "allocation": {
                    "variant_a": 50,
                    "variant_b": 50
                },
                "variants": {
                    "variant_a": {
                        "name": "Current Layout",
                        "structure": ["intro", "comparison_table", "benefits", "use_cases", "faq"]
                    },
                    "variant_b": {
                        "name": "Benefits First",
                        "structure": ["intro", "benefits", "use_cases", "comparison_table", "faq"]
                    }
                },
                "metrics": {
                    "primary": "time_on_page",
                    "secondary": ["scroll_depth", "cta_clicks"]
                },
                "duration_days": 30,
                "min_sample_size": 500
            }
        ],
        "tracking": {
            "analytics_property": "G-XXXXXXXXXX",  # Substituir com GA4 ID real
            "events": {
                "cta_click": "zapier_cta_click",
                "n8n_link_click": "n8n_comparison_click",
                "page_view": "zapier_template_view"
            },
            "custom_dimensions": {
                "test_id": "dimension1",
                "variant": "dimension2",
                "template_slug": "dimension3",
                "platform": "dimension4"
            }
        },
        "implementation": {
            "method": "javascript_client_side",
            "cookie_name": "ab_test_variant",
            "cookie_duration_days": 30,
            "exclude_bots": True
        }
    }
    
    return config


def generate_javascript_ab_code():
    """Gera código JavaScript para implementar A/B tests"""
    
    js_code = """
// ============================================================
// A/B Testing Implementation - Automations Cookbook
// ============================================================

(function() {
    'use strict';
    
    // Configuração dos testes A/B
    const AB_CONFIG = {
        cookieName: 'ab_test_variant',
        cookieDuration: 30, // dias
        tests: {
            cta_button_text: {
                enabled: true,
                allocation: [33, 33, 34], // variant_a, variant_b, variant_c
                variants: {
                    variant_a: {
                        ctaText: '⚡ Abrir no Zapier',
                        ctaSubtext: 'Configure em 2 minutos'
                    },
                    variant_b: {
                        ctaText: '⚡ Usar este Zap',
                        ctaSubtext: 'Começar automação'
                    },
                    variant_c: {
                        ctaText: '⚡ Começar Agora',
                        ctaSubtext: 'Economize tempo hoje'
                    }
                }
            },
            platform_comparison: {
                enabled: true,
                allocation: [33, 33, 34],
                variants: {
                    variant_a: {
                        n8nBanner: true,
                        bannerText: '💡 Prefere código aberto? Veja a versão N8N',
                        bannerPosition: 'top'
                    },
                    variant_b: {
                        n8nBanner: false,
                        footerText: 'Versão N8N disponível'
                    },
                    variant_c: {
                        n8nBanner: false,
                        showN8nLink: false
                    }
                }
            }
        }
    };
    
    // Funções auxiliares
    function setCookie(name, value, days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        const expires = "expires=" + date.toUTCString();
        document.cookie = name + "=" + value + ";" + expires + ";path=/;SameSite=Lax";
    }
    
    function getCookie(name) {
        const nameEQ = name + "=";
        const ca = document.cookie.split(';');
        for(let i = 0; i < ca.length; i++) {
            let c = ca[i];
            while (c.charAt(0) == ' ') c = c.substring(1, c.length);
            if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
        }
        return null;
    }
    
    function isBot() {
        const botPattern = /bot|crawler|spider|crawling|googlebot|bingbot|slurp|duckduckbot/i;
        return botPattern.test(navigator.userAgent);
    }
    
    function assignVariant(testId, allocation) {
        const random = Math.random() * 100;
        let cumulative = 0;
        
        if (random < (cumulative += allocation[0])) return 'variant_a';
        if (random < (cumulative += allocation[1])) return 'variant_b';
        return 'variant_c';
    }
    
    function getOrAssignVariant(testId) {
        // Verificar se já tem variant atribuída
        const existingVariant = getCookie(AB_CONFIG.cookieName + '_' + testId);
        if (existingVariant) {
            return existingVariant;
        }
        
        // Atribuir nova variant
        const test = AB_CONFIG.tests[testId];
        if (!test || !test.enabled) return null;
        
        const variant = assignVariant(testId, test.allocation);
        setCookie(AB_CONFIG.cookieName + '_' + testId, variant, AB_CONFIG.cookieDuration);
        
        return variant;
    }
    
    // Implementação dos testes
    function applyCTAButtonTest() {
        const testId = 'cta_button_text';
        const variant = getOrAssignVariant(testId);
        if (!variant) return;
        
        const variantConfig = AB_CONFIG.tests[testId].variants[variant];
        
        // Aplicar mudanças no CTA
        const ctaButtons = document.querySelectorAll('.zapier-cta, .btn-zapier');
        ctaButtons.forEach(button => {
            button.textContent = variantConfig.ctaText;
            
            // Adicionar subtext se houver
            if (variantConfig.ctaSubtext && !button.querySelector('.cta-subtext')) {
                const subtext = document.createElement('small');
                subtext.className = 'cta-subtext d-block mt-1 opacity-75';
                subtext.textContent = variantConfig.ctaSubtext;
                button.appendChild(subtext);
            }
        });
        
        // Track no Analytics
        if (typeof gtag !== 'undefined') {
            gtag('event', 'ab_test_view', {
                test_id: testId,
                variant: variant,
                page_path: window.location.pathname
            });
        }
    }
    
    function applyPlatformComparisonTest() {
        const testId = 'platform_comparison';
        const variant = getOrAssignVariant(testId);
        if (!variant) return;
        
        const variantConfig = AB_CONFIG.tests[testId].variants[variant];
        
        if (variantConfig.n8nBanner) {
            // Criar banner comparativo
            const banner = document.createElement('div');
            banner.className = 'alert alert-warning d-flex align-items-center mb-4';
            banner.style.backgroundColor = '#FEF3C7';
            banner.style.border = '1px solid #FDE047';
            banner.innerHTML = `
                <div class="flex-grow-1">
                    ${variantConfig.bannerText}
                </div>
                <a href="#" class="btn btn-sm btn-outline-dark ms-3 n8n-comparison-link">
                    Ver N8N
                </a>
            `;
            
            // Inserir no topo do conteúdo
            const mainContent = document.querySelector('.container.mt-5, main');
            if (mainContent && mainContent.firstChild) {
                mainContent.insertBefore(banner, mainContent.firstChild);
            }
            
            // Track cliques no link N8N
            banner.querySelector('.n8n-comparison-link').addEventListener('click', function(e) {
                e.preventDefault();
                
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'n8n_comparison_click', {
                        test_id: testId,
                        variant: variant,
                        page_path: window.location.pathname
                    });
                }
                
                // Redirecionar para página N8N equivalente
                const currentSlug = window.location.pathname.split('/').pop().replace('.html', '');
                const n8nSlug = currentSlug.replace('-zapier', '-n8n');
                window.location.href = `/integracoes/${n8nSlug}.html`;
            });
            
        } else if (variantConfig.footerText) {
            // Adicionar link sutil no footer
            const footer = document.querySelector('footer, .container:last-child');
            if (footer) {
                const footerLink = document.createElement('p');
                footerLink.className = 'text-muted small mt-3';
                footerLink.innerHTML = `
                    <a href="#" class="text-decoration-none n8n-comparison-link">
                        ${variantConfig.footerText} →
                    </a>
                `;
                footer.appendChild(footerLink);
                
                // Track
                footerLink.querySelector('.n8n-comparison-link').addEventListener('click', function(e) {
                    e.preventDefault();
                    
                    if (typeof gtag !== 'undefined') {
                        gtag('event', 'n8n_comparison_click', {
                            test_id: testId,
                            variant: variant,
                            position: 'footer'
                        });
                    }
                    
                    const currentSlug = window.location.pathname.split('/').pop().replace('.html', '');
                    const n8nSlug = currentSlug.replace('-zapier', '-n8n');
                    window.location.href = `/integracoes/${n8nSlug}.html`;
                });
            }
        }
        // variant_c: não faz nada (sem cross-link)
        
        // Track no Analytics
        if (typeof gtag !== 'undefined') {
            gtag('event', 'ab_test_view', {
                test_id: testId,
                variant: variant,
                page_path: window.location.pathname
            });
        }
    }
    
    function trackCTAClicks() {
        // Track todos os cliques em CTAs Zapier
        document.addEventListener('click', function(e) {
            const ctaButton = e.target.closest('.zapier-cta, .btn-zapier');
            if (!ctaButton) return;
            
            if (typeof gtag !== 'undefined') {
                const ctaVariant = getCookie(AB_CONFIG.cookieName + '_cta_button_text');
                const comparisonVariant = getCookie(AB_CONFIG.cookieName + '_platform_comparison');
                
                gtag('event', 'zapier_cta_click', {
                    cta_variant: ctaVariant,
                    comparison_variant: comparisonVariant,
                    page_path: window.location.pathname,
                    button_text: ctaButton.textContent.trim()
                });
            }
        });
    }
    
    // Inicialização
    function init() {
        // Não executar para bots
        if (isBot()) return;
        
        // Verificar se está em página Zapier
        const isZapierPage = window.location.pathname.includes('/integracoes-zapier/');
        if (!isZapierPage) return;
        
        // Aplicar testes
        applyCTAButtonTest();
        applyPlatformComparisonTest();
        trackCTAClicks();
        
        console.log('✅ A/B tests initialized');
    }
    
    // Executar quando DOM estiver pronto
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
"""
    
    return js_code


def save_ab_config():
    """Salva configuração de A/B testing"""
    
    print("🧪 Gerando configuração de A/B Testing...\n")
    
    # Gerar JSON config
    config = generate_ab_config()
    
    with open('ab_testing_config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print("✅ ab_testing_config.json criado")
    
    # Gerar JavaScript
    js_code = generate_javascript_ab_code()
    
    with open('assets/js/ab_testing.js', 'w', encoding='utf-8') as f:
        f.write(js_code)
    
    print("✅ assets/js/ab_testing.js criado")
    
    # Criar arquivo de instruções
    instructions = """
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
"""
    
    with open('AB_TESTING_INSTRUCTIONS.md', 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print("✅ AB_TESTING_INSTRUCTIONS.md criado")
    
    print("\n" + "="*60)
    print("✅ A/B TESTING SETUP CONCLUÍDO!")
    print("="*60)
    print("\n📋 Próximos passos:")
    print("1. Adicionar <script src='/assets/js/ab_testing.js'></script> ao template")
    print("2. Configurar Custom Dimensions no Google Analytics 4")
    print("3. Atualizar GA ID em ab_testing_config.json")
    print("4. Regenerar páginas: python build_zapier.py")
    print("5. Monitorar resultados por 14-21 dias")
    print("\n📖 Veja AB_TESTING_INSTRUCTIONS.md para detalhes completos")
    print("="*60)


if __name__ == "__main__":
    save_ab_config()
