/**
 * 🌍 AI Factory - i18n Detection & Language Switcher
 * 
 * Sistema completo de internacionalização integrado ao menu
 */

(function() {
    'use strict';
    
    // Configuração
    const CONFIG = {
        defaultLanguage: 'pt',
        supportedLanguages: ['pt', 'en'],
        cookieName: 'ai_factory_language',
        cookieExpiry: 365,
        portugueseRegions: ['BR', 'PT'],
        languageData: {
            pt: { flag: '🇧🇷', name: 'Português', code: 'PT' },
            en: { flag: '🇺🇸', name: 'English', code: 'EN' }
        }
    };

    /**
     * Gerenciamento de Cookies
     */
    function getCookie(name) {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [key, value] = cookie.trim().split('=');
            if (key === name) return value;
        }
        return null;
    }

    function setCookie(name, value, days) {
        const date = new Date();
        date.setDate(date.getDate() + days);
        document.cookie = `${name}=${value}; path=/; expires=${date.toUTCString()}; SameSite=Lax`;
    }

    /**
     * Detecta idioma do navegador
     */
    function getBrowserLanguage() {
        const lang = navigator.language || navigator.userLanguage;
        if (lang) {
            return lang.split('-')[0].toLowerCase();
        }
        return null;
    }

    /**
     * Detecta região via API
     */
    async function detectRegion() {
        try {
            const controller = new AbortController();
            const timeout = setTimeout(() => controller.abort(), 3000);
            
            const response = await fetch('https://ipapi.co/json/', { 
                signal: controller.signal
            });
            
            clearTimeout(timeout);
            
            if (response.ok) {
                const data = await response.json();
                return data.country_code;
            }
        } catch (error) {
            console.log('🌍 Geolocation API timeout, usando fallback');
        }
        return null;
    }

    /**
     * Verifica se deve usar português baseado na região
     */
    function shouldUsePortuguese(region) {
        return region && CONFIG.portugueseRegions.includes(region.toUpperCase());
    }

    /**
     * Detecta idioma preferido
     */
    async function detectLanguage() {
        // 1. Cookie (maior prioridade)
        const cookieLang = getCookie(CONFIG.cookieName);
        if (cookieLang && CONFIG.supportedLanguages.includes(cookieLang)) {
            console.log('🌍 Idioma do cookie:', cookieLang);
            return cookieLang;
        }

        // 2. Região geográfica
        const region = await detectRegion();
        if (region) {
            const lang = shouldUsePortuguese(region) ? 'pt' : 'en';
            console.log(`🌍 Idioma por região (${region}):`, lang);
            return lang;
        }

        // 3. Idioma do navegador
        const browserLang = getBrowserLanguage();
        if (browserLang && CONFIG.supportedLanguages.includes(browserLang)) {
            console.log('🌍 Idioma do navegador:', browserLang);
            return browserLang;
        }

        // 4. Default
        console.log('🌍 Idioma padrão:', CONFIG.defaultLanguage);
        return CONFIG.defaultLanguage;
    }

    /**
     * Obtém idioma atual da URL
     */
    function getCurrentLanguageFromURL() {
        const path = window.location.pathname;
        
        // Verifica se está em /translated/en/
        if (path.includes('/translated/en/')) {
            return 'en';
        }
        
        // Verifica se está em /en/
        if (path.startsWith('/en/')) {
            return 'en';
        }
        
        // Default é português
        return 'pt';
    }

    /**
     * Obtém caminho sem prefixo de idioma
     */
    function getCleanPath() {
        let path = window.location.pathname;
        
        // Remove /translated/en/ se presente
        if (path.includes('/translated/en/')) {
            path = path.replace('/translated/en/', '');
        }
        
        // Remove /en/ se presente
        if (path.startsWith('/en/')) {
            path = path.substring(4);
        }
        
        // Remove barra inicial extra
        if (path.startsWith('//')) {
            path = path.substring(1);
        }
        
        // Se vazio, retorna index.html
        if (!path || path === '/' || path === '/fabrica-n8n/' || path === '/fabrica-n8n') {
            return 'index.html';
        }
        
        // Remove /fabrica-n8n/ se presente (para GitHub Pages)
        if (path.startsWith('/fabrica-n8n/')) {
            path = path.replace('/fabrica-n8n/', '');
        }
        
        return path;
    }

    /**
     * Constrói URL para o idioma especificado
     */
    function buildLanguageURL(lang) {
        const cleanPath = getCleanPath();
        const baseURL = window.location.origin;
        const repoPath = '/fabrica-n8n'; // GitHub Pages
        
        if (lang === 'pt') {
            // Português é o padrão (sem prefixo)
            return `${baseURL}${repoPath}/${cleanPath}`;
        } else {
            // Outros idiomas usam /translated/lang/
            return `${baseURL}${repoPath}/translated/${lang}/${cleanPath}`;
        }
    }

    /**
     * Atualiza UI do seletor de idioma
     */
    function updateLanguageUI(currentLang) {
        const data = CONFIG.languageData[currentLang];
        if (!data) return;
        
        // Atualiza botão principal
        const flagEl = document.getElementById('current-flag');
        const langEl = document.getElementById('current-lang');
        
        if (flagEl) flagEl.textContent = data.flag;
        if (langEl) langEl.textContent = data.code;
        
        // Marca opção ativa no menu
        document.querySelectorAll('.language-option').forEach(option => {
            const optionLang = option.getAttribute('data-lang');
            if (optionLang === currentLang) {
                option.classList.add('bg-slate-100', 'font-semibold');
                
                // Adiciona checkmark se não existir
                if (!option.innerHTML.includes('✓')) {
                    const textSpan = option.querySelector('span:last-child');
                    if (textSpan) {
                        textSpan.innerHTML += ' <span class="text-indigo-600">✓</span>';
                    }
                }
            } else {
                option.classList.remove('bg-slate-100', 'font-semibold');
                
                // Remove checkmark
                const checkmark = option.querySelector('.text-indigo-600');
                if (checkmark) checkmark.remove();
            }
        });
    }

    /**
     * Muda idioma e redireciona
     */
    window.changeLanguage = function(lang) {
        if (!CONFIG.supportedLanguages.includes(lang)) {
            console.error('Idioma não suportado:', lang);
            return;
        }
        
        // Marca escolha manual
        sessionStorage.setItem('manual_language_choice', 'true');
        
        // Salva no cookie
        setCookie(CONFIG.cookieName, lang, CONFIG.cookieExpiry);
        
        // Fecha menu
        const menu = document.getElementById('language-menu');
        if (menu) menu.classList.add('hidden');
        
        // Verifica se já está no idioma correto
        const currentLang = getCurrentLanguageFromURL();
        if (currentLang === lang) {
            console.log('✅ Já está no idioma:', lang);
            updateLanguageUI(lang);
            return;
        }
        
        // Redireciona
        const newURL = buildLanguageURL(lang);
        console.log('🔄 Redirecionando para:', newURL);
        
        // Adiciona feedback visual
        const button = document.getElementById('language-toggle');
        if (button) {
            button.classList.add('opacity-50', 'pointer-events-none');
            button.innerHTML = '<span>🔄</span><span class="hidden sm:inline">...</span>';
        }
        
        window.location.href = newURL;
    };

    /**
     * Toggle do menu de idiomas
     */
    window.toggleLanguageMenu = function(e) {
        if (e) e.stopPropagation();
        
        const menu = document.getElementById('language-menu');
        if (!menu) return;
        
        menu.classList.toggle('hidden');
    };

    /**
     * Fecha menu ao clicar fora
     */
    function setupClickOutside() {
        document.addEventListener('click', (e) => {
            const container = document.getElementById('language-selector-container');
            const menu = document.getElementById('language-menu');
            
            if (!container || !menu) return;
            
            // Se clicou fora do container, fecha o menu
            if (!container.contains(e.target)) {
                menu.classList.add('hidden');
            }
        });
        
        // Fecha ao pressionar ESC
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                const menu = document.getElementById('language-menu');
                if (menu) menu.classList.add('hidden');
            }
        });
    }

    /**
     * Auto-detecção e redirecionamento inicial
     */
    async function autoDetectAndRedirect() {
        // Detecta idioma preferido
        const detectedLang = await detectLanguage();
        
        // Obtém idioma atual da URL
        const currentLang = getCurrentLanguageFromURL();
        
        // Atualiza UI
        updateLanguageUI(currentLang);
        
        // Se detectou idioma diferente do atual, redireciona automaticamente
        // apenas na primeira visita (sem escolha manual)
        const hasManualChoice = sessionStorage.getItem('manual_language_choice');
        
        if (!hasManualChoice && detectedLang !== currentLang) {
            console.log(`🔄 Auto-redirecionando de ${currentLang} para ${detectedLang}`);
            
            // Salva no cookie
            setCookie(CONFIG.cookieName, detectedLang, CONFIG.cookieExpiry);
            
            // Redireciona
            const newURL = buildLanguageURL(detectedLang);
            window.location.href = newURL;
        } else {
            // Salva o idioma atual no cookie
            setCookie(CONFIG.cookieName, currentLang, CONFIG.cookieExpiry);
        }
    }

    /**
     * Adiciona estilos CSS dinamicamente
     */
    function injectStyles() {
        const style = document.createElement('style');
        style.textContent = `
            /* Animação suave para o menu */
            #language-menu {
                animation: slideDown 0.2s ease-out;
                transform-origin: top;
            }
            
            @keyframes slideDown {
                from {
                    opacity: 0;
                    transform: translateY(-10px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            /* Hover effect para opções */
            .language-option {
                position: relative;
                transition: all 0.2s;
            }
            
            .language-option::before {
                content: '';
                position: absolute;
                left: 0;
                top: 0;
                bottom: 0;
                width: 3px;
                background: #4f46e5;
                opacity: 0;
                transition: opacity 0.2s;
            }
            
            .language-option:hover::before,
            .language-option.bg-slate-100::before {
                opacity: 1;
            }
            
            /* Mobile: menu full width */
            @media (max-width: 640px) {
                #language-menu {
                    left: 0;
                    right: 0;
                    width: auto;
                    margin: 0 1rem;
                }
            }
        `;
        document.head.appendChild(style);
    }

    /**
     * Inicialização
     */
    function init() {
        // Aguardar DOM carregar
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
            return;
        }

        console.log('🌍 AI Factory i18n inicializado');
        
        // Injeta estilos
        injectStyles();
        
        // Setup
        setupClickOutside();
        
        // Auto-detecção (com delay para não bloquear carregamento)
        setTimeout(() => {
            autoDetectAndRedirect();
        }, 500);
    }

    // Executar
    init();
})();
