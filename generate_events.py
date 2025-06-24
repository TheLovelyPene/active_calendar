# This script reads event data from nyc_free_events_database
# and generates an HTML file to display the events.

# Import necessary modules
import os

# --- Your NYC Free Events Database (from the previous immersive artifact) ---
# Ensure this data is up-to-date in your actual script
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
        "date": "2025-07-19 to 2025-07-21", # Series runs over these dates
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
        "name": "Summer Market in Cobble Hill",
        "date": "2025-07-26 to 2025-07-27",
        "time": "TBD (likely daytime)",
        "address": "Cobble Hill, Brooklyn",
        "borough": "Brooklyn",
        "link": "https://www.timeout.com/newyork/events-calendar/july-events-calendar"
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
        "date": "July 2025 (specific Fridays TBD)",
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
    {
        "name": "Sunset Wednesdays",
        "date": "Starting 2025-07-09 (likely weekly or bi-weekly)",
        "time": "TBD (likely evening)",
        "address": "Wave Hill, The Bronx",
        "borough": "The Bronx",
        "link": "https://www.reddit.com/r/visitingnyc/comments/1kqmg4t/what_to_do_in_nyc_summer_2025_read_this_before/"
    },

    # --- Staten Island Events ---
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
        "date": "2025-07-26 to 2025-07-27", # Series runs over these dates
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
]

# Define colors for each borough (you can customize these)
# These colors will be used for the background of each event card.
BOROUGH_COLORS = {
    "Manhattan": "#f8d7da",  # Light red/pink
    "Brooklyn": "#d4edda",   # Light green
    "Queens": "#cce5ff",     # Light blue
    "The Bronx": "#fff3cd",  # Light yellow
    "Staten Island": "#e2e3e5", # Light grey
    "Manhattan (Primary launch area)": "#f8d7da", # Same as Manhattan
    "Brooklyn (accessible, shared)": "#d4edda" # Same as Brooklyn
}

def generate_events_html(events_data, output_filename="nyc_events_calendar.html"):
    """
    Generates an HTML file from the provided events data,
    color-coding events by borough.

    Args:
        events_data (list of dict): A list of dictionaries, where each
                                     dictionary contains event details.
        output_filename (str): The name of the HTML file to create.
    """
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NYC Free Events - July 2025</title>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        <style>
            body { font-family: 'Inter', sans-serif; background-color: #f0f2f5; }
            .event-card {
                border-radius: 0.75rem; /* rounded-lg */
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06); /* shadow-md */
                margin-bottom: 1rem; /* mb-4 */
                padding: 1rem; /* p-4 */
            }
            .borough-manhattan { background-color: #f8d7da; } /* Light Red */
            .borough-brooklyn { background-color: #d4edda; }  /* Light Green */
            .borough-queens { background-color: #cce5ff; }    /* Light Blue */
            .borough-the-bronx { background-color: #fff3cd; } /* Light Yellow */
            .borough-staten-island { background-color: #e2e3e5; } /* Light Grey */
            .borough-manhattan-primary-launch-area { background-color: #f8d7da; } # Same as Manhattan
            .borough-brooklyn-accessible-shared { background-color: #d4edda; } # Same as Brooklyn
            .event-title {
                font-weight: bold;
                font-size: 1.25rem; /* text-xl */
                margin-bottom: 0.5rem; /* mb-2 */
            }
            .event-detail {
                font-size: 0.875rem; /* text-sm */
                color: #4a5568; /* gray-700 */
                margin-bottom: 0.25rem; /* mb-1 */
            }
            .event-link {
                color: #2b6cb0; /* blue-700 */
                text-decoration: underline;
                word-break: break-all; /* Break long links */
            }
            .borough-header {
                font-size: 1.5rem; /* text-2xl */
                font-weight: bold;
                margin-top: 1.5rem; /* mt-6 */
                margin-bottom: 1rem; /* mb-4 */
                color: #2d3748; /* gray-800 */
            }
        </style>
    </head>
    <body class="p-4">
        <div class="max-w-4xl mx-auto">
            <h1 class="text-3xl font-bold text-center text-gray-800 mb-6">NYC Free Events - July 2025</h1>
            <p class="text-center text-gray-600 mb-8">Festivals, Fairs, and Concerts</p>
    """

    # Sort events by date to display them chronologically
    sorted_events = sorted(events_data, key=lambda x: x["date"])

    current_borough = ""
    for event in sorted_events:
        # Clean up borough name for CSS class
        # This converts "Manhattan (Primary launch area)" to "manhattan-primary-launch-area"
        borough_class = event["borough"].lower().replace(" ", "-").replace("(", "").replace(")", "")

        # Add a new borough header if the borough changes
        if event["borough"] != current_borough:
            html_content += f'<h2 class="borough-header">{event["borough"]}</h2>\n'
            current_borough = event["borough"]

        html_content += f"""
            <div class="event-card borough-{borough_class}">
                <div class="event-title">{event["name"]}</div>
                <div class="event-detail"><strong>Date:</strong> {event["date"]}</div>
                <div class="event-detail"><strong>Time:</strong> {event["time"]}</div>
                <div class="event-detail"><strong>Address:</strong> {event["address"]}</div>
                <div class="event-detail"><strong>Borough:</strong> {event["borough"]}</div>
                <div class="event-detail"><strong>Link:</strong> <a href="{event["link"]}" target="_blank" class="event-link">{event["link"]}</a></div>
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
    generate_events_html(nyc_free_events_database)
