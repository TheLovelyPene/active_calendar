import firebase_admin
from firebase_admin import credentials, firestore
import hashlib
from datetime import datetime

# Initialize Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def generate_event_id(event):
    """Generate a unique ID for each event based on its content"""
    unique_string = f"{event['name']}_{event['date']}_{event['time']}_{event['address']}"
    return hashlib.md5(unique_string.encode()).hexdigest()

# New events from August to December 2025
new_events = [
    # --- NYC Events ---
    {
        "name": "SummerStage: Hip-Hop Appreciation Park Jam and Barbecue Curated by Doug E. Fresh and Funk Flex",
        "date": "2025-08-01",
        "time": "5:00 PM",
        "address": "Crotona Park (Crotona Park N, Bronx, NY 10457)",
        "borough": "Bronx",
        "link": "https://www.summerstage.org/"
    },
    {
        "name": "Newark First Fridays",
        "date": "2025-08-01",
        "time": "6:00 PM - 10:00 PM",
        "address": "Express Newark, 54 Halsey Street, Newark, NJ 07102",
        "borough": "Newark, NJ",
        "link": "https://www.newarkhappening.com/event/newark-first-fridays-2025/"
    },
    {
        "name": "SummerStage: Taiwanese Waves: Bulareyaung Dance Company / ABAO + Nanguaq Girls / Enno Cheng",
        "date": "2025-08-03",
        "time": "5:00 PM",
        "address": "Central Park (Rumsey Playfield, East 72nd Street, NYC)",
        "borough": "Manhattan",
        "link": "https://www.summerstage.org/"
    },
    {
        "name": "Music Mondays at Springwood Park: The Sounds of Sandstorm",
        "date": "2025-08-04",
        "time": "6:00 PM",
        "address": "Springwood Park, Asbury Park, NJ",
        "borough": "Asbury Park, NJ",
        "link": "https://asburyparkchamber.com/events/"
    },
    {
        "name": "AP Live: Indigo Sky | Emerson Woolf & The Wishbones",
        "date": "2025-08-06",
        "time": "7:00 PM - 10:00 PM",
        "address": "First Avenue Green, next to MOGO Korean Fusion Tacos and Watermark on the Asbury Park Boardwalk, Asbury Park, NJ",
        "borough": "Asbury Park, NJ",
        "link": "https://www.newjerseystage.com/articles2/2025/06/17/asbury-park-music-foundation-launches-summer-music-season-featuring-free-concerts-across-the-city/"
    },
    {
        "name": "SummerStage: Tony Vega / La Excelencia / Ariacne Trujilo",
        "date": "2025-08-08",
        "time": "5:00 PM",
        "address": "Coney Island Amphitheater (Boardwalk West, Brooklyn, NY 11224)",
        "borough": "Brooklyn",
        "link": "https://www.summerstage.org/"
    },
    {
        "name": "Jersey City Night Market",
        "date": "2025-08-11",
        "time": "3:00 PM - 9:00 PM",
        "address": "City Hall Ancillary Lot, 179 Montgomery Street, Jersey City, NJ",
        "borough": "Jersey City, NJ",
        "link": "https://www.midnightmarketevents.com/jcnightmarket"
    },
    {
        "name": "Music Mondays at Springwood Park: TBA",
        "date": "2025-08-11",
        "time": "6:00 PM",
        "address": "Springwood Park, Asbury Park, NJ",
        "borough": "Asbury Park, NJ",
        "link": "https://asburyparkchamber.com/events/"
    },
    {
        "name": "AP Live: October Man | Great Oblivion",
        "date": "2025-08-12",
        "time": "7:00 PM - 10:00 PM",
        "address": "First Avenue Green, next to MOGO Korean Fusion Tacos and Watermark on the Asbury Park Boardwalk, Asbury Park, NJ",
        "borough": "Asbury Park, NJ",
        "link": "https://www.newjerseystage.com/articles2/2025/06/17/asbury-park-music-foundation-launches-summer-music-season-featuring-free-concerts-across-the-city/"
    },
    {
        "name": "Rooftop Outdoor Movies: Crazy, Stupid, Love",
        "date": "2025-08-15",
        "time": "8:00 PM",
        "address": "The Asbury Hotel Rooftop, 210 Fifth Ave, Asbury Park, NJ 07712",
        "borough": "Asbury Park, NJ",
        "link": "https://www.eventbrite.com/e/crazy-stupid-love-tickets-1388661898119"
    },
    {
        "name": "SummerStage: Blacktronica Festival",
        "date": "2025-08-17",
        "time": "5:00 PM",
        "address": "Marcus Garvey Park (18 Mount Morris Park West, New York, NY 10027)",
        "borough": "Manhattan",
        "link": "https://www.summerstage.org/"
    },
    {
        "name": "Jersey City Night Market",
        "date": "2025-08-17",
        "time": "3:00 PM - 9:00 PM",
        "address": "City Hall Ancillary Lot, 179 Montgomery Street, Jersey City, NJ",
        "borough": "Jersey City, NJ",
        "link": "https://www.midnightmarketevents.com/jcnightmarket"
    },
    {
        "name": "Music Mondays at Springwood Park: Ms. G & Da Guyz | Kuf Knotz & Christine Elise",
        "date": "2025-08-18",
        "time": "6:00 PM",
        "address": "Springwood Park, Asbury Park, NJ",
        "borough": "Asbury Park, NJ",
        "link": "https://asburyparkchamber.com/events/"
    },
    {
        "name": "AP Live: Mike Frank & Friends | Foes of Fern",
        "date": "2025-08-20",
        "time": "7:00 PM - 10:00 PM",
        "address": "First Avenue Green, next to MOGO Korean Fusion Tacos and Watermark on the Asbury Park Boardwalk, Asbury Park, NJ",
        "borough": "Asbury Park, NJ",
        "link": "https://www.newjerseystage.com/articles2/2025/06/17/asbury-park-music-foundation-launches-summer-music-season-featuring-free-concerts-across-the-city/"
    },
    {
        "name": "Riverside Park Conservancy's Summer on the Hudson: Vinyl Nights",
        "date": "2025-08-23",
        "time": "7:00 PM",
        "address": "Pier I at 70th Street, NYC",
        "borough": "Manhattan",
        "link": "https://riversideparknyc.org/announcing-soh-2025/"
    },
    {
        "name": "Music Mondays at Springwood Park: The Sensational Soul Cruisers",
        "date": "2025-08-26",
        "time": "6:00 PM",
        "address": "Springwood Park, Asbury Park, NJ",
        "borough": "Asbury Park, NJ",
        "link": "https://asburyparkchamber.com/events/"
    },
    {
        "name": "SummerStage: Morgan Freeman's Symphonic Blues",
        "date": "2025-08-27",
        "time": "5:00 PM",
        "address": "Herbert Von King Park (670 Lafayette Ave, Brooklyn, NY 11216)",
        "borough": "Brooklyn",
        "link": "https://www.summerstage.org/"
    },
    {
        "name": "AP Live: Alors Alors | S0ulfood | Des & The Swagmatics",
        "date": "2025-08-28",
        "time": "7:00 PM - 10:00 PM",
        "address": "First Avenue Green, next to MOGO Korean Fusion Tacos and Watermark on the Asbury Park Boardwalk, Asbury Park, NJ",
        "borough": "Asbury Park, NJ",
        "link": "https://www.newjerseystage.com/articles2/2025/06/17/asbury-park-music-foundation-launches-summer-music-season-featuring-free-concerts-across-the-city/"
    },
    {
        "name": "Riverside Park Conservancy's Summer on the Hudson: Riverside Comedy Club",
        "date": "2025-08-29",
        "time": "8:00 PM",
        "address": "Pier I at 70th Street, NYC",
        "borough": "Manhattan",
        "link": "https://riversideparknyc.org/announcing-soh-2025/"
    },
    {
        "name": "Riverside Park Conservancy's Summer on the Hudson: Sketch Jam",
        "date": "2025-08-30",
        "time": "11:00 AM - 1:00 PM",
        "address": "Sakura Park (122nd St.), NYC",
        "borough": "Manhattan",
        "link": "https://riversideparknyc.org/announcing-soh-2025/"
    },
    {
        "name": "NYC Parks Kids in Motion at Gertrude Ederle Playground",
        "date": "2025-08-30",
        "time": "10:00 AM - 6:00 PM",
        "address": "Between 59th Street and 60th Street and Amsterdam Avenue and West End Avenue, Manhattan, NYC",
        "borough": "Manhattan",
        "link": "https://www.nycgovparks.org/events/"
    },
    {
        "name": "Newark First Fridays",
        "date": "2025-09-05",
        "time": "6:00 PM - 10:00 PM",
        "address": "Express Newark, 54 Halsey Street, Newark, NJ 07102",
        "borough": "Newark, NJ",
        "link": "https://www.newarkhappening.com/event/newark-first-fridays-2025/"
    },
    {
        "name": "Riverside Park Conservancy's Summer on the Hudson: West Side County Fair",
        "date": "2025-09-07",
        "time": "1:00 PM - 6:00 PM",
        "address": "Pier I at 70th Street, NYC",
        "borough": "Manhattan",
        "link": "https://riversideparknyc.org/announcing-soh-2025/"
    },
    {
        "name": "Riverside Park Conservancy's Summer on the Hudson: Sketch Jam",
        "date": "2025-09-13",
        "time": "11:00 AM - 1:00 PM",
        "address": "72nd St., NYC",
        "borough": "Manhattan",
        "link": "https://riversideparknyc.org/announcing-soh-2025/"
    },
    {
        "name": "Jersey City Night Market",
        "date": "2025-09-21",
        "time": "3:00 PM - 9:00 PM",
        "address": "City Hall Ancillary Lot, 179 Montgomery Street, Jersey City, NJ",
        "borough": "Jersey City, NJ",
        "link": "https://www.midnightmarketevents.com/jcnightmarket"
    },
    {
        "name": "Asbury Park Bazaar - Fall Bazaar",
        "date": "2025-09-27",
        "time": "12:00 PM - 5:00 PM",
        "address": "Grand Arcade at Historic Convention Hall, 1300 Ocean Ave, Asbury Park, NJ 07712",
        "borough": "Asbury Park, NJ",
        "link": "https://www.asburyparkbazaar.com/asbury-park-fall-bazaar-application-2025"
    },
    {
        "name": "Asbury Park Bazaar - Fall Bazaar",
        "date": "2025-09-28",
        "time": "12:00 PM - 5:00 PM",
        "address": "Grand Arcade at Historic Convention Hall, 1300 Ocean Ave, Asbury Park, NJ 07712",
        "borough": "Asbury Park, NJ",
        "link": "https://www.asburyparkbazaar.com/asbury-park-fall-bazaar-application-2025"
    },
    {
        "name": "Newark First Fridays",
        "date": "2025-10-03",
        "time": "6:00 PM - 10:00 PM",
        "address": "Express Newark, 54 Halsey Street, Newark, NJ 07102",
        "borough": "Newark, NJ",
        "link": "https://www.newarkhappening.com/event/newark-first-fridays-2025/"
    },
    {
        "name": "JCAST Handmade Market (HDSID Handmade Market)",
        "date": "2025-10-04",
        "time": "12:00 PM - 6:00 PM",
        "address": "Grove PATH Plaza, 87 Newark Ave, Jersey City, NJ",
        "borough": "Jersey City, NJ",
        "link": "https://newjersey.news12.com/pages/new-jersey-events#!/details/jcast-handmade-market/14281393/2025-10-04T12"
    },
    {
        "name": "JCAST Handmade Market (HDSID Handmade Market)",
        "date": "2025-10-05",
        "time": "12:00 PM - 6:00 PM",
        "address": "Grove PATH Plaza, 87 Newark Ave, Jersey City, NJ",
        "borough": "Jersey City, NJ",
        "link": "https://newjersey.news12.com/pages/new-jersey-events#!/details/jcast-handmade-market/14281393/2025-10-04T12"
    },
    {
        "name": "Jersey City Night Market",
        "date": "2025-10-05",
        "time": "3:00 PM - 9:00 PM",
        "address": "City Hall Ancillary Lot, 179 Montgomery Street, Jersey City, NJ",
        "borough": "Jersey City, NJ",
        "link": "https://www.midnightmarketevents.com/jcnightmarket"
    },
    {
        "name": "Jersey City Night Market",
        "date": "2025-10-19",
        "time": "3:00 PM - 9:00 PM",
        "address": "City Hall Ancillary Lot, 179 Montgomery Street, Jersey City, NJ",
        "borough": "Jersey City, NJ",
        "link": "https://www.midnightmarketevents.com/jcnightmarket"
    },
    {
        "name": "Newark First Fridays",
        "date": "2025-11-07",
        "time": "6:00 PM - 10:00 PM",
        "address": "Express Newark, 54 Halsey Street, Newark, NJ 07102",
        "borough": "Newark, NJ",
        "link": "https://www.newarkhappening.com/event/newark-first-fridays-2025/"
    },
    {
        "name": "Rockefeller Center Christmas Tree Lighting",
        "date": "2025-12-03",
        "time": "Evening (exact time TBA)",
        "address": "Rockefeller Plaza, NYC",
        "borough": "Manhattan",
        "link": "https://www.rockefellercenter.com/attractions/tree-lighting/"
    },
    {
        "name": "Newark First Fridays",
        "date": "2025-12-05",
        "time": "6:00 PM - 10:00 PM",
        "address": "Express Newark, 54 Halsey Street, Newark, NJ 07102",
        "borough": "Newark, NJ",
        "link": "https://www.newarkhappening.com/event/newark-first-fridays-2025/"
    }
]

def upload_new_events():
    """Upload all new events to Firestore"""
    print("=== Uploading August-December 2025 Events to Firestore ===")
    print()
    
    success_count = 0
    error_count = 0
    
    for event in new_events:
        try:
            # Generate unique ID
            event_id = generate_event_id(event)
            event["event_id"] = event_id
            event["uploaded_at"] = datetime.now()
            
            # Upload to Firestore
            events_ref = db.collection('events')
            events_ref.document(event_id).set(event)
            
            print(f"✅ Added: {event['name']} ({event['date']})")
            success_count += 1
            
        except Exception as e:
            print(f"❌ Error adding {event['name']}: {str(e)}")
            error_count += 1
    
    print(f"\n=== Upload Complete ===")
    print(f"Successfully uploaded: {success_count} events")
    print(f"Errors: {error_count} events")

if __name__ == "__main__":
    upload_new_events() 