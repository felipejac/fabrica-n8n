-- ============================================================================
-- SCRIPT DEFINITIVO: Tabela leads SEM RLS (mais simples e funcional)
-- Execute TODO este script no SQL Editor do Supabase
-- ============================================================================

-- 1. REMOVER tabela antiga completamente
DROP TABLE IF EXISTS leads CASCADE;

-- 2. CRIAR tabela de leads (SEM RLS)
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

-- 3. CRIAR índices para performance
CREATE INDEX idx_leads_email ON leads(email);
CREATE INDEX idx_leads_created_at ON leads(created_at DESC);
CREATE INDEX idx_leads_source ON leads(source);

-- 4. NÃO habilitar RLS (deixar desabilitado para funcionamento público)
-- RLS está DESABILITADO por padrão em novas tabelas

-- 5. GARANTIR que RLS está desabilitado
ALTER TABLE leads DISABLE ROW LEVEL SECURITY;

-- 6. GRANT de permissões explícitas para anon e authenticated
GRANT INSERT ON leads TO anon;
GRANT INSERT ON leads TO authenticated;
GRANT SELECT ON leads TO authenticated;
GRANT USAGE, SELECT ON SEQUENCE leads_id_seq TO anon;
GRANT USAGE, SELECT ON SEQUENCE leads_id_seq TO authenticated;

-- 7. Documentação
COMMENT ON TABLE leads IS 'Tabela de leads do formulário de contato - RLS desabilitado para acesso público';
COMMENT ON COLUMN leads.id IS 'ID único auto-incremento';
COMMENT ON COLUMN leads.full_name IS 'Nome completo do lead';
COMMENT ON COLUMN leads.phone IS 'Telefone internacional (E.164)';
COMMENT ON COLUMN leads.email IS 'Email do lead';
COMMENT ON COLUMN leads.message IS 'Mensagem (max 140 chars)';
COMMENT ON COLUMN leads.optin IS 'Aceite LGPD';
COMMENT ON COLUMN leads.source IS 'Origem do lead';
COMMENT ON COLUMN leads.user_agent IS 'Navegador/dispositivo';
COMMENT ON COLUMN leads.page_url IS 'URL origem';
COMMENT ON COLUMN leads.created_at IS 'Data/hora criação';

-- ============================================================================
-- VERIFICAÇÕES
-- ============================================================================

-- Ver estrutura da tabela
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns 
WHERE table_name = 'leads' 
ORDER BY ordinal_position;

-- Verificar que RLS está DESABILITADO
SELECT schemaname, tablename, rowsecurity
FROM pg_tables 
WHERE tablename = 'leads';
-- Resultado esperado: rowsecurity = false

-- Verificar permissões
SELECT grantee, privilege_type
FROM information_schema.table_privileges
WHERE table_name = 'leads';

-- ============================================================================
-- TESTE MANUAL (opcional)
-- ============================================================================

-- Inserir um registro de teste
INSERT INTO leads (full_name, phone, email, message, optin, source, user_agent, page_url)
VALUES (
    'Teste Manual SQL',
    '+5511999999999',
    'teste@automationscookbook.com',
    'Lead de teste inserido manualmente via SQL Editor',
    true,
    'SQL Editor - Teste Manual',
    'PostgreSQL/Manual',
    'https://supabase.com/dashboard'
);

-- Ver todos os leads
SELECT id, full_name, email, phone, message, created_at
FROM leads
ORDER BY created_at DESC
LIMIT 5;

-- ============================================================================
-- RESULTADO ESPERADO:
-- ============================================================================
-- ✅ Tabela criada com 10 colunas
-- ✅ RLS desabilitado (rowsecurity = false)
-- ✅ Permissões INSERT para anon e authenticated
-- ✅ Permissões SELECT para authenticated
-- ✅ Sequence permissions para anon e authenticated
-- ✅ Teste manual inserido com sucesso
-- ============================================================================
