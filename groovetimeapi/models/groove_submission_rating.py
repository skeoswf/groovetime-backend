from django.db import models


from .rating import Rating
from .user_profile import User_Profile


class Groove_Submission_Rating(models.Model):
    groove_submission = models.ForeignKey(
        "groovetimeapi.Groove_Submission", on_delete=models.CASCADE, related_name="submission_being_rated")

    user = models.ForeignKey(User_Profile, on_delete=models.CASCADE)
    rating = models.ForeignKey(Rating, on_delete=models.CASCADE)
