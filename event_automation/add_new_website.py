"""
Template for adding new websites to the NYC Events Scraper
Copy this template and modify it for each new website you want to scrape.
"""

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

def scrape_new_website():
    """
    Template function for scraping a new website.
    Replace 'new_website' with the actual website name.
    """
    print("Scraping FREE events from new_website...")
    
    # Replace with the actual URL
    url = "https://example.com/events"
    
    # Headers to mimic a real browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Fetch the webpage
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse the HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        events = []
        
        # STEP 1: Find event containers
        # Look for HTML elements that contain event information
        # Common patterns: div with class containing 'event', 'card', 'item', etc.
        event_containers = soup.find_all('div', class_=re.compile(r'event|card|item|listing'))
        
        # Alternative: Look for specific HTML structure
        # event_containers = soup.find_all('article')  # If events are in <article> tags
        # event_containers = soup.find_all('li', class_='event-item')  # If events are in list items
        
        print(f"Found {len(event_containers)} potential event containers")
        
        for container in event_containers[:15]:  # Limit to first 15 for testing
            try:
                # STEP 2: Extract event name
                # Look for headings (h1-h6) or links that contain the event name
                name_elem = container.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']) or container.find('a')
                if name_elem:
                    name = name_elem.get_text(strip=True)
                else:
                    continue
                
                # STEP 3: Extract description (optional)
                desc_elem = container.find('p') or container.find('div', class_=re.compile(r'desc|summary|description'))
                description = desc_elem.get_text(strip=True) if desc_elem else ""
                
                # STEP 4: Check if it's a free event
                if not is_free_event(name, description):
                    continue
                
                # STEP 5: Extract date
                # Look for date patterns in the text
                date_elem = container.find(string=re.compile(r'\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2}'))
                date = date_elem.strip() if date_elem else "2025-07-01"
                
                # STEP 6: Extract time
                time_elem = container.find(string=re.compile(r'\d{1,2}:\d{2}\s*(AM|PM|am|pm)'))
                time = time_elem.strip() if time_elem else "TBD"
                
                # STEP 7: Extract location
                location_elem = container.find(string=re.compile(r'New York|NYC|Manhattan|Brooklyn|Queens|Bronx|Staten Island'))
                address = location_elem.strip() if location_elem else "New York, NY"
                
                # STEP 8: Determine borough
                borough = determine_borough(address)
                
                # STEP 9: Extract link
                link_elem = container.find('a')
                link = link_elem.get('href') if link_elem else ""
                if link and not link.startswith('http'):
                    link = "https://example.com" + link  # Replace with actual domain
                
                # STEP 10: Create event object
                event = {
                    "name": name,
                    "date": date,
                    "time": time,
                    "address": address,
                    "borough": borough,
                    "link": link,
                    "source": "new_website",  # Replace with actual website name
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
        print(f"Error scraping new_website: {str(e)}")
        return []

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

def determine_borough(address):
    """Determine borough based on address"""
    address_lower = address.lower()
    
    if "brooklyn" in address_lower:
        return "Brooklyn"
    elif "queens" in address_lower:
        return "Queens"
    elif "bronx" in address_lower:
        return "The Bronx"
    elif "staten island" in address_lower:
        return "Staten Island"
    elif "asbury park" in address_lower:
        return "Asbury Park, NJ"
    else:
        return "Manhattan"  # Default

# Example usage and testing
if __name__ == "__main__":
    print("=== Website Scraper Template ===")
    print("This is a template for adding new websites to scrape.")
    print("Copy this file and modify it for each new website.")
    print()
    print("Steps to add a new website:")
    print("1. Copy this template file")
    print("2. Rename the function (e.g., scrape_eventbrite())")
    print("3. Update the URL")
    print("4. Modify the HTML selectors to match the website structure")
    print("5. Test the scraper")
    print("6. Add it to the main scrape_events.py file")
    print()
    print("Common HTML patterns to look for:")
    print("- Event containers: div, article, li with classes like 'event', 'card', 'item'")
    print("- Event names: h1-h6 tags, or a tags")
    print("- Dates: text containing date patterns")
    print("- Times: text containing time patterns")
    print("- Locations: text containing NYC borough names")
    print("- Links: a tags with href attributes") 