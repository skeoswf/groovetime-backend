from django.db import models
from .weekly_groove import Weekly_Groove
from .user_profile import User_Profile


class Groove_Submission(models.Model):

    weekly_groove = models.ForeignKey(Weekly_Groove, on_delete=models.CASCADE)
    submitted_by = models.ForeignKey(User_Profile, on_delete=models.CASCADE)

    video_url = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    average_rating = models.DecimalField(max_digits=5, decimal_places=2)
    user_ratings = models.ForeignKey()

    comments = models.ForeignKey()
