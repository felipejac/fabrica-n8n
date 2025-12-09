#!/usr/bin/env python3
"""
Script para melhorar títulos e descriptions com linguagem natural
Otimiza para queries conversacionais e AEO (Answer Engine Optimization)
"""

import csv
import re

def improve_title(software_a, software_b, tipo_evento, titulo_atual):
    """
    Melhora título para ser mais conversacional
    De: "Como enviar leads do Facebook Ads para o WhatsApp (Chatwoot) usando N8N"
    Para: "Como enviar leads do Facebook Ads para WhatsApp automaticamente"
    """
    
    # Padrões de melhoria
    improvements = {
        # Remover redundâncias
        'usando N8N': '',
        'com N8N': '',
        'via N8N': '',
        'pelo N8N': '',
        
        # Adicionar palavras-chave naturais
        'Como integrar': 'Como integrar automaticamente',
        'Como enviar': 'Como enviar automaticamente',
        'Como salvar': 'Como salvar automaticamente',
        'Como receber': 'Como receber automaticamente',
        'Como criar': 'Como criar automaticamente',
        'Como registrar': 'Como registrar automaticamente',
        'Como sincronizar': 'Como sincronizar automaticamente',
    }
    
    improved = titulo_atual
    for old, new in improvements.items():
        improved = improved.replace(old, new)
    
    # Garantir "automaticamente" ou "em tempo real" no final se não tiver
    if 'automati' not in improved.lower() and 'tempo real' not in improved.lower():
        improved = improved.rstrip('.') + ' automaticamente'
    
    return improved.strip()

def improve_description(descricao_atual, software_a, software_b, caso_uso):
    """
    Melhora description para SEO e AEO
    Adiciona contexto, benefícios e palavras-chave
    """
    
    # Garantir que tem pelo menos 120 caracteres
    if len(descricao_atual) < 120:
        benefit_phrases = [
            'Economize tempo automatizando este processo.',
            'Sem código, sem complicação.',
            'Configure em minutos.',
            'Ideal para equipes de marketing e vendas.',
            'Workflow pronto para usar no n8n.',
        ]
        
        # Adicionar frase de benefício apropriada
        if 'leads' in descricao_atual.lower() or 'vendas' in caso_uso.lower():
            descricao_atual += ' ' + benefit_phrases[3]
        elif 'automati' in descricao_atual.lower():
            descricao_atual += ' ' + benefit_phrases[0]
        else:
            descricao_atual += ' ' + benefit_phrases[4]
    
    # Adicionar call-to-action se não tiver
    cta_phrases = ['Veja o passo a passo completo.', 'Baixe o template pronto.', 'Configure em minutos.']
    if not any(cta in descricao_atual for cta in cta_phrases):
        descricao_atual += ' ' + cta_phrases[0]
    
    return descricao_atual.strip()

def process_csv(input_file='automacoes_db.csv', output_file='automacoes_db_improved.csv'):
    """
    Processa o CSV melhorando títulos e descriptions
    """
    
    print(f"📖 Lendo {input_file}...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    print(f"✅ {len(rows)} registros encontrados")
    print(f"🔧 Melhorando títulos e descriptions...")
    
    improved_count = 0
    
    for row in rows:
        software_a = row['software_a']
        software_b = row['software_b']
        tipo_evento = row['tipo_evento']
        caso_uso = row['caso_uso_resumido']
        
        # Melhorar título
        old_title = row['titulo_pagina']
        new_title = improve_title(software_a, software_b, tipo_evento, old_title)
        
        if new_title != old_title:
            row['titulo_pagina'] = new_title
            improved_count += 1
        
        # Melhorar description
        old_desc = row['descricao_curta']
        new_desc = improve_description(old_desc, software_a, software_b, caso_uso)
        
        if new_desc != old_desc:
            row['descricao_curta'] = new_desc
            improved_count += 1
    
    print(f"✨ {improved_count} melhorias aplicadas")
    print(f"💾 Salvando em {output_file}...")
    
    # Salvar arquivo melhorado
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        if rows:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
    
    print(f"✅ Concluído!")
    print(f"\nExemplos de melhorias:")
    print("-" * 80)
    
    # Mostrar 5 exemplos
    for i, row in enumerate(rows[:5]):
        print(f"\n{i+1}. {row['software_a']} → {row['software_b']}")
        print(f"   Título: {row['titulo_pagina'][:80]}...")
        print(f"   Descrição: {row['descricao_curta'][:100]}...")

if __name__ == '__main__':
    process_csv()
