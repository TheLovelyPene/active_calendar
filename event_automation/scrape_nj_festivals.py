import requests
from bs4 import BeautifulSoup
from event_automation.firestore_utils import save_events_to_firestore
from datetime import datetime

# 1. New Jersey Isn't Boring (fully implemented example for free events)
def scrape_newjerseyisntboring():
    url = "https://newjerseyisntboring.com/njibs-guide-to-70-new-jersey-july-festivals-and-events/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    events = []
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch New Jersey Isn't Boring: {response.status_code}")
        return events
    soup = BeautifulSoup(response.text, 'html.parser')
    # Example: Find all bolded event names and their following text for date/location
    for strong in soup.find_all('strong'):
        name = strong.get_text(strip=True)
        # Only include if 'free' in the event name or nearby text
        if isinstance(name, str) and 'free' in name.lower():
            # Try to get the next sibling for date/location
            date = None
            location = None
            next_elem = strong.find_next_sibling(text=True)  # type: ignore
            if isinstance(next_elem, str):
                date = next_elem.strip()
            events.append({
                'name': name,
                'date': date or 'TBD',
                'location': location or 'New Jersey',
                'link': url,
                'source': "newjerseyisntboring.com"
            })
    return events

# 2. Visit NJ Events (template, Asbury Park, Jersey City, Newark only)
def scrape_visitnj():
    url = "https://visitnj.org/nj/events"
    # TODO: Implement scraping logic for this site (filter for Asbury Park, Jersey City, Newark)
    return []

# 3. Jersey City Culture Events Calendar (template)
def scrape_jerseycityculture():
    url = "https://jerseycityculture.org/events-calendar/"
    # TODO: Implement scraping logic for this site
    return []

def scrape_all_nj_festivals():
    events = []
    events.extend(scrape_newjerseyisntboring())
    events.extend(scrape_visitnj())
    events.extend(scrape_jerseycityculture())
    return events

if __name__ == "__main__":
    all_events = scrape_all_nj_festivals()
    for event in all_events:
        print(event)
    if all_events:
        upload = input("\nUpload these events to Firestore? (y/n): ").strip().lower()
        if upload == 'y':
            save_events_to_firestore(all_events, source="nj_festivals")
        else:
            print("Events not uploaded.") 