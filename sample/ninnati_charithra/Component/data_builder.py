import math

class DataBuilder:

    def build_submission_dictionaries(self,
                                      submissions,
                                      flair_dictionary,
                                      upvote_ratio_dictionary,
                                      submissions_num_comments_dictionary,
                                      submissions_with_awards_dictionary):
        for submission in submissions:
            flair = submission.link_flair_text.split(":")[0]
            flair_dictionary[flair] = flair_dictionary.get(flair, 0) + 1
            rounded_ratio = math.floor(submission.upvote_ratio * 10) / 10
            if rounded_ratio not in upvote_ratio_dictionary:
                upvote_ratio_dictionary[rounded_ratio] = []
            upvote_ratio_dictionary[rounded_ratio].append(
                submission.shortlink + " created at " + str(submission.created_utc) + " withupvoteratio " + str(
                    submission.upvote_ratio))
            submissions_num_comments_dictionary[submission.shortlink] = submission.num_comments
            award_string = ""
            award_string_suffix = ""
            total_awards = 0
            for award in submission.all_awardings:
                award_string += award_string_suffix + award["name"] + "(" + str(award["count"]) + "\)"
                total_awards += award["count"]
                award_string_suffix = ", "
            if len(award_string) > 0:
                submissions_with_awards_dictionary[submission.shortlink] = total_awards