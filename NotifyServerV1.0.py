# MemeEconomy Investment Opportunity Notifier
import praw
import time
import requests
import os

authors = [
    'organic_crystal_meth', 'SlothySurprise', 'bleach_tastes_bad', 'lukenamop', 'blkmmb', 'iscatmypants', 't3karnOnYoAzz'
]
# discord webhook url as variable for ease
DWU = 'https://discordapp.com/api/webhooks/573591094491611136/-baoU5nY7JFrDoTe7jcwyFhZ3yWnXaZ5YCfW1PJL-LstFpofIElIlYdXJ1-r_c10zvr-'

message = " Has Posted!! Go Invest Now, Before Its Too Late!! "


def authenticate():
    print('Attempting Authentication...')
    reddit = praw.Reddit('bot1')
    print('Authenticated as user: {}...'.format(reddit.user.me()))
    return reddit


def run_bot(reddit, PostsNotified):
    print('Looking for posts')
    subreddit = reddit.subreddit('MemeEconomy')
    for submission in subreddit.new(limit=5):
        # Check the subreddit for new posts by specified authors and that you haven't scanned that post yet
        if submission.author in authors and submission.id not in PostsNotified:
            print('Found Post By {}...'.format(submission.author))
            # build url to post
            suburl = 'https://www.reddit.com/r/{}/comments/{}'.format(submission.subreddit, submission.id)
            # build message to be sent with gathered info
            data = {"content": "{} {} {}".format(submission.author, message, suburl)}
            # send message
            requests.post(DWU, data=data)
            
            print('Notifying Discord Users...')
            # put post id in memory so you don't catch it again
            PostsNotified.append(submission.id)

            with open("PostsNotified.txt", "a") as f:
                f.write(submission.id + "\n")

    print('Sleeping For 1 Minute....')
    # wait 1 minute to scan for new posts
    time.sleep(60)


def CheckNotified():
    # if the file isn't there, make it
    if not os.path.isfile('PostsNotified.txt'):
        PostsNotified = []
    else:
        # if it is, read it
        with open('PostsNotified.txt', 'r') as f:
            PostsNotified = f.read()
            PostsNotified = PostsNotified.split("\n")
            PostsNotified = list(filter(None, PostsNotified))
    return PostsNotified
# run the script


reddit = authenticate()
PostsNotified = CheckNotified()
while True:
    run_bot(reddit, PostsNotified)
