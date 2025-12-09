-- ============================================================================
-- SOLUÇÃO SIMPLES: Desabilitar RLS (mais fácil para começar)
-- ============================================================================

-- Se a tabela já existe, apenas desabilite o RLS:
ALTER TABLE leads DISABLE ROW LEVEL SECURITY;

-- ============================================================================
-- OU se preferir manter RLS, use esta política alternativa:
-- ============================================================================

-- Remover políticas antigas
DROP POLICY IF EXISTS "allow_anonymous_insert" ON leads;
DROP POLICY IF EXISTS "allow_authenticated_select" ON leads;
DROP POLICY IF EXISTS "Permitir insert público de leads" ON leads;
DROP POLICY IF EXISTS "Permitir leitura apenas autenticados" ON leads;

-- Criar política que permite INSERT sem RLS check
CREATE POLICY "enable_insert_for_all"
ON leads
FOR INSERT
WITH CHECK (true);

-- Criar política para SELECT
CREATE POLICY "enable_read_for_authenticated"  
ON leads
FOR SELECT
TO authenticated
USING (true);

-- ============================================================================
-- VERIFICAR
-- ============================================================================

SELECT tablename, policyname, cmd, roles 
FROM pg_policies 
WHERE tablename = 'leads';
