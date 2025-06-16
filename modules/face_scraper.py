import json
import logging
import socket
from datetime import datetime
from pathlib import Path
from io import BytesIO
from urllib.parse import urlparse, quote_plus

import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.prompt import Prompt

try:
    import face_recognition
    from PIL import Image
except Exception as e:  # modules missing
    face_recognition = None
    Image = None
    logging.error(f"Face recognition dependencies missing: {e}")

console = Console()
OUTPUT_DIR = Path('output/faces')
MATCH_DIR = OUTPUT_DIR / 'matches'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
MATCH_DIR.mkdir(parents=True, exist_ok=True)


def input():
    img_path = Prompt.ask('Path to known face image')
    query = Prompt.ask('Search term for Google Images', default='')
    return {'image': img_path, 'query': query}


def save_output(target, data):
    filename = OUTPUT_DIR / f"{target}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    logging.info(f"Face scraper results saved to {filename}")
    console.print(f"[green]Results saved to {filename}[/green]")


def print_summary():
    console.print("[bold magenta]Face scraping completed[/bold magenta]")


def fetch_image_urls(query, limit=5):
    url = f"https://www.google.com/search?tbm=isch&q={quote_plus(query)}"
    try:
        resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
    except Exception as e:
        logging.error(f"Failed to query Google: {e}")
        return []
    soup = BeautifulSoup(resp.text, 'html.parser')
    urls = []
    for img in soup.find_all('img'):
        src = img.get('src')
        if src and src.startswith('http'):
            urls.append(src)
        if len(urls) >= limit:
            break
    return urls


def geo_ip(url):
    try:
        domain = urlparse(url).netloc
        ip = socket.gethostbyname(domain)
        resp = requests.get(f"https://freegeoip.app/json/{ip}", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            return {
                'ip': ip,
                'country': data.get('country_name'),
                'city': data.get('city'),
            }
    except Exception as e:
        logging.error(f"GeoIP lookup failed: {e}")
    return {}


def match_faces(known_path, urls):
    results = []
    if not face_recognition:
        console.print("[red]face_recognition not available[/red]")
        return results
    try:
        known_img = face_recognition.load_image_file(known_path)
        known_enc = face_recognition.face_encodings(known_img)[0]
    except Exception as e:
        console.print(f"[red]Failed to load known image: {e}[/red]")
        logging.error(f"Failed to load known image: {e}")
        return results
    for url in urls:
        try:
            r = requests.get(url, timeout=5)
            unknown_img = face_recognition.load_image_file(BytesIO(r.content))
            encs = face_recognition.face_encodings(unknown_img)
        except Exception as e:
            logging.error(f"Failed to process image {url}: {e}")
            continue
        for enc in encs:
            match = face_recognition.compare_faces([known_enc], enc, tolerance=0.6)
            if match and match[0]:
                meta = extract_exif(BytesIO(r.content))
                geo = geo_ip(url)
                fname = MATCH_DIR / f"match_{datetime.now().strftime('%H%M%S%f')}.jpg"
                try:
                    with open(fname, 'wb') as f:
                        f.write(r.content)
                except Exception as e:
                    logging.error(f"Failed to save image {fname}: {e}")
                results.append({'file': str(fname), 'url': url, 'exif': meta, 'geo': geo})
                console.print(f"[green]Match found: {url} -> {fname}[/green]")
    return results


def extract_exif(buf):
    if not Image:
        return {}
    try:
        img = Image.open(buf)
        exif = img._getexif() or {}
        gps = exif.get(34853)  # GPSInfo
        return {'gps': gps}
    except Exception:
        return {}


def run():
    params = input()
    urls = fetch_image_urls(params['query']) if params['query'] else []
    matches = match_faces(params['image'], urls)
    data = {'input_image': params['image'], 'query': params['query'], 'matches': matches}
    save_output('faces', data)
    print_summary()
