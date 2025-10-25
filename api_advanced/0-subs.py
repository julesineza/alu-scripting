#!/usr/bin/python3
"""Module that queries the Reddit API and returns number of subscribers."""

import requests

def number_of_subscribers(subreddit):
    """returns the number of subscribers for a given subreddit."""
    if subreddit is None or not isinstance(subreddit, str):
        return 0

    url = f"https://www.reddit.com/r/{subreddit}/about.json"
    headers = {"User-Agent": "MyRedditApp/0.1"}

    try:
        response = requests.get(url, headers=headers, allow_redirects=False)

        # If subreddit is invalid, Reddit api returns 302 or 404
        if response.status_code != 200:
            return 0

        data = response.json().get("data", {})
        return data.get("subscribers", 0)

    except Exception:
        return 0
