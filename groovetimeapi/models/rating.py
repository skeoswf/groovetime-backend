from django.db import models


class Rating(models.Model):

    value = models.IntegerField(unique=True)
    description = models.CharField(max_length=200)
