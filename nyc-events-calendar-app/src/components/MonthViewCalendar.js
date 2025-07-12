import React, { useState, useEffect } from 'react';
import { eventService } from '../services/eventService';

const DAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
const MONTHS = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December'
];

function getStartOfMonth(year, month) {
  return new Date(year, month, 1);
}

function getEndOfMonth(year, month) {
  return new Date(year, month + 1, 0);
}

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

function getWeeksInMonth(year, month) {
  const start = getStartOfMonth(year, month);
  const end = getEndOfMonth(year, month);
  const startOfFirstWeek = getStartOfWeek(start);
  const endOfLastWeek = getStartOfWeek(end);
  endOfLastWeek.setDate(endOfLastWeek.getDate() + 6);
  
  const weeks = [];
  let currentWeek = new Date(startOfFirstWeek);
  
  while (currentWeek <= endOfLastWeek) {
    const week = [];
    for (let i = 0; i < 7; i++) {
      week.push(new Date(currentWeek));
      currentWeek.setDate(currentWeek.getDate() + 1);
    }
    weeks.push(week);
  }
  
  return weeks;
}

function formatDate(date) {
  return date.toLocaleDateString('en-US', { 
    month: 'short', 
    day: 'numeric' 
  });
}

function isSameDate(date1, date2) {
  return date1.getFullYear() === date2.getFullYear() &&
         date1.getMonth() === date2.getMonth() &&
         date1.getDate() === date2.getDate();
}

function isToday(date) {
  return isSameDate(date, new Date());
}

function isCurrentMonth(date, year, month) {
  return date.getFullYear() === year && date.getMonth() === month;
}

const getBoroughColor = (borough) => {
  const colors = {
    'Manhattan': '#ff6b6b',
    'Brooklyn': '#4ecdc4',
    'Queens': '#3498db',
    'The Bronx': '#feca57',
    'Staten Island': '#a8e6cf',
    'Asbury Park, NJ': '#d1ecf1',
    'Newark, NJ': '#ffeaa7',
    'Jersey City, NJ': '#fd79a8'
  };
  return colors[borough] || '#ddd';
};

const MonthViewCalendar = () => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentYear, setCurrentYear] = useState(2025);
  const [selectedMonth, setSelectedMonth] = useState(null);
  const [viewMode, setViewMode] = useState('months'); // 'months' or 'weeks'

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

  const handleMonthClick = (month) => {
    setSelectedMonth(month);
    setViewMode('weeks');
  };

  const handleBackToMonths = () => {
    setViewMode('months');
    setSelectedMonth(null);
  };

  const handlePrevYear = () => {
    setCurrentYear(currentYear - 1);
  };

  const handleNextYear = () => {
    setCurrentYear(currentYear + 1);
  };

  const getEventsForDate = (date) => {
    return events.filter(event => {
      if (!event.date) return false;
      const eventDate = new Date(event.date);
      return isSameDate(eventDate, date);
    });
  };

  const renderMonthView = () => {
    return (
      <div style={{ maxWidth: 1200, margin: '0 auto', padding: 20 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 30 }}>
          <button onClick={handlePrevYear}>Previous Year</button>
          <h1>{currentYear}</h1>
          <button onClick={handleNextYear}>Next Year</button>
        </div>
        
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', 
          gap: 20 
        }}>
          {MONTHS.map((month, index) => {
            const monthEvents = events.filter(event => {
              if (!event.date) return false;
              const eventDate = new Date(event.date);
              return eventDate.getFullYear() === currentYear && eventDate.getMonth() === index;
            });

            return (
              <div 
                key={month}
                onClick={() => handleMonthClick(index)}
                style={{
                  border: '2px solid #e9ecef',
                  borderRadius: 12,
                  padding: 20,
                  cursor: 'pointer',
                  transition: 'all 0.3s ease',
                  background: monthEvents.length > 0 ? '#f8f9fa' : '#fff',
                  ':hover': {
                    transform: 'translateY(-2px)',
                    boxShadow: '0 4px 12px rgba(0,0,0,0.1)'
                  }
                }}
                onMouseEnter={(e) => {
                  e.target.style.transform = 'translateY(-2px)';
                  e.target.style.boxShadow = '0 4px 12px rgba(0,0,0,0.1)';
                }}
                onMouseLeave={(e) => {
                  e.target.style.transform = 'translateY(0)';
                  e.target.style.boxShadow = 'none';
                }}
              >
                <h3 style={{ margin: '0 0 15px 0', color: '#333' }}>{month}</h3>
                <div style={{ fontSize: 14, color: '#666', marginBottom: 10 }}>
                  {monthEvents.length} event{monthEvents.length !== 1 ? 's' : ''}
                </div>
                {monthEvents.length > 0 && (
                  <div style={{ fontSize: 12, color: '#888' }}>
                    Click to view calendar
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    );
  };

  const renderWeekView = () => {
    if (selectedMonth === null) return null;

    const weeks = getWeeksInMonth(currentYear, selectedMonth);
    const monthName = MONTHS[selectedMonth];

    return (
      <div style={{ maxWidth: 1200, margin: '0 auto', padding: 20 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 30 }}>
          <button onClick={handleBackToMonths}>← Back to Months</button>
          <h1>{monthName} {currentYear}</h1>
          <div style={{ width: 100 }}></div> {/* Spacer for centering */}
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
          {weeks.map((week, weekIndex) => (
            <div key={weekIndex} style={{ border: '1px solid #e9ecef', borderRadius: 8, overflow: 'hidden' }}>
              <div style={{ 
                background: '#f8f9fa', 
                padding: '10px 15px', 
                borderBottom: '1px solid #e9ecef',
                fontWeight: 'bold'
              }}>
                Week {weekIndex + 1}
              </div>
              
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(7, 1fr)' }}>
                {DAYS.map(day => (
                  <div key={day} style={{ 
                    padding: '8px', 
                    textAlign: 'center', 
                    background: '#f8f9fa',
                    borderBottom: '1px solid #e9ecef',
                    borderRight: '1px solid #e9ecef',
                    fontWeight: 'bold',
                    fontSize: 12
                  }}>
                    {day}
                  </div>
                ))}
                
                {week.map((date, dayIndex) => {
                  const dayEvents = getEventsForDate(date);
                  const isCurrentMonthDate = isCurrentMonth(date, currentYear, selectedMonth);
                  const isTodayDate = isToday(date);
                  
                  return (
                    <div 
                      key={dayIndex}
                      style={{
                        minHeight: 120,
                        padding: '8px',
                        borderBottom: '1px solid #e9ecef',
                        borderRight: '1px solid #e9ecef',
                        background: isTodayDate ? '#fff3cd' : 
                                  isCurrentMonthDate ? '#fff' : '#f8f9fa',
                        color: isCurrentMonthDate ? '#333' : '#999',
                        position: 'relative'
                      }}
                    >
                      <div style={{ 
                        fontSize: 14, 
                        fontWeight: isTodayDate ? 'bold' : 'normal',
                        marginBottom: '5px',
                        textAlign: 'center'
                      }}>
                        {date.getDate()}
                      </div>
                      
                      <div style={{ maxHeight: 80, overflowY: 'auto' }}>
                        {dayEvents.map((event, eventIndex) => (
                          <div 
                            key={eventIndex}
                            style={{
                              background: getBoroughColor(event.borough),
                              color: '#222',
                              borderRadius: 4,
                              margin: '2px 0',
                              padding: '4px 6px',
                              fontSize: 10,
                              cursor: 'pointer'
                            }}
                            title={`${event.name} - ${event.time} - ${event.borough}`}
                          >
                            <div style={{ fontWeight: 'bold', fontSize: 11 }}>
                              {event.name.length > 20 ? event.name.substring(0, 20) + '...' : event.name}
                            </div>
                            <div style={{ fontSize: 9 }}>{event.time || 'TBD'}</div>
                            {event.link && (
                              <a 
                                href={event.link} 
                                target="_blank" 
                                rel="noopener noreferrer"
                                style={{ color: '#007bff', fontSize: 9 }}
                                onClick={(e) => e.stopPropagation()}
                              >
                                Info
                              </a>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  if (loading) {
    return <div style={{ textAlign: 'center', marginTop: 50 }}>Loading events...</div>;
  }

  if (error) {
    return <div style={{ color: 'red', textAlign: 'center', marginTop: 50 }}>{error}</div>;
  }

  return (
    <div>
      {viewMode === 'months' ? renderMonthView() : renderWeekView()}
    </div>
  );
};

export default MonthViewCalendar; 