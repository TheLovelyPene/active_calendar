# NYC Free Events Calendar - Event Automation

This project automatically scrapes FREE events from multiple websites and stores them in a Firestore database for your React app.

## 🎯 Key Features

- **FREE Events Only**: Advanced filtering to ensure only free events are included
- **Multiple Sources**: Scrapes from allevents.in, timeout.com, NYC Parks, and Bryant Park
- **Firestore Integration**: Automatically saves events to your Firebase database
- **React App Ready**: Includes components to display events from Firestore
- **Easy to Extend**: Template for adding new websites

## 📋 Prerequisites

1. **Firebase Project**: You need a Firebase project with Firestore enabled
2. **Service Account Key**: Download `serviceAccountKey.json` from Firebase Console
3. **Python Libraries**: Install required packages

## 🚀 Quick Setup

### 1. Install Python Dependencies

```bash
pip install firebase-admin beautifulsoup4 requests
```

### 2. Set Up Firebase

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or select existing one
3. Enable Firestore Database
4. Go to Project Settings → Service Accounts
5. Generate new private key → Download `serviceAccountKey.json`
6. Place the file in the `event_automation` folder

### 3. Run the Scraper

```bash
cd event_automation
python scrape_events.py
```

## 🔧 Connecting React App to Firestore

### 1. Install Firebase in React App

```bash
cd nyc-events-calendar-app
npm install firebase
```

### 2. Get Firebase Web Config

1. Go to Firebase Console → Project Settings → General
2. Scroll down to "Your apps" section
3. Click "Add app" → Web app
4. Copy the config object

### 3. Update Firebase Config

Edit `src/firebase.js` and replace the placeholder values:

```javascript
const firebaseConfig = {
  apiKey: "your-actual-api-key",
  authDomain: "your-project-id.firebaseapp.com",
  projectId: "your-project-id",
  storageBucket: "your-project-id.appspot.com",
  messagingSenderId: "your-sender-id",
  appId: "your-app-id"
};
```

### 4. Use the Events Component

In your `App.js`, import and use the Firestore component:

```javascript
import EventsFromFirestore from './components/EventsFromFirestore';

function App() {
  return (
    <div className="App">
      <EventsFromFirestore />
    </div>
  );
}
```

## 🌐 Adding New Websites

### Step 1: Copy the Template

```bash
cp add_new_website.py scrape_mywebsite.py
```

### Step 2: Modify the Template

1. **Update function name**: `scrape_mywebsite()`
2. **Update URL**: Replace with the actual website URL
3. **Find event containers**: Inspect the website's HTML structure
4. **Extract data**: Modify selectors to match the website's format

### Step 3: Test Your Scraper

```bash
python scrape_mywebsite.py
```

### Step 4: Add to Main Scraper

Edit `scrape_events.py` and add your new function:

```python
# Import your new function
from scrape_mywebsite import scrape_mywebsite

# Add to main() function
mywebsite_events = scrape_mywebsite()
all_events.extend(mywebsite_events)
print(f"Found {len(mywebsite_events)} FREE events from mywebsite.com")
```

## 🔍 How Free Event Filtering Works

The scraper uses intelligent keyword detection:

### ✅ FREE Keywords (Include)
- "free", "no cost", "complimentary"
- "free admission", "free entry"
- "donation", "pay what you wish"

### ❌ PAID Keywords (Exclude)
- "ticket", "buy", "purchase", "cost"
- "$", "dollars", "admission fee"
- "premium", "vip", "members only"

### 🎯 Filtering Logic
1. If event has PAID keywords but NO FREE keywords → **Exclude**
2. If event has FREE keywords → **Include**
3. If unclear → **Exclude** (conservative approach)

## 📊 Available Scripts

### `scrape_events.py`
Main scraper that gets events from all sources and saves to Firestore.

### `add_event.py`
Manually add individual events to Firestore.

### `list_events.py`
View all events currently in Firestore.

### `auto_scrape.py`
Automated version that runs without user prompts.

## 🎨 React Components

### `EventsFromFirestore.js`
Main component that displays events from Firestore with:
- Borough filtering
- Modern card layout
- Responsive design
- Loading states

### `eventService.js`
Service layer for Firestore operations:
- Get all events
- Filter by borough
- Filter by date range
- Get free events only

## 🔄 Automation Options

### Manual (Recommended for testing)
```bash
python scrape_events.py
```

### Automated (for production)
```bash
python auto_scrape.py
```

### Cron Job (Linux/Mac)
```bash
# Add to crontab to run daily at 9 AM
0 9 * * * cd /path/to/event_automation && python auto_scrape.py
```

## 🛠️ Troubleshooting

### Common Issues

1. **"No events found"**
   - Check your Firebase config
   - Verify serviceAccountKey.json is in the right place
   - Check internet connection

2. **"Permission denied"**
   - Make sure Firestore rules allow read/write
   - Verify service account has proper permissions

3. **"Website not loading"**
   - Some websites block scrapers
   - Try different User-Agent headers
   - Add delays between requests

### Debug Mode

Add this to see more details:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Monitoring

Check your Firestore database in Firebase Console:
1. Go to Firestore Database
2. View the "events" collection
3. See real-time updates as events are added

## 🎯 Best Practices

1. **Respect websites**: Add delays between requests
2. **Test thoroughly**: Always test new scrapers before production
3. **Monitor quality**: Regularly check that events are actually free
4. **Backup data**: Export events periodically
5. **Update regularly**: Websites change, update scrapers as needed

## 📞 Support

If you need help:
1. Check the troubleshooting section
2. Look at the template files for examples
3. Test with a single website first
4. Verify your Firebase setup

## 🚀 Next Steps

1. **Deploy to production**: Set up automated scraping
2. **Add more sources**: Use the template to add new websites
3. **Improve filtering**: Add more sophisticated free event detection
4. **Add notifications**: Alert users about new events
5. **Analytics**: Track which events are most popular

---

**Remember**: This scraper is designed to find FREE events only. Always respect website terms of service and implement proper delays between requests. 