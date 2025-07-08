import React, { useState, useEffect } from 'react';
import { eventService } from '../services/eventService';
import './EventsFromFirestore.css';

const EventsFromFirestore = () => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedBorough, setSelectedBorough] = useState('all');

  useEffect(() => {
    loadEvents();
  }, [selectedBorough]);

  const loadEvents = async () => {
    try {
      setLoading(true);
      let eventsData;
      
      if (selectedBorough === 'all') {
        eventsData = await eventService.getFreeEvents();
      } else {
        eventsData = await eventService.getEventsByBorough(selectedBorough);
      }
      
      setEvents(eventsData);
      setError(null);
    } catch (err) {
      setError('Failed to load events from Firestore');
      console.error('Error loading events:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Date TBD';
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    } catch {
      return dateString;
    }
  };

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

  if (loading) {
    return (
      <div className="events-container">
        <div className="loading">Loading events from Firestore...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="events-container">
        <div className="error">
          {error}
          <button onClick={loadEvents}>Try Again</button>
        </div>
      </div>
    );
  }

  return (
    <div className="events-container">
      <div className="events-header">
        <h1>🗽 NYC Free Events Calendar</h1>
        <p>Events from Firestore Database</p>
        
        <div className="borough-filter">
          <label>Filter by Borough: </label>
          <select 
            value={selectedBorough} 
            onChange={(e) => setSelectedBorough(e.target.value)}
          >
            <option value="all">All Boroughs</option>
            <option value="Manhattan">Manhattan</option>
            <option value="Brooklyn">Brooklyn</option>
            <option value="Queens">Queens</option>
            <option value="The Bronx">The Bronx</option>
            <option value="Staten Island">Staten Island</option>
            <option value="Asbury Park, NJ">Asbury Park, NJ</option>
          </select>
        </div>
        
        <div className="events-count">
          Found {events.length} free events
        </div>
      </div>

      <div className="events-grid">
        {events.length === 0 ? (
          <div className="no-events">
            No events found. Make sure your Firebase configuration is correct.
          </div>
        ) : (
          events.map((event) => (
            <div 
              key={event.id} 
              className="event-card"
              style={{ borderLeftColor: getBoroughColor(event.borough) }}
            >
              <div className="event-header">
                <h3 className="event-name">{event.name}</h3>
                <span className="event-date">{formatDate(event.date)}</span>
              </div>
              
              <div className="event-details">
                <div className="event-time">
                  <strong>Time:</strong> {event.time || 'TBD'}
                </div>
                <div className="event-address">
                  <strong>Location:</strong> {event.address}
                </div>
                <div className="event-borough">
                  <span 
                    className="borough-badge"
                    style={{ backgroundColor: getBoroughColor(event.borough) }}
                  >
                    {event.borough}
                  </span>
                </div>
                {event.source && (
                  <div className="event-source">
                    <small>Source: {event.source}</small>
                  </div>
                )}
              </div>
              
              {event.link && (
                <div className="event-link">
                  <a href={event.link} target="_blank" rel="noopener noreferrer">
                    More Info
                  </a>
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default EventsFromFirestore; 