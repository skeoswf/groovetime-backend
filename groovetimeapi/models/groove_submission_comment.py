from django.db import models

from .user_profile import User_Profile


class GrooveSubmissionComments(models.Model):

    groove_submission = models.ForeignKey(
        "groovetimeapi.Groove_Submission", on_delete=models.CASCADE, related_name="groove_submission_comments")

    text = models.CharField(max_length=200)
    commented_by = models.ForeignKey(User_Profile, on_delete=models.CASCADE)

    date_created = models.CharField(max_length=25)
    # automatically set when  profile is created. formatted ex. "Tuesday, May 16th, 2000"
