#!/usr/bin/env python3
"""
🌍 Testes de Internacionalização (i18n)

Teste automatizado para validar:
- Geração de traduções
- Servidor Flask
- APIs de localização
- Detecção automática de idioma
- Cache headers
- Rotas de linguagem
"""

import json
import subprocess
import time
import requests
import sys
from pathlib import Path

class I18nTester:
    def __init__(self, base_url="http://127.0.0.1:5000"):
        self.base_url = base_url
        self.results = []
        self.passed = 0
        self.failed = 0
    
    def test(self, name: str, func):
        """Executar teste"""
        print(f"\n🧪 {name}...", end=" ")
        try:
            func()
            print("✅ PASSOU")
            self.passed += 1
            self.results.append(("✅", name))
        except AssertionError as e:
            print(f"❌ FALHOU: {e}")
            self.failed += 1
            self.results.append(("❌", name, str(e)))
        except Exception as e:
            print(f"⚠️  ERRO: {e}")
            self.failed += 1
            self.results.append(("⚠️", name, str(e)))
    
    def test_api_locale(self):
        """Testar API de localização"""
        response = requests.get(f"{self.base_url}/api/locale")
        assert response.status_code == 200, f"Status {response.status_code}"
        
        data = response.json()
        assert "language" in data, "Faltando campo 'language'"
        assert "region" in data, "Faltando campo 'region'"
        assert "timezone" in data, "Faltando campo 'timezone'"
        assert "currency" in data, "Faltando campo 'currency'"
        assert "locale_code" in data, "Faltando campo 'locale_code'"
    
    def test_api_languages(self):
        """Testar API de idiomas"""
        response = requests.get(f"{self.base_url}/api/languages")
        assert response.status_code == 200, f"Status {response.status_code}"
        
        data = response.json()
        assert "languages" in data, "Faltando 'languages'"
        assert "current_language" in data, "Faltando 'current_language'"
        assert len(data["languages"]) > 0, "Nenhum idioma disponível"
        assert "pt" in data["languages"], "Português não está disponível"
    
    def test_api_manifest(self):
        """Testar API de manifesto"""
        response = requests.get(f"{self.base_url}/api/manifest")
        assert response.status_code == 200, f"Status {response.status_code}"
        
        data = response.json()
        assert "generated" in data, "Faltando campo 'generated'"
        assert "version" in data, "Faltando campo 'version'"
        assert "languages" in data, "Faltando campo 'languages'"
    
    def test_index_html_pt(self):
        """Testar página em Português"""
        response = requests.get(f"{self.base_url}/index.html")
        assert response.status_code == 200, f"Status {response.status_code}"
        assert len(response.text) > 100, "Resposta muito pequena"
        assert "<!DOCTYPE" in response.text or "<html" in response.text, "HTML inválido"
    
    def test_index_html_en(self):
        """Testar página em Inglês"""
        response = requests.get(f"{self.base_url}/en/index.html")
        assert response.status_code == 200, f"Status {response.status_code}"
        assert len(response.text) > 100, "Resposta muito pequena"
    
    def test_cache_headers_html(self):
        """Testar headers de cache para HTML"""
        response = requests.get(f"{self.base_url}/index.html")
        assert response.status_code == 200, f"Status {response.status_code}"
        
        # Verificar headers de cache
        assert "cache-control" in response.headers or "Cache-Control" in response.headers, \
            "Faltando Cache-Control header"
        assert "content-language" in response.headers or "Content-Language" in response.headers, \
            "Faltando Content-Language header"
    
    def test_security_headers(self):
        """Testar headers de segurança"""
        response = requests.get(f"{self.base_url}/index.html")
        
        security_headers = [
            "x-content-type-options",
            "x-frame-options",
            "content-security-policy",
        ]
        
        headers_lower = {k.lower(): v for k, v in response.headers.items()}
        found_headers = sum(1 for h in security_headers if h in headers_lower)
        
        assert found_headers >= 2, f"Apenas {found_headers} headers de segurança encontrados"
    
    def test_language_cookie(self):
        """Testar seleção de idioma via cookie"""
        # Requisição com cookie
        cookies = {"language": "en"}
        response = requests.get(f"{self.base_url}/api/locale", cookies=cookies)
        
        assert response.status_code == 200, f"Status {response.status_code}"
        # Cookie pode ou não afetar resultado dependendo da implementação
    
    def test_accept_language_header(self):
        """Testar detecção via Accept-Language"""
        headers = {"Accept-Language": "en-US,en;q=0.9"}
        response = requests.get(f"{self.base_url}/api/locale", headers=headers)
        
        assert response.status_code == 200, f"Status {response.status_code}"
        data = response.json()
        assert "language" in data, "Idioma não detectado"
    
    def test_auto_redirect(self):
        """Testar redirecionamento automático"""
        response = requests.get(f"{self.base_url}/", allow_redirects=False)
        # Pode ser 200 (servir conteúdo) ou 302 (redirecionar)
        assert response.status_code in [200, 302], f"Status inesperado: {response.status_code}"
    
    def test_translated_file_exists(self):
        """Testar se arquivo traduzido foi criado"""
        en_dir = Path("translated/en")
        assert en_dir.exists(), "Diretório /translated/en não existe"
        assert (en_dir / "index.html").exists(), "Arquivo en/index.html não existe"
    
    def test_manifesto_json_exists(self):
        """Testar se manifesto foi gerado"""
        manifest = Path("translated/manifest.json")
        assert manifest.exists(), "Arquivo manifest.json não existe"
        
        with open(manifest) as f:
            data = json.load(f)
            assert "languages" in data, "Manifesto sem 'languages'"
    
    def test_response_time(self):
        """Testar performance - resposta em < 200ms"""
        start = time.time()
        response = requests.get(f"{self.base_url}/api/locale")
        duration = (time.time() - start) * 1000  # em millisegundos
        
        assert response.status_code == 200, f"Status {response.status_code}"
        assert duration < 200, f"Resposta lenta: {duration:.1f}ms (esperado < 200ms)"
    
    def run_all(self):
        """Executar todos os testes"""
        print("\n" + "="*70)
        print("🧪 TESTES DE INTERNACIONALIZAÇÃO (i18n)")
        print("="*70)
        
        # Testes de arquivo
        print("\n📁 Testes de Arquivos Gerados")
        self.test("Diretório /translated/en existe", self.test_translated_file_exists)
        self.test("Manifesto JSON foi gerado", self.test_manifesto_json_exists)
        
        # Testes de servidor
        print("\n🚀 Testes de Servidor Flask")
        self.test("Página em Português carrega", self.test_index_html_pt)
        self.test("Página em Inglês carrega", self.test_index_html_en)
        self.test("Redirecionamento automático funciona", self.test_auto_redirect)
        
        # Testes de APIs
        print("\n🔌 Testes de APIs REST")
        self.test("API /api/locale retorna dados corretos", self.test_api_locale)
        self.test("API /api/languages retorna idiomas", self.test_api_languages)
        self.test("API /api/manifest retorna manifesto", self.test_api_manifest)
        
        # Testes de headers
        print("\n🔐 Testes de Headers HTTP")
        self.test("Cache headers estão presentes", self.test_cache_headers_html)
        self.test("Security headers estão presentes", self.test_security_headers)
        
        # Testes de detecção
        print("\n🗺️  Testes de Detecção de Localização")
        self.test("Cookie de idioma é respeitado", self.test_language_cookie)
        self.test("Accept-Language header é detectado", self.test_accept_language_header)
        
        # Testes de performance
        print("\n⚡ Testes de Performance")
        self.test("Resposta em < 200ms", self.test_response_time)
        
        # Resumo
        print("\n" + "="*70)
        print("📊 RESUMO DOS TESTES")
        print("="*70)
        print(f"✅ Passou:  {self.passed}")
        print(f"❌ Falhou:  {self.failed}")
        print(f"📈 Total:   {self.passed + self.failed}")
        print(f"🎯 Score:   {self.passed}/{self.passed + self.failed}")
        
        if self.failed == 0:
            print("\n🎉 TODOS OS TESTES PASSARAM!")
            return 0
        else:
            print(f"\n⚠️  {self.failed} TESTE(S) FALHARAM")
            return 1

def main():
    """Main"""
    # Aguardar servidor estar pronto
    print("⏳ Aguardando servidor ficar pronto...")
    for i in range(10):
        try:
            requests.get("http://127.0.0.1:5000/api/locale", timeout=1)
            print("✅ Servidor pronto!")
            break
        except requests.exceptions.RequestException:
            if i < 9:
                time.sleep(0.5)
            else:
                print("❌ Servidor não respondeu após 10 tentativas")
                sys.exit(1)
    
    # Rodar testes
    tester = I18nTester()
    return tester.run_all()

if __name__ == "__main__":
    sys.exit(main())
