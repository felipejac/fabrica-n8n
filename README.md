🏭 AI Factory Ultimate

A Suite Definitiva para Desenvolvedores n8n. > Automação Inteligente, Documentação e Produtividade em um único lugar.

A AI Factory é uma aplicação web estática (Client-Side) projetada para superalimentar a produtividade de quem trabalha com n8n. Ela combina geradores de conteúdo em massa, bibliotecas vastas de recursos e assistentes de IA para resolver problemas complexos em segundos.

🚀 Novas Funcionalidades (v3.5.0)

Esta versão transforma a ferramenta em uma Central de Comando completa:

1. 🏭 Fábrica de Conteúdo (Gerador)

Transforme planilhas CSV em centenas de arquivos de documentação Markdown formatados instantaneamente.

Enriquecimento com IA: Se sua planilha estiver incompleta, a IA preenche descrições e resumos automaticamente.

Saída: Arquivo .zip pronto para download.

2. 📚 Biblioteca de Templates Massiva

Acesso simulado a mais de 3.200 templates de automação.

Busca Instantânea: Filtre por ferramentas (ex: "OpenAI", "Slack", "Stripe").

Gerador de Workflow IA: Descreva o que você precisa (ex: "Monitorar preço do Bitcoin e avisar no Telegram") e a IA escreve o código JSON do workflow para você importar.

3. 🔌 Guia de Integrações

Catálogo interativo com mais de 800 nodes.

Aprenda os principais Gatilhos e Ações de cada serviço.

Veja cenários de uso prático para ferramentas como AWS, Google, HubSpot e mais.

4. 🧰 Toolbox do Automatizador

Ferramentas utilitárias essenciais impulsionadas por IA para configurar nodes difíceis:

Cron Helper: Converta linguagem natural ("toda sexta às 18h") em expressões Cron (0 18 * * 5).

Regex Generator: Crie expressões regulares complexas para validar dados.

cURL to HTTP: Cole um comando cURL e receba o JSON pronto para o node HTTP Request.

JS Generator: Descreva a lógica e receba o código JavaScript para o node Code.

5. 🚑 Doutor N8N (AI Debugger)

Seu workflow quebrou?

Cole o log de erro ou selecione sintomas comuns (Erro 429, JSON Inválido, Memória).

Receba um diagnóstico preciso e passos para solução gerados pela IA.

6. 🎓 Academia N8N

Biblioteca de Snippets JavaScript curados.

Códigos prontos para copiar e colar: Formatação de Datas (Luxon), Manipulação de Arrays, Limpeza de HTML, Validação de CPF/CNPJ, etc.

⚡ Performance e SEO

O projeto foi reescrito para máxima performance e visibilidade:

Arquitetura SPA: Tudo roda em um único arquivo index.html.

SEO Técnico: Inclui JSON-LD (Schema.org) para WebApplication e FAQPage.

Core Web Vitals: Scripts carregados com defer, conexões pré-estabelecidas (preconnect) e geração de dados "lazy" para não bloquear a renderização inicial.

🔒 Segurança e Privacidade (Modelo BYOK)

Esta aplicação segue estritamente o modelo BYOK (Bring Your Own Key):

Sem Backend: Não existe servidor intermediário. O site é 100% estático.

Conexão Direta: Quando você usa uma função de IA, seu navegador se conecta diretamente à API do Google Gemini.

Armazenamento Local: Sua API Key é salva exclusivamente no localStorage do seu navegador. Ela nunca sai da sua máquina para nossos servidores.

🛠️ Como Usar

Instalação Rápida (Deploy)

Como é um projeto de arquivo único, a hospedagem é trivial:

Opção A: GitHub Pages (Recomendado)

Faça um fork deste repositório.

Vá em Settings > Pages.

Selecione a branch main e salve.

Seu site estará no ar em https://seu-usuario.github.io/n8n-factory.

Opção B: Uso Local

Baixe o arquivo index.html.

Abra diretamente no Chrome, Firefox ou Edge.

Configuração da IA

Para habilitar as funcionalidades inteligentes (Toolbox, Doctor, Criador de Workflow):

Clique no ícone de engrenagem ⚙️ no menu superior.

Insira sua Google Gemini API Key (Gratuita no Google AI Studio).

Clique em Salvar.

💻 Guia de Desenvolvimento

Para manter este projeto atualizado, sugerimos o seguinte fluxo:

# 1. Verifique o status
git status

# 2. Adicione as mudanças
git add index.html README.md

# 3. Commit com mensagem descritiva
git commit -m "feat: atualização para v3.5.0 com novas ferramentas de IA"

# 4. Envie para o repositório
git push origin main


🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests com novos snippets para a Academia ou melhorias no gerador.

📄 Licença

Este projeto está sob a licença MIT. Sinta-se livre para usar, modificar e distribuir.
