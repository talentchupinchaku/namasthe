class DiscussedPosts:

    def prepare_discussed_posts(self, body, submissions_num_comments_dictionary, reddit):
        if len(submissions_num_comments_dictionary) >= 5:
            body += "**Top five posts sorted by most commented:**   \n"
            submissions_sorted_by_comments = sorted(submissions_num_comments_dictionary.items(),
                                                    key=lambda item: item[1], reverse=True)
            first_five_commented = submissions_sorted_by_comments[0:5]
            use_tab = False
            comment_sort_string = ""
            for each_commented_post in first_five_commented:
                if use_tab:
                    # comment_sort_string += "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + "[" + reddit.submission(url=each_commented_post[0]).title + "]" + "(" + each_commented_post[0] + ")" + " (" + str(each_commented_post[1]) + ")" + "   \n"
                    comment_sort_string += "[" + reddit.submission(url=each_commented_post[0]).title + "]" + "(" + \
                                           each_commented_post[0] + ")" + "&nbsp;&nbsp;(" + str(
                        each_commented_post[1]) + ")" + "   \n"
                else:
                    # print(reddit.submission(url=each_commented_post[0]).title)
                    comment_sort_string += "[" + reddit.submission(url=each_commented_post[0]).title + "]" + "(" + \
                                           each_commented_post[0] + ")" + "&nbsp;&nbsp;(" + str(
                        each_commented_post[1]) + ")" + "   \n"
                use_tab = ~use_tab
            body += comment_sort_string + "   \n"
        return body