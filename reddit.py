import praw

from settings import get_reddit_auth_info

reddit = praw.Reddit(**get_reddit_auth_info(), user_agent="TopOfTheBot v2.0 (by u/OneUpPotato)")

def get_reddit():
    return reddit
