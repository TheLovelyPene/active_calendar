import firebase_admin
from firebase_admin import credentials, firestore
import json
from datetime import datetime
import hashlib

# Initialize Firebase Admin SDK
# Make sure you have serviceAccountKey.json in this folder
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Your existing events data (copied from nyc_free_events_database_2.py)
nyc_free_events_database = [
    # --- Manhattan Events ---
    {
        "name": "Hudson River Park's Jazz at Pier 84",
        "date": "2025-07-02",
        "time": "7:00 PM – 8:30 PM",
        "address": "Hudson River Park's Pier 84, Manhattan",
        "borough": "Manhattan",
        "link": "https://www.nycgovparks.org/events/free_summer_concerts"
    },
    {
        "name": "NY Classical presents: All's Well That Ends Well",
        "date": "2025-07-02",
        "time": "7:00 PM – 9:00 PM",
        "address": "Castle Clinton (in The Battery), Manhattan",
        "borough": "Manhattan",
        "link": "https://www.nycgovparks.org/events/free_summer_concerts"
    },
    {
        "name": "NY Classical presents: All's Well That Ends Well",
        "date": "2025-07-06",
        "time": "7:00 PM – 9:00 PM",
        "address": "Castle Clinton (in The Battery), Manhattan",
        "borough": "Manhattan",
        "link": "https://www.nycgovparks.org/events/free_summer_concerts"
    },
    {
        "name": "New York Guitar Festival: Pedro Cortes Flamenco, Big Lazy, Marel Hidalgo",
        "date": "2025-07-03",
        "time": "7:00 PM",
        "address": "Bryant Park Stage, Manhattan",
        "borough": "Manhattan",
        "link": "https://bryantpark.org/activities/picnic-performances"
    },
    {
        "name": "New York Guitar Festival: Louis Cato, Jackie Venson, Jontavious Willis",
        "date": "2025-07-04",
        "time": "7:00 PM",
        "address": "Bryant Park Stage, Manhattan",
        "borough": "Manhattan",
        "link": "https://bryantpark.org/activities/picnic-performances"
    },
    {
        "name": "Macy's 4th of July Fireworks",
        "date": "2025-07-04",
        "time": "8:00 PM",
        "address": "East River (viewable from Manhattan, Brooklyn, and Queens waterfronts)",
        "borough": "Manhattan (Primary launch area)",
        "link": "https://www.timeout.com/newyork/events-calendar/july-events-calendar"
    },
    {
        "name": "East Village Street Fair",
        "date": "2025-07-05",
        "time": "10:00 AM",
        "address": "East Village (exact location TBD, likely main streets), Manhattan",
        "borough": "Manhattan",
        "link": "https://www.clubfreetime.com/new-york-city-nyc/free-fair/2025-07-05/event/688018"
    },
    {
        "name": "Taikoza Drumming Performance",
        "date": "2025-07-08",
        "time": "3:00 PM – 4:00 PM",
        "address": "Jackie Robinson Park - Bandshell, Manhattan",
        "borough": "Manhattan",
        "link": "https://www.nycgovparks.org/events/free_summer_concerts"
    },
    {
        "name": "Reading Rhythms at Hudson Yards",
        "date": "2025-07-08",
        "time": "TBD (likely daytime/evening)",
        "address": "Hudson Yards, Manhattan",
        "borough": "Manhattan",
        "link": "https://www.nycforfree.co/events"
    },
    {
        "name": "Carnegie Hall Citywide: Toomai String Quintet",
        "date": "2025-07-09",
        "time": "TBD (likely evening)",
        "address": "Madison Square Park, Manhattan",
        "borough": "Manhattan",
        "link": "https://www.carnegiehall.org/About/Press/Press-Releases/2025/04/15/Carnegie-Hall-Citywide-Announces-20252026-Season-with-Free-Performances-Across-NYC"
    },
    {
        "name": "River & Blues Concert Series (Maggie Rose)",
        "date": "2025-07-10",
        "time": "TBD (likely evening)",
        "address": "Rockefeller Park, Battery Park City, Manhattan",
        "borough": "Manhattan",
        "link": "https://secretnyc.co/free-summer-concerts-2025-full-list/"
    },
    {
        "name": "Carnegie Hall Citywide: The Knights with Julien Labro",
        "date": "2025-07-11",
        "time": "7:00 PM",
        "address": "Bryant Park Stage, Manhattan",
        "borough": "Manhattan",
        "link": "https://bryantpark.org/activities/picnic-performances"
    },
    {
        "name": "Manhattanhenge (Full Sun on Grid)",
        "date": "2025-07-11",
        "time": "8:20 PM ET",
        "address": "Viewable from 14th, 23rd, 34th, 42nd, 57th Streets (Manhattan)",
        "borough": "Manhattan",
        "link": "https://www.nycforfree.co/events/manhattanhenge-july-2025"
    },
    {
        "name": "Manhattanhenge (Half Sun on Grid)",
        "date": "2025-07-12",
        "time": "8:22 PM ET",
        "address": "Viewable from 14th, 23rd, 34th, 42nd, 57th Streets (Manhattan)",
        "borough": "Manhattan",
        "link": "https://www.nycforfree.co/events/manhattanhenge-july-2025"
    },
    {
        "name": "Carnegie Hall Citywide: Ziggy and Miles",
        "date": "2025-07-16",
        "time": "6:00 PM",
        "address": "Madison Square Park, Manhattan",
        "borough": "Manhattan",
        "link": "https://www.carnegiehall.org/About/Press/Press-Releases/2025/04/15/Carnegie-Hall-Citywide-Announces-20252026-Season-with-Free-Performances-Across-NYC"
    },
    {
        "name": "Hudson River Park's Jazz at Pier 84",
        "date": "2025-07-16",
        "time": "7:00 PM – 8:30 PM",
        "address": "Hudson River Park's Pier 84, Manhattan",
        "borough": "Manhattan",
        "link": "https://www.nycgovparks.org/events/free_summer_concerts"
    },
    {
        "name": "River & Blues Concert Series (Amythyst Kiah)",
        "date": "2025-07-17",
        "time": "TBD (likely evening)",
        "address": "Rockefeller Park, Battery Park City, Manhattan",
        "borough": "Manhattan",
        "link": "https://secretnyc.co/free-summer-concerts-2025-full-list/"
    },
    {
        "name": "Carnegie Hall Citywide: La Excelencia",
        "date": "2025-07-18",
        "time": "7:00 PM",
        "address": "Bryant Park Stage, Manhattan",
        "borough": "Manhattan",
        "link": "https://bryantpark.org/activities/picnic-performances"
    },
    {
        "name": "Carnegie Hall Citywide: Catalyst Quartet",
        "date": "2025-07-23",
        "time": "TBD (likely evening)",
        "address": "Madison Square Park, Manhattan",
        "borough": "Manhattan",
        "link": "https://www.carnegiehall.org/About/Press/Press-Releases/2025/04/15/Carnegie-Hall-Citywide-Announces-20252026-Season-with-Free-Performances-Across-NYC"
    },
    {
        "name": "River & Blues Concert Series (Afro Latin Jazz Orchestra)",
        "date": "2025-07-24",
        "time": "TBD (likely evening)",
        "address": "Rockefeller Park, Battery Park City, Manhattan",
        "borough": "Manhattan",
        "link": "https://secretnyc.co/free-summer-concerts-2025-full-list/"
    },
    {
        "name": "Carnegie Hall Citywide: Cécile McLorin Salvant",
        "date": "2025-07-25",
        "time": "7:00 PM",
        "address": "Bryant Park Stage, Manhattan",
        "borough": "Manhattan",
        "link": "https://bryantpark.org/activities/picnic-performances"
    },
    {
        "name": "Summer Streets NYC",
        "date": "2025-07-26",
        "time": "7:00 AM – 3:00 PM",
        "address": "Park Avenue & other car-free streets, Manhattan",
        "borough": "Manhattan",
        "link": "https://www.unlimitedbiking.com/blog/bike-events/summer-streets-nyc-2025-a-car%E2%80%91free-celebration-of-the-city/"
    },
    {
        "name": "Hudson River Park's Jazz at Pier 84",
        "date": "2025-07-30",
        "time": "7:00 PM – 8:30 PM",
        "address": "Hudson River Park's Pier 84, Manhattan",
        "borough": "Manhattan",
        "link": "https://www.nycgovparks.org/events/free_summer_concerts"
    },
    {
        "name": "River & Blues Concert Series (Lady Blackbird)",
        "date": "2025-07-31",
        "time": "TBD (likely evening)",
        "address": "Rockefeller Park, Battery Park City, Manhattan",
        "borough": "Manhattan",
        "link": "https://secretnyc.co/free-summer-concerts-2025-full-list/"
    },
    # --- Brooklyn Events ---
    {
        "name": "Nathan's Hot Dog Eating Contest",
        "date": "2025-07-04",
        "time": "TBD (morning/afternoon)",
        "address": "Nathan's Famous, 1310 Surf Ave, Coney Island, Brooklyn",
        "borough": "Brooklyn",
        "link": "https://www.iloveny.com/blog/post/things-to-do-this-july-in-new-york-state/"
    },
    {
        "name": "Flatbush Avenue Street Fair",
        "date": "2025-07-13",
        "time": "12:00 PM - 6:00 PM",
        "address": "Parkside Ave to Courtelyou Road, Flatbush, Brooklyn",
        "borough": "Brooklyn",
        "link": "https://brooklynbridgeparents.com/outdoor-festivals-and-street-fairs-in-brooklyn-in-2025/"
    },
    {
        "name": "Summer Market at Empire Stores in Dumbo",
        "date": "2025-07-12 to 2025-07-13",
        "time": "TBD (likely daytime)",
        "address": "Empire Stores, Dumbo, Brooklyn",
        "borough": "Brooklyn",
        "link": "https://www.timeout.com/newyork/events-calendar/july-events-calendar"
    },
    {
        "name": "BRIC Celebrate Brooklyn! (Still Woozy – Loveseat Tour)",
        "date": "2025-07-12",
        "time": "TBD (likely evening)",
        "address": "Lena Horne Bandshell (Prospect Park), Brooklyn",
        "borough": "Brooklyn",
        "link": "https://bricartsmedia.org/celebrate-brooklyn/"
    },
    {
        "name": "Park Pitch In: Lake Appreciation Month – Boathouse",
        "date": "2025-07-13",
        "time": "10:30 AM – 12:00 PM",
        "address": "Prospect Park Boathouse, 101 East Dr, Prospect Park, Brooklyn",
        "borough": "Brooklyn",
        "link": "https://www.reddit.com/r/nyc/comments/1li14mo/things-to-do-in-nyc-july-2025/"
    },
    {
        "name": "BRIC Celebrate Brooklyn! (Dinosaur Jr. & Snail Mail with Easy Action)",
        "date": "2025-07-17",
        "time": "TBD (likely evening)",
        "address": "Lena Horne Bandshell (Prospect Park), Brooklyn",
        "borough": "Brooklyn",
        "link": "https://bricartsmedia.org/celebrate-brooklyn/"
    },
    {
        "name": "Summer Stroll on Third Avenue",
        "date": "2025-07-18",
        "time": "6:00 PM - 10:00 PM",
        "address": "82nd Street to Marine Avenue, Bay Ridge, Brooklyn",
        "borough": "Brooklyn",
        "link": "https://brooklynbridgeparents.com/outdoor-festivals-and-street-fairs-in-brooklyn-in-2025/"
    },
    {
        "name": "BRIC Celebrate Brooklyn! (Men I Trust and strongboi)",
        "date": "2025-07-18",
        "time": "TBD (likely evening)",
        "address": "Lena Horne Bandshell (Prospect Park), Brooklyn",
        "borough": "Brooklyn",
        "link": "https://bricartsmedia.org/celebrate-brooklyn/"
    },
    {
        "name": "BRIC Celebrate Brooklyn! at Brower Park",
        "date": "2025-07-19",
        "time": "TBD (likely evening)",
        "address": "Brower Park, Brooklyn",
        "borough": "Brooklyn",
        "link": "https://bricartsmedia.org/celebrate-brooklyn/"
    },
    {
        "name": "Rise Up NYC Concert Series (Brooklyn Dates)",
        "date": "2025-07-19 to 2025-07-21",
        "time": "TBD (check link closer to date)",
        "address": "Venue details coming soon, Brooklyn",
        "borough": "Brooklyn",
        "link": "https://riseupnycconcerts.com/rise-up-nyc-2025-official-dates-announced-for-the-citys-biggest-free-concert-series/"
    },
    {
        "name": "Governors Island Market",
        "date": "2025-07-19 to 2025-07-20",
        "time": "TBD (likely daytime)",
        "address": "Governors Island (accessible via ferry from Manhattan or Brooklyn)",
        "borough": "Brooklyn (accessible, shared)",
        "link": "https://www.timeout.com/newyork/events-calendar/july-events-calendar"
    },
    {
        "name": "Summer Stroll on Third Avenue",
        "date": "2025-07-25",
        "time": "6:00 PM - 10:00 PM",
        "address": "68th Street to 82nd Street, Bay Ridge, Brooklyn",
        "borough": "Brooklyn",
        "link": "https://brooklynbridgeparents.com/outdoor-festivals-and-street-fairs-in-brooklyn-in-2025/"
    },
    {
        "name": "Summer Market in Cobble Hill",
        "date": "2025-07-26 to 2025-07-27",
        "time": "TBD (likely daytime)",
        "address": "Cobble Hill, Brooklyn",
        "borough": "Brooklyn",
        "link": "https://www.timeout.com/newyork/events-calendar/july-events-calendar"
    },
    {
        "name": "FREE art market in Brooklyn",
        "date": "2025-07-26 to 2025-07-27",
        "time": "1:00 PM - 7:00 PM EDT",
        "address": "26 Bridge St, Brooklyn, NY 11201",
        "borough": "Brooklyn",
        "link": "https://www.eventbrite.co.uk/e/free-art-market-in-brooklyn-tickets-1310673171739"
    },
    {
        "name": "FREE Community Fair at Brooklyn RISE Charter School",
        "date": "2025-07-26",
        "time": "12:00 PM - 4:00 PM",
        "address": "9 Hanover Pl, Brooklyn, NY 11217",
        "borough": "Brooklyn",
        "link": "https://www.eventbrite.com/e/free-community-fair-at-brooklyn-rise-charter-school-tickets-1431990254399?aff=erelexpmlt"
    },
    {
        "name": "BRIC Celebrate Brooklyn! (A Tribute to Quincy Jones: The Wiz)",
        "date": "2025-07-26",
        "time": "Doors 6:00 PM / Show 7:00 PM",
        "address": "Lena Horne Bandshell, Prospect Park West, Brooklyn, NY",
        "borough": "Brooklyn",
        "link": "https://bricartsmedia.org/event/the-wiz/"
    },
    {
        "name": "Bats! Night Walk",
        "date": "2025-07-31",
        "time": "7:30 PM – 9:00 PM",
        "address": "Seba Playground, Seba Ave & Gerritsen Ave (Marine Park), Brooklyn",
        "borough": "Brooklyn",
        "link": "https://www.reddit.com/r/nyc/comments/1li14mo/things-to-do-in-nyc-july-2025/"
    },
    {
        "name": "BRIC Celebrate Brooklyn! at Brower Park",
        "date": "2025-07-19",
        "time": "4:00 PM – 7:15 PM",
        "address": "Park Place between Brooklyn Ave & Kingston Ave, Brooklyn, NY",
        "borough": "Brooklyn",
        "link": "https://bricartsmedia.org/event/bric-celebrate-brooklyn-at-brower-park-2025"
    },
    {
        "name": "A Tribute to Quincy Jones: The Wiz",
        "date": "2025-07-26",
        "time": "Doors 6:00 PM / Show 7:00 PM",
        "address": "Lena Horne Bandshell, Prospect Park West, Brooklyn, NY",
        "borough": "Brooklyn",
        "link": "https://bricartsmedia.org/event/the-wiz/"
    },
    # --- Queens Events ---
    {
        "name": "2025 Waterfront Summer Concert Series (Astoria Park)",
        "date": "2025-07-03",
        "time": "7:00 PM – 9:00 PM",
        "address": "Great Lawn at Astoria Park, Queens",
        "borough": "Queens",
        "link": "https://www.nycgovparks.org/events/2025/07/17/2025-waterfront-summer-concert-series"
    },
    {
        "name": "2025 Waterfront Summer Concert Series (Astoria Park)",
        "date": "2025-07-10",
        "time": "7:00 PM – 9:00 PM",
        "address": "Great Lawn at Astoria Park, Queens",
        "borough": "Queens",
        "link": "https://www.nycgovparks.org/events/2025/07/17/2025-waterfront-summer-concert-series"
    },
    {
        "name": "Summer Concert Series - Forest Park Trust (Draw the Line - Aerosmith Tribute)",
        "date": "2025-07-10",
        "time": "7:30 PM",
        "address": "George Seuffert, Sr. Bandshell (in Forest Park), Queens",
        "borough": "Queens",
        "link": "https://forestparktrust.org/events/2024-summer-concert-series-4acsh"
    },
    {
        "name": "The Queens Jazz Trail Free Concert Series: Bryan Carrott",
        "date": "2025-07-10",
        "time": "7:00 PM – 8:00 PM",
        "address": "Baisley Pond Park, Jamaica, Queens",
        "borough": "Queens",
        "link": "https://www.nycgovparks.org/events/free_summer_concerts"
    },
    {
        "name": "2025 Waterfront Summer Concert Series (Astoria Park)",
        "date": "2025-07-17",
        "time": "7:00 PM – 9:00 PM",
        "address": "Great Lawn at Astoria Park, Queens",
        "borough": "Queens",
        "link": "https://www.nycgovparks.org/events/2025/07/17/2025-waterfront-summer-concert-series"
    },
    {
        "name": "Summer Concert Series - Forest Park Trust (Zac N' Fried - Zac Brown Tribute)",
        "date": "2025-07-17",
        "time": "7:30 PM",
        "address": "George Seuffert, Sr. Bandshell (in Forest Park), Queens",
        "borough": "Queens",
        "link": "https://forestparktrust.org/events/2024-summer-concert-series-4acsh"
    },
    {
        "name": "Basement Bhangra Beyond",
        "date": "2025-07-19",
        "time": "6:00 PM",
        "address": "Adjacent to Unisphere, Flushing Meadows-Corona Park, Queens",
        "borough": "Queens",
        "link": "https://qns.com/2025/06/richards-queens-day-july-free-concert-the-roots/"
    },
    {
        "name": "Queens Day! (Concert with The Roots)",
        "date": "2025-07-20",
        "time": "10:00 AM – 8:00 PM (Festivities, concert time TBD)",
        "address": "Flushing Meadows Corona Park, Queens",
        "borough": "Queens",
        "link": "https://allianceforfmcp.org/events/2025/7/20/queens-day"
    },
    {
        "name": "2025 Waterfront Summer Concert Series (Astoria Park)",
        "date": "2025-07-24",
        "time": "7:00 PM – 9:00 PM",
        "address": "Great Lawn at Astoria Park, Queens",
        "borough": "Queens",
        "link": "https://www.nycgovparks.org/events/2025/07/17/2025-waterfront-summer-concert-series"
    },
    {
        "name": "Summer Concert Series - Forest Park Trust (Standing Ovation - Musical Theater)",
        "date": "2025-07-24",
        "time": "7:30 PM",
        "address": "George Seuffert, Sr. Bandshell (in Forest Park), Queens",
        "borough": "Queens",
        "link": "https://forestparktrust.org/events/2024-summer-concert-series-4acsh"
    },
    {
        "name": "MoMA PS1 Warm Up",
        "date": "2025-07-25",
        "time": "TBD (likely evening)",
        "address": "MoMA PS1, Long Island City, Queens",
        "borough": "Queens",
        "link": "https://www.timeout.com/newyork/events-calendar/july-events-calendar"
    },
    {
        "name": "2025 Waterfront Summer Concert Series (Astoria Park)",
        "date": "2025-07-31",
        "time": "7:00 PM – 9:00 PM",
        "address": "Great Lawn at Astoria Park, Queens",
        "borough": "Queens",
        "link": "https://www.nycgovparks.org/events/2025/07/17/2025-waterfront-summer-concert-series"
    },
    {
        "name": "Summer Concert Series - Forest Park Trust (Jay Bon Jovi - Bon Jovi Tribute)",
        "date": "2025-07-31",
        "time": "7:30 PM",
        "address": "George Seuffert, Sr. Bandshell (in Forest Park), Queens",
        "borough": "Queens",
        "link": "https://forestparktrust.org/events/2024-summer-concert-series-4acsh"
    },
    # --- Staten Island Events ---
    {
        "name": "Our Lady of Mount Carmel Feast / Celebration",
        "date": "2025-07-13 to 2025-07-27",
        "time": "TBD (check link closer to date)",
        "address": "Rosebank, Staten Island",
        "borough": "Staten Island",
        "link": "https://www.statenbuzz.nyc/article/113/staten-island-street-fairs---staten-island-nyc"
    },
    {
        "name": "Cottage Row Curiosities",
        "date": "2025-07-19",
        "time": "11:00 AM - 4:00 PM",
        "address": "Snug Harbor Cultural Center, 1000 Richmond Terrace, Randall Manor, Staten Island",
        "borough": "Staten Island",
        "link": "https://www.statenbuzz.nyc/article/113/staten-island-street-fairs---staten-island-nyc"
    },
    {
        "name": "Stars, Stripes and Staten Sights (Vendor Fair)",
        "date": "2025-07-04",
        "time": "12:00 PM – 8:00 PM",
        "address": "Empire Outlets, 55 Richmond Terrace, Staten Island",
        "borough": "Staten Island",
        "link": "https://www.siparent.com/4th-of-july-events-in-staten-island-2025/"
    },
    {
        "name": "Pizza Party 2025",
        "date": "2025-07-26",
        "time": "TBD (likely daytime)",
        "address": "Snug Harbor Cultural Center & Botanical Garden, Staten Island",
        "borough": "Staten Island",
        "link": "https://allevents.in/staten-island/festivals"
    },
    {
        "name": "Rosebank Street Tree Care (Volunteer Event)",
        "date": "2025-07-26",
        "time": "10:00 AM – 12:00 PM",
        "address": "Von Briesen Park, 1271 Bay St (Shore Acres), Staten Island",
        "borough": "Staten Island",
        "link": "https://www.reddit.com/r/nyc/comments/1li14mo/things-to-do-in-nyc-july-2025/"
    },
    {
        "name": "Rise Up NYC Concert Series (Staten Island Dates)",
        "date": "2025-07-26 to 2025-07-27",
        "time": "TBD (check link closer to date)",
        "address": "Venue details coming soon, Staten Island",
        "borough": "Staten Island",
        "link": "https://riseupnycconcerts.com/rise-up-nyc-2025-official-dates-announced-for-the-citys-biggest-free-concert-series/"
    },
    {
        "name": "Carnegie Hall Citywide: Symphonic Brass Alliance",
        "date": "2025-07-26",
        "time": "TBD (likely evening)",
        "address": "Historic Richmond Town, Staten Island",
        "borough": "Staten Island",
        "link": "https://secretnyc.co/free-summer-concerts-2025-full-list/"
    },
    # --- Asbury Park, NJ Events ---
    {
        "name": "Asbury Park Spring Bazaar",
        "date": "2025-07-17",
        "time": "12:00 PM - 5:00 PM",
        "address": "Asbury Park Convention Hall, Asbury Park, NJ",
        "borough": "Asbury Park, NJ",
        "link": "https://www.njfamily.com/events/asbury-park-spring-bazaar-2025/2025-07-17/"
    },
    {
        "name": "Independence Day Fireworks",
        "date": "2025-07-03",
        "time": "9:00 PM",
        "address": "Boardwalk & Waterfront, Asbury Park, NJ",
        "borough": "Asbury Park",
        "link": "https://www.cityofasburypark.com/CivicAlerts.aspx?AID=2450"
    },
    {
        "name": "Shoreline Social Club Trivia Night",
        "date": "2025-07-10",
        "time": "7:00 PM – 9:00 PM",
        "address": "Shoreline Social Club, Asbury Park, NJ",
        "borough": "Asbury Park",
        "link": ""
    }
]

def generate_event_id(event):
    """Generate a unique ID for each event based on its content"""
    # Create a unique string from event data
    unique_string = f"{event['name']}_{event['date']}_{event['time']}_{event['address']}"
    # Create a hash of this string
    return hashlib.md5(unique_string.encode()).hexdigest()

def upload_events_to_firestore():
    """Upload all events to Firestore"""
    print("Starting to upload events to Firestore...")
    
    # Reference to the events collection
    events_ref = db.collection('events')
    
    # Counter for progress
    uploaded_count = 0
    total_events = len(nyc_free_events_database)
    
    for event in nyc_free_events_database:
        try:
            # Generate unique ID for this event
            event_id = generate_event_id(event)
            
            # Add timestamp for when this event was uploaded
            event_data = {
                **event,
                'uploaded_at': datetime.now(),
                'event_id': event_id
            }
            
            # Upload to Firestore with the unique ID as document ID
            events_ref.document(event_id).set(event_data)
            
            uploaded_count += 1
            print(f"Uploaded {uploaded_count}/{total_events}: {event['name']}")
            
        except Exception as e:
            print(f"Error uploading {event['name']}: {str(e)}")
    
    print(f"\n✅ Successfully uploaded {uploaded_count} events to Firestore!")
    print("You can now view your events in the Firebase Console under Firestore Database.")

if __name__ == "__main__":
    upload_events_to_firestore() 