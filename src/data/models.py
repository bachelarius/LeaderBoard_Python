from datetime import date
from django.db import models
from django.db.models import UniqueConstraint

class Contestant(models.Model):
    """Leaderboard contestant."""
    name = models.CharField(max_length=255, unique=True)

class Competition(models.Model):
    """Names for the """
    name = models.CharField(max_length=255, unique=True)

class Submission(models.Model):
    """Submission scores associated with a contestant."""
    contestant = models.ForeignKey(Contestant, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    date = models.DateField()
    score = models.IntegerField()

    class Meta:
        constraints = [
            UniqueConstraint(fields=['contestant', 'competition', 'date'], name='unique_submission'),
        ]


class SubmissionDto:
    def __init__(self, contestant_name: str,
                       competition_name: str,
                       date: date,
                       score: int):
        self.contestant_name=contestant_name
        self.competition_name=competition_name
        self.date=date
        self.score=score
