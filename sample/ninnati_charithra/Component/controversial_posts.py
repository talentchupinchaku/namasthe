from datetime import datetime, timedelta

class ControversialPosts:

    def prepare_controversial_posts(self, body, upvote_ratio_dictionary, reddit):
        controversial_upvote_list = self.build_controversial_upvote_list(upvote_ratio_dictionary, reddit)
        if len(controversial_upvote_list) > 0:
            body += "**Posts with controversial upvote ratio:**   \n"
            for each_controversial_upvote in controversial_upvote_list:
                    body += each_controversial_upvote + "   \n"
        return body

    def build_controversial_upvote_list(self, upvote_ratio_dictionary, reddit):
        controversial_upvote_list = []
        for item in upvote_ratio_dictionary.items():
            if item[0] < 0.8:
                for each_submission in item[1]:
                    split_string = each_submission.split(" ")
                    submission_time = split_string[-3]
                    upvote_ratio = split_string[-1]
                    if datetime.utcfromtimestamp(float(submission_time)) < (datetime.utcnow() - timedelta(hours=6)):
                        controversial_upvote_list.append(
                            "[" + reddit.submission(url=split_string[0].strip()).title + "]" + "(" + split_string[
                                0] + ")" + " ratio: " + upvote_ratio)
        return controversial_upvote_list