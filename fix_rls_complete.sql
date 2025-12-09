-- SOLUÇÃO COMPLETA: Corrigir RLS para permitir INSERT público
-- Execute TODOS os comandos abaixo no SQL Editor do Supabase

-- PASSO 1: Remover todas as políticas existentes
DROP POLICY IF EXISTS "Permitir insert público de leads" ON leads;
DROP POLICY IF EXISTS "Permitir leitura apenas autenticados" ON leads;

-- PASSO 2: Desabilitar RLS temporariamente para testar
ALTER TABLE leads DISABLE ROW LEVEL SECURITY;

-- TESTE: Tente inserir um lead agora (deve funcionar)
-- Se funcionar, vá para o PASSO 3

-- PASSO 3: Reabilitar RLS com políticas corretas
ALTER TABLE leads ENABLE ROW LEVEL SECURITY;

-- PASSO 4: Criar política para INSERT público (anônimo)
CREATE POLICY "allow_public_insert"
ON leads
FOR INSERT
WITH CHECK (true);

-- PASSO 5: Criar política para SELECT apenas autenticados
CREATE POLICY "allow_authenticated_select"
ON leads
FOR SELECT
USING (auth.role() = 'authenticated');

-- VERIFICAÇÃO: Listar políticas ativas
SELECT 
    schemaname,
    tablename, 
    policyname,
    permissive,
    roles,
    cmd,
    qual,
    with_check
FROM pg_policies 
WHERE tablename = 'leads';

-- Resultado esperado:
-- policyname: allow_public_insert
-- cmd: INSERT
-- with_check: true
--
-- policyname: allow_authenticated_select  
-- cmd: SELECT
-- qual: (auth.role() = 'authenticated')
