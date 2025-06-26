import React, { useState } from 'react';
import './App.css';

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
    name: "Macy's 4th of July Fireworks",
    date: "2025-07-04",
    time: "8:00 PM",
    address: "East River (viewable from Manhattan, Brooklyn, and Queens waterfronts)",
    borough: "Manhattan",
    link: "https://www.timeout.com/newyork/events-calendar/july-events-calendar"
  },
  {
    name: "Nathan's Hot Dog Eating Contest",
    date: "2025-07-04",
    time: "TBD (morning/afternoon)",
    address: "Nathan's Famous, 1310 Surf Ave, Coney Island, Brooklyn",
    borough: "Brooklyn",
    link: "https://www.iloveny.com/blog/post/things-to-do-this-july-in-new-york-state/"
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
    name: "Manhattanhenge (Full Sun on Grid)",
    date: "2025-07-11",
    time: "8:20 PM ET",
    address: "Viewable from 14th, 23rd, 34th, 42nd, 57th Streets (Manhattan)",
    borough: "Manhattan",
    link: "https://www.nycforfree.co/events/manhattanhenge-july-2025"
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
    name: "Carnegie Hall Citywide: Cécile McLorin Salvant",
    date: "2025-07-25",
    time: "7:00 PM",
    address: "Bryant Park Stage, Manhattan",
    borough: "Manhattan",
    link: "https://bryantpark.org/activities/picnic-performances"
  }
];

function App() {
  const [currentWeek, setCurrentWeek] = useState(0);
  
  // Group events by week
  const weeks = [];
  const weekStarts = [
    new Date('2025-06-30'),
    new Date('2025-07-07'),
    new Date('2025-07-14'),
    new Date('2025-07-21'),
    new Date('2025-07-28')
  ];
  
  weekStarts.forEach((weekStart, index) => {
    const weekEnd = new Date(weekStart);
    weekEnd.setDate(weekEnd.getDate() + 6);
    
    const weekEvents = nycEvents.filter(event => {
      const eventDate = new Date(event.date);
      return eventDate >= weekStart && eventDate <= weekEnd;
    });
    
    weeks.push({
      start: weekStart,
      end: weekEnd,
      events: weekEvents
    });
  });

  const getBoroughColor = (borough) => {
    const colors = {
      'Manhattan': '#ff6b6b',
      'Brooklyn': '#4ecdc4',
      'Queens': '#45b7d1',
      'Bronx': '#96ceb4',
      'Staten Island': '#feca57'
    };
    return colors[borough] || '#ddd';
  };

  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { 
      weekday: 'short', 
      month: 'short', 
      day: 'numeric' 
    });
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>NYC Free Events Calendar - July 2025</h1>
        <div className="week-navigation">
          {weeks.map((week, index) => (
            <button
              key={index}
              onClick={() => setCurrentWeek(index)}
              className={currentWeek === index ? 'active' : ''}
            >
              Week of {week.start.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
            </button>
          ))}
        </div>
      </header>
      
      <main className="calendar-content">
        <div className="week-header">
          <h2>Week of {weeks[currentWeek]?.start.toLocaleDateString('en-US', { 
            month: 'long', 
            day: 'numeric', 
            year: 'numeric' 
          })}</h2>
        </div>
        
        <div className="events-grid">
          {weeks[currentWeek]?.events.length > 0 ? (
            weeks[currentWeek].events.map((event, index) => (
              <div 
                key={index} 
                className="event-card"
                style={{ borderLeft: `4px solid ${getBoroughColor(event.borough)}` }}
              >
                <h3>{event.name}</h3>
                <p className="event-date">{formatDate(event.date)}</p>
                <p className="event-time">{event.time}</p>
                <p className="event-address">{event.address}</p>
                <p className="event-borough">{event.borough}</p>
                <a href={event.link} target="_blank" rel="noopener noreferrer" className="event-link">
                  More Info
                </a>
              </div>
            ))
          ) : (
            <p className="no-events">No events scheduled for this week</p>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;

