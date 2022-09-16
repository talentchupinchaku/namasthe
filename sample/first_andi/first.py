import random

import praw
import time
from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient

# initialize with appropriate values
bot_id = "5-hv-Mrpww0aUimZk18fbg"
username = "nee_charithra_bot"
user_agent = "http-client"
responses = [
    "హే... మళ్ళీ వేసేశాడు",
    "ఆఁ సర్లే నువ్వెళ్లు",
    "టాలెంటు చుపిస్తున్నావేంటీ",
    "వాడొక పెద్ద సిద్ధాంతి, వీడొక పెద్ద వేదాంతి",
    "idhi ra intensity ante, idhi ra modulation ante, idhi ra diction ante",
    "అబ్బా సాయిరాం",
    "ఏది, ఒక్కసారి మావయ్యా అనమ్మా",
    "కానివ్వండ్రా, కానివ్వండి",
    "part lu part lu gaa choosthunte idhi kuda baane undhe"
]

def init():

    credential = ManagedIdentityCredential(client_id="49f9fa53-a238-4ac8-b4f2-ab82433075c0")
    # credential = DefaultAzureCredential()
    client = SecretClient(vault_url="https://bondha-vault.vault.azure.net/", credential=credential)

    password = client.get_secret("namasthe").value
    bot_secret = client.get_secret("bot-secret").value

    # creating an authorized reddit instance
    reddit = praw.Reddit(client_id=bot_id,
                         client_secret=bot_secret,
                         username=username,
                         password=password,
                         user_agent=user_agent)

    # to find the top most submission in the subreddit "MLPLounge"
    my_sub = reddit.subreddit('insginificant')
    bondha_sub = reddit.subreddit('ni_bondha')
    my_submissions = my_sub.new()
    my_comments = reddit.redditor('nee_charithra_bot').comments.new(limit=None)
    for my_comment in my_comments:
        print("deleting comment: " + my_comment.id)
        my_comment.delete()

    bondha_submissions = list(bondha_sub.top(limit=5, time_filter="day"))

    for submission in my_submissions:
        for bondha_submission in bondha_submissions:
            bondha_submission.comments_sort = "top"
            comments = bondha_submission.comments.list()
            for comment in comments:
                submission.reply(body=(comment.body + " submissionId: " + bondha_submission.id + " I would have replied " + random.choice(responses)))
                break