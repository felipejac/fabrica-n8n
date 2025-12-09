-- Criar tabela de leads para o formulário de contato
CREATE TABLE IF NOT EXISTS leads (
    id BIGSERIAL PRIMARY KEY,
    full_name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL,
    message TEXT NOT NULL,
    optin BOOLEAN DEFAULT true,
    source TEXT DEFAULT 'Automations Cookbook - Homepage',
    user_agent TEXT,
    page_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Criar índices para melhorar performance de consultas
CREATE INDEX IF NOT EXISTS idx_leads_email ON leads(email);
CREATE INDEX IF NOT EXISTS idx_leads_created_at ON leads(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_leads_source ON leads(source);

-- Habilitar RLS (Row Level Security)
ALTER TABLE leads ENABLE ROW LEVEL SECURITY;

-- Política para permitir INSERT público (qualquer pessoa pode inserir)
CREATE POLICY "Permitir insert público de leads"
ON leads
FOR INSERT
TO public
WITH CHECK (true);

-- Política para permitir leitura apenas para usuários autenticados
CREATE POLICY "Permitir leitura apenas autenticados"
ON leads
FOR SELECT
TO authenticated
USING (true);

-- Comentários na tabela
COMMENT ON TABLE leads IS 'Tabela para armazenar leads capturados do formulário de contato do site';
COMMENT ON COLUMN leads.full_name IS 'Nome completo do lead';
COMMENT ON COLUMN leads.phone IS 'Telefone no formato internacional (E.164)';
COMMENT ON COLUMN leads.email IS 'E-mail do lead';
COMMENT ON COLUMN leads.message IS 'Mensagem enviada pelo lead (máximo 140 caracteres)';
COMMENT ON COLUMN leads.optin IS 'Confirmação LGPD para recebimento de comunicações';
COMMENT ON COLUMN leads.source IS 'Origem/fonte do lead';
COMMENT ON COLUMN leads.user_agent IS 'User agent do navegador';
COMMENT ON COLUMN leads.page_url IS 'URL da página onde o formulário foi enviado';
