#!/usr/bin/env python3
"""
Analytics Tracking Script for Schema.org Implementation
Monitor Google Search Console metrics and track Rich Results performance
"""

import json
import csv
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
WORKSPACE_DIR = Path(__file__).parent
METRICS_FILE = WORKSPACE_DIR / "analytics_metrics.json"
REPORT_FILE = WORKSPACE_DIR / "weekly_seo_report.md"

def initialize_metrics():
    """Initialize baseline metrics"""
    baseline = {
        "last_updated": datetime.now().isoformat(),
        "baseline": {
            "monthly_visits": 10000,
            "avg_ctr": 0.02,
            "avg_position": 18,
            "rich_results_count": 20,
            "indexed_pages": 500
        },
        "weekly_data": [],
        "monthly_data": []
    }
    
    with open(METRICS_FILE, 'w') as f:
        json.dump(baseline, f, indent=2)
    
    print(f"✅ Metrics file initialized: {METRICS_FILE}")
    return baseline

def add_weekly_data(clicks, impressions, ctr, position, rich_results):
    """Add weekly performance data"""
    
    if not METRICS_FILE.exists():
        data = initialize_metrics()
    else:
        with open(METRICS_FILE, 'r') as f:
            data = json.load(f)
    
    week_number = len(data['weekly_data']) + 1
    week_data = {
        "week": week_number,
        "date": datetime.now().isoformat(),
        "clicks": clicks,
        "impressions": impressions,
        "ctr": ctr,
        "position": position,
        "rich_results": rich_results,
        "growth": {
            "clicks_pct": ((clicks - data['baseline']['monthly_visits']) / data['baseline']['monthly_visits']) * 100,
            "impressions_pct": 0,  # Calculate based on baseline impressions
            "ctr_improvement": ctr - data['baseline']['avg_ctr'],
            "position_improvement": data['baseline']['avg_position'] - position,
            "rich_results_growth": rich_results - data['baseline']['rich_results_count']
        }
    }
    
    data['weekly_data'].append(week_data)
    data['last_updated'] = datetime.now().isoformat()
    
    with open(METRICS_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Week {week_number} data added")
    print(f"   Clicks: {clicks:,} | CTR: {ctr:.2%} | Position: {position:.1f}")
    print(f"   Rich Results: {rich_results:,}")
    
    return week_data

def generate_weekly_report():
    """Generate markdown report with current metrics"""
    
    if not METRICS_FILE.exists():
        print("❌ No metrics file found. Run with --init first.")
        return
    
    with open(METRICS_FILE, 'r') as f:
        data = json.load(f)
    
    baseline = data['baseline']
    weekly = data['weekly_data']
    
    if not weekly:
        print("❌ No weekly data available yet.")
        return
    
    latest = weekly[-1]
    
    report = f"""# SEO Performance Report - Week {latest['week']}

**Data:** {datetime.fromisoformat(latest['date']).strftime('%d/%m/%Y')}
**Status:** Schema.org Phase 2 Complete (12.542 templates)

---

## 📊 Métricas da Semana

### Performance Geral

| Métrica | Valor Atual | Baseline | Crescimento |
|---------|-------------|----------|-------------|
| **Cliques** | {latest['clicks']:,} | {baseline['monthly_visits']:,} | **{latest['growth']['clicks_pct']:+.1f}%** |
| **Impressões** | {latest['impressions']:,} | - | - |
| **CTR Médio** | {latest['ctr']:.2%} | {baseline['avg_ctr']:.2%} | **{latest['growth']['ctr_improvement']:+.2%}** |
| **Posição Média** | {latest['position']:.1f} | {baseline['avg_position']:.1f} | **{latest['growth']['position_improvement']:+.1f}** |
| **Rich Results** | {latest['rich_results']:,} | {baseline['rich_results_count']:,} | **+{latest['growth']['rich_results_growth']:,}** |

---

## 📈 Tendência Semanal

"""
    
    # Add weekly trend table
    report += "| Semana | Cliques | Impressões | CTR | Posição | Rich Results |\n"
    report += "|--------|---------|------------|-----|---------|---------------|\n"
    
    for week in weekly[-8:]:  # Last 8 weeks
        report += f"| {week['week']} | {week['clicks']:,} | {week['impressions']:,} | {week['ctr']:.2%} | {week['position']:.1f} | {week['rich_results']:,} |\n"
    
    report += f"""
---

## 🎯 Análise

### Destaques

"""
    
    # Calculate insights
    if latest['growth']['clicks_pct'] > 50:
        report += f"✅ **Crescimento excepcional**: Cliques aumentaram {latest['growth']['clicks_pct']:.1f}% vs baseline\n"
    
    if latest['growth']['ctr_improvement'] > 0.01:
        report += f"✅ **CTR melhorando**: +{latest['growth']['ctr_improvement']:.2%} pontos de CTR\n"
    
    if latest['growth']['position_improvement'] > 3:
        report += f"✅ **Rankings subindo**: Posição média melhorou {latest['growth']['position_improvement']:.1f} posições\n"
    
    if latest['rich_results'] > 5000:
        report += f"✅ **Rich Results massivos**: {latest['rich_results']:,} páginas com Rich Snippets\n"
    
    report += """
### Próximos Passos

- [ ] Monitorar páginas com melhor performance
- [ ] Identificar queries de alto potencial
- [ ] Otimizar templates com baixo CTR
- [ ] Expandir para novos keywords
- [ ] Construir backlinks para páginas top

---

## 📝 Notas

*Este relatório é gerado automaticamente pelo script analytics_tracking.py*
*Dados baseados no Google Search Console*
*Para mais detalhes, ver: GOOGLE_SEARCH_CONSOLE_GUIDE.md*

---

**Próxima atualização:** {(datetime.fromisoformat(latest['date']) + timedelta(days=7)).strftime('%d/%m/%Y')}
"""
    
    with open(REPORT_FILE, 'w') as f:
        f.write(report)
    
    print(f"\n✅ Relatório gerado: {REPORT_FILE}")
    print(f"\n📊 Resumo da Semana {latest['week']}:")
    print(f"   Cliques: {latest['clicks']:,} ({latest['growth']['clicks_pct']:+.1f}%)")
    print(f"   CTR: {latest['ctr']:.2%} ({latest['growth']['ctr_improvement']:+.2%})")
    print(f"   Posição: {latest['position']:.1f} ({latest['growth']['position_improvement']:+.1f})")
    print(f"   Rich Results: {latest['rich_results']:,}")

def export_to_csv():
    """Export metrics to CSV for analysis"""
    
    if not METRICS_FILE.exists():
        print("❌ No metrics file found.")
        return
    
    with open(METRICS_FILE, 'r') as f:
        data = json.load(f)
    
    csv_file = WORKSPACE_DIR / "seo_metrics_export.csv"
    
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Week', 'Date', 'Clicks', 'Impressions', 'CTR', 'Position', 'Rich_Results'])
        
        for week in data['weekly_data']:
            writer.writerow([
                week['week'],
                datetime.fromisoformat(week['date']).strftime('%Y-%m-%d'),
                week['clicks'],
                week['impressions'],
                f"{week['ctr']:.4f}",
                f"{week['position']:.2f}",
                week['rich_results']
            ])
    
    print(f"✅ Dados exportados: {csv_file}")

def show_dashboard():
    """Display ASCII dashboard"""
    
    if not METRICS_FILE.exists():
        print("❌ No metrics file found. Run with --init first.")
        return
    
    with open(METRICS_FILE, 'r') as f:
        data = json.load(f)
    
    if not data['weekly_data']:
        print("❌ No data available yet.")
        return
    
    latest = data['weekly_data'][-1]
    baseline = data['baseline']
    
    print("\n" + "="*70)
    print("  📊 SEO PERFORMANCE DASHBOARD")
    print("="*70)
    print(f"\n  Última atualização: {datetime.fromisoformat(latest['date']).strftime('%d/%m/%Y %H:%M')}")
    print(f"  Semana: {latest['week']}")
    print("\n" + "-"*70)
    
    print(f"\n  🎯 MÉTRICAS PRINCIPAIS\n")
    print(f"     Cliques:      {latest['clicks']:>10,}  ({latest['growth']['clicks_pct']:+6.1f}%)")
    print(f"     Impressões:   {latest['impressions']:>10,}")
    print(f"     CTR Médio:    {latest['ctr']:>10.2%}  ({latest['growth']['ctr_improvement']:+6.2%})")
    print(f"     Posição:      {latest['position']:>10.1f}  ({latest['growth']['position_improvement']:+6.1f})")
    print(f"     Rich Results: {latest['rich_results']:>10,}  (+{latest['growth']['rich_results_growth']:,})")
    
    print("\n" + "-"*70)
    
    # Simple trend chart
    if len(data['weekly_data']) > 1:
        print(f"\n  📈 TENDÊNCIA (últimas {min(8, len(data['weekly_data']))} semanas)\n")
        
        max_clicks = max(w['clicks'] for w in data['weekly_data'][-8:])
        
        for week in data['weekly_data'][-8:]:
            bar_length = int((week['clicks'] / max_clicks) * 40)
            bar = "█" * bar_length
            print(f"     Sem {week['week']:2d}: {bar} {week['clicks']:,}")
    
    print("\n" + "="*70)
    print()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("""
📊 Analytics Tracking Script

Usage:
    python analytics_tracking.py --init
        Initialize metrics tracking
    
    python analytics_tracking.py --add <clicks> <impressions> <ctr> <position> <rich_results>
        Add weekly data (example: --add 15000 200000 0.035 12.5 5000)
    
    python analytics_tracking.py --report
        Generate weekly report
    
    python analytics_tracking.py --export
        Export to CSV
    
    python analytics_tracking.py --dashboard
        Show dashboard
        
Example:
    python analytics_tracking.py --add 15000 200000 0.035 12.5 5000
        """)
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == "--init":
        initialize_metrics()
    
    elif command == "--add":
        if len(sys.argv) != 7:
            print("❌ Usage: --add <clicks> <impressions> <ctr> <position> <rich_results>")
            sys.exit(1)
        
        clicks = int(sys.argv[2])
        impressions = int(sys.argv[3])
        ctr = float(sys.argv[4])
        position = float(sys.argv[5])
        rich_results = int(sys.argv[6])
        
        add_weekly_data(clicks, impressions, ctr, position, rich_results)
        generate_weekly_report()
    
    elif command == "--report":
        generate_weekly_report()
    
    elif command == "--export":
        export_to_csv()
    
    elif command == "--dashboard":
        show_dashboard()
    
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)
