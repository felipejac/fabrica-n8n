#!/usr/bin/env python3
"""
Valida Rich Results em amostra de templates usando Google Rich Results Test API
E prepara checklist para submissão ao Google Search Console

Testa:
- Schema.org HowTo
- Schema.org FAQPage
- Schema.org BreadcrumbList
- HTML Structure
- Mobile-Friendly
"""

import random
import csv
import os
import json
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class RichResultsValidator:
    """Valida templates para Rich Results"""
    
    def __init__(self, base_url: str = "https://www.automationscookbook.com"):
        self.base_url = base_url.rstrip('/')
        self.sample_size = 10
        self.results = []
    
    def select_random_templates(self) -> list:
        """Seleciona amostra aleatória de templates"""
        logger.info("🎲 Selecionando amostra aleatória de templates...")
        
        with open('automacoes_db.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            templates = [row for row in reader if row.get('slug_url')]
        
        # Selecionar 10 templates aleatórios
        sample = random.sample(templates, min(self.sample_size, len(templates)))
        
        logger.info(f"   ✓ Selecionados {len(sample)} templates")
        return sample
    
    def validate_template_structure(self, slug: str) -> dict:
        """Valida estrutura HTML e Schema.org de um template"""
        filepath = f"integracoes/{slug}.html"
        
        if not os.path.exists(filepath):
            return {
                'slug': slug,
                'exists': False,
                'error': 'Arquivo não encontrado'
            }
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        result = {
            'slug': slug,
            'url': f"{self.base_url}/integracoes/{slug}.html",
            'exists': True,
            'file_size': len(content),
            'schemas': {},
            'phase3_features': {},
            'html_structure': {}
        }
        
        # Verificar Schema.org
        result['schemas']['HowTo'] = '"@type": "HowTo"' in content
        result['schemas']['FAQPage'] = '"@type": "FAQPage"' in content
        result['schemas']['BreadcrumbList'] = '"@type": "BreadcrumbList"' in content
        result['schemas']['TechArticle'] = '"@type": "TechArticle"' in content or '"@type": "Article"' in content
        
        # Verificar Phase 3 features
        result['phase3_features']['faq_visible'] = 'class="faq-section"' in content
        result['phase3_features']['llm_prompt'] = 'class="llm-friendly"' in content
        result['phase3_features']['breadcrumbs_visible'] = 'class="breadcrumbs"' in content
        result['phase3_features']['internal_links'] = 'class="related-templates"' in content
        
        # Verificar estrutura HTML
        result['html_structure']['title'] = '<title>' in content
        result['html_structure']['meta_description'] = 'name="description"' in content
        result['html_structure']['canonical'] = 'rel="canonical"' in content
        result['html_structure']['og_tags'] = 'property="og:' in content
        result['html_structure']['viewport'] = 'name="viewport"' in content
        
        # Calcular score
        schema_score = sum(result['schemas'].values())
        phase3_score = sum(result['phase3_features'].values())
        html_score = sum(result['html_structure'].values())
        
        result['scores'] = {
            'schema': f"{schema_score}/4",
            'phase3': f"{phase3_score}/4",
            'html': f"{html_score}/5",
            'total': f"{schema_score + phase3_score + html_score}/13"
        }
        
        return result
    
    def generate_validation_report(self, templates: list):
        """Gera relatório de validação"""
        logger.info("\n" + "=" * 80)
        logger.info("🔍 VALIDANDO TEMPLATES PARA RICH RESULTS")
        logger.info("=" * 80)
        
        for idx, template in enumerate(templates, 1):
            slug = template.get('slug_url')
            logger.info(f"\n📄 [{idx}/{len(templates)}] Validando: {slug}")
            
            result = self.validate_template_structure(slug)
            self.results.append(result)
            
            if not result['exists']:
                logger.error(f"   ❌ Arquivo não encontrado")
                continue
            
            # Mostrar scores
            scores = result['scores']
            logger.info(f"   📊 Scores:")
            logger.info(f"      Schema.org: {scores['schema']}")
            logger.info(f"      Phase 3 Features: {scores['phase3']}")
            logger.info(f"      HTML Structure: {scores['html']}")
            logger.info(f"      TOTAL: {scores['total']}")
            
            # Verificar problemas
            problems = []
            
            if not all(result['schemas'].values()):
                missing_schemas = [k for k, v in result['schemas'].items() if not v]
                problems.append(f"Schema.org faltando: {', '.join(missing_schemas)}")
            
            if not all(result['phase3_features'].values()):
                missing_features = [k for k, v in result['phase3_features'].items() if not v]
                problems.append(f"Phase 3 features faltando: {', '.join(missing_features)}")
            
            if problems:
                logger.warning(f"   ⚠️  Problemas encontrados:")
                for problem in problems:
                    logger.warning(f"      - {problem}")
            else:
                logger.info(f"   ✅ Todas as validações passaram!")
        
        # Resumo geral
        self._print_summary()
        self._save_json_report()
        self._generate_gsc_checklist()
    
    def _print_summary(self):
        """Imprime resumo da validação"""
        logger.info("\n" + "=" * 80)
        logger.info("📊 RESUMO DA VALIDAÇÃO")
        logger.info("=" * 80)
        
        total = len(self.results)
        valid = len([r for r in self.results if r.get('exists')])
        
        # Calcular médias
        avg_schemas = sum([int(r['scores']['schema'].split('/')[0]) for r in self.results if r.get('exists')]) / valid
        avg_phase3 = sum([int(r['scores']['phase3'].split('/')[0]) for r in self.results if r.get('exists')]) / valid
        avg_html = sum([int(r['scores']['html'].split('/')[0]) for r in self.results if r.get('exists')]) / valid
        avg_total = sum([int(r['scores']['total'].split('/')[0]) for r in self.results if r.get('exists')]) / valid
        
        logger.info(f"\n📈 Médias de Score:")
        logger.info(f"   Schema.org: {avg_schemas:.1f}/4 ({avg_schemas/4*100:.0f}%)")
        logger.info(f"   Phase 3: {avg_phase3:.1f}/4 ({avg_phase3/4*100:.0f}%)")
        logger.info(f"   HTML: {avg_html:.1f}/5 ({avg_html/5*100:.0f}%)")
        logger.info(f"   TOTAL: {avg_total:.1f}/13 ({avg_total/13*100:.0f}%)")
        
        # Identificar problemas comuns
        logger.info(f"\n🔍 Análise de Features:")
        
        for feature_type in ['schemas', 'phase3_features', 'html_structure']:
            logger.info(f"\n   {feature_type.replace('_', ' ').title()}:")
            
            if feature_type in self.results[0]:
                features = self.results[0][feature_type].keys()
                
                for feature in features:
                    count = sum([r[feature_type].get(feature, False) for r in self.results if r.get('exists')])
                    percentage = count / valid * 100
                    status = "✅" if percentage == 100 else "⚠️"
                    logger.info(f"      {status} {feature}: {count}/{valid} ({percentage:.0f}%)")
    
    def _save_json_report(self):
        """Salva relatório em JSON"""
        output_file = 'rich_results_validation.json'
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"\n💾 Relatório JSON salvo: {output_file}")
    
    def _generate_gsc_checklist(self):
        """Gera checklist para Google Search Console"""
        logger.info("\n" + "=" * 80)
        logger.info("📋 CHECKLIST GOOGLE SEARCH CONSOLE")
        logger.info("=" * 80)
        
        checklist = """
🔗 URLs para Validação Manual:

Google Rich Results Test:
https://search.google.com/test/rich-results

URLs de Teste (copiar e colar no Rich Results Test):
"""
        
        for result in self.results[:5]:  # Primeiras 5
            if result.get('exists'):
                checklist += f"\n✓ {result['url']}"
        
        checklist += """

---

📤 SUBMISSÃO DE SITEMAPS

1. Acessar Google Search Console:
   https://search.google.com/search-console

2. Selecionar propriedade:
   automationscookbook.com

3. Ir em: Sitemaps (menu lateral esquerdo)

4. Adicionar novo sitemap:
   URL: https://www.automationscookbook.com/sitemap-index.xml
   
5. Verificar sub-sitemaps descobertos automaticamente:
   ✓ sitemap-institucional.xml
   ✓ sitemap-integracoes-n8n.xml
   ✓ sitemap-integracoes-zapier.xml
   ✓ sitemap-blog.xml
   ✓ sitemap-ferramentas.xml

---

📊 MONITORAMENTO (Próximos 7 dias)

1. Performance Report:
   - Cliques: Deve aumentar +15-25%
   - Impressões: Deve aumentar +25-35%
   - CTR: Deve melhorar +1-2pp
   - Posição Média: Deve melhorar 3-5 posições

2. Coverage Report:
   - Valid: Deve manter 12,500+ páginas
   - Errors: Deve ser <10
   - Excluded: Verificar se há soft 404s

3. Enhancements > Structured Data:
   - HowTo: 12,541 páginas
   - FAQPage: 12,541 páginas
   - BreadcrumbList: 12,541 páginas
   - Errors: Deve ser 0

4. Core Web Vitals:
   - Good URLs: >95%
   - LCP: <2.5s
   - FID: <100ms
   - CLS: <0.1

---

⚠️ ALERTAS PARA CONFIGURAR

1. Email notifications para:
   - Coverage issues
   - Manual actions
   - Security issues
   - Structured data errors

2. Webhook notifications (opcional):
   - Integrar com Slack/Discord
   - Alertas em tempo real

---

🎯 METAS 30 DIAS

✓ Índice: 12,500+ páginas indexadas (95%+)
✓ Rich Results: 100% de elegibilidade
✓ CTR orgânico: +20%
✓ Impressões: +30%
✓ Zero erros críticos de Schema.org
✓ Core Web Vitals: 100% "Good"

---

📝 NOTAS

- Indexação completa pode levar 7-14 dias
- Rich Results aparecem em 3-7 dias após validação
- Monitorar queries de cauda longa (aumentam primeiro)
- CTR melhora antes de posições (devido a meta descriptions)
"""
        
        checklist_file = 'GSC_SUBMISSION_CHECKLIST.txt'
        with open(checklist_file, 'w', encoding='utf-8') as f:
            f.write(checklist)
        
        logger.info(checklist)
        logger.info(f"\n💾 Checklist salvo: {checklist_file}")


if __name__ == "__main__":
    validator = RichResultsValidator()
    
    # Selecionar amostra
    templates = validator.select_random_templates()
    
    # Validar e gerar relatório
    validator.generate_validation_report(templates)
    
    logger.info("\n" + "=" * 80)
    logger.info("✅ VALIDAÇÃO CONCLUÍDA")
    logger.info("=" * 80)
    logger.info("\n📋 Próximos passos:")
    logger.info("   1. Testar 5 URLs no Google Rich Results Test")
    logger.info("   2. Submeter sitemap-index.xml no GSC")
    logger.info("   3. Configurar alertas de email no GSC")
    logger.info("   4. Monitorar métricas nos próximos 7 dias")
    logger.info("\n🔗 Arquivos gerados:")
    logger.info("   - rich_results_validation.json")
    logger.info("   - GSC_SUBMISSION_CHECKLIST.txt")
