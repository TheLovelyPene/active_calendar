import React, { useState, useEffect } from 'react';
import { eventService } from '../services/eventService';

const DAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
const START_HOUR = 5;
const END_HOUR = 22;

function getStartOfWeek(date) {
  const d = new Date(date);
  const day = d.getDay();
  d.setDate(d.getDate() - day);
  d.setHours(0, 0, 0, 0);
  return d;
}

function addDays(date, days) {
  const d = new Date(date);
  d.setDate(d.getDate() + days);
  return d;
}

function formatHour(hour) {
  const ampm = hour < 12 ? 'AM' : 'PM';
  const h = hour % 12 === 0 ? 12 : hour % 12;
  return `${h}:00 ${ampm}`;
}

function getEventTimeHour(event) {
  if (!event.time) return null;
  // Try to extract hour from time string (e.g., '7:00 PM')
  const match = event.time.match(/(\d{1,2}):(\d{2})?\s*(AM|PM)/i);
  if (!match) return null;
  let hour = parseInt(match[1], 10);
  if (/PM/i.test(match[3]) && hour !== 12) hour += 12;
  if (/AM/i.test(match[3]) && hour === 12) hour = 0;
  return hour;
}

const getBoroughColor = (borough) => {
  const colors = {
    'Manhattan': '#ff6b6b',
    'Brooklyn': '#4ecdc4',
    'Queens': '#3498db',
    'The Bronx': '#feca57',
    'Staten Island': '#a8e6cf',
    'Asbury Park, NJ': '#d1ecf1'
  };
  return colors[borough] || '#ddd';
};

const WeekViewCalendar = () => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentWeekStart, setCurrentWeekStart] = useState(getStartOfWeek(new Date()));

  useEffect(() => {
    const fetchEvents = async () => {
      setLoading(true);
      try {
        const allEvents = await eventService.getAllEvents();
        setEvents(allEvents);
        setError(null);
      } catch (err) {
        setError('Failed to load events');
      } finally {
        setLoading(false);
      }
    };
    fetchEvents();
  }, []);

  // Filter events for the current week
  const weekEvents = events.filter(event => {
    if (!event.date) return false;
    const eventDate = new Date(event.date);
    return eventDate >= currentWeekStart && eventDate < addDays(currentWeekStart, 7);
  });

  // Map events by day and hour
  const eventsByDayHour = {};
  for (let d = 0; d < 7; d++) {
    eventsByDayHour[d] = {};
    for (let h = START_HOUR; h <= END_HOUR; h++) {
      eventsByDayHour[d][h] = [];
    }
  }
  weekEvents.forEach(event => {
    const eventDate = new Date(event.date);
    const day = eventDate.getDay();
    const hour = getEventTimeHour(event) || START_HOUR;
    if (eventsByDayHour[day] && eventsByDayHour[day][hour]) {
      eventsByDayHour[day][hour].push(event);
    }
  });

  const handlePrevWeek = () => {
    setCurrentWeekStart(addDays(currentWeekStart, -7));
  };
  const handleNextWeek = () => {
    setCurrentWeekStart(addDays(currentWeekStart, 7));
  };

  const weekLabel = () => {
    const end = addDays(currentWeekStart, 6);
    return `${currentWeekStart.toLocaleDateString()} - ${end.toLocaleDateString()}`;
  };

  return (
    <div style={{ maxWidth: 1200, margin: '0 auto', padding: 20 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
        <button onClick={handlePrevWeek}>Previous Week</button>
        <h2>Week of {weekLabel()}</h2>
        <button onClick={handleNextWeek}>Next Week</button>
      </div>
      <div style={{ overflowX: 'auto' }}>
        <table style={{ borderCollapse: 'collapse', width: '100%' }}>
          <thead>
            <tr>
              <th style={{ width: 80, background: '#f8f9fa' }}></th>
              {DAYS.map(day => (
                <th key={day} style={{ padding: 8, background: '#f8f9fa', textAlign: 'center' }}>{day}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {Array.from({ length: END_HOUR - START_HOUR + 1 }, (_, i) => START_HOUR + i).map(hour => (
              <tr key={hour}>
                <td style={{ padding: 4, background: '#f8f9fa', textAlign: 'right', fontWeight: 600 }}>{formatHour(hour)}</td>
                {DAYS.map((_, dayIdx) => (
                  <td key={dayIdx} style={{ minWidth: 120, border: '1px solid #e9ecef', verticalAlign: 'top', padding: 2 }}>
                    {eventsByDayHour[dayIdx][hour].map(event => (
                      <div key={event.id} style={{ background: getBoroughColor(event.borough), color: '#222', borderRadius: 8, margin: '2px 0', padding: 4 }}>
                        <strong>{event.name}</strong>
                        <div style={{ fontSize: 12 }}>{event.time || 'TBD'}</div>
                        <div style={{ fontSize: 12 }}>{event.borough}</div>
                        <div style={{ fontSize: 12 }}>{event.address}</div>
                        {event.link && (
                          <a href={event.link} target="_blank" rel="noopener noreferrer" style={{ color: '#007bff', fontSize: 12 }}>More Info</a>
                        )}
                      </div>
                    ))}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {loading && <div style={{ textAlign: 'center', marginTop: 20 }}>Loading events...</div>}
      {error && <div style={{ color: 'red', textAlign: 'center', marginTop: 20 }}>{error}</div>}
    </div>
  );
};

export default WeekViewCalendar; 