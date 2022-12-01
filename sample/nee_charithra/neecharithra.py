from datetime import datetime, timedelta

import praw
from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient

class NeeCharithra:
    # initialize with appropriate values
    username = "nee_charithra_bot"
    user_agent = "http-client"
    responses = []
    target_word_list = ["charithra cheppu chiluka", "charitra cheppu chiluka", "charithra cheppu chilaka", "charithra cheppu chilaka", "naa charithra cheppu", "naa charitra cheppu", "charithra cheppu", "charitra cheppu"]
    comment_dialog_dictionary = {
        -1: "arey sub ki vachi inka moodu nelalu kuda kaaledha, ela undhi? nachindha?",
        0: "commentlu pettatledem? sigga? bhayama? gouravama?",
        1: "kothallo memu kuda inthe, ippudu chudu ela rechipothunnamo",
        2: "kothallo memu kuda inthe, ippudu chudu ela rechipothunnamo",
        3: "kothallo memu kuda inthe, ippudu chudu ela rechipothunnamo",
        4: "adhi ala speedu penchaali, mana dayanandana jeevitham ela aithe speedochindho, "
           "alaane nee comments lo kuda raavallanna maata",
        5: "adhi ala speedu penchaali, mana dayanandana jeevitham ela aithe speedochindho, "
           "alaane nee comments lo kuda raavallanna maata",
        6: "adhi ala speedu penchaali, mana dayanandana jeevitham ela aithe speedochindho, "
           "alaane nee comments lo kuda raavallanna maata",
        7: "ee maatram hint ichaanu kada, ika chelaregipondi maastaaru",
        8: "ee maatram hint ichaanu kada, ika chelaregipondi maastaaru",
        9: "ee maatram hint ichaanu kada, ika chelaregipondi maastaaru",
        10: "century lu kotte vayassu meedhi!",
        11: "manishannaaka ee maatram kalaaposhana undaalayya",
        12: "manishannaaka ee maatram kalaaposhana undaalayya",
        13: "manishannaaka ee maatram kalaaposhana undaalayya",
        14: "manishannaaka ee maatram kalaaposhana undaalayya",
        15: "manishannaaka ee maatram kalaaposhana undaalayya",
        16: "chala baga comment chesthunnave",
        17: "chala baga comment chesthunnave",
        18: "chala baga comment chesthunnave",
        19: "chala baga comment chesthunnave",
        20: "double century kottadaniki nuvvemaina Tendulkar anukuntunnava",
        21: "inni comment lu peduthunnaventi",
        22: "inni comment lu peduthunnaventi",
        23: "inni comment lu peduthunnaventi",
        24: "ori veedi veshaaloo",
        25: "ori veedi veshaaloo",
        26: "ori veedi veshaaloo",
        27: "poddu asthamaanu comment lu pettukuntu kurchunte mari post lu evadu vesthadu?",
        28: "poddu asthamaanu comment lu pettukuntu kurchunte mari post lu evadu vesthadu?",
        29: "poddu asthamaanu comment lu pettukuntu kurchunte mari post lu evadu vesthadu?",
        30: "muchataga moodo century kottavu ga",
        31: "naku thelisina ankela kanna nee comment le ekkuva unnayi",
        32: "naku thelisina ankela kanna nee comment le ekkuva unnayi",
        33: "naku thelisina ankela kanna nee comment le ekkuva unnayi",
        34: "nuvvu maatladedi teluga, tamilama, malayalama inni comment lu pettavu enti",
        35: "nuvvu maatladedi teluga, tamilama, malayalama inni comment lu pettavu enti",
        36: "nuvvu maatladedi teluga, tamilama, malayalama inni comment lu pettavu enti",
        37: "nuvvu maatladedi teluga, tamilama, malayalama inni comment lu pettavu enti",
        38: "nuvvu enni comment lu pettina chiru family introduce chesina actor la kanna ekkuva undavu le",
        39: "nuvvu enni comment lu pettina chiru family introduce chesina actor la kanna ekkuva undavu le",
        40: "naalugu vandhalu dhaatayi, ikanaina aapava?",
        41: "naalugu vandhalu dhaatayi, ikanaina aapava?",
        42: "rajamouli cinema budget laga unnayi nee comment lu",
        43: "rajamouli cinema budget laga unnayi nee comment lu",
        44: "rajamouli cinema budget laga unnayi nee comment lu",
        45: "rajamouli cinema budget laga unnayi nee comment lu",
        46: "rajamouli cinema budget laga unnayi nee comment lu",
        47: "rajamouli cinema budget laga unnayi nee comment lu",
        48: "rajamouli cinema budget laga unnayi nee comment lu",
        49: "penta century kottadaaniki siddamavuthunnavu",
        50: "dandaalu saami, meere number 1 ika"
    }
    credential = None
    client = None
    password = None
    bot_id = None
    bot_secret = None

    def init(self):

        if NeeCharithra.credential is None:
            NeeCharithra.credential = ManagedIdentityCredential(client_id="b0b16c58-d25f-4878-8f38-eb21f62a6321")
            # NeeCharithra.credential = DefaultAzureCredential()

        if NeeCharithra.client is None:
            NeeCharithra.client = SecretClient(vault_url="https://bondha-keyvault.vault.azure.net/",
                                               credential=NeeCharithra.credential)

        if NeeCharithra.password is None:
            NeeCharithra.password = NeeCharithra.client.get_secret("namasthe").value

        if NeeCharithra.bot_id is None:
            NeeCharithra.bot_id = NeeCharithra.client.get_secret("bondha-charithra-client").value

        if NeeCharithra.bot_secret is None:
            NeeCharithra.bot_secret = NeeCharithra.client.get_secret("bondha-charithra-secret").value

        # creating an authorized reddit instance
        reddit = praw.Reddit(client_id=NeeCharithra.bot_id,
                             client_secret=NeeCharithra.bot_secret,
                             username=NeeCharithra.username,
                             password=NeeCharithra.password,
                             user_agent=NeeCharithra.user_agent)

        target_time = datetime.utcnow() - timedelta(minutes=55)
        my_comment_set = set()
        for comment in reddit.redditor("nee_charithra_bot").comments.new(limit=200):
            my_comment_set.add(comment.id)

        bondha_comments = list(reddit.subreddit('ni_bondha').comments(limit=500))

        for bondha_comment in bondha_comments:
            bondha_comment.refresh()
            bondha_comment_set = set(map(lambda comment_reply: comment_reply.id, bondha_comment.replies.list()))
            if datetime.utcfromtimestamp(bondha_comment.created_utc) > target_time:
                for target_word in NeeCharithra.target_word_list:
                    if target_word in bondha_comment.body.lower() and bondha_comment.author.name != "nee_charithra_bot":
                        if (len(my_comment_set & bondha_comment_set)) == 0:
                            response = NeeCharithra.calculate_charithra(self, bondha_comment.author.name, reddit)
                            bondha_comment.reply(body="You asked for charithra somewhere in your comment and I'm supposed to respond with your acitivity, but I disabled this work temporarily. I will make some changes and reenable this in few weeks")
                            # bondha_comment.reply(body=response)
                            break
            else:
                break


    def prepare_response(self, response):
        return "gatha moodu nelalu ga:" + "   \n" + response + "   \n" \
               + "(_under construction, message my author with suggestions_)" \
               + "   \n" + "^(made by) [^(u/insginificant)](https://www.reddit.com/user/insginificant) " \
                          "^(|) [^(About me)](https://www.reddit.com/r/nee_charithra_bot/comments/xp8nw4/introduction/)"

    def calculate_charithra(self, author, reddit):
        submission_string = NeeCharithra.calculate_submissions(self, author, reddit)
        comment_string = NeeCharithra.calculate_comments(self, author, reddit)
        return NeeCharithra.prepare_response(self, submission_string + "\n\n" + comment_string)


    def calculate_comments(self, author, reddit):
        count = 0
        max_score = 0
        comment_permalink = ""
        target_time = datetime.utcnow() - timedelta(days=90)
        pilla_bondha = True
        for comment in reddit.redditor(author).comments.new(limit=None):
            if datetime.utcfromtimestamp(comment.created_utc) < target_time:
                pilla_bondha = False
                break
            if comment.subreddit == "Ni_Bondha":
                count += 1
                if max_score < comment.score:
                    max_score = comment.score
                    comment_permalink = comment.permalink
        if count == 0 or count == 1:
            return "ayyagaaru enni hitlu kottaaro nuvvu anni comment lu pettavu   \n"
        return_string = "nuvvu sub lo pettina comment lu: " + str(count) + "   \n" \
                        + "rigging chesi vote lu guddinchukunna [comment](https://reddit.com" \
                        + comment_permalink + ")"
        return return_string
               # + " \n nee comments meedha naa comment: " + give_comment_dialog_array(count, pilla_bondha)

    def calculate_submissions(self, author, reddit):
        count = 0
        max_score = 0
        max_comments = 0
        score_submission_permalink = ""
        comment_submission_permalink = ""
        target_time = datetime.utcnow() - timedelta(days=90)
        for submission in reddit.redditor(author).submissions.new(limit=None):
            if datetime.utcfromtimestamp(submission.created_utc) < target_time and not submission.stickied:
                break
            if not datetime.utcfromtimestamp(submission.created_utc) < target_time:
                if submission.subreddit == "Ni_Bondha":
                    count += 1
                    if max_score < submission.score:
                        max_score = submission.score
                        score_submission_permalink = submission.permalink
                    if max_comments < submission.num_comments:
                        max_comments = submission.num_comments
                        comment_submission_permalink = submission.permalink
        if count == 0:
            return "ayyagaaru enni hit lu kottaro nuvvu anni post lu pettavu   \n"
        return_string = "nuvvu sub lo pettina post lu: " + str(count) + "   \n" \
                        + "lancham ichi vote lu veyinchukunna [post](https://reddit.com" \
                        + score_submission_permalink + ")" + "   \n"
        # if comment_submission_permalink == score_submission_permalink:
        #     return_string = return_string + "kuda "
                        # + "[idhe](https://reddit.com" + comment_submission_permalink + ")"

        return return_string

    def calculate_rating(self, count):
        return

    def give_comment_dialog_array(self, count, pilla_bondha):
        if pilla_bondha:
            return NeeCharithra.comment_dialog_dictionary[-1]
        if count / 10 not in NeeCharithra.comment_dialog_dictionary:
            return NeeCharithra.comment_dialog_dictionary[50]
        return NeeCharithra.comment_dialog_dictionary[count / 10]

