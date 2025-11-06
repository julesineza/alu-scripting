#!/usr/bin/python3
"""
This module provides a function to query the Reddit API and print the titles
of the first 10 hot posts from a specified subreddit.

If the subreddit is invalid or cannot be accessed, the function prints None.

Example:
    >>> top_ten("python")
    Post Title 1
    Post Title 2
    ...
    Post Title 10

Functions:
    top_ten(subreddit): Prints the titles of the first 10 hot posts
    for a subreddit.
"""

import requests


def top_ten(subreddit):
    """
    Query the Reddit API and print the titles of the top 10 hot posts
    in a subreddit.

    This function sends a GET request to the Reddit API endpoint for
    the specified subreddit and retrieves the list of "hot" posts. It
    then prints the titles of the first 10 posts. If the subreddit is
    invalid or inaccessible, it prints None.

    Args:
        subreddit (str): The name of the subreddit to query.

    Returns:
        None
    """
    url = (
        f"https://www.reddit.com/r/{subreddit}/hot.json"
    )
    headers = {
        "User-Agent": "MyRedditApp/0.1"
    }
    params = {"limit": 10}

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            allow_redirects=False
        )

        if response.status_code != 200:
            print(None)
            return

        data = response.json()
        for child in data["data"]["children"]:
            print(child["data"]["title"])

    except Exception:
        print(None)
