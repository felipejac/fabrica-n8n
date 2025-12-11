# 🎯 Sistema de Filtros Automáticos do Blog

## Visão Geral

Script Python que analisa automaticamente todos os posts do blog, identifica categorias e gera botões de filtro dinâmicos.

## 📊 Categorias Atuais (68 posts)

O sistema agrupa **45 categorias únicas** em **10 grupos principais**:

1. **IA** (7 posts) - IA, Agentes, RAG, Local AI, Voice AI
2. **Comparação** (6 posts) - Comparação
3. **Segurança** (6 posts) - Segurança, Compliance
4. **DevOps** (5 posts) - DevOps, Cloud
5. **Tutorial** (5 posts) - Tutorial, Setup
6. **Desenvolvimento** (5 posts) - Desenvolvimento, Plugins, Frontend, Backend, Frameworks
7. **Análise** (5 posts) - Economia, Análise de Mercado, Tendências, Negócios
8. **Ferramentas** (4 posts) - Scraping, Templates, Chatbots, CRM
9. **Automação** (4 posts) - Automação, Integração
10. **Marketing** (4 posts) - Marketing, Growth, Marketing Digital, Conteúdo

## 🚀 Como Usar

### Atualizar filtros após adicionar novos posts

```bash
cd /workspaces/fabrica-n8n/blog
python3 update_filters.py
```

O script irá:
1. ✅ Analisar todos os `<article>` no `index.html`
2. ✅ Extrair badges de categoria de cada post
3. ✅ Contar frequência e agrupar categorias similares
4. ✅ Gerar HTML dos botões de filtro (top 8 categorias)
5. ✅ Gerar JavaScript para filtrar posts dinamicamente
6. ✅ Atualizar `index.html` automaticamente

### Personalizar agrupamento de categorias

Edite o dicionário `category_map` em `update_filters.py`:

```python
category_map = {
    'IA': ['IA', 'Agentes', 'RAG', 'Local AI', 'Voice AI'],
    'Comparação': ['Comparação'],
    'Segurança': ['Segurança', 'Compliance'],
    # Adicione novos grupos aqui
    'Nova Categoria': ['Keyword1', 'Keyword2', 'Keyword3']
}
```

### Alterar mínimo de posts por categoria

Por padrão, apenas categorias com 2+ posts aparecem. Para mudar:

```python
buttons_html, category_map = generate_filter_buttons(category_count, min_posts=3)  # Mínimo 3 posts
```

## 🔧 Funcionamento Técnico

### Estrutura HTML dos Filtros

```html
<div class="flex gap-2" id="filter-buttons">
    <button class="filter-btn ... " data-filter="all">Todos</button>
    <button class="filter-btn ... " data-filter="ia">IA</button>
    <button class="filter-btn ... " data-filter="comparação">Comparação</button>
    <!-- ... -->
</div>
```

### JavaScript de Filtro

- Escuta cliques nos botões `.filter-btn`
- Lê atributo `data-filter` do botão clicado
- Busca badge de categoria em cada `<article>`
- Compara com keywords do `filterMap`
- Mostra/oculta posts com `display: block/none`
- Atualiza estilo do botão ativo (azul)

### Análise de Categorias

O script usa BeautifulSoup para:
- Encontrar todos `<article>` tags
- Localizar badges: `<span class="bg-* px-2 py-1">`
- Extrair texto do badge (categoria)
- Contar com `collections.Counter`

## 📝 Workflow Recomendado

Sempre que adicionar novos posts em massa:

```bash
# 1. Adicionar novos posts ao index.html
python3 generate_new_posts.py

# 2. Atualizar filtros automaticamente
python3 update_filters.py

# 3. Verificar mudanças
git diff index.html

# 4. Commit
git add blog/index.html
git commit -m "feat: adicionar X novos posts + atualizar filtros"
git push
```

## 🎨 Personalização de UI

### Cores dos botões

Ativo: `bg-blue-600 text-white`
Inativo: `bg-gray-200 text-gray-700`

Para mudar cores, edite as classes Tailwind em `generate_filter_buttons()`:

```python
buttons_html += f'<button class="filter-btn px-4 py-2 bg-purple-600 text-white ..." ...>'
```

### Número de botões visíveis

Atualmente mostra top 8 categorias + "Todos". Para mudar:

```python
for category, count in sorted_categories[:10]:  # Mostrar top 10
```

## 🐛 Troubleshooting

**Filtros não aparecem:**
- Verifique se `id="filter-buttons"` existe no HTML
- Confirme que script está antes do `</body>`

**Contador mostra 0:**
- Hard refresh (Ctrl+Shift+R)
- Verifique console do navegador (F12)

**Categorias erradas:**
- Atualize `category_map` em `update_filters.py`
- Execute novamente o script

## 📦 Dependências

```bash
pip install beautifulsoup4
```

## 📄 Arquivos

- `update_filters.py` - Script principal
- `index.html` - Página do blog (atualizada automaticamente)
- `README_FILTERS.md` - Esta documentação

## 🔮 Futuras Melhorias

- [ ] Suporte a múltiplos filtros simultâneos
- [ ] Animações de transição nos filtros
- [ ] URL params para filtros (ex: `/blog?category=ia`)
- [ ] Contadores por categoria no botão
- [ ] Search bar integrado com filtros
