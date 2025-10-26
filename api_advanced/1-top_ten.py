#!/usr/bin/python3
"""Module that queries the Reddit API and prints the titlesof the first 10 hot posts for a given subreddit."""
import requests


def top_ten(subreddit):
    """
    Query the Reddit API and print the titles of the top 10 hot posts in a subreddit.

    This function sends a GET request to the Reddit API endpoint for the specified
    subreddit and retrieves the list of "hot" posts. It then prints the titles of
    the first 10 posts. If the subreddit is invalid or inaccessible, it prints None.

    Args:
        subreddit (str): The name of the subreddit to query.

    Returns:
        None: Prints the titles of the first 10 hot posts to standard output.
               Prints None if the subreddit is invalid.
    """
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

