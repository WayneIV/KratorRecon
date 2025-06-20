import logging
import time
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from pyfiglet import figlet_format

console = Console()
try:
    VERSION = Path('krator_version.txt').read_text().strip()
except Exception:
    VERSION = "0.0.0"
OUTPUT_DIR = Path('output/banner')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def generate_banner() -> str:
    """Return ASCII art banner text."""
    return figlet_format("KratorStrike", font="slant")


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
    """Render the animated banner."""
    console.clear()
    banner = generate_banner()
    captured = ""
    with Live(console=console, refresh_per_second=4) as live:
        rendered = ""
        for line in banner.splitlines():
            rendered += line + "\n"
            live.update(Panel(rendered, title=f"Krator v{VERSION}", border_style="red"))
            time.sleep(0.1)
        captured = rendered
    status_panel = Panel(f"Version: {VERSION}\nStatus: Ready", title="Status", style="green")
    console.print(status_panel)
    save_output('banner', captured)
    print_summary()
