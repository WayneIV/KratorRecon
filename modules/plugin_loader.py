import os
import subprocess
import logging
from pathlib import Path

from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

console = Console()
PLUG_DIR = Path('plugins')
PLUG_DIR.mkdir(exist_ok=True)


def list_plugins():
    return [f for f in PLUG_DIR.iterdir() if f.suffix in ('.py', '.sh')]


def run_plugin(path: Path):
    logging.info(f'Running plugin {path}')
    try:
        if path.suffix == '.py':
            subprocess.run(['python3', str(path)], check=True)
        elif path.suffix == '.sh':
            subprocess.run(['bash', str(path)], check=True)
    except subprocess.CalledProcessError as e:
        console.print(f'[red]Plugin {path} failed: {e}[/red]')
        logging.error(f'Plugin {path} failed: {e}')


def save_output(_target, _data):
    pass


def print_summary():
    console.print('[cyan]Plugin loader finished[/cyan]')


def run():
    console.print('[bold cyan]Plugin Loader[/bold cyan]')
    plugins = list_plugins()
    if not plugins:
        console.print('[yellow]No plugins found[/yellow]')
        return
    table = Table('Index', 'Plugin')
    for i, p in enumerate(plugins, 1):
        table.add_row(str(i), p.name)
    console.print(table)
    choice = Prompt.ask('Select plugin number (0 to cancel)', default='0')
    if choice == '0':
        return
    try:
        idx = int(choice) - 1
        if idx < 0 or idx >= len(plugins):
            raise ValueError
    except ValueError:
        console.print('[red]Invalid selection[/red]')
        return
    run_plugin(plugins[idx])
    print_summary()
    console.print('[green]Plugin execution completed[/green]')
