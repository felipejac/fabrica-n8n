#!/bin/bash

# 🧪 Script de Verificação Pós-Deploy
# Verifica se o deploy foi bem-sucedido e testa funcionalidades

echo "🧪 Verificando Deploy em Produção..."
echo ""

# Cores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# URLs
BASE_URL="https://felipejac.github.io/fabrica-n8n"
PT_URL="$BASE_URL/index.html"
EN_URL="$BASE_URL/translated/en/index.html"
INT_URL="$BASE_URL/integracoes/"

# Função de teste
test_url() {
    local url=$1
    local name=$2
    
    echo -n "   Testando $name... "
    
    status=$(curl -s -o /dev/null -w "%{http_code}" "$url" --max-time 10)
    
    if [ "$status" = "200" ]; then
        echo -e "${GREEN}✅ OK${NC} (HTTP $status)"
        return 0
    else
        echo -e "${RED}❌ FALHOU${NC} (HTTP $status)"
        return 1
    fi
}

# Contador
passed=0
failed=0

echo "🌐 Testando URLs principais:"
echo ""

# Teste 1: Página principal
if test_url "$PT_URL" "Português (index.html)"; then
    ((passed++))
else
    ((failed++))
fi

# Teste 2: Versão inglês
if test_url "$EN_URL" "Inglês (translated/en/)"; then
    ((passed++))
else
    ((failed++))
fi

# Teste 3: Integrações
if test_url "$INT_URL" "Integrações"; then
    ((passed++))
else
    ((failed++))
fi

# Teste 4: Script i18n
I18N_JS="$BASE_URL/assets/js/i18n-detect.js"
if test_url "$I18N_JS" "Script i18n-detect.js"; then
    ((passed++))
else
    ((failed++))
fi

# Teste 5: Arquivo traduzido específico
SAMPLE_EN="$BASE_URL/translated/en/integracoes/shopify-para-slack-novas-vendas-n8n.html"
if test_url "$SAMPLE_EN" "Integração traduzida (sample)"; then
    ((passed++))
else
    ((failed++))
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 RESULTADO DOS TESTES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "   ${GREEN}✅ Passou:${NC}  $passed"
echo -e "   ${RED}❌ Falhou:${NC}  $failed"
echo "   📈 Total:   $((passed + failed))"
echo ""

# Resultado final
if [ $failed -eq 0 ]; then
    echo -e "${GREEN}🎉 TODOS OS TESTES PASSARAM!${NC}"
    echo ""
    echo "✅ Site está no ar e funcionando corretamente!"
    echo ""
    echo "🌍 Acesse:"
    echo "   🇧🇷 https://felipejac.github.io/fabrica-n8n/"
    echo "   🇺🇸 https://felipejac.github.io/fabrica-n8n/translated/en/"
    echo ""
    exit 0
else
    echo -e "${YELLOW}⚠️  $failed TESTE(S) FALHARAM${NC}"
    echo ""
    echo "Possíveis causas:"
    echo "   1. Deploy ainda em andamento (aguarde 2-3 min)"
    echo "   2. GitHub Pages não está ativado"
    echo "   3. Arquivos não foram commitados corretamente"
    echo ""
    echo "🔍 Verificar:"
    echo "   https://github.com/felipejac/fabrica-n8n/actions"
    echo ""
    exit 1
fi
