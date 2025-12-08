Plano de Implementação: N8N Factory pSEO & Growth

Este documento descreve a arquitetura para transformar o N8N Factory em um diretório de integrações escalável, focado em capturar tráfego de cauda longa (ex: "como integrar x com y").

1. Estrutura de URLs (Silo Architecture)

Para maximizar a autoridade de domínio, adotaremos uma estrutura hierárquica clara:

Home (Ferramenta): /index.html (Sua SPA atual, focada em utilitários).

Diretório (Hub): /integracoes/index.html (Página que lista todas as integrações geradas).

Páginas de Destino (Spokes): /integracoes/{slug-url}.html

Ex: /integracoes/facebook-ads-para-whatsapp-chatwoot-n8n.html

Ex: /integracoes/typeform-para-google-sheets-n8n.html

2. Modelo de Dados (Schema do CSV)

A base de dados automacoes_db.csv alimenta o gerador. Campos definidos:

software_a: Origem (ex: Facebook).

software_b: Destino (ex: Google Sheets).

tipo_evento: Gatilho (ex: Lead).

titulo_pagina: H1 Otimizado (Keyword principal).

slug_url: URL amigável (sem acentos, com hífens).

descricao_curta: Meta description e intro.

caso_uso_resumido: Texto explicativo do "Porquê".

passos_resumo: Lista técnica de steps (separados por |).

json_n8n_url: Link para download do template.

tags: Categorias para linkagem interna.

3. Funil de Conversão (CTAs)

Cada página gerada terá pontos de conversão estratégicos:

Topo (Interesse): Botão "Baixar JSON" -> Mede intenção de uso.

Meio (Engajamento): Links para "Ferramentas Relacionadas" (Toolbox, Gerador).

Fundo (Venda): "Precisa de ajuda para implementar?" -> Link para WhatsApp/Consultoria.

4. Próximos Passos (Escala)

Rodar o Script: Execute python build.py para gerar as primeiras 20 páginas na pasta integracoes/.

Indexação: Submeter o sitemap gerado no Google Search Console (o script pode ser expandido para gerar sitemap.xml).

Expansão: Usar a IA (Gemini) para gerar mais 200 linhas no CSV combinando ferramentas populares (HubSpot, Salesforce, WooCommerce).
