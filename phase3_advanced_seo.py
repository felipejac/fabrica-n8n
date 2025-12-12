#!/usr/bin/env python3
"""
PHASE 3: Advanced SEO Enhancements
Implementa melhorias avançadas de SEO após Phase 2 (12,542 templates com Schema.org)

TAREFAS:
1. Adicionar seções FAQ visíveis nos templates HTML
2. Criar blocos "Como Explicar para IA" (LLM-friendly)
3. Melhorar títulos e meta descriptions
4. Adicionar links internos estratégicos
5. Implementar breadcrumbs visíveis

Autor: AI Trend Hunter + SEO Master
Data: 12 de Dezembro de 2025
"""

import csv
import os
import re
from bs4 import BeautifulSoup
from typing import List, Dict, Tuple
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Phase3SEOEnhancer:
    """Adiciona melhorias avançadas de SEO aos templates"""
    
    def __init__(self, csv_path: str = 'automacoes_db.csv'):
        self.csv_path = csv_path
        self.templates_processed = 0
        self.templates_enhanced = 0
        self.errors = []
    
    def process_batch(self, skip: int = 0, limit: int = None, dry_run: bool = False):
        """
        Processa batch de templates para adicionar melhorias SEO
        
        Args:
            skip: Quantos templates pular
            limit: Quantos processar (None = todos)
            dry_run: Se True, não salva alterações
        """
        logger.info("=" * 80)
        logger.info("🚀 PHASE 3: Advanced SEO Enhancements")
        logger.info("=" * 80)
        
        if dry_run:
            logger.info("⚠️  DRY RUN MODE - Nenhuma alteração será salva")
        
        # Ler CSV
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            templates = list(reader)
        
        # Aplicar skip/limit
        if skip > 0:
            templates = templates[skip:]
        if limit:
            templates = templates[:limit]
        
        logger.info(f"📊 Total de templates a processar: {len(templates)}")
        logger.info(f"   Skip: {skip} | Limit: {limit or 'all'}")
        logger.info("")
        
        # Processar cada template
        for idx, template in enumerate(templates, 1):
            try:
                self._process_template(template, idx, len(templates), dry_run)
            except Exception as e:
                logger.error(f"❌ Erro no template {idx}: {e}")
                self.errors.append((idx, str(e)))
        
        # Relatório final
        self._print_summary()
    
    def _process_template(self, template: Dict, idx: int, total: int, dry_run: bool):
        """Processa um template individual"""
        slug = template.get('slug_url', '')
        if not slug:
            return
        
        filepath = f"integracoes/{slug}.html"
        
        if not os.path.exists(filepath):
            logger.warning(f"⚠️  [{idx}/{total}] Arquivo não encontrado: {filepath}")
            return
        
        self.templates_processed += 1
        
        # Ler HTML
        with open(filepath, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Verificar se já tem enhancements
        if self._has_phase3_markers(soup):
            logger.info(f"✓ [{idx}/{total}] {slug} - Já possui Phase 3 enhancements")
            return
        
        # Aplicar melhorias
        modified = False
        
        # 1. Adicionar FAQ visível
        if self._add_visible_faq(soup, template):
            modified = True
        
        # 2. Adicionar seção "Como Explicar para IA"
        if self._add_llm_section(soup, template):
            modified = True
        
        # 3. Melhorar meta description
        if self._improve_meta_description(soup, template):
            modified = True
        
        # 4. Adicionar breadcrumbs visíveis
        if self._add_visible_breadcrumbs(soup, template):
            modified = True
        
        # 5. Adicionar links internos
        if self._add_internal_links(soup, template):
            modified = True
        
        if not modified:
            return
        
        # Salvar se não for dry-run
        if not dry_run:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            logger.info(f"✅ [{idx}/{total}] {slug} - Enhanced")
            self.templates_enhanced += 1
        else:
            logger.info(f"🔍 [{idx}/{total}] {slug} - Would be enhanced (dry-run)")
    
    def _has_phase3_markers(self, soup: BeautifulSoup) -> bool:
        """Verifica se template já tem Phase 3 enhancements"""
        # Procurar por marcadores específicos
        faq_section = soup.find('section', {'class': 'faq-section'})
        llm_section = soup.find('section', {'class': 'llm-friendly'})
        
        return faq_section is not None or llm_section is not None
    
    def _add_visible_faq(self, soup: BeautifulSoup, template: Dict) -> bool:
        """Adiciona seção FAQ visível baseada no FAQPage schema"""
        
        # Buscar FAQPage schema existente
        faq_schema = soup.find('script', {'type': 'application/ld+json'})
        if not faq_schema:
            return False
        
        import json
        try:
            schema_data = json.loads(faq_schema.string)
            
            # Verificar se é FAQPage
            if not isinstance(schema_data, list):
                schema_data = [schema_data]
            
            faq_page = None
            for item in schema_data:
                if item.get('@type') == 'FAQPage':
                    faq_page = item
                    break
            
            if not faq_page or 'mainEntity' not in faq_page:
                return False
            
            # Criar HTML da FAQ
            faq_html = self._generate_faq_html(faq_page['mainEntity'])
            
            # Inserir antes do footer
            main_content = soup.find('main') or soup.find('body')
            if main_content:
                faq_section = BeautifulSoup(faq_html, 'html.parser')
                main_content.append(faq_section)
                return True
        
        except Exception as e:
            logger.warning(f"Erro ao processar FAQ: {e}")
        
        return False
    
    def _generate_faq_html(self, questions: List[Dict]) -> str:
        """Gera HTML formatado para FAQ"""
        html = '''
<section class="faq-section" style="margin-top: 3rem; padding: 2rem; background: #f8f9fa; border-radius: 8px;">
    <h2 style="font-size: 1.8rem; margin-bottom: 1.5rem; color: #2c3e50;">❓ Perguntas Frequentes</h2>
    <div class="faq-container">
'''
        
        for idx, q in enumerate(questions, 1):
            question = q.get('name', '')
            answer = q.get('acceptedAnswer', {}).get('text', '')
            
            html += f'''
        <details class="faq-item" style="margin-bottom: 1rem; padding: 1rem; background: white; border-radius: 6px; border-left: 4px solid #3498db;">
            <summary style="font-weight: 600; cursor: pointer; font-size: 1.1rem; color: #2c3e50;">
                {idx}. {question}
            </summary>
            <div style="margin-top: 0.8rem; padding-left: 1rem; color: #555; line-height: 1.6;">
                {answer}
            </div>
        </details>
'''
        
        html += '''
    </div>
</section>
'''
        return html
    
    def _add_llm_section(self, soup: BeautifulSoup, template: Dict) -> bool:
        """Adiciona seção 'Como Explicar para IA' (LLM-friendly)"""
        
        software_a = template.get('software_a', '')
        software_b = template.get('software_b', '')
        tipo_evento = template.get('tipo_evento', '')
        
        if not software_a or not software_b:
            return False
        
        # Gerar prompt otimizado para LLMs
        llm_prompt = self._generate_llm_prompt(template)
        
        llm_html = f'''
<section class="llm-friendly" style="margin-top: 3rem; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 8px; color: white;">
    <h2 style="font-size: 1.8rem; margin-bottom: 1rem;">🤖 Como Explicar para IA (Prompt Pronto)</h2>
    <p style="margin-bottom: 1.5rem; opacity: 0.9;">
        Use este prompt com ChatGPT, Claude ou qualquer LLM para criar esta automação:
    </p>
    
    <div style="background: rgba(0,0,0,0.2); padding: 1.5rem; border-radius: 6px; font-family: 'Courier New', monospace; white-space: pre-wrap; line-height: 1.6; border-left: 4px solid #ffd700;">
{llm_prompt}
    </div>
    
    <div style="margin-top: 1.5rem; padding: 1rem; background: rgba(255,255,255,0.1); border-radius: 6px;">
        <strong>💡 Dica:</strong> Copie este prompt e cole no ChatGPT. A IA irá te guiar passo a passo na criação da automação.
    </div>
</section>
'''
        
        # Inserir antes do footer
        main_content = soup.find('main') or soup.find('body')
        if main_content:
            llm_section = BeautifulSoup(llm_html, 'html.parser')
            main_content.append(llm_section)
            return True
        
        return False
    
    def _generate_llm_prompt(self, template: Dict) -> str:
        """Gera prompt otimizado para LLMs"""
        software_a = template.get('software_a', '')
        software_b = template.get('software_b', '')
        tipo_evento = template.get('tipo_evento', '')
        caso_uso = template.get('caso_uso_resumido', '')
        
        prompt = f"""Preciso criar uma automação no n8n que conecte {software_a} com {software_b}.

🎯 OBJETIVO:
Quando acontecer: {tipo_evento} no {software_a}
Então fazer: Enviar dados para {software_b}

📋 CONTEXTO:
{caso_uso}

❓ ME AJUDE COM:
1. Qual webhook ou trigger usar no {software_a}
2. Quais dados preciso capturar
3. Como transformar os dados (se necessário)
4. Como autenticar no {software_b}
5. Qual ação executar no {software_b}

💻 PLATAFORMA:
n8n (ferramenta open-source de automação)

🔗 REFERÊNCIA:
Este template está documentado em: automationscookbook.com"""
        
        return prompt
    
    def _improve_meta_description(self, soup: BeautifulSoup, template: Dict) -> bool:
        """Melhora a meta description com fórmula otimizada"""
        
        meta_desc = soup.find('meta', {'name': 'description'})
        if not meta_desc:
            # Criar nova meta description
            meta_desc = soup.new_tag('meta', attrs={'name': 'description'})
            head = soup.find('head')
            if head:
                head.append(meta_desc)
        
        # Fórmula: Ação + Benefício + Plataforma + CTA
        software_a = template.get('software_a', '')
        software_b = template.get('software_b', '')
        tipo_evento = template.get('tipo_evento', 'evento')
        
        new_description = (
            f"Automatize {software_a} → {software_b} quando {tipo_evento} acontecer. "
            f"Template n8n pronto, gratuito e fácil de implementar. "
            f"↓ Baixe o JSON agora!"
        )
        
        # Limitar a 155 caracteres
        if len(new_description) > 155:
            new_description = new_description[:152] + "..."
        
        current_desc = meta_desc.get('content', '')
        if current_desc != new_description:
            meta_desc['content'] = new_description
            return True
        
        return False
    
    def _add_visible_breadcrumbs(self, soup: BeautifulSoup, template: Dict) -> bool:
        """Adiciona breadcrumbs visíveis no topo da página"""
        
        # Verificar se já existe
        if soup.find('nav', {'class': 'breadcrumbs'}):
            return False
        
        titulo = template.get('titulo_pagina', '')
        
        breadcrumb_html = f'''
<nav class="breadcrumbs" style="padding: 1rem 0; margin-bottom: 1.5rem; font-size: 0.9rem;" aria-label="Breadcrumb">
    <ol style="list-style: none; display: flex; gap: 0.5rem; padding: 0; margin: 0; flex-wrap: wrap;">
        <li>
            <a href="/" style="color: #3498db; text-decoration: none;">🏠 Home</a>
        </li>
        <li style="color: #999;">›</li>
        <li>
            <a href="/integracoes/" style="color: #3498db; text-decoration: none;">Integrações</a>
        </li>
        <li style="color: #999;">›</li>
        <li style="color: #555;" aria-current="page">
            {titulo[:50]}...
        </li>
    </ol>
</nav>
'''
        
        # Inserir no início do main
        main_content = soup.find('main')
        if main_content:
            breadcrumb = BeautifulSoup(breadcrumb_html, 'html.parser')
            main_content.insert(0, breadcrumb)
            return True
        
        return False
    
    def _add_internal_links(self, soup: BeautifulSoup, template: Dict) -> bool:
        """Adiciona seção de templates relacionados"""
        
        # Buscar templates relacionados por tags
        tags = template.get('tags', '').split(',')
        if not tags or not tags[0]:
            return False
        
        related_html = f'''
<section class="related-templates" style="margin-top: 3rem; padding: 2rem; background: #ecf0f1; border-radius: 8px;">
    <h2 style="font-size: 1.6rem; margin-bottom: 1rem; color: #2c3e50;">🔗 Templates Relacionados</h2>
    <p style="margin-bottom: 1.5rem; color: #555;">
        Explore outras automações similares:
    </p>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">
        <a href="/integracoes/" style="padding: 1rem; background: white; border-radius: 6px; text-decoration: none; color: #2c3e50; border-left: 4px solid #3498db; transition: transform 0.2s;" onmouseover="this.style.transform='translateX(5px)'" onmouseout="this.style.transform='translateX(0)'">
            <strong>📚 Ver Todas as Integrações</strong>
            <div style="font-size: 0.9rem; color: #777; margin-top: 0.3rem;">13.269+ templates disponíveis</div>
        </a>
        
        <a href="/guia-automacoes-n8n" style="padding: 1rem; background: white; border-radius: 6px; text-decoration: none; color: #2c3e50; border-left: 4px solid #e74c3c;">
            <strong>📖 Guia Completo n8n</strong>
            <div style="font-size: 0.9rem; color: #777; margin-top: 0.3rem;">Aprenda do zero</div>
        </a>
        
        <a href="/ai-agents" style="padding: 1rem; background: white; border-radius: 6px; text-decoration: none; color: #2c3e50; border-left: 4px solid #9b59b6;">
            <strong>🤖 Para IAs e Agentes</strong>
            <div style="font-size: 0.9rem; color: #777; margin-top: 0.3rem;">Dados estruturados para LLMs</div>
        </a>
    </div>
</section>
'''
        
        # Inserir antes do footer
        main_content = soup.find('main') or soup.find('body')
        if main_content:
            related_section = BeautifulSoup(related_html, 'html.parser')
            main_content.append(related_section)
            return True
        
        return False
    
    def _print_summary(self):
        """Imprime resumo da execução"""
        logger.info("")
        logger.info("=" * 80)
        logger.info("📊 PHASE 3 - RESUMO DA EXECUÇÃO")
        logger.info("=" * 80)
        logger.info(f"Templates processados: {self.templates_processed}")
        logger.info(f"Templates enhanced: {self.templates_enhanced}")
        logger.info(f"Erros encontrados: {len(self.errors)}")
        
        if self.errors:
            logger.info("\n❌ ERROS:")
            for idx, error in self.errors[:10]:
                logger.info(f"   Template {idx}: {error}")
        
        logger.info("=" * 80)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Phase 3: Advanced SEO Enhancements')
    parser.add_argument('--skip', type=int, default=0, help='Quantos templates pular')
    parser.add_argument('--limit', type=int, default=None, help='Quantos processar')
    parser.add_argument('--dry-run', action='store_true', help='Não salvar alterações')
    
    args = parser.parse_args()
    
    enhancer = Phase3SEOEnhancer()
    enhancer.process_batch(
        skip=args.skip,
        limit=args.limit,
        dry_run=args.dry_run
    )
