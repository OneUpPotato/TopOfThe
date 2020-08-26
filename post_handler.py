from praw.models import Comment

from reddit import get_reddit
from webhooks import post_submissions_embed
from settings import get_templates, get_subreddit, get_flairs
from helpers import current_date, format_item, format_time_iso

def get_totd_text():
    """
    Get the text for the Top of the Day post.
    :return: The body for the post.
    """
    sections = []

    # Most Upvoted Posts
    top_submissions = sorted([submission for submission in get_reddit().subreddit("all").top("day", limit=5)], key=lambda x: x.score, reverse=True)
    items = [format_item(i, item) for i, item in enumerate(top_submissions)]
    sections.append(get_templates()["section_template"].format(
        section_title="Most Upvoted Posts of the Day",
        section_note="",
        title_body="Title",
        items="\n".join(items),
    ))

    # Most Upvoted Comments
    comments = []
    for submission in top_submissions:
        comments.extend([[comment, comment.score] for comment in submission.comments if isinstance(comment, Comment)])
    top_comments = sorted(comments, key=lambda x: x[1], reverse=True)
    items = [format_item(i, item) for i, item in enumerate([comment_info[0] for comment_info in top_comments[:5]])]
    sections.append(get_templates()["section_template"].format(
        section_title="Most Upvoted Comments of the Day",
        section_note="\n\n^(Note: These may not be entirely accurate. Currently these are out of the comments taken from the top 5 submissions.)",
        title_body="Body",
        items="\n".join(items),
    ))

    submission_text = get_templates()["main"].format(date=current_date(), sections="\n\n".join(sections))
    return submission_text

def post_totd():
    """
    Post the Top of the Day post.
    """
    submission = get_reddit().subreddit(get_subreddit()).submit(f"Top of the Day - {current_date()}", selftext=get_totd_text())
    submission.flair.select(flair_template_id=get_flairs()["totd"])

    post_submissions_embed({
        "title": submission.title,
        "description": "There's a new TOTD post!",
        "url": f"https://reddit.com{submission.permalink}",
        "timestamp": format_time_iso(submission.created_utc),
    })
