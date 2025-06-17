import importlib
import sys
import logging
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

from modules import ascii_banner

logging.basicConfig(filename='logs/session.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

console = Console()
Path('logs').mkdir(exist_ok=True)

MODULES = {
    '1': ('Passive Recon', 'recon_passive'),
    '2': ('Active Recon', 'recon_active'),
    '3': ('Brute Force', 'brute_force'),
    '4': ('Visual Recon', 'visual_recon'),
    '5': ('AI Analyst', 'ai_analyst'),
    '6': ('Plugin Loader', 'plugin_loader'),
    '7': ('Generate Report', 'report_gen'),
    '8': ('Self Updater', 'self_updater'),
}


def disclaimer():
    console.print('[bold red]Warning:[/bold red] Use only on systems you own or have permission to test.')
    console.print('Unauthorized use may violate the CFAA and Iowa Code \u00a7715.6')
    ans = Prompt.ask('Do you accept the acceptable use policy? (yes/no)', default='no')
    if ans.lower() != 'yes':
        console.print('Declined. Exiting.')
        sys.exit(0)

def main():
    disclaimer()
    try:
        ascii_banner.run()
    except Exception as e:
        logging.error(f"Failed to display banner: {e}")
    while True:
        table = Table(title="KratorStrike")
        table.add_column("Option")
        table.add_column("Module")
        for key in sorted(MODULES.keys(), key=int):
            name, _ = MODULES[key]
            table.add_row(key, name)
        table.add_row('0', 'Exit')
        console.print(table)
        choice = Prompt.ask("Select option")
        if choice == '0':
            break
        module = MODULES.get(choice)
        if not module:
            console.print("[red]Invalid choice[/red]")
            continue
        name, mod_name = module
        try:
            logging.info(f"Launching module: {name}")
            mod = importlib.import_module(f"modules.{mod_name}")
            mod.run()
        except Exception as e:
            logging.error(f"Error running {name}: {e}")
            console.print(f"[red]Error running {name}: {e}[/red]")

if __name__ == '__main__':
    main()
