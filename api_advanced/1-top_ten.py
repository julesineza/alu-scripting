#!/usr/bin/python3
"""Module that queries the Reddit API and prints the titlesof the first 10 hot posts for a given subreddit."""
import requests


def top_ten(subreddit):
    """Prints the titles of the first 10 hot posts for a subreddit."""
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "MyRedditApp/0.1"}
    params = {"limit": 100}

    try:
        response = requests.get(url, headers=headers, params=params, allow_redirects=False)

        # If subreddit is invalid, Reddit returns 302 or 404
        if response.status_code != 200:
            print(None)
            return

        data = response.json()
        for child in data["data"]["children"]:
            print(child["data"]["title"])

    except Exception:
        print(None)

top_ten("programming")