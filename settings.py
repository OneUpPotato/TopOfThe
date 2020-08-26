from os import getenv
from pathlib import Path
from yaml import safe_load
from dotenv import load_dotenv

settings = {}

def load_configs():
    # Load all the needed configuration files.
    global settings

    # Load the .env file.
    load_dotenv(verbose=True)

    # Load the settings file in YAML.
    settings = safe_load(Path("settings.yml", encoding="utf-8").read_text())

def get_subreddit():
    # Returns the subreddit name from the settings file.
    return settings["subreddit"]

def get_flairs():
    # Returns the flairs in the settings file.
    return settings["flairs"]

def get_templates():
    # Returns the templates from the settings file.
    return settings["templates"]

def get_reddit_auth_info():
    # Get the Reddit authentication info.
    return {
        "client_id": getenv("REDDIT_CLIENT_ID"),
        "client_secret": getenv("REDDIT_CLIENT_SECRET"),
        "refresh_token": getenv("REDDIT_REFRESH_TOKEN"),
    }

def get_submissions_webhook():
    # Get the discord webhook URL for the new submissions feed.
    return getenv("DISCORD_SUBMISSIONS_WEBHOOK")
