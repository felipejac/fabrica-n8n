# 🌍 Seletor de Idioma - Guia Visual

**Versão:** 2.0  
**Data:** 9 de Dezembro, 2025  
**Status:** ✅ Deployado

---

## 🎨 Design

### 📱 Mobile (< 640px)

```
┌─────────────────────────────┐
│  🏭 AI Factory              │
├─────────────────────────────┤
│ 🏠 🏭 📚 🔌 🧰 🎓 🚑 │ 🇧🇷▾ │⚙️│
└─────────────────────────────┘
       Menu scroll horizontal
       
Ao clicar em 🇧🇷▾:

┌─────────────────────────────┐
│  🇧🇷  Português      ✓      │
│  🇺🇸  English               │
└─────────────────────────────┘
```

### 💻 Desktop (> 640px)

```
┌──────────────────────────────────────────────────┐
│  🏭 AI Factory                                   │
│                                                  │
│  🏠  🏭  📚  🔌  🧰  🎓  🚑  │  🇧🇷 PT ▾  │  ⚙️  │
└──────────────────────────────────────────────────┘

Ao clicar em 🇧🇷 PT ▾:

                              ┌────────────────┐
                              │ 🇧🇷  Português ✓│
                              │ 🇺🇸  English   │
                              └────────────────┘
```

---

## ✨ Funcionalidades

### 1. **Auto-Detecção Inteligente**

```javascript
Prioridade:
1. Cookie (preferência salva)      → Maior prioridade
2. Região (via IP geolocation)     → BR/PT = Português
3. Idioma do navegador             → navigator.language
4. Default                         → Português
```

### 2. **Lógica Regional**

| Região | Idioma |
|--------|--------|
| 🇧🇷 Brasil | Português |
| 🇵🇹 Portugal | Português |
| 🇺🇸 Estados Unidos | English |
| 🇬🇧 Reino Unido | English |
| 🌎 Resto do mundo | English |

### 3. **Estados do Botão**

**Normal:**
```
🇧🇷 PT ▾
```

**Hover:**
```
🇧🇷 PT ▾  (fundo branco, seta desce)
```

**Clicado:**
```
🇧🇷 PT ▾  (menu aberto)
```

**Trocando:**
```
🔄 ...  (loading durante redirect)
```

---

## 🎯 Comportamento

### Desktop

1. **Hover** → Fundo fica branco, seta anima
2. **Click** → Menu dropdown aparece (slide-down)
3. **Selecionar idioma** → Checkmark ✓ aparece
4. **Click fora** → Menu fecha
5. **ESC** → Menu fecha

### Mobile

1. **Tap** → Menu aparece full-width
2. **Tap opção** → Troca idioma (loading)
3. **Tap fora** → Menu fecha
4. **Botão** → Só mostra bandeira (economiza espaço)

---

## 🔄 Fluxo de Troca de Idioma

```
1. Usuário clica em idioma
   ↓
2. Marca escolha manual (sessionStorage)
   ↓
3. Salva no cookie (365 dias)
   ↓
4. Fecha menu dropdown
   ↓
5. Verifica se já está no idioma
   ↓
6. Se não: Constrói nova URL
   ↓
7. Mostra feedback visual (🔄 ...)
   ↓
8. Redireciona para nova URL
   ↓
9. Página carrega no novo idioma
   ↓
10. UI atualiza automaticamente
```

---

## 💾 Estrutura de URLs

### Português (padrão)
```
https://felipejac.github.io/fabrica-n8n/
https://felipejac.github.io/fabrica-n8n/index.html
https://felipejac.github.io/fabrica-n8n/integracoes/
```

### Inglês (traduzido)
```
https://felipejac.github.io/fabrica-n8n/translated/en/index.html
https://felipejac.github.io/fabrica-n8n/translated/en/integracoes/
```

---

## 🎨 Estilos CSS

### Animações

```css
/* Slide down do menu */
@keyframes slideDown {
    from { opacity: 0; transform: translateY(-10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Hover nas opções */
.language-option::before {
    width: 3px;
    background: #4f46e5;
    opacity: 0 → 1 (on hover)
}
```

### Responsividade

```css
/* Mobile */
@media (max-width: 640px) {
    #current-lang { display: none; }  /* Esconde "PT" */
    #language-menu { width: auto; }   /* Full width */
}

/* Desktop */
@media (min-width: 640px) {
    #current-lang { display: inline; } /* Mostra "PT" */
    #language-menu { width: 10rem; }   /* Fixed width */
}
```

---

## 🧪 Teste Manual

### Cenário 1: Primeira Visita (Brasil)
1. Acessar site
2. ✅ Detecta região = BR
3. ✅ Mantém português
4. ✅ Botão mostra 🇧🇷 PT

### Cenário 2: Primeira Visita (EUA)
1. Acessar site
2. ✅ Detecta região = US
3. ✅ Redireciona para /translated/en/
4. ✅ Botão mostra 🇺🇸 EN

### Cenário 3: Troca Manual
1. Clicar em 🇧🇷 PT ▾
2. ✅ Menu abre
3. Clicar em 🇺🇸 English
4. ✅ Loading aparece
5. ✅ Redireciona
6. ✅ Cookie salvo
7. ✅ Próxima visita mantém escolha

### Cenário 4: Mobile
1. Abrir em celular
2. ✅ Botão compacto (só 🇧🇷▾)
3. ✅ Menu full-width
4. ✅ Fácil de clicar
5. ✅ Fecha ao tocar fora

---

## 🐛 Tratamento de Erros

### Erro 1: API de Geolocalização falha
```javascript
try {
    const response = await fetch('https://ipapi.co/json/');
} catch (error) {
    console.log('Geolocation timeout, usando fallback');
    // Usa idioma do navegador
}
```

### Erro 2: URL inválida
```javascript
if (!CONFIG.supportedLanguages.includes(lang)) {
    console.error('Idioma não suportado:', lang);
    return;
}
```

### Erro 3: Elementos não encontrados
```javascript
const flagEl = document.getElementById('current-flag');
if (!flagEl) return; // Fail silently
```

---

## 📊 Performance

| Métrica | Valor |
|---------|-------|
| Tamanho JS | ~9 KB |
| Tamanho CSS | ~500 bytes |
| Tempo de detecção | < 500ms |
| Tempo de troca | < 100ms |
| API timeout | 3000ms |

---

## 🔧 Configuração

### Adicionar Novo Idioma

```javascript
// Em i18n-detect.js
const CONFIG = {
    supportedLanguages: ['pt', 'en', 'es'], // Adicionar 'es'
    languageData: {
        es: { 
            flag: '🇪🇸', 
            name: 'Español', 
            code: 'ES' 
        }
    }
};
```

```html
<!-- Em index.html -->
<button 
    onclick="changeLanguage('es')"
    data-lang="es"
    class="language-option"
>
    <span>🇪🇸</span>
    <span>Español</span>
</button>
```

---

## ✅ Checklist de Implementação

- [x] HTML do seletor no menu
- [x] JavaScript de detecção
- [x] CSS de animações
- [x] Auto-detecção por região
- [x] Cookie de preferência
- [x] Redirecionamento automático
- [x] Feedback visual
- [x] Responsivo mobile
- [x] Acessibilidade (ESC fecha)
- [x] Tratamento de erros
- [x] Console logs para debug
- [x] Committed e pushed
- [x] Deploy automático

---

## 🎉 Resultado Final

### ✅ Desktop
```
Menu horizontal com botão elegante:
🇧🇷 PT ▾
```

### ✅ Mobile
```
Botão compacto:
🇧🇷▾
```

### ✅ Funcionalidades
- Auto-detecção ✅
- Troca manual ✅
- Persistência ✅
- Responsivo ✅
- Acessível ✅

---

**Status:** 🚀 PRODUÇÃO  
**URL:** https://felipejac.github.io/fabrica-n8n/
