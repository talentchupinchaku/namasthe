import praw
import time
from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient

# initialize with appropriate values
bot_id = "5-hv-Mrpww0aUimZk18fbg"
username = "nee_charithra_bot"
user_agent = "http-client"


def init():

    credential = ManagedIdentityCredential(client_id="49f9fa53-a238-4ac8-b4f2-ab82433075c0")
    # credential = DefaultAzureCredential()
    # call close when the client and credential are no longer needed
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
    bondha_submissions = bondha_sub.new(limit=1)
    my_comments = reddit.redditor('nee_charithra_bot').comments.new(limit=None)
    for my_comment in my_comments:
        print("deleting comment: " + my_comment.id)
        my_comment.delete()

    for submission in my_submissions:
        for bondha_submission in bondha_submissions:
            print("responding to : " + bondha_submission.id)
            submission.reply(body=(bondha_submission.title + " submissionId: " + bondha_submission.id))