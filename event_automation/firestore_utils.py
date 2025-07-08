import firebase_admin
from firebase_admin import credentials, firestore
import hashlib
from datetime import datetime
import os
import time

# Path to service account key (relative to this file)
SERVICE_ACCOUNT_PATH = os.path.join(os.path.dirname(__file__), 'serviceAccountKey.json')

# Only initialize once
if not firebase_admin._apps:
    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    firebase_admin.initialize_app(cred)
db = firestore.client()

def generate_event_id(event):
    """Generate a unique ID for each event based on its content"""
    # Use name, date, time, and address for uniqueness
    unique_string = f"{event.get('name','')}_{event.get('date','')}_{event.get('time','')}_{event.get('address','') or event.get('location','')}"
    return hashlib.md5(unique_string.encode()).hexdigest()

def map_event_to_schema(event, source=None):
    """Map a raw event dict to the standard Firestore schema."""
    return {
        'name': event.get('name', ''),
        'date': event.get('date', ''),
        'time': event.get('time', 'TBD'),
        'address': event.get('address') or event.get('location', 'New York, NY'),
        'borough': event.get('borough', 'Unknown'),
        'link': event.get('link', ''),
        'source': source or event.get('source', ''),
        'scraped_at': event.get('scraped_at', datetime.now()),
        'is_free': event.get('is_free', True),
    }

def save_events_to_firestore(events, source=None, verbose=True):
    """Save a list of events to Firestore with deduplication."""
    events_ref = db.collection('events')
    saved_count = 0
    duplicate_count = 0
    for event in events:
        mapped_event = map_event_to_schema(event, source=source)
        event_id = generate_event_id(mapped_event)
        mapped_event['event_id'] = event_id
        # Check for existing event
        existing_doc = events_ref.document(event_id).get()
        if existing_doc.exists:
            if verbose:
                print(f"Event already exists: {mapped_event['name']}")
            duplicate_count += 1
            continue
        # Save to Firestore
        events_ref.document(event_id).set(mapped_event)
        if verbose:
            print(f"✅ Saved event: {mapped_event['name']}")
        saved_count += 1
        time.sleep(0.1)  # Avoid overwhelming Firestore
    if verbose:
        print(f"\n📊 Summary: New events saved: {saved_count}, Duplicates skipped: {duplicate_count}, Total processed: {len(events)}") 