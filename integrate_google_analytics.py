#!/usr/bin/env python3
"""
Integra Google Analytics 4 (GA4) em todas as páginas HTML do site

Este script adiciona:
1. Tag Google Analytics 4 no <head>
2. Configuração de eventos personalizados
3. Tracking de conversões (download template, scroll, tempo na página)
4. Enhanced measurements

Uso:
    python integrate_google_analytics.py --measurement-id G-XXXXXXXXXX
    python integrate_google_analytics.py --measurement-id G-XXXXXXXXXX --dry-run
"""

import os
import sys
import re
from pathlib import Path
import argparse
import logging
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class GoogleAnalyticsIntegrator:
    """Integra Google Analytics 4 em páginas HTML"""
    
    def __init__(self, measurement_id: str, dry_run: bool = False):
        self.measurement_id = measurement_id
        self.dry_run = dry_run
        self.files_processed = 0
        self.files_updated = 0
        self.files_skipped = 0
        
    def generate_ga4_snippet(self) -> str:
        """Gera snippet do Google Analytics 4"""
        return f"""
<!-- Google Analytics 4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id={self.measurement_id}"></script>
<script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    
    // Configuração básica
    gtag('config', '{self.measurement_id}', {{
        'send_page_view': true,
        'anonymize_ip': true,
        'allow_google_signals': true,
        'allow_ad_personalization_signals': false
    }});
    
    // Eventos personalizados para templates
    document.addEventListener('DOMContentLoaded', function() {{
        
        // Track download de template (clique em botões de download)
        const downloadButtons = document.querySelectorAll('a[href*=".json"], button[class*="download"], a[class*="download"]');
        downloadButtons.forEach(function(btn) {{
            btn.addEventListener('click', function(e) {{
                gtag('event', 'template_download', {{
                    'event_category': 'engagement',
                    'event_label': window.location.pathname,
                    'value': 1
                }});
            }});
        }});
        
        // Track scroll depth (75% da página)
        let scrollTracked = false;
        window.addEventListener('scroll', function() {{
            if (scrollTracked) return;
            
            const scrollPercent = (window.scrollY + window.innerHeight) / document.documentElement.scrollHeight * 100;
            if (scrollPercent >= 75) {{
                gtag('event', 'scroll', {{
                    'event_category': 'engagement',
                    'event_label': '75_percent',
                    'value': 75
                }});
                scrollTracked = true;
            }}
        }});
        
        // Track tempo na página (2+ minutos = engajamento alto)
        setTimeout(function() {{
            gtag('event', 'time_on_page', {{
                'event_category': 'engagement',
                'event_label': '2_minutes',
                'value': 120
            }});
        }}, 120000); // 2 minutos
        
        // Track clique em links internos (navegação)
        const internalLinks = document.querySelectorAll('a[href^="/"], a[href^="./"]');
        internalLinks.forEach(function(link) {{
            link.addEventListener('click', function(e) {{
                gtag('event', 'internal_navigation', {{
                    'event_category': 'navigation',
                    'event_label': this.getAttribute('href'),
                    'value': 1
                }});
            }});
        }});
        
        // Track expansão de FAQ (se existir)
        const faqItems = document.querySelectorAll('details.faq-item');
        faqItems.forEach(function(item, index) {{
            item.addEventListener('toggle', function() {{
                if (this.open) {{
                    gtag('event', 'faq_expansion', {{
                        'event_category': 'engagement',
                        'event_label': 'faq_item_' + (index + 1),
                        'value': 1
                    }});
                }}
            }});
        }});
        
        // Track copy de prompt LLM (se existir)
        const llmSection = document.querySelector('.llm-friendly');
        if (llmSection) {{
            const promptBox = llmSection.querySelector('div[style*="monospace"]');
            if (promptBox) {{
                promptBox.addEventListener('click', function() {{
                    gtag('event', 'llm_prompt_interaction', {{
                        'event_category': 'engagement',
                        'event_label': 'prompt_clicked',
                        'value': 1
                    }});
                }});
            }}
        }}
    }});
</script>
"""
    
    def has_ga4(self, html_content: str) -> bool:
        """Verifica se já possui GA4"""
        return 'googletagmanager.com/gtag/js' in html_content or \
               f'gtag/js?id={self.measurement_id}' in html_content
    
    def integrate_ga4(self, filepath: str) -> bool:
        """Integra GA4 em um arquivo HTML"""
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Verificar se já tem GA4
            if self.has_ga4(html_content):
                logger.info(f"   ⏭️  Já possui GA4: {os.path.basename(filepath)}")
                self.files_skipped += 1
                return False
            
            soup = BeautifulSoup(html_content, 'html.parser')
            head = soup.find('head')
            
            if not head:
                logger.warning(f"   ⚠️  Sem <head>: {os.path.basename(filepath)}")
                return False
            
            # Gerar snippet GA4
            ga4_snippet = self.generate_ga4_snippet()
            
            # Inserir antes do </head>
            ga4_tag = BeautifulSoup(ga4_snippet, 'html.parser')
            head.append(ga4_tag)
            
            # Salvar se não for dry-run
            if not self.dry_run:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(str(soup))
                logger.info(f"   ✅ Integrado: {os.path.basename(filepath)}")
                self.files_updated += 1
            else:
                logger.info(f"   🔍 Seria integrado: {os.path.basename(filepath)}")
            
            return True
            
        except Exception as e:
            logger.error(f"   ❌ Erro em {os.path.basename(filepath)}: {e}")
            return False
    
    def process_directory(self, directory: str, pattern: str = "*.html"):
        """Processa todos os HTMLs de um diretório"""
        
        logger.info(f"\n📂 Processando diretório: {directory}")
        
        path = Path(directory)
        html_files = list(path.glob(pattern))
        
        if not html_files:
            logger.info(f"   ℹ️  Nenhum arquivo HTML encontrado")
            return
        
        logger.info(f"   📄 Encontrados {len(html_files)} arquivos HTML")
        
        for filepath in html_files:
            self.files_processed += 1
            self.integrate_ga4(str(filepath))
    
    def process_all(self):
        """Processa todas as páginas do site"""
        
        logger.info("=" * 80)
        logger.info("🚀 INTEGRAÇÃO GOOGLE ANALYTICS 4")
        logger.info("=" * 80)
        logger.info(f"Measurement ID: {self.measurement_id}")
        logger.info(f"Modo: {'DRY-RUN (sem alterações)' if self.dry_run else 'PRODUÇÃO (aplicando mudanças)'}")
        logger.info("")
        
        # Processar páginas principais
        self.process_directory('.', '*.html')
        
        # Processar diretórios
        directories = [
            'integracoes',
            'integracoes-zapier',
            'blog',
            'ferramentas',
        ]
        
        for directory in directories:
            if os.path.exists(directory):
                self.process_directory(directory)
        
        # Resumo
        self._print_summary()
    
    def _print_summary(self):
        """Imprime resumo da execução"""
        logger.info("")
        logger.info("=" * 80)
        logger.info("📊 RESUMO DA INTEGRAÇÃO")
        logger.info("=" * 80)
        logger.info(f"Arquivos processados: {self.files_processed}")
        logger.info(f"Arquivos atualizados: {self.files_updated}")
        logger.info(f"Arquivos pulados (já tinham GA4): {self.files_skipped}")
        logger.info("")
        
        if self.dry_run:
            logger.info("⚠️  DRY-RUN: Nenhuma alteração foi salva")
            logger.info("   Execute sem --dry-run para aplicar as mudanças")
        else:
            logger.info("✅ Integração concluída com sucesso!")
            logger.info("")
            logger.info("📋 PRÓXIMOS PASSOS:")
            logger.info("   1. Criar propriedade GA4 em: https://analytics.google.com")
            logger.info("   2. Copiar Measurement ID (formato: G-XXXXXXXXXX)")
            logger.info("   3. Verificar instalação em: https://analytics.google.com/analytics/web/")
            logger.info("   4. Aguardar 24-48h para primeiros dados")
        
        logger.info("=" * 80)


def main():
    parser = argparse.ArgumentParser(description='Integra Google Analytics 4 no site')
    parser.add_argument('--measurement-id', required=True, help='GA4 Measurement ID (ex: G-XXXXXXXXXX)')
    parser.add_argument('--dry-run', action='store_true', help='Simular sem salvar alterações')
    
    args = parser.parse_args()
    
    # Validar Measurement ID
    if not re.match(r'^G-[A-Z0-9]{10}$', args.measurement_id):
        logger.error("❌ Measurement ID inválido. Formato esperado: G-XXXXXXXXXX")
        logger.error("   Exemplo: G-ABC1234567")
        sys.exit(1)
    
    # Executar integração
    integrator = GoogleAnalyticsIntegrator(args.measurement_id, args.dry_run)
    integrator.process_all()


if __name__ == "__main__":
    main()
