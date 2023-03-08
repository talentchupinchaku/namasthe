class DiscussedPosts:

    def prepare_discussed_posts(self, body, submissions_num_comments_dictionary, reddit):
        if len(submissions_num_comments_dictionary) >= 15:
            body += "**Top fifteen posts sorted by most commented:**   \n"
            submissions_sorted_by_comments = sorted(submissions_num_comments_dictionary.items(),
                                                    key=lambda item: item[1], reverse=True)
            first_fifteen_commented = submissions_sorted_by_comments[0:15]
            comment_sort_string = ""
            for each_commented_post in first_fifteen_commented:
                curr_submission = reddit.submission(url=each_commented_post[0])
                title_string = curr_submission.title
                if len(title_string) < 3:
                    title_string = curr_submission.id
                comment_sort_string += "[" + title_string + "]" + "(" + \
                                       each_commented_post[0] + ")" + "&nbsp;&nbsp;(" + str(
                    each_commented_post[1]) + ")" + "   \n"
            body += comment_sort_string + "   \n"
        else:
            body += "not even fifteen posts were submitted in last three days :(   \n"
        return body