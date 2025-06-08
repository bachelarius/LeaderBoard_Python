from datetime import date
from django.db import models
from django.db.models import UniqueConstraint

class Contestant(models.Model):
    """Leaderboard contestant."""
    name = models.CharField(max_length=255, unique=True)

class Competition(models.Model):
    """Names for the competitions"""
    name = models.CharField(max_length=255, unique=True)

class Submission(models.Model):
    """Submission scores associated with a contestant."""
    contestant = models.ForeignKey(Contestant, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    date = models.DateField()
    score = models.IntegerField()

    class Meta:
        constraints = [UniqueConstraint(fields=['contestant', 'competition', 'date'], name='unique_submission')]

class Ranking(models.Model):
    """Computed table for displaying the rankings of contestants"""
    contestant = models.OneToOneField(Contestant, on_delete=models.CASCADE)
    total_score = models.IntegerField()
    latest_submission_date = models.DateField()
    num_submissions_included = models.IntegerField()

class RankingSubmission(models.Model):
    """Join between rankings and submissions, to show exactly which submissions are included in a ranking"""
    ranking = models.ForeignKey(Ranking, on_delete=models.CASCADE)
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    class Meta:
        constraints = [
            UniqueConstraint(fields=['ranking', 'submission'], name='unique_ranking_submission'),
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

class RankingDto:
    def __init__(self, contestant_name: str,
                       total_score: int,
                       latest_submission_date: date,
                       num_submissions_included: int,
                       submissions: list[SubmissionDto]):
        self.contestant_name=contestant_name
        self.total_score = total_score
        self.latest_submission_date = latest_submission_date
        self.num_submissions_included = num_submissions_included
        self.submissions = submissions