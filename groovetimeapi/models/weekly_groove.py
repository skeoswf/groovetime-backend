from django.db import models


class Weekly_Groove(models.Model):

    active = models.BooleanField(default=False)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=50)

    start_day = models.CharField(max_length=25)
    # automatically set when created. formatted ex. "Tuesday, May 16th, 2000"
    end_day = models.CharField(max_length=25)
    # i can write it manually / or maybe i could pick set a calendar in the admin-only panel that would give me that string
    submissions = models.ForeignKey(
        "groovetimeapi.Groove_Submission", blank=True, related_name="submissions_for_weekly_groove", on_delete=models.CASCADE)


class Meta:
    db_table = "weekly_groove_submissions"
