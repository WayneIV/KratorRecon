import importlib
import sys
import logging
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

logging.basicConfig(filename='logs/session.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

console = Console()

MODULES = {
    '1': ('Passive Recon', 'recon_passive'),
    '2': ('Active Recon', 'recon_active'),
    '3': ('AI Analyst', 'ai_analyst'),
    '4': ('Plugin Loader', 'plugin_loader'),
    '5': ('Generate Report', 'report_gen')
}

def main():
    while True:
        table = Table(title="KratorStrike")
        table.add_column("Option")
        table.add_column("Module")
        for key, (name, _) in MODULES.items():
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
