# 🚀 Deploy em Produção - GitHub Pages

## ✅ Status: CONFIGURADO

### 📋 Configurações Aplicadas

1. **GitHub Actions Workflow**
   - Atualizado `.github/workflows/deploy.yml`
   - Inclui instalação de dependências
   - Gera traduções automaticamente no build

2. **Client-side i18n Detection**
   - Criado `assets/js/i18n-detect.js`
   - Detecta idioma do usuário
   - Redireciona automaticamente
   - Seletor de idioma visual

3. **Traduções**
   - 12,543 arquivos em `/translated/en/`
   - Estrutura completa pronta

---

## 🌐 URLs de Produção

Após o deploy, o site estará disponível em:

**Português (padrão):**
```
https://felipejac.github.io/fabrica-n8n/
https://felipejac.github.io/fabrica-n8n/index.html
```

**Inglês (traduzido):**
```
https://felipejac.github.io/fabrica-n8n/translated/en/index.html
```

**Integrações:**
```
https://felipejac.github.io/fabrica-n8n/integracoes/
https://felipejac.github.io/fabrica-n8n/translated/en/integracoes/
```

---

## 🔄 Processo de Deploy

### Automático (GitHub Actions)

Cada push na branch `main` dispara automaticamente:

1. ✅ Checkout do código
2. ✅ Configuração do Python
3. ✅ Instalação de dependências (Flask)
4. ✅ Execução do `build.py`
5. ✅ Geração de traduções i18n
6. ✅ Upload para GitHub Pages
7. ✅ Deploy automático

### Manual

Para forçar um deploy manual:

```bash
# 1. Gerar traduções localmente
python3 i18n_service.py --all --languages en

# 2. Commit e push
git add translated/
git commit -m "🌍 Atualizar traduções"
git push origin main
```

---

## 🧪 Testar Localmente

### Com Python HTTP Server

```bash
# Servidor simples
python3 -m http.server 8000

# Acessar
open http://localhost:8000
```

### Com Flask (i18n completo)

```bash
# Instalar dependências
pip install flask

# Iniciar servidor
python3 i18n_server.py --debug

# Acessar
open http://localhost:5000
```

---

## 🌍 Funcionalidades i18n em Produção

### Detecção Automática

O sistema detecta automaticamente o idioma do usuário:

1. **Cookie** (preferência salva)
2. **Região geográfica** (via API)
3. **Idioma do navegador**
4. **Default: Português**

### Lógica Regional

- 🇧🇷 **Brasil** → Português
- 🇵🇹 **Portugal** → Português
- 🌎 **Resto do mundo** → Inglês

### Seletor Manual

Usuário pode mudar idioma manualmente:
- Seletor visual no canto superior direito
- Preferência salva em cookie (365 dias)

---

## 📊 Estatísticas de Deploy

| Métrica | Valor |
|---------|-------|
| Arquivos HTML | 12,544 |
| Idiomas | PT, EN |
| Size total | ~500 MB |
| Build time | ~2-3 min |
| Deploy time | ~1-2 min |

---

## ⚙️ Configurações do GitHub

### Settings → Pages

1. **Source:** Deploy from a branch
2. **Branch:** `gh-pages` (criado automaticamente)
3. **Folder:** `/` (root)

### Settings → Actions

1. **Workflow permissions:** Read and write
2. **Allow GitHub Actions:** All actions and reusable workflows

---

## 🔍 Monitoramento

### Ver Status do Deploy

1. Acesse: https://github.com/felipejac/fabrica-n8n/actions
2. Veja o workflow "Build and Deploy to GitHub Pages"
3. Verifique logs em tempo real

### Verificar Erros

```bash
# Ver logs do último deploy
gh run list --workflow=deploy.yml --limit 1
gh run view <run-id>
```

---

## 🐛 Troubleshooting

### Problema: Traduções não aparecem

**Solução:**
```bash
# Regenerar traduções localmente
python3 i18n_service.py --all --languages en

# Commit e push
git add translated/
git commit -m "🔧 Regenerar traduções"
git push
```

### Problema: Deploy falhou

**Solução:**
1. Verificar logs no GitHub Actions
2. Verificar se `build.py` executa sem erros
3. Verificar se `i18n_service.py` executa sem erros

### Problema: Redirecionamento não funciona

**Solução:**
- GitHub Pages não suporta server-side redirects
- Usar detecção client-side (já implementado)
- Script `i18n-detect.js` faz isso automaticamente

---

## 📝 Próximos Passos

### Opcional: Custom Domain

1. Comprar domínio (ex: `ai-factory.com`)
2. Configurar DNS:
   ```
   A     @     185.199.108.153
   A     @     185.199.109.153
   A     @     185.199.110.153
   A     @     185.199.111.153
   CNAME www   felipejac.github.io
   ```
3. Adicionar em Settings → Pages → Custom domain

### Opcional: CDN/Cloudflare

1. Adicionar site no Cloudflare
2. Configurar DNS no Cloudflare
3. Ativar proxy (nuvem laranja)
4. Benefícios:
   - ⚡ Cache global
   - 🔐 DDoS protection
   - 📊 Analytics
   - 🌍 CF-IPCountry header (melhor detecção)

---

## ✅ Checklist de Deploy

- [x] Workflow do GitHub Actions atualizado
- [x] Script de detecção client-side criado
- [x] Traduções geradas (12,543 arquivos)
- [x] index.html atualizado com script
- [x] Documentação de deploy criada
- [ ] Push para GitHub (próximo passo)
- [ ] Verificar deploy no GitHub Actions
- [ ] Testar URLs de produção
- [ ] Verificar seletor de idioma
- [ ] Validar redirecionamento automático

---

## 🎉 Conclusão

Sistema pronto para deploy em produção no GitHub Pages!

**Próximo comando:**
```bash
git add .
git commit -m "🚀 Deploy: Configuração i18n para GitHub Pages"
git push origin main
```

Após o push, aguarde ~3-5 minutos para o deploy completar.

---

**Criado por:** AI Factory  
**Data:** 9 de Dezembro, 2025  
**Status:** ✅ PRONTO PARA PRODUÇÃO
