import requests
import time
import sys
import argparse

# Default config.yaml
config = {
    'hunt_settings': {
        'interval_seconds': 120,
        'default_api': 'all',
        'only_hits': False,
        'run_once': False
    },
    'api_endpoints': {
        'phishstats': "https://api.phishstats.info/api/phishing?_sort=-date&_size=100",
        'openphish': "https://openphish.com/feed.txt",
        'phishunt': "https://phishunt.io/feed.txt"
    },
    'keywords': []
}

try:
    import yaml
    with open("config.yaml", "r") as f:
        yaml_config = yaml.safe_load(f)
        if yaml_config:
            if 'hunt_settings' in yaml_config:
                config['hunt_settings'].update(yaml_config['hunt_settings'])
            if 'api_endpoints' in yaml_config:
                config['api_endpoints'].update(yaml_config['api_endpoints'])
            if 'keywords' in yaml_config:
                config['keywords'] = yaml_config['keywords']
except ImportError:
    print("[!] PyYAML module is required to read config.yaml")
except FileNotFoundError:
    pass
except Exception as e:
    print(f"[!] Error loading config.yaml: {e}")

fetch = False
keywords = []

parser = argparse.ArgumentParser()
parser.add_argument('--api', choices=['phishstats', 'openphish', 'phishunt', 'all'], default=config['hunt_settings']['default_api'])
parser.add_argument('-oh', '--only-hits', action='store_true', default=None)
parser.add_argument('-o', '--once', action='store_true', default=None)
args = parser.parse_args()

only_hits = args.only_hits if args.only_hits is not None else config['hunt_settings']['only_hits']
once = args.once if args.once is not None else config['hunt_settings']['run_once']

def fetch_phishstats():
    try:
        url = config['api_endpoints']['phishstats']
        r = requests.get(url, timeout=10)
        return [
            {"url": e.get("url", ""), "source": "PhishStats", "title": e.get("title", "") or ""}
            for e in r.json()
            if "bad gateway" not in (e.get("title", "") or "").lower()
        ]
    except:
        return []

def fetch_openphish():
    try:
        url = config['api_endpoints']['openphish']
        r = requests.get(url, timeout=10)
        return [{"url": u, "source": "OpenPhish", "title": ""} for u in r.text.strip().split('\n')[:20]]
    except:
        return []

def fetch_phishunt():
    try:
        url = config['api_endpoints']['phishunt']
        r = requests.get(url, timeout=10)
        return [{"url": u, "source": "PhishHunt", "title": ""} for u in r.text.strip().split('\n')[:20]]
    except:
        return []

def wordlist():
    while True:
        word = input("Keyword (leave blank to initiate scan): ").strip()
        if not word:
            break
        keywords.append(word.lower())
        print("Added: {}".format(word))

def hunt():
    global keywords, fetch
    if not fetch:
        wordlist()
        fetch = True
    if keywords == []:
        config_keywords = config.get("keywords", [])
        if config_keywords:
            keywords = [k.strip().lower() for k in config_keywords if k.strip()]
            print("[/] No keywords entered. Using keywords from config.yaml.")
        else:
            print("[!] No keywords found in config.yaml.")
            sys.exit(1)
            
    print(f"\n{'='*60}")
    print(f"  FLOYA'S PHISH HUNTER - {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    all_urls = []
    
    if args.api in ['phishstats', 'all']:
        print("[*] Fetching from PhishStats")
        all_urls += fetch_phishstats()
    
    if args.api in ['openphish', 'all']:
        print("[*] Fetching from OpenPhish")
        all_urls += fetch_openphish()
    
    if args.api in ['phishunt', 'all']:
        print("[*] Fetching from PhishHunt")
        all_urls += fetch_phishunt()
    
    print(f"\n[*] Total URLs: {len(all_urls)}\n")
    
    matched_entries = []
    unmatched_entries = []
    
    for entry in all_urls:
        url = entry['url']
        source = entry['source']
        title = entry['title']
        
        is_match = any(k in url.lower() or k in title.lower() for k in keywords)
        
        if is_match:
            matched_entries.append(entry)
        else:
            unmatched_entries.append(entry)
            
    for entry in unmatched_entries:
        if not only_hits:
            print(f"[-] [{entry['source']}] {entry['url'][:70]}")
        
    if matched_entries:
        print(f"\n{'='*20} MATCHED URLs {'='*20}\n")
        for entry in matched_entries:
            print(f"[!] [{entry['source']}] MATCH: {entry['url']}")
            
    hits = len(matched_entries)
    
    print(f"\n{'='*60}")
    print(f"  Results: {hits} matches out of {len(all_urls)} URLs")
    print(f"{'='*60}")

while True:
    hunt()
    if once:
        break
    interval = config['hunt_settings']['interval_seconds']
    print(f"\n [*] Waiting {interval} seconds before next scan...\n")
    time.sleep(interval)