import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from event_automation.firestore_utils import save_events_to_firestore
from datetime import datetime

BASE_URL = "https://www.nycforfree.co/events/"

# Helper to get all months from now to December
from calendar import month_name

def get_month_urls():
    now = datetime.now()
    year = now.year
    month_urls = []
    for m in range(now.month, 13):
        month_str = month_name[m].lower()
        url = f"{BASE_URL}{month_str}-{year}"
        month_urls.append(url)
    return month_urls

def scrape_nycforfree_events():
    """
    Scrape free NYC events from nycforfree.co for the rest of the year and return a list of event dicts:
    [{ 'name': ..., 'date': ..., 'location': ..., 'link': ... }, ...]
    """
    events = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    month_urls = get_month_urls()
    for url in month_urls:
        response = requests.get(url, headers=headers)
        print(f"Fetching {url} - Status: {response.status_code}")
        if response.status_code != 200:
            print(f"Failed to fetch {url}: {response.status_code}")
            continue
        soup = BeautifulSoup(response.text, 'html.parser')
        # Try to find event blocks (update selector as needed)
        for event_block in soup.find_all('section'):
            if not isinstance(event_block, Tag):
                continue
            name_tag = event_block.find('h2') if isinstance(event_block, Tag) else None
            if not name_tag:
                name_tag = event_block.find('h3') if isinstance(event_block, Tag) else None
            name = name_tag.text.strip() if name_tag and hasattr(name_tag, 'text') else None
            date_tag = event_block.find('p') if isinstance(event_block, Tag) else None
            date = date_tag.text.strip() if date_tag and hasattr(date_tag, 'text') else None
            location = None
            link_tag = event_block.find('a') if isinstance(event_block, Tag) else None
            link = link_tag.get('href') if isinstance(link_tag, Tag) else None
            if isinstance(link, str) and not link.startswith('http'):
                link = 'https://www.nycforfree.co' + link
            if name and date:
                events.append({
                    'name': name,
                    'date': date,
                    'location': location,
                    'link': link
                })
    return events

if __name__ == "__main__":
    events = scrape_nycforfree_events()
    for event in events:
        print(event)
    if events:
        upload = input("\nUpload these events to Firestore? (y/n): ").strip().lower()
        if upload == 'y':
            save_events_to_firestore(events, source="nycforfree.co")
        else:
            print("Events not uploaded.") 