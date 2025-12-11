/**
 * Netlify Function para processar inscrição na newsletter
 * 
 * Funcionalidades:
 * 1. Valida email
 * 2. Salva no Supabase
 * 3. Envia email de boas-vindas via Resend
 */

const { createClient } = require('@supabase/supabase-js');

// Configurações - adicionar no Netlify Environment Variables
const SUPABASE_URL = process.env.SUPABASE_URL;
const SUPABASE_ANON_KEY = process.env.SUPABASE_ANON_KEY;
const RESEND_API_KEY = process.env.RESEND_API_KEY;

// Validação de email
function isValidEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

// Template de email de boas-vindas
function getWelcomeEmailHTML(email) {
    return `<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background-color: #f3f4f6; }
        .container { max-width: 600px; margin: 40px auto; background: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .header { background: linear-gradient(135deg, #2563eb 0%, #9333ea 100%); padding: 40px 30px; text-align: center; color: white; }
        .header h1 { margin: 0; font-size: 28px; font-weight: 700; }
        .emoji { font-size: 48px; margin: 20px 0; }
        .content { padding: 40px 30px; color: #374151; line-height: 1.6; }
        .benefits { background: #f9fafb; border-left: 4px solid #2563eb; padding: 20px; margin: 25px 0; border-radius: 4px; }
        .benefits li { margin: 10px 0; }
        .cta-button { display: inline-block; background: linear-gradient(135deg, #2563eb 0%, #9333ea 100%); color: white; text-decoration: none; padding: 14px 32px; border-radius: 8px; font-weight: 600; margin: 20px 0; }
        .footer { background: #f9fafb; padding: 30px; text-align: center; color: #6b7280; font-size: 14px; border-top: 1px solid #e5e7eb; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="emoji">🎉</div>
            <h1>Bem-vindo à Newsletter!</h1>
            <p>Automations Cookbook</p>
        </div>
        <div class="content">
            <h2>Olá! 👋</h2>
            <p>Seja muito bem-vindo à comunidade <strong>Automations Cookbook</strong>! Estamos muito felizes em ter você conosco.</p>
            <p>A partir de agora, você receberá diretamente no seu email:</p>
            <div class="benefits">
                <ul>
                    <li>📝 <strong>Novos artigos</strong> assim que forem publicados</li>
                    <li>🔍 <strong>Análises exclusivas</strong> sobre automação e IA</li>
                    <li>💡 <strong>Dicas práticas</strong> de n8n, Zapier e Make</li>
                    <li>📊 <strong>Tendências de mercado</strong> e insights estratégicos</li>
                    <li>🚀 <strong>Tutoriais avançados</strong> de automação</li>
                    <li>🎁 <strong>Conteúdos exclusivos</strong> para assinantes</li>
                </ul>
            </div>
            <p style="text-align: center;">
                <a href="https://fabrica-n8n.vercel.app/blog" class="cta-button">Explorar o Blog 📚</a>
            </p>
            <p>Até breve! 🚀<br><strong>Equipe Automations Cookbook</strong></p>
        </div>
        <div class="footer">
            <p><strong>Automations Cookbook</strong><br>Seu guia para automação e IA</p>
            <p style="margin-top: 15px; color: #9ca3af; font-size: 12px;">© 2025 Automations Cookbook</p>
        </div>
    </div>
</body>
</html>`;
}

exports.handler = async (event, context) => {
    // CORS headers
    const headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Content-Type': 'application/json'
    };

    // Handle preflight
    if (event.httpMethod === 'OPTIONS') {
        return { statusCode: 200, headers, body: '' };
    }

    // Only accept POST
    if (event.httpMethod !== 'POST') {
        return {
            statusCode: 405,
            headers,
            body: JSON.stringify({ error: 'Method not allowed' })
        };
    }

    try {
        // Parse body
        const { email } = JSON.parse(event.body);

        // Validate email
        if (!email || !isValidEmail(email)) {
            return {
                statusCode: 400,
                headers,
                body: JSON.stringify({ error: 'Email inválido' })
            };
        }

        // Initialize Supabase
        const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

        // Check if email already exists
        const { data: existing, error: checkError } = await supabase
            .from('newsletter_subscribers')
            .select('email, status')
            .eq('email', email.toLowerCase())
            .single();

        if (existing) {
            if (existing.status === 'active') {
                return {
                    statusCode: 200,
                    headers,
                    body: JSON.stringify({ 
                        success: true, 
                        message: 'Você já está inscrito na nossa newsletter! 🎉',
                        alreadySubscribed: true
                    })
                };
            }
        }

        // Save to Supabase
        const { data, error: insertError } = await supabase
            .from('newsletter_subscribers')
            .insert([
                { 
                    email: email.toLowerCase(),
                    status: 'active',
                    source: 'blog'
                }
            ])
            .select();

        if (insertError) {
            console.error('Supabase error:', insertError);
            throw new Error('Erro ao salvar inscrição');
        }

        // Send welcome email via Resend
        try {
            const resendResponse = await fetch('https://api.resend.com/emails', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${RESEND_API_KEY}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    from: 'Automations Cookbook <newsletter@automationscookbook.com>',
                    to: [email],
                    subject: '🎉 Bem-vindo à Newsletter do Automations Cookbook!',
                    html: getWelcomeEmailHTML(email)
                })
            });

            if (!resendResponse.ok) {
                console.error('Resend error:', await resendResponse.text());
                // Não falhar se email não enviar
            }
        } catch (emailError) {
            console.error('Email sending error:', emailError);
            // Continuar mesmo se email falhar
        }

        return {
            statusCode: 200,
            headers,
            body: JSON.stringify({ 
                success: true, 
                message: 'Inscrição realizada com sucesso! Verifique seu email. 🎉'
            })
        };

    } catch (error) {
        console.error('Error:', error);
        return {
            statusCode: 500,
            headers,
            body: JSON.stringify({ 
                error: 'Erro ao processar inscrição. Tente novamente.',
                details: error.message 
            })
        };
    }
};
