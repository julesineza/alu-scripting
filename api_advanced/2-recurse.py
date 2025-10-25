#!/usr/bin/python3

"""
recursive function that returns a list contanining titles of all hot articles for a given subreddit 
if no results return none
"""
import requests

def recurse(subreddit ,after=None, hot_list=[]):
    """Return list of all hot post titles for a subreddit (recursively)."""
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "MyRedditApp/0.1"}
    params = {"limit": 100 , "after" : after}
    
    response = requests.get(url,headers=headers,params=params,allow_redirects=False)
    
    if response.status_code != 200 :
        return None
    
    data = response.json().get("data", {})
    children = data.get("children", [])

    for post in children:
        hot_list.append(post["data"]["title"])

    next_after = data.get("after")

    if next_after is None:
        return hot_list 
    
    return recurse(subreddit,after=next_after,hot_list=hot_list)

    

    

