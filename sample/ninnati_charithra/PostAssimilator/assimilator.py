from datetime import datetime, timedelta
from praw.models import MoreComments

class Assimilator:

    previous_summary_comment = None

    def assimilate_summary(self, reddit, awarded_posts, controversial_posts, data_builder, discussed_posts):
        submissions = reddit.subreddit("ni_bondha").new(limit=300)
        three_day_submissions = []
        for submission in submissions:
            if datetime.utcfromtimestamp(submission.created_utc) >= datetime.utcnow() - timedelta(hours=36):
                three_day_submissions.append(submission)
            else:
                break
        submissions = three_day_submissions

        recent_submissions = reddit.subreddit("ni_bondha").new(limit=400)
        automoderator_submissions = []
        for recent_submission in recent_submissions:
            if recent_submission.author == "AutoModerator" \
                    and "ఈ రోజు ఊర పంచాయతీ" in recent_submission.title \
                    and len(automoderator_submissions) < 2:
                automoderator_submissions.append(recent_submission)
            if len(automoderator_submissions) == 2:
                break

        history_posted = False
        latest_automoderator_submission = automoderator_submissions[0]
        previous_automoderator_submission = automoderator_submissions[1]

        if latest_automoderator_submission is not None:
            latest_automoderator_comments = latest_automoderator_submission.comments.list()
            for latest_automoderator_comment in latest_automoderator_comments:
                if isinstance(latest_automoderator_comment, MoreComments):
                    continue
                if latest_automoderator_comment.author == "nee_charithra_bot" and "Last" in latest_automoderator_comment.body:
                    history_posted = True

        if not history_posted and latest_automoderator_submission is not None:
        # if True:
            previous_automoderator_comments = previous_automoderator_submission.comments.list()
            for previous_automoderator_comment in previous_automoderator_comments:
                if isinstance(previous_automoderator_comment, MoreComments):
                    continue
                if previous_automoderator_comment.author == "nee_charithra_bot" and "controversial upvote ratio" in previous_automoderator_comment.body:
                    self.previous_summary_comment = previous_automoderator_comment
            flair_dictionary = {}
            upvote_ratio_dictionary = {}
            submissions_num_comments_dictionary = {}
            submissions_with_awards_dictionary = {}
            data_builder_component = data_builder.DataBuilder()
            data_builder_component.build_submission_dictionaries(submissions,
                                                       flair_dictionary,
                                                       upvote_ratio_dictionary,
                                                       submissions_num_comments_dictionary,
                                                       submissions_with_awards_dictionary)
            body = "**Last three days' activity**\n\n"
            discussed_posts_component = discussed_posts.DiscussedPosts()
            body = discussed_posts_component.prepare_discussed_posts(body, submissions_num_comments_dictionary, reddit)

            awarded_posts_component = awarded_posts.AwardedPosts()
            body = awarded_posts_component.prepare_awarded_posts(body, submissions_with_awards_dictionary, reddit)

            controversial_posts_component = controversial_posts.ControversialPosts()
            body = controversial_posts_component.prepare_controversial_posts(body, upvote_ratio_dictionary, reddit)

            if self.previous_summary_comment is not None:
                body += "   \n [previous summary](" + "https://reddit.com" + self.previous_summary_comment.permalink + ")"
            disclaimer_string = "   \n(_Please upvote this comment if you find this information useful. Also, respond with a comment and tag the author if you have any feedback._)"
            body += disclaimer_string + "   \n^(made by) [^(u/insginificant)](https://www.reddit.com/user/insginificant) ^(|) " \
                                        "[^(About me)](https://www.reddit.com/r/nee_charithra_bot/comments/xp8nw4/introduction/)"
            print(body)
            # latest_automoderator_submission.reply(body=body)
