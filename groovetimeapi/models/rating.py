from django.db import models


class Rating(models.Model):
    value = models.PositiveIntegerField()
    description = models.CharField(max_length=70)
