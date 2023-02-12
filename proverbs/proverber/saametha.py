import random
from datetime import datetime
from datetime import timedelta
from azure.storage.blob import BlobServiceClient


import praw
import time
import json
from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient
from random import randrange


from praw.models import MoreComments

import proverb_eligibility
import proverber_utils

class Saametha:
    # initialize with appropriate values
    username = "nee_charithra_bot"
    user_agent = "http-client"
    target_word_list = ["saametha", "sametha", "sameta", "saameta", "సామెత",
                        "సామిత", "saamitha", "saamita", "samita", "samitha"]
    curr_responses_used = len(proverber_utils.responses) - 1
    credential = None
    count = 0
    client = None
    saametha_secret = None
    blob_service_client = None
    saametha_client = None
    blob_url = None
    password = None
    processed_comments = {}
    ancestral_dictionary = {}
    current_parent = None
    flagged_authors = {}

    def setup(self):

        if Saametha.credential is None:
            Saametha.credential = ManagedIdentityCredential(client_id="b0b16c58-d25f-4878-8f38-eb21f62a6321")
            # Saametha.credential = DefaultAzureCredential()

        if Saametha.client is None:
            Saametha.client = SecretClient(vault_url="https://bondha-keyvault.vault.azure.net/",
                                           credential=Saametha.credential)
        if Saametha.saametha_client is None:
            Saametha.saametha_client = Saametha.client.get_secret("saametha-client").value

        if Saametha.password is None:
            Saametha.password = Saametha.client.get_secret("namasthe").value

        if Saametha.saametha_secret is None:
            Saametha.saametha_secret = Saametha.client.get_secret("saametha-secret").value

        if Saametha.blob_url is None:
            Saametha.blob_url = Saametha.client.get_secret("blob-url").value

        if Saametha.blob_service_client is None:
            Saametha.blob_service_client = BlobServiceClient(Saametha.blob_url, credential=Saametha.credential)

        # creating an authorized reddit instance
        reddit = praw.Reddit(client_id=Saametha.saametha_client,
                             client_secret=Saametha.saametha_secret,
                             username=Saametha.username,
                             password=Saametha.password,
                             user_agent=Saametha.user_agent)
        self.run_saametha(reddit)
        self.delete_all(reddit)

    def run_saametha(self, reddit):
        # test = {"a": "a1", "b": "b1"}
        # proverb_blob_client = Saametha.blob_service_client.get_blob_client(container="proverbs", blob="sample")
        # proverb_blob_client.upload_blob(json.dumps(test), overwrite=True)
        # test_reader = json.loads(proverb_blob_client.download_blob().readall())
        # print(test_reader["a"])
        # dummy_blob_client = Saametha.blob_service_client.get_blob_client(container="proverbs", blob="dummy")
        # if not dummy_blob_client.exists():
        #     print("doesn't exist")
        potential_comments = proverb_eligibility.comments_to_be_processed(
            reddit.subreddit('insginificant').comments(limit=500),
            Saametha.processed_comments,
            Saametha.flagged_authors,
            Saametha.target_word_list,
            Saametha.blob_service_client)

        current_parent_blob_client = Saametha.blob_service_client.get_blob_client(container="proverbs", blob="current_parent")
        Saametha.current_parent = json.loads(current_parent_blob_client.download_blob().readall()) if Saametha.blob_service_client.get_blob_client(container="proverbs", blob="current_parent").exists() else None
        ancestral_dictionary_blob_client = Saametha.blob_service_client.get_blob_client(container="proverbs", blob="ancestral_dictionary")
        flagged_authors_blob_client = Saametha.blob_service_client.get_blob_client(container="proverbs", blob="flagged_authors")
        processed_comments_blob_client = Saametha.blob_service_client.get_blob_client(container="proverbs", blob="processed_comments")

        for potential_comment in potential_comments:
            posted_comment = potential_comment.reply(body="this will be a sametha place 1" + " parent is " + potential_comment.id)
        #     if Saametha.current_parent is None:
        #         posted_comment = potential_comment.reply(body="this will be a sametha place 1" + " parent is " + potential_comment.id)
        #         current_parent_blob_client.upload_blob(json.dumps([potential_comment.id, potential_comment.created_utc]), overwrite=True)
        #         ancestral_dictionary_blob_client.upload_blob(json.dumps({"t1_" + posted_comment.id: posted_comment.created_utc,
        #                                          "t1_" + potential_comment.id: potential_comment.created_utc}), overwrite=True)
        #         Saametha.ancestral_dictionary = {"t1_" + posted_comment.id: posted_comment.created_utc,
        #                                          "t1_" + potential_comment.id: potential_comment.created_utc}
        #     else:
        #         if potential_comment.parent_id in Saametha.ancestral_dictionary:
        #             if datetime.utcfromtimestamp(Saametha.current_parent[1]) < datetime.utcnow() - timedelta(hours=24):
        #                 potential_comment.reply(body="its been over a day since this thread started, "
        #                                              "can you please start a new thread elsewhere?")
        #             else:
        #                 posted_comment = potential_comment.reply(body="this will be a sametha place 2" + " parent is " + Saametha.current_parent[0])
        #                 Saametha.ancestral_dictionary["t1_" + posted_comment.id] = posted_comment.created_utc
        #                 Saametha.ancestral_dictionary["t1_" + potential_comment.id] = potential_comment.created_utc
        #                 ancestral_dictionary_blob_client.upload_blob(json.dumps(Saametha.ancestral_dictionary), overwrite=True)
        #         else:
        #             if datetime.utcfromtimestamp(Saametha.current_parent[1]) < datetime.utcnow() - timedelta(hours=24):
        #                 posted_comment = potential_comment.reply(body="this will be a sametha place 3")
        #                 Saametha.current_parent[0] = potential_comment.id
        #                 Saametha.current_parent[1] = potential_comment.created_utc
        #                 current_parent_blob_client.upload_blob(
        #                     json.dumps([potential_comment.id, potential_comment.created_utc]), overwrite=True)
        #                 Saametha.ancestral_dictionary = {"t1_" + posted_comment.id: posted_comment.created_utc,
        #                                                  "t1_" + potential_comment.id: potential_comment.created_utc}
        #                 ancestral_dictionary_blob_client.upload_blob(json.dumps(Saametha.ancestral_dictionary), overwrite=True)
        #             else:
        #                 if potential_comment.author.id not in Saametha.flagged_authors:
        #                     potential_comment.reply(body="another bird started a nest here. "
        #                                                  "Can you thread this same question there?" + " parent is " + Saametha.current_parent[0])
        #                     Saametha.flagged_authors[potential_comment.author.id] = potential_comment.created_utc
        #                     flagged_authors_blob_client.upload_blob(json.dumps(Saametha.flagged_authors), overwrite=True)
            Saametha.processed_comments[potential_comment.id] = potential_comment.created_utc
            processed_comments_blob_client.upload_blob(json.dumps(Saametha.processed_comments), overwrite=True)

    def delete_all(self, reddit):
        comments_to_be_deleted = reddit.subreddit("insginificant").comments.new(limit=100)
        for comment_to_be_deleted in comments_to_be_deleted:
            comment_to_be_deleted.delete()