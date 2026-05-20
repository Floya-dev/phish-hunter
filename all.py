import requests
import time
import sys

fetch = False
keywords = []

def fetch_phishstats():
    try:
        url = "https://api.phishstats.info/api/phishing?_sort=-date&_size=20" # Phistats limits one user to 20 queries per minute
        r = requests.get(url, timeout=10)
        return [
            {"url": e.get("url", ""), "source": "PhishStats", "title": ""}
            for e in r.json()
            if "bad gateway" not in e.get("title", "").lower()
        ]
    except:
        return []

def fetch_openphish():
    try:
        r = requests.get("https://openphish.com/feed.txt", timeout=10)
        return [{"url": u, "source": "OpenPhish", "title": ""} for u in r.text.strip().split('\n')[:20]]
    except:
        return []

def fetch_phishunt():
    try:
        r = requests.get("https://phishunt.io/feed.txt", timeout=10)
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
        try:
            with open("keywords.txt", "r") as f:
                keywords = [line.strip().lower() for line in f if line.strip()]
            print("[/] No keywords entered. Using default keywords from keywords.txt.")
        except FileNotFoundError:
            print("[!] keywords.txt not found. Download it from my GitHub repo.")
            sys.exit(1)
            
    print(f"\n{'='*60}")
    print(f"  FLOYA'S PHISH HUNTER - {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    all_urls = []
    
    print("[*] Fetching from PhishStats")
    all_urls += fetch_phishstats()
    
    print("[*] Fetching from OpenPhish")
    all_urls += fetch_openphish()
    
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
        print(f"[-] [{entry['source']}] {entry['url'][:70]}")
        
    if matched_entries:
        print(f"\n{'='*20} MATCHED URLs {'='*20}\n")
        for entry in matched_entries:
            print(f"[!] [{entry['source']}] MATCH: {entry['url']}")
            if entry['title']:
                print(f"   Title/Tags: {entry['title']}")
            
    hits = len(matched_entries)
    
    print(f"\n{'='*60}")
    print(f"  Results: {hits} matches out of {len(all_urls)} URLs")
    print(f"{'='*60}")

while True:
    hunt()
    print("\n [*] Waiting 120 seconds before next scan...\n")
    time.sleep(120)
