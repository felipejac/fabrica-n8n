# 🔄 Automations Cookbook - Bulk HTML Updater

Script Node.js para atualizar **13.000+ páginas HTML** em massa com a nova marca **Automations Cookbook**, incluindo rebranding completo, SEO on-page, CTAs padronizados e internal linking automático.

## 📋 Índice

- [Características](#características)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
- [O que o script faz](#o-que-o-script-faz)
- [Estrutura dos arquivos](#estrutura-dos-arquivos)
- [Solução de problemas](#solução-de-problemas)

## ✨ Características

### 🎨 Rebranding Completo
- Substitui "AI Factory" e outras marcas antigas por "Automations Cookbook"
- Atualiza domínio de `fabrica-n8n` para `automationscookbook.com`
- Aplica mudanças em título, header, footer e conteúdo

### 🔍 SEO On-Page
- **Meta Title**: Padrão `"{{H1}} | Automations Cookbook"`
- **Meta Description**: Extraída do conteúdo ou gerada automaticamente (120-160 caracteres)
- **Headings**: Estrutura H1 + H2 padronizada
- **Internal Linking**: 3 links relacionados por página

### 📄 Estrutura de Conteúdo Padronizada
Cada página de template recebe:
1. H1 principal (título da automação)
2. **Visão geral do fluxo** - resumo da integração
3. **Pré-requisitos** - lista de contas/APIs necessárias
4. **Passo a passo no N8N** - guia de implementação
5. **Baixar template JSON** - seção com CTAs
6. **Variações avançadas** - ideias de expansão
7. **Integrações relacionadas** - internal linking

### 🎯 CTAs Padronizados
- **Botão de Download**: Link direto para arquivo JSON do workflow
- **Botão de Consultoria**: Link para formulário de contato/consultoria
- Design responsivo e estilizado inline

### 🔗 Internal Linking Automático
- Mapeia todas as páginas por software de origem e destino
- Adiciona 3 links relacionados em cada página
- Melhora SEO e navegação do usuário

## 📦 Pré-requisitos

- **Node.js** v16 ou superior
- **npm** ou **yarn**

## 🚀 Instalação

### 1. Clone ou navegue até o diretório do projeto

```bash
cd /seu-projeto/fabrica-n8n
```

### 2. Instale as dependências

```bash
npm install
```

Isso instalará:
- `cheerio` (^1.0.0-rc.12) - Parser HTML/DOM manipulation
- `glob` (^10.3.10) - Pattern matching de arquivos

## ⚙️ Configuração

Edite o arquivo `update-html.js` e ajuste as constantes no objeto `CONFIG`:

```javascript
const CONFIG = {
  // Diretório base com os arquivos HTML
  INPUT_DIR: './integracoes',
  
  // Processar também index.html e docs na raiz
  ALSO_PROCESS_ROOT: true,
  
  // Nova marca
  BRAND_NAME: 'Automations Cookbook',
  DOMAIN: 'automationscookbook.com',
  
  // Marcas antigas para substituir
  OLD_BRAND_PATTERNS: [
    'AI Factory',
    'AIfactory',
    'ai-factory',
    'fabrica-n8n',
    'Fábrica de Automações'
  ],
  
  // Link para CTA de consultoria (CUSTOMIZE AQUI!)
  CONSULTORIA_LINK: 'https://forms.gle/automations-cookbook-consulting',
  
  // Meta description padrão
  DEFAULT_META_DESC: 'Aprenda passo a passo como montar esta automação...',
};
```

### 🔧 Principais configurações a ajustar:

| Configuração | Descrição | Exemplo |
|--------------|-----------|---------|
| `INPUT_DIR` | Pasta com os arquivos HTML | `'./integracoes'` |
| `CONSULTORIA_LINK` | URL do formulário de consultoria | `'https://typeform.com/...'` |
| `OLD_BRAND_PATTERNS` | Variações da marca antiga | `['AI Factory', 'ai-factory']` |

## 🎯 Uso

### Teste primeiro com dry-run (recomendado)

```bash
npm run test
# ou
node update-html.js --dry-run
```

Isso executará o script **SEM SALVAR** alterações, mostrando o que seria feito.

### Executar atualização completa

```bash
npm run update
# ou
node update-html.js
```

### Saída esperada

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   🔄 AUTOMATIONS COOKBOOK - BULK HTML UPDATER                ║
║                                                               ║
║   Atualizando 13k+ páginas HTML com nova marca e SEO         ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

📌 Configurações:
   Diretório: ./integracoes
   Nova marca: Automations Cookbook
   Domínio: automationscookbook.com
   Link consultoria: https://forms.gle/...

🔍 Buscando arquivos HTML...

✓ 13,247 arquivos HTML encontrados

🗺️  Mapeando páginas para internal linking...

✓ 13,247 páginas mapeadas
✓ 156 softwares de origem indexados
✓ 189 softwares de destino indexados

🚀 Iniciando processamento em massa...

═══════════════════════════════════════════════════════════════

📄 Processando: integracoes/facebook-ads-para-whatsapp-chatwoot-n8n.html
  ✓ Marca atualizada
  ✓ Title atualizado
  ✓ Meta description atualizada
  ✓ Estrutura de conteúdo padronizada
  ✓ CTAs adicionados
  ✓ Links relacionados adicionados
  💾 Arquivo salvo

[... continua para todas as páginas ...]

═══════════════════════════════════════════════════════════════

📊 ESTATÍSTICAS FINAIS

✓ Arquivos processados:          13,247
✓ Branding atualizado:            13,247
✓ Titles atualizados:             13,247
✓ Meta descriptions adicionadas:  13,247
✓ CTAs adicionados:               13,247
✓ Links relacionados adicionados: 13,247
✓ Estruturas padronizadas:        13,247

✅ Processo concluído com sucesso!
```

## 🔍 O que o script faz

### Para cada arquivo HTML processado:

#### 1️⃣ **Atualização de Branding**
```html
<!-- ANTES -->
<title>Facebook Ads para WhatsApp | AI Factory</title>

<!-- DEPOIS -->
<title>Facebook Ads para WhatsApp Chatwoot | Automations Cookbook</title>
```

#### 2️⃣ **Meta Description**
```html
<!-- ANTES -->
<meta name="description" content="">

<!-- DEPOIS -->
<meta name="description" content="Aprenda passo a passo como montar esta automação e baixe o template JSON pronto no Automations Cookbook, sua biblioteca de workflows...">
```

#### 3️⃣ **Estrutura de Conteúdo**
```html
<main>
  <h1>Facebook Ads para WhatsApp Chatwoot</h1>
  
  <h2>Visão geral do fluxo</h2>
  <p>Este fluxo de automação conecta Facebook Ads com WhatsApp Chatwoot...</p>
  
  <h2>Pré-requisitos</h2>
  <ul>
    <li>Conta ativa no software de origem</li>
    <li>Conta ativa no software de destino</li>
    <li>Instância N8N ou plataforma equivalente</li>
    <li>Chaves de API necessárias</li>
  </ul>
  
  <h2>Passo a passo no N8N</h2>
  <ol>
    <li>Crie um novo workflow no N8N</li>
    <li>Adicione o gatilho do software de origem</li>
    <!-- ... -->
  </ol>
  
  <!-- CTAs e Related Links são adicionados automaticamente -->
</main>
```

#### 4️⃣ **CTAs Padronizados**
```html
<section class="download-section">
  <h2>Baixar template JSON</h2>
  <div>
    <a id="cta-download-json" 
       href="./workflows/facebook-ads-para-whatsapp.json" 
       class="btn btn-primary">
      📥 Baixar JSON deste fluxo
    </a>
    <a id="cta-consultoria" 
       href="https://forms.gle/..." 
       class="btn btn-secondary">
      💬 Quero ajuda para adaptar este fluxo
    </a>
  </div>
</section>
```

#### 5️⃣ **Internal Linking**
```html
<section class="related-integrations">
  <h2>🔗 Outras integrações relacionadas no Automations Cookbook</h2>
  <ul>
    <li><a href="./facebook-ads-para-google-sheets-n8n.html">→ Facebook Ads para Google Sheets</a></li>
    <li><a href="./instagram-para-whatsapp-n8n.html">→ Instagram para WhatsApp</a></li>
    <li><a href="./whatsapp-para-hubspot-n8n.html">→ WhatsApp para HubSpot</a></li>
  </ul>
</section>
```

## 📁 Estrutura dos arquivos

```
fabrica-n8n/
├── package.json              # Dependências e scripts npm
├── update-html.js            # Script principal (este arquivo)
├── README.md                 # Esta documentação
├── integracoes/              # Pasta com as 13k páginas HTML
│   ├── facebook-ads-para-whatsapp-chatwoot-n8n.html
│   ├── gmail-para-openai-classificacao-n8n.html
│   └── ... (13.000+ arquivos)
├── index.html                # Homepage (também processada)
└── translated/
    └── en/
        └── index.html        # Homepage em inglês
```

## 🛠️ Solução de problemas

### Erro: "Cannot find module 'cheerio'"

```bash
npm install
```

### Erro: "No HTML files found"

Verifique se o `INPUT_DIR` está correto no `CONFIG`:

```javascript
INPUT_DIR: './integracoes',  // Caminho relativo à raiz do projeto
```

### O script está muito lento

O processamento de 13k+ arquivos pode levar **5-15 minutos** dependendo do hardware.

Para testar com subset menor:

```javascript
// No código, após buscar arquivos:
const htmlFiles = allFiles.slice(0, 100); // Processar apenas 100 arquivos
```

### Páginas não estão sendo atualizadas

1. Verifique se não está rodando em `--dry-run`
2. Confirme permissões de escrita nos arquivos
3. Rode com `node update-html.js` (sem flags)

### Links relacionados não aparecem

O script precisa de **pelo menos 2 páginas** para criar links relacionados. Em testes com poucos arquivos, pode não haver páginas relacionadas suficientes.

### CTAs estão duplicados

O script é **idempotente** e verifica se `#cta-download-json` já existe antes de adicionar. Se estiver duplicando:

1. Verifique se há CTAs com IDs diferentes no HTML original
2. Remova manualmente CTAs antigos antes de rodar o script

## 📊 Performance

### Métricas esperadas:

| Métrica | Valor |
|---------|-------|
| Arquivos/segundo | ~15-30 arquivos/segundo |
| Tempo total (13k páginas) | 7-15 minutos |
| Uso de memória | ~200-500 MB |
| Tamanho médio de arquivo | 15-50 KB |

## 🔒 Segurança

### ⚠️ IMPORTANTE - Backup antes de executar

```bash
# Crie um backup da pasta integracoes antes de rodar
cp -r integracoes integracoes_backup_$(date +%Y%m%d)
```

### O script é idempotente

Pode ser executado **múltiplas vezes** no mesmo conjunto de arquivos sem criar duplicações. Ele verifica se elementos já existem antes de adicionar.

## 🚀 Próximos passos após execução

1. **Validar HTML**: Teste algumas páginas aleatórias
2. **Testar responsividade**: Verificar mobile/desktop
3. **SEO Audit**: Rodar Lighthouse ou similar
4. **Deploy**: Fazer commit e push para produção
5. **Monitorar**: Verificar Google Search Console para erros

## 📝 Logs e Debug

Para ver logs detalhados durante execução:

```bash
node update-html.js 2>&1 | tee update-log.txt
```

Isso salvará todo o output em `update-log.txt`.

## 🤝 Contribuindo

Para modificar o comportamento do script:

1. Edite as funções específicas em `update-html.js`:
   - `updateTitle()` - Lógica de títulos
   - `updateMetaDescription()` - Meta descriptions
   - `addCTAs()` - Botões de ação
   - `addRelatedLinks()` - Internal linking

2. Teste com `--dry-run` primeiro

3. Execute em subset pequeno antes de processar todas as páginas

## 📄 Licença

MIT

## 👨‍💻 Autor

**Automations Cookbook Team**

- Website: https://automationscookbook.com
- Support: support@automationscookbook.com

---

**🎯 Pronto para começar?**

```bash
npm install
npm run test    # Dry-run primeiro
npm run update  # Atualização completa
```

✅ **Sucesso!** Suas 13k+ páginas agora estão com a nova marca, SEO otimizado e CTAs padronizados.
