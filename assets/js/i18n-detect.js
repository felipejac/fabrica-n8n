/**
 * 🌍 Client-side i18n Detection for GitHub Pages
 * 
 * Detecta o idioma do usuário e redireciona para a versão apropriada
 * Usado no GitHub Pages onde não há servidor backend
 */

(function() {
    'use strict';
    
    // Configuração
    const CONFIG = {
        defaultLanguage: 'pt',
        supportedLanguages: ['pt', 'en'],
        cookieName: 'language',
        cookieExpiry: 365, // dias
        portugueseRegions: ['BR', 'PT']
    };

    /**
     * Obtém idioma do cookie
     */
    function getLanguageFromCookie() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === CONFIG.cookieName) {
                return value;
            }
        }
        return null;
    }

    /**
     * Define idioma no cookie
     */
    function setLanguageCookie(lang) {
        const expiry = new Date();
        expiry.setDate(expiry.getDate() + CONFIG.cookieExpiry);
        document.cookie = `${CONFIG.cookieName}=${lang}; path=/; expires=${expiry.toUTCString()}`;
    }

    /**
     * Obtém idioma do navegador
     */
    function getLanguageFromBrowser() {
        const lang = navigator.language || navigator.userLanguage;
        if (lang) {
            // Extrai código do idioma (ex: "pt-BR" -> "pt")
            return lang.split('-')[0].toLowerCase();
        }
        return null;
    }

    /**
     * Detecta região do usuário via CloudFlare (se disponível)
     * ou via API de geolocalização
     */
    async function detectRegion() {
        // Tentar obter do CloudFlare header (se disponível via meta tag)
        const cfMeta = document.querySelector('meta[name="cf-country"]');
        if (cfMeta) {
            return cfMeta.content;
        }

        // Fallback: usar API de geolocalização gratuita
        try {
            const response = await fetch('https://ipapi.co/json/', { timeout: 2000 });
            if (response.ok) {
                const data = await response.json();
                return data.country_code;
            }
        } catch (error) {
            console.log('Geolocation API unavailable:', error);
        }

        return null;
    }

    /**
     * Determina se deve usar português baseado na região
     */
    function shouldUsePortuguese(region) {
        return region && CONFIG.portugueseRegions.includes(region.toUpperCase());
    }

    /**
     * Detecta idioma preferido do usuário
     */
    async function detectLanguage() {
        // 1. Cookie (maior prioridade)
        const cookieLang = getLanguageFromCookie();
        if (cookieLang && CONFIG.supportedLanguages.includes(cookieLang)) {
            return cookieLang;
        }

        // 2. Região geográfica
        const region = await detectRegion();
        if (region) {
            if (shouldUsePortuguese(region)) {
                return 'pt';
            } else {
                return 'en';
            }
        }

        // 3. Idioma do navegador
        const browserLang = getLanguageFromBrowser();
        if (browserLang && CONFIG.supportedLanguages.includes(browserLang)) {
            return browserLang;
        }

        // 4. Default
        return CONFIG.defaultLanguage;
    }

    /**
     * Obtém caminho atual sem prefixo de idioma
     */
    function getCurrentPath() {
        let path = window.location.pathname;
        
        // Remove prefixos de idioma existentes
        for (let lang of CONFIG.supportedLanguages) {
            if (path.startsWith(`/${lang}/`)) {
                path = path.substring(3); // Remove "/en/" ou "/pt/"
                break;
            }
        }

        // Remove barra inicial se houver
        if (path.startsWith('/')) {
            path = path.substring(1);
        }

        // Se vazio, use index.html
        if (!path || path === '/') {
            path = 'index.html';
        }

        return path;
    }

    /**
     * Redireciona para versão traduzida
     */
    function redirectToLanguage(lang) {
        const currentPath = getCurrentPath();
        const currentLang = window.location.pathname.split('/')[1];

        // Se já está no idioma correto, não fazer nada
        if (currentLang === lang) {
            return;
        }

        let newPath;
        if (lang === 'pt') {
            // Português é o idioma padrão (sem prefixo)
            newPath = `/${currentPath}`;
        } else {
            // Outros idiomas usam prefixo
            newPath = `/translated/${lang}/${currentPath}`;
        }

        // Preservar query string e hash
        const search = window.location.search;
        const hash = window.location.hash;

        window.location.href = newPath + search + hash;
    }

    /**
     * Cria seletor de idioma
     */
    function createLanguageSelector() {
        const selector = document.createElement('div');
        selector.id = 'language-selector';
        selector.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 8px 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            font-family: 'Inter', sans-serif;
        `;

        const select = document.createElement('select');
        select.style.cssText = `
            border: none;
            background: transparent;
            font-size: 14px;
            cursor: pointer;
            outline: none;
        `;

        const languages = [
            { code: 'pt', name: '🇧🇷 Português', native: 'Português' },
            { code: 'en', name: '🇺🇸 English', native: 'English' }
        ];

        languages.forEach(lang => {
            const option = document.createElement('option');
            option.value = lang.code;
            option.textContent = lang.name;
            select.appendChild(option);
        });

        // Define idioma atual
        const currentLang = getLanguageFromCookie() || CONFIG.defaultLanguage;
        select.value = currentLang;

        // Evento de mudança
        select.addEventListener('change', (e) => {
            const newLang = e.target.value;
            setLanguageCookie(newLang);
            redirectToLanguage(newLang);
        });

        selector.appendChild(select);
        document.body.appendChild(selector);
    }

    /**
     * Inicialização
     */
    async function init() {
        // Aguardar DOM carregar
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
            return;
        }

        // Detectar e redirecionar
        const detectedLang = await detectLanguage();
        
        // Salvar no cookie
        setLanguageCookie(detectedLang);

        // Verificar se precisa redirecionar
        const currentPath = window.location.pathname;
        const isEnglishPath = currentPath.startsWith('/translated/en/');
        const isPortuguesePath = !currentPath.startsWith('/translated/');

        if (detectedLang === 'en' && !isEnglishPath) {
            redirectToLanguage('en');
        } else if (detectedLang === 'pt' && !isPortuguesePath) {
            redirectToLanguage('pt');
        }

        // Criar seletor de idioma
        createLanguageSelector();

        // Log para debug
        console.log('🌍 i18n detected:', {
            language: detectedLang,
            path: currentPath
        });
    }

    // Executar
    init();
})();
