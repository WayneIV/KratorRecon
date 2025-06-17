# KratorStrike

KratorStrike is a modular terminal-based toolkit for ethical red team reconnaissance and analysis. Each module logs actions to `logs/session.log` and writes JSON results to the `output/` directory.

## Installation

Run the installer to set up dependencies and create a `kratorstrike` alias:

```bash
bash install.sh
```

## Usage

Launch the dashboard:

```bash
python3 kratorstrike.py
```

Use the arrow keys to navigate the vibrant menu and select a module. You can drop custom scripts into the `plugins/` directory and run them via the **Plugin Loader** option. Reports can be generated from collected JSON files with the **Generate Report** option.

## Disclaimer

KratorStrike is provided for lawful, authorized security testing only. Users must comply with all applicable laws including the CFAA and Iowa Code §715.6.
