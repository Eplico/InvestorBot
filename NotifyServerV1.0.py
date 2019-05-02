# MemeEconomy Investment Opportunity Notifier
import praw
import time
import requests
import os

authors = [
    'organic_crystal_meth', 'SlothySurprise', 'bleach_tastes_bad', 'lukenamop', 'blkmmb', 'iscatmypants'
]
MGDWU = 'https://discordapp.com/api/webhooks/562009771587272724/S_lNTtWogUbnyhKH8HIPQTPI2OxdXSD2_hypCVTxi2SKBAbPPX9SC4Tg7aK_ZHX0YtGW'
#TSDWU = 'https://discordapp.com/api/webhooks/565854496157335573/grLVILfHxOjP-aBB0PHvInH7GGU709MDURJYGz8Q70Bj0mV0KZFDk5bagCft1oTma3PS'
message = " Has Posted!! Go Invest Now, Before Its Too Late!! "


def authenticate():
    print('Attempting Authentication...')
    reddit = praw.Reddit('bot1')
    print('Authenticated as user: {}...'.format(reddit.user.me()))
    return reddit


def run_bot(reddit, PostsNotified):
    print('Looking for posts by {}...'.format(authors))
    subreddit = reddit.subreddit('MemeEconomy')
    for submission in subreddit.new(limit=5):

        if submission.author in authors and submission.id not in PostsNotified:
            print('Found Post By {}...'.format(submission.author))
            suburl = 'https://www.reddit.com/r/{}/comments/{}'.format(submission.subreddit, submission.id)
            data = {"content": "{} {} {}".format(submission.author, message, suburl)}
            requests.post(MGDWU, data=data)
            print('Notifying Discord Users...')
            PostsNotified.append(submission.id)

            with open("PostsNotified.txt", "a") as f:
                f.write(submission.id + "\n")

    print('Sleeping For 50 Seconds....')
    time.sleep(50)


def CheckNotified():
    if not os.path.isfile('PostsNotified.txt'):
        PostsNotified = []
    else:
        with open('PostsNotified.txt', 'r') as f:
            PostsNotified = f.read()
            PostsNotified = PostsNotified.split("\n")
            PostsNotified = list(filter(None, PostsNotified))
    return PostsNotified


reddit = authenticate()
PostsNotified = CheckNotified()
while True:
    run_bot(reddit, PostsNotified)
