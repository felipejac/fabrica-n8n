# 🔍 Diagnóstico do Seletor de Idioma

Se o seletor de idioma não está funcionando, execute este teste no console do navegador (F12):

## Teste 1: Verificar se elementos existem

```javascript
// Verificar se elementos HTML existem
console.log('=== DIAGNÓSTICO ===');
console.log('1. Container existe?', !!document.getElementById('language-selector-container'));
console.log('2. Toggle button existe?', !!document.getElementById('language-toggle'));
console.log('3. Menu existe?', !!document.getElementById('language-menu'));
console.log('4. i18n-detect.js carregado?', typeof toggleLanguageMenu !== 'undefined');

// Contar quantos elementos têm "language" no ID
const langElements = document.querySelectorAll('[id*="language"]');
console.log('5. Total de elementos com "language" no ID:', langElements.length);

// Listar todos
langElements.forEach((el, i) => {
    console.log(`   ${i}: ${el.id} (${el.tagName})`);
});
```

## Teste 2: Testar funções

```javascript
// Verificar se funções estão acessíveis
console.log('=== FUNÇÕES ===');
console.log('toggleLanguageMenu:', typeof toggleLanguageMenu);
console.log('changeLanguage:', typeof changeLanguage);
console.log('updateLanguageUI:', typeof updateLanguageUI);
```

## Teste 3: Verificar cookie

```javascript
// Ver se há cookie de idioma
const getCookie = (name) => {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [key, value] = cookie.trim().split('=');
        if (key === name) return value;
    }
    return null;
};

console.log('=== COOKIE ===');
console.log('ai_factory_language:', getCookie('ai_factory_language'));
console.log('sessionStorage.manual_language_choice:', sessionStorage.getItem('manual_language_choice'));
```

## Teste 4: Testar clique

```javascript
// Simular clique
console.log('=== TESTE DE CLIQUE ===');
const btn = document.getElementById('language-toggle');
if (btn) {
    console.log('Clicando no botão...');
    btn.click();
    console.log('Menu visível?', !document.getElementById('language-menu').classList.contains('hidden'));
} else {
    console.error('Botão não encontrado!');
}
```

## Se encontrar problema...

### Problema: "toggleLanguageMenu is not defined"
- **Causa:** i18n-detect.js não foi carregado
- **Solução:** 
  1. Abra a aba "Network" (F12)
  2. Procure por `assets/js/i18n-detect.js`
  3. Verifique se o status é 200 (sucesso)
  4. Se for 404, o arquivo está faltando

### Problema: "language-selector-container is null"
- **Causa:** HTML não foi renderizado corretamente
- **Solução:**
  1. Inspecione o elemento (F12 → Elements)
  2. Procure por `language-selector-container`
  3. Se não estiver lá, pode ser um problema de HTML

### Problema: Menu não abre
- **Causa:** CSS ou JavaScript bloqueado
- **Solução:**
  1. Verifique se há erros no console (F12 → Console)
  2. Limpe o cache (Ctrl+Shift+Delete)
  3. Recarregue a página

---

## Informações para Relatar

Se nada funcionar, capture:

```javascript
console.log({
    userAgent: navigator.userAgent,
    url: window.location.href,
    containerExists: !!document.getElementById('language-selector-container'),
    functionsLoaded: typeof toggleLanguageMenu,
    cookieLanguage: getCookie('ai_factory_language'),
    localStorage: localStorage.getItem('ai_factory_language'),
    sessionStorage: sessionStorage.getItem('manual_language_choice')
});
```

Copie o output e me mostre!
