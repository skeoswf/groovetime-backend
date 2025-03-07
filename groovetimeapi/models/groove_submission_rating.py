from django.db import models

from .groove_submission import GrooveSubmission
from .groovetime_user import GroovetimeUser
from .rating import Rating


class GrooveSubmissionRating(models.Model):
    groove_submission = models.ForeignKey(
        GrooveSubmission, on_delete=models.CASCADE)
    user_submitted = models.ForeignKey(
        GroovetimeUser, on_delete=models.CASCADE)
    rating_value = models.ForeignKey(Rating, on_delete=models.CASCADE)
