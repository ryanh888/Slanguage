import praw 
from praw.models import MoreComments

CLIENT_ID = 'F1ve7qu66gDKKQ'
SECRET_KEY = 'm3XOZjNGIOkhIq3VCN9zkFt35aLa1g'

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=SECRET_KEY,
    user_agent="KamiWaffle",
)

subreddit = reddit.subreddit("popular")

hot = subreddit.hot(limit = 1)

x = next(hot)


# for submissions in hot:
#     print(submissions.title)

def print_5_best_comments(submission):
    submission.comment_sort = 'best'
    submission.comment_limit = 5
    # Fetch the comments and print each comment body
    # This must be done _after_ the above lines or they won't take affect.
    for top_level_comment in submission.comments:
        if isinstance(top_level_comment, MoreComments):
            continue
        print(top_level_comment.body)

def hot_posts_subreddit(sub_name):
    subreddit = reddit.subreddit(sub_name)
    hot_posts = []
    for post in subreddit.hot(limit = 3):
        hot_posts.append(post)
    return hot_posts

posts = hot_posts_subreddit('memes')
for post in posts:
    print_5_best_comments(post)