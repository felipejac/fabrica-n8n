#!/usr/bin/env python3
"""
Script para submeter sitemap ao Google Search Console via API
Requer configuração de credenciais OAuth2
"""

import os
import sys
from datetime import datetime

def print_instructions():
    """Imprime instruções de configuração"""
    print("""
╔═══════════════════════════════════════════════════════════════════════╗
║  📊 Submissão de Sitemap ao Google Search Console                    ║
╚═══════════════════════════════════════════════════════════════════════╝

Este script facilita a submissão do sitemap, mas requer configuração manual
inicial no Google Search Console.

═══════════════════════════════════════════════════════════════════════════

📋 PASSO A PASSO MANUAL (Mais Simples):

1️⃣  Acesse: https://search.google.com/search-console
2️⃣  Adicione a propriedade (escolha uma opção):
    
    Opção A - Domínio (Recomendado):
    • Domínio: automationscookbook.com
    • Verificação: Adicione registro TXT no DNS
    
    Opção B - Prefixo de URL (Mais Rápido):
    • URL: https://felipejac.github.io/fabrica-n8n/
    • Verificação: Tag HTML no <head> ou arquivo HTML

3️⃣  Após verificação, vá em "Sitemaps" no menu lateral

4️⃣  Digite no campo "Adicionar um novo sitemap":
    sitemap.xml

5️⃣  Clique em "Enviar"

6️⃣  Aguarde 24-48h para ver resultados em "Cobertura"

═══════════════════════════════════════════════════════════════════════════

🔐 OPÇÃO AVANÇADA - API (Automação):

Se você quer automatizar, precisará:

1. Criar projeto no Google Cloud Console
2. Habilitar "Search Console API"
3. Criar credenciais OAuth 2.0
4. Instalar biblioteca: pip install google-auth google-api-python-client
5. Executar este script com credenciais configuradas

Documentação: https://developers.google.com/webmaster-tools/v1/how-tos/authorizing

═══════════════════════════════════════════════════════════════════════════

📊 INFORMAÇÕES DO SEU SITEMAP:
""")
    
    # Verificar se sitemap existe
    sitemap_path = os.path.join(os.path.dirname(__file__), 'sitemap.xml')
    if os.path.exists(sitemap_path):
        size_mb = os.path.getsize(sitemap_path) / (1024 * 1024)
        print(f"✅ Sitemap encontrado: sitemap.xml ({size_mb:.1f} MB)")
        
        # Contar URLs
        with open(sitemap_path, 'r', encoding='utf-8') as f:
            content = f.read()
            url_count = content.count('<loc>')
        print(f"✅ Total de URLs: {url_count:,}")
        
        # URLs importantes para indexação prioritária
        print("\n🎯 URLs PRIORITÁRIAS (solicite indexação manualmente):")
        priority_urls = [
            "https://felipejac.github.io/fabrica-n8n/",
            "https://felipejac.github.io/fabrica-n8n/sobre.html",
            "https://felipejac.github.io/fabrica-n8n/llm.html",
            "https://felipejac.github.io/fabrica-n8n/guia-automacoes-n8n.html",
            "https://felipejac.github.io/fabrica-n8n/casos-de-uso.html",
            "https://felipejac.github.io/fabrica-n8n/integracoes/",
        ]
        for url in priority_urls:
            print(f"   • {url}")
        
        print("\n💡 DICA: Use 'Inspeção de URL' no Search Console para forçar indexação")
        print("   destas páginas prioritárias individualmente.")
    else:
        print("❌ Sitemap não encontrado. Execute: python generate_sitemap.py")
    
    print("\n" + "="*75)
    print("📚 Documentação completa: submit_to_search_console.md")
    print("="*75 + "\n")


def check_api_setup():
    """Verifica se API está configurada"""
    try:
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        
        print("✅ Bibliotecas Google API instaladas")
        
        # Verificar se existe arquivo de credenciais
        cred_files = ['credentials.json', 'token.json', 'client_secret.json']
        found = False
        for cred_file in cred_files:
            if os.path.exists(cred_file):
                print(f"✅ Arquivo de credenciais encontrado: {cred_file}")
                found = True
                break
        
        if not found:
            print("⚠️  Nenhum arquivo de credenciais encontrado")
            print("   Configure OAuth2 antes de usar a API")
            return False
        
        return True
        
    except ImportError:
        print("❌ Bibliotecas Google API não instaladas")
        print("\nInstale com:")
        print("   pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
        return False


def submit_sitemap_api(site_url, sitemap_url):
    """Submete sitemap via API (requer autenticação)"""
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build
        import pickle
        
        SCOPES = ['https://www.googleapis.com/auth/webmasters']
        creds = None
        
        # Token de autenticação
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        # Se não tem credenciais válidas, faz login
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists('credentials.json'):
                    print("❌ Arquivo credentials.json não encontrado")
                    print("   Baixe do Google Cloud Console")
                    return False
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Salvar credenciais
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        # Criar serviço
        service = build('searchconsole', 'v1', credentials=creds)
        
        # Submeter sitemap
        print(f"\n📤 Submetendo sitemap...")
        print(f"   Site: {site_url}")
        print(f"   Sitemap: {sitemap_url}")
        
        request = service.sitemaps().submit(
            siteUrl=site_url,
            feedpath=sitemap_url
        )
        
        response = request.execute()
        
        print("✅ Sitemap submetido com sucesso!")
        print("\n📊 Próximos passos:")
        print("   1. Aguarde 24-48h para indexação inicial")
        print("   2. Monitore em: Sitemaps → Cobertura")
        print("   3. Verifique relatório de Performance após 7 dias")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao submeter via API: {e}")
        print("\n💡 Sugestão: Use o método manual (mais simples)")
        return False


def main():
    """Função principal"""
    print("\n" + "="*75)
    print("  🚀 Automations Cookbook - Submissão ao Google Search Console")
    print("="*75 + "\n")
    
    # Mostrar instruções
    print_instructions()
    
    # Perguntar se quer usar API
    use_api = input("❓ Você configurou a API do Google? (s/N): ").lower().strip()
    
    if use_api == 's':
        print("\n🔍 Verificando configuração da API...")
        if check_api_setup():
            print("\n📋 Configure os seguintes valores:")
            site_url = input("   URL do site (ex: sc-domain:automationscookbook.com): ").strip()
            if not site_url:
                site_url = "https://felipejac.github.io/fabrica-n8n/"
                print(f"   Usando padrão: {site_url}")
            
            sitemap_url = f"{site_url.rstrip('/')}/sitemap.xml"
            
            confirm = input(f"\n   Submeter {sitemap_url}? (s/N): ").lower().strip()
            if confirm == 's':
                submit_sitemap_api(site_url, sitemap_url)
            else:
                print("❌ Cancelado pelo usuário")
        else:
            print("\n💡 Configure a API ou use o método manual descrito acima")
    else:
        print("\n✅ Sem problemas! O método manual é mais simples e funciona perfeitamente.")
        print("   Siga as instruções acima ou consulte: submit_to_search_console.md")
    
    print("\n" + "="*75)
    print("  ✨ Obrigado por usar Automations Cookbook!")
    print("="*75 + "\n")


if __name__ == "__main__":
    main()
