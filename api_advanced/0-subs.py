#!/usr/bin/python3
"""Return the number of subscribers for a given subreddit using Reddit API."""

import requests


def number_of_subscribers(subreddit):
    """Return total subscribers for a subreddit, or 0 if invalid."""
    if subreddit is None or not isinstance(subreddit, str):
        return 0

    url = "https://www.reddit.com/r/{}/about.json".format(subreddit)
    headers = {"User-Agent": "ALU-Reddit-Task/0.1"}

    try:
        response = requests.get(
            url, headers=headers, allow_redirects=False, timeout=10
        )
        if response.status_code != 200:
            return 0

        data = response.json().get("data", {})
        return data.get("subscribers", 0)
    except Exception:
        return 0