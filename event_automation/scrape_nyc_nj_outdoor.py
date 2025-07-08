import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from event_automation.firestore_utils import save_events_to_firestore
from datetime import datetime

# 1. NYC Parks Free Events (fully implemented example)
def scrape_nyc_parks():
    url = "https://www.nycgovparks.org/events/f2025-07-08/t2025-12-31/free"
    headers = {'User-Agent': 'Mozilla/5.0'}
    events = []
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch NYC Parks: {response.status_code}")
        return events
    soup = BeautifulSoup(response.text, 'html.parser')
    # Example: Find event listings by class
    for event_div in soup.find_all('div', class_='event-list-item'):  # type: ignore
        name_tag = event_div.find('h3')  # type: ignore
        name = name_tag.text.strip() if isinstance(name_tag, Tag) else None
        date_tag = event_div.find('span', class_='date')  # type: ignore
        date = date_tag.text.strip() if isinstance(date_tag, Tag) else None
        location_tag = event_div.find('span', class_='location')  # type: ignore
        location = location_tag.text.strip() if isinstance(location_tag, Tag) else None
        link_tag = event_div.find('a', href=True)  # type: ignore
        link = link_tag.get('href') if link_tag and hasattr(link_tag, 'get') else None  # type: ignore
        if isinstance(link, str) and not link.startswith('http'):
            link = 'https://www.nycgovparks.org' + link
        if name and date:
            events.append({
                'name': name,
                'date': date,
                'location': location,
                'link': link,
                'source': 'nycgovparks.org'
            })
    return events

# 2. NY State Parks Events (template)
def scrape_ny_state_parks():
    url = "https://parks.ny.gov/events/event-results.aspx?sdt=07%2f08%2f2025&edt=12%2f31%2f2025&lct=0&r=12"
    # TODO: Implement scraping logic for this site
    return []

# 3. Sierra Club NJ Outings (template, free events only)
def scrape_sierra_club_nj():
    url = "https://www.sierraclub.org/new-jersey/upcoming-outings"
    # TODO: Implement scraping logic for this site (free events only)
    return []

def scrape_all_outdoor_events():
    events = []
    events.extend(scrape_nyc_parks())
    events.extend(scrape_ny_state_parks())
    events.extend(scrape_sierra_club_nj())
    return events

if __name__ == "__main__":
    all_events = scrape_all_outdoor_events()
    for event in all_events:
        print(event)
    if all_events:
        upload = input("\nUpload these events to Firestore? (y/n): ").strip().lower()
        if upload == 'y':
            save_events_to_firestore(all_events, source="nyc_nj_outdoor")
        else:
            print("Events not uploaded.") 