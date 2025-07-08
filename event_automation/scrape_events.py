import sys
sys.path.append('..')  # Ensure parent dir is in path for import
from event_automation.firestore_utils import save_events_to_firestore
from scrape_nycforfree import scrape_nycforfree_events
from scrape_eventbrite import scrape_eventbrite_events
from event_automation.scrape_nj_festivals import scrape_all_nj_festivals
from event_automation.scrape_nyc_street_fairs import scrape_all_street_fairs
from event_automation.scrape_nyc_nj_outdoor import scrape_all_outdoor_events

def main():
    print("=== NYC & NJ Events Master Scraper ===")
    print("This script will scrape events from all sources and upload them to Firestore.")
    print()
    all_events = []

    # Scrape from nycforfree.co
    print("Scraping FREE events from nycforfree.co...")
    nycforfree_events = scrape_nycforfree_events()
    all_events.extend(nycforfree_events)
    print(f"Found {len(nycforfree_events)} events from nycforfree.co")

    # Scrape from Eventbrite
    print("Scraping FREE events from eventbrite.com...")
    eventbrite_events = scrape_eventbrite_events()
    all_events.extend(eventbrite_events)
    print(f"Found {len(eventbrite_events)} events from eventbrite.com")

    # Scrape from NJ festivals
    print("Scraping FREE events from NJ festivals...")
    nj_festivals_events = scrape_all_nj_festivals()
    all_events.extend(nj_festivals_events)
    print(f"Found {len(nj_festivals_events)} events from NJ festivals")

    # Scrape from NYC street fairs
    print("Scraping FREE events from NYC street fairs...")
    nyc_street_fairs_events = scrape_all_street_fairs()
    all_events.extend(nyc_street_fairs_events)
    print(f"Found {len(nyc_street_fairs_events)} events from NYC street fairs")

    # Scrape from NYC/NJ outdoor events
    print("Scraping FREE events from NYC/NJ outdoor events...")
    nyc_nj_outdoor_events = scrape_all_outdoor_events()
    all_events.extend(nyc_nj_outdoor_events)
    print(f"Found {len(nyc_nj_outdoor_events)} events from NYC/NJ outdoor events")

    print(f"\nTotal events found: {len(all_events)}")
    for event in all_events:
        print(event)

    if all_events:
        upload = input("\nUpload ALL these events to Firestore? (y/n): ").strip().lower()
        if upload == 'y':
            save_events_to_firestore(all_events, source="master_script")
        else:
            print("Events not uploaded.")
    else:
        print("No events found to upload.")

if __name__ == "__main__":
    main() 