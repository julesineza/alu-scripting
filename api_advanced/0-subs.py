#!/usr/bin/python3

import requests

from requests.auth import HTTPBasicAuth

"""
0-main
"""

import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")

auth = HTTPBasicAuth(client_id, client_secret)
data = {"grant_type": "client_credentials"}
headers = {"User-Agent": "myredditapp "}


# Step 1: Get an access token
res= requests.post("https://www.reddit.com/api/v1/access_token",auth=auth,data=data,headers=headers)

TOKEN = res.json()["access_token"]


# Step 2: Use token to access API
headers["Authorization"] = f"bearer {TOKEN}"

def number_of_subscribers(subreddit):
    url = f"https://oauth.reddit.com/r/{subreddit}/about.json"
    response = requests.get(url,headers=headers)
    if response.status_code == 200 :
        data = response.json()
        return data['data']['subscribers']
    elif response.status_code == 404:
        return 0 

 
    