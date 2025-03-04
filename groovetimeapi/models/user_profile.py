from django.db import models


class User_Profile(models.Model):
    uid = models.CharField(max_length=50)

    image_url = models.URLField(max_length=250)
    bio = models.CharField(max_length=200)

    groove_points = models.DecimalField(max_digits=5, decimal_places=2)
    grooves_won = models.IntegerField()

    date_joined = models.CharField(max_length=25)
    # automatically set when  profile is created. formatted ex. "Tuesday, May 16th, 2000"
    admin = models.BooleanField(default=False)
