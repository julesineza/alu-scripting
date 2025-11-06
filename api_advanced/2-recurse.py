#!/usr/bin/python3
"""Recursively return a list of all hot article titles for a subreddit."""

import requests


def recurse(subreddit, hot_list=None, after=None):
    """
    Recursively retrieve all hot post titles from a subreddit.

    This function queries the Reddit API's hot posts endpoint for the given
    subreddit. It collects post titles into a list and continues retrieving
    additional pages of results using the `after` pagination token until no
    more data is available.

    If the subreddit is invalid, inaccessible, or an error occurs during the
    request, the function returns None.

    Args:
        subreddit (str):
            The name of the subreddit to query.
        hot_list (list, optional):
            Accumulator list used during recursion. Should not be provided
            by the caller; default is None.
        after (str, optional):
            Token for pagination used internally for recursive calls.

    Returns:
        list | None:
            A list of strings containing titles of all hot posts if
            successful; otherwise, None.
    """
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