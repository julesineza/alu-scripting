#!/usr/bin/python3
"""Recursively return a list of all hot article titles for a subreddit."""

import requests


def recurse(subreddit, hot_list=None, after=None):
    """Return list of all hot post titles for a subreddit (recursively)."""
    if hot_list is None:
        hot_list = []

    if subreddit is None or not isinstance(subreddit, str):
        return None

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "ALU-Reddit-Task/0.1"}
    params = {"after": after, "limit": 100}

    try:
        response = requests.get(
            url, headers=headers, params=params,
            allow_redirects=False, timeout=10
        )
        if response.status_code != 200:
            return None

        data = response.json().get("data", {})
        children = data.get("children", [])
        for post in children:
            hot_list.append(post.get("data", {}).get("title"))

        after = data.get("after")
        if after is not None:
            return recurse(subreddit, hot_list, after)
        return hot_list
    except Exception:
        return None