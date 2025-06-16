import subprocess
from pathlib import Path
from rich.console import Console

console = Console()


def save_output(_t, _d):
    pass


def print_summary():
    console.print('[cyan]Update check finished[/cyan]')


def run():
    console.print('[bold cyan]Self Updater[/bold cyan]')
    repo = Path(__file__).resolve().parent.parent
    try:
        subprocess.run(['git', '-C', str(repo), 'pull'], check=True)
        console.print('[green]Repository updated[/green]')
    except subprocess.CalledProcessError:
        console.print('[red]Update failed[/red]')
    print_summary()
