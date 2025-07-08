import React from 'react';
import './App.css';
import EventsFromFirestore from './components/EventsFromFirestore';

// NYC Free Events Database
const nycEvents = [
  {
    name: "Hudson River Park's Jazz at Pier 84",
    date: "2025-07-02",
    time: "7:00 PM – 8:30 PM",
    address: "Hudson River Park's Pier 84, Manhattan",
    borough: "Manhattan",
    link: "https://www.nycgovparks.org/events/free_summer_concerts"
  },
  {
    name: "NY Classical presents: All's Well That Ends Well",
    date: "2025-07-02",
    time: "7:00 PM – 9:00 PM",
    address: "Castle Clinton (in The Battery), Manhattan",
    borough: "Manhattan",
    link: "https://www.nycgovparks.org/events/free_summer_concerts"
  },
  {
    name: "NY Classical presents: All's Well That Ends Well",
    date: "2025-07-06",
    time: "7:00 PM – 9:00 PM",
    address: "Castle Clinton (in The Battery), Manhattan",
    borough: "Manhattan",
    link: "https://www.nycgovparks.org/events/free_summer_concerts"
  },
  {
    name: "New York Guitar Festival: Pedro Cortes Flamenco, Big Lazy, Marel Hidalgo",
    date: "2025-07-03",
      time: "7:00 PM",
    address: "Bryant Park Stage, Manhattan",
    borough: "Manhattan",
    link: "https://bryantpark.org/activities/picnic-performances"
  },
  {
    name: "New York Guitar Festival: Louis Cato, Jackie Venson, Jontavious Willis",
    date: "2025-07-04",
    time: "7:00 PM",
    address: "Bryant Park Stage, Manhattan",
    borough: "Manhattan",
    link: "https://bryantpark.org/activities/picnic-performances"
  },
  {
    name: "Macy's 4th of July Fireworks",
    date: "2025-07-04",
      time: "8:00 PM",
    address: "East River (viewable from Manhattan, Brooklyn, and Queens waterfronts)",
    borough: "Manhattan",
    link: "https://www.timeout.com/newyork/events-calendar/july-events-calendar"
  },
  {
    name: "East Village Street Fair",
    date: "2025-07-05",
    time: "10:00 AM",
    address: "East Village (exact location TBD, likely main streets), Manhattan",
    borough: "Manhattan",
    link: "https://www.clubfreetime.com/new-york-city-nyc/free-fair/2025-07-05/event/688018"
  },
  {
    name: "Taikoza Drumming Performance",
    date: "2025-07-08",
    time: "3:00 PM – 4:00 PM",
    address: "Jackie Robinson Park - Bandshell, Manhattan",
    borough: "Manhattan",
    link: "https://www.nycgovparks.org/events/free_summer_concerts"
  },
  {
    name: "Reading Rhythms at Hudson Yards",
    date: "2025-07-08",
    time: "TBD (likely daytime/evening)",
    address: "Hudson Yards, Manhattan",
    borough: "Manhattan",
    link: "https://www.nycforfree.co/events"
  },
  {
    name: "Carnegie Hall Citywide: Toomai String Quintet",
    date: "2025-07-09",
    time: "TBD (likely evening)",
    address: "Madison Square Park, Manhattan",
    borough: "Manhattan",
    link: "https://www.carnegiehall.org/About/Press/Press-Releases/2025/04/15/Carnegie-Hall-Citywide-Announces-20252026-Season-with-Free-Performances-Across-NYC"
  },
  {
    name: "River & Blues Concert Series (Maggie Rose)",
    date: "2025-07-10",
    time: "TBD (likely evening)",
    address: "Rockefeller Park, Battery Park City, Manhattan",
    borough: "Manhattan",
    link: "https://secretnyc.co/free-summer-concerts-2025-full-list/"
  },
  {
    name: "Carnegie Hall Citywide: The Knights with Julien Labro",
    date: "2025-07-11",
    time: "7:00 PM",
    address: "Bryant Park Stage, Manhattan",
    borough: "Manhattan",
    link: "https://bryantpark.org/activities/picnic-performances"
  },
  {
    name: "Manhattanhenge (Full Sun on Grid)",
    date: "2025-07-11",
    time: "8:20 PM ET",
    address: "Viewable from 14th, 23rd, 34th, 42nd, 57th Streets (Manhattan)",
    borough: "Manhattan",
    link: "https://www.nycforfree.co/events/manhattanhenge-july-2025"
  },
  {
    name: "Manhattanhenge (Half Sun on Grid)",
    date: "2025-07-12",
    time: "8:22 PM ET",
    address: "Viewable from 14th, 23rd, 34th, 42nd, 57th Streets (Manhattan)",
    borough: "Manhattan",
    link: "https://www.nycforfree.co/events/manhattanhenge-july-2025"
  },
  {
    name: "Carnegie Hall Citywide: Ziggy and Miles",
    date: "2025-07-16",
    time: "6:00 PM",
    address: "Madison Square Park, Manhattan",
    borough: "Manhattan",
    link: "https://www.carnegiehall.org/About/Press/Press-Releases/2025/04/15/Carnegie-Hall-Citywide-Announces-20252026-Season-with-Free-Performances-Across-NYC"
  },
  {
    name: "Hudson River Park's Jazz at Pier 84",
    date: "2025-07-16",
    time: "7:00 PM – 8:30 PM",
    address: "Hudson River Park's Pier 84, Manhattan",
    borough: "Manhattan",
    link: "https://www.nycgovparks.org/events/free_summer_concerts"
  },
  {
    name: "River & Blues Concert Series (Amythyst Kiah)",
    date: "2025-07-17",
    time: "TBD (likely evening)",
    address: "Rockefeller Park, Battery Park City, Manhattan",
    borough: "Manhattan",
    link: "https://secretnyc.co/free-summer-concerts-2025-full-list/"
  },
  {
    name: "Carnegie Hall Citywide: La Excelencia",
    date: "2025-07-18",
    time: "7:00 PM",
    address: "Bryant Park Stage, Manhattan",
    borough: "Manhattan",
    link: "https://bryantpark.org/activities/picnic-performances"
  },
  {
    name: "Carnegie Hall Citywide: Catalyst Quartet",
    date: "2025-07-23",
    time: "TBD (likely evening)",
    address: "Madison Square Park, Manhattan",
    borough: "Manhattan",
    link: "https://www.carnegiehall.org/About/Press/Press-Releases/2025/04/15/Carnegie-Hall-Citywide-Announces-20252026-Season-with-Free-Performances-Across-NYC"
  },
  {
    name: "River & Blues Concert Series (Afro Latin Jazz Orchestra)",
    date: "2025-07-24",
    time: "TBD (likely evening)",
    address: "Rockefeller Park, Battery Park City, Manhattan",
    borough: "Manhattan",
    link: "https://secretnyc.co/free-summer-concerts-2025-full-list/"
  },
  {
    name: "Carnegie Hall Citywide: Cécile McLorin Salvant",
    date: "2025-07-25",
    time: "7:00 PM",
    address: "Bryant Park Stage, Manhattan",
    borough: "Manhattan",
    link: "https://bryantpark.org/activities/picnic-performances"
  },
  {
    name: "Summer Streets NYC",
    date: "2025-07-26",
    time: "7:00 AM – 3:00 PM",
    address: "Park Avenue & other car-free streets, Manhattan",
    borough: "Manhattan",
    link: "https://www.unlimitedbiking.com/blog/bike-events/summer-streets-nyc-2025-a-car-free-celebration-of-the-city/"
  },
  {
    name: "Hudson River Park's Jazz at Pier 84",
    date: "2025-07-30",
    time: "7:00 PM – 8:30 PM",
    address: "Hudson River Park's Pier 84, Manhattan",
    borough: "Manhattan",
    link: "https://www.nycgovparks.org/events/free_summer_concerts"
  },
  {
    name: "River & Blues Concert Series (Lady Blackbird)",
    date: "2025-07-31",
    time: "TBD (likely evening)",
    address: "Rockefeller Park, Battery Park City, Manhattan",
    borough: "Manhattan",
    link: "https://secretnyc.co/free-summer-concerts-2025-full-list/"
  },

  // Brooklyn Events
  {
    name: "Nathan's Hot Dog Eating Contest",
    date: "2025-07-04",
    time: "TBD (morning/afternoon)",
    address: "Nathan's Famous, 1310 Surf Ave, Coney Island, Brooklyn",
    borough: "Brooklyn",
    link: "https://www.iloveny.com/blog/post/things-to-do-this-july-in-new-york-state/"
  },
  {
    name: "Flatbush Avenue Street Fair",
    date: "2025-07-13",
    time: "12:00 PM - 6:00 PM",
    address: "Parkside Ave to Courtelyou Road, Flatbush, Brooklyn",
    borough: "Brooklyn",
    link: "https://brooklynbridgeparents.com/outdoor-festivals-and-street-fairs-in-brooklyn-in-2025/"
  },
  {
    name: "Summer Market at Empire Stores in Dumbo",
    date: "2025-07-12",
    time: "TBD (likely daytime)",
    address: "Empire Stores, Dumbo, Brooklyn",
    borough: "Brooklyn",
    link: "https://www.timeout.com/newyork/events-calendar/july-events-calendar"
  },
  {
    name: "BRIC Celebrate Brooklyn! (Still Woozy – Loveseat Tour)",
    date: "2025-07-12",
    time: "TBD (likely evening)",
    address: "Lena Horne Bandshell (Prospect Park), Brooklyn",
    borough: "Brooklyn",
    link: "https://bricartsmedia.org/celebrate-brooklyn/"
  },
  {
    name: "Park Pitch In: Lake Appreciation Month – Boathouse",
    date: "2025-07-13",
    time: "10:30 AM – 12:00 PM",
    address: "Prospect Park Boathouse, 101 East Dr, Prospect Park, Brooklyn",
    borough: "Brooklyn",
    link: "https://www.reddit.com/r/nyc/comments/1li14mo/things-to-do-in-nyc-july-2025/"
  },
  {
    name: "BRIC Celebrate Brooklyn! (Dinosaur Jr. & Snail Mail with Easy Action)",
    date: "2025-07-17",
    time: "TBD (likely evening)",
    address: "Lena Horne Bandshell (Prospect Park), Brooklyn",
    borough: "Brooklyn",
    link: "https://bricartsmedia.org/celebrate-brooklyn/"
  },
  {
    name: "Summer Stroll on Third Avenue",
    date: "2025-07-18",
    time: "6:00 PM - 10:00 PM",
    address: "82nd Street to Marine Avenue, Bay Ridge, Brooklyn",
    borough: "Brooklyn",
    link: "https://brooklynbridgeparents.com/outdoor-festivals-and-street-fairs-in-brooklyn-in-2025/"
  },
  {
    name: "BRIC Celebrate Brooklyn! (Men I Trust and strongboi)",
    date: "2025-07-18",
    time: "TBD (likely evening)",
    address: "Lena Horne Bandshell (Prospect Park), Brooklyn",
    borough: "Brooklyn",
    link: "https://bricartsmedia.org/celebrate-brooklyn/"
  },
  {
    name: "BRIC Celebrate Brooklyn! at Brower Park",
    date: "2025-07-19",
    time: "TBD (likely evening)",
    address: "Brower Park, Brooklyn",
    borough: "Brooklyn",
    link: "https://bricartsmedia.org/celebrate-brooklyn/"
  },
  {
    name: "Rise Up NYC Concert Series (Brooklyn Dates)",
    date: "2025-07-19",
    time: "TBD (check link closer to date)",
    address: "Venue details coming soon, Brooklyn",
    borough: "Brooklyn",
    link: "https://riseupnycconcerts.com/rise-up-nyc-2025-official-dates-announced-for-the-citys-biggest-free-concert-series/"
  },
  {
    name: "Governors Island Market",
    date: "2025-07-19",
    time: "TBD (likely daytime)",
    address: "Governors Island (accessible via ferry from Manhattan or Brooklyn)",
    borough: "Brooklyn",
    link: "https://www.timeout.com/newyork/events-calendar/july-events-calendar"
  },
  {
    name: "Summer Stroll on Third Avenue",
    date: "2025-07-25",
    time: "6:00 PM - 10:00 PM",
    address: "68th Street to 82nd Street, Bay Ridge, Brooklyn",
    borough: "Brooklyn",
    link: "https://brooklynbridgeparents.com/outdoor-festivals-and-street-fairs-in-brooklyn-in-2025/"
  },
  {
    name: "Summer Market in Cobble Hill",
    date: "2025-07-26",
    time: "TBD (likely daytime)",
    address: "Cobble Hill, Brooklyn",
    borough: "Brooklyn",
    link: "https://www.timeout.com/newyork/events-calendar/july-events-calendar"
  },
  {
    name: "FREE art market in Brooklyn",
    date: "2025-07-26",
    time: "1:00 PM - 7:00 PM EDT",
    address: "26 Bridge St, Brooklyn, NY 11201",
    borough: "Brooklyn",
    link: "https://www.eventbrite.co.uk/e/free-art-market-in-brooklyn-tickets-1310673171739"
  },
  {
    name: "FREE Community Fair at Brooklyn RISE Charter School",
    date: "2025-07-26",
    time: "12:00 PM - 4:00 PM",
    address: "9 Hanover Pl, Brooklyn, NY 11217",
    borough: "Brooklyn",
    link: "https://www.eventbrite.com/e/free-community-fair-at-brooklyn-rise-charter-school-tickets-1431990254399?aff=erelexpmlt"
  },
  {
    name: "BRIC Celebrate Brooklyn! (A Tribute to Quincy Jones: The Wiz)",
    date: "2025-07-27",
    time: "TBD (likely evening)",
    address: "Lena Horne Bandshell (Prospect Park), Brooklyn",
    borough: "Brooklyn",
    link: "https://bricartsmedia.org/celebrate-brooklyn/"
  },
  {
    name: "Bats! Night Walk",
    date: "2025-07-31",
    time: "7:30 PM – 9:00 PM",
    address: "Seba Playground, Seba Ave & Gerritsen Ave (Marine Park), Brooklyn",
    borough: "Brooklyn",
    link: "https://www.reddit.com/r/nyc/comments/1li14mo/things-to-do-in-nyc-july-2025/"
  },

  // Queens Events
  {
    name: "2025 Waterfront Summer Concert Series (Astoria Park)",
    date: "2025-07-03",
    time: "7:00 PM – 9:00 PM",
    address: "Great Lawn at Astoria Park, Queens",
    borough: "Queens",
    link: "https://www.nycgovparks.org/events/2025/07/17/2025-waterfront-summer-concert-series"
  },
  {
    name: "2025 Waterfront Summer Concert Series (Astoria Park)",
    date: "2025-07-10",
    time: "7:00 PM – 9:00 PM",
    address: "Great Lawn at Astoria Park, Queens",
    borough: "Queens",
    link: "https://www.nycgovparks.org/events/2025/07/17/2025-waterfront-summer-concert-series"
  },
  {
    name: "Summer Concert Series - Forest Park Trust (Draw the Line - Aerosmith Tribute)",
    date: "2025-07-10",
    time: "7:30 PM",
    address: "George Seuffert, Sr. Bandshell (in Forest Park), Queens",
    borough: "Queens",
    link: "https://forestparktrust.org/events/2024-summer-concert-series-4acsh"
  },
  {
    name: "The Queens Jazz Trail Free Concert Series: Bryan Carrott",
    date: "2025-07-10",
    time: "7:00 PM – 8:00 PM",
    address: "Baisley Pond Park, Jamaica, Queens",
    borough: "Queens",
    link: "https://www.nycgovparks.org/events/free_summer_concerts"
  },
  {
    name: "2025 Waterfront Summer Concert Series (Astoria Park)",
    date: "2025-07-17",
    time: "7:00 PM – 9:00 PM",
    address: "Great Lawn at Astoria Park, Queens",
    borough: "Queens",
    link: "https://www.nycgovparks.org/events/2025/07/17/2025-waterfront-summer-concert-series"
  },
  {
    name: "Summer Concert Series - Forest Park Trust (Zac N' Fried - Zac Brown Tribute)",
    date: "2025-07-17",
    time: "7:30 PM",
    address: "George Seuffert, Sr. Bandshell (in Forest Park), Queens",
    borough: "Queens",
    link: "https://forestparktrust.org/events/2024-summer-concert-series-4acsh"
  },
  {
    name: "Basement Bhangra Beyond",
    date: "2025-07-19",
    time: "6:00 PM",
    address: "Adjacent to Unisphere, Flushing Meadows-Corona Park, Queens",
    borough: "Queens",
    link: "https://qns.com/2025/06/richards-queens-day-july-free-concert-the-roots/"
  },
  {
    name: "Queens Day! (Concert with The Roots)",
    date: "2025-07-20",
    time: "10:00 AM – 8:00 PM (Festivities, concert time TBD)",
    address: "Flushing Meadows Corona Park, Queens",
    borough: "Queens",
    link: "https://allianceforfmcp.org/events/2025/7/20/queens-day"
  },
  {
    name: "2025 Waterfront Summer Concert Series (Astoria Park)",
    date: "2025-07-24",
    time: "7:00 PM – 9:00 PM",
    address: "Great Lawn at Astoria Park, Queens",
    borough: "Queens",
    link: "https://www.nycgovparks.org/events/2025/07/17/2025-waterfront-summer-concert-series"
  },
  {
    name: "Summer Concert Series - Forest Park Trust (Standing Ovation - Musical Theater)",
    date: "2025-07-24",
    time: "7:30 PM",
    address: "George Seuffert, Sr. Bandshell (in Forest Park), Queens",
    borough: "Queens",
    link: "https://forestparktrust.org/events/2024-summer-concert-series-4acsh"
  },
  {
    name: "MoMA PS1 Warm Up",
    date: "2025-07-25",
    time: "TBD (likely evening)",
    address: "MoMA PS1, Long Island City, Queens",
    borough: "Queens",
    link: "https://www.timeout.com/newyork/events-calendar/july-events-calendar"
  },
  {
    name: "2025 Waterfront Summer Concert Series (Astoria Park)",
    date: "2025-07-31",
    time: "7:00 PM – 9:00 PM",
    address: "Great Lawn at Astoria Park, Queens",
    borough: "Queens",
    link: "https://www.nycgovparks.org/events/2025/07/17/2025-waterfront-summer-concert-series"
  },
  {
    name: "Summer Concert Series - Forest Park Trust (Jay Bon Jovi - Bon Jovi Tribute)",
    date: "2025-07-31",
    time: "7:30 PM",
    address: "George Seuffert, Sr. Bandshell (in Forest Park), Queens",
    borough: "Queens",
    link: "https://forestparktrust.org/events/2024-summer-concert-series-4acsh"
  },

  // Staten Island Events
  {
    name: "Our Lady of Mount Carmel Feast / Celebration",
    date: "2025-07-13",
    time: "TBD (check link closer to date)",
    address: "Rosebank, Staten Island",
    borough: "Staten Island",
    link: "https://www.statenbuzz.nyc/article/113/staten-island-street-fairs---staten-island-nyc"
  },
  {
    name: "Cottage Row Curiosities",
    date: "2025-07-19",
    time: "11:00 AM - 4:00 PM",
    address: "Snug Harbor Cultural Center, 1000 Richmond Terrace, Randall Manor, Staten Island",
    borough: "Staten Island",
    link: "https://www.statenbuzz.nyc/article/113/staten-island-street-fairs---staten-island-nyc"
  },
  {
    name: "Stars, Stripes and Staten Sights (Vendor Fair)",
    date: "2025-07-04",
    time: "12:00 PM – 8:00 PM",
    address: "Empire Outlets, 55 Richmond Terrace, Staten Island",
    borough: "Staten Island",
    link: "https://www.siparent.com/4th-of-july-events-in-staten-island-2025/"
  },
  {
    name: "Pizza Party 2025",
    date: "2025-07-26",
    time: "TBD (likely daytime)",
    address: "Snug Harbor Cultural Center & Botanical Garden, Staten Island",
    borough: "Staten Island",
    link: "https://allevents.in/staten-island/festivals"
  },
  {
    name: "Rosebank Street Tree Care (Volunteer Event)",
    date: "2025-07-26",
    time: "10:00 AM – 12:00 PM",
    address: "Von Briesen Park, 1271 Bay St (Shore Acres), Staten Island",
    borough: "Staten Island",
    link: "https://www.reddit.com/r/nyc/comments/1li14mo/things-to-do-in-nyc-july-2025/"
  },
  {
    name: "Rise Up NYC Concert Series (Staten Island Dates)",
    date: "2025-07-26",
    time: "TBD (check link closer to date)",
    address: "Venue details coming soon, Staten Island",
    borough: "Staten Island",
    link: "https://riseupnycconcerts.com/rise-up-nyc-2025-official-dates-announced-for-the-citys-biggest-free-concert-series/"
  },
  {
    name: "Carnegie Hall Citywide: Symphonic Brass Alliance",
    date: "2025-07-26",
    time: "TBD (likely evening)",
    address: "Historic Richmond Town, Staten Island",
    borough: "Staten Island",
    link: "https://secretnyc.co/free-summer-concerts-2025-full-list/"
  },

  // Asbury Park, NJ Events
  {
    name: "Asbury Park Spring Bazaar",
    date: "2025-07-17",
    time: "12:00 PM - 5:00 PM",
    address: "Asbury Park Convention Hall, Asbury Park, NJ",
    borough: "Asbury Park, NJ",
    link: "https://www.njfamily.com/events/asbury-park-spring-bazaar-2025/2025-07-17/"
  },

  // NYC Parks Events (Official NYC Parks Programming)
  {
    name: "Summer on the Hudson: Concert Series",
    date: "2025-07-02",
    time: "6:00 PM - 8:00 PM",
    address: "Riverside Park, 103rd Street, New York, NY 10025",
    borough: "Manhattan",
    link: "https://www.nycgovparks.org/events/summer_on_the_hudson"
  },
  {
    name: "Summer on the Hudson: Movies Under the Stars",
      date: "2025-07-05",
    time: "8:00 PM - 10:00 PM",
    address: "Riverside Park, 91st Street, New York, NY 10024",
    borough: "Manhattan",
    link: "https://www.nycgovparks.org/events/summer_on_the_hudson"
  },
  {
    name: "Summer on the Hudson: Jazz Performance",
    date: "2025-07-09",
    time: "6:00 PM - 8:00 PM",
    address: "Riverside Park, 79th Street, New York, NY 10024",
    borough: "Manhattan",
    link: "https://www.nycgovparks.org/events/summer_on_the_hudson"
  },
  {
    name: "Summer on the Hudson: Family Dance Party",
    date: "2025-07-16",
    time: "6:00 PM - 8:00 PM",
    address: "Riverside Park, 103rd Street, New York, NY 10025",
    borough: "Manhattan",
    link: "https://www.nycgovparks.org/events/summer_on_the_hudson"
  },
  {
    name: "Summer on the Hudson: World Music Night",
    date: "2025-07-23",
    time: "6:00 PM - 8:00 PM",
    address: "Riverside Park, 96th Street, New York, NY 10025",
    borough: "Manhattan",
    link: "https://www.nycgovparks.org/events/summer_on_the_hudson"
  },
  {
    name: "Summer on the Hudson: Kids Show",
    date: "2025-07-30",
    time: "6:00 PM - 7:00 PM",
    address: "Riverside Park, 91st Street, New York, NY 10024",
    borough: "Manhattan",
    link: "https://www.nycgovparks.org/events/summer_on_the_hudson"
  },
  {
    name: "Movies Under the Stars - Central Park",
    date: "2025-07-07",
    time: "8:00 PM - 10:00 PM",
    address: "Central Park Great Lawn, 79th St Transverse, New York, NY 10024",
    borough: "Manhattan",
    link: "https://www.nycgovparks.org/events/free_summer_movies"
  },
  {
    name: "Movies Under the Stars - Bryant Park",
    date: "2025-07-14",
    time: "8:00 PM - 10:00 PM",
    address: "Bryant Park, 1065 Avenue of the Americas, New York, NY 10018",
    borough: "Manhattan",
    link: "https://www.nycgovparks.org/events/free_summer_movies"
  },
  {
    name: "Shakespeare in the Park: Romeo & Juliet",
    date: "2025-07-01",
    time: "8:00 PM - 10:30 PM",
    address: "Delacorte Theater, Central Park, 81st St & Central Park West, New York, NY 10024",
    borough: "Manhattan",
    link: "https://www.nycgovparks.org/events/free_summer_theater"
  },
  {
    name: "Shakespeare in the Park: Romeo & Juliet",
    date: "2025-07-08",
    time: "8:00 PM - 10:30 PM",
    address: "Delacorte Theater, Central Park, 81st St & Central Park West, New York, NY 10024",
    borough: "Manhattan",
    link: "https://www.nycgovparks.org/events/free_summer_theater"
  },
  {
    name: "Shakespeare in the Park: Romeo & Juliet",
    date: "2025-07-15",
    time: "8:00 PM - 10:30 PM",
    address: "Delacorte Theater, Central Park, 81st St & Central Park West, New York, NY 10024",
    borough: "Manhattan",
    link: "https://www.nycgovparks.org/events/free_summer_theater"
  },
  {
    name: "Shakespeare in the Park: Romeo & Juliet",
    date: "2025-07-22",
    time: "8:00 PM - 10:30 PM",
    address: "Delacorte Theater, Central Park, 81st St & Central Park West, New York, NY 10024",
    borough: "Manhattan",
    link: "https://www.nycgovparks.org/events/free_summer_theater"
  },
  {
    name: "Shakespeare in the Park: Romeo & Juliet",
    date: "2025-07-29",
    time: "8:00 PM - 10:30 PM",
    address: "Delacorte Theater, Central Park, 81st St & Central Park West, New York, NY 10024",
    borough: "Manhattan",
    link: "https://www.nycgovparks.org/events/free_summer_theater"
  },
  {
    name: "Bryant Park Picnic Performances",
    date: "2025-07-04",
    time: "12:00 PM - 2:00 PM",
    address: "Bryant Park, 1065 Avenue of the Americas, New York, NY 10018",
    borough: "Manhattan",
    link: "https://www.nycgovparks.org/events"
  },
  {
    name: "Bryant Park Yoga",
    date: "2025-07-11",
    time: "10:00 AM - 11:00 AM",
    address: "Bryant Park, 1065 Avenue of the Americas, New York, NY 10018",
    borough: "Manhattan",
    link: "https://www.nycgovparks.org/events"
  },
  {
    name: "Bryant Park Chess Tournament",
    date: "2025-07-18",
    time: "6:00 PM - 8:00 PM",
    address: "Bryant Park, 1065 Avenue of the Americas, New York, NY 10018",
    borough: "Manhattan",
    link: "https://www.nycgovparks.org/events"
  },
  {
    name: "Bryant Park Reading Room",
    date: "2025-07-25",
    time: "11:00 AM - 7:00 PM",
    address: "Bryant Park, 1065 Avenue of the Americas, New York, NY 10018",
    borough: "Manhattan",
    link: "https://www.nycgovparks.org/events"
  },
  {
    name: "Governors Island Art Fair",
    date: "2025-07-12",
      time: "11:00 AM - 6:00 PM",
    address: "Governors Island, 10 South St, New York, NY 10004",
    borough: "Manhattan",
    link: "https://www.nycgovparks.org/events"
  },
  {
    name: "Governors Island Food Festival",
    date: "2025-07-19",
    time: "12:00 PM - 6:00 PM",
    address: "Governors Island, 10 South St, New York, NY 10004",
    borough: "Manhattan",
    link: "https://www.nycgovparks.org/events"
  },
  {
    name: "Governors Island Jazz Festival",
    date: "2025-07-26",
    time: "2:00 PM - 7:00 PM",
    address: "Governors Island, 10 South St, New York, NY 10004",
    borough: "Manhattan",
    link: "https://www.nycgovparks.org/events"
  },

  // Brooklyn NYC Parks Events
  {
    name: "Prospect Park Bandshell Concert",
    date: "2025-07-06",
    time: "7:30 PM - 9:30 PM",
    address: "Prospect Park Bandshell, 9th St & Prospect Park West, Brooklyn, NY 11215",
    borough: "Brooklyn",
    link: "https://www.nycgovparks.org/parks/prospect-park/events"
  },
  {
    name: "Prospect Park Summer Concert",
    date: "2025-07-13",
    time: "7:30 PM - 9:30 PM",
    address: "Prospect Park Bandshell, 9th St & Prospect Park West, Brooklyn, NY 11215",
    borough: "Brooklyn",
    link: "https://www.nycgovparks.org/parks/prospect-park/events"
  },
  {
    name: "Prospect Park Jazz Concert",
    date: "2025-07-20",
    time: "7:30 PM - 9:30 PM",
    address: "Prospect Park Bandshell, 9th St & Prospect Park West, Brooklyn, NY 11215",
    borough: "Brooklyn",
    link: "https://www.nycgovparks.org/parks/prospect-park/events"
  },
  {
    name: "Prospect Park World Music Night",
    date: "2025-07-27",
    time: "7:30 PM - 9:30 PM",
    address: "Prospect Park Bandshell, 9th St & Prospect Park West, Brooklyn, NY 11215",
    borough: "Brooklyn",
    link: "https://www.nycgovparks.org/parks/prospect-park/events"
  },
  {
    name: "Movies Under the Stars - Prospect Park",
    date: "2025-07-21",
    time: "8:00 PM - 10:00 PM",
    address: "Prospect Park Long Meadow, Prospect Park West, Brooklyn, NY 11215",
    borough: "Brooklyn",
    link: "https://www.nycgovparks.org/events/free_summer_movies"
  },

  // Queens NYC Parks Events
  {
    name: "Queens County Farm Hayrides",
      date: "2025-07-06",
    time: "1:00 PM - 4:00 PM",
    address: "Queens County Farm Museum, 73-50 Little Neck Pkwy, Floral Park, NY 11004",
    borough: "Queens",
    link: "https://www.nycgovparks.org/events"
  },
  {
    name: "Flushing Meadows World Music Festival",
    date: "2025-07-13",
    time: "3:00 PM - 7:00 PM",
    address: "Flushing Meadows Corona Park, Grand Central Pkwy, Flushing, NY 11368",
    borough: "Queens",
    link: "https://www.nycgovparks.org/events"
  },
  {
    name: "Forest Park Summer Concert",
    date: "2025-07-20",
    time: "6:00 PM - 8:00 PM",
    address: "Forest Park, Forest Park Dr, Woodhaven, NY 11421",
    borough: "Queens",
    link: "https://www.nycgovparks.org/events"
  },
  {
    name: "Alley Pond Park Nature Walk",
    date: "2025-07-27",
    time: "10:00 AM - 12:00 PM",
    address: "Alley Pond Park, 228-06 Northern Blvd, Douglaston, NY 11362",
    borough: "Queens",
    link: "https://www.nycgovparks.org/events"
  },
  {
    name: "Movies Under the Stars - Flushing Meadows",
    date: "2025-07-28",
    time: "8:00 PM - 10:00 PM",
    address: "Flushing Meadows Corona Park, Grand Central Pkwy, Flushing, NY 11368",
    borough: "Queens",
    link: "https://www.nycgovparks.org/events/free_summer_movies"
  },

  // The Bronx NYC Parks Events
  {
    name: "Bronx River Festival",
    date: "2025-07-05",
    time: "12:00 PM - 5:00 PM",
    address: "Bronx River Park, E 177th St & Southern Blvd, Bronx, NY 10460",
    borough: "The Bronx",
    link: "https://www.nycgovparks.org/events"
  },
  {
    name: "Van Cortlandt Park Summer Concert",
    date: "2025-07-12",
    time: "7:00 PM - 9:00 PM",
    address: "Van Cortlandt Park, Van Cortlandt Park S, Bronx, NY 10463",
    borough: "The Bronx",
    link: "https://www.nycgovparks.org/events"
  },
  {
    name: "Pelham Bay Park Nature Festival",
    date: "2025-07-19",
    time: "11:00 AM - 4:00 PM",
    address: "Pelham Bay Park, Bruckner Blvd & Wilkinson Ave, Bronx, NY 10461",
    borough: "The Bronx",
    link: "https://www.nycgovparks.org/events"
  },
  {
    name: "Crotona Park Summer Festival",
    date: "2025-07-26",
    time: "2:00 PM - 6:00 PM",
    address: "Crotona Park, Crotona Ave & E 173rd St, Bronx, NY 10457",
    borough: "The Bronx",
    link: "https://www.nycgovparks.org/events"
  },

  // Staten Island NYC Parks Events
  {
    name: "Staten Island Boardwalk Summer Concert",
    date: "2025-07-05",
    time: "7:00 PM - 9:00 PM",
    address: "Franklin D. Roosevelt Boardwalk, Staten Island, NY 10305",
    borough: "Staten Island",
    link: "https://www.nycgovparks.org/events"
  },
  {
    name: "Conference House Park Cultural Festival",
      date: "2025-07-12",
    time: "1:00 PM - 5:00 PM",
    address: "Conference House Park, 298 Satterlee St, Staten Island, NY 10307",
    borough: "Staten Island",
    link: "https://www.nycgovparks.org/events"
  },
  {
    name: "Great Kills Park Beach Concert",
    date: "2025-07-19",
    time: "6:00 PM - 8:00 PM",
    address: "Great Kills Park, Hylan Blvd, Staten Island, NY 10308",
    borough: "Staten Island",
    link: "https://www.nycgovparks.org/events"
  },
  {
    name: "Snug Harbor Cultural Festival",
    date: "2025-07-26",
    time: "2:00 PM - 6:00 PM",
    address: "Snug Harbor Cultural Center, 1000 Richmond Terrace, Staten Island, NY 10301",
    borough: "Staten Island",
    link: "https://www.nycgovparks.org/events"
  }
];

function App() {
  return (
    <div className="App">
      <EventsFromFirestore />
    </div>
  );
}

export default App;

