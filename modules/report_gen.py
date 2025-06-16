import json
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt

console = Console()
REPORTS_DIR = Path('output')
OUT_FILE = Path('output/report.md')


def gather_files():
    files = list(REPORTS_DIR.rglob('*.json'))
    return files


def run():
    console.print('[bold cyan]Report Generator[/bold cyan]')
    files = gather_files()
    if not files:
        console.print('[yellow]No JSON files found[/yellow]')
        return
    report_lines = ['# KratorStrike Report']
    for path in files:
        report_lines.append(f'## {path.stem}')
        try:
            data = json.load(open(path))
            report_lines.append('```json')
            report_lines.append(json.dumps(data, indent=2))
            report_lines.append('```')
        except Exception as e:
            console.print(f'[red]Failed to load {path}: {e}[/red]')
    OUT_FILE.write_text('\n'.join(report_lines))
    console.print(f'[green]Report written to {OUT_FILE}[/green]')
