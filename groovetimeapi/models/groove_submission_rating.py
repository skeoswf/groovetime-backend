from django.db import models

from .groove_submission import Groove_Submission
from .rating import Rating
from .user_profile import User_Profile


class Groove_Submission_Rating(models.Model):
    user = models.ForeignKey(User_Profile, on_delete=models.CASCADE)
