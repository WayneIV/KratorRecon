import logging
import subprocess
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

console = Console()
PLUG_DIR = Path('plugins')
PLUG_DIR.mkdir(exist_ok=True)
OUTPUT_DIR = Path('output/plugins')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def list_plugins():
    return [f for f in PLUG_DIR.iterdir() if f.suffix in ('.py', '.sh')]


def run_plugin(path: Path) -> str:
    """Execute a plugin and capture its output."""
    logging.info(f'Running plugin {path}')
    try:
        if path.suffix == '.py':
            result = subprocess.run(['python3', str(path)], capture_output=True, text=True)
        elif path.suffix == '.sh':
            result = subprocess.run(['bash', str(path)], capture_output=True, text=True)
        else:
            console.print(f'[red]Unsupported plugin type: {path}[/red]')
            return ''
        if result.returncode != 0:
            console.print(f'[red]Plugin {path.name} exited with code {result.returncode}[/red]')
        return result.stdout + result.stderr
    except subprocess.CalledProcessError as e:
        console.print(f'[red]Plugin {path} failed: {e}[/red]')
        logging.error(f'Plugin {path} failed: {e}')
        return str(e)


def save_output(plugin: str, output: str):
    """Save plugin output to a timestamped log file."""
    filename = OUTPUT_DIR / f"{plugin}_{datetime.now().strftime('%Y%m%d%H%M%S')}.log"
    with open(filename, 'w') as f:
        f.write(output)
    logging.info(f'Plugin output saved to {filename}')


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
    output = run_plugin(plugins[idx])
    save_output(plugins[idx].stem, output)
    print_summary()
    console.print('[green]Plugin execution completed[/green]')

