import logging
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from pyfiglet import figlet_format

console = Console()
try:
    VERSION = Path('krator_version.txt').read_text().strip()
except Exception:
    VERSION = "0.0.0"
OUTPUT_DIR = Path('output/banner')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BANNER = figlet_format("Krator", font="slant")


# required input() function

def input():
    """No user input required for banner."""
    return {}



def save_output(_target, data):
    filename = OUTPUT_DIR / f"banner_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
    with open(filename, 'w') as f:
        f.write(data)
    logging.info(f"Banner saved to {filename}")


def print_summary():
    console.print("[bold magenta]Banner displayed.[/bold magenta]")


def run():
    console.clear()
    color_banner = f"[bold magenta]{BANNER}[/bold magenta]"
    panel = Panel.fit(color_banner, title=f"Krator v{VERSION}", border_style="red")
    console.print(panel)
    status_panel = Panel(f"Version: {VERSION}\nStatus: Ready", title="Status", style="green")
    console.print(status_panel)
    save_output('banner', BANNER + "\n")
    print_summary()
