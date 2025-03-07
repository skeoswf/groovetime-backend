from django.db import models

from .groove_submission import GrooveSubmission
from .groovetime_user import GroovetimeUser


class GrooveSubmissionComment(models.Model):
    groove_submission = models.ForeignKey(
        GrooveSubmission, on_delete=models.CASCADE)
    commented_by = models.ForeignKey(
        GroovetimeUser, on_delete=models.CASCADE, null=True)
    comment_text = models.CharField(max_length=400)
    date_created = models.DateTimeField(auto_now_add=True)
