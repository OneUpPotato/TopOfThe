from pytz import timezone
from datetime import datetime
from num2words import num2words
from praw.models import Submission
from markdown_strings import esc_format

from settings import get_templates

def format_number(num):
    """
    Formats a number.
    :param num: The number to format.
    :return: The number formatted with commas.
    """
    return f"{num:,}"

def format_time(timestamp):
    """
    Formats a time for the post.
    :param timestamp: The timestamp to format.
    :return: The time and date in the format of D/M/Y H:M
    """
    time = datetime.utcfromtimestamp(timestamp)
    return time.strftime("%d/%m/%Y %H:%M") + " UTC"

def format_time_iso(timestamp):
    """
    Formats a UNIX timestamp to ISO8601 time.
    :param timestamp: The timestamp to format.
    :return: The time in ISO8601 format.
    """
    return datetime.fromtimestamp(timestamp, timezone("Etc/UTC")).isoformat()

def current_time():
    """
    Get the current date.
    :return: Current date formatted as D/M/Y
    """
    return datetime.now(timezone("Etc/UTC"))

def current_date():
    """
    Get the current date.
    :return: Current date formatted as D/M/Y
    """
    return current_time().strftime("%d/%m/%Y")

def format_title_body(title_body):
    """
    Formats a title or a comment body.
    :param title_body: The title/body to be formatted.
    :return: The formatted title/body.
    """
    if title_body != "":
        add_ellipsis = False

        split_by = ["\n\n", "&#x200B;"]
        for item in split_by:
            split = title_body.split(item)
            title_body = split[0]
            if len(split) >= 2:
                add_ellipsis = True

        title_body = esc_format(title_body)

        if add_ellipsis:
            title_body += "(...)"
    return title_body

def format_item(i, item):
    """
    Formats an item into the item template.
    :param i: The place in the section the item is used.
    :param item: The submission/comment.
    :return: The item template filled with the item's info.
    """
    title_body = ""
    if isinstance(item, Submission):
        title_body = item.title
    else:
        title_body = item.body
    title_body = format_title_body(title_body)

    item_author = "[removed]"
    try:
        item_author = item.author.name
    except:
        pass

    return get_templates()["item_template"].format(
        place=num2words((i + 1), to="ordinal_num"),
        title_body=title_body,
        permalink=item.permalink,
        author=item_author,
        subreddit=item.subreddit.display_name,
        score=format_number(item.score),
        time_submitted=format_time(item.created_utc),
    )
