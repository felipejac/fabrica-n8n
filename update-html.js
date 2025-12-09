#!/usr/bin/env node

/**
 * 🔄 AUTOMATIONS COOKBOOK - BULK HTML UPDATER
 * 
 * Script para atualizar 13.000+ páginas HTML em massa:
 * - Rebranding completo para "Automations Cookbook"
 * - SEO on-page (title, meta description)
 * - CTAs padronizados (download JSON + consultoria)
 * - Internal linking automático entre páginas relacionadas
 * - Estrutura de conteúdo padronizada
 * 
 * Uso: node update-html.js [--dry-run]
 */

const fs = require('fs');
const path = require('path');
const cheerio = require('cheerio');
const { glob } = require('glob');

// ============================================================================
// 📌 CONFIGURAÇÕES - CUSTOMIZE AQUI
// ============================================================================

const CONFIG = {
  // Diretório base com os arquivos HTML
  INPUT_DIR: './integracoes',
  
  // Também processar index.html e outros na raiz
  ALSO_PROCESS_ROOT: true,
  
  // Nova marca
  BRAND_NAME: 'Automations Cookbook',
  DOMAIN: 'automationscookbook.com',
  
  // Marca antiga para substituir
  OLD_BRAND_PATTERNS: [
    'AI Factory',
    'AIfactory',
    'ai-factory',
    'fabrica-n8n',
    'Fábrica de Automações'
  ],
  
  // Link para CTA de consultoria
  CONSULTORIA_LINK: 'https://forms.gle/automations-cookbook-consulting',
  
  // Meta description padrão (quando não houver conteúdo suficiente)
  DEFAULT_META_DESC: 'Aprenda passo a passo como montar esta automação e baixe o template JSON pronto no Automations Cookbook, sua biblioteca de workflows de marketing, vendas e suporte.',
  
  // Modo dry-run (não salva arquivos)
  DRY_RUN: process.argv.includes('--dry-run')
};

// ============================================================================
// 📊 ESTATÍSTICAS GLOBAIS
// ============================================================================

const stats = {
  filesProcessed: 0,
  brandUpdated: 0,
  titleUpdated: 0,
  metaDescAdded: 0,
  ctasAdded: 0,
  relatedLinksAdded: 0,
  structureFixed: 0,
  errors: []
};

// ============================================================================
// 🗺️ MAPA DE PÁGINAS PARA INTERNAL LINKING
// ============================================================================

let pagesMap = {
  all: [],           // Lista de todas as páginas
  bySoftwareA: {},   // Índice por software de origem
  bySoftwareB: {}    // Índice por software de destino
};

// ============================================================================
// 🔧 FUNÇÕES UTILITÁRIAS
// ============================================================================

/**
 * Extrai software_a e software_b do nome do arquivo
 * Exemplo: "facebook-ads-para-whatsapp-chatwoot-n8n.html"
 * -> { softwareA: "facebook-ads", softwareB: "whatsapp-chatwoot" }
 */
function extractSoftwareNames(filename) {
  const name = path.basename(filename, '.html');
  const match = name.match(/^(.+?)-para-(.+?)(?:-n8n)?$/);
  
  if (match) {
    return {
      softwareA: match[1].trim(),
      softwareB: match[2].replace(/-n8n$/, '').trim()
    };
  }
  
  return { softwareA: null, softwareB: null };
}

/**
 * Cria nome amigável a partir do slug
 * "facebook-ads" -> "Facebook Ads"
 */
function slugToTitle(slug) {
  if (!slug) return '';
  return slug
    .split('-')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}

/**
 * Trunca texto para meta description (120-160 caracteres)
 */
function truncateForMeta(text, maxLength = 155) {
  text = text.trim().replace(/\s+/g, ' ');
  if (text.length <= maxLength) return text;
  
  const truncated = text.substring(0, maxLength);
  const lastSpace = truncated.lastIndexOf(' ');
  return truncated.substring(0, lastSpace) + '...';
}

/**
 * Substitui marca antiga por nova em todo o HTML
 */
function replaceBrand($, html) {
  let updated = html;
  let hasChanges = false;
  
  CONFIG.OLD_BRAND_PATTERNS.forEach(oldBrand => {
    const regex = new RegExp(oldBrand, 'gi');
    if (regex.test(updated)) {
      updated = updated.replace(regex, CONFIG.BRAND_NAME);
      hasChanges = true;
    }
  });
  
  return { html: updated, changed: hasChanges };
}

// ============================================================================
// 🔨 FUNÇÕES DE ATUALIZAÇÃO DE CONTEÚDO
// ============================================================================

/**
 * 1. Atualiza <title> com padrão: "{{H1}} | Automations Cookbook"
 */
function updateTitle($, filepath) {
  let h1Text = $('h1').first().text().trim();
  
  if (!h1Text) {
    // Fallback: usar nome do arquivo
    const basename = path.basename(filepath, '.html');
    h1Text = slugToTitle(basename.replace(/-n8n$/, '').replace(/-para-/, ' para '));
  }
  
  const newTitle = `${h1Text} | ${CONFIG.BRAND_NAME}`;
  
  if ($('title').length === 0) {
    $('head').prepend('<title></title>');
  }
  
  const oldTitle = $('title').text();
  if (oldTitle !== newTitle) {
    $('title').text(newTitle);
    return true;
  }
  
  return false;
}

/**
 * 2. Atualiza ou cria <meta name="description">
 */
function updateMetaDescription($, filepath) {
  let description = '';
  
  // Tentar extrair descrição do primeiro parágrafo após h1
  const firstP = $('h1').first().nextAll('p').first().text().trim();
  
  if (firstP && firstP.length > 50) {
    description = truncateForMeta(firstP);
  } else {
    // Usar descrição padrão
    description = CONFIG.DEFAULT_META_DESC;
  }
  
  let metaDesc = $('meta[name="description"]');
  
  if (metaDesc.length === 0) {
    $('head').append(`<meta name="description" content="${description}">`);
    return true;
  } else if (metaDesc.attr('content') !== description) {
    metaDesc.attr('content', description);
    return true;
  }
  
  return false;
}

/**
 * 3. Garante estrutura padrão de conteúdo no <main>
 */
function ensureStandardStructure($, filepath) {
  const main = $('main').first();
  if (main.length === 0) return false;
  
  let hasChanges = false;
  const h1 = main.find('h1').first();
  
  if (h1.length === 0) {
    // Se não tem H1, criar um baseado no filename
    const basename = path.basename(filepath, '.html');
    const title = slugToTitle(basename.replace(/-n8n$/, '').replace(/-para-/, ' para '));
    main.prepend(`<h1>${title}</h1>`);
    hasChanges = true;
  }
  
  // Verificar se já tem "Visão geral do fluxo"
  if (main.find('h2:contains("Visão geral")').length === 0) {
    const { softwareA, softwareB } = extractSoftwareNames(filepath);
    const overview = `
      <h2>Visão geral do fluxo</h2>
      <p>Este fluxo de automação conecta ${slugToTitle(softwareA)} com ${slugToTitle(softwareB)}, permitindo sincronização automática de dados e ações entre as duas plataformas.</p>
    `;
    h1.after(overview);
    hasChanges = true;
  }
  
  // Verificar "Pré-requisitos"
  if (main.find('h2:contains("Pré-requisitos")').length === 0) {
    const prereqs = `
      <h2>Pré-requisitos</h2>
      <ul>
        <li>Conta ativa no software de origem</li>
        <li>Conta ativa no software de destino</li>
        <li>Instância N8N ou plataforma de automação equivalente</li>
        <li>Chaves de API / tokens de autenticação necessários</li>
      </ul>
    `;
    
    // Inserir antes do primeiro h2 ou após overview
    const firstH2 = main.find('h2').first();
    if (firstH2.length > 0) {
      firstH2.after(prereqs);
    } else {
      main.append(prereqs);
    }
    hasChanges = true;
  }
  
  // Verificar "Passo a passo"
  if (main.find('h2:contains("Passo a passo")').length === 0) {
    const steps = `
      <h2>Passo a passo no N8N</h2>
      <ol>
        <li>Crie um novo workflow no N8N</li>
        <li>Adicione o gatilho (trigger) do software de origem</li>
        <li>Configure a autenticação e eventos</li>
        <li>Adicione a ação no software de destino</li>
        <li>Mapeie os campos entre origem e destino</li>
        <li>Teste o fluxo com dados reais</li>
        <li>Ative o workflow</li>
      </ol>
    `;
    main.append(steps);
    hasChanges = true;
  }
  
  // Verificar "Variações avançadas"
  if (main.find('h2:contains("Variações")').length === 0) {
    const variations = `
      <h2>Variações avançadas</h2>
      <ul>
        <li>Adicionar registro de log em Google Sheets para auditoria</li>
        <li>Enviar notificação em Slack quando ocorrer erro</li>
        <li>Enriquecer dados com OpenAI antes de enviar</li>
      </ul>
    `;
    main.append(variations);
    hasChanges = true;
  }
  
  return hasChanges;
}

/**
 * 4. Adiciona CTAs padronizados (download JSON + consultoria)
 */
function addCTAs($, filepath) {
  const main = $('main').first();
  if (main.length === 0) return false;
  
  let hasChanges = false;
  
  // Procurar link existente para JSON
  const existingJsonLink = main.find('a[href*=".json"]').first();
  let jsonUrl = existingJsonLink.attr('href') || '#';
  
  // Se não encontrou, tentar criar URL baseada no filename
  if (jsonUrl === '#') {
    const basename = path.basename(filepath, '.html');
    jsonUrl = `./workflows/${basename}.json`;
  }
  
  // Verificar se já existem os CTAs
  if ($('#cta-download-json').length === 0) {
    // Adicionar seção de download
    const downloadSection = `
      <section class="download-section" style="margin: 2rem 0; padding: 1.5rem; background: #f8f9fa; border-radius: 8px;">
        <h2>Baixar template JSON</h2>
        <p>Baixe o template pronto e importe direto no seu N8N:</p>
        <div style="display: flex; gap: 1rem; flex-wrap: wrap; margin-top: 1rem;">
          <a id="cta-download-json" 
             class="btn btn-primary" 
             href="${jsonUrl}" 
             target="_blank" 
             rel="noopener"
             style="display: inline-block; padding: 0.75rem 1.5rem; background: #0066cc; color: white; text-decoration: none; border-radius: 4px; font-weight: 600;">
            📥 Baixar JSON deste fluxo
          </a>
          <a id="cta-consultoria" 
             class="btn btn-secondary" 
             href="${CONFIG.CONSULTORIA_LINK}" 
             target="_blank" 
             rel="noopener"
             style="display: inline-block; padding: 0.75rem 1.5rem; background: #28a745; color: white; text-decoration: none; border-radius: 4px; font-weight: 600;">
            💬 Quero ajuda para adaptar este fluxo
          </a>
        </div>
      </section>
    `;
    
    // Inserir antes de "Variações avançadas" ou no final do main
    const variationsH2 = main.find('h2:contains("Variações")').first();
    if (variationsH2.length > 0) {
      variationsH2.before(downloadSection);
    } else {
      main.append(downloadSection);
    }
    
    hasChanges = true;
  } else {
    // CTAs já existem, apenas atualizar URLs se necessário
    const downloadBtn = $('#cta-download-json');
    const consultoriaBtn = $('#cta-consultoria');
    
    if (downloadBtn.attr('href') !== jsonUrl) {
      downloadBtn.attr('href', jsonUrl);
      hasChanges = true;
    }
    
    if (consultoriaBtn.attr('href') !== CONFIG.CONSULTORIA_LINK) {
      consultoriaBtn.attr('href', CONFIG.CONSULTORIA_LINK);
      hasChanges = true;
    }
  }
  
  return hasChanges;
}

/**
 * 5. Adiciona internal linking para páginas relacionadas
 */
function addRelatedLinks($, filepath) {
  const main = $('main').first();
  if (main.length === 0) return false;
  
  // Se já existe seção de relacionados, não duplicar
  if (main.find('.related-integrations').length > 0) {
    return false;
  }
  
  const { softwareA, softwareB } = extractSoftwareNames(filepath);
  if (!softwareA && !softwareB) return false;
  
  // Buscar até 3 páginas relacionadas
  const related = [];
  const currentBasename = path.basename(filepath);
  
  // Páginas com mesmo software A
  if (softwareA && pagesMap.bySoftwareA[softwareA]) {
    const candidates = pagesMap.bySoftwareA[softwareA]
      .filter(p => p.filename !== currentBasename)
      .slice(0, 2);
    related.push(...candidates);
  }
  
  // Páginas com mesmo software B (se ainda não temos 3)
  if (related.length < 3 && softwareB && pagesMap.bySoftwareB[softwareB]) {
    const candidates = pagesMap.bySoftwareB[softwareB]
      .filter(p => p.filename !== currentBasename)
      .filter(p => !related.find(r => r.filename === p.filename))
      .slice(0, 3 - related.length);
    related.push(...candidates);
  }
  
  // Se não encontrou relacionados, pegar páginas aleatórias
  if (related.length === 0) {
    const allPages = pagesMap.all.filter(p => p.filename !== currentBasename);
    const randomPages = allPages
      .sort(() => Math.random() - 0.5)
      .slice(0, 3);
    related.push(...randomPages);
  }
  
  if (related.length === 0) return false;
  
  // Construir HTML da seção de relacionados
  const relatedLinksHTML = `
    <section class="related-integrations" style="margin: 3rem 0; padding: 2rem; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #0066cc;">
      <h2>🔗 Outras integrações relacionadas no ${CONFIG.BRAND_NAME}</h2>
      <ul style="list-style: none; padding: 0; margin: 1rem 0;">
        ${related.map(page => `
          <li style="margin: 0.75rem 0;">
            <a href="${page.relativePath}" style="color: #0066cc; text-decoration: none; font-weight: 500; display: inline-flex; align-items: center; gap: 0.5rem;">
              → ${page.title}
            </a>
          </li>
        `).join('\n')}
      </ul>
    </section>
  `;
  
  // Adicionar no final do main
  main.append(relatedLinksHTML);
  return true;
}

// ============================================================================
// 🚀 FUNÇÃO PRINCIPAL DE PROCESSAMENTO
// ============================================================================

/**
 * Processa um único arquivo HTML
 */
function processHTMLFile(filepath) {
  try {
    console.log(`\n📄 Processando: ${path.relative(process.cwd(), filepath)}`);
    
    // Skip homepage files (not integration pages)
    const basename = path.basename(filepath);
    if (basename === 'index.html' && !filepath.includes('integracoes/')) {
      console.log('  ⏭️  Pulando homepage (não é página de integração)');
      stats.filesProcessed++;
      return;
    }
    
    // Ler arquivo
    let html = fs.readFileSync(filepath, 'utf-8');
    
    // Carregar com cheerio
    let $ = cheerio.load(html, {
      decodeEntities: false,
      xmlMode: false
    });
    
    let fileChanged = false;
    
    // 1. Substituir marca antiga
    const brandResult = replaceBrand($, html);
    if (brandResult.changed) {
      html = brandResult.html;
      $ = cheerio.load(html, { decodeEntities: false });
      stats.brandUpdated++;
      fileChanged = true;
      console.log('  ✓ Marca atualizada');
    }
    
    // 2. Atualizar <title>
    if (updateTitle($, filepath)) {
      stats.titleUpdated++;
      fileChanged = true;
      console.log('  ✓ Title atualizado');
    }
    
    // 3. Atualizar <meta description>
    if (updateMetaDescription($, filepath)) {
      stats.metaDescAdded++;
      fileChanged = true;
      console.log('  ✓ Meta description atualizada');
    }
    
    // 4. Garantir estrutura padrão
    if (ensureStandardStructure($, filepath)) {
      stats.structureFixed++;
      fileChanged = true;
      console.log('  ✓ Estrutura de conteúdo padronizada');
    }
    
    // 5. Adicionar CTAs
    if (addCTAs($, filepath)) {
      stats.ctasAdded++;
      fileChanged = true;
      console.log('  ✓ CTAs adicionados');
    }
    
    // 6. Adicionar links relacionados
    if (addRelatedLinks($, filepath)) {
      stats.relatedLinksAdded++;
      fileChanged = true;
      console.log('  ✓ Links relacionados adicionados');
    }
    
    // Salvar arquivo (se não for dry-run e houve mudanças)
    if (fileChanged && !CONFIG.DRY_RUN) {
      fs.writeFileSync(filepath, $.html(), 'utf-8');
      console.log('  💾 Arquivo salvo');
    } else if (fileChanged && CONFIG.DRY_RUN) {
      console.log('  🔍 [DRY-RUN] Arquivo seria salvo');
    } else {
      console.log('  ⏭️  Nenhuma alteração necessária');
    }
    
    stats.filesProcessed++;
    
  } catch (error) {
    console.error(`  ❌ Erro ao processar ${filepath}:`, error.message);
    stats.errors.push({ file: filepath, error: error.message });
  }
}

// ============================================================================
// 🗺️ MAPEAMENTO DE PÁGINAS
// ============================================================================

/**
 * Mapeia todas as páginas HTML para criar índice de internal linking
 */
async function mapAllPages(htmlFiles) {
  console.log('\n🗺️  Mapeando páginas para internal linking...\n');
  
  htmlFiles.forEach(filepath => {
    const basename = path.basename(filepath);
    const { softwareA, softwareB } = extractSoftwareNames(filepath);
    
    // Ler título da página
    try {
      const html = fs.readFileSync(filepath, 'utf-8');
      const $ = cheerio.load(html);
      const title = $('title').text() || $('h1').first().text() || slugToTitle(basename.replace('.html', ''));
      
      const pageInfo = {
        filename: basename,
        filepath: filepath,
        relativePath: './' + basename,
        title: title.replace(` | ${CONFIG.BRAND_NAME}`, '').trim(),
        softwareA,
        softwareB
      };
      
      pagesMap.all.push(pageInfo);
      
      // Indexar por software A
      if (softwareA) {
        if (!pagesMap.bySoftwareA[softwareA]) {
          pagesMap.bySoftwareA[softwareA] = [];
        }
        pagesMap.bySoftwareA[softwareA].push(pageInfo);
      }
      
      // Indexar por software B
      if (softwareB) {
        if (!pagesMap.bySoftwareB[softwareB]) {
          pagesMap.bySoftwareB[softwareB] = [];
        }
        pagesMap.bySoftwareB[softwareB].push(pageInfo);
      }
      
    } catch (error) {
      console.error(`Erro ao mapear ${basename}:`, error.message);
    }
  });
  
  console.log(`✓ ${pagesMap.all.length} páginas mapeadas`);
  console.log(`✓ ${Object.keys(pagesMap.bySoftwareA).length} softwares de origem indexados`);
  console.log(`✓ ${Object.keys(pagesMap.bySoftwareB).length} softwares de destino indexados`);
}

// ============================================================================
// 🎯 MAIN - EXECUÇÃO PRINCIPAL
// ============================================================================

async function main() {
  console.log(`
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   🔄 AUTOMATIONS COOKBOOK - BULK HTML UPDATER                ║
║                                                               ║
║   Atualizando 13k+ páginas HTML com nova marca e SEO         ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
  `);
  
  if (CONFIG.DRY_RUN) {
    console.log('⚠️  MODO DRY-RUN ATIVO - Nenhum arquivo será modificado\n');
  }
  
  console.log('📌 Configurações:');
  console.log(`   Diretório: ${CONFIG.INPUT_DIR}`);
  console.log(`   Nova marca: ${CONFIG.BRAND_NAME}`);
  console.log(`   Domínio: ${CONFIG.DOMAIN}`);
  console.log(`   Link consultoria: ${CONFIG.CONSULTORIA_LINK}\n`);
  
  try {
    // 1. Buscar todos os arquivos HTML
    console.log('🔍 Buscando arquivos HTML...\n');
    
    const patterns = [
      path.join(CONFIG.INPUT_DIR, '**/*.html'),
    ];
    
    if (CONFIG.ALSO_PROCESS_ROOT) {
      patterns.push('./index.html');
      patterns.push('./translated/en/index.html');
    }
    
    const htmlFiles = [];
    for (const pattern of patterns) {
      const files = await glob(pattern, { ignore: ['**/node_modules/**', '**/dist/**'] });
      htmlFiles.push(...files);
    }
    
    console.log(`✓ ${htmlFiles.length} arquivos HTML encontrados\n`);
    
    if (htmlFiles.length === 0) {
      console.log('❌ Nenhum arquivo HTML encontrado. Verifique o INPUT_DIR.');
      process.exit(1);
    }
    
    // 2. Mapear páginas para internal linking
    await mapAllPages(htmlFiles);
    
    // 3. Processar cada arquivo
    console.log('\n🚀 Iniciando processamento em massa...\n');
    console.log('═'.repeat(70));
    
    for (const filepath of htmlFiles) {
      processHTMLFile(filepath);
    }
    
    // 4. Exibir estatísticas finais
    console.log('\n' + '═'.repeat(70));
    console.log('\n📊 ESTATÍSTICAS FINAIS\n');
    console.log(`✓ Arquivos processados:        ${stats.filesProcessed}`);
    console.log(`✓ Branding atualizado:         ${stats.brandUpdated}`);
    console.log(`✓ Titles atualizados:          ${stats.titleUpdated}`);
    console.log(`✓ Meta descriptions adicionadas: ${stats.metaDescAdded}`);
    console.log(`✓ CTAs adicionados:            ${stats.ctasAdded}`);
    console.log(`✓ Links relacionados adicionados: ${stats.relatedLinksAdded}`);
    console.log(`✓ Estruturas padronizadas:     ${stats.structureFixed}`);
    
    if (stats.errors.length > 0) {
      console.log(`\n⚠️  Erros encontrados: ${stats.errors.length}`);
      stats.errors.forEach(err => {
        console.log(`   - ${err.file}: ${err.error}`);
      });
    }
    
    console.log('\n✅ Processo concluído com sucesso!\n');
    
    if (CONFIG.DRY_RUN) {
      console.log('💡 Execute sem --dry-run para aplicar as alterações.\n');
    }
    
  } catch (error) {
    console.error('\n❌ Erro fatal:', error);
    process.exit(1);
  }
}

// Executar
main();
