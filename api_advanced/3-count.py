#!/usr/bin/python3

""" recursive function that queries the Reddit API, parses the title of all 
hot articles, and prints a sorted count of given keywords """
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
    
    if after:
        params["after"] = after
    
    response = requests.get(url, headers=headers, params=params, 
                          allow_redirects=False)
    
    if response.status_code != 200:
        return
    
    data = response.json().get("data", {})
    children = data.get("children", [])
    
    # Count words in titles
    for child in children:
        title = child["data"]["title"].lower()
        words_in_title = title.split()
        
        for word in words_in_title:
            # Clean word from punctuation
            cleaned_word = ''.join(c for c in word if c.isalnum())
            if cleaned_word in word_count:
                word_count[cleaned_word] += 1
    
    next_after = data.get("after")
    
    if next_after is None:
        if word_count:
            # Filter out words with 0 count and sort
            sorted_words = sorted(
                [(k, v) for k, v in word_count.items() if v > 0],
                key=lambda x: (-x[1], x[0])  # Sort by count desc, then word asc
            )
            
            for word, count in sorted_words:
                print(f"{word}: {count}")
        return
    
    return count_words(subreddit, word_list, after=next_after, 
                      word_count=word_count)


