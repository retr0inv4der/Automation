import notify2
import json
from pathlib import Path
import requests


def fetch_data(username , repo):
    response = requests.get(f"https://api.github.com/repos/{username}/{repo}/commits")
    if response.status_code == 200:
        print("Data fetched successfully")
        return response.json()
    else:
        return {"error": "Failed to fetch data" , "status_code": response.status_code}

def save_to_file(data, pathto="/tmp/commits.json"):
    try:
        STATE_FILE = Path(pathto)
        STATE_FILE.write_text(json.dumps(data, indent=4))
    except Exception as e:
        print(f"Error saving to file: {e}")

def load_from_file(pathto="/tmp/commits.json"):
    try:
        STATE_FILE = Path(pathto)
        if STATE_FILE.exists():
            content = STATE_FILE.read_text()
            return json.loads(content)
        else:
            return {"error": "File does not exist"}
    except Exception as e:
        print(f"Error loading from file: {e}")
        return {"error": str(e)}

def check_for_updates(new_data, old_data):
    if new_data.get("sha") != old_data.get("sha"):
        return True
    return False


def send_notification(title, message):
    notify2.init("Commit Notifier")
    n = notify2.Notification(title, message)
    n.set_urgency(notify2.URGENCY_NORMAL)
    n.set_icon_from_pixbuf("github-logo.png")
    n.show()
if __name__ == "__main__":
    username = "retr0inv4der"
    repo = "Automation"
    
    data = {"sha" : fetch_data(username, repo)[0]["sha"]}
    
    old_data = load_from_file()
    
    if check_for_updates(data, old_data):
        print("Update detected!")
        save_to_file(data)
        send_notification("New Commit Detected", f"New commit SHA: {data['sha']}")
    else:
        print("No update detected.")
    
    