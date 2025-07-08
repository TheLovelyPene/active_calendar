import requests
import firebase_admin
from firebase_admin import credentials, firestore

# --- Fetch the webpage ---
url = "https://allevents.in/"
response = requests.get(url)

print("Status code:", response.status_code)
print("Page title:", response.text.split('<title>')[1].split('</title>')[0])
print("First 500 characters of HTML:\n", response.text[:500])

# --- Connect to Firestore ---
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

print("Connected to Firestore!") 