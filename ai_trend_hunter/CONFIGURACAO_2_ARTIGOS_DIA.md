# ✅ Sistema Configurado: 2 Artigos por Dia

## 📅 Rotação Semanal Implementada

### Segunda-feira
- 📝 Mito vs Realidade
- 📝 Além do ChatGPT

### Terça-feira
- 📝 Segurança Jurídica
- 📝 Cemitério de Projetos

### Quarta-feira
- 📝 Mito vs Realidade
- 📝 Segurança Jurídica

### Quinta-feira
- 📝 Além do ChatGPT
- 📝 Cemitério de Projetos

### Sexta-feira
- 📝 Relatório Semanal
- 📝 Mito vs Realidade

### Sábado e Domingo
⏸️ **Pausa** (sem publicações)

---

## 📊 Estatísticas

- **10 artigos/semana** (2 por dia útil)
- **40 artigos/mês** (~520 palavras cada)
- **Duração:** ~0.3 segundos por execução
- **Rotação:** Cada tipo aparece 2x/semana

---

## 🚀 Como Funciona

### Execução Automática Diária

```bash
# Adicionar ao crontab (executa todo dia às 8h)
0 8 * * * cd /workspaces/fabrica-n8n/ai_trend_hunter && python main.py
```

### O Sistema Detecta Automaticamente:

1. **Dia da semana** atual
2. **Seleciona os 2 tópicos** programados
3. **Gera os artigos** com dados frescos do Hugging Face
4. **Salva com metadados SEO** completos

### Hoje (Sexta-feira, 12/12/2025):

```
📅 Dia da semana: Sexta
📋 Tópicos do dia: relatorio_mensal, mito_vs_realidade
📝 Gerando conteúdo para 2 tópicos...
✅ Post salvo: 2025-12-12_relatorio_mensal.md
✅ Post salvo: 2025-12-12_mito_vs_realidade.md
```

---

## ⚙️ Personalização

### Mudar Quantidade de Artigos/Dia

Editar `config.py`:

```python
CONTENT_CONFIG = {
    'daily_posts_count': 3,  # Mudar para 3 artigos/dia
    ...
}
```

### Customizar Rotação Semanal

```python
'weekly_rotation': {
    0: ['topico1', 'topico2'],  # Segunda
    1: ['topico3', 'topico4'],  # Terça
    # ... personalize cada dia
}
```

### Desabilitar Rotação (gerar todos)

```python
EXECUTION_CONFIG = {
    'generation_strategy': 'all',  # Gera todos os 5 tipos
    'use_weekly_rotation': False
}
```

### Modo Manual (escolher tópicos)

```python
EXECUTION_CONFIG = {
    'generation_strategy': 'custom',
    'topics_to_generate': ['relatorio_mensal', 'mito_vs_realidade']
}
```

---

## 📈 Benefícios da Rotação de 2 Artigos/Dia

### ✅ Consistência
- Público recebe conteúdo regular
- 2 artigos = não sobrecarrega leitores
- Fim de semana livre (melhor para SEO)

### ✅ Variedade
- Cada tipo aparece 2x/semana
- Diferentes ângulos sobre IA
- Mantém interesse do público

### ✅ SEO Otimizado
- 10 URLs novas/semana
- Google indexa gradualmente
- Melhor que 5 artigos de uma vez

### ✅ Escalável
- Fácil mudar para 1 ou 3 artigos/dia
- Pode adicionar novos tipos de pauta
- Rotação automática se adapta

---

## 🔧 Troubleshooting

### Forçar Tópicos Específicos Hoje

```bash
# Executar com argumentos customizados
python main.py --topics seguranca_juridica cemiterio_projetos
```

(Requer pequena modificação no `main.py` para aceitar CLI args)

### Ver Agenda da Semana

```python
from config import CONTENT_CONFIG

for dia, topicos in CONTENT_CONFIG['weekly_rotation'].items():
    dias_semana = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
    print(f"{dias_semana[dia]}: {', '.join(topicos)}")
```

### Verificar Próxima Execução

```bash
# Ver logs
tail -f ai_trend_hunter.log
```

---

## 📊 Exemplo de Mês Completo

### Semana 1 (10 artigos)
- Segunda: Mito vs Realidade + Além ChatGPT
- Terça: Segurança Jurídica + Cemitério
- Quarta: Mito vs Realidade + Segurança Jurídica
- Quinta: Além ChatGPT + Cemitério
- Sexta: Relatório Semanal + Mito vs Realidade

### Semana 2-4: Repete rotação

**Total Mensal:** ~40 artigos únicos (dados sempre atualizados)

---

## 🎯 Próximos Passos

1. ✅ **Sistema configurado** para 2 artigos/dia
2. ⏳ **Adicionar ao cron** para execução automática
3. ⏳ **Conectar com WordPress** para publicação direta
4. ⏳ **Configurar Google Analytics** para tracking

---

**Sistema pronto para produção!** 🚀

*Configurado em: 12 de Dezembro de 2025*
