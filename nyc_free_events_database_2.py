## This script reads event data from nyc_free_events_database
# and generates multiple HTML files (one per week) to display the events,
# including navigation between weeks and color-coding by borough.

import os
from datetime import datetime, date, timedelta, time
import re
from collections import defaultdict
import calendar

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

    # --- NYC Parks Events (Official NYC Parks Programming) ---
    {
        "name": "Summer on the Hudson: Concert Series",
        "date": "2025-07-02",
        "time": "6:00 PM - 8:00 PM",
        "address": "Riverside Park, 103rd Street, New York, NY 10025",
        "borough": "Manhattan",
        "link": "https://www.nycgovparks.org/events/summer_on_the_hudson"
    },
    {
        "name": "Summer on the Hudson: Movies Under the Stars",
        "date": "2025-07-05",
        "time": "8:00 PM - 10:00 PM",
        "address": "Riverside Park, 91st Street, New York, NY 10024",
        "borough": "Manhattan",
        "link": "https://www.nycgovparks.org/events/summer_on_the_hudson"
    },
    {
        "name": "Summer on the Hudson: Jazz Performance",
        "date": "2025-07-09",
        "time": "6:00 PM - 8:00 PM",
        "address": "Riverside Park, 79th Street, New York, NY 10024",
        "borough": "Manhattan",
        "link": "https://www.nycgovparks.org/events/summer_on_the_hudson"
    },
    {
        "name": "Summer on the Hudson: Family Dance Party",
        "date": "2025-07-16",
        "time": "6:00 PM - 8:00 PM",
        "address": "Riverside Park, 103rd Street, New York, NY 10025",
        "borough": "Manhattan",
        "link": "https://www.nycgovparks.org/events/summer_on_the_hudson"
    },
    {
        "name": "Summer on the Hudson: World Music Night",
        "date": "2025-07-23",
        "time": "6:00 PM - 8:00 PM",
        "address": "Riverside Park, 96th Street, New York, NY 10025",
        "borough": "Manhattan",
        "link": "https://www.nycgovparks.org/events/summer_on_the_hudson"
    },
    {
        "name": "Summer on the Hudson: Kids Show",
        "date": "2025-07-30",
        "time": "6:00 PM - 7:00 PM",
        "address": "Riverside Park, 91st Street, New York, NY 10024",
        "borough": "Manhattan",
        "link": "https://www.nycgovparks.org/events/summer_on_the_hudson"
    },
    {
        "name": "Movies Under the Stars - Central Park",
        "date": "2025-07-07",
        "time": "8:00 PM - 10:00 PM",
        "address": "Central Park Great Lawn, 79th St Transverse, New York, NY 10024",
        "borough": "Manhattan",
        "link": "https://www.nycgovparks.org/events/free_summer_movies"
    },
    {
        "name": "Movies Under the Stars - Bryant Park",
        "date": "2025-07-14",
        "time": "8:00 PM - 10:00 PM",
        "address": "Bryant Park, 1065 Avenue of the Americas, New York, NY 10018",
        "borough": "Manhattan",
        "link": "https://www.nycgovparks.org/events/free_summer_movies"
    },
    {
        "name": "Shakespeare in the Park: Romeo & Juliet",
        "date": "2025-07-01",
        "time": "8:00 PM - 10:30 PM",
        "address": "Delacorte Theater, Central Park, 81st St & Central Park West, New York, NY 10024",
        "borough": "Manhattan",
        "link": "https://www.nycgovparks.org/events/free_summer_theater"
    },
    {
        "name": "Shakespeare in the Park: Romeo & Juliet",
        "date": "2025-07-08",
        "time": "8:00 PM - 10:30 PM",
        "address": "Delacorte Theater, Central Park, 81st St & Central Park West, New York, NY 10024",
        "borough": "Manhattan",
        "link": "https://www.nycgovparks.org/events/free_summer_theater"
    },
    {
        "name": "Shakespeare in the Park: Romeo & Juliet",
        "date": "2025-07-15",
        "time": "8:00 PM - 10:30 PM",
        "address": "Delacorte Theater, Central Park, 81st St & Central Park West, New York, NY 10024",
        "borough": "Manhattan",
        "link": "https://www.nycgovparks.org/events/free_summer_theater"
    },
    {
        "name": "Shakespeare in the Park: Romeo & Juliet",
        "date": "2025-07-22",
        "time": "8:00 PM - 10:30 PM",
        "address": "Delacorte Theater, Central Park, 81st St & Central Park West, New York, NY 10024",
        "borough": "Manhattan",
        "link": "https://www.nycgovparks.org/events/free_summer_theater"
    },
    {
        "name": "Shakespeare in the Park: Romeo & Juliet",
        "date": "2025-07-29",
        "time": "8:00 PM - 10:30 PM",
        "address": "Delacorte Theater, Central Park, 81st St & Central Park West, New York, NY 10024",
        "borough": "Manhattan",
        "link": "https://www.nycgovparks.org/events/free_summer_theater"
    },
    {
        "name": "Bryant Park Picnic Performances",
        "date": "2025-07-04",
        "time": "12:00 PM - 2:00 PM",
        "address": "Bryant Park, 1065 Avenue of the Americas, New York, NY 10018",
        "borough": "Manhattan",
        "link": "https://www.nycgovparks.org/events"
    },
    {
        "name": "Bryant Park Yoga",
        "date": "2025-07-11",
        "time": "10:00 AM - 11:00 AM",
        "address": "Bryant Park, 1065 Avenue of the Americas, New York, NY 10018",
        "borough": "Manhattan",
        "link": "https://www.nycgovparks.org/events"
    },
    {
        "name": "Bryant Park Chess Tournament",
        "date": "2025-07-18",
        "time": "6:00 PM - 8:00 PM",
        "address": "Bryant Park, 1065 Avenue of the Americas, New York, NY 10018",
        "borough": "Manhattan",
        "link": "https://www.nycgovparks.org/events"
    },
    {
        "name": "Bryant Park Reading Room",
        "date": "2025-07-25",
        "time": "11:00 AM - 7:00 PM",
        "address": "Bryant Park, 1065 Avenue of the Americas, New York, NY 10018",
        "borough": "Manhattan",
        "link": "https://www.nycgovparks.org/events"
    },
    {
        "name": "Governors Island Art Fair",
        "date": "2025-07-12",
        "time": "11:00 AM - 6:00 PM",
        "address": "Governors Island, 10 South St, New York, NY 10004",
        "borough": "Manhattan",
        "link": "https://www.nycgovparks.org/events"
    },
    {
        "name": "Governors Island Food Festival",
        "date": "2025-07-19",
        "time": "12:00 PM - 6:00 PM",
        "address": "Governors Island, 10 South St, New York, NY 10004",
        "borough": "Manhattan",
        "link": "https://www.nycgovparks.org/events"
    },
    {
        "name": "Governors Island Jazz Festival",
        "date": "2025-07-26",
        "time": "2:00 PM - 7:00 PM",
        "address": "Governors Island, 10 South St, New York, NY 10004",
        "borough": "Manhattan",
        "link": "https://www.nycgovparks.org/events"
    },

    # --- Brooklyn NYC Parks Events ---
    {
        "name": "Prospect Park Bandshell Concert",
        "date": "2025-07-06",
        "time": "7:30 PM - 9:30 PM",
        "address": "Prospect Park Bandshell, 9th St & Prospect Park West, Brooklyn, NY 11215",
        "borough": "Brooklyn",
        "link": "https://www.nycgovparks.org/parks/prospect-park/events"
    },
    {
        "name": "Prospect Park Summer Concert",
        "date": "2025-07-13",
        "time": "7:30 PM - 9:30 PM",
        "address": "Prospect Park Bandshell, 9th St & Prospect Park West, Brooklyn, NY 11215",
        "borough": "Brooklyn",
        "link": "https://www.nycgovparks.org/parks/prospect-park/events"
    },
    {
        "name": "Prospect Park Jazz Concert",
        "date": "2025-07-20",
        "time": "7:30 PM - 9:30 PM",
        "address": "Prospect Park Bandshell, 9th St & Prospect Park West, Brooklyn, NY 11215",
        "borough": "Brooklyn",
        "link": "https://www.nycgovparks.org/parks/prospect-park/events"
    },
    {
        "name": "Prospect Park World Music Night",
        "date": "2025-07-27",
        "time": "7:30 PM - 9:30 PM",
        "address": "Prospect Park Bandshell, 9th St & Prospect Park West, Brooklyn, NY 11215",
        "borough": "Brooklyn",
        "link": "https://www.nycgovparks.org/parks/prospect-park/events"
    },
    {
        "name": "Movies Under the Stars - Prospect Park",
        "date": "2025-07-21",
        "time": "8:00 PM - 10:00 PM",
        "address": "Prospect Park Long Meadow, Prospect Park West, Brooklyn, NY 11215",
        "borough": "Brooklyn",
        "link": "https://www.nycgovparks.org/events/free_summer_movies"
    },

    # --- Queens NYC Parks Events ---
    {
        "name": "Queens County Farm Hayrides",
        "date": "2025-07-06",
        "time": "1:00 PM - 4:00 PM",
        "address": "Queens County Farm Museum, 73-50 Little Neck Pkwy, Floral Park, NY 11004",
        "borough": "Queens",
        "link": "https://www.nycgovparks.org/events"
    },
    {
        "name": "Flushing Meadows World Music Festival",
        "date": "2025-07-13",
        "time": "3:00 PM - 7:00 PM",
        "address": "Flushing Meadows Corona Park, Grand Central Pkwy, Flushing, NY 11368",
        "borough": "Queens",
        "link": "https://www.nycgovparks.org/events"
    },
    {
        "name": "Forest Park Summer Concert",
        "date": "2025-07-20",
        "time": "6:00 PM - 8:00 PM",
        "address": "Forest Park, Forest Park Dr, Woodhaven, NY 11421",
        "borough": "Queens",
        "link": "https://www.nycgovparks.org/events"
    },
    {
        "name": "Alley Pond Park Nature Walk",
        "date": "2025-07-27",
        "time": "10:00 AM - 12:00 PM",
        "address": "Alley Pond Park, 228-06 Northern Blvd, Douglaston, NY 11362",
        "borough": "Queens",
        "link": "https://www.nycgovparks.org/events"
    },
    {
        "name": "Movies Under the Stars - Flushing Meadows",
        "date": "2025-07-28",
        "time": "8:00 PM - 10:00 PM",
        "address": "Flushing Meadows Corona Park, Grand Central Pkwy, Flushing, NY 11368",
        "borough": "Queens",
        "link": "https://www.nycgovparks.org/events/free_summer_movies"
    },

    # --- The Bronx NYC Parks Events ---
    {
        "name": "Bronx River Festival",
        "date": "2025-07-05",
        "time": "12:00 PM - 5:00 PM",
        "address": "Bronx River Park, E 177th St & Southern Blvd, Bronx, NY 10460",
        "borough": "The Bronx",
        "link": "https://www.nycgovparks.org/events"
    },
    {
        "name": "Van Cortlandt Park Summer Concert",
        "date": "2025-07-12",
        "time": "7:00 PM - 9:00 PM",
        "address": "Van Cortlandt Park, Van Cortlandt Park S, Bronx, NY 10463",
        "borough": "The Bronx",
        "link": "https://www.nycgovparks.org/events"
    },
    {
        "name": "Pelham Bay Park Nature Festival",
        "date": "2025-07-19",
        "time": "11:00 AM - 4:00 PM",
        "address": "Pelham Bay Park, Bruckner Blvd & Wilkinson Ave, Bronx, NY 10461",
        "borough": "The Bronx",
        "link": "https://www.nycgovparks.org/events"
    },
    {
        "name": "Crotona Park Summer Festival",
        "date": "2025-07-26",
        "time": "2:00 PM - 6:00 PM",
        "address": "Crotona Park, Crotona Ave & E 173rd St, Bronx, NY 10457",
        "borough": "The Bronx",
        "link": "https://www.nycgovparks.org/events"
    },

    # --- Staten Island NYC Parks Events ---
    {
        "name": "Staten Island Boardwalk Summer Concert",
        "date": "2025-07-05",
        "time": "7:00 PM - 9:00 PM",
        "address": "Franklin D. Roosevelt Boardwalk, Staten Island, NY 10305",
        "borough": "Staten Island",
        "link": "https://www.nycgovparks.org/events"
    },
    {
        "name": "Conference House Park Cultural Festival",
        "date": "2025-07-12",
        "time": "1:00 PM - 5:00 PM",
        "address": "Conference House Park, 298 Satterlee St, Staten Island, NY 10307",
        "borough": "Staten Island",
        "link": "https://www.nycgovparks.org/events"
    },
    {
        "name": "Great Kills Park Beach Concert",
        "date": "2025-07-19",
        "time": "6:00 PM - 8:00 PM",
        "address": "Great Kills Park, Hylan Blvd, Staten Island, NY 10308",
        "borough": "Staten Island",
        "link": "https://www.nycgovparks.org/events"
    },
    {
        "name": "Snug Harbor Cultural Festival",
        "date": "2025-07-26",
        "time": "2:00 PM - 6:00 PM",
        "address": "Snug Harbor Cultural Center, 1000 Richmond Terrace, Staten Island, NY 10301",
        "borough": "Staten Island",
        "link": "https://www.nycgovparks.org/events"
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
    Generates a single HTML file with both weekly and borough-based navigation,
    including a toggle between week view and destination view.

    Args:
        events_data (list of dict): A list of dictionaries with event details.
        output_filename (str): The name of the HTML file to create.
    """
    # Filter out events from The Bronx (as previously requested)
    filtered_events_data = [event for event in events_data if event["borough"] != "The Bronx"]

    # Group events by week
    events_by_week = {}
    
    # Start from the Monday of the week containing July 1st
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

    # Get a sorted list of week keys
    sorted_weeks = sorted(events_by_week.keys(), key=lambda x: int(x.split('_')[1]))

    # Group events by borough for borough view
    events_by_borough = {}
    for event in filtered_events_data:
        borough = event["borough"]
        if borough not in events_by_borough:
            events_by_borough[borough] = []
        events_by_borough[borough].append(event)

    # Generate week navigation
    week_navigation = ""
    for i, week_key in enumerate(sorted_weeks):
        week_start = week_start_date + timedelta(days=i * 7)
        week_label = f"Week of {week_start.strftime('%B %d')}"
        active_class = "active" if i == 0 else ""
        week_navigation += f'<button class="nav-button {active_class}" onclick="showWeek({i})">{week_label}</button>'

    # Generate week sections
    week_sections = ""
    for i, week_key in enumerate(sorted_weeks):
        week_start = week_start_date + timedelta(days=i * 7)
        week_end = week_start + timedelta(days=6)
        week_label = f"Week of {week_start.strftime('%B %d, %Y')}"
        
        active_class = "active" if i == 0 else ""
        week_sections += f'<div id="week-{i}" class="week-section {active_class}">'
        week_sections += f'''
            <div class="week-header">
                <h2>{week_label}</h2>
                <p>{week_start.strftime('%B %d')} - {week_end.strftime('%B %d, %Y')}</p>
            </div>
            <div class="events-grid">
        '''
        
        # Get all events for this week
        week_events = []
        for day in range(1, 8):
            week_events.extend(events_by_week[week_key][day])
        
        if week_events:
            for event in week_events:
                borough_class = get_borough_class(event["borough"])
                week_sections += generate_event_card(event)
        else:
            week_sections += '<p class="no-events">No events scheduled for this week</p>'
        
        week_sections += '</div></div>'

    # Generate borough sections
    borough_sections = ""
    borough_buttons = ""
    
    borough_configs = {
        "Manhattan": {"class": "manhattan", "color": "#ff6b6b"},
        "Brooklyn": {"class": "brooklyn", "color": "#4ecdc4"},
        "Queens": {"class": "queens", "color": "#45b7d1"},
        "The Bronx": {"class": "bronx", "color": "#feca57"},
        "Staten Island": {"class": "staten-island", "color": "#a8e6cf"},
        "Asbury Park, NJ": {"class": "asbury-park", "color": "#d1ecf1"}
    }
    
    for borough, config in borough_configs.items():
        if borough in events_by_borough:
            borough_class = config["class"]
            active_class = "active" if borough == "Manhattan" else ""
            
            # Borough navigation button
            borough_buttons += f'<button class="borough-button {borough_class} {active_class}" onclick="showBorough(\'{borough_class}\')">{borough}</button>'
            
            # Borough section
            borough_sections += f'<div id="borough-{borough_class}" class="borough-section {active_class}">'
            borough_sections += f'''
                <div class="week-header">
                    <h2>{borough} Events</h2>
                    <p>All free events in {borough} for July 2025</p>
                </div>
                <div class="events-grid">
            '''
            
            # Sort events by date
            borough_events = sorted(events_by_borough[borough], key=lambda x: x["date"])
            
            if borough_events:
                for event in borough_events:
                    borough_sections += generate_event_card(event)
            else:
                borough_sections += f'<p class="no-events">No events scheduled for {borough}</p>'
            
            borough_sections += '</div></div>'

    # Generate the HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NYC Free Events Calendar - July 2025</title>
            <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 30px;
            background: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            color: #2c3e50;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        }}
        
        .header p {{
            font-size: 1.1rem;
            color: #7f8c8d;
            margin-bottom: 20px;
        }}
        
        .nav-section {{
            background: rgba(255, 255, 255, 0.95);
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }}
        
        .nav-section h3 {{
            text-align: center;
            margin-bottom: 15px;
            color: #2c3e50;
            font-size: 1.3rem;
        }}
        
        .week-nav {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            justify-content: center;
        }}
        
        .borough-nav {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            justify-content: center;
        }}
        
        .nav-button {{
            padding: 12px 20px;
            border: none;
            border-radius: 25px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
            text-align: center;
            min-width: 120px;
        }}
        
        .nav-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
        }}
        
        .nav-button.active {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            transform: scale(1.05);
        }}
        
        .borough-button {{
            padding: 10px 16px;
            border: none;
            border-radius: 20px;
            color: white;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
            text-align: center;
            min-width: 100px;
            font-size: 0.9rem;
        }}
        
        .borough-button.manhattan {{ background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); }}
        .borough-button.brooklyn {{ background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%); }}
        .borough-button.queens {{ background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); }}
        .borough-button.bronx {{ background: linear-gradient(135deg, #feca57 0%, #ff9ff3 100%); }}
        .borough-button.staten-island {{ background: linear-gradient(135deg, #a8e6cf 0%, #dcedc1 100%); color: #333; }}
        .borough-button.asbury-park {{ background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%); color: #333; }}
        
        .borough-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
        }}
        
        .borough-button.active {{
            transform: scale(1.1);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
        }}
        
        .content-section {{
            background: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }}
        
        .week-section {{
            display: none;
            animation: fadeIn 0.5s ease-in;
        }}
        
        .week-section.active {{
            display: block;
        }}
        
        .borough-section {{
            display: none;
            animation: fadeIn 0.5s ease-in;
        }}
        
        .borough-section.active {{
            display: block;
        }}
        
        .week-header {{
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
        }}
        
        .week-header h2 {{
            font-size: 2rem;
            margin-bottom: 10px;
        }}
        
        .week-header p {{
            font-size: 1.1rem;
            opacity: 0.9;
        }}
        
        /* Calendar Grid Layout */
        .calendar-grid {{
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 1px;
            background: #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
            margin-top: 20px;
            min-height: 600px;
        }}
        
        .calendar-day-header {{
            background: #2c3e50;
            color: white;
            padding: 12px 8px;
            text-align: center;
            font-weight: 600;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .calendar-day {{
            background: white;
            min-height: 140px;
            padding: 8px;
            border: 1px solid #f0f0f0;
            position: relative;
            display: flex;
            flex-direction: column;
        }}
        
        .calendar-day.empty {{
            background: #f8f9fa;
            color: #ccc;
        }}
        
        .day-number {{
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 6px;
            font-size: 1rem;
            text-align: center;
            padding: 2px;
            border-radius: 3px;
        }}
        
        .calendar-day.empty .day-number {{
            color: #ccc;
        }}
        
        .day-events {{
            display: flex;
            flex-direction: column;
            gap: 3px;
            flex: 1;
            overflow-y: auto;
        }}
        
        .day-event {{
            background: white;
            border-radius: 4px;
            padding: 4px 6px;
            font-size: 0.7rem;
            border-left: 2px solid #ddd;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
            margin-bottom: 2px;
        }}
        
        .day-event:hover {{
            transform: translateY(-1px);
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
            z-index: 10;
        }}
        
        .day-event.manhattan {{ border-left-color: #ff6b6b; }}
        .day-event.brooklyn {{ border-left-color: #4ecdc4; }}
        .day-event.queens {{ border-left-color: #3498db; }}
        .day-event.bronx {{ border-left-color: #feca57; }}
        .day-event.staten-island {{ border-left-color: #a8e6cf; }}
        .day-event.asbury-park {{ border-left-color: #d1ecf1; }}
        
        .day-event-name {{
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 2px;
            line-height: 1.1;
            font-size: 0.65rem;
        }}
        
        .day-event-time {{
            color: #7f8c8d;
            font-size: 0.6rem;
            margin-bottom: 2px;
        }}
        
        .day-event-borough {{
            display: inline-block;
            padding: 1px 4px;
            border-radius: 6px;
            font-size: 0.55rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.3px;
        }}
        
        .day-event-borough.manhattan {{ background: #ff6b6b; color: white; }}
        .day-event-borough.brooklyn {{ background: #4ecdc4; color: white; }}
        .day-event-borough.queens {{ background: #3498db; color: white; }}
        .day-event-borough.bronx {{ background: #feca57; color: #333; }}
        .day-event-borough.staten-island {{ background: #a8e6cf; color: #333; }}
        .day-event-borough.asbury-park {{ background: #d1ecf1; color: #333; }}
        
        .events-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        
                .event-card {{
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            border-left: 6px solid #ddd;
            position: relative;
            overflow: hidden;
        }}
        
                .event-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
        }}
        
        .event-card.manhattan {{ border-left-color: #ff6b6b; }}
        .event-card.brooklyn {{ border-left-color: #4ecdc4; }}
        .event-card.queens {{ border-left-color: #3498db; }}
        .event-card.bronx {{ border-left-color: #feca57; }}
        .event-card.staten-island {{ border-left-color: #a8e6cf; }}
        .event-card.asbury-park {{ border-left-color: #d1ecf1; }}
        
        .event-name {{
            font-size: 1.3rem;
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 15px;
            line-height: 1.3;
        }}
        
        .event-details {{
            margin-bottom: 15px;
        }}
        
                .event-detail {{
            display: flex;
            align-items: center;
            margin-bottom: 8px;
            font-size: 0.95rem;
        }}
        
        .event-detail i {{
            width: 20px;
            margin-right: 10px;
            color: #7f8c8d;
        }}
        
        .event-date {{
            font-weight: 600;
            color: #e74c3c;
        }}
        
        .event-time {{
            font-weight: 600;
            color: #3498db;
        }}
        
        .event-address {{
            color: #7f8c8d;
            font-style: italic;
        }}
        
        .event-borough {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 10px;
        }}
        
        .event-borough.manhattan {{ background: #ff6b6b; color: white; }}
        .event-borough.brooklyn {{ background: #4ecdc4; color: white; }}
        .event-borough.queens {{ background: #45b7d1; color: white; }}
        .event-borough.bronx {{ background: #feca57; color: #333; }}
        .event-borough.staten-island {{ background: #a8e6cf; color: #333; }}
        .event-borough.asbury-park {{ background: #d1ecf1; color: #333; }}
        
                .event-link {{
            display: inline-block;
            margin-top: 15px;
            padding: 10px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 25px;
            font-weight: 600;
            transition: all 0.3s ease;
        }}
        
        .event-link:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
        }}
        
        .no-events {{
            text-align: center;
            padding: 40px;
            color: #7f8c8d;
            font-size: 1.2rem;
            font-style: italic;
        }}
        
        .view-toggle {{
            text-align: center;
            margin-bottom: 20px;
        }}
        
        .toggle-button {{
            padding: 10px 20px;
            margin: 0 10px;
            border: none;
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.8);
            color: #333;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease;
        }}
        
        .toggle-button.active {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 10px;
            }}
            
            .header h1 {{
                font-size: 2rem;
            }}
            
            .events-grid {{
                grid-template-columns: 1fr;
            }}
            
            .week-nav, .borough-nav {{
                justify-content: center;
            }}
            
            .nav-button, .borough-button {{
                min-width: auto;
                padding: 10px 15px;
                font-size: 0.9rem;
            }}
        }}
        
        /* Weekly Calendar Grid Layout */
        .weekly-calendar-grid {{
            display: grid;
            grid-template-columns: 150px repeat(7, 1fr);
            gap: 1px;
            background: #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
            margin-top: 20px;
            font-size: 0.8rem;
        }}
        
        .calendar-header {{
            display: contents;
        }}
        
        .time-slot-header {{
            background: #2c3e50;
            color: white;
            padding: 12px 8px;
            text-align: center;
            font-weight: 600;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .date-header {{
            background: #34495e;
            color: white;
            padding: 12px 8px;
            text-align: center;
            font-weight: 600;
            font-size: 1rem;
        }}
        
        .time-row {{
            display: contents;
        }}
        
        .time-slot-label {{
            background: #ecf0f1;
            color: #2c3e50;
            padding: 10px 8px;
            text-align: center;
            font-weight: 600;
            font-size: 0.8rem;
            border-right: 1px solid #ddd;
        }}
        
        .day-cell {{
            background: white;
            min-height: 80px;
            padding: 4px;
            border: 1px solid #f0f0f0;
            display: flex;
            flex-direction: column;
            gap: 2px;
        }}
        
        .day-cell.empty {{
            background: #f8f9fa;
        }}
        
        .day-cell.with-events {{
            background: #f8f9fa;
        }}
        
        .grid-event {{
            background: white;
            border-radius: 4px;
            padding: 4px 6px;
            border-left: 3px solid #ddd;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
            margin-bottom: 2px;
        }}
        
        .grid-event.manhattan {{ border-left-color: #ff6b6b; }}
        .grid-event.brooklyn {{ border-left-color: #4ecdc4; }}
        .grid-event.queens {{ border-left-color: #3498db; }}
        .grid-event.bronx {{ border-left-color: #feca57; }}
        .grid-event.staten-island {{ border-left-color: #a8e6cf; }}
        .grid-event.asbury-park {{ border-left-color: #d1ecf1; }}
        
        .grid-event .event-name {{
            font-weight: 600;
            color: #2c3e50;
            font-size: 0.7rem;
            line-height: 1.1;
            margin-bottom: 2px;
        }}
        
        .grid-event .event-borough {{
            display: inline-block;
            padding: 1px 4px;
            border-radius: 6px;
            font-size: 0.6rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.3px;
            margin-bottom: 2px;
        }}
        
        .grid-event .event-borough.manhattan {{ background: #ff6b6b; color: white; }}
        .grid-event .event-borough.brooklyn {{ background: #4ecdc4; color: white; }}
        .grid-event .event-borough.queens {{ background: #3498db; color: white; }}
        .grid-event .event-borough.bronx {{ background: #feca57; color: #333; }}
        .grid-event .event-borough.staten-island {{ background: #a8e6cf; color: #333; }}
        .grid-event .event-borough.asbury-park {{ background: #d1ecf1; color: #333; }}
        
        .grid-event .event-link {{
            margin-top: 2px;
        }}
        
        .grid-event .event-link a {{
            display: inline-block;
            padding: 2px 6px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 12px;
            font-size: 0.6rem;
            font-weight: 600;
            transition: all 0.2s ease;
        }}
        
        .grid-event .event-link a:hover {{
            transform: translateY(-1px);
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }}
        
        /* Center navigation */
        .navigation {{
            text-align: center;
        }}
        
        .nav-section {{
            display: inline-block;
            margin: 0 20px 20px 20px;
        }}
        
        .nav-buttons, .borough-buttons {{
            justify-content: center;
        }}
        
        /* TBD styling */
        .time-slot-label:first-child {{
            font-weight: 700;
            color: #e74c3c;
        }}
        
        /* Weekly Calendar Table Layout */
        .weekly-calendar-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            background: #f8f9fa;
            font-size: 0.9rem;
            min-width: 900px;
        }}
        .weekly-calendar-table th, .weekly-calendar-table td {{
            border: 1px solid #e0e0e0;
            padding: 6px 4px;
            text-align: left;
            vertical-align: top;
        }}
        .weekly-calendar-table th {{
            background: #34495e;
            color: #fff;
            font-weight: 600;
            text-align: center;
        }}
        .weekly-calendar-table .time-slot-label {{
            background: #ecf0f1;
            color: #2c3e50;
            font-weight: 700;
            width: 120px;
            text-align: right;
        }}
        .weekly-calendar-table td.day-cell.empty {{
            background: #f8f9fa;
        }}
        .weekly-calendar-table td.day-cell.with-events {{
            background: #fff;
        }}
        .grid-event {{
            background: white;
            border-radius: 4px;
            padding: 4px 6px;
            border-left: 3px solid #ddd;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.07);
            margin-bottom: 2px;
        }}
        .grid-event.manhattan {{ border-left-color: #ff6b6b; }}
        .grid-event.brooklyn {{ border-left-color: #4ecdc4; }}
        .grid-event.queens {{ border-left-color: #3498db; }}
        .grid-event.bronx {{ border-left-color: #feca57; }}
        .grid-event.staten-island {{ border-left-color: #a8e6cf; }}
        .grid-event.asbury-park {{ border-left-color: #d1ecf1; }}
        .grid-event .event-name {{
            font-weight: 600;
            color: #2c3e50;
            font-size: 0.8rem;
            line-height: 1.1;
            margin-bottom: 2px;
        }}
        .grid-event .event-borough {{
            display: inline-block;
            padding: 1px 4px;
            border-radius: 6px;
            font-size: 0.65rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.3px;
            margin-bottom: 2px;
        }}
        .grid-event .event-link {{
            margin-top: 2px;
        }}
        .grid-event .event-link a {{
            display: inline-block;
            padding: 2px 6px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 12px;
            font-size: 0.7rem;
            font-weight: 600;
            transition: all 0.2s ease;
        }}
        .grid-event .event-link a:hover {{
            transform: translateY(-1px);
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }}
        
        /* Responsive scroll for table */
        .weekly-calendar-table-wrapper {{
            width: 100%;
            overflow-x: auto;
        }}
        
        /* Enhanced Mobile Responsiveness */
        @media (max-width: 768px) {{
            .container {{
                padding: 10px;
                margin: 0;
            }}
            
            .header {{
                padding: 20px 15px;
            }}
            
            .header h1 {{
                font-size: 1.8rem;
            }}
            
            .header p {{
                font-size: 1rem;
            }}
            
            .nav-section {{
                padding: 15px;
                margin-bottom: 15px;
            }}
            
            .nav-section h3 {{
                font-size: 1.1rem;
                margin-bottom: 10px;
            }}
            
            .week-nav, .borough-nav {{
                flex-direction: column;
                gap: 8px;
            }}
            
            .nav-button, .borough-button {{
                min-width: auto;
                padding: 12px 20px;
                font-size: 0.9rem;
                width: 100%;
                max-width: 300px;
                margin: 0 auto;
            }}
            
            .view-toggle {{
                margin-bottom: 15px;
            }}
            
            .toggle-button {{
                padding: 12px 20px;
                margin: 0 5px;
                font-size: 0.9rem;
            }}
            
            .content-section {{
                padding: 20px 15px;
            }}
            
            .week-header {{
                padding: 15px;
                margin-bottom: 20px;
            }}
            
            .week-header h2 {{
                font-size: 1.5rem;
            }}
            
            .week-header p {{
                font-size: 1rem;
            }}
            
            .events-grid {{
                grid-template-columns: 1fr;
                gap: 15px;
            }}
            
            .event-card {{
                padding: 20px;
            }}
            
            .event-header {{
                flex-direction: column;
                align-items: flex-start;
                gap: 10px;
            }}
            
            .event-title {{
                font-size: 1.2rem;
            }}
            
            .event-date {{
                font-size: 0.9rem;
                padding: 6px 12px;
            }}
            
            .event-details {{
                margin-bottom: 12px;
            }}
            
            .event-detail {{
                font-size: 0.9rem;
                margin-bottom: 6px;
            }}
            
            .event-detail i {{
                width: 16px;
                margin-right: 8px;
            }}
            
            .event-description {{
                font-size: 0.9rem;
                margin-bottom: 12px;
            }}
            
            .event-borough {{
                font-size: 0.75rem;
                padding: 4px 10px;
                margin-top: 8px;
            }}
            
            .event-link {{
                margin-top: 12px;
            }}
            
            .event-link a {{
                padding: 10px 20px;
                font-size: 0.9rem;
                width: 100%;
                text-align: center;
                display: block;
            }}
            
            .weekly-calendar-table-wrapper {{
                margin: 0 -15px 15px -15px;
                padding: 0 15px;
                box-shadow: inset -10px 0 10px -10px rgba(0, 0, 0, 0.1);
            }}
            
            .weekly-calendar-table {{
                min-width: 600px;
                font-size: 0.7rem;
            }}
        }}
        
        @media (max-width: 480px) {{
            .container {{
                padding: 5px;
            }}
            
            .header {{
                padding: 15px 10px;
            }}
            
            .header h1 {{
                font-size: 1.5rem;
            }}
            
            .header p {{
                font-size: 0.9rem;
            }}
            
            .nav-section {{
                padding: 10px;
            }}
            
            .nav-section h3 {{
                font-size: 1rem;
            }}
            
            .nav-button, .borough-button {{
                padding: 10px 15px;
                font-size: 0.8rem;
            }}
            
            .toggle-button {{
                padding: 10px 15px;
                font-size: 0.8rem;
                margin: 0 2px;
            }}
            
            .content-section {{
                padding: 15px 10px;
            }}
            
            .week-header {{
                padding: 12px;
            }}
            
            .week-header h2 {{
                font-size: 1.3rem;
            }}
            
            .week-header p {{
                font-size: 0.9rem;
            }}
            
            .event-card {{
                padding: 15px;
            }}
            
            .event-title {{
                font-size: 1.1rem;
            }}
            
            .event-date {{
                font-size: 0.8rem;
                padding: 5px 10px;
            }}
            
            .event-detail {{
                font-size: 0.85rem;
            }}
            
            .event-description {{
                font-size: 0.85rem;
            }}
            
            .event-borough {{
                font-size: 0.7rem;
                padding: 3px 8px;
            }}
            
            .event-link a {{
                padding: 8px 16px;
                font-size: 0.8rem;
            }}
            
            .weekly-calendar-table {{
                min-width: 400px;
                font-size: 0.6rem;
            }}
        }}
            </style>
        </head>
<body>
    <div class="container">
        <div class="header">
            <h1>🗽 NYC Free Events Calendar</h1>
            <p>July 2025 • Discover Free Events Across All Boroughs</p>
        </div>
        
        <div class="nav-section">
            <h3>📅 Browse by Week</h3>
            <div class="week-nav">
                {week_navigation}
            </div>
                </div>

        <div class="nav-section">
            <h3>🗺️ Browse by Destination</h3>
            <div class="borough-nav">
                {borough_buttons}
            </div>
        </div>
        
        <div class="view-toggle">
            <button class="toggle-button active" onclick="toggleView('week')">📅 Week View</button>
            <button class="toggle-button" onclick="toggleView('borough')">🗺️ Destination View</button>
        </div>
        
        <!-- Week View -->
        <div id="week-view" class="content-section">
            {week_sections}
        </div>
        
        <!-- Borough View -->
        <div id="borough-view" class="content-section" style="display: none;">
            {borough_sections}
        </div>
    </div>

    <script>
        let currentView = 'week';
        let currentBorough = 'manhattan';
        
        function showWeek(weekIndex) {{
            // Hide all week sections
            document.querySelectorAll('.week-section').forEach(section => {{
                section.classList.remove('active');
            }});
            
            // Show selected week section
            document.getElementById(`week-${{weekIndex}}`).classList.add('active');
            
            // Update navigation buttons
            document.querySelectorAll('.nav-button').forEach(button => {{
                button.classList.remove('active');
            }});
            event.target.classList.add('active');
        }}
        
        function showBorough(borough) {{
            currentBorough = borough;
            
            // Hide all borough sections
            document.querySelectorAll('.borough-section').forEach(section => {{
                section.classList.remove('active');
            }});
            
            // Show selected borough section
            document.getElementById(`borough-${{borough}}`).classList.add('active');
            
            // Update navigation buttons
            document.querySelectorAll('.borough-button').forEach(button => {{
                button.classList.remove('active');
            }});
            event.target.classList.add('active');
            
            // Switch to borough view if not already there
            if (currentView !== 'borough') {{
                toggleView('borough');
            }}
        }}
        
        function toggleView(view) {{
            currentView = view;
            
            // Update toggle buttons
            document.querySelectorAll('.toggle-button').forEach(button => {{
                button.classList.remove('active');
            }});
            event.target.classList.add('active');
            
            // Show/hide appropriate view
            if (view === 'week') {{
                document.getElementById('week-view').style.display = 'block';
                document.getElementById('borough-view').style.display = 'none';
            }} else {{
                document.getElementById('week-view').style.display = 'none';
                document.getElementById('borough-view').style.display = 'block';
            }}
        }}
        
        // Initialize with first week active
        document.addEventListener('DOMContentLoaded', function() {{
            showWeek(0);
            showBorough('manhattan');
        }});
    </script>
</body>
</html>
"""

    # Write the HTML content to the file
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"HTML calendar generated successfully: {os.path.abspath(output_filename)}")
    print("You can open 'nyc_events_calendar.html' in your web browser to view it.")

def get_borough_class(borough):
    """Get CSS class for borough color coding"""
    borough_lower = borough.lower()
    if 'manhattan' in borough_lower:
        return 'manhattan'
    elif 'brooklyn' in borough_lower:
        return 'brooklyn'
    elif 'queens' in borough_lower:
        return 'queens'
    elif 'bronx' in borough_lower:
        return 'bronx'
    elif 'staten island' in borough_lower:
        return 'staten-island'
    elif 'asbury park' in borough_lower:
        return 'asbury-park'
    else:
        return 'other'

def is_event_in_week(event, week_start):
    """Check if an event falls within a given week, supporting date ranges."""
    date_str = event['date']
    week_end = week_start + timedelta(days=6)
    if ' to ' in date_str:
        start_date_str, end_date_str = date_str.split(' to ')
        event_start = datetime.strptime(start_date_str.strip(), '%Y-%m-%d').date()
        event_end = datetime.strptime(end_date_str.strip(), '%Y-%m-%d').date()
        return (event_start <= week_end) and (event_end >= week_start)
    else:
        event_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        return week_start <= event_date <= week_end

def format_date(date_str):
    """Format date string for display"""
    # Handle date ranges like "2025-07-01 to 2025-07-13"
    if ' to ' in date_str:
        start_date = date_str.split(' to ')[0].strip()
        end_date = date_str.split(' to ')[1].strip()
        start_obj = datetime.strptime(start_date, '%Y-%m-%d')
        end_obj = datetime.strptime(end_date, '%Y-%m-%d')
        return f"{start_obj.strftime('%B %d')} - {end_obj.strftime('%B %d, %Y')}"
    else:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%B %d, %Y')

def generate_event_card(event):
    """
    Generate event card with borough color coding and More Info links.
    """
    name = event.get('name', 'Untitled Event')
    date_str = event.get('date', 'Date TBD')
    time_str = event.get('time', 'Time TBD')
    address = event.get('address', 'Location TBD')
    borough = event.get('borough', 'NYC')
    link = event.get('link', '')
    
    # Get borough class for color coding
    borough_class = get_borough_class(borough)
    
    # Format date for display
    formatted_date = format_date(date_str)
    
    # Create description without duplicate address
    description = f"Free event in {borough}"
    
    # If there's additional description content that's NOT the address, use it
    original_description = event.get('description', '')
    if original_description and original_description.strip() != address.strip():
        description = original_description
    
    # Generate the event card HTML with borough class and link
    card_html = f'''
    <div class="event-card {borough_class}" data-borough="{borough.lower()}">
        <div class="event-header">
            <div class="event-title">{name}</div>
            <div class="event-date">{formatted_date}</div>
        </div>
        <div class="event-details">
            <div class="event-detail">
                <i>🕒</i>
                <span class="event-time">{time_str}</span>
            </div>
            <div class="event-detail">
                <i>📍</i>
                <span class="event-address">{address}</span>
            </div>
        </div>
        <div class="event-description">{description}</div>
        <div class="event-borough {borough_class}">{borough}</div>
    '''
    
    # Add link if available
    if link:
        card_html += f'<div class="event-link"><a href="{link}" target="_blank">More Info</a></div>'
    
    card_html += '</div>'
    
    return card_html

def parse_time_for_sorting(time_str):
    """
    Parse various time formats for sorting events chronologically.
    Returns a time object that can be used for sorting.
    """
    if not time_str or time_str.strip() == "":
        return time(23, 59)  # Put empty times at end of day
    
    time_str = time_str.strip().upper()
    
    # Handle TBD cases with intelligent defaults
    if "TBD" in time_str:
        if "MORNING" in time_str:
            return time(9, 0)
        elif "AFTERNOON" in time_str:
            return time(14, 0)
        elif "EVENING" in time_str:
            return time(19, 0)
        else:
            return time(12, 0)  # Default noon for generic TBD
    
    # Handle all-day events
    if "ALL DAY" in time_str:
        return time(0, 0)  # Show all-day events first
    
    # Parse time ranges - extract start time
    # Format: "7:00 PM – 8:30 PM" or "7:00 PM - 8:30 PM"
    time_match = re.search(r'(\d{1,2}):(\d{2})\s*(AM|PM)', time_str)
    if time_match:
        hours = int(time_match.group(1))
        minutes = int(time_match.group(2))
        am_pm = time_match.group(3)
        
        # Convert to 24-hour format
        if am_pm == 'PM' and hours != 12:
            hours += 12
        elif am_pm == 'AM' and hours == 12:
            hours = 0
            
        return time(hours, minutes)
    
    # Handle 24-hour format (e.g., "19:00")
    time_24h_match = re.search(r'(\d{1,2}):(\d{2})', time_str)
    if time_24h_match:
        hours = int(time_24h_match.group(1))
        minutes = int(time_24h_match.group(2))
        return time(hours, minutes)
    
    # Default fallback for unparseable times
    return time(23, 59)

def create_calendar_grid(events_data, year, month, week_start):
    """
    Table-based weekly time grid: header row is days, first column is hours (5am-11pm), TBD row at top.
    """
    # Time slots: TBD, then 5am to 11pm
    time_slots = [("TBD", "TBD")] + [(f"{h:02d}:00", f"{h % 12 or 12}{'am' if h < 12 else 'pm'}") for h in range(5, 24)]
    events_by_date = defaultdict(lambda: defaultdict(list))
    for event in events_data:
        event_date = event.get('date')
        if event_date:
            try:
                if isinstance(event_date, str):
                    date_parts = event_date.split('-')
                    if len(date_parts) == 3:
                        event_year, event_month, event_day = map(int, date_parts)
                        if event_year == year and event_month == month:
                            time_str = event.get('time', 'TBD')
                            slot = "TBD"
                            if 'TBD' not in time_str and 'likely' not in time_str.lower():
                                # Try to extract hour
                                import re
                                match = re.search(r'(\d{1,2}):(\d{2})\s*(AM|PM)', time_str, re.IGNORECASE)
                                if match:
                                    hour = int(match.group(1))
                                    ampm = match.group(3).upper()
                                    if ampm == 'PM' and hour != 12:
                                        hour += 12
                                    elif ampm == 'AM' and hour == 12:
                                        hour = 0
                                    if 5 <= hour <= 23:
                                        slot = f"{hour:02d}:00"
                            events_by_date[event_day][slot].append(event)
            except (ValueError, AttributeError):
                continue
    # Start table
    html = '<div class="weekly-calendar-table-wrapper">'
    html += '<table class="weekly-calendar-table">'
    # Header row
    html += '<tr><th>Time</th>'
    for i in range(7):
        current_date = week_start + timedelta(days=i)
        day_number = current_date.day
        day_name = current_date.strftime('%a')
        html += f'<th>{day_name}<br>{day_number}</th>'
    html += '</tr>'
    # Time slot rows
    for slot, slot_label in time_slots:
        html += f'<tr><th class="time-slot-label">{slot_label}</th>'
        for i in range(7):
            current_date = week_start + timedelta(days=i)
            day_number = current_date.day
            day_events = events_by_date.get(day_number, {}).get(slot, [])
            if day_events:
                html += '<td class="day-cell with-events">'
                for event in day_events:
                    borough_class = get_borough_class(event['borough'])
                    link = event.get('link', '')
                    html += f'<div class="grid-event {borough_class}">' \
                            f'<div class="event-name">{event["name"]}</div>' \
                            f'<div class="event-borough {borough_class}">{event["borough"]}</div>'
                    if link:
                        html += f'<div class="event-link"><a href="{link}" target="_blank">More Info</a></div>'
                    html += '</div>'
                html += '</td>'
            else:
                html += '<td class="day-cell empty"></td>'
        html += '</tr>'
    html += '</table></div>'
    return html

def generate_html():
    """Generate the HTML calendar"""
    # Calculate week starts for July 2025 starting from the first of the month
    events = nyc_free_events_database
    july_start = date(2025, 7, 1)
    july_end = date(2025, 7, 31)
    
    # Start from July 1st and create weeks
    week_starts = []
    current_week_start = july_start
    
    # Create weeks that contain July days
    while current_week_start <= july_end:
        week_starts.append(current_week_start)
        current_week_start += timedelta(days=7)
    
    # Generate iCal content for download
    ical_content = generate_ical_content(events)
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NYC Free Events Calendar - July 2025</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }}
            
            .container {{
                max-width: 1400px;
                margin: 0 auto;
                background: rgba(255, 255, 255, 0.95);
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
                overflow: hidden;
            }}
            
            .header {{
                background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
                color: white;
                text-align: center;
                padding: 40px 20px;
            }}
            
            .header h1 {{
                font-size: 2.5rem;
                margin-bottom: 10px;
                font-weight: 300;
            }}
            
            .header p {{
                font-size: 1.2rem;
                opacity: 0.9;
                margin-bottom: 20px;
            }}
            
            .download-section {{
                background: rgba(255, 255, 255, 0.1);
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0;
            }}
            
            .download-button {{
                display: inline-block;
                background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
                color: white;
                padding: 15px 30px;
                border-radius: 25px;
                text-decoration: none;
                font-weight: 600;
                transition: all 0.3s ease;
                margin: 10px;
            }}
            
            .download-button:hover {{
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
            }}
            
            .navigation {{
                background: white;
                padding: 20px;
                border-bottom: 1px solid #eee;
            }}
            
            .nav-section {{
                margin-bottom: 20px;
            }}
            
            .nav-section h3 {{
                margin-bottom: 15px;
                color: #2c3e50;
                font-size: 1.1rem;
            }}
            
            .nav-buttons {{
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
                margin-bottom: 20px;
            }}
            
            .nav-button {{
                padding: 12px 20px;
                border: none;
                border-radius: 25px;
                background: #ecf0f1;
                color: #2c3e50;
                cursor: pointer;
                transition: all 0.3s ease;
                font-weight: 500;
                text-decoration: none;
                display: inline-block;
            }}
            
            .nav-button:hover {{
                background: #bdc3c7;
                transform: translateY(-2px);
            }}
            
            .nav-button.active {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }}
            
            .view-toggle {{
                display: flex;
                gap: 10px;
                margin-bottom: 20px;
            }}
            
            .toggle-button {{
                padding: 10px 20px;
                border: 2px solid #667eea;
                background: white;
                color: #667eea;
                border-radius: 25px;
                cursor: pointer;
                transition: all 0.3s ease;
                font-weight: 500;
            }}
            
            .toggle-button:hover {{
                background: #667eea;
                color: white;
            }}
            
            .toggle-button.active {{
                background: #667eea;
                color: white;
            }}
            
            .borough-buttons {{
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
                justify-content: center;
                margin-bottom: 20px;
            }}
            
            .borough-button {{
                padding: 12px 20px;
                border: none;
                border-radius: 25px;
                color: white;
                cursor: pointer;
                transition: all 0.3s ease;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                font-size: 0.9rem;
            }}
            
            .borough-button.manhattan {{ background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); }}
            .borough-button.brooklyn {{ background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%); }}
            .borough-button.queens {{ background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); }}
            .borough-button.bronx {{ background: linear-gradient(135deg, #feca57 0%, #ff9ff3 100%); }}
            .borough-button.staten-island {{ background: linear-gradient(135deg, #a8e6cf 0%, #dcedc1 100%); color: #333; }}
            .borough-button.asbury-park {{ background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%); color: #333; }}
            
            .borough-button:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
            }}
            
            .borough-button.active {{
                transform: scale(1.1);
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
            }}
            
            .content-section {{
                background: rgba(255, 255, 255, 0.95);
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                margin-bottom: 20px;
            }}
            
            .week-section {{
                display: none;
                animation: fadeIn 0.5s ease-in;
            }}
            
            .week-section.active {{
                display: block;
            }}
            
            .borough-section {{
                display: none;
                animation: fadeIn 0.5s ease-in;
            }}
            
            .borough-section.active {{
                display: block;
            }}
            
            .week-header {{
                text-align: center;
                margin-bottom: 30px;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-radius: 10px;
            }}
            
            .week-header h2 {{
                font-size: 2rem;
                margin-bottom: 10px;
            }}
            
            .week-header p {{
                font-size: 1.1rem;
                opacity: 0.9;
            }}
            
            /* Calendar Grid Layout */
            .calendar-grid {{
                display: grid;
                grid-template-columns: repeat(7, 1fr);
                gap: 1px;
                background: #e0e0e0;
                border-radius: 10px;
                overflow: hidden;
                margin-top: 20px;
                min-height: 600px;
            }}
            
            .calendar-day-header {{
                background: #2c3e50;
                color: white;
                padding: 12px 8px;
                text-align: center;
                font-weight: 600;
                font-size: 0.85rem;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            
            .calendar-day {{
                background: white;
                min-height: 140px;
                padding: 8px;
                border: 1px solid #f0f0f0;
                position: relative;
                display: flex;
                flex-direction: column;
            }}
            
            .calendar-day.empty {{
                background: #f8f9fa;
                color: #ccc;
            }}
            
            .day-number {{
                font-weight: 600;
                color: #2c3e50;
                margin-bottom: 6px;
                font-size: 1rem;
                text-align: center;
                padding: 2px;
                border-radius: 3px;
            }}
            
            .calendar-day.empty .day-number {{
                color: #ccc;
            }}
            
            .day-events {{
                display: flex;
                flex-direction: column;
                gap: 3px;
                flex: 1;
                overflow-y: auto;
            }}
            
            .day-event {{
                background: white;
                border-radius: 4px;
                padding: 4px 6px;
                font-size: 0.7rem;
                border-left: 2px solid #ddd;
                cursor: pointer;
                transition: all 0.2s ease;
                box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
                margin-bottom: 2px;
            }}
            
            .day-event:hover {{
                transform: translateY(-1px);
                box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
                z-index: 10;
            }}
            
            .day-event.manhattan {{ border-left-color: #ff6b6b; }}
            .day-event.brooklyn {{ border-left-color: #4ecdc4; }}
            .day-event.queens {{ border-left-color: #3498db; }}
            .day-event.bronx {{ border-left-color: #feca57; }}
            .day-event.staten-island {{ border-left-color: #a8e6cf; }}
            .day-event.asbury-park {{ border-left-color: #d1ecf1; }}
            
            .day-event-name {{
                font-weight: 600;
                color: #2c3e50;
                margin-bottom: 2px;
                line-height: 1.1;
                font-size: 0.65rem;
            }}
            
            .day-event-time {{
                color: #7f8c8d;
                font-size: 0.6rem;
                margin-bottom: 2px;
            }}
            
            .day-event-borough {{
                display: inline-block;
                padding: 1px 4px;
                border-radius: 6px;
                font-size: 0.55rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.3px;
            }}
            
            .day-event-borough.manhattan {{ background: #ff6b6b; color: white; }}
            .day-event-borough.brooklyn {{ background: #4ecdc4; color: white; }}
            .day-event-borough.queens {{ background: #3498db; color: white; }}
            .day-event-borough.bronx {{ background: #feca57; color: #333; }}
            .day-event-borough.staten-island {{ background: #a8e6cf; color: #333; }}
            .day-event-borough.asbury-park {{ background: #d1ecf1; color: #333; }}
            
            .day-event-more {{
                text-align: center;
                color: #7f8c8d;
                font-size: 0.7rem;
                font-style: italic;
                padding: 5px;
            }}
            
            .events-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                gap: 20px;
                margin-top: 20px;
            }}
            
            .event-card {{
                background: white;
                border-radius: 15px;
                padding: 25px;
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
                transition: all 0.3s ease;
                border-left: 6px solid #ddd;
                position: relative;
                overflow: hidden;
            }}
            
            .event-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
            }}
            
            .event-card.manhattan {{ border-left-color: #ff6b6b; }}
            .event-card.brooklyn {{ border-left-color: #4ecdc4; }}
            .event-card.queens {{ border-left-color: #3498db; }}
            .event-card.bronx {{ border-left-color: #feca57; }}
            .event-card.staten-island {{ border-left-color: #a8e6cf; }}
            .event-card.asbury-park {{ border-left-color: #d1ecf1; }}
            
            .event-header {{
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                margin-bottom: 15px;
            }}
            
            .event-title {{
                font-size: 1.3rem;
                font-weight: 600;
                color: #2c3e50;
                margin-bottom: 5px;
                line-height: 1.3;
            }}
            
            .event-date {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 8px 15px;
                border-radius: 20px;
                font-size: 0.9rem;
                font-weight: 500;
            }}
            
            .event-details {{
                margin-bottom: 15px;
            }}
            
            .event-detail {{
                display: flex;
                align-items: center;
                margin-bottom: 8px;
                color: #555;
            }}
            
            .event-detail i {{
                margin-right: 10px;
                color: #667eea;
                width: 16px;
            }}
            
            .event-description {{
                color: #666;
                line-height: 1.6;
                font-size: 0.95rem;
            }}
            
            .event-borough {{
                display: inline-block;
                padding: 6px 12px;
                border-radius: 15px;
                font-size: 0.8rem;
                font-weight: 600;
                text-transform: uppercase;
                margin-top: 10px;
            }}
            
            .event-borough.manhattan {{ background: #ff6b6b; color: white; }}
            .event-borough.brooklyn {{ background: #4ecdc4; color: white; }}
            .event-borough.queens {{ background: #3498db; color: white; }}
            .event-borough.bronx {{ background: #feca57; color: #333; }}
            .event-borough.staten-island {{ background: #a8e6cf; color: #333; }}
            .event-borough.asbury-park {{ background: #d1ecf1; color: #333; }}
            
            @keyframes fadeIn {{
                from {{ opacity: 0; transform: translateY(20px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            
            @media (max-width: 768px) {{
                .calendar-grid {{
                    grid-template-columns: 1fr;
                }}
                
                .calendar-day-header {{
                    display: none;
                }}
                
                .calendar-day {{
                    margin-bottom: 10px;
                    border-radius: 10px;
                }}
                
                .nav-buttons {{
                    flex-direction: column;
                }}
                
                .borough-buttons {{
                    flex-direction: column;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🗽 NYC Free Events Calendar</h1>
                <p>July 2025 • Discover Amazing Free Events Across the City</p>
                <div class="download-section">
                    <h3>📅 Download to Your Calendar</h3>
                    <p>Add all events to your personal calendar (Google Calendar, Outlook, Apple Calendar, etc.)</p>
                    <a href="data:text/calendar;charset=utf-8,{ical_content}" download="nyc_free_events_july_2025.ics" class="download-button">
                        📥 Download Calendar (.ics)
                    </a>
                    <a href="#" onclick="downloadSelectedEvents()" class="download-button">
                        📥 Download Selected Events
                    </a>
                </div>
            </div>
            
            <div class="navigation">
                <div class="nav-section">
                    <h3>📅 View Options</h3>
                    <div class="view-toggle">
                        <button class="toggle-button active" onclick="switchView('week')">Week View</button>
                        <button class="toggle-button" onclick="switchView('destination')">Destination View</button>
                    </div>
                </div>
                
                <div class="nav-section" id="week-nav">
                    <h3>📅 Jump to Week</h3>
                    <div class="nav-buttons">
    """
    
    # Add week navigation buttons
    for i, week_start in enumerate(week_starts):
        week_label = week_start.strftime("Week of %B %d")
        html_content += f'<a href="#" class="nav-button{" active" if i == 0 else ""}" onclick="showWeek({i})">{week_label}</a>'
    
    html_content += """
                    </div>
                </div>
                
                <div class="nav-section" id="destination-nav" style="display: none;">
                    <h3>🗺️ Browse by Destination</h3>
                    <div class="borough-buttons">
                        <button class="borough-button manhattan active" onclick="showBorough('manhattan')">Manhattan</button>
                        <button class="borough-button brooklyn" onclick="showBorough('brooklyn')">Brooklyn</button>
                        <button class="borough-button queens" onclick="showBorough('queens')">Queens</button>
                        <button class="borough-button bronx" onclick="showBorough('bronx')">Bronx</button>
                        <button class="borough-button staten-island" onclick="showBorough('staten-island')">Staten Island</button>
                        <button class="borough-button asbury-park" onclick="showBorough('asbury-park')">Asbury Park</button>
                    </div>
                </div>
            </div>
            
            <div class="content">
    """
    
    # Generate week sections with calendar grid
    for i, week_start in enumerate(week_starts):
        week_events = [event for event in events if is_event_in_week(event, week_start)]
        week_end = week_start + timedelta(days=6)
        
        html_content += f"""
                <div class="week-section{" active" if i == 0 else ""}" id="week-{i}">
                    <div class="week-header">
                        <h2>Week of {week_start.strftime('%B %d')}</h2>
                        <p>{week_start.strftime('%B %d')} - {week_end.strftime('%B %d, %Y')}</p>
                    </div>
                    {create_calendar_grid(week_events, week_start.year, week_start.month, week_start)}
                </div>
        """
    
    # Generate borough sections
    boroughs = ['manhattan', 'brooklyn', 'queens', 'bronx', 'staten-island', 'asbury-park']
    for borough in boroughs:
        borough_events = [event for event in events if get_borough_class(event['borough']) == borough]
        
        html_content += f"""
                <div class="borough-section" id="borough-{borough}">
                    <div class="week-header">
                        <h2>{borough.replace('-', ' ').title()} Events</h2>
                        <p>All free events in {borough.replace('-', ' ').title()}</p>
                    </div>
                    <div class="events-grid">
        """
        
        for event in borough_events:
            borough_class = get_borough_class(event['borough'])
            html_content += generate_event_card(event)
        
        html_content += """
                    </div>
                </div>
        """
            
        html_content += """
                </div>
            </div>
        
        <script>
            function showWeek(weekIndex) {
                // Hide all week sections
                document.querySelectorAll('.week-section').forEach(section => {
                    section.classList.remove('active');
                });
                
                // Show selected week
                document.getElementById(`week-${weekIndex}`).classList.add('active');
                
                // Update navigation buttons
                document.querySelectorAll('#week-nav .nav-button').forEach(button => {
                    button.classList.remove('active');
                });
                event.target.classList.add('active');
            }
            
            function showBorough(borough) {
                // Hide all borough sections
                document.querySelectorAll('.borough-section').forEach(section => {
                    section.classList.remove('active');
                });
                
                // Show selected borough
                document.getElementById(`borough-${borough}`).classList.add('active');
                
                // Update borough buttons
                document.querySelectorAll('.borough-button').forEach(button => {
                    button.classList.remove('active');
                });
                event.target.classList.add('active');
            }
            
            function switchView(view) {
                const weekNav = document.getElementById('week-nav');
                const destinationNav = document.getElementById('destination-nav');
                const toggleButtons = document.querySelectorAll('.toggle-button');
                
                if (view === 'week') {
                    weekNav.style.display = 'block';
                    destinationNav.style.display = 'none';
                    
                    // Show first week
                    document.querySelectorAll('.week-section').forEach(section => {
                        section.classList.remove('active');
                    });
                    document.querySelectorAll('.borough-section').forEach(section => {
                        section.classList.remove('active');
                    });
                    document.getElementById('week-0').classList.add('active');
                    
                    // Update toggle buttons
                    toggleButtons[0].classList.add('active');
                    toggleButtons[1].classList.remove('active');
                } else {
                    weekNav.style.display = 'none';
                    destinationNav.style.display = 'block';
                    
                    // Show first borough
                    document.querySelectorAll('.week-section').forEach(section => {
                        section.classList.remove('active');
                    });
                    document.querySelectorAll('.borough-section').forEach(section => {
                        section.classList.remove('active');
                    });
                    document.getElementById('borough-manhattan').classList.add('active');
                    
                    // Update toggle buttons
                    toggleButtons[0].classList.remove('active');
                    toggleButtons[1].classList.add('active');
                }
            }
            
            function showEventDetails(name, date, time, location, borough, description) {
                alert(`Event Details:\\n\\nName: ${name}\\nDate: ${date}\\nTime: ${time}\\nLocation: ${location}\\nBorough: ${borough}\\n\\nDescription: ${description}`);
            }
            
            function downloadSelectedEvents() {
                // This would allow users to select specific events and download them
                alert('Feature coming soon! You can currently download all events using the main download button.');
            }
        </script>
        </body>
        </html>
        """

    return html_content

def generate_ical_content(events):
    """Generate iCal content for calendar download"""
    ical_content = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//NYC Free Events Calendar//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
X-WR-CALNAME:NYC Free Events - July 2025
X-WR-CALDESC:Free events across NYC boroughs and Asbury Park
"""
    
    for event in events:
        # Parse date and time - handle date ranges by using the start date
        date_str = event['date']
        if " to " in date_str:
            # Extract start date from range
            start_date_str = date_str.split(" to ")[0].strip()
            event_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        else:
            event_date = datetime.strptime(date_str, '%Y-%m-%d')
        
        # Create event start time (default to 7 PM if time is TBD)
        time_str = event['time']
        if 'TBD' in time_str or 'likely' in time_str.lower():
            start_time = event_date.replace(hour=19, minute=0)  # 7 PM
        else:
            # Try to parse time like "7:00 PM – 8:30 PM"
            try:
                time_parts = time_str.split('–')[0].strip()
                if 'PM' in time_parts:
                    hour = int(time_parts.split(':')[0])
                    if hour != 12:
                        hour += 12
                    minute = int(time_parts.split(':')[1].split()[0])
                    start_time = event_date.replace(hour=hour, minute=minute)
                elif 'AM' in time_parts:
                    hour = int(time_parts.split(':')[0])
                    if hour == 12:
                        hour = 0
                    minute = int(time_parts.split(':')[1].split()[0])
                    start_time = event_date.replace(hour=hour, minute=minute)
                else:
                    start_time = event_date.replace(hour=19, minute=0)
            except:
                start_time = event_date.replace(hour=19, minute=0)
        
        # Create end time (1 hour later by default)
        end_time = start_time + timedelta(hours=1)
        
        # Format dates for iCal
        start_str = start_time.strftime('%Y%m%dT%H%M%S')
        end_str = end_time.strftime('%Y%m%dT%H%M%S')
        
        # Clean event name and description for iCal
        event_name = event['name'].replace('\n', ' ').replace('\r', ' ')
        event_description = f"Location: {event['address']}\\nBorough: {event['borough']}\\nTime: {event['time']}"
        if 'link' in event:
            event_description += f"\\nMore info: {event['link']}"
        
        ical_content += f"""BEGIN:VEVENT
UID:{event['date']}-{hash(event['name'])}@nycfreeevents.com
DTSTART:{start_str}
DTEND:{end_str}
SUMMARY:{event_name}
DESCRIPTION:{event_description}
LOCATION:{event['address']}
STATUS:CONFIRMED
SEQUENCE:0
END:VEVENT
"""
    
    ical_content += "END:VCALENDAR"
    return ical_content

# --- Execute the HTML generation ---
if __name__ == "__main__":
    # Generate the calendar grid layout
    html_content = generate_html()
    
    # Write to file
    with open("nyc_events_calendar.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("HTML calendar generated successfully: /Users/penny/Desktop/Jobs/Pursuit/NYC Events/active_calendar/nyc_events_calendar.html")
    print("You can open 'nyc_events_calendar.html' in your web browser to view it.")
