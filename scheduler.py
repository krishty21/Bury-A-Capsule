import sqlite3
import requests
import time
from datetime import datetime

API_KEY = "YOUR_MAILGUN_API_KEY_HERE"
DOMAIN_NAME = "YOUR_DOMAIN_NAME_HERE"
FROM_EMAIL = "TimeKeeper <postmaster@YOUR_DOMAIN_NAME_HERE>"

def send_email(to_email, message_body, filename):
    files = []
    if filename:
        file_path = f"uploads/{filename}"
        try:
            opened_file = open(file_path, "rb")
            files = [("attachment", (filename, opened_file))]
        except FileNotFoundError:
            pass

    response = requests.post(
        f"https://api.mailgun.net/v3/{DOMAIN_NAME}/messages",
        auth=("api", API_KEY),
        files=files,
        data={"from": FROM_EMAIL,
              "to": to_email,
              "subject": "Incoming Transmission from the Past",
              "text": f"Capsule Unlocked.\n\nMessage:\n\n{message_body}"}
    )
    
    if filename and files:
        files[0][1][1].close()

    return response.status_code == 200

def check_for_capsules():
    conn = sqlite3.connect('capsules.db')
    c = conn.cursor()
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    c.execute("SELECT * FROM capsules WHERE status='locked' AND open_date <= ?", (today,))
    capsules = c.fetchall()
    
    if capsules:
        for cap in capsules:
            cap_id, email, msg, fname, date, status = cap
            
            success = send_email(email, msg, fname)
            
            if success:
                c.execute("UPDATE capsules SET status='sent' WHERE id=?", (cap_id,))
                conn.commit()
        
    conn.close()

if __name__ == "__main__":
    while True:
        check_for_capsules()
        time.sleep(60)