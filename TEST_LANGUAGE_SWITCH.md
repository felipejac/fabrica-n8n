# 🧪 Teste de Troca de Idioma

## ✅ Problema Corrigido

**Causa:** O arquivo `i18n-detect.js` não estava no diretório `translated/en/assets/js/`

**Solução:** Copiado o arquivo para o local correto

---

## 🧪 Como Testar

### 1. **Acesse a página em Português**
```
https://felipejac.github.io/fabrica-n8n/
```
- Você deve ver: `🇧🇷 PT` no menu

### 2. **Clique no seletor de idioma**
- Clique no botão `🇧🇷 PT ▾`
- Um menu deve aparecer com:
  - 🇧🇷 Português (com checkmark ✓)
  - 🇺🇸 English

### 3. **Clique em "English"**
- A página deve redirecionar para: `/translated/en/index.html`
- O botão deve mudar para: `🇺🇸 EN`
- O menu deve mostrar checkmark em English

### 4. **Clique em "Português"**
- A página deve redirecionar de volta para: `/index.html`
- O botão deve voltar para: `🇧🇷 PT`

---

## 🔍 Se Não Funcionar

### Teste no Console (F12)

```javascript
// Verificar se elemento existe
console.log('HTML ok?', !!document.getElementById('language-selector-container'));

// Verificar se função existe
console.log('JS ok?', typeof toggleLanguageMenu);

// Tentar mudar idioma manualmente
changeLanguage('en');
```

### Se receber erro "cannot find changeLanguage"
- Abra F12 → Network
- Procure por `i18n-detect.js`
- Verifique se status é 200 (sucesso) ou 404 (não encontrado)
- Se 404, o arquivo pode não ter sido deployado ainda
- Aguarde 2-3 minutos e recarregue (Ctrl+F5)

---

## 📋 Status do Deploy

Deploy iniciado em: 09/12/2025 00:54 UTC

Tempo estimado: 2-3 minutos

Se tudo funcionar, você deve conseguir:
- ✅ Clicar no seletor
- ✅ Ver o menu abrir
- ✅ Trocar para English
- ✅ Página redireciona
- ✅ URL muda para `/translated/en/`
- ✅ Clicar novamente para voltar a Português

---

## 🐛 Debug Info

Se ainda houver problema, execute isto no console e envie o resultado:

```javascript
{
  url: window.location.href,
  i18nLoaded: typeof window.toggleLanguageMenu,
  containerFound: !!document.getElementById('language-selector-container'),
  cookie: document.cookie.split('ai_factory_language=')[1]?.split(';')[0],
  sessionStorage: sessionStorage.getItem('manual_language_choice')
}
```
