from datetime import datetime, timedelta

class ControversialPosts:

    def prepare_controversial_posts(self, body, upvote_ratio_dictionary, reddit):
        controversial_upvote_list = self.build_controversial_upvote_list(upvote_ratio_dictionary, reddit)
        body += "**Posts with controversial upvote ratio:**   \n"
        if len(controversial_upvote_list) > 0:
            for each_controversial_upvote in controversial_upvote_list:
                    body += each_controversial_upvote + "   \n"
        else:
            body += "no controversial posts yesterday :(   \n"
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
                        curr_submission = reddit.submission(url=split_string[0].strip()).title
                        title_string = curr_submission.title
                        if len(title_string) < 3:
                            title_string = curr_submission.id
                        controversial_upvote_list.append(
                            "[" + title_string + "]" + "(" + split_string[
                                0] + ")" + " ratio: " + upvote_ratio)
        return controversial_upvote_list