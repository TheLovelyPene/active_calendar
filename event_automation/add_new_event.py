import firebase_admin
from firebase_admin import credentials, firestore
import hashlib
from datetime import datetime

# Initialize Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def generate_event_id(event):
    """Generate a unique ID for each event based on its content"""
    unique_string = f"{event['name']}_{event['date']}_{event['time']}_{event['address']}"
    return hashlib.md5(unique_string.encode()).hexdigest()

def add_new_event():
    """Add a new event to Firestore"""
    print("=== Add New Event to NYC Events Calendar ===")
    print()
    
    # Get event details from user
    name = input("Event name: ").strip()
    date = input("Event date (YYYY-MM-DD): ").strip()
    time = input("Event time (e.g., 7:00 PM): ").strip()
    address = input("Event address: ").strip()
    
    # Borough selection
    print("\nSelect borough:")
    boroughs = ["Manhattan", "Brooklyn", "Queens", "Staten Island", "Asbury Park, NJ"]
    for i, borough in enumerate(boroughs, 1):
        print(f"{i}. {borough}")
    
    borough_choice = input("Enter borough number (1-5): ").strip()
    try:
        borough = boroughs[int(borough_choice) - 1]
    except (ValueError, IndexError):
        print("Invalid choice. Using Manhattan as default.")
        borough = "Manhattan"
    
    link = input("Event link (optional): ").strip()
    if not link:
        link = ""
    
    # Create event object
    event = {
        "name": name,
        "date": date,
        "time": time,
        "address": address,
        "borough": borough,
        "link": link,
        "uploaded_at": datetime.now()
    }
    
    # Generate unique ID
    event_id = generate_event_id(event)
    event["event_id"] = event_id
    
    # Confirm before uploading
    print(f"\n=== Event Summary ===")
    print(f"Name: {name}")
    print(f"Date: {date}")
    print(f"Time: {time}")
    print(f"Address: {address}")
    print(f"Borough: {borough}")
    if link:
        print(f"Link: {link}")
    
    confirm = input("\nAdd this event to Firestore? (y/n): ").strip().lower()
    
    if confirm == 'y':
        try:
            # Upload to Firestore
            events_ref = db.collection('events')
            events_ref.document(event_id).set(event)
            print(f"✅ Event '{name}' successfully added to Firestore!")
            print(f"Event ID: {event_id}")
        except Exception as e:
            print(f"❌ Error adding event: {str(e)}")
    else:
        print("Event not added.")

def list_recent_events():
    """List the most recent events in Firestore"""
    print("=== Recent Events in Firestore ===")
    try:
        events_ref = db.collection('events')
        # Get the 10 most recent events (ordered by upload time)
        docs = events_ref.order_by('uploaded_at', direction=firestore.Query.DESCENDING).limit(10).stream()
        
        for i, doc in enumerate(docs, 1):
            event_data = doc.to_dict()
            print(f"{i}. {event_data['name']}")
            print(f"   Date: {event_data['date']} | Time: {event_data['time']}")
            print(f"   Borough: {event_data['borough']}")
            print(f"   ID: {event_data['event_id']}")
            print()
            
    except Exception as e:
        print(f"❌ Error listing events: {str(e)}")

def main():
    while True:
        print("\n=== NYC Events Calendar - Event Management ===")
        print("1. Add new event")
        print("2. List recent events")
        print("3. Exit")
        
        choice = input("\nSelect an option (1-3): ").strip()
        
        if choice == '1':
            add_new_event()
        elif choice == '2':
            list_recent_events()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 