import logging
import subprocess
from datetime import datetime
from pathlib import Path
from rich.console import Console

console = Console()
OUTPUT_DIR = Path('output/update')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def save_output(_target, data: str):
    """Save git pull output."""
    filename = OUTPUT_DIR / f"update_{datetime.now().strftime('%Y%m%d%H%M%S')}.log"
    with open(filename, 'w') as f:
        f.write(data)
    logging.info(f'Update log saved to {filename}')


def print_summary():
    console.print('[cyan]Update check finished[/cyan]')


def run():
    console.print('[bold cyan]Self Updater[/bold cyan]')
    repo = Path(__file__).resolve().parent.parent
    try:
        result = subprocess.run(['git', '-C', str(repo), 'pull'], capture_output=True, text=True)
        save_output('update', result.stdout + result.stderr)
        if result.returncode == 0:
            console.print('[green]Repository updated[/green]')
        else:
            console.print('[red]Update failed[/red]')
            logging.error('Update failed')
    except subprocess.CalledProcessError as e:
        console.print('[red]Update failed[/red]')
        save_output('update', str(e))
        logging.error(f'Update failed: {e}')
    print_summary()
