
class AwardedPosts:

    def prepare_awarded_posts(self, body, submissions_with_awards_dictionary, reddit):
        body += "**Posts with awards:**   \n"
        if len(submissions_with_awards_dictionary) > 0:
            award_string = ""
            for each_submission_with_award in submissions_with_awards_dictionary.items():
                curr_submission = reddit.submission(url=each_submission_with_award[0])
                title_string = curr_submission.title
                if len(title_string) < 3:
                    title_string = curr_submission.id
                award_string += "[" + title_string + "]" + "(" + \
                                each_submission_with_award[0] + ")" + " (" + str(
                    each_submission_with_award[1]) + ")" + "   \n"
            body += award_string + "   \n"
        else:
            body += "no posts with awards yesterday :(   \n"
        return body
