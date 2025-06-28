## This script reads event data from nyc_free_events_database
# and generates separate HTML files for each week with Previous/Next navigation.

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
        "name": "Brooklyn Bridge Park Conservancy: Movies With a View",
        "date": "2025-07-10",
        "time": "TBD (likely evening)",
        "address": "Brooklyn Bridge Park, Brooklyn",
        "borough": "Brooklyn",
        "link": "https://www.brooklynbridgepark.org/events"
    },
    {
        "name": "Brooklyn Bridge Park Conservancy: Movies With a View",
        "date": "2025-07-17",
        "time": "TBD (likely evening)",
        "address": "Brooklyn Bridge Park, Brooklyn",
        "borough": "Brooklyn",
        "link": "https://www.brooklynbridgepark.org/events"
    },
    {
        "name": "Brooklyn Bridge Park Conservancy: Movies With a View",
        "date": "2025-07-24",
        "time": "TBD (likely evening)",
        "address": "Brooklyn Bridge Park, Brooklyn",
        "borough": "Brooklyn",
        "link": "https://www.brooklynbridgepark.org/events"
    },
    {
        "name": "Brooklyn Bridge Park Conservancy: Movies With a View",
        "date": "2025-07-31",
        "time": "TBD (likely evening)",
        "address": "Brooklyn Bridge Park, Brooklyn",
        "borough": "Brooklyn",
        "link": "https://www.brooklynbridgepark.org/events"
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
        "name": "2025 Waterfront Summer Concert Series (Astoria Park)",
        "date": "2025-07-17",
        "time": "7:00 PM – 9:00 PM",
        "address": "Great Lawn at Astoria Park, Queens",
        "borough": "Queens",
        "link": "https://www.nycgovparks.org/events/2025/07/17/2025-waterfront-summer-concert-series"
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
        "name": "2025 Waterfront Summer Concert Series (Astoria Park)",
        "date": "2025-07-31",
        "time": "7:00 PM – 9:00 PM",
        "address": "Great Lawn at Astoria Park, Queens",
        "borough": "Queens",
        "link": "https://www.nycgovparks.org/events/2025/07/17/2025-waterfront-summer-concert-series"
    },

    # --- Staten Island Events ---
    {
        "name": "Staten Island Summer Concert Series",
        "date": "2025-07-15",
        "time": "TBD (likely evening)",
        "address": "Various locations, Staten Island",
        "borough": "Staten Island",
        "link": "https://www.nycgovparks.org/events/free_summer_concerts"
    },
    {
        "name": "Staten Island Summer Concert Series",
        "date": "2025-07-22",
        "time": "TBD (likely evening)",
        "address": "Various locations, Staten Island",
        "borough": "Staten Island",
        "link": "https://www.nycgovparks.org/events/free_summer_concerts"
    },
    {
        "name": "Staten Island Summer Concert Series",
        "date": "2025-07-29",
        "time": "TBD (likely evening)",
        "address": "Various locations, Staten Island",
        "borough": "Staten Island",
        "link": "https://www.nycgovparks.org/events/free_summer_concerts"
    },

    # --- Asbury Park, NJ Events ---
    {
        "name": "Asbury Park Boardwalk Summer Concerts",
        "date": "2025-07-05",
        "time": "TBD (likely evening)",
        "address": "Asbury Park Boardwalk, Asbury Park, NJ",
        "borough": "Asbury Park, NJ",
        "link": "https://www.visitasburypark.com/events"
    },
    {
        "name": "Asbury Park Boardwalk Summer Concerts",
        "date": "2025-07-12",
        "time": "TBD (likely evening)",
        "address": "Asbury Park Boardwalk, Asbury Park, NJ",
        "borough": "Asbury Park, NJ",
        "link": "https://www.visitasburypark.com/events"
    },
    {
        "name": "Asbury Park Boardwalk Summer Concerts",
        "date": "2025-07-19",
        "time": "TBD (likely evening)",
        "address": "Asbury Park Boardwalk, Asbury Park, NJ",
        "borough": "Asbury Park, NJ",
        "link": "https://www.visitasburypark.com/events"
    },
    {
        "name": "Asbury Park Boardwalk Summer Concerts",
        "date": "2025-07-26",
        "time": "TBD (likely evening)",
        "address": "Asbury Park Boardwalk, Asbury Park, NJ",
        "borough": "Asbury Park, NJ",
        "link": "https://www.visitasburypark.com/events"
    }
]

def generate_weekly_pages(events_data):
    """
    Generates separate HTML files for each week with Previous/Next navigation,
    including color-coding by borough.

    Args:
        events_data (list of dict): A list of dictionaries with event details.
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

    # Create html_calendar directory if it doesn't exist
    os.makedirs("html_calendar", exist_ok=True)

    # Generate individual HTML files for each week
    for i, week_key in enumerate(sorted_weeks):
        week_number = int(week_key.split('_')[1])
        week_start_date = week_start_date + timedelta(days=week_number * 7)
        week_end_date = week_start_date + timedelta(days=6)
        
        # Create week label for filename and title
        week_label = f"Week of {week_start_date.strftime('%B %d')}, {week_start_date.year}"
        filename = f"week_of_{week_start_date.strftime('%B_%d_%Y').lower()}.html"
        
        # Determine navigation links
        prev_week_link = ""
        next_week_link = ""
        
        if i > 0:
            prev_week_number = int(sorted_weeks[i-1].split('_')[1])
            prev_week_start = week_start_date + timedelta(days=(prev_week_number - week_number) * 7)
            prev_filename = f"week_of_{prev_week_start.strftime('%B_%d_%Y').lower()}.html"
            prev_week_link = f'<a href="{prev_filename}" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full transition duration-300 shadow-md">← Previous Week</a>'
        
        if i < len(sorted_weeks) - 1:
            next_week_number = int(sorted_weeks[i+1].split('_')[1])
            next_week_start = week_start_date + timedelta(days=(next_week_number - week_number) * 7)
            next_filename = f"week_of_{next_week_start.strftime('%B_%d_%Y').lower()}.html"
            next_week_link = f'<a href="{next_filename}" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full transition duration-300 shadow-md">Next Week →</a>'

        # Generate HTML content for this week
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>NYC & NJ Free Events - {week_label}</title>
            <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
            <style>
                body {{ font-family: 'Inter', sans-serif; background-color: #f0f2f5; }}
                .event-card {{
                    border-radius: 0.75rem; /* rounded-lg */
                    box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.1), 0 1px 2px -1px rgba(0, 0, 0, 0.06); /* shadow-sm */
                    margin-bottom: 0.75rem; /* mb-3 */
                    padding: 0.75rem; /* p-3 */
                    transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
                }}
                .event-card:hover {{
                    transform: translateY(-3px);
                    box-shadow: 0 6px 10px -1px rgba(0, 0, 0, 0.15), 0 4px 6px -2px rgba(0, 0, 0, 0.08);
                }}
                .borough-manhattan {{ background-color: #f8d7da; }}
                .borough-brooklyn {{ background-color: #d4edda; }}
                .borough-queens {{ background-color: #cce5ff; }}
                .borough-the-bronx {{ background-color: #fff3cd; }}
                .borough-staten-island {{ background-color: #e2e3e5; }}
                .borough-asbury-park-nj {{ background-color: #d1ecf1; }}
                .borough-manhattan-primary-launch-area {{ background-color: #f8d7da; }} /* Same as Manhattan */
                .borough-brooklyn-accessible-shared {{ background-color: #d4edda; }} /* Same as Brooklyn */
                .event-title {{
                    font-weight: bold;
                    font-size: 1.125rem; /* text-lg */
                    margin-bottom: 0.25rem; /* mb-1 */
                    color: #2d3748; /* gray-800 */
                }}
                .event-detail {{
                    font-size: 0.75rem; /* text-xs */
                    color: #4a5568; /* gray-700 */
                    margin-bottom: 0.125rem; /* mb-px */
                }}
                .event-link {{
                    color: #3182ce; /* blue-600 */
                    text-decoration: underline;
                    word-break: break-all;
                }}
                .day-card {{
                    background-color: #ffffff;
                    border-radius: 0.75rem; /* rounded-lg */
                    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06); /* shadow-sm */
                    padding: 1rem;
                    margin-bottom: 1rem;
                }}
                .day-header {{
                    font-size: 1.25rem; /* text-xl */
                    font-weight: bold;
                    color: #2d3748;
                    margin-bottom: 0.75rem;
                    border-bottom: 2px solid #edf2f7; /* gray-200 */
                    padding-bottom: 0.5rem;
                }}
            </style>
        </head>
        <body class="p-4">
            <div class="max-w-5xl mx-auto">
                <h1 class="text-3xl font-bold text-center text-gray-800 mb-6">NYC & NJ Free Events</h1>
                <h2 class="text-2xl font-semibold text-center text-gray-700 mb-8">{week_label}</h2>

                <div class="flex justify-between mb-8">
                    {prev_week_link}
                    {next_week_link}
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        """
        
        # Iterate through days of the week (Monday=1 to Sunday=7)
        for weekday_num in range(1, 8):
            current_day_date = week_start_date + timedelta(days=weekday_num - 1)
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
        </body>
        </html>
        """

        # Write the HTML file
        filepath = os.path.join("html_calendar", filename)
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(html_content)
            print(f"Generated: {filepath}")
        except IOError as e:
            print(f"Error writing HTML file {filepath}: {e}")

    print(f"\nAll weekly HTML files generated in the 'html_calendar' directory.")
    print(f"You can open any of these files in your web browser to view individual weeks.")

# --- Execute the HTML generation ---
if __name__ == "__main__":
    generate_weekly_pages(nyc_free_events_database) 