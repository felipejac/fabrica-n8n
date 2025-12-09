/**
 * 🌍 Simple Language Switcher
 * Sem IIFE, sem async, apenas JavaScript vanilla puro
 */

console.log('🌍 Language Switcher iniciando...');

// Setup ao carregar
function setupLanguageSwitcher() {
    console.log('📍 setupLanguageSwitcher chamado');
    
    const toggle = document.getElementById('language-toggle');
    const menu = document.getElementById('language-menu');
    const options = document.querySelectorAll('.language-option');
    
    if (!toggle) {
        console.error('❌ Toggle não encontrado');
        return;
    }
    
    if (!menu) {
        console.error('❌ Menu não encontrado');
        return;
    }
    
    console.log('✓ Elementos encontrados');
    
    // Toggle menu
    toggle.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        console.log('🔘 Toggle clicado');
        menu.classList.toggle('hidden');
        console.log('📋 Menu agora:', menu.classList.contains('hidden') ? 'FECHADO' : 'ABERTO');
    });
    
    // Opções de idioma
    options.forEach(option => {
        option.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const lang = this.getAttribute('data-lang');
            console.log('🌐 Idioma clicado:', lang);
            
            // Fecha menu
            menu.classList.add('hidden');
            
            // Verifica URL atual
            const currentPath = window.location.pathname;
            const isEnglish = currentPath.includes('/translated/en/');
            
            console.log('📍 Caminho atual:', currentPath);
            console.log('🌍 É English?', isEnglish);
            
            let newURL = '';
            
            if (lang === 'en') {
                if (!isEnglish) {
                    // Ir para English
                    let cleanPath = currentPath
                        .replace('/fabrica-n8n/', '')
                        .replace(/^\//, '');
                    
                    if (!cleanPath || cleanPath === '') {
                        cleanPath = 'index.html';
                    }
                    
                    newURL = window.location.origin + '/fabrica-n8n/translated/en/' + cleanPath;
                    console.log('🔄 Redirecionando para EN:', newURL);
                    window.location.href = newURL;
                }
            } else if (lang === 'pt') {
                if (isEnglish) {
                    // Ir para Português
                    let cleanPath = currentPath
                        .replace('/fabrica-n8n/translated/en/', '')
                        .replace(/^\//, '');
                    
                    if (!cleanPath || cleanPath === '') {
                        cleanPath = 'index.html';
                    }
                    
                    newURL = window.location.origin + '/fabrica-n8n/' + cleanPath;
                    console.log('🔄 Redirecionando para PT:', newURL);
                    window.location.href = newURL;
                }
            }
        });
    });
    
    // Fechar ao clicar fora
    document.addEventListener('click', function(e) {
        const container = document.getElementById('language-selector-container');
        if (container && !container.contains(e.target)) {
            menu.classList.add('hidden');
        }
    });
    
    // Fechar ao pressionar ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            menu.classList.add('hidden');
        }
    });
    
    console.log('✓ Language Switcher pronto');
}

// Executar quando DOM estiver pronto
if (document.readyState === 'loading') {
    console.log('⏳ DOM ainda carregando, aguardando...');
    document.addEventListener('DOMContentLoaded', setupLanguageSwitcher);
} else {
    console.log('✓ DOM já carregado, setupando agora');
    setupLanguageSwitcher();
}

// Também tentar quando página ficar pronta
window.addEventListener('load', function() {
    console.log('✓ Página completamente carregada');
    // Verificar se elementos existem agora
    if (!document.getElementById('language-toggle')) {
        console.warn('⚠️ Toggle ainda não encontrado, tentando setup novamente');
        setupLanguageSwitcher();
    }
});
