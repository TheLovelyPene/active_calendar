# NYC & NJ Free Events Calendar

## About This Project

This is a dynamic React web application designed to help users discover free events happening in New York City's boroughs (Manhattan, Brooklyn, Queens, Staten Island) and Asbury Park, NJ, specifically for July 2025. It provides an intuitive, weekly calendar view to make browsing events easy and enjoyable.

## Key Features:

- **Weekly Navigation System**: Effortlessly browse events by week using "Previous Week" and "Next Week" buttons.

- **Borough Color Coding**: Each event card is visually distinct with a background color corresponding to its borough (e.g., Manhattan events in light red, Brooklyn in light green, Queens in light blue, Asbury Park, NJ in light teal, etc.).

- **Responsive Design**: The calendar layout adapts seamlessly for optimal viewing on both desktop and mobile devices.

- **Detailed Event Cards**: Each event is presented in a clear card format, displaying its name, date, time, address, borough/area, and a clickable link for more information.

- **Real NYC & NJ Data**: The calendar is populated with actual free event listings for July 2025, including:
  - Hudson River Park Jazz concerts
  - Macy's 4th of July Fireworks
  - Carnegie Hall Citywide performances
  - Manhattanhenge viewing opportunities
  - Nathan's Hot Dog Eating Contest
  - Various free fairs and festivals (e.g., Flatbush Avenue Street Fair, Summer Stroll on Third Avenue, Queens Day!, Bronx Pride Festival, Cottage Row Curiosities, Asbury Park Spring Bazaar).
  
  *(Note: Events from The Bronx are currently filtered out from display in the application logic.)*

## How It Works (Core Logic)

This application was developed iteratively with AI assistance (Gemini), focusing on transforming raw event data into a user-friendly, interactive web experience using React.

### Data Source & Structure:

- The core event information is stored in `src/data/eventsData.js` as a JavaScript array of objects, each representing a free event with details like name, date, time, location, and a link.
- This file also defines the color mappings for each borough/area.

### Date Processing & Grouping (`src/utils/dateHelpers.js`):

- The application uses custom utility functions (`getISOWeek`, `getMondayOfISOWeek`) to accurately determine the ISO week number for each event.
- Events, including those spanning multiple days, are programmatically grouped by their respective week and then by the specific day of the week they occur on.
- The core logic in `App.js` initializes all possible July weeks and then populates them with events, ensuring events are correctly assigned even if they start in late June or end in early August but fall primarily within July.

### Component-Based UI (`src/App.js` & `src/components/EventCard.js`):

- **App.js (Main Calendar)**: This is the central component that manages the application's state, including the `currentWeekIndex` to control which week is displayed. It orchestrates the rendering of the navigation buttons and the grid of daily event cards.

- **EventCard.js (Individual Event)**: A reusable, functional component designed to render the details of a single event. It dynamically applies CSS classes and inline styles based on the event's borough to achieve the color-coding effect and formats the event details for clear presentation.

### Dynamic Rendering & Navigation:

- React's `useState` and `useEffect` hooks are used to manage the active week and to process the event data efficiently only once on component mount.
- The "Previous Week" and "Next Week" buttons update the `currentWeekIndex`, triggering React to re-render the App component and display the events for the newly selected week.
- Events within each day are sorted by time (with "TBD" times appearing last for better organization).

## How to Run It

To get this project up and running on your local machine, follow these steps:

### Prerequisites

You need Node.js and npm (Node Package Manager) installed on your system. You can download them from [nodejs.org](https://nodejs.org).

### Setup & Installation

1. **Create a React Project** (if you don't have one already):
   If you're starting fresh, open your terminal or command prompt and run:

   ```bash
   npx create-react-app nyc-events-calendar-app
   ```

   This will create a new directory named `nyc-events-calendar-app` with a basic React project structure.

2. **Navigate into your project directory**:

   ```bash
   cd nyc-events-calendar-app
   ```

3. **Create necessary folders**:
   Inside the `src/` directory, create the following sub-directories:

   ```
   nyc-events-calendar-app/
   ├── src/
   │   ├── data/
   │   ├── utils/
   │   └── components/
   ```

4. **Place the code files**:

   - **`src/data/eventsData.js`**: Copy the content from the "1. src/data/eventsData.js" immersive block into a new file named `eventsData.js` inside the `src/data/` folder.

   - **`src/utils/dateHelpers.js`**: Copy the content from the "2. src/utils/dateHelpers.js" immersive block into a new file named `dateHelpers.js` inside the `src/utils/` folder.

   - **`src/components/EventCard.js`**: Copy the content from the "3. src/components/EventCard.js" immersive block into a new file named `EventCard.js` inside the `src/components/` folder.

   - **`src/App.js`**: Open your existing `src/App.js` file and replace its entire content with the code from the "4. src/App.js (The Condensed Main Application Logic)" immersive block.

### Running the Application

Once all files are in place, save them, then go back to your terminal or command prompt (ensuring you are in the `nyc-events-calendar-app` root directory) and run:

```bash
npm start
```

This command will start the development server. Your application should automatically open in your web browser, usually at `http://localhost:3000` (or another available port). You'll then be able to navigate through the weekly calendar of events.

## Live Demo

Visit the live application: [NYC & NJ Free Events Calendar](https://thelovelypene.github.io/active_calendar/nyc_events_calendar.html)
