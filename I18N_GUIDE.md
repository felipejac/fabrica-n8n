# 🌍 Internacionalização (i18n) - Guia Completo

**Versão:** 1.0.0  
**Data:** 9 de Dezembro, 2025  
**Status:** Production Ready ✅

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Arquitetura](#arquitetura)
3. [Instalação](#instalação)
4. [Uso](#uso)
5. [APIs](#apis)
6. [Detecção de Localização](#detecção-de-localização)
7. [Melhores Práticas](#melhores-práticas)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 Visão Geral

Sistema de internacionalização (i18n) completo que:

✅ **Detecta automaticamente** a localização do usuário  
✅ **Serve português** para Brasil e Portugal  
✅ **Serve inglês** para resto do mundo  
✅ **Permite preferência manual** via cookie  
✅ **Otimizado para performance** com cache  
✅ **Seguro** com proteção contra path traversal  
✅ **SEO-friendly** com Content-Language headers  
✅ **Escalável** para múltiplos idiomas  

---

## 🏗️ Arquitetura

### Fluxo de Detecção

```
Requisição do Usuário
    ↓
1. Cookie Language (preferência manual) ?
    ├─ SIM → Usar cookie
    └─ NÃO ↓
2. Cloudflare CF-IPCountry (mais confiável)
    ├─ Sim → Detectar país
    └─ NÃO ↓
3. IP Geolocation
    ├─ Sucesso → Detectar país
    └─ NÃO ↓
4. Accept-Language Header
    ├─ Encontrado → Extrair idioma
    └─ NÃO ↓
5. Default (Português)

Resultado: Locale Config (idioma, região, timezone, etc)
```

### Estrutura de Diretórios

```
fabrica-n8n/
├── index.html                 (Português original)
├── assets/
│   ├── css/
│   ├── js/
│   └── images/
├── integracoes/
│   ├── google-sheets.html
│   ├── slack.html
│   └── ...
├── translated/                (Gerado automaticamente)
│   ├── en/                     (Inglês)
│   │   ├── index.html
│   │   ├── assets/
│   │   └── integracoes/
│   ├── es/                     (Espanhol - futuro)
│   │   └── ...
│   └── manifest.json          (Metadados)
├── i18n_service.py            (Motor de tradução)
└── i18n_server.py             (Servidor Flask)
```

---

## 🚀 Instalação

### Requisitos

```bash
Python 3.8+
Flask 2.0+
```

### Setup

```bash
# 1. Instalar dependências
pip install flask

# 2. Gerar traduções
python3 i18n_service.py --all --base-dir .

# 3. Iniciar servidor
python3 i18n_server.py --port 5000 --debug

# 4. Acessar no navegador
open http://localhost:5000
```

---

## 📖 Uso

### Script Standalone (Geração de Arquivos)

```bash
# Gerar estrutura de diretórios
python3 i18n_service.py --setup

# Traduzir apenas index.html
python3 i18n_service.py --translate-index --languages en es

# Traduzir apenas integrações
python3 i18n_service.py --translate-integrations

# Traduzir tudo de uma vez
python3 i18n_service.py --all
```

### Servidor Flask (Em Produção)

```bash
# Desenvolvimento
python3 i18n_server.py --debug

# Produção
python3 i18n_server.py --host 0.0.0.0 --port 8080

# Gerar traduções e iniciar
python3 i18n_server.py --generate-translations
```

### Usar como Biblioteca Python

```python
from i18n_service import TranslationGenerator, GeoLocationDetector, Language

# Inicializar
generator = TranslationGenerator(base_dir=".")
geo_detector = GeoLocationDetector()

# Detectar localização
locale = geo_detector.get_locale_config(
    ip_address="200.1.0.1",
    accept_language="pt-BR,pt;q=0.9",
    cloudflare_country="BR"
)
print(locale.language)  # Language.PT
print(locale.locale_code)  # pt_BR

# Traduzir arquivo
generator.translate_file(
    "index.html",
    languages=[Language.EN, Language.ES]
)

# Gerar manifesto
generator.generate_translation_manifest()
```

---

## 🔌 APIs

### GET `/` (Auto-detect)
Redireciona automaticamente para versão apropriada

```
Requisição:
  GET / (do Brasil)
  
Resposta:
  Location: /index.html (Português)

---

Requisição:
  GET / (dos USA)
  
Resposta:
  Location: /en/index.html (Inglês)
```

### GET `/api/locale`
Retorna informações de localização do cliente

```json
GET /api/locale

{
  "language": "pt",
  "language_name": "Portuguese",
  "region": "BR",
  "timezone": "America/Sao_Paulo",
  "currency": "BRL",
  "locale_code": "pt_BR",
  "should_use_portuguese": true
}
```

### GET `/api/languages`
Retorna idiomas disponíveis

```json
GET /api/languages

{
  "languages": {
    "pt": {
      "name": "Portuguese",
      "native_name": "Português",
      "regions": ["BR", "PT"]
    },
    "en": {
      "name": "English",
      "native_name": "English",
      "regions": ["US", "GB", "AU", "CA"]
    }
  },
  "current_language": "pt"
}
```

### GET `/api/manifest`
Retorna manifesto de tradução

```json
GET /api/manifest

{
  "generated": "2025-12-09T10:30:00",
  "version": "1.0.0",
  "languages": { ... },
  "statistics": {
    "files_processed": 150,
    "files_translated": 150,
    "total_translations": 2500
  }
}
```

---

## 🗺️ Detecção de Localização

### Ordem de Prioridade

1. **Cookie `language`** (Preferência do usuário)
   - Máxima prioridade
   - Válido por 1 ano
   - Pode ser alterado pelo seletor de idioma

2. **Cloudflare `CF-IPCountry`** (Mais confiável)
   - Header gerado por Cloudflare
   - Indicador de país com 99%+ de precisão
   - Automático quando usa Cloudflare

3. **GeoIP do IP**
   - Mapeamento IP → País
   - ~95% de precisão
   - Necessário MaxMind em produção

4. **`Accept-Language` Header**
   - Enviado pelo navegador
   - Parse: "pt-BR,pt;q=0.9,en;q=0.8"
   - Confiabilidade variável

5. **Default**
   - Português se nada mais funcionar

### Exemplo: Detectar Localização em JavaScript

```javascript
// Frontend - Detectar automaticamente
fetch('/api/locale')
  .then(r => r.json())
  .then(locale => {
    console.log(`Idioma: ${locale.language}`);
    console.log(`Região: ${locale.region}`);
    console.log(`Timezone: ${locale.timezone}`);
  });

// Mudar idioma manualmente
function changeLanguage(lang) {
  document.cookie = `language=${lang}; path=/; max-age=31536000`;
  window.location.reload();
}
```

---

## 💡 Melhores Práticas

### 1. **Caching Eficiente**

```python
# HTML: Cache 1 hora (conteúdo muda raramente)
CACHE_DURATION_HTML = 3600

# Assets (CSS, JS): Cache 1 dia (versioned)
CACHE_DURATION_ASSETS = 86400

# APIs: Cache 5 min
CACHE_DURATION_DEFAULT = 300
```

### 2. **Headers de Segurança**

```
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
```

### 3. **SEO Otimizado**

```
Content-Language: pt  (Para português)
Content-Language: en  (Para inglês)
```

Adicionar ao HTML:
```html
<html lang="pt">  <!-- ou lang="en" -->
```

### 4. **Fallback em Caso de Falha**

- Sempre ter versão portuguesa como fallback
- Se arquivo em inglês não existir, servir português
- Nunca quebrar com erro 404

### 5. **Performance**

- **Lazy load** de integrações (13K items é muito)
- **Compress** HTML/CSS/JS
- **CDN** para assets estáticos
- **Service Worker** para offline (futuro)

### 6. **Acessibilidade**

```html
<!-- Seletor de idioma acessível -->
<label for="lang-select">Idioma:</label>
<select id="lang-select" aria-label="Selecionar idioma">
  <option value="pt">Português</option>
  <option value="en">English</option>
</select>
```

---

## 📊 Exemplo: Estrutura de Tradução

### Adicionar Nova Tradução

```python
# Em i18n_service.py -> TranslationMemory.TRANSLATIONS

"Novo Texto em Português": {
    Language.EN: "New Text in English",
    Language.PT: "Novo Texto em Português",
    Language.ES: "Nuevo Texto en Español",
    Language.FR: "Nouveau Texte en Français",
}
```

### Padrão de Organização

```python
TRANSLATIONS = {
    # Navegação
    "🏠 Home": { ... },
    
    # Títulos
    "Título da Página": { ... },
    
    # Botões & CTA
    "Clique Aqui": { ... },
    
    # Mensagens
    "Erro ao carregar": { ... },
    
    # Footer
    "Sobre Nós": { ... },
}
```

---

## 🚀 Deployment

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Gerar traduções
RUN python3 i18n_service.py --all

EXPOSE 8080
CMD ["python3", "i18n_server.py", "--host", "0.0.0.0", "--port", "8080"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  i18n:
    build: .
    ports:
      - "8080:8080"
    environment:
      - FLASK_ENV=production
      - DEBUG=False
    volumes:
      - ./translated:/app/translated

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - i18n
```

### Nginx Proxy (Recomendado)

```nginx
upstream i18n {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name fabrica-n8n.com;

    # Gzip compression
    gzip on;
    gzip_types text/html text/css text/javascript;

    # Cache estático
    location ~* \.(css|js|woff2|svg)$ {
        proxy_pass http://i18n;
        proxy_cache_valid 200 30d;
        expires 30d;
    }

    # Cache HTML
    location ~* \.html$ {
        proxy_pass http://i18n;
        proxy_cache_valid 200 1h;
        expires 1h;
    }

    # Tudo mais
    location / {
        proxy_pass http://i18n;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 🐛 Troubleshooting

### Problema: Sempre retorna português

**Causa:** Cookie language não está sendo limpo

**Solução:**
```bash
# Limpar cookie
document.cookie = "language=; path=/; max-age=0";

# Ou deletar manualmente no DevTools
```

### Problema: Geolocalização imprecisa

**Causa:** IP não mapeia corretamente

**Solução:**
```python
# Em produção, usar MaxMind GeoIP2
from geoip2.database import Reader

reader = Reader('/path/to/GeoLite2-City.mmdb')
response = reader.city(ip_address)
country = response.country.iso_code
```

### Problema: Arquivo não traduzido

**Causa:** Arquivo não foi processado pela tradução

**Solução:**
```bash
# Regenerar traduções
python3 i18n_service.py --all --base-dir .

# Ou manualmente
python3 i18n_service.py --translate-integrations
```

### Problema: HTML malformado após tradução

**Causa:** Regex muito agressivo

**Solução:**
```python
# Verificar logs
python3 i18n_service.py --all --verbose

# Ou processar arquivo específico
python3 -c "
from i18n_service import TranslationGenerator, Language
gen = TranslationGenerator()
gen.translate_file('index.html', [Language.EN])
"
```

---

## 📈 Métricas & Monitoramento

### Logs de Tradução

```bash
# Ver estatísticas após tradução
python3 i18n_service.py --all
# Output:
# ========== ESTATÍSTICAS DE TRADUÇÃO ==========
# Arquivos processados: 150
# Arquivos traduzidos: 150
# Total de traduções: 2500
```

### Monitorar Performance

```python
# Em i18n_server.py
@app.after_request
def log_performance(response):
    duration = request.environ.get('werkzeug.request.start_time', 0)
    if duration:
        print(f"[{request.path}] {duration:.3f}s")
    return response
```

### Rastrear Uso de Idiomas

```javascript
// No frontend
fetch('/api/locale').then(r => r.json()).then(locale => {
    // Enviar para analytics
    gtag('event', 'language_detected', {
        language: locale.language,
        region: locale.region,
    });
});
```

---

## 🔮 Futuro (Roadmap)

- [ ] Suporte para Espanhol (ES)
- [ ] Suporte para Francês (FR)
- [ ] Suporte para Chinês (ZH)
- [ ] Service Worker para offline
- [ ] Integração com Cloudflare Workers
- [ ] Dashboard de analytics de idiomas
- [ ] Traduções automáticas via API (Google Translate)
- [ ] RTL (Right-to-Left) para árabe/hebraico

---

## 📚 Referências

- [RFC 7231 - Accept-Language](https://tools.ietf.org/html/rfc7231#section-5.3.5)
- [Cloudflare CF-IPCountry Header](https://developers.cloudflare.com/workers/runtime-apis/web-crypto/)
- [MDN - Internationalization (i18n)](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Internationalization)
- [MaxMind GeoIP2](https://www.maxmind.com/en/geoip2-services-and-databases)

---

## 📝 Licença

MIT License - Livre para usar em projetos comerciais

---

**Versão:** 1.0.0  
**Última Atualização:** 9 de Dezembro, 2025  
**Status:** Production Ready ✅
