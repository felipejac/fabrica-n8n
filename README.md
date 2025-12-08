🏭 N8N Factory

Gerador de Conteúdo e Biblioteca de Templates para n8n com Inteligência Artificial.

A N8N Factory é uma ferramenta web estática (sem backend) projetada para acelerar a criação de documentação e fluxos de trabalho para o n8n. Ela combina um gerador de Markdown em massa com uma biblioteca vasta de templates prontos.

✨ Funcionalidades

1. 🏭 Fábrica de Conteúdo (Gerador)

Transforme planilhas CSV em centenas de arquivos Markdown formatados em segundos. Ideal para blogs programáticos e documentação.

Entrada: CSV (copiar e colar).

Template: Markdown com variáveis {{ mustache }}.

Saída: Arquivo ZIP com todos os .md gerados.

Novo: Enriquecimento de dados com IA (preenche descrições faltantes).

2. 📚 Biblioteca de Templates

Acesso a mais de 3.200 templates de automação.

Filtro por palavras-chave em tempo real.

Download imediato do arquivo JSON para importar no n8n.

IA Creator: Descreva o que você quer (ex: "Monitorar Bitcoin e avisar no Slack") e a IA gera o JSON do workflow na hora.

🚀 Como Usar (Segurança BYOK)

Esta aplicação segue o modelo BYOK (Bring Your Own Key) para máxima segurança e privacidade.

Clone este repositório ou baixe o arquivo index.html.

Abra o index.html em qualquer navegador moderno.

Para usar os recursos de IA (Enriquecer CSV ou Criar Workflow):

Clique no ícone de engrenagem ⚙️ no menu.

Insira sua Google Gemini API Key.

A chave é salva apenas no seu navegador (LocalStorage). Ela nunca é enviada para servidores de terceiros, apenas diretamente para a API do Google.

🛠️ Instalação / Deploy

Como é um projeto estático (Single File App), a hospedagem é trivial.

Opção A: GitHub Pages (Recomendado)

Faça um fork deste repositório.

Vá em Settings > Pages.

Selecione a branch main e salve.

Seu site estará no ar em https://seu-usuario.github.io/n8n-factory.

Opção B: Netlify Drop

Acesse app.netlify.com/drop.

Arraste a pasta contendo o index.html.

Pronto!

🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests com novos templates manuais ou melhorias no gerador.

📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
