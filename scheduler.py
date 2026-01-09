import sqlite3
import requests
import time
from datetime import datetime

# 1. Update these with your IndiePitcher details
API_KEY = "sc_643522ce52017fd5267e21471e8472f9b7e124a22e1a9b9e321cb6972117f81a"
# IndiePitcher uses the 'to' field to determine the destination. 
# You don't necessarily need a verified sender domain for the free tier (it uses a default sender), 
# but you can configure one in their dashboard.

def send_email(to_email, message_body, filename):
    # IndiePitcher REST API Endpoint
    url = "https://api.indiepitcher.com/v1/email/transactional"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # 2. Construct the JSON payload
    # Note: IndiePitcher's simple API supports Markdown or HTML. 
    # We will use 'markdown' which treats plain text normally.
    payload = {
        "to": to_email,
        "subject": "Incoming Transmission from the Past",
        "body": f"Capsule Unlocked.\n\nMessage:\n\n{message_body}",
        "bodyFormat": "markdown"
    }

    # Note: The basic IndiePitcher transactional API primarily handles text/html.
    # If you absolutely need attachments (the 'filename' part), you might need 
    # to host the file somewhere and include a link in the 'body', 
    # or use their SMTP integration instead of the REST API.
    # For now, this code sends the MESSAGE only.

    try:
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            return True
        else:
            print(f"Error sending to {to_email}: {response.text}")
            return False
            
    except Exception as e:
        print(f"Failed to connect to API: {e}")
        return False

def check_for_capsules():
    conn = sqlite3.connect('capsules.db')
    c = conn.cursor()
    
    # Get current time in format: YYYY-MM-DDTHH:MM
    now = datetime.now().strftime('%Y-%m-%dT%H:%M')
    
    # Check for capsules where the scheduled time is NOW or in the PAST
    c.execute("SELECT * FROM capsules WHERE status='locked' AND open_date <= ?", (now,))
    capsules = c.fetchall()
    
    if capsules:
        print(f"Found {len(capsules)} capsules ready to unlock...")
        for cap in capsules:
            cap_id, email, msg, fname, date, status = cap
            
            success = send_email(email, msg, fname)
            
            if success:
                print(f"Sent capsule {cap_id} to {email}")
                c.execute("UPDATE capsules SET status='sent' WHERE id=?", (cap_id,))
                conn.commit()
            else:
                print(f"Failed to send capsule {cap_id}")
    else:
        print(f"Scanning... ({now}) No capsules ready.")
        
    conn.close()

if __name__ == "__main__":
    print("Time Capsule Scheduler Started (IndiePitcher Edition)...")
    while True:
        check_for_capsules()
        time.sleep(30)