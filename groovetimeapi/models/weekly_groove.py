from django.db import models


class WeeklyGroove(models.Model):
    active = models.BooleanField(default=True)

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=600)

    start_day = models.CharField(max_length=40)
    end_day = models.CharField(max_length=40)
    # if admin only, may just do a character field and put it in manually
