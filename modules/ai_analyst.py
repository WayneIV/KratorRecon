import json
import logging
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt

console = Console()
OUTPUT_DIR = Path('output/analysis')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def get_input():
    return Prompt.ask('Enter path to JSON file for analysis')


def analyze(data):
    summary = []
    if 'ports' in data:
        open_ports = [str(p) for p, s in data['ports'].items() if s == 'open']
        if open_ports:
            summary.append('Open ports: ' + ', '.join(open_ports))
    if 'directories' in data and data['directories']:
        dirs = ', '.join(d['path'] for d in data['directories'])
        summary.append('Interesting directories: ' + dirs)
    if not summary:
        summary.append('No notable findings.')
    return '\n'.join(summary)


def save_output(src, text):
    out_file = OUTPUT_DIR / (Path(src).stem + '_summary.txt')
    with open(out_file, 'w') as f:
        f.write(text)
    console.print(f'[green]Summary saved to {out_file}[/green]')


def run():
    console.print('[bold cyan]AI Analyst[/bold cyan]')
    path = get_input()
    try:
        data = json.load(open(path))
    except Exception as e:
        console.print(f'[red]Failed to load JSON: {e}[/red]')
        logging.error(f'Failed to load JSON: {e}')
        return
    result = analyze(data)
    console.print(result)
    save_output(path, result)
