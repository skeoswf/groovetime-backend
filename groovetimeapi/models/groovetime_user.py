from django.db import models


class GroovetimeUser(models.Model):

    uid = models.CharField(max_length=50)

    profile_picture = models.URLField()
    bio = models.CharField(max_length=500)

    groove_points = models.FloatField(default=0.0)
    grooves_won = models.PositiveIntegerField(default=0)

    date_joined = models.DateTimeField(auto_now_add=True)
    admin = models.BooleanField(default=False)
