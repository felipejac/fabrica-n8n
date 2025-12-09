#!/usr/bin/env node

/**
 * 🧪 VALIDAÇÃO AUTOMATIZADA - AUTOMATIONS COOKBOOK
 * 
 * Script para validar que todas as páginas foram atualizadas corretamente
 * após o rebranding para Automations Cookbook.
 */

const https = require('https');
const http = require('http');

const CONFIG = {
  DOMAIN: 'http://www.automationscookbook.com',
  PAGES_TO_TEST: [
    '/',
    '/index.html',
    '/integracoes/facebook-ads-para-google-sheets-n8n.html',
    '/integracoes/facebook-ads-para-whatsapp-chatwoot-n8n.html',
    '/integracoes/google-forms-para-whatsapp-kommo-n8n.html',
    '/integracoes/gmail-para-openai-classificacao-n8n.html',
    '/integracoes/hubspot-para-postgresql-backup-n8n.html',
  ],
  EXPECTED_BRAND: 'Automations Cookbook',
  OLD_BRAND: 'AI Factory',
};

const stats = {
  tested: 0,
  passed: 0,
  failed: 0,
  errors: []
};

/**
 * Faz requisição HTTP e retorna o HTML
 */
function fetchPage(url) {
  return new Promise((resolve, reject) => {
    const protocol = url.startsWith('https') ? https : http;
    
    protocol.get(url, (res) => {
      let data = '';
      
      res.on('data', (chunk) => {
        data += chunk;
      });
      
      res.on('end', () => {
        resolve(data);
      });
    }).on('error', (err) => {
      reject(err);
    });
  });
}

/**
 * Valida uma página
 */
async function validatePage(pagePath) {
  const url = CONFIG.DOMAIN + pagePath;
  console.log(`\n📄 Testando: ${pagePath}`);
  
  try {
    const html = await fetchPage(url);
    
    // Testes
    const tests = {
      hasNewBrand: html.includes(CONFIG.EXPECTED_BRAND),
      noOldBrand: !html.includes(CONFIG.OLD_BRAND),
      hasTitle: /<title>.*<\/title>/.test(html),
      hasMetaDesc: /<meta name="description"/.test(html),
      hasCTA: /cta-download-json/.test(html) || pagePath === '/' || pagePath === '/index.html',
    };
    
    // Verificar resultados
    const allPassed = Object.values(tests).every(v => v === true);
    
    if (allPassed) {
      console.log('  ✅ PASSOU em todos os testes');
      stats.passed++;
    } else {
      console.log('  ❌ FALHOU em alguns testes:');
      if (!tests.hasNewBrand) console.log('     - Nova marca não encontrada');
      if (!tests.noOldBrand) console.log('     - Marca antiga ainda presente');
      if (!tests.hasTitle) console.log('     - Title ausente');
      if (!tests.hasMetaDesc) console.log('     - Meta description ausente');
      if (!tests.hasCTA) console.log('     - CTA ausente');
      
      stats.failed++;
      stats.errors.push({ page: pagePath, tests });
    }
    
    // Contar ocorrências
    const newBrandCount = (html.match(new RegExp(CONFIG.EXPECTED_BRAND, 'g')) || []).length;
    const oldBrandCount = (html.match(new RegExp(CONFIG.OLD_BRAND, 'g')) || []).length;
    
    console.log(`  📊 "${CONFIG.EXPECTED_BRAND}": ${newBrandCount} ocorrências`);
    console.log(`  📊 "${CONFIG.OLD_BRAND}": ${oldBrandCount} ocorrências`);
    
    stats.tested++;
    
  } catch (error) {
    console.log(`  ❌ ERRO: ${error.message}`);
    stats.failed++;
    stats.errors.push({ page: pagePath, error: error.message });
    stats.tested++;
  }
}

/**
 * Executa todos os testes
 */
async function runAllTests() {
  console.log(`
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║   🧪 VALIDAÇÃO AUTOMATIZADA - AUTOMATIONS COOKBOOK            ║
║                                                                ║
║   Testando páginas em: ${CONFIG.DOMAIN}
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
  `);
  
  console.log(`📋 ${CONFIG.PAGES_TO_TEST.length} páginas serão testadas\n`);
  
  // Testar cada página
  for (const page of CONFIG.PAGES_TO_TEST) {
    await validatePage(page);
  }
  
  // Relatório final
  console.log('\n' + '═'.repeat(70));
  console.log('\n📊 RELATÓRIO FINAL\n');
  console.log(`✓ Páginas testadas:  ${stats.tested}`);
  console.log(`✓ Testes aprovados:  ${stats.passed} (${Math.round(stats.passed/stats.tested*100)}%)`);
  console.log(`✗ Testes falhados:   ${stats.failed}`);
  
  if (stats.errors.length > 0) {
    console.log('\n⚠️  DETALHES DOS ERROS:\n');
    stats.errors.forEach((err, i) => {
      console.log(`${i+1}. ${err.page}`);
      if (err.error) {
        console.log(`   Erro: ${err.error}`);
      } else if (err.tests) {
        console.log(`   Testes falhados: ${Object.keys(err.tests).filter(k => !err.tests[k]).join(', ')}`);
      }
    });
  }
  
  console.log('\n' + '═'.repeat(70));
  
  if (stats.passed === stats.tested) {
    console.log('\n✅ TODOS OS TESTES PASSARAM!\n');
    process.exit(0);
  } else {
    console.log('\n⚠️  ALGUNS TESTES FALHARAM. Revise os erros acima.\n');
    process.exit(1);
  }
}

// Executar
runAllTests().catch(err => {
  console.error('❌ Erro fatal:', err);
  process.exit(1);
});
