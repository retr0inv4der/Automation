from calendar import prmonth
from os import link
import re
import requests


def fetch_data(username , repo):
    response = requests.get(f"https://api.github.com/repos/{username}/{repo}/commits")
    if response.status_code == 200:
        print("Data fetched successfully")
        Link_header = response.headers.get("Link")
        print("Link Header:", Link_header)
        return response.json()
    else:
        return {"error": "Failed to fetch data" , "status_code": response.status_code}
    
print(fetch_data("retr0inv4der" , "Automation"))