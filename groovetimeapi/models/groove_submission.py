from django.db import models
from .user_profile import User_Profile
from .groove_submission_rating import Groove_Submission_Rating
from .groove_submission_comment import GrooveSubmissionComments


class Groove_Submission(models.Model):

    weekly_groove = models.ForeignKey(
        "groovetimeapi.Weekly_Groove", on_delete=models.CASCADE, related_name="assigned_weekly_groove")

    submitted_by = models.ForeignKey(User_Profile, on_delete=models.CASCADE)

    video_url = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    average_rating = models.DecimalField(max_digits=5, decimal_places=2)
    user_ratings = models.ManyToManyField(
        "groovetimeapi.Groove_Submission_Rating", blank=True, related_name="ratings_for_groove_submission")
    comments = models.ManyToManyField(
        "groovetimeapi.GrooveSubmissionComments", blank=True, related_name="comments_for_groove_submission")
