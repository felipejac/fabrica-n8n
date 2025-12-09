-- ============================================================================
-- SCRIPT COMPLETO: Criar tabela de leads do ZERO com políticas RLS corretas
-- Execute TODO este script no SQL Editor do Supabase
-- ============================================================================

-- 1. REMOVER tabela antiga (se existir)
DROP TABLE IF EXISTS leads CASCADE;

-- 2. CRIAR tabela de leads
CREATE TABLE leads (
    id BIGSERIAL PRIMARY KEY,
    full_name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL,
    message TEXT NOT NULL,
    optin BOOLEAN DEFAULT true NOT NULL,
    source TEXT DEFAULT 'Automations Cookbook - Homepage',
    user_agent TEXT,
    page_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);

-- 3. CRIAR índices para melhorar performance
CREATE INDEX idx_leads_email ON leads(email);
CREATE INDEX idx_leads_created_at ON leads(created_at DESC);
CREATE INDEX idx_leads_source ON leads(source);

-- 4. HABILITAR RLS (Row Level Security)
ALTER TABLE leads ENABLE ROW LEVEL SECURITY;

-- 5. CRIAR política para permitir INSERT público (qualquer visitante)
CREATE POLICY "allow_anonymous_insert"
ON leads
FOR INSERT
TO anon, authenticated
WITH CHECK (true);

-- 6. CRIAR política para permitir SELECT apenas para usuários autenticados
CREATE POLICY "allow_authenticated_select"
ON leads
FOR SELECT
TO authenticated
USING (true);

-- 7. ADICIONAR comentários na tabela (documentação)
COMMENT ON TABLE leads IS 'Tabela para armazenar leads capturados do formulário de contato';
COMMENT ON COLUMN leads.id IS 'ID único do lead';
COMMENT ON COLUMN leads.full_name IS 'Nome completo do lead';
COMMENT ON COLUMN leads.phone IS 'Telefone no formato internacional (E.164)';
COMMENT ON COLUMN leads.email IS 'E-mail do lead';
COMMENT ON COLUMN leads.message IS 'Mensagem enviada pelo lead (máximo 140 caracteres)';
COMMENT ON COLUMN leads.optin IS 'Confirmação LGPD para recebimento de comunicações';
COMMENT ON COLUMN leads.source IS 'Origem/fonte do lead';
COMMENT ON COLUMN leads.user_agent IS 'User agent do navegador';
COMMENT ON COLUMN leads.page_url IS 'URL da página onde o formulário foi enviado';
COMMENT ON COLUMN leads.created_at IS 'Data e hora de criação do registro';

-- ============================================================================
-- VERIFICAÇÃO: Conferir se tudo foi criado corretamente
-- ============================================================================

-- Verificar estrutura da tabela
SELECT 
    column_name, 
    data_type, 
    is_nullable,
    column_default
FROM information_schema.columns 
WHERE table_name = 'leads' 
ORDER BY ordinal_position;

-- Verificar políticas RLS
SELECT 
    schemaname,
    tablename, 
    policyname,
    permissive,
    roles,
    cmd,
    with_check
FROM pg_policies 
WHERE tablename = 'leads';

-- Verificar se RLS está habilitado
SELECT 
    schemaname,
    tablename,
    rowsecurity
FROM pg_tables 
WHERE tablename = 'leads';

-- ============================================================================
-- RESULTADO ESPERADO:
-- ============================================================================
-- 
-- Políticas criadas:
-- 1. allow_anonymous_insert - INSERT permitido para anon e authenticated
-- 2. allow_authenticated_select - SELECT apenas para authenticated
--
-- Row Security: true (RLS habilitado)
--
-- ============================================================================
