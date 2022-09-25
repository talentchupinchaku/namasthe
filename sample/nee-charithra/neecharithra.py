import random
from datetime import datetime, timedelta

import praw
import time
from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient

# initialize with appropriate values
bot_id = "5-hv-Mrpww0aUimZk18fbg"
username = "nee_charithra_bot"
user_agent = "http-client"
responses = []
target_word_list = ["charithra cheppu chiluka", "charithra cheppu chilaka", "naa charithra cheppu", "charithra cheppu"]

def init():

    # credential = ManagedIdentityCredential(client_id="49f9fa53-a238-4ac8-b4f2-ab82433075c0")
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url="https://bondha-vault.vault.azure.net/", credential=credential)

    password = client.get_secret("namasthe").value
    bot_secret = client.get_secret("bot-secret").value

    # creating an authorized reddit instance
    reddit = praw.Reddit(client_id=bot_id,
                         client_secret=bot_secret,
                         username=username,
                         password=password,
                         user_agent=user_agent)

    target_time = datetime.utcnow() - timedelta(minutes=55)
    my_comment_set = set()
    for comment in reddit.redditor("nee_charithra_bot").comments.new(limit=200):
        my_comment_set.add(comment.id)

    bondha_comments = list(reddit.subreddit('ni_bondha').comments(limit=500))
    start = time.time()
    calculate_charithra("insginificant", reddit)
    print(time.time() - start)

    # for bondha_comment in bondha_comments:
    #     bondha_comment.refresh()
    #     bondha_comment_set = set(map(lambda comment_reply: comment_reply.id, bondha_comment.replies.list()))
    #     if datetime.utcfromtimestamp(bondha_comment.created_utc) > target_time:
    #         for target_word in target_word_list:
    #             if target_word in bondha_comment.body.lower() and bondha_comment.author.name != "nee_charithra_bot":
    #                 if (len(my_comment_set & bondha_comment_set)) == 0:
    #                     calculate_charithra(bondha_comment.author.name, reddit)
    #                     break
    #     else:
    #         break


def prepare_response(response):
    return response + "\n\n" + "(_this a bot account, upvote if you like the dialogue, redirect abuse to u/insginificant_)"

def calculate_charithra(author, reddit):
    comment_size = list(reddit.redditor(author).comments.new(limit=None))
    submission_size = list(reddit.redditor(author).submissions.new(limit=None))
    print("comments: " + str(len(comment_size)))
    print("submissions: " + str(len(submission_size)))
    return

init()


