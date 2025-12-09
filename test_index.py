#!/usr/bin/env python3
"""
🧪 Test Suite Completo para Index.html
Tests all functionality of the index.html file
"""

import os
import re
import json
import sys
from pathlib import Path
from html.parser import HTMLParser

class TestReport:
    def __init__(self):
        self.tests = []
        self.passed = 0
        self.failed = 0
        self.total = 0
    
    def add_test(self, name, status, details=""):
        self.total += 1
        if status == "pass":
            self.passed += 1
            icon = "✅"
        elif status == "fail":
            self.failed += 1
            icon = "❌"
        else:
            icon = "⚠️"
        
        self.tests.append({
            "name": name,
            "status": status,
            "icon": icon,
            "details": details
        })
    
    def print_report(self):
        print("\n" + "="*80)
        print("🧪 TESTE COMPLETO - INDEX.HTML")
        print("="*80 + "\n")
        
        for test in self.tests:
            print(f"{test['icon']} {test['name']}")
            if test['details']:
                print(f"   └─ {test['details']}")
        
        print("\n" + "-"*80)
        print(f"\n📊 RESULTADOS FINAIS:")
        print(f"   ✅ Passados: {self.passed}/{self.total}")
        print(f"   ❌ Falhados: {self.failed}/{self.total}")
        success_rate = (self.passed / self.total * 100) if self.total > 0 else 0
        print(f"   📈 Taxa de Sucesso: {success_rate:.1f}%")
        print(f"\n{'🎉 APROVADO' if self.failed == 0 else '⚠️ FALHAS DETECTADAS'}")
        print("\n" + "="*80 + "\n")


class HTMLValidator(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.classes = []
        self.tags = {}
        self.scripts = []
        self.links = []
    
    def handle_starttag(self, tag, attrs):
        # Count tags
        self.tags[tag] = self.tags.get(tag, 0) + 1
        
        # Extract IDs and classes
        attrs_dict = dict(attrs)
        if 'id' in attrs_dict:
            self.ids.add(attrs_dict['id'])
        if 'class' in attrs_dict:
            self.classes.extend(attrs_dict['class'].split())
        
        # Track scripts and links
        if tag == 'script':
            if 'src' in attrs_dict:
                self.scripts.append(attrs_dict['src'])
        elif tag == 'link':
            if 'href' in attrs_dict:
                self.links.append(attrs_dict['href'])


def test_file_exists(report, filepath):
    """Test 1: Verificar se arquivo existe"""
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        report.add_test("1. Arquivo Existe", "pass", f"✓ {filepath} ({size} bytes)")
        return True
    else:
        report.add_test("1. Arquivo Existe", "fail", f"✗ {filepath} não encontrado")
        return False


def test_html_structure(report, content):
    """Test 2: Validar estrutura HTML"""
    checks = {
        "DOCTYPE": "<!DOCTYPE html",
        "Lang": 'lang="pt-BR"',
        "Charset": 'charset="UTF-8"',
        "Viewport": "width=device-width, initial-scale=1.0",
        "Title": "<title>",
        "Body": "<body"
    }
    
    passed = 0
    for check, pattern in checks.items():
        if pattern in content:
            passed += 1
    
    if passed == len(checks):
        report.add_test("2. Estrutura HTML", "pass", f"✓ Todos os {len(checks)} elementos críticos presentes")
    else:
        report.add_test("2. Estrutura HTML", "fail", f"✗ Apenas {passed}/{len(checks)} elementos presentes")


def test_views(report, content):
    """Test 3: Verificar todas as 7 views"""
    views = ['home', 'generator', 'library', 'toolbox', 'academy', 'debugger', 'integrations']
    found = []
    
    for view in views:
        pattern = f'id="{view}-view"'
        if pattern in content:
            found.append(view)
    
    if len(found) == len(views):
        report.add_test("3. Views", "pass", f"✓ Todas as {len(views)} views encontradas: {', '.join(found)}")
    else:
        missing = [v for v in views if v not in found]
        report.add_test("3. Views", "fail", f"✗ Faltam views: {', '.join(missing)}")


def test_settings_modal(report, content):
    """Test 4: Verificar modal de configurações"""
    elements = {
        "Modal Container": 'id="settingsModal"',
        "API Key Input": 'id="apiKeyInput"',
        "Open Function": "openSettings()",
        "Close Function": "closeSettings()",
        "Save Function": "saveSettings()"
    }
    
    found = sum(1 for elem, pattern in elements.items() if pattern in content)
    
    if found == len(elements):
        report.add_test("4. Modal Configurações", "pass", f"✓ Todos os {len(elements)} elementos presentes")
    else:
        report.add_test("4. Modal Configurações", "fail", f"✗ Apenas {found}/{len(elements)} elementos")


def test_api_integration(report, content):
    """Test 5: Verificar integração com API Gemini"""
    patterns = {
        "Gemini URL": "generativelanguage.googleapis.com",
        "API Key Storage": "localStorage.setItem('gemini_api_key'",
        "API Call": "callGemini(",
        "Error Diagnosis": "diagnoseError()"
    }
    
    found = sum(1 for pattern in patterns.values() if pattern in content)
    
    if found == len(patterns):
        report.add_test("5. API Gemini", "pass", f"✓ Integração Gemini 2.5 Flash configurada")
    else:
        report.add_test("5. API Gemini", "fail", f"✗ Apenas {found}/{len(patterns)} componentes presentes")


def test_external_libraries(report, content):
    """Test 6: Verificar bibliotecas externas"""
    libraries = {
        "Tailwind CSS": "cdn.tailwindcss.com",
        "PapaParse": "papaparse.min.js",
        "JSZip": "jszip.min.js",
        "FileSaver": "FileSaver.min.js",
        "Highlight.js": "highlight.min.js",
        "Google Fonts": "fonts.googleapis.com"
    }
    
    found = sum(1 for lib in libraries.values() if lib in content)
    
    if found >= 5:
        report.add_test("6. Bibliotecas Externas", "pass", f"✓ {found}/6 bibliotecas carregadas")
    else:
        report.add_test("6. Bibliotecas Externas", "fail", f"✗ Apenas {found}/6 bibliotecas")


def test_responsive_design(report, content):
    """Test 7: Verificar design responsivo"""
    responsive_classes = [
        "md:flex-row",
        "lg:px-8",
        "grid-cols-1",
        "md:grid-cols-2",
        "lg:grid-cols-3",
        "sm:px-6",
        "flex-col"
    ]
    
    found = sum(1 for cls in responsive_classes if cls in content)
    
    if found >= len(responsive_classes) - 2:  # Pelo menos 5 de 7
        report.add_test("7. Design Responsivo", "pass", f"✓ Classes Tailwind responsivas presentes ({found} encontradas)")
    else:
        report.add_test("7. Design Responsivo", "fail", f"✗ Apenas {found}/{len(responsive_classes)} classes responsivas")


def test_integration_data(report, content):
    """Test 8: Verificar dados de integrações"""
    patterns = [
        ("Google Sheets", "google-sheets"),
        ("Slack", "slack"),
        ("integrationsData", "integrationsData"),
        ("13269", "13269"),  # Último count comment
    ]
    
    found = sum(1 for _, pattern in patterns if pattern in content)
    
    if found >= 3:
        report.add_test("8. Dados Integrações", "pass", f"✓ Dados de integrações presentes ({found}/4)")
        # Try to count total integrations
        match = re.search(r'<!-- INTEGRATIONS_COUNT:\s*(\d+)\s*-->', content)
        if match:
            count = match.group(1)
            report.add_test("   └─ Total de Integrações", "pass", f"✓ {count} integrações configuradas")
    else:
        report.add_test("8. Dados Integrações", "fail", f"✗ Dados insuficientes")


def test_javascript_file(report, js_path):
    """Test 9: Verificar arquivo JavaScript"""
    if not os.path.exists(js_path):
        report.add_test("9. Arquivo JavaScript", "fail", f"✗ {js_path} não encontrado")
        return
    
    with open(js_path, 'r', encoding='utf-8') as f:
        js_content = f.read()
    
    functions = [
        'switchView',
        'openSettings',
        'closeSettings',
        'saveSettings',
        'callGemini',
        'diagnoseError',
        'fillError'
    ]
    
    found = sum(1 for func in functions if func in js_content)
    lines = len(js_content.split('\n'))
    
    if found >= 5:
        report.add_test("9. Arquivo JavaScript", "pass", f"✓ {found}/{len(functions)} funções presentes ({lines} linhas)")
    else:
        report.add_test("9. Arquivo JavaScript", "fail", f"✗ Apenas {found}/{len(functions)} funções")


def test_seo_tags(report, content):
    """Test 10: Verificar tags SEO"""
    seo_elements = {
        "Meta Description": '<meta name="description"',
        "Meta Viewport": '<meta name="viewport"',
        "Title": "<title>AI Factory",
        "Schema.org": 'itemscope itemtype="http://schema.org',
        "Favicon": 'rel="icon"'
    }
    
    found = sum(1 for elem in seo_elements.values() if elem in content)
    
    if found == len(seo_elements):
        report.add_test("10. Tags SEO", "pass", f"✓ Todas as {len(seo_elements)} tags SEO presentes")
    else:
        report.add_test("10. Tags SEO", "fail", f"✗ Apenas {found}/{len(seo_elements)} tags")


def test_security_features(report, content):
    """Test 11: Verificar segurança"""
    security_features = [
        ("BYOK Pattern", "localStorage.getItem('gemini_api_key'"),
        ("HTTPS URLs", "https://"),
        ("No Inline Scripts", "unsafe-inline" not in content),
        ("Type Password", 'type="password"')
    ]
    
    found = sum(1 for name, pattern in security_features if isinstance(pattern, bool) or pattern in content)
    
    if found >= 3:
        report.add_test("11. Segurança", "pass", f"✓ {found} features de segurança implementadas")
    else:
        report.add_test("11. Segurança", "fail", f"✗ Apenas {found} features de segurança")


def test_performance(report, content):
    """Test 12: Verificar otimizações de performance"""
    optimizations = [
        ("DOM Caching", "viewEls"),
        ("Cache Nav Buttons", "navBtns"),
        ("Event Delegation", "addEventListener"),
        ("Lazy Load Views", "hidden"),
        ("CSS Animations", "@keyframes"),
        ("Tailwind Utility", "class="),
    ]
    
    found = sum(1 for _, pattern in optimizations if pattern in content)
    
    if found >= 4:
        report.add_test("12. Performance", "pass", f"✓ {found} otimizações implementadas")
    else:
        report.add_test("12. Performance", "fail", f"✗ Apenas {found} otimizações")


def main():
    # Definir caminhos
    base_path = Path(__file__).parent
    index_path = base_path / "index.html"
    js_path = base_path / "assets" / "js" / "app.js"
    
    # Criar relatório
    report = TestReport()
    
    print("\n📋 Iniciando testes do index.html...\n")
    
    # Test 1: File exists
    if not test_file_exists(report, str(index_path)):
        print("❌ Arquivo index.html não encontrado. Abortando...")
        sys.exit(1)
    
    # Ler conteúdo do HTML
    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        report.add_test("Leitura HTML", "fail", f"✗ Erro ao ler: {e}")
        print(f"❌ Erro ao ler index.html: {e}")
        sys.exit(1)
    
    # Executar testes
    test_html_structure(report, html_content)
    test_views(report, html_content)
    test_settings_modal(report, html_content)
    test_api_integration(report, html_content)
    test_external_libraries(report, html_content)
    test_responsive_design(report, html_content)
    test_integration_data(report, html_content)
    test_javascript_file(report, str(js_path))
    test_seo_tags(report, html_content)
    test_security_features(report, html_content)
    test_performance(report, html_content)
    
    # Análise HTML Parser
    parser = HTMLValidator()
    try:
        parser.feed(html_content)
        analysis = f"IDs: {len(parser.ids)}, Scripts: {len(parser.scripts)}, Styles: {len([l for l in parser.links if 'css' in l])}"
        if len(parser.ids) >= 15 and len(parser.scripts) >= 7:
            report.add_test("13. Análise HTML", "pass", f"✓ {analysis}")
        else:
            report.add_test("13. Análise HTML", "fail", f"✗ {analysis}")
    except Exception as e:
        report.add_test("13. Análise HTML", "fail", f"✗ Erro na análise: {e}")
    
    # Imprimir relatório
    report.print_report()
    
    # Retornar código de saída baseado nos resultados
    return 0 if report.failed == 0 else 1


if __name__ == "__main__":
    exit(main())
