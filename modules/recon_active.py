import json
import logging
from datetime import datetime
from pathlib import Path
import socket

import requests
from rich.console import Console
from rich.prompt import Prompt

console = Console()
OUTPUT_DIR = Path('output/recon_active')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

COMMON_PORTS = [21,22,23,25,53,80,110,139,143,443,445,3389]
WORDLIST = ['admin','login','dashboard','robots.txt','sitemap.xml']


def get_input():
    return Prompt.ask('Enter target domain or IP')


def save_output(target, data):
    filename = OUTPUT_DIR / f'{target}_{datetime.now().strftime("%Y%m%d%H%M%S")}.json'
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    console.print(f'[green]Results saved to {filename}[/green]')


def print_summary(data):
    open_ports = [str(p) for p, v in data['ports'].items() if v == 'open']
    console.print(f'[cyan]Open ports: {", ".join(open_ports)}[/cyan]')


def scan_ports(target):
    results = {}
    for port in COMMON_PORTS:
        try:
            with socket.create_connection((target, port), timeout=1) as s:
                results[port] = 'open'
        except Exception:
            results[port] = 'closed'
    return results


def banner_grab(target, port):
    try:
        with socket.create_connection((target, port), timeout=2) as s:
            s.sendall(b'\n')
            return s.recv(1024).decode(errors='ignore').strip()
    except Exception:
        return ''


def dir_search(target):
    if not target.startswith('http'):
        url_base = 'http://' + target.rstrip('/') + '/'
    else:
        url_base = target.rstrip('/') + '/'
    found = []
    for word in WORDLIST:
        url = url_base + word
        try:
            resp = requests.get(url, timeout=3)
            if resp.status_code < 400:
                found.append({'path': word, 'status': resp.status_code})
        except Exception:
            continue
    return found


def run():
    console.print('[bold cyan]Active Recon Module[/bold cyan]')
    target = get_input()
    logging.info(f'Active recon for {target}')

    port_results = scan_ports(target)
    banners = {port: banner_grab(target, port) for port, state in port_results.items() if state == 'open'}
    dir_results = dir_search(target)

    data = {
        'target': target,
        'ports': port_results,
        'banners': banners,
        'directories': dir_results
    }

    save_output(target, data)
    print_summary(data)
    console.print('[bold green]Active recon completed[/bold green]')

