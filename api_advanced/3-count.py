#!/usr/bin/python3
"""Recursively count given keywords in hot article titles of a subreddit."""

import requests


def count_words(subreddit, word_list, after=None, counts=None):
    """Count occurrences of keywords in hot titles recursively."""
    if counts is None:
        counts = {}
        temp = {}
        for w in word_list:
            lw = w.lower()
            temp[lw] = temp.get(lw, 0) + 1
        word_list = list(temp.keys())
        counts = {w: 0 for w in word_list}

    if subreddit is None or not isinstance(subreddit, str):
        return

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "ALU-Reddit-Task/0.1"}
    params = {"after": after, "limit": 100}

    try:
        response = requests.get(
            url, headers=headers, params=params,
            allow_redirects=False, timeout=10
        )
        if response.status_code != 200:
            return

        data = response.json().get("data", {})
        children = data.get("children", [])
        for post in children:
            title = post.get("data", {}).get("title", "").lower().split()
            for word in counts.keys():
                counts[word] += title.count(word)

        after = data.get("after")
        if after is not None:
            return count_words(subreddit, word_list, after, counts)

        # Print final sorted results
        sorted_counts = sorted(
            [(w, c) for w, c in counts.items() if c > 0],
            key=lambda kv: (-kv[1], kv[0])
        )
        for w, c in sorted_counts:
            print("{}: {}".format(w, c))
    except Exception:
        return