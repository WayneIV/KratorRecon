import subprocess
from datetime import datetime
from pathlib import Path
from rich.console import Console

console = Console()
OUTPUT_DIR = Path('output/updater')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def save_output(target: str, data: str) -> None:
    """Save updater output to a timestamped file."""
    filename = OUTPUT_DIR / f"{target}_{datetime.now().strftime('%Y%m%d%H%M%S')}.log"
    with open(filename, 'w') as f:
        f.write(data)
    console.log(f'Update output saved to {filename}')


def print_summary():
    console.print('[cyan]Update check finished[/cyan]')


def run():
    console.print('[bold cyan]Self Updater[/bold cyan]')
    repo = Path(__file__).resolve().parent.parent
    try:
        result = subprocess.run(['git', '-C', str(repo), 'pull'], capture_output=True, text=True, check=True)
        console.print('[green]Repository updated[/green]')
        save_output('update', result.stdout + result.stderr)
    except subprocess.CalledProcessError as e:
        console.print('[red]Update failed[/red]')
        save_output('update_error', e.stderr if hasattr(e, 'stderr') else str(e))
    print_summary()
