#!/usr/bin/python3
"""
This module defines a recursive function that queries the Reddit API to count
how many times specified keywords appear in the titles of all hot posts from a
given subreddit.

The function fetches results page by page using the API `after` pagination
token until all hot posts have been processed. After collecting all counts, it
prints each keyword that appears at least once, sorted primarily by descending
frequency and secondarily in alphabetical order.

Example:
    >>> count_words("python", ["async", "package", "requests"])
    async: 4
    requests: 1

Functions:
    count_words(subreddit, word_list, after=None, word_count=None):
        Recursively count keyword occurrences in hot post titles and
        print results in sorted order.
"""

import requests


def count_words(subreddit, word_list, after=None, word_count=None):
    """
    Recursively query the Reddit API and count keyword occurrences
    in the titles of hot posts for a given subreddit.

    Each API request retrieves up to 100 hot posts. The function extracts
    titles, normalizes them to lowercase, strips punctuation, and counts
    occurrences of each keyword from `word_list`. Duplicate keywords in
    `word_list` are aggregated into a single count.

    Pagination is handled using the `after` token: if more results exist,
    the function recursively retrieves them. Once all posts have been
    processed, keyword counts greater than zero are printed in the
    following order:
        1. Descending frequency
        2. Alphabetical order

    Args:
        subreddit (str):
            The name of the subreddit to query.
        word_list (list[str]):
            List of target keywords. Matching is case-insensitive.
        after (str, optional):
            Pagination token for API continuation; used internally.
        word_count (dict, optional):
            Accumulator tracking occurrences; used internally.

    Returns:
        None:
            Prints the sorted keyword counts to stdout. If the subreddit
            is invalid or unreachable, no output is printed.
    """
    if word_count is None:
        word_count = {}
        for word in word_list:
            word_lower = word.lower()
            word_count[word_lower] = word_count.get(word_lower, 0)

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "MyRedditApp/0.1"}
    params = {"limit": 100}

    if after is not None:
        params["after"] = after

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            allow_redirects=False
        )
    except Exception:
        return

    if response.status_code != 200:
        return

    data = response.json().get("data", {})
    children = data.get("children", [])

    for child in children:
        title = child.get("data", {}).get("title", "").lower()
        words_in_title = title.split()

        for word in words_in_title:
            cleaned = "".join(c for c in word if c.isalnum())
            if cleaned in word_count:
                word_count[cleaned] += 1

    next_after = data.get("after")

    if next_after is None:
        sorted_words = sorted(
            [(k, v) for k, v in word_count.items() if v > 0],
            key=lambda item: (-item[1], item[0])
        )
        for word, count in sorted_words:
            print(f"{word}: {count}")
        return

    return count_words(
        subreddit,
        word_list,
        after=next_after,
        word_count=word_count
    )
