# 🔍 Debug Interativo - Seletor de Idioma

Abra o console (F12) e execute esses comandos **um por um** para diagnosticar:

---

## ✅ Teste 1: Verificar Elementos HTML

```javascript
// Verificar se elementos existem
const container = document.getElementById('language-selector-container');
const toggle = document.getElementById('language-toggle');
const menu = document.getElementById('language-menu');

console.log('=== ELEMENTOS HTML ===');
console.log('container:', container ? '✓ ENCONTRADO' : '❌ NÃO ENCONTRADO');
console.log('toggle:', toggle ? '✓ ENCONTRADO' : '❌ NÃO ENCONTRADO');
console.log('menu:', menu ? '✓ ENCONTRADO' : '❌ NÃO ENCONTRADO');

// Se encontrado, inspecionar
if (toggle) {
    console.log('toggle.onclick:', toggle.onclick);
    console.log('toggle HTML:', toggle.outerHTML.substring(0, 100));
}
```

---

## ✅ Teste 2: Verificar Funções

```javascript
console.log('=== FUNÇÕES GLOBAIS ===');
console.log('toggleLanguageMenu:', typeof window.toggleLanguageMenu);
console.log('changeLanguage:', typeof window.changeLanguage);

// Tentar chamar manualmente
if (typeof window.toggleLanguageMenu === 'function') {
    console.log('✓ Função toggleLanguageMenu pode ser chamada');
} else {
    console.error('❌ toggleLanguageMenu NÃO é função!');
}
```

---

## ✅ Teste 3: Testar Clique Programático

```javascript
// Simular clique no botão
const button = document.getElementById('language-toggle');
if (button) {
    console.log('🔵 Clicando no botão...');
    button.click();
    
    // Verificar se menu ficou visível
    const menu = document.getElementById('language-menu');
    setTimeout(() => {
        console.log('Menu hidden?', menu?.classList.contains('hidden'));
        console.log('Menu visível?', !menu?.classList.contains('hidden'));
    }, 100);
} else {
    console.error('❌ Botão não encontrado');
}
```

---

## ✅ Teste 4: Verificar Eventos

```javascript
// Listar todos os listeners do botão
const button = document.getElementById('language-toggle');
if (button) {
    console.log('=== LISTENERS DO BOTÃO ===');
    console.log('onclick attribute:', button.getAttribute('onclick'));
    console.log('onclick property:', button.onclick);
    
    // Tentar chamar o onclick diretamente
    const onclickCode = button.getAttribute('onclick');
    if (onclickCode) {
        console.log('Tentando executar onclick:', onclickCode);
        eval(onclickCode);
    }
}
```

---

## ✅ Teste 5: Verificar CSS

```javascript
// Ver estilos do menu
const menu = document.getElementById('language-menu');
if (menu) {
    console.log('=== ESTILOS DO MENU ===');
    console.log('classes:', menu.className);
    console.log('hidden?', menu.classList.contains('hidden'));
    console.log('display:', window.getComputedStyle(menu).display);
    console.log('visibility:', window.getComputedStyle(menu).visibility);
    console.log('opacity:', window.getComputedStyle(menu).opacity);
}
```

---

## 🎯 Se Tudo Estiver OK

Execute este teste final:

```javascript
// Teste completo de mudança de idioma
console.log('=== TESTE COMPLETO ===');

// 1. Abrir menu
document.getElementById('language-toggle').click();
console.log('Menu aberto:', !document.getElementById('language-menu').classList.contains('hidden'));

// 2. Clicar em English
setTimeout(() => {
    document.querySelector('[data-lang="en"]').click();
    console.log('Clique em English enviado');
}, 100);
```

---

## 📊 Se Encontrar Erro

Copie o output COMPLETO do console e envie, incluindo:
- ✓ ou ❌ de cada teste
- Mensagens de erro (em vermelho)
- Stack trace se houver

Isso vai me mostrar exatamente qual é o problema!
