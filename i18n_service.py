#!/usr/bin/env python3
"""
🌍 AI Factory - Internationalization (i18n) Service
Sistema de tradução e localização com detecção automática de localidade
Melhores práticas: gettext, locale detection, content negotiation
"""

import os
import json
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path
from enum import Enum
from datetime import datetime
import hashlib

# ============================================================================
# CONFIGURAÇÃO GLOBAL
# ============================================================================

class Language(Enum):
    """Idiomas suportados"""
    PT = "pt"      # Português (padrão)
    EN = "en"      # Inglês
    ES = "es"      # Espanhol (futuro)
    FR = "fr"      # Francês (futuro)

class Region(Enum):
    """Regiões específicas para localização"""
    BR = "BR"      # Brasil
    PT = "PT"      # Portugal
    US = "US"      # USA
    GB = "GB"      # UK
    GLOBAL = "GLOBAL"  # Resto do mundo

@dataclass
class LocaleConfig:
    """Configuração de localização"""
    language: Language
    region: Region
    timezone: str
    currency: str
    date_format: str
    decimal_separator: str
    thousands_separator: str
    
    @property
    def locale_code(self) -> str:
        """Retorna código locale (pt_BR, en_US, etc)"""
        return f"{self.language.value}_{self.region.value}"
    
    @property
    def should_use_portuguese(self) -> bool:
        """Determina se deve usar português"""
        return self.region in [Region.BR, Region.PT]

# ============================================================================
# GEOLOCALIZAÇÃO E DETECÇÃO DE LOCALIDADE
# ============================================================================

class GeoLocationDetector:
    """
    Detecta localização do usuário baseado em múltiplas fontes
    Melhores práticas: fallbacks, cache, performance
    """
    
    def __init__(self):
        # Cache simples em memória
        self.cache: Dict[str, LocaleConfig] = {}
        # IPs de teste para desenvolvimento
        self.test_ips = {
            "200.1.0.0": Region.BR,      # Brasil (exemplo)
            "189.0.0.0": Region.BR,      # Brasil
            "185.0.0.0": Region.PT,      # Portugal
            "203.0.113.0": Region.US,    # USA
            "198.51.100.0": Region.US,   # USA
            "192.0.2.0": Region.GB,      # UK
        }
    
    def detect_from_ip(self, ip_address: str) -> Optional[Region]:
        """
        Detecta região a partir do IP
        Em produção, usar GeoIP2 ou MaxMind
        """
        # Desenvolvimento: usar teste IPs
        for test_ip, region in self.test_ips.items():
            if ip_address.startswith(test_ip.split(".")[0]):
                return region
        return None
    
    def detect_from_headers(self, 
                           accept_language: Optional[str] = None,
                           cloudflare_country: Optional[str] = None,
                           user_agent: Optional[str] = None) -> Language:
        """
        Detecta idioma a partir de headers HTTP
        Ordem de prioridade:
        1. CF-IPCountry (Cloudflare)
        2. Accept-Language
        3. User-Agent
        """
        # 1. Cloudflare Country Header (melhor opção)
        if cloudflare_country:
            country = cloudflare_country.upper()
            # Mapa país → idioma
            country_lang_map = {
                "BR": Language.PT, "PT": Language.PT,
                "US": Language.EN, "GB": Language.EN,
                "AU": Language.EN, "CA": Language.EN,
                "ES": Language.ES, "MX": Language.ES,
                "FR": Language.FR,
            }
            return country_lang_map.get(country, Language.PT)
        
        # 2. Accept-Language header
        if accept_language:
            # Parse: "pt-BR,pt;q=0.9,en;q=0.8"
            langs = [
                lang.split(";")[0].split("-")[0].lower()
                for lang in accept_language.split(",")
            ]
            lang_priority = {
                "pt": Language.PT,
                "en": Language.EN,
                "es": Language.ES,
                "fr": Language.FR,
            }
            for lang_code in langs:
                if lang_code in lang_priority:
                    return lang_priority[lang_code]
        
        # 3. Default
        return Language.PT
    
    def get_locale_config(self,
                         ip_address: str = "127.0.0.1",
                         accept_language: Optional[str] = None,
                         cloudflare_country: Optional[str] = None) -> LocaleConfig:
        """
        Retorna configuração de localização completa
        Com prioridade: CF-IPCountry > IP > Accept-Language > Default
        """
        # Cache hit
        cache_key = f"{ip_address}:{accept_language}:{cloudflare_country}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Detectar região do IP ou headers
        region = None
        
        # 1. Cloudflare Country é mais confiável
        if cloudflare_country:
            country = cloudflare_country.upper()
            country_region_map = {
                "BR": Region.BR, "PT": Region.PT,
                "US": Region.US, "GB": Region.GB,
                "AU": Region.US, "CA": Region.US,
                "ES": Region.GLOBAL, "MX": Region.GLOBAL,
                "FR": Region.GLOBAL,
            }
            region = country_region_map.get(country)
        
        # 2. IP Geolocation
        if not region:
            region = self.detect_from_ip(ip_address)
        
        # 3. Default
        if not region:
            region = Region.GLOBAL
        
        # Detectar idioma
        language = self.detect_from_headers(
            accept_language=accept_language,
            cloudflare_country=cloudflare_country
        )
        
        # Sobrescrever: Brasil e Portugal usam português
        if region in [Region.BR, Region.PT]:
            language = Language.PT
        
        # Mapa region-timezone
        timezone_map = {
            Region.BR: "America/Sao_Paulo",
            Region.PT: "Europe/Lisbon",
            Region.US: "America/New_York",
            Region.GB: "Europe/London",
            Region.GLOBAL: "UTC",
        }
        
        locale = LocaleConfig(
            language=language,
            region=region,
            timezone=timezone_map.get(region, "UTC"),
            currency="BRL" if region == Region.BR else "USD",
            date_format="%d/%m/%Y" if region in [Region.BR, Region.PT] else "%m/%d/%Y",
            decimal_separator="," if region in [Region.BR, Region.PT] else ".",
            thousands_separator="." if region in [Region.BR, Region.PT] else ",",
        )
        
        # Cache
        self.cache[cache_key] = locale
        return locale

# ============================================================================
# SISTEMA DE TRADUÇÃO
# ============================================================================

class TranslationMemory:
    """
    Memória de tradução com suporte a múltiplos idiomas
    Padrão gettext: chave em português, valores em outros idiomas
    """
    
    # Dicionário de tradução estruturado
    TRANSLATIONS = {
        # Navegação
        "🏠 Home": {
            Language.EN: "🏠 Home",
            Language.PT: "🏠 Home",
        },
        "🏭 Gerador": {
            Language.EN: "🏭 Generator",
            Language.PT: "🏭 Gerador",
        },
        "📚 Templates": {
            Language.EN: "📚 Templates",
            Language.PT: "📚 Templates",
        },
        "🔌 Integrações": {
            Language.EN: "🔌 Integrations",
            Language.PT: "🔌 Integrações",
        },
        "🧰 Toolbox": {
            Language.EN: "🧰 Toolbox",
            Language.PT: "🧰 Toolbox",
        },
        "🎓 Academia": {
            Language.EN: "🎓 Academy",
            Language.PT: "🎓 Academia",
        },
        "🚑 Doctor": {
            Language.EN: "🚑 Doctor",
            Language.PT: "🚑 Doctor",
        },
        
        # Títulos
        "AI Factory | Automação e Templates com IA": {
            Language.EN: "AI Factory | Automation and Templates with AI",
            Language.PT: "AI Factory | Automação e Templates com IA",
        },
        "Sua central de comando para n8n: Templates, Geradores de Código, Debugger com IA e Documentação.": {
            Language.EN: "Your command center for n8n: Templates, Code Generators, AI Debugger and Documentation.",
            Language.PT: "Sua central de comando para n8n: Templates, Geradores de Código, Debugger com IA e Documentação.",
        },
        
        # Buttons & CTA
        "Explorar Templates": {
            Language.EN: "Explore Templates",
            Language.PT: "Explorar Templates",
        },
        "Ver Integrações": {
            Language.EN: "View Integrations",
            Language.PT: "Ver Integrações",
        },
        "Comece Agora": {
            Language.EN: "Get Started",
            Language.PT: "Comece Agora",
        },
        
        # Configurações
        "Configurações": {
            Language.EN: "Settings",
            Language.PT: "Configurações",
        },
        "Google Gemini API Key": {
            Language.EN: "Google Gemini API Key",
            Language.PT: "Google Gemini API Key",
        },
        "Cole sua chave aqui...": {
            Language.EN: "Paste your key here...",
            Language.PT: "Cole sua chave aqui...",
        },
        "Cancelar": {
            Language.EN: "Cancel",
            Language.PT: "Cancelar",
        },
        "Salvar": {
            Language.EN: "Save",
            Language.PT: "Salvar",
        },
        
        # Debugger
        "Doutor N8N": {
            Language.EN: "N8N Doctor",
            Language.PT: "Doutor N8N",
        },
        "Diagnóstico de erros com IA.": {
            Language.EN: "AI-powered error diagnosis.",
            Language.PT: "Diagnóstico de erros com IA.",
        },
        "Console de Erro": {
            Language.EN: "Error Console",
            Language.PT: "Console de Erro",
        },
        "Diagnosticar com IA": {
            Language.EN: "Diagnose with AI",
            Language.PT: "Diagnosticar com IA",
        },
        
        # Academia
        "Academia N8N": {
            Language.EN: "N8N Academy",
            Language.PT: "Academia N8N",
        },
        "Snippets de JavaScript prontos para copiar e colar.": {
            Language.EN: "JavaScript snippets ready to copy and paste.",
            Language.PT: "Snippets de JavaScript prontos para copiar e colar.",
        },
        
        # Library
        "Biblioteca de Templates": {
            Language.EN: "Template Library",
            Language.PT: "Biblioteca de Templates",
        },
        "Procure templates por nome, tags ou integrações.": {
            Language.EN: "Search templates by name, tags or integrations.",
            Language.PT: "Procure templates por nome, tags ou integrações.",
        },
        
        # Toolbox
        "Caixa de Ferramentas": {
            Language.EN: "Toolbox",
            Language.PT: "Caixa de Ferramentas",
        },
        "Utilitários para desenvolvedores n8n.": {
            Language.EN: "Utilities for n8n developers.",
            Language.PT: "Utilitários para desenvolvedores n8n.",
        },
        
        # Footer
        "Sobre o AI Factory": {
            Language.EN: "About AI Factory",
            Language.PT: "Sobre o AI Factory",
        },
        "O AI Factory é uma suite open-source projetada para acelerar o desenvolvimento de automações.": {
            Language.EN: "AI Factory is an open-source suite designed to accelerate automation development.",
            Language.PT: "O AI Factory é uma suite open-source projetada para acelerar o desenvolvimento de automações.",
        },
        "Recursos Populares": {
            Language.EN: "Popular Resources",
            Language.PT: "Recursos Populares",
        },
        "Tags": {
            Language.EN: "Tags",
            Language.PT: "Tags",
        },
    }
    
    @staticmethod
    def translate(text: str, language: Language) -> str:
        """
        Traduz texto para o idioma especificado
        Se não encontrar, retorna o texto original
        """
        if language == Language.PT:
            return text  # Português é a lingua base
        
        if text in TranslationMemory.TRANSLATIONS:
            return TranslationMemory.TRANSLATIONS[text].get(language, text)
        
        return text  # Fallback ao original

# ============================================================================
# PROCESSADOR DE HTML
# ============================================================================

class HTMLTranslator:
    """
    Traduz conteúdo HTML mantendo estrutura e IDs
    Usa regex para preservar tags e atributos
    """
    
    def __init__(self, translation_memory: TranslationMemory):
        self.translations = translation_memory
        # Elementos que nunca devem ser traduzidos
        self.preserve_tags = {
            'code', 'pre', 'script', 'style', 'meta', 
            'link', 'title', 'id', 'class', 'data-'
        }
    
    def should_skip_text(self, text: str) -> bool:
        """Verifica se texto deve ser pulado"""
        # Pular: IDs, classes, URLs, emails, códigos
        return (
            text.startswith("#") or
            text.startswith(".") or
            text.startswith("http") or
            "@" in text or
            "::" in text or
            len(text) < 3 or
            text.isupper() and len(text) < 10  # Provavelmente acrônimo
        )
    
    def translate_html(self, html_content: str, language: Language) -> str:
        """
        Traduz conteúdo HTML preservando estrutura
        """
        if language == Language.PT:
            return html_content  # Português é original
        
        result = html_content
        
        # 1. Traduzir atributos de títulos e placeholders
        # <title>...</title>
        result = re.sub(
            r'<title>([^<]+)</title>',
            lambda m: f'<title>{self.translations.translate(m.group(1), language)}</title>',
            result
        )
        
        # meta name="description"
        result = re.sub(
            r'(content=")([^"]+)(")',
            lambda m: m.group(1) + self.translations.translate(m.group(2), language) + m.group(3)
            if 'description' in result[max(0, result.rfind(m.group(0), 0, 200)-200):result.rfind(m.group(0))]
            else m.group(0),
            result
        )
        
        # 2. Traduzir textos entre tags (mas não inside <code>, <script>, etc)
        # Pattern: >texto< mas não dentro de tags especiais
        def translate_text_nodes(match):
            tag = match.group(1)
            text = match.group(2)
            end_tag = match.group(3)
            
            # Verificar se está dentro de tag preservada
            if any(skip in tag.lower() or skip in end_tag.lower() 
                   for skip in self.preserve_tags):
                return match.group(0)
            
            if self.should_skip_text(text):
                return match.group(0)
            
            translated = self.translations.translate(text.strip(), language)
            whitespace_prefix = len(text) - len(text.lstrip())
            whitespace_suffix = len(text) - len(text.rstrip())
            
            return (tag + 
                    ' ' * whitespace_prefix + 
                    translated + 
                    ' ' * whitespace_suffix + 
                    end_tag)
        
        result = re.sub(
            r'(>)\s*([^<>]+?)\s*(<)',
            translate_text_nodes,
            result
        )
        
        # 3. Traduzir atributos onclick e data-*
        def translate_onclick(match):
            full = match.group(0)
            # Pular funções e variáveis JavaScript
            if 'switchView' in full or 'function' in full:
                return full
            return full
        
        result = re.sub(r'onclick="([^"]*)"', translate_onclick, result)
        
        return result

# ============================================================================
# GERADOR DE ARQUIVOS TRADUCIDOS
# ============================================================================

class TranslationGenerator:
    """
    Gera arquivos HTML traduzidos em múltiplos idiomas
    Estrutura: /translated/en/, /translated/es/, etc.
    """
    
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.translated_dir = self.base_dir / "translated"
        self.translator = HTMLTranslator(TranslationMemory())
        self.geo_detector = GeoLocationDetector()
        self.stats = {
            "files_processed": 0,
            "files_translated": 0,
            "total_translations": 0,
        }
    
    def setup_directories(self):
        """Cria estrutura de diretórios para traduções"""
        languages = [Language.EN, Language.ES, Language.FR]
        
        for lang in languages:
            lang_dir = self.translated_dir / lang.value
            lang_dir.mkdir(parents=True, exist_ok=True)
            
            # Copiar estrutura de assets
            assets_src = self.base_dir / "assets"
            assets_dst = lang_dir / "assets"
            if assets_src.exists() and not assets_dst.exists():
                import shutil
                shutil.copytree(assets_src, assets_dst)
        
        print(f"✅ Estrutura de diretórios criada em {self.translated_dir}")
    
    def translate_file(self, 
                      source_file: str,
                      languages: List[Language] = None) -> Dict[Language, str]:
        """
        Traduz um arquivo HTML para múltiplos idiomas
        Retorna: {Language: caminho_arquivo_traduzido}
        """
        if languages is None:
            languages = [Language.EN]
        
        source_path = self.base_dir / source_file
        if not source_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {source_path}")
        
        with open(source_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.stats["files_processed"] += 1
        results = {}
        
        for language in languages:
            if language == Language.PT:
                # Português: copiar original
                results[language] = str(source_path)
                continue
            
            # Traduzir
            translated_content = self.translator.translate_html(content, language)
            
            # Salvar
            lang_dir = self.translated_dir / language.value
            output_path = lang_dir / source_file
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(translated_content)
            
            results[language] = str(output_path)
            self.stats["files_translated"] += 1
        
        return results
    
    def translate_integrations(self, integrations_dir: str = "integracoes"):
        """
        Traduz todas as páginas de integrações
        """
        integrations_path = self.base_dir / integrations_dir
        
        if not integrations_path.exists():
            print(f"⚠️ Diretório de integrações não encontrado: {integrations_path}")
            return
        
        html_files = list(integrations_path.glob("*.html"))
        print(f"📁 Encontrados {len(html_files)} arquivos de integração")
        
        for html_file in html_files:
            relative_path = html_file.relative_to(self.base_dir)
            try:
                self.translate_file(str(relative_path), languages=[Language.EN])
            except Exception as e:
                print(f"❌ Erro ao traduzir {html_file}: {e}")
    
    def generate_translation_manifest(self):
        """
        Gera manifesto JSON com metadados de tradução
        Útil para front-end gerenciar idiomas disponíveis
        """
        manifest = {
            "generated": datetime.now().isoformat(),
            "version": "1.0.0",
            "languages": {
                lang.value: {
                    "name": self._get_language_name(lang),
                    "native_name": self._get_language_native_name(lang),
                    "direction": "ltr",  # left-to-right
                    "regions": self._get_regions_for_language(lang),
                }
                for lang in Language
            },
            "statistics": self.stats,
        }
        
        manifest_path = self.translated_dir / "manifest.json"
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Manifesto de tradução gerado: {manifest_path}")
        return manifest
    
    @staticmethod
    def _get_language_name(lang: Language) -> str:
        """Nome do idioma em inglês"""
        names = {
            Language.PT: "Portuguese",
            Language.EN: "English",
            Language.ES: "Spanish",
            Language.FR: "French",
        }
        return names.get(lang, lang.value)
    
    @staticmethod
    def _get_language_native_name(lang: Language) -> str:
        """Nome nativo do idioma"""
        names = {
            Language.PT: "Português",
            Language.EN: "English",
            Language.ES: "Español",
            Language.FR: "Français",
        }
        return names.get(lang, lang.value)
    
    @staticmethod
    def _get_regions_for_language(lang: Language) -> List[str]:
        """Regiões onde o idioma é usado"""
        regions = {
            Language.PT: ["BR", "PT"],
            Language.EN: ["US", "GB", "AU", "CA"],
            Language.ES: ["ES", "MX", "AR", "CO"],
            Language.FR: ["FR", "CA", "BE", "CH"],
        }
        return regions.get(lang, [])

# ============================================================================
# MIDDLEWARE E ROUTER (Flask compatible)
# ============================================================================

class I18nMiddleware:
    """
    Middleware para roteamento automático de idiomas
    Detecta localização e serve versão apropriada
    """
    
    def __init__(self, translation_generator: TranslationGenerator):
        self.generator = translation_generator
        self.geo_detector = GeoLocationDetector()
    
    def get_language_from_request(self,
                                  ip_address: str = "127.0.0.1",
                                  accept_language: Optional[str] = None,
                                  cloudflare_country: Optional[str] = None,
                                  cookie_lang: Optional[str] = None) -> Language:
        """
        Retorna o idioma apropriado para a requisição
        Ordem de prioridade:
        1. Cookie (user preference)
        2. Cloudflare Country
        3. Accept-Language header
        4. IP Geolocation
        5. Default (PT)
        """
        # 1. Cookie tem prioridade (user preference)
        if cookie_lang:
            try:
                return Language[cookie_lang.upper()]
            except (KeyError, AttributeError):
                pass
        
        # 2-4. Usar geo detector
        locale = self.geo_detector.get_locale_config(
            ip_address=ip_address,
            accept_language=accept_language,
            cloudflare_country=cloudflare_country
        )
        
        return locale.language
    
    def get_file_path(self, language: Language, file_path: str) -> str:
        """
        Retorna caminho correto do arquivo baseado no idioma
        """
        if language == Language.PT:
            return file_path  # Original
        
        # Traduzido
        return f"translated/{language.value}/{file_path}"

# ============================================================================
# EXEMPLO DE USO E UTILITÁRIOS
# ============================================================================

def generate_language_selector_html(current_lang: Language = Language.PT) -> str:
    """
    Gera HTML para seletor de idioma
    Útil para colocar no footer ou header
    """
    html = """
    <div class="language-selector">
        <label for="lang-select">🌍 Language:</label>
        <select id="lang-select" onchange="changeLanguage(this.value)">
    """
    
    for lang in Language:
        selected = "selected" if lang == current_lang else ""
        lang_name = TranslationGenerator._get_language_native_name(lang)
        html += f'            <option value="{lang.value}" {selected}>{lang_name}</option>\n'
    
    html += """        </select>
    </div>
    
    <script>
    function changeLanguage(lang) {
        // Salvar preferência em cookie
        document.cookie = `language=${lang}; path=/; max-age=31536000`;
        
        // Redirecionar ou carregar página
        const currentPath = window.location.pathname;
        if (lang === 'pt') {
            window.location.href = currentPath.replace(/^\\/translated\\/[a-z]{2}\\//, '/');
        } else {
            window.location.href = `/translated/${lang}${currentPath}`;
        }
    }
    </script>
    """
    return html

def print_stats(stats: Dict):
    """Exibe estatísticas de tradução"""
    print("\n" + "=" * 70)
    print("📊 ESTATÍSTICAS DE TRADUÇÃO")
    print("=" * 70)
    print(f"Arquivos processados: {stats['files_processed']}")
    print(f"Arquivos traduzidos: {stats['files_translated']}")
    print(f"Total de traduções: {stats['total_translations']}")
    print("=" * 70 + "\n")

# ============================================================================
# CLI - INTERFACE DE LINHA DE COMANDO
# ============================================================================

def main():
    """Script principal para gerar traduções"""
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(
        description="🌍 AI Factory - Internacionalização (i18n)"
    )
    parser.add_argument(
        "--base-dir",
        default=".",
        help="Diretório base do projeto (padrão: .)"
    )
    parser.add_argument(
        "--languages",
        nargs="+",
        default=["en"],
        help="Idiomas para traduzir (padrão: en)"
    )
    parser.add_argument(
        "--setup",
        action="store_true",
        help="Criar estrutura de diretórios"
    )
    parser.add_argument(
        "--translate-index",
        action="store_true",
        help="Traduzir index.html"
    )
    parser.add_argument(
        "--translate-integrations",
        action="store_true",
        help="Traduzir páginas de integrações"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Executar todas as operações"
    )
    
    args = parser.parse_args()
    
    # Converter códigos de idioma para enum
    selected_languages = []
    for lang_code in args.languages:
        try:
            selected_languages.append(Language[lang_code.upper()])
        except KeyError:
            print(f"❌ Idioma não suportado: {lang_code}")
            sys.exit(1)
    
    # Inicializar gerador
    generator = TranslationGenerator(base_dir=args.base_dir)
    
    print("\n🌍 AI Factory - Internacionalização (i18n)")
    print("=" * 70 + "\n")
    
    # Setup
    if args.setup or args.all:
        print("📁 Criando estrutura de diretórios...")
        generator.setup_directories()
    
    # Traduzir index.html
    if args.translate_index or args.all:
        print("\n📄 Traduzindo index.html...")
        try:
            generator.translate_file("index.html", languages=selected_languages)
            print("✅ index.html traduzido com sucesso")
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    # Traduzir integrações
    if args.translate_integrations or args.all:
        print("\n🔌 Traduzindo páginas de integrações...")
        generator.translate_integrations()
        print("✅ Integrações traduzidas com sucesso")
    
    # Gerar manifesto
    print("\n📋 Gerando manifesto de tradução...")
    generator.generate_translation_manifest()
    
    # Exibir estatísticas
    print_stats(generator.stats)
    
    print("🎉 Tradução concluída com sucesso!")
    print(f"📂 Arquivos traduzidos em: {generator.translated_dir}")

if __name__ == "__main__":
    main()
