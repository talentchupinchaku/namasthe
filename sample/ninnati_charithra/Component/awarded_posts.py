
class AwardedPosts:

    def prepare_awarded_posts(self, body, submissions_with_awards_dictionary, reddit):
        if len(submissions_with_awards_dictionary) > 0:
            body += "**Posts with awards:**   \n"
            award_string = ""
            use_tab = False
            for each_submission_with_award in submissions_with_awards_dictionary.items():
                if use_tab:
                    # award_string += "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + "[" + reddit.submission(url=each_submission_with_award[0]).title + "]" + "(" + each_submission_with_award[0] + ")" + " (" + str(each_submission_with_award[1]) + ")" + "   \n"
                    award_string += "[" + reddit.submission(url=each_submission_with_award[0]).title + "]" + "(" + \
                                    each_submission_with_award[0] + ")" + " (" + str(
                        each_submission_with_award[1]) + ")" + "   \n"
                else:
                    award_string += "[" + reddit.submission(url=each_submission_with_award[0]).title + "]" + "(" + \
                                    each_submission_with_award[0] + ")" + " (" + str(
                        each_submission_with_award[1]) + ")" + "   \n"
                use_tab = ~use_tab
            body += award_string + "   \n"
        return body
