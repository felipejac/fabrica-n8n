# Sistema de Newsletter - Automations Cookbook

Sistema completo de inscrição em newsletter com armazenamento no Supabase e envio automático de email de boas-vindas.

## 📋 Funcionalidades

- ✅ Validação de email no frontend e backend
- ✅ Armazenamento seguro no Supabase
- ✅ Verificação de duplicatas
- ✅ Envio automático de email de boas-vindas
- ✅ Mensagens de sucesso/erro para o usuário
- ✅ Design responsivo e acessível

## 🚀 Setup

### 1. Configurar Supabase

1. Acesse seu projeto no [Supabase](https://supabase.com)
2. Vá em **SQL Editor**
3. Execute o script `supabase_setup.sql`
4. Anote suas credenciais:
   - `SUPABASE_URL`: URL do projeto
   - `SUPABASE_ANON_KEY`: Chave pública (anon key)

### 2. Configurar Resend (Email)

1. Crie uma conta no [Resend](https://resend.com)
2. Gere uma API Key
3. Adicione e verifique seu domínio (ou use o domínio de teste)
4. Anote sua API Key: `RESEND_API_KEY`

### 3. Configurar Netlify Environment Variables

No dashboard do Netlify, adicione as seguintes variáveis de ambiente:

```
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_ANON_KEY=sua-chave-anon
RESEND_API_KEY=re_sua-chave-resend
```

**Caminho**: Site Settings → Environment Variables → Add a variable

### 4. Instalar Dependências

```bash
cd netlify
npm install
```

### 5. Deploy

O deploy acontece automaticamente via Netlify quando você faz push para o repositório.

Para testar localmente:

```bash
# Instalar Netlify CLI
npm install -g netlify-cli

# Executar localmente
netlify dev
```

## 📧 Email de Boas-Vindas

O email de boas-vindas inclui:

- 🎉 Mensagem de boas-vindas personalizada
- 📝 Lista de benefícios da newsletter
- 🔗 Link para o blog
- 👥 Assinatura da equipe Automations Cookbook

Template disponível em: `email_template_welcome.html`

## 🗄️ Estrutura do Banco de Dados

### Tabela: `newsletter_subscribers`

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | UUID | Identificador único |
| email | VARCHAR(255) | Email do inscrito (único) |
| subscribed_at | TIMESTAMP | Data de inscrição |
| status | VARCHAR(50) | Status: active, unsubscribed, bounced |
| source | VARCHAR(100) | Origem: blog, landing_page, etc |
| created_at | TIMESTAMP | Data de criação do registro |
| updated_at | TIMESTAMP | Data de atualização |

## 🔒 Segurança

- **Row Level Security (RLS)** habilitado
- Política de INSERT pública (apenas para o formulário)
- Política de SELECT apenas para usuários autenticados
- Validação de email no backend
- Prevenção de duplicatas
- CORS configurado

## 📊 Monitoramento

### Verificar inscritos no Supabase

```sql
SELECT 
    email, 
    subscribed_at, 
    status, 
    source 
FROM newsletter_subscribers 
WHERE status = 'active'
ORDER BY subscribed_at DESC;
```

### Estatísticas

```sql
SELECT 
    status,
    COUNT(*) as total
FROM newsletter_subscribers
GROUP BY status;
```

## 🎨 Personalização

### Alterar Template de Email

Edite o arquivo `email_template_welcome.html` ou a função `getWelcomeEmailHTML()` em `newsletter-subscribe.js`.

### Alterar Mensagens

As mensagens de sucesso/erro estão no handler JavaScript no `index.html`.

### Adicionar Campos

Para coletar mais informações (nome, empresa, etc):

1. Adicione colunas na tabela Supabase
2. Atualize o formulário HTML
3. Modifique a função Netlify para processar os novos campos

## 🐛 Troubleshooting

### Email não está sendo enviado

1. Verifique se `RESEND_API_KEY` está configurada corretamente
2. Confirme que seu domínio está verificado no Resend
3. Verifique os logs da função no Netlify: Functions → newsletter-subscribe → Logs

### Erro ao salvar no Supabase

1. Verifique as credenciais `SUPABASE_URL` e `SUPABASE_ANON_KEY`
2. Confirme que a tabela foi criada corretamente
3. Verifique as políticas RLS no Supabase

### Formulário não responde

1. Abra o console do navegador (F12)
2. Verifique se há erros JavaScript
3. Confirme que o endpoint `/.netlify/functions/newsletter-subscribe` está acessível

## 📚 Recursos

- [Documentação Supabase](https://supabase.com/docs)
- [Documentação Resend](https://resend.com/docs)
- [Netlify Functions](https://docs.netlify.com/functions/overview/)

## 🤝 Suporte

Para problemas ou sugestões, abra uma issue no repositório.

---

**Equipe Automations Cookbook** 🚀
