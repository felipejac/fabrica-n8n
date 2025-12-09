-- Script para corrigir as políticas RLS (Row Level Security)
-- Execute este script no SQL Editor do Supabase

-- 1. Remover política antiga (se existir)
DROP POLICY IF EXISTS "Permitir insert público de leads" ON leads;

-- 2. Criar nova política correta para INSERT público
CREATE POLICY "Permitir insert público de leads"
ON leads
FOR INSERT
TO public
WITH CHECK (true);

-- 3. Verificar se a política foi criada corretamente
SELECT schemaname, tablename, policyname, roles, cmd, qual, with_check
FROM pg_policies
WHERE tablename = 'leads';

-- Resultado esperado:
-- policyname: "Permitir insert público de leads"
-- roles: {public}
-- cmd: INSERT
-- with_check: true
