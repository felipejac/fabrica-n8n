#!/usr/bin/env python3
"""
🚀 AI Factory - Servidor i18n com Flask
Implementa detecção de localização e roteamento automático de idiomas
Melhores práticas: caching, content negotiation, performance
"""

import os
import mimetypes
from pathlib import Path
from flask import Flask, request, send_file, render_template_string, make_response
from werkzeug.exceptions import NotFound, BadRequest
from i18n_service import (
    I18nMiddleware,
    TranslationGenerator,
    GeoLocationDetector,
    Language,
    Region,
)

# ============================================================================
# CONFIGURAÇÃO
# ============================================================================

class Config:
    """Configuração da aplicação"""
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    BASE_DIR = Path(__file__).parent
    TRANSLATED_DIR = BASE_DIR / "translated"
    
    # Cache (em segundos)
    CACHE_DURATION_HTML = 3600      # 1 hora para HTML
    CACHE_DURATION_ASSETS = 86400   # 1 dia para assets
    CACHE_DURATION_DEFAULT = 300    # 5 min padrão
    
    # CORS
    ALLOWED_ORIGINS = [
        "localhost:5000",
        "localhost:3000",
        "127.0.0.1:5000",
    ]
    
    # Rate limiting
    MAX_REQUESTS_PER_MINUTE = 60
    
    # Compressão
    GZIP_COMPRESSION = True
    GZIP_LEVEL = 6

# ============================================================================
# APLICAÇÃO FLASK
# ============================================================================

def create_app():
    """Factory function para criar aplicação Flask"""
    app = Flask(__name__, static_folder=str(Config.BASE_DIR / "assets"))
    app.config.from_object(Config)
    
    # Inicializar i18n
    generator = TranslationGenerator(base_dir=str(Config.BASE_DIR))
    i18n = I18nMiddleware(generator)
    geo_detector = GeoLocationDetector()
    
    # ========================================================================
    # HELPERS
    # ========================================================================
    
    def get_client_ip():
        """Obtém IP do cliente respeitando proxies"""
        # X-Forwarded-For (Cloudflare, AWS, etc)
        if request.headers.get('X-Forwarded-For'):
            return request.headers.get('X-Forwarded-For').split(',')[0].strip()
        # X-Real-IP (Nginx)
        if request.headers.get('X-Real-IP'):
            return request.headers.get('X-Real-IP')
        # Fallback
        return request.remote_addr or "127.0.0.1"
    
    def get_cloudflare_country():
        """Obtém país de header Cloudflare (se disponível)"""
        return request.headers.get('CF-IPCountry')
    
    def get_accept_language():
        """Obtém Accept-Language header"""
        return request.headers.get('Accept-Language')
    
    def get_cookie_language():
        """Obtém idioma do cookie"""
        return request.cookies.get('language')
    
    def set_cache_headers(response, duration: int):
        """Define headers de cache"""
        response.headers['Cache-Control'] = f'public, max-age={duration}'
        try:
            response.headers['ETag'] = f'"{hash(response.data)}"'
        except RuntimeError:
            # Response em modo direct passthrough (send_file)
            pass
        return response
    
    def detect_language():
        """Detecta idioma para requisição atual"""
        lang = i18n.get_language_from_request(
            ip_address=get_client_ip(),
            accept_language=get_accept_language(),
            cloudflare_country=get_cloudflare_country(),
            cookie_lang=get_cookie_language()
        )
        return lang
    
    def should_use_portuguese():
        """Verifica se deve usar português"""
        locale = geo_detector.get_locale_config(
            ip_address=get_client_ip(),
            cloudflare_country=get_cloudflare_country()
        )
        return locale.should_use_portuguese
    
    # ========================================================================
    # ROTAS PRINCIPAIS
    # ========================================================================
    
    @app.route('/')
    def root():
        """
        Rota raiz com redirecionamento automático
        Detecta localização e redireciona para versão apropriada
        """
        if should_use_portuguese():
            # Brasil/Portugal: servir português original
            return serve_file('index.html', Language.PT)
        else:
            # Resto do mundo: redirecionar para versão em inglês
            return redirect_to_language(Language.EN, 'index.html')
    
    @app.route('/index.html')
    def index():
        """Serve index.html (original em português)"""
        return serve_file('index.html', Language.PT)
    
    @app.route('/en/index.html')
    @app.route('/en/')
    def index_en():
        """Serve index.html em inglês"""
        return serve_file('index.html', Language.EN)
    
    @app.route('/<lang_code>/<path:filepath>')
    def serve_translated_file(lang_code: str, filepath: str):
        """
        Rota genérica para arquivos traduzidos
        Exemplo: /en/integracoes/google-sheets.html
        """
        try:
            language = Language[lang_code.upper()]
        except (KeyError, ValueError):
            raise NotFound(f"Idioma não suportado: {lang_code}")
        
        return serve_file(filepath, language)
    
    @app.route('/integracoes/<filename>')
    @app.route('/integrações/<filename>')
    def integrations_pt(filename: str):
        """Serve páginas de integração em português"""
        return serve_file(f'integracoes/{filename}', Language.PT)
    
    @app.route('/en/integrations/<filename>')
    def integrations_en(filename: str):
        """Serve páginas de integração em inglês"""
        return serve_file(f'integracoes/{filename}', Language.EN)
    
    def serve_file(filepath: str, language: Language):
        """
        Serve arquivo com cache e compressão
        """
        file_path = i18n.get_file_path(language, filepath)
        full_path = Config.BASE_DIR / file_path
        
        # Security: prevenir path traversal
        try:
            full_path = full_path.resolve()
            if not str(full_path).startswith(str(Config.BASE_DIR.resolve())):
                raise NotFound("Acesso negado")
        except Exception:
            raise NotFound("Arquivo não encontrado")
        
        # Verificar se arquivo existe
        if not full_path.exists():
            # Tentar português como fallback
            if language != Language.PT:
                fallback_path = Config.BASE_DIR / filepath
                if fallback_path.exists():
                    return serve_file(filepath, Language.PT)
            raise NotFound(f"Arquivo não encontrado: {filepath}")
        
        # Servir arquivo
        response = make_response(send_file(
            str(full_path),
            mimetype=get_mimetype(str(full_path))
        ))
        
        # Adicionar language cookie
        response.set_cookie('language', language.value, max_age=31536000, path='/')
        
        # Determinar duração do cache
        if filepath.endswith('.html'):
            cache_duration = Config.CACHE_DURATION_HTML
        elif any(filepath.endswith(ext) for ext in ['.css', '.js', '.woff2', '.svg']):
            cache_duration = Config.CACHE_DURATION_ASSETS
        else:
            cache_duration = Config.CACHE_DURATION_DEFAULT
        
        # Adicionar headers de cache
        set_cache_headers(response, cache_duration)
        
        # Adicionar headers de segurança
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Adicionar header de idioma
        response.headers['Content-Language'] = language.value
        
        return response
    
    @app.route('/api/locale')
    def api_locale():
        """
        API para obter informações de localização do cliente
        Útil para JavaScript detectar configurações
        """
        locale = geo_detector.get_locale_config(
            ip_address=get_client_ip(),
            accept_language=get_accept_language(),
            cloudflare_country=get_cloudflare_country()
        )
        
        return {
            'language': locale.language.value,
            'language_name': TranslationGenerator._get_language_native_name(
                locale.language
            ),
            'region': locale.region.value,
            'timezone': locale.timezone,
            'currency': locale.currency,
            'locale_code': locale.locale_code,
            'should_use_portuguese': locale.should_use_portuguese,
        }
    
    @app.route('/api/languages')
    def api_languages():
        """API para obter lista de idiomas disponíveis"""
        return {
            'languages': {
                lang.value: {
                    'name': TranslationGenerator._get_language_name(lang),
                    'native_name': TranslationGenerator._get_language_native_name(lang),
                    'regions': TranslationGenerator._get_regions_for_language(lang),
                }
                for lang in Language
            },
            'current_language': detect_language().value,
        }
    
    @app.route('/api/manifest')
    def api_manifest():
        """API para obter manifesto de tradução"""
        manifest_path = Config.BASE_DIR / 'translated' / 'manifest.json'
        if manifest_path.exists():
            import json
            with open(manifest_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'error': 'Manifesto não encontrado'}, 404
    
    @app.route('/language-selector.html')
    def language_selector():
        """Página com seletor de idioma"""
        from i18n_service import generate_language_selector_html
        html = generate_language_selector_html(detect_language())
        return html
    
    # ========================================================================
    # TRATAMENTO DE ERROS
    # ========================================================================
    
    @app.errorhandler(404)
    def not_found(error):
        """Erro 404 personalizado"""
        return render_template_string("""
        <!DOCTYPE html>
        <html lang="pt">
        <head>
            <meta charset="UTF-8">
            <title>404 - Página não encontrada</title>
            <style>
                body { font-family: sans-serif; margin: 50px; }
                h1 { color: #e74c3c; }
                p { color: #7f8c8d; }
                a { color: #3498db; }
            </style>
        </head>
        <body>
            <h1>404 - Página não encontrada</h1>
            <p>Desculpe, a página que você procura não existe.</p>
            <a href="/">← Voltar ao início</a>
        </body>
        </html>
        """), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Erro 500 personalizado"""
        return render_template_string("""
        <!DOCTYPE html>
        <html lang="pt">
        <head>
            <meta charset="UTF-8">
            <title>500 - Erro Interno</title>
            <style>
                body { font-family: sans-serif; margin: 50px; }
                h1 { color: #e74c3c; }
                p { color: #7f8c8d; }
                a { color: #3498db; }
            </style>
        </head>
        <body>
            <h1>500 - Erro Interno do Servidor</h1>
            <p>Desculpe, algo deu errado. Estamos trabalhando para corrigir.</p>
            <a href="/">← Voltar ao início</a>
        </body>
        </html>
        """), 500
    
    # ========================================================================
    # HELPERS (dentro do app context)
    # ========================================================================
    
    def redirect_to_language(language: Language, filepath: str):
        """Redireciona para versão do arquivo em outro idioma"""
        from flask import redirect
        if language == Language.PT:
            return redirect(f'/{filepath}')
        return redirect(f'/{language.value}/{filepath}')
    
    def get_mimetype(filepath: str):
        """Obtém MIME type correto"""
        mime, _ = mimetypes.guess_type(filepath)
        return mime or 'text/plain'
    
    # Injetar helpers no contexto
    app.jinja_env.globals.update(
        detect_language=detect_language,
        should_use_portuguese=should_use_portuguese,
        get_client_ip=get_client_ip,
    )
    
    # ========================================================================
    # LOGGING E MONITORAMENTO
    # ========================================================================
    
    @app.before_request
    def log_request():
        """Log de requisições (em desenvolvimento)"""
        if app.config['DEBUG']:
            print(f"[{request.method}] {request.path}")
            print(f"  IP: {get_client_ip()}")
            print(f"  Accept-Language: {get_accept_language()}")
            print(f"  CF-IPCountry: {get_cloudflare_country()}")
            print(f"  Language Cookie: {get_cookie_language()}")
            print(f"  Detected Language: {detect_language().value}")
    
    @app.after_request
    def add_security_headers(response):
        """Adiciona headers de segurança a todas as respostas"""
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        return response
    
    return app

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Inicia servidor de desenvolvimento"""
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(
        description="🚀 AI Factory - Servidor i18n com Flask"
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host para bind (padrão: 127.0.0.1)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="Porta (padrão: 5000)"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Modo debug"
    )
    parser.add_argument(
        "--generate-translations",
        action="store_true",
        help="Gerar traduções antes de iniciar"
    )
    
    args = parser.parse_args()
    
    # Gerar traduções se necessário
    if args.generate_translations:
        print("🌍 Gerando traduções...")
        from i18n_service import TranslationGenerator
        generator = TranslationGenerator()
        generator.setup_directories()
        generator.translate_file("index.html", languages=[Language.EN])
        generator.translate_integrations()
        generator.generate_translation_manifest()
        print("✅ Traduções geradas com sucesso")
    
    # Criar e iniciar app
    app = create_app()
    
    print(f"""
    🚀 AI Factory - Servidor i18n
    ====================================
    Host: {args.host}
    Port: {args.port}
    Debug: {args.debug}
    
    URLs:
    - http://{args.host}:{args.port}/                 (Auto-detect)
    - http://{args.host}:{args.port}/index.html       (Português)
    - http://{args.host}:{args.port}/en/index.html    (Inglês)
    
    APIs:
    - http://{args.host}:{args.port}/api/locale       (Info de localização)
    - http://{args.host}:{args.port}/api/languages    (Idiomas disponíveis)
    - http://{args.host}:{args.port}/api/manifest     (Manifesto de tradução)
    
    ====================================
    """)
    
    app.run(
        host=args.host,
        port=args.port,
        debug=args.debug,
        use_reloader=args.debug,
    )

if __name__ == '__main__':
    main()
