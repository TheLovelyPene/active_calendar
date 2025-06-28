## This script reads event data from nyc_free_events_database
# and generates multiple HTML files (one per week) to display the events,
# including navigation between weeks and color-coding by borough.

import os
from datetime import datetime, date, timedelta

# --- Your NYC Free Events Database ---
# This database contains free events for July 2025,
# including festivals, fairs, and concerts, across NYC boroughs and Asbury Park, NJ.
# Bronx events are filtered out as per previous request.
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
        "date": "2025-07-27",
        "time": "TBD (likely evening)",
        "address": "Lena Horne Bandshell (Prospect Park), Brooklyn",
        "borough": "Brooklyn",
        "link": "https://bricartsmedia.org/celebrate-brooklyn/"
    },
    {
        "name": "Bats! Night Walk",
        "date": "2025-07-31",
        "time": "7:30 PM – 9:00 PM",
        "address": "Seba Playground, Seba Ave & Gerritsen Ave (Marine Park), Brooklyn",
        "borough": "Brooklyn",
        "link": "https://www.reddit.com/r/nyc/comments/1li14mo/things-to-do-in-nyc-july-2025/"
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

    # --- The Bronx Events ---
    # Note: Events from The Bronx are currently filtered out in App.js.
    # To display them, remove or modify the filter in App.js.
    {
        "name": "Bronx Pride Festival & Health Fair",
        "date": "2025-07-19",
        "time": "TBD (likely daytime)",
        "address": "TBD (check link closer to date), The Bronx",
        "borough": "The Bronx",
        "link": "https://bucketlisters.com/inspiration/443-every-street-festival-in-new-york-city-this-summer"
    },
    {
        "name": "Bronx Night Market",
        "date": "2025-07-26",
        "time": "TBD (likely evening)",
        "address": "TBD (check link closer to date), The Bronx",
        "borough": "The Bronx",
        "link": "https://bucketlisters.com/inspiration/443-every-street-festival-in-new-york-city-this-summer"
    },
    {
        "name": "Summer Streets NYC (Bronx route)",
        "date": "2025-07-26",
        "time": "7:00 AM – 3:00 PM",
        "address": "Poe Park (E 192nd & Kingsbridge Rd), The Bronx",
        "borough": "The Bronx",
        "link": "https://www.unlimitedbiking.com/blog/bike-events/summer-streets-nyc-2025-a-car%E2%80%91free-celebration-of-the-city/"
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
    }
];

# Define colors for each borough (you can customize these)
BOROUGH_COLORS = {
    "Manhattan": "#f8d7da",  # Light red/pink
    "Brooklyn": "#d4edda",   # Light green
    "Queens": "#cce5ff",     # Light blue
    "The Bronx": "#fff3cd",  # Light yellow - Note: Events from The Bronx are currently filtered out.
    "Staten Island": "#e2e3e5", # Light grey
    "Asbury Park, NJ": "#d1ecf1", # Light teal/cyan for New Jersey
    "Manhattan (Primary launch area)": "#f8d7da", # Same as Manhattan
    "Brooklyn (accessible, shared)": "#d4edda" # Same as Brooklyn
}

def get_week_label(iso_year, iso_week):
    """Generates a user-friendly label for the week (e.g., 'Week of July 1st, 2025')."""
    # Get the date of the Monday of the given ISO week (ISO week starts on Monday)
    first_day_of_week = datetime.strptime(f'{iso_year}-W{iso_week}-1', "%Y-W%W-%w").date()
    return first_day_of_week.strftime("Week of %B %d, %Y")

def get_iso_week_from_date_str(date_str):
    """Parses a date string and returns its ISO year and week number."""
    # Handle single date format
    if "to" not in date_str:
        event_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    else: # For date ranges, use the start date to determine the week
        start_date_str = date_str.split(" to ")[0]
        event_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()

    iso_year, iso_week, _ = event_date.isocalendar()
    return iso_year, iso_week

def generate_weekly_events_html(events_data, output_filename="nyc_events_calendar.html"):
    """
    Generates a single HTML file with weekly sections from the provided events data,
    including navigation between weeks and color-coding by borough.

    Args:
        events_data (list of dict): A list of dictionaries with event details.
        output_filename (str): The name of the HTML file to create.
    """
    # Filter out events from The Bronx (as previously requested)
    filtered_events_data = [event for event in events_data if event["borough"] != "The Bronx"]

    # Group events by week
    events_by_week = {}

    # Start from the Monday of the week containing July 1st
    # July 1st, 2025 is a Tuesday, so the week starts Monday June 30th
    start_july = date(2025, 7, 1)
    end_july = date(2025, 7, 31)
    
    # Find the Monday of the week containing July 1st
    days_since_monday = start_july.weekday()  # 0=Monday, 1=Tuesday, etc.
    week_start_date = start_july - timedelta(days=days_since_monday)  # This gives us Monday June 30th
    
    # Create weekly chunks starting from the Monday of the week containing July 1st
    current_date = week_start_date
    week_number = 0
    
    while current_date <= end_july:
        # Create a week starting from current_date
        week_start = current_date
        week_end = current_date + timedelta(days=6)
        
        # Create a unique week identifier
        week_key = f"week_{week_number}"
        events_by_week[week_key] = {i: [] for i in range(1, 8)} # 1=Mon, 7=Sun
        
        # Move to next week
        current_date = week_end + timedelta(days=1)
        week_number += 1

    # Populate events into their respective weeks and days
    for event in filtered_events_data:
        # Debug: Print July 2nd events to see what's happening
        if event["date"] == "2025-07-02":
            print(f"Processing July 2nd event: {event['name']}")
        
        # Handle date ranges by adding event to each relevant day within the range
        if " to " in event["date"]:
            start_date_str, end_date_str = event["date"].split(" to ")
            start_event_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_event_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

            current_event_date = start_event_date
            while current_event_date <= end_event_date:
                # Find which week this date belongs to
                days_since_week_start = (current_event_date - week_start_date).days
                week_index = days_since_week_start // 7
                week_key = f"week_{week_index}"
                
                if week_key in events_by_week:
                    # Calculate day of week (1=Monday, 7=Sunday)
                    weekday = current_event_date.weekday() + 1
                    events_by_week[week_key][weekday].append(event)
                    if event["date"] == "2025-07-02":
                        print(f"Added July 2nd event to week {week_key}, day {weekday}")
                current_event_date += timedelta(days=1)
        else:
            event_date = datetime.strptime(event["date"], "%Y-%m-%d").date()
            # Find which week this date belongs to
            days_since_week_start = (event_date - week_start_date).days
            week_index = days_since_week_start // 7
            week_key = f"week_{week_index}"
            
            if week_key in events_by_week:
                # Calculate day of week (1=Monday, 7=Sunday)
                weekday = event_date.weekday() + 1
                events_by_week[week_key][weekday].append(event)
                if event["date"] == "2025-07-02":
                    print(f"Added July 2nd event to week {week_key}, day {weekday}")
            else:
                if event["date"] == "2025-07-02":
                    print(f"July 2nd event NOT added - week {week_key} not in events_by_week")

    # Get a sorted list of week keys
    sorted_weeks = sorted(events_by_week.keys(), key=lambda x: int(x.split('_')[1]))

    # Start building the HTML content
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NYC & NJ Free Events - July 2025</title>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
        <style>
            body { font-family: 'Inter', sans-serif; background-color: #f0f2f5; }
            .event-card {
                border-radius: 0.75rem; /* rounded-lg */
                box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.06); /* shadow-sm */
                margin-bottom: 0.75rem; /* mb-3 */
                padding: 0.75rem; /* p-3 */
                transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
            }
            .event-card:hover {
                transform: translateY(-3px);
                box-shadow: 0 6px 10px -1px rgba(0, 0, 0, 0.15), 0 4px 6px -2px rgba(0, 0, 0, 0.08);
            }
            .borough-manhattan { background-color: #f8d7da; } /* Light Red */
            .borough-brooklyn { background-color: #d4edda; }  /* Light Green */
            .borough-queens { background-color: #cce5ff; }    /* Light Blue */
            .borough-the-bronx { background-color: #fff3cd; } /* Light Yellow */
            .borough-staten-island { background-color: #e2e3e5; } /* Light Grey */
            .borough-asbury-park-nj { background-color: #d1ecf1; } /* Light Teal/Cyan for NJ */
            .borough-manhattan-primary-launch-area { background-color: #f8d7da; } /* Same as Manhattan */
            .borough-brooklyn-accessible-shared { background-color: #d4edda; } /* Same as Brooklyn */
            .event-title {
                font-weight: bold;
                font-size: 1.125rem; /* text-lg */
                margin-bottom: 0.25rem; /* mb-1 */
                color: #2d3748; /* gray-800 */
            }
            .event-detail {
                font-size: 0.75rem; /* text-xs */
                color: #4a5568; /* gray-700 */
                margin-bottom: 0.125rem; /* mb-px */
            }
            .event-link {
                color: #3182ce; /* blue-600 */
                text-decoration: underline;
                word-break: break-all;
            }
            .day-card {
                background-color: #ffffff;
                border-radius: 0.75rem; /* rounded-lg */
                box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06); /* shadow-sm */
                padding: 1rem;
                margin-bottom: 1rem;
            }
            .day-header {
                font-size: 1.25rem; /* text-xl */
                font-weight: bold;
                color: #2d3748;
                margin-bottom: 0.75rem;
                border-bottom: 2px solid #edf2f7; /* gray-200 */
                padding-bottom: 0.5rem;
            }
            .week-section {
                margin-bottom: 3rem;
                padding: 2rem;
                background-color: #ffffff;
                border-radius: 1rem;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                display: none; /* Hide all weeks by default */
            }
            .week-section.active {
                display: block; /* Show only the active week */
            }
            .week-nav {
                position: sticky;
                top: 0;
                background-color: #ffffff;
                padding: 1rem;
                border-bottom: 2px solid #edf2f7;
                z-index: 100;
                margin-bottom: 2rem;
            }
            .week-nav a {
                display: inline-block;
                margin: 0 0.5rem;
                padding: 0.5rem 1rem;
                background-color: #3182ce;
                color: white;
                text-decoration: none;
                border-radius: 0.5rem;
                transition: background-color 0.2s;
                cursor: pointer;
            }
            .week-nav a:hover {
                background-color: #2c5aa0;
            }
            .week-nav a.active {
                background-color: #2c5aa0;
                font-weight: bold;
            }
        </style>
        <script>
            function showWeek(weekId) {
                // Hide all week sections
                const allWeeks = document.querySelectorAll('.week-section');
                allWeeks.forEach(week => {
                    week.classList.remove('active');
                });
                
                // Show the selected week
                const selectedWeek = document.getElementById(weekId);
                if (selectedWeek) {
                    selectedWeek.classList.add('active');
                }
                
                // Update navigation links
                const allNavLinks = document.querySelectorAll('.week-nav a');
                allNavLinks.forEach(link => {
                    link.classList.remove('active');
                });
                
                const activeNavLink = document.querySelector(`[onclick="showWeek('${weekId}')"]`);
                if (activeNavLink) {
                    activeNavLink.classList.add('active');
                }
            }
            
            // Show the first week by default when page loads
            window.onload = function() {
                showWeek('week-0');
            };
        </script>
    </head>
    <body class="p-4">
        <div class="max-w-6xl mx-auto">
            <h1 class="text-4xl font-bold text-center text-gray-800 mb-6">NYC & NJ Free Events - July 2025</h1>
            <p class="text-center text-gray-600 mb-8">Festivals, Fairs, and Concerts</p>
            
            <!-- Week Navigation -->
            <div class="week-nav">
                <h3 class="text-lg font-semibold mb-2">Jump to Week:</h3>
    """

    # Add navigation links
    for i, week_key in enumerate(sorted_weeks):
        week_number = int(week_key.split('_')[1])
        nav_week_start = week_start_date + timedelta(days=week_number * 7)
        nav_week_end = nav_week_start + timedelta(days=6)
        
        # Create week label
        week_label = f"Week of {nav_week_start.strftime('%B %d')}, {nav_week_start.year}"
        
        week_id = f"week-{i}"
        
        # Add 'active' class to the first navigation link
        active_class = " active" if i == 0 else ""
        
        html_content += f'<a onclick="showWeek(\'{week_id}\')" class="{active_class}">{week_label}</a>'

    html_content += """
            </div>
    """

    # Generate weekly sections
    for i, week_key in enumerate(sorted_weeks):
        week_number = int(week_key.split('_')[1])
        content_week_start = week_start_date + timedelta(days=week_number * 7)
        content_week_end = content_week_start + timedelta(days=6)
        
        # Create week label
        week_label = f"Week of {content_week_start.strftime('%B %d')}, {content_week_start.year}"
        
        week_id = f"week-{i}"

        # Add 'active' class to the first week
        active_class = " active" if i == 0 else ""

        html_content += f"""
            <div id="{week_id}" class="week-section{active_class}">
                <h2 class="text-3xl font-bold text-center text-gray-800 mb-6">{week_label}</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        """
        
        # Iterate through days of the week (Monday=1 to Sunday=7)
        for weekday_num in range(1, 8):
            current_day_date = content_week_start + timedelta(days=weekday_num - 1)
            # Only show days that are in July
            if start_july <= current_day_date <= end_july:
                day_name = current_day_date.strftime("%A, %B %d")
                events_for_day = sorted(events_by_week.get(week_key, {}).get(weekday_num, []),
                                         key=lambda x: x["time"] if x["time"] != "TBD (likely daytime)" and x["time"] != "TBD (likely evening)" and x["time"] != "TBD (morning/afternoon)" else "ZZZ")
                
                html_content += f"""
                    <div class="day-card">
                        <div class="day-header">{day_name}</div>
                """
                if events_for_day:
                    for event in events_for_day:
                        borough_class = event["borough"].lower().replace(" ", "-").replace("(", "").replace(")", "").replace(",", "")
                        html_content += f"""
                            <div class="event-card borough-{borough_class}">
                                <div class="event-title">{event["name"]}</div>
                                <div class="event-detail"><strong>Time:</strong> {event["time"]}</div>
                                <div class="event-detail"><strong>Address:</strong> {event["address"]}</div>
                                <div class="event-detail"><strong>Borough/Area:</strong> {event["borough"]}</div>
                                <div class="event-detail"><strong>Link:</strong> <a href="{event["link"]}" target="_blank" class="event-link">{event["link"]}</a></div>
                            </div>
                        """
                else:
                    html_content += """
                        <p class="text-gray-500 text-sm italic">No events scheduled for this day.</p>
                    """
                html_content += """
                    </div>
                """
            
        html_content += """
                </div>
            </div>
        """

    html_content += """
        </div>
    </body>
    </html>
    """

    # Write the generated HTML content to a file
    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"HTML calendar generated successfully: {os.path.abspath(output_filename)}")
        print(f"You can open '{output_filename}' in your web browser to view it.")
    except IOError as e:
        print(f"Error writing HTML file: {e}")

# --- Execute the HTML generation ---
if __name__ == "__main__":
    generate_weekly_events_html(nyc_free_events_database)
