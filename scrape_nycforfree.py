import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from event_automation.firestore_utils import save_events_to_firestore

NYCFORFREE_URL = "https://www.nycforfree.co/events"

def scrape_nycforfree_events():
    """
    Scrape free NYC events from nycforfree.co and return a list of event dicts:
    [{ 'name': ..., 'date': ..., 'location': ..., 'link': ... }, ...]
    """
    events = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(NYCFORFREE_URL, headers=headers)
    print(response.status_code)
    print(response.text[:500])
    if response.status_code != 200:
        print(f"Failed to fetch NYC for FREE page: {response.status_code}")
        return events
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find event blocks (structure may change, so this is a best guess)
    for event_block in soup.find_all('section'):
        if not isinstance(event_block, Tag):
            continue
        # Try to find event name
        name_tag = event_block.find('h2') if isinstance(event_block, Tag) else None
        if not name_tag:
            name_tag = event_block.find('h3') if isinstance(event_block, Tag) else None
        name = name_tag.text.strip() if name_tag and hasattr(name_tag, 'text') else None
        # Try to find date
        date_tag = event_block.find('p') if isinstance(event_block, Tag) else None
        date = date_tag.text.strip() if date_tag and hasattr(date_tag, 'text') else None
        # Try to find location
        location = None
        # Try to find link
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