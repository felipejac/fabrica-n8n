# 🚀 Guia Rápido de Setup - Sistema de Newsletter

## ⚡ Passos para Ativar o Sistema

### 1️⃣ Configurar Supabase (5 minutos)

1. Acesse [supabase.com](https://supabase.com) e faça login
2. Selecione seu projeto (ou crie um novo)
3. No menu lateral, clique em **SQL Editor**
4. Clique em **New Query**
5. Copie todo o conteúdo do arquivo `blog/supabase_setup.sql`
6. Cole no editor e clique em **Run**
7. ✅ Tabela criada!

**Copiar credenciais:**
- Vá em **Settings** → **API**
- Copie:
  - **Project URL** (será o `SUPABASE_URL`)
  - **anon public** key (será o `SUPABASE_ANON_KEY`)

---

### 2️⃣ Configurar Resend (3 minutos)

1. Acesse [resend.com](https://resend.com) e crie uma conta (gratuita)
2. Vá em **API Keys**
3. Clique em **Create API Key**
4. Copie a chave gerada (será o `RESEND_API_KEY`)

**Para email em produção:**
- Vá em **Domains** → **Add Domain**
- Adicione seu domínio (ex: `automationscookbook.com`)
- Configure os registros DNS conforme instruções
- Aguarde verificação (alguns minutos)

**Para testes:**
- Use o domínio de teste: `onboarding@resend.dev`
- Altere no código: `from: 'Automations Cookbook <onboarding@resend.dev>'`

---

### 3️⃣ Configurar Netlify (2 minutos)

1. Acesse [app.netlify.com](https://app.netlify.com)
2. Selecione seu site
3. Vá em **Site configuration** → **Environment variables**
4. Clique em **Add a variable**
5. Adicione as 3 variáveis:

```
Key: SUPABASE_URL
Value: https://seu-projeto.supabase.co

Key: SUPABASE_ANON_KEY
Value: sua-chave-anon-aqui

Key: RESEND_API_KEY
Value: re_sua-chave-resend-aqui
```

6. Clique em **Save**
7. Vá em **Deploys** → **Trigger deploy** → **Deploy site**

---

### 4️⃣ Testar o Sistema

1. Aguarde o deploy finalizar (1-2 minutos)
2. Acesse seu blog: `https://seu-site.netlify.app/blog`
3. Role até a seção "Receba Insights Exclusivos"
4. Insira seu email e clique em **Inscrever**
5. ✅ Você deve ver: "Inscrição realizada com sucesso! Verifique seu email. 🎉"
6. Verifique sua caixa de entrada (e spam) pelo email de boas-vindas

**Verificar no Supabase:**
1. Vá em **Table Editor** → **newsletter_subscribers**
2. Você deve ver seu email na lista!

---

## 🐛 Problemas Comuns

### "Erro ao processar inscrição"
- ✅ Verifique se as variáveis no Netlify estão corretas
- ✅ Confirme que fez o deploy após adicionar as variáveis
- ✅ Veja os logs: Netlify → Functions → newsletter-subscribe → Logs

### "Email não chegou"
- ✅ Verifique a pasta de spam
- ✅ Confirme que o domínio está verificado no Resend
- ✅ Use o email de teste temporariamente: `onboarding@resend.dev`

### "Formulário não responde"
- ✅ Abra o Console (F12) e veja se há erros JavaScript
- ✅ Confirme que o deploy foi concluído
- ✅ Limpe o cache do navegador (Ctrl+Shift+R)

---

## 📊 Monitorar Inscrições

### No Supabase:
```sql
-- Ver todos inscritos
SELECT * FROM newsletter_subscribers 
ORDER BY subscribed_at DESC;

-- Contar inscritos ativos
SELECT COUNT(*) FROM newsletter_subscribers 
WHERE status = 'active';

-- Últimos 10 inscritos
SELECT email, subscribed_at 
FROM newsletter_subscribers 
ORDER BY subscribed_at DESC 
LIMIT 10;
```

### No Netlify:
- **Functions** → **newsletter-subscribe** → **Function log**
- Veja todas as tentativas de inscrição em tempo real

---

## 🎨 Personalizar Email

Edite o template em `blog/email_template_welcome.html` ou a função `getWelcomeEmailHTML()` em `netlify/functions/newsletter-subscribe.js`.

Após editar, faça commit e push:
```bash
git add .
git commit -m "feat: personalizar email de boas-vindas"
git push
```

Netlify fará deploy automático!

---

## ✅ Checklist Final

- [ ] Supabase configurado (tabela criada)
- [ ] Resend configurado (API key obtida)
- [ ] Netlify com 3 variáveis de ambiente
- [ ] Deploy realizado após configurar variáveis
- [ ] Teste de inscrição realizado com sucesso
- [ ] Email de boas-vindas recebido
- [ ] Verificado registro no Supabase

---

## 🆘 Precisa de Ajuda?

1. Verifique os logs do Netlify Functions
2. Verifique o Console do navegador (F12)
3. Consulte `NEWSLETTER_README.md` para troubleshooting detalhado
4. As credenciais estão corretas nas variáveis de ambiente?

---

**Sistema pronto!** 🎉 

Agora toda vez que alguém se inscrever:
1. ✅ Email salvo no Supabase
2. ✅ Email de boas-vindas enviado automaticamente
3. ✅ Usuário vê mensagem de sucesso

**Equipe Automations Cookbook** 🚀
