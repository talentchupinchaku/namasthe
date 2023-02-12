import json
from datetime import datetime
from datetime import timedelta


def comments_to_be_processed(comment_stream, processed_comments, flagged_authors, target_words, blob_client):
    potential_comments = []
    processed_comments_blob_client = blob_client.get_blob_client(container="proverbs", blob="processed_comments")
    flagged_authors_blob_client = blob_client.get_blob_client(container="proverbs", blob="flagged_authors")
    if processed_comments_blob_client.exists():
        processed_comments = json.loads(processed_comments_blob_client.download_blob().readall())
    clean_processed_comments(processed_comments)
    processed_comments_blob_client.upload_blob(json.dumps(processed_comments), overwrite=True)
    if flagged_authors_blob_client.exists():
        flagged_authors = json.loads(flagged_authors_blob_client.download_blob().readall())
    clean_flagged_authors(flagged_authors)
    for comment in comment_stream:
        if datetime.utcfromtimestamp(comment.created_utc) > datetime.utcnow() - timedelta(hours=2):
            for target_word in target_words:
                if target_word in comment.body.lower():
                    if comment.id not in processed_comments:
                        potential_comments.append(comment)
                    break
    flagged_authors_blob_client.upload_blob(json.dumps(flagged_authors), overwrite=True)
    a = sorted(potential_comments, key=lambda x: x.created_utc, reverse=False)
    return potential_comments


def clean_processed_comments(processed_comments):
    target_keys = []
    for k, v in processed_comments.items():
        if datetime.utcfromtimestamp(v) < datetime.utcnow() - timedelta(hours=24):
            target_keys.append(k)
    for target_key in target_keys:
        del processed_comments[target_key]

def clean_flagged_authors(flagged_authors):
    target_keys = []
    for k, v in flagged_authors.items():
        if datetime.utcfromtimestamp(v) < datetime.utcnow() - timedelta(hours=24):
            target_keys.append(k)
    for target_key in target_keys:
        del flagged_authors[target_key]
