
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
