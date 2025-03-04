from django.db import models
from .weekly_groove import Weekly_Groove
from .user_profile import User_Profile


class Groove_Submission(models.Model):

    weekly_groove = models.ForeignKey(Weekly_Groove, on_delete=models.CASCADE)
    submitted_by = models.ForeignKey(User_Profile, on_delete=models.CASCADE)

    video_url = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    average_rating = models.DecimalField(max_digits=5, decimal_places=2)
    user_ratings = models.ForeignKey(
        "groovetimeapi.Groove_Submission_Rating", blank=True, related_name="rating_submissions", on_delete=models.CASCADE, default=None
    )

    comments = models.ForeignKey(
        "groovetimeapi.GrooveSubmissionComments", blank=True, related_name="comments_for_submissions", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "groove_submission_test"
