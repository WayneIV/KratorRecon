import hashlib
import json
import logging
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

from rich.console import Console
from rich.prompt import Prompt

console = Console()
OUTPUT_DIR = Path('output/brute')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
WORDLIST_DIR = Path('data/wordlists')


def choose_wordlist():
    lists = list(WORDLIST_DIR.glob('*.txt'))
    table = '\n'.join(f"{i+1}. {p.name}" for i, p in enumerate(lists))
    console.print(table)
    idx = Prompt.ask('Select wordlist number', default='1')
    try:
        return lists[int(idx)-1]
    except Exception:
        return lists[0]


def save_output(target, data):
    fn = OUTPUT_DIR / f"{target}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    with open(fn, 'w') as f:
        json.dump(data, f, indent=2)
    console.print(f"[green]Results saved to {fn}[/green]")


def print_summary(data):
    if data.get('credentials'):
        for cred in data['credentials']:
            console.print(f"[cyan]Found: {cred['username']}:{cred['password']}")
    else:
        console.print('[yellow]No credentials found[/yellow]')


def brute_hash():
    hash_value = Prompt.ask('Hash value')
    algo = Prompt.ask('Algorithm (md5/sha1/sha256)', default='sha256')
    wordlist = choose_wordlist()
    found = None
    for word in open(wordlist, 'r', errors='ignore'):
        word = word.strip()
        h = getattr(hashlib, algo)(word.encode()).hexdigest()
        if h == hash_value:
            found = word
            break
    data = {'type': 'hash', 'hash': hash_value, 'algorithm': algo}
    if found:
        data['credentials'] = [{'password': found}]
    return data


def hydra_brute(service):
    if not shutil.which('hydra'):
        console.print('[red]Hydra not installed[/red]')
        return {'error': 'hydra missing'}
    target = Prompt.ask('Target (ip or url)')
    user = Prompt.ask('Username')
    wordlist = choose_wordlist()
    outfile = OUTPUT_DIR / 'hydra.txt'
    cmd = ['hydra', '-l', user, '-P', str(wordlist), service, target, '-o', str(outfile)]
    try:
        subprocess.run(cmd, check=True)
        creds = []
        for line in outfile.read_text().splitlines():
            if ':' in line:
                creds.append({'username': user, 'password': line.split(':')[-1]})
        return {'type': service, 'target': target, 'credentials': creds}
    except subprocess.CalledProcessError as e:
        logging.error(f'Hydra failed: {e}')
        return {'error': str(e)}


def run():
    console.print('[bold cyan]Brute Force Engine[/bold cyan]')
    mode = Prompt.ask('Mode: hash, ssh, ftp, http', default='hash')
    if mode == 'hash':
        result = brute_hash()
        save_output('hash', result)
        print_summary(result)
    else:
        result = hydra_brute(mode)
        save_output(mode, result)
        print_summary(result)

