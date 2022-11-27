import praw

from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient

from PostAssimilator import assimilator
from Component import awarded_posts, controversial_posts, data_builder, discussed_posts

class NinnatiCharithra:
    username = "nee_charithra_bot"
    user_agent = "http-client"
    credential = None
    client = None
    ninna_charithra_secret = None
    ninna_charithra_client = None
    password = None
    def __init__(self):
        if NinnatiCharithra.credential is None:
            NinnatiCharithra.credential = ManagedIdentityCredential(client_id="b0b16c58-d25f-4878-8f38-eb21f62a6321")
            # NinnatiCharithra.credential = DefaultAzureCredential()

        if NinnatiCharithra.client is None:
            NinnatiCharithra.client = SecretClient(vault_url="https://bondha-keyvault.vault.azure.net/",
                                                   credential=NinnatiCharithra.credential)
        if NinnatiCharithra.ninna_charithra_client is None:
            NinnatiCharithra.ninna_charithra_client = NinnatiCharithra.client.get_secret("ninna-charithra-client").value
        if NinnatiCharithra.password is None:
            NinnatiCharithra.password = NinnatiCharithra.client.get_secret("namasthe").value

        if NinnatiCharithra.ninna_charithra_secret is None:
            NinnatiCharithra.ninna_charithra_secret = NinnatiCharithra.client.get_secret("ninna-charithra-secret").value
        # creating an authorized reddit instance
        reddit = praw.Reddit(client_id=NinnatiCharithra.ninna_charithra_client,
                             client_secret=NinnatiCharithra.ninna_charithra_secret,
                             username=NinnatiCharithra.username,
                             password=NinnatiCharithra.password,
                             user_agent=NinnatiCharithra.user_agent)
        assimilator_component = assimilator.Assimilator()
        assimilator_component.assimilate_summary(reddit,
                                                 awarded_posts,
                                                 controversial_posts,
                                                 data_builder,
                                                 discussed_posts)