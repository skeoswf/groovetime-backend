from django.db import models

from .weekly_groove import WeeklyGroove
from .groovetime_user import GroovetimeUser
from .rating import Rating


class GrooveSubmission(models.Model):
    weekly_groove = models.ForeignKey(WeeklyGroove, on_delete=models.CASCADE)
    submitted_by = models.ForeignKey(GroovetimeUser, on_delete=models.CASCADE)

    video_url = models.URLField()
    description = models.CharField(max_length=500)

    average_rating = models.DecimalField(max_digits=3, decimal_places=1)

    user_ratings = models.ManyToManyField(Rating)
