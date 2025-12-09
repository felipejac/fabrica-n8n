# 📋 Checklist de Problemas do Seletor de Idioma

## ✅ Status Atual

- [x] **HTML:** Seletor adicionado ao menu (linha 84-120)
- [x] **JavaScript:** i18n-detect.js carregado (570 linhas)
- [x] **CSS:** Tailwind CDN está ativo
- [x] **Deploy:** GitHub Pages atualizado
- [x] **Funções:** `toggleLanguageMenu()` e `changeLanguage()` definidas

## ❓ Problema Relatado

**"O seletor de idioma não funciona, e o botão antigo continua no menu, na lateral da página"**

## 🔧 Possíveis Causas

### 1. **Cache do Navegador** 🌐
- **Sintoma:** Página mostra versão antiga
- **Solução:** 
  - Pressione `Ctrl+Shift+Delete` (Windows/Linux) ou `Cmd+Shift+Delete` (Mac)
  - Marque "Cookies" e "Cached images"
  - Limpe os últimos "Todos os horários"
  - Recarregue a página

### 2. **Cache de Serviço Worker** 🔄
- **Sintoma:** Página não atualiza mesmo após F5
- **Solução:**
  - F12 → Application → Service Workers
  - Clique "Unregister"
  - Recarregue

### 3. **Problema de Carregamento do JavaScript** 📦
- **Sintoma:** `toggleLanguageMenu is not defined`
- **Solução:**
  - F12 → Network → reload
  - Procure por `i18n-detect.js`
  - Verifique status: deve ser 200
  - Se for 404: arquivo não está sendo servido

### 4. **Elemento HTML Duplicado** 👥
- **Sintoma:** Dois botões de idioma
- **Solução:**
  - F12 → Elements → Ctrl+F → "language-selector"
  - Conte quantos aparecem (deve ser 1)
  - Se houver 2, há um duplicado que precisa ser removido

### 5. **CSS Tailwind não Renderizado** 🎨
- **Sintoma:** Botão existe mas não tem estilo
- **Solução:**
  - F12 → Elements → Inspecione o botão
  - Verifique se classes como `px-3`, `py-1.5` existem
  - Se Tailwind falhar, classes não serão aplicadas

## 📱 Teste Manual

Execute no console do navegador (F12 → Console):

```javascript
// Teste 1: Elementos HTML
console.log('Container:', document.getElementById('language-selector-container') ? '✅' : '❌');
console.log('Toggle:', document.getElementById('language-toggle') ? '✅' : '❌');
console.log('Menu:', document.getElementById('language-menu') ? '✅' : '❌');

// Teste 2: Funções
console.log('toggleLanguageMenu:', typeof toggleLanguageMenu);
console.log('changeLanguage:', typeof changeLanguage);

// Teste 3: Clique
document.getElementById('language-toggle')?.click();
console.log('Menu visível:', !document.getElementById('language-menu').classList.contains('hidden'));
```

## 🎯 Solução Recomendada

Tente em ordem:

1. **Limpe o cache do navegador**
   - Ctrl+Shift+Delete → Limpar "Todos os horários"

2. **Recarregue a página**
   - Ctrl+F5 (força reload sem cache)

3. **Abra em navegador diferente ou incógnito**
   - Chrome/Edge: Ctrl+Shift+N
   - Firefox: Ctrl+Shift+P
   - Safari: Cmd+Shift+N

4. **Verifique o console (F12)**
   - Procure por erros em vermelho
   - Procure por mensagens com 🌍

Se ainda assim não funcionar, execute o teste acima e me envie o resultado.

## 📸 O que Esperar

### Desktop (> 640px)
```
┌─────────────────────────────────┐
│ ...menu... │ 🇧🇷 PT ▾ │ ⚙️ │
└─────────────────────────────────┘
                    └─────────────────┐
                    │ 🇧🇷 Português ✓ │
                    │ 🇺🇸 English     │
                    └─────────────────┘
```

### Mobile (< 640px)
```
┌─────────────────────────────────┐
│ ...menu... │ 🇧🇷▾ │ ⚙️ │
└─────────────────────────────────┘
     └──────────┐
     │🇧🇷 Português│
     │🇺🇸 English  │
     └──────────┘
```

---

## 🚀 Próximos Passos

1. Teste local: `npm run dev` ou abra `file://` local
2. Se funciona localmente mas não em GitHub Pages:
   - Problema é específico de GitHub Pages/CDN
   - Cheque URLs de assets
   - Verifique paths relativos vs absolutos

3. Se funciona em github.com mas não no navegador:
   - Problema é cache do navegador
   - Limpe tudo (cookies, cache, storage local)

---

**Data:** Dec 9, 2025  
**Status:** Investigando cache e elementos duplicados
