-- Criar tabela de subscribers da newsletter
CREATE TABLE IF NOT EXISTS newsletter_subscribers (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    subscribed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    status VARCHAR(50) DEFAULT 'active',
    source VARCHAR(100) DEFAULT 'blog',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Criar índice para busca rápida por email
CREATE INDEX IF NOT EXISTS idx_newsletter_email ON newsletter_subscribers(email);

-- Criar índice para busca por status
CREATE INDEX IF NOT EXISTS idx_newsletter_status ON newsletter_subscribers(status);

-- Adicionar RLS (Row Level Security)
ALTER TABLE newsletter_subscribers ENABLE ROW LEVEL SECURITY;

-- Política para permitir INSERT público (para formulário do site)
CREATE POLICY "Allow public insert" ON newsletter_subscribers
    FOR INSERT
    WITH CHECK (true);

-- Política para permitir SELECT apenas para usuários autenticados
CREATE POLICY "Allow authenticated read" ON newsletter_subscribers
    FOR SELECT
    USING (auth.role() = 'authenticated');

-- Comentários para documentação
COMMENT ON TABLE newsletter_subscribers IS 'Armazena emails dos inscritos na newsletter do blog';
COMMENT ON COLUMN newsletter_subscribers.email IS 'Email do inscrito (único)';
COMMENT ON COLUMN newsletter_subscribers.status IS 'Status: active, unsubscribed, bounced';
COMMENT ON COLUMN newsletter_subscribers.source IS 'Origem da inscrição: blog, landing_page, etc';
