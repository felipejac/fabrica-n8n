#!/usr/bin/env python3
"""
Integra Google Tag Manager (GTM) em todas as páginas HTML do site

Este script adiciona:
1. GTM snippet no <head> (o mais alto possível)
2. GTM noscript snippet logo após <body>

Uso:
    python integrate_google_tag_manager.py
    python integrate_google_tag_manager.py --dry-run
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


class GoogleTagManagerIntegrator:
    """Integra Google Tag Manager em páginas HTML"""
    
    def __init__(self, gtm_id: str = "GTM-KVTHGKJR", dry_run: bool = False):
        self.gtm_id = gtm_id
        self.dry_run = dry_run
        self.files_processed = 0
        self.files_updated = 0
        self.files_skipped = 0
        
    def generate_gtm_head_snippet(self) -> str:
        """Gera snippet do GTM para o <head>"""
        return f"""<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','{self.gtm_id}');</script>
<!-- End Google Tag Manager -->"""
    
    def generate_gtm_body_snippet(self) -> str:
        """Gera snippet do GTM para o <body> (noscript)"""
        return f"""<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id={self.gtm_id}"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->"""
    
    def has_gtm(self, html_content: str) -> bool:
        """Verifica se a página já possui GTM"""
        return 'googletagmanager.com/gtm.js' in html_content or self.gtm_id in html_content
    
    def integrate_gtm(self, file_path: Path) -> bool:
        """
        Integra GTM em um arquivo HTML
        
        Returns:
            True se o arquivo foi atualizado, False se foi pulado
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Verificar se já tem GTM
            if self.has_gtm(content):
                logger.info(f"   ⏭️  Já possui GTM: {file_path.name}")
                self.files_skipped += 1
                return False
            
            # Parse HTML
            soup = BeautifulSoup(content, 'html.parser')
            
            # Encontrar <head>
            head = soup.find('head')
            if not head:
                logger.warning(f"   ⚠️  Sem <head>: {file_path.name}")
                return False
            
            # Encontrar <body>
            body = soup.find('body')
            if not body:
                logger.warning(f"   ⚠️  Sem <body>: {file_path.name}")
                return False
            
            # Adicionar GTM no <head> (o mais alto possível, logo após <head>)
            gtm_head_tag = BeautifulSoup(self.generate_gtm_head_snippet(), 'html.parser')
            
            # Inserir no início do <head>
            if head.contents:
                head.insert(0, gtm_head_tag)
                head.insert(1, soup.new_string('\n'))
            else:
                head.append(gtm_head_tag)
            
            # Adicionar GTM noscript logo após <body>
            gtm_body_tag = BeautifulSoup(self.generate_gtm_body_snippet(), 'html.parser')
            
            # Inserir no início do <body>
            if body.contents:
                body.insert(0, gtm_body_tag)
                body.insert(1, soup.new_string('\n'))
            else:
                body.append(gtm_body_tag)
            
            # Salvar (se não for dry-run)
            if not self.dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(str(soup))
                logger.info(f"   ✅ Integrado: {file_path.name}")
            else:
                logger.info(f"   🔍 Seria integrado: {file_path.name}")
            
            self.files_updated += 1
            return True
            
        except Exception as e:
            logger.error(f"   ❌ Erro em {file_path.name}: {e}")
            return False
    
    def process_directory(self, directory: str) -> None:
        """Processa todos os arquivos HTML em um diretório"""
        dir_path = Path(directory)
        
        if not dir_path.exists():
            logger.warning(f"Diretório não encontrado: {directory}")
            return
        
        # Encontrar todos os arquivos HTML
        html_files = list(dir_path.glob("*.html"))
        
        if not html_files:
            return
        
        logger.info(f"\n📂 Processando diretório: {directory}")
        logger.info(f"   📄 Encontrados {len(html_files)} arquivos HTML")
        
        for html_file in html_files:
            self.files_processed += 1
            self.integrate_gtm(html_file)
    
    def process_all(self) -> None:
        """Processa todos os diretórios do site"""
        directories = [
            ".",  # Raiz
            "integracoes",
            "integracoes-zapier",
            "blog",
            "ferramentas",
        ]
        
        for directory in directories:
            self.process_directory(directory)
    
    def print_summary(self) -> None:
        """Exibe resumo da integração"""
        logger.info("\n" + "=" * 80)
        logger.info("📊 RESUMO DA INTEGRAÇÃO GTM")
        logger.info("=" * 80)
        logger.info(f"Arquivos processados: {self.files_processed}")
        logger.info(f"Arquivos atualizados: {self.files_updated}")
        logger.info(f"Arquivos pulados (já tinham GTM): {self.files_skipped}")
        logger.info("")
        
        if not self.dry_run:
            logger.info("✅ Integração concluída com sucesso!")
        else:
            logger.info("🔍 DRY-RUN: Nenhuma alteração foi feita")
        
        logger.info("")
        logger.info("📋 PRÓXIMOS PASSOS:")
        logger.info("   1. Verificar instalação em: https://tagmanager.google.com")
        logger.info("   2. Configurar tags, triggers e variáveis no GTM")
        logger.info("   3. Publicar container GTM")
        logger.info("   4. Testar com Google Tag Assistant")
        logger.info("=" * 80)


def main():
    parser = argparse.ArgumentParser(description='Integra Google Tag Manager em todas as páginas HTML')
    parser.add_argument('--gtm-id', default='GTM-KVTHGKJR', help='GTM Container ID (padrão: GTM-KVTHGKJR)')
    parser.add_argument('--dry-run', action='store_true', help='Simular integração sem salvar alterações')
    
    args = parser.parse_args()
    
    logger.info("=" * 80)
    logger.info("🚀 INTEGRAÇÃO GOOGLE TAG MANAGER")
    logger.info("=" * 80)
    logger.info(f"GTM Container ID: {args.gtm_id}")
    logger.info(f"Modo: {'DRY-RUN (sem alterações)' if args.dry_run else 'PRODUÇÃO'}")
    logger.info("")
    
    integrator = GoogleTagManagerIntegrator(gtm_id=args.gtm_id, dry_run=args.dry_run)
    integrator.process_all()
    integrator.print_summary()


if __name__ == "__main__":
    main()
