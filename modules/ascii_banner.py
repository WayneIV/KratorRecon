import json
import logging
import time
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.live import Live

console = Console()
VERSION = "0.1.0"
OUTPUT_DIR = Path('output/banner')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BANNER_LINES = [
    "  _  __               _            _____ _     _       ",
    " | |/ /              | |          /  __ \ |   | |      ",
    " | ' / ___ _ __   ___| | _____    | /  \/ |__ | | ___  ",
    " |  < / _ \ '_ \ / __| |/ / __|   | |   | '_ \| |/ _ \ ",
    " | . \  __/ | | | (__|   <\__ \   | \__/\ | | | |  __/ ",
    " |_|\_\___|_| |_|\___|_|\_\___/    \____/_| |_|_|\___| ",
]


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
    captured = ""
    with Live(console=console, refresh_per_second=4) as live:
        rendered = ""
        for line in BANNER_LINES:
            rendered += line + "\n"
            live.update(Panel(rendered, title=f"KratorStrike v{VERSION}", border_style="red"))
            time.sleep(0.2)
        captured = rendered
    status_panel = Panel(f"Version: {VERSION}\nStatus: Ready", title="Status", style="green")
    console.print(status_panel)
    save_output('banner', captured)
    print_summary()
