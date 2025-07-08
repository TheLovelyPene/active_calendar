import requests
from bs4 import BeautifulSoup
from event_automation.firestore_utils import save_events_to_firestore
from datetime import datetime

EVENTBRITE_URL = "https://www.eventbrite.com/d/ny--new-york/free--events/"


def scrape_eventbrite_events():
    """
    Scrape free NYC events from Eventbrite and return a list of event dicts:
    [{ 'name': ..., 'date': ..., 'location': ..., 'link': ... }, ...]
    """
    events = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(EVENTBRITE_URL, headers=headers)
    print(response.status_code)
    print(response.text[:500])
    if response.status_code != 200:
        print(f"Failed to fetch Eventbrite page: {response.status_code}")
        return events
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find event cards (structure may change, so this is a best guess)
    for card in soup.find_all('div', class_='eds-event-card-content__content__principal'):  # type: ignore
        name_tag = card.find('div', class_='eds-event-card-content__title')  # type: ignore
        name = name_tag.text.strip() if name_tag else None
        link_tag = card.find('a', href=True)  # type: ignore
        link = link_tag.get('href') if link_tag and hasattr(link_tag, 'get') else None  # type: ignore
        date_tag = card.find('div', class_='eds-text-bs--fixed')  # type: ignore
        date = date_tag.text.strip() if date_tag else None
        location_tag = card.find('div', class_='card-text--truncated__one')  # type: ignore
        location = location_tag.text.strip() if location_tag else None
        if name and date:
            events.append({
                'name': name,
                'date': date,
                'location': location,
                'link': link
            })
    return events

if __name__ == "__main__":
    events = scrape_eventbrite_events()
    for event in events:
        print(event)
    if events:
        upload = input("\nUpload these events to Firestore? (y/n): ").strip().lower()
        if upload == 'y':
            save_events_to_firestore(events, source="eventbrite.com")
        else:
            print("Events not uploaded.") 