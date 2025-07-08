import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, firestore
import hashlib
from datetime import datetime
import re
import time
import json

# Initialize Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def generate_event_id(event):
    """Generate a unique ID for each event based on its content"""
    unique_string = f"{event['name']}_{event['date']}_{event['time']}_{event['address']}"
    return hashlib.md5(unique_string.encode()).hexdigest()

def is_free_event(name, description=""):
    """Check if an event is likely free based on name and description"""
    text = (name + " " + description).lower()
    
    # Keywords that indicate FREE events
    free_keywords = [
        'free', 'no cost', 'no charge', 'complimentary', 'gratis', 
        'free admission', 'free entry', 'free event', 'free concert',
        'free festival', 'free fair', 'free workshop', 'free class',
        'free movie', 'free screening', 'free performance', 'free show',
        'free exhibition', 'free art', 'free music', 'free dance',
        'free yoga', 'free fitness', 'free workshop', 'free seminar',
        'free lecture', 'free talk', 'free reading', 'free book',
        'free food', 'free tasting', 'free sample', 'free giveaway',
        'free market', 'free bazaar', 'free flea market', 'free sale',
        'donation', 'pay what you wish', 'suggested donation'
    ]
    
    # Keywords that indicate PAID events (exclude these)
    paid_keywords = [
        'ticket', 'tickets', 'buy', 'purchase', 'cost', 'price', 'fee',
        'admission', 'entry fee', 'cover charge', 'door charge',
        '$', 'dollars', 'cash only', 'credit card', 'payment required',
        'reservation required', 'booking fee', 'service charge',
        'premium', 'vip', 'exclusive', 'members only', 'subscription'
    ]
    
    # Check for free keywords
    has_free = any(keyword in text for keyword in free_keywords)
    
    # Check for paid keywords
    has_paid = any(keyword in text for keyword in paid_keywords)
    
    # If it has paid keywords but no free keywords, exclude it
    if has_paid and not has_free:
        return False
    
    # If it has free keywords, include it
    if has_free:
        return True
    
    # For events without clear indicators, be conservative and exclude
    return False

def scrape_allevents_in():
    """Scrape FREE events from allevents.in"""
    print("Scraping FREE events from allevents.in...")
    
    url = "https://allevents.in/new-york/free"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        events = []
        
        # Look for event cards/containers
        event_containers = soup.find_all('div', class_=re.compile(r'event|card|item'))
        
        for container in event_containers[:15]:  # Check more events
            try:
                # Extract event name
                name_elem = container.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']) or container.find('a')
                if name_elem:
                    name = name_elem.get_text(strip=True)
                else:
                    continue
                
                # Extract description
                desc_elem = container.find('p') or container.find('div', class_=re.compile(r'desc|summary'))
                description = desc_elem.get_text(strip=True) if desc_elem else ""
                
                # Check if it's a free event
                if not is_free_event(name, description):
                    continue
                
                # Extract date (this is a simplified version)
                date_elem = container.find(string=re.compile(r'\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2}'))
                date = date_elem.strip() if date_elem else "2025-07-01"
                
                # Extract time
                time_elem = container.find(string=re.compile(r'\d{1,2}:\d{2}\s*(AM|PM|am|pm)'))
                time = time_elem.strip() if time_elem else "TBD"
                
                # Extract location
                location_elem = container.find(string=re.compile(r'New York|NYC|Manhattan|Brooklyn|Queens|Bronx|Staten Island'))
                address = location_elem.strip() if location_elem else "New York, NY"
                
                # Determine borough based on address
                borough = "Manhattan"  # Default
                if "Brooklyn" in address:
                    borough = "Brooklyn"
                elif "Queens" in address:
                    borough = "Queens"
                elif "Bronx" in address:
                    borough = "The Bronx"
                elif "Staten Island" in address:
                    borough = "Staten Island"
                
                # Extract link
                link_elem = container.find('a')
                link = link_elem.get('href') if link_elem else ""
                if link and not link.startswith('http'):
                    link = "https://allevents.in" + link
                
                event = {
                    "name": name,
                    "date": date,
                    "time": time,
                    "address": address,
                    "borough": borough,
                    "link": link,
                    "source": "allevents.in",
                    "scraped_at": datetime.now(),
                    "is_free": True
                }
                
                events.append(event)
                print(f"Found FREE event: {name}")
                
            except Exception as e:
                print(f"Error parsing event: {str(e)}")
                continue
        
        return events
        
    except Exception as e:
        print(f"Error scraping allevents.in: {str(e)}")
        return []

def scrape_timeout_nyc():
    """Scrape FREE events from timeout.com/newyork"""
    print("Scraping FREE events from timeout.com/newyork...")
    
    url = "https://www.timeout.com/newyork/things-to-do/free-things-to-do-in-nyc"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        events = []
        
        # Look for event articles or cards
        event_containers = soup.find_all(['article', 'div'], class_=re.compile(r'article|card|event'))
        
        for container in event_containers[:15]:  # Check more events
            try:
                # Extract event name
                name_elem = container.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                if name_elem:
                    name = name_elem.get_text(strip=True)
                else:
                    continue
                
                # Extract description
                desc_elem = container.find('p') or container.find('div', class_=re.compile(r'desc|summary'))
                description = desc_elem.get_text(strip=True) if desc_elem else ""
                
                # Check if it's a free event
                if not is_free_event(name, description):
                    continue
                
                # Extract date (simplified)
                date = "2025-07-01"  # Default date
                
                # Extract time
                time = "TBD"
                
                # Extract location
                address = "New York, NY"
                
                # Determine borough
                borough = "Manhattan"
                
                # Extract link
                link_elem = container.find('a')
                link = link_elem.get('href') if link_elem else ""
                if link and not link.startswith('http'):
                    link = "https://www.timeout.com" + link
                
                event = {
                    "name": name,
                    "date": date,
                    "time": time,
                    "address": address,
                    "borough": borough,
                    "link": link,
                    "source": "timeout.com",
                    "scraped_at": datetime.now(),
                    "is_free": True
                }
                
                events.append(event)
                print(f"Found FREE event: {name}")
                
            except Exception as e:
                print(f"Error parsing event: {str(e)}")
                continue
        
        return events
        
    except Exception as e:
        print(f"Error scraping timeout.com: {str(e)}")
        return []

def scrape_nycgovparks():
    """Scrape FREE events from NYC Parks"""
    print("Scraping FREE events from NYC Parks...")
    
    url = "https://www.nycgovparks.org/events"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        events = []
        
        # Look for event listings
        event_containers = soup.find_all(['div', 'article'], class_=re.compile(r'event|listing|item'))
        
        for container in event_containers[:10]:
            try:
                # Extract event name
                name_elem = container.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                if name_elem:
                    name = name_elem.get_text(strip=True)
                else:
                    continue
                
                # NYC Parks events are typically free
                if not is_free_event(name):
                    continue
                
                # Extract date
                date = "2025-07-01"  # Default
                
                # Extract time
                time = "TBD"
                
                # Extract location
                address = "NYC Parks Location"
                
                # Determine borough
                borough = "Manhattan"
                
                # Extract link
                link_elem = container.find('a')
                link = link_elem.get('href') if link_elem else ""
                if link and not link.startswith('http'):
                    link = "https://www.nycgovparks.org" + link
                
                event = {
                    "name": name,
                    "date": date,
                    "time": time,
                    "address": address,
                    "borough": borough,
                    "link": link,
                    "source": "nycgovparks.org",
                    "scraped_at": datetime.now(),
                    "is_free": True
                }
                
                events.append(event)
                print(f"Found FREE event: {name}")
                
            except Exception as e:
                print(f"Error parsing event: {str(e)}")
                continue
        
        return events
        
    except Exception as e:
        print(f"Error scraping nycgovparks.org: {str(e)}")
        return []

def scrape_bryantpark():
    """Scrape FREE events from Bryant Park"""
    print("Scraping FREE events from Bryant Park...")
    
    url = "https://bryantpark.org/activities"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        events = []
        
        # Look for event listings
        event_containers = soup.find_all(['div', 'article'], class_=re.compile(r'event|activity|item'))
        
        for container in event_containers[:10]:
            try:
                # Extract event name
                name_elem = container.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                if name_elem:
                    name = name_elem.get_text(strip=True)
                else:
                    continue
                
                # Bryant Park events are typically free
                if not is_free_event(name):
                    continue
                
                # Extract date
                date = "2025-07-01"  # Default
                
                # Extract time
                time = "TBD"
                
                # Extract location
                address = "Bryant Park, Manhattan"
                
                # Determine borough
                borough = "Manhattan"
                
                # Extract link
                link_elem = container.find('a')
                link = link_elem.get('href') if link_elem else ""
                if link and not link.startswith('http'):
                    link = "https://bryantpark.org" + link
                
                event = {
                    "name": name,
                    "date": date,
                    "time": time,
                    "address": address,
                    "borough": borough,
                    "link": link,
                    "source": "bryantpark.org",
                    "scraped_at": datetime.now(),
                    "is_free": True
                }
                
                events.append(event)
                print(f"Found FREE event: {name}")
                
            except Exception as e:
                print(f"Error parsing event: {str(e)}")
                continue
        
        return events
        
    except Exception as e:
        print(f"Error scraping bryantpark.org: {str(e)}")
        return []

def save_events_to_firestore(events):
    """Save scraped events to Firestore"""
    print(f"Saving {len(events)} FREE events to Firestore...")
    
    events_ref = db.collection('events')
    saved_count = 0
    duplicate_count = 0
    
    for event in events:
        try:
            # Generate unique ID
            event_id = generate_event_id(event)
            event["event_id"] = event_id
            
            # Check if event already exists
            existing_doc = events_ref.document(event_id).get()
            
            if existing_doc.exists:
                print(f"Event already exists: {event['name']}")
                duplicate_count += 1
                continue
            
            # Save to Firestore
            events_ref.document(event_id).set(event)
            print(f"✅ Saved FREE event: {event['name']} (from {event['source']})")
            saved_count += 1
            
            # Small delay to avoid overwhelming the database
            time.sleep(0.1)
            
        except Exception as e:
            print(f"❌ Error saving event {event['name']}: {str(e)}")
    
    print(f"\n📊 Summary:")
    print(f"   New FREE events saved: {saved_count}")
    print(f"   Duplicates skipped: {duplicate_count}")
    print(f"   Total processed: {len(events)}")

def main():
    print("=== NYC FREE Events Web Scraper ===")
    print("This script will scrape FREE events from multiple websites and save them to Firestore.")
    print()
    
    # Scrape from different sources
    all_events = []
    
    # Scrape from allevents.in
    allevents_events = scrape_allevents_in()
    all_events.extend(allevents_events)
    print(f"Found {len(allevents_events)} FREE events from allevents.in")
    
    # Scrape from timeout.com
    timeout_events = scrape_timeout_nyc()
    all_events.extend(timeout_events)
    print(f"Found {len(timeout_events)} FREE events from timeout.com")
    
    # Scrape from NYC Parks
    parks_events = scrape_nycgovparks()
    all_events.extend(parks_events)
    print(f"Found {len(parks_events)} FREE events from nycgovparks.org")
    
    # Scrape from Bryant Park
    bryant_events = scrape_bryantpark()
    all_events.extend(bryant_events)
    print(f"Found {len(bryant_events)} FREE events from bryantpark.org")
    
    print(f"\nTotal FREE events found: {len(all_events)}")
    
    if all_events:
        # Ask user if they want to save events
        save_choice = input("\nSave these FREE events to Firestore? (y/n): ").strip().lower()
        
        if save_choice == 'y':
            save_events_to_firestore(all_events)
        else:
            print("Events not saved.")
    else:
        print("No FREE events found to save.")

if __name__ == "__main__":
    main() 