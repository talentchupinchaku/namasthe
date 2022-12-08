class DiscussedPosts:

    def prepare_discussed_posts(self, body, submissions_num_comments_dictionary, reddit):
        if len(submissions_num_comments_dictionary) >= 5:
            body += "**Top five posts sorted by most commented:**   \n"
            submissions_sorted_by_comments = sorted(submissions_num_comments_dictionary.items(),
                                                    key=lambda item: item[1], reverse=True)
            first_five_commented = submissions_sorted_by_comments[0:5]
            comment_sort_string = ""
            for each_commented_post in first_five_commented:
                title_string = reddit.submission(url=each_commented_post[0]).title
                if len(title_string) < 3:
                    title_string = reddit.submission(url=each_commented_post[0]).id
                comment_sort_string += "[" + title_string + "]" + "(" + \
                                       each_commented_post[0] + ")" + "&nbsp;&nbsp;(" + str(
                    each_commented_post[1]) + ")" + "   \n"
            body += comment_sort_string + "   \n"
        else:
            body += "not even five posts were submitted yesterda :(   \n"
        return body