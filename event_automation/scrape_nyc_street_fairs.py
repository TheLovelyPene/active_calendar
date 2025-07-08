import requests
from bs4 import BeautifulSoup
from event_automation.firestore_utils import save_events_to_firestore
from datetime import datetime

# 1. Grand Bazaar NYC (fully implemented example)
def scrape_grand_bazaar_nyc():
    url = "https://grandbazaarnyc.org/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    events = []
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch Grand Bazaar NYC: {response.status_code}")
        return events
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find special events (e.g., Jul13 Picnic Paradise Bazaar)
    for event_tag in soup.find_all(string=True):
        parent = getattr(event_tag, 'parent', None)
        if parent and hasattr(parent, 'name') and (
            parent.name in ['h4', 'h5', 'h6'] or (parent.name == 'div' and isinstance(event_tag, str) and 'event' in event_tag.lower())
        ):
            text = event_tag.strip() if isinstance(event_tag, str) else ''
            # Look for date and event name pattern (e.g., Jul13 Picnic Paradise Bazaar)
            import re
            if isinstance(text, str):
                match = re.match(r'([A-Za-z]{3}\d{1,2}) (.+)', text)
                if match:
                    date_str, name = match.groups()
                    # Try to parse date (assume current year)
                    try:
                        date = datetime.strptime(date_str + ' 2025', '%b%d %Y').strftime('%Y-%m-%d')
                    except Exception:
                        date = date_str
                    events.append({
                        'name': name,
                        'date': date,
                        'location': 'Grand Bazaar NYC, 100 W 77th St, Manhattan',
                        'link': url,
                        'source': 'Grand Bazaar NYC'
                    })
    # Add recurring event (every Sunday)
    events.append({
        'name': 'Grand Bazaar NYC Weekly Market',
        'date': 'Every Sunday',
        'location': 'Grand Bazaar NYC, 100 W 77th St, Manhattan',
        'link': url,
        'source': 'Grand Bazaar NYC'
    })
    return events

# 2. New Yorkled Events Calendar (template)
def scrape_new_yorkled():
    url = "https://www.newyorkled.com/new-york-city-events-listings-calendar/"
    # TODO: Implement scraping logic for this site
    return []

# 3. NYC Tourism Annual Events (template)
def scrape_nyc_tourism():
    url = "https://www.nyctourism.com/annual-events/"
    # TODO: Implement scraping logic for this site
    return []

def scrape_all_street_fairs():
    events = []
    events.extend(scrape_grand_bazaar_nyc())
    events.extend(scrape_new_yorkled())
    events.extend(scrape_nyc_tourism())
    return events

if __name__ == "__main__":
    all_events = scrape_all_street_fairs()
    for event in all_events:
        print(event)
    if all_events:
        upload = input("\nUpload these events to Firestore? (y/n): ").strip().lower()
        if upload == 'y':
            save_events_to_firestore(all_events, source="nyc_street_fairs")
        else:
            print("Events not uploaded.") 