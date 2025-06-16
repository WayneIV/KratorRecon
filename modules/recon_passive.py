import json
import logging
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.prompt import Prompt

import dns.resolver
import requests
from ipwhois import IPWhois
import whois

console = Console()
OUTPUT_DIR = Path('output/recon_passive')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def get_input():
    return Prompt.ask('Enter domain or IP')


def save_output(target, data):
    filename = OUTPUT_DIR / f'{target}_{datetime.now().strftime("%Y%m%d%H%M%S")}.json'
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    console.print(f'[green]Results saved to {filename}[/green]')


def whois_lookup(target):
    try:
        if all(c.isdigit() or c == '.' for c in target):
            return IPWhois(target).lookup_rdap()
        return whois.whois(target)
    except Exception as e:
        logging.error(f'WHOIS failed: {e}')
        return {'error': str(e)}


def dns_lookup(target):
    records = {}
    resolver = dns.resolver.Resolver()
    resolver.nameservers = ['8.8.8.8']
    try:
        for rtype in ['A', 'AAAA', 'MX', 'NS']:
            try:
                answers = resolver.resolve(target, rtype)
                records[rtype] = [a.to_text() for a in answers]
            except Exception:
                records[rtype] = []
    except Exception as e:
        logging.error(f'DNS lookup error: {e}')
    return records


def http_headers(target):
    if not target.startswith('http'):
        url = 'http://' + target
    else:
        url = target
    try:
        resp = requests.get(url, timeout=5)
        return dict(resp.headers)
    except Exception as e:
        logging.error(f'HTTP headers error: {e}')
        return {'error': str(e)}


def run():
    console.print('[bold cyan]Passive Recon Module[/bold cyan]')
    target = get_input()
    logging.info(f'Passive recon for {target}')

    data = {
        'target': target,
        'whois': whois_lookup(target),
        'dns': dns_lookup(target),
        'http_headers': http_headers(target)
    }

    save_output(target, data)
    console.print('[bold green]Passive recon completed[/bold green]')

