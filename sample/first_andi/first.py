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
    "అబ్బా సాయిరాం",
    "ఏది, ఒక్కసారి మావయ్యా అనమ్మా",
    "కానివ్వండ్రా, కానివ్వండి",
    "పార్ట్ లు పార్ట్ లు గా చూస్తుంటే ఇది కూడా బానే ఉందే",
    "టంగుటూరి వీరేహం ప్రకాహం పంతులు తెలుసా నీకు?",
    "నువ్వు ఉండవమ్మా, తుత్తుతుతుతు అంటావ్",
    "మనకి హీరో దొరికేసాడయ్యా ప్రకాశం"
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

    bondha_sub = reddit.subreddit('ni_bondha')
    my_comments_set = set(map(lambda comment: comment.id, list(reddit.redditor('nee_charithra_bot')
                                                               .comments.new(limit=100))))

    bondha_submissions = list(bondha_sub.top(limit=3, time_filter="day"))
    for bondha_submission in bondha_submissions:
        bondha_submission.comment_sort = "top"
        top_comment = bondha_submission.comments.list()
        comment_replies = map(lambda comment_reply: comment_reply.id, top_comment.replies.list())
        if (len(my_comments_set & set(comment_replies))) == 0:
            top_comment.reply(body=prepare_response(random.choice(responses)))

def prepare_response(response):
    return response + "\n\n" + "(_this a bot account, upvote if you like the dialogue, redirect your abuse to u/insginificant_)"