from datetime import date
from django.db import models

class Contestant(models.Model):
    """Leaderboard contestant."""
    name = models.CharField(max_length=255, unique=True)

class Submission(models.Model):
    """Submission scores associated with a contestant."""
    contestant = models.ForeignKey(Contestant, on_delete=models.CASCADE)
    submission_name = models.CharField(max_length=255)
    date = models.DateField()
    score = models.IntegerField()

class SubmissionDto():
    def __init__(self, contestant_name: str,
                       submission_name: str,
                       date: date,
                       score: int):
        self.contestant_name = contestant_name
        self.submission_name=submission_name
        self.date=date
        self.score=score