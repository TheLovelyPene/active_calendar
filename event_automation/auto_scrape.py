#!/usr/bin/env python3
"""
Automated NYC Events Scraper
This script automatically scrapes events from multiple websites and saves them to Firestore.
You can run this script manually or set it up to run automatically (cron job, etc.).
"""

import subprocess
import sys
import os
from datetime import datetime

def run_scraper():
    """Run the event scraper script"""
    print(f"=== Automated NYC Events Scraper ===")
    print(f"Started at: {datetime.now()}")
    print()
    
    try:
        # Run the scraper script
        result = subprocess.run([sys.executable, 'scrape_events.py'], 
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Scraping completed successfully!")
            print("\nOutput:")
            print(result.stdout)
        else:
            print("❌ Scraping failed!")
            print("\nError:")
            print(result.stderr)
            
    except subprocess.TimeoutExpired:
        print("❌ Scraping timed out after 5 minutes")
    except Exception as e:
        print(f"❌ Error running scraper: {str(e)}")

def setup_automation():
    """Show instructions for setting up automated scraping"""
    print("=== Setting Up Automated Scraping ===")
    print()
    print("To run this script automatically, you have several options:")
    print()
    print("1. CRON JOB (macOS/Linux):")
    print("   - Open terminal and type: crontab -e")
    print("   - Add this line to run daily at 9 AM:")
    print("     0 9 * * * cd /path/to/your/event_automation && python3 auto_scrape.py")
    print()
    print("2. MANUAL RUN:")
    print("   - Just run: python3 auto_scrape.py")
    print()
    print("3. SCHEDULED TASK (Windows):")
    print("   - Use Task Scheduler to run this script")
    print()
    print("4. CLOUD AUTOMATION:")
    print("   - Use Google Cloud Functions")
    print("   - Use AWS Lambda")
    print("   - Use GitHub Actions")
    print()

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--setup":
        setup_automation()
    else:
        run_scraper()

if __name__ == "__main__":
    main() 