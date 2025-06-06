from django.db import models

class Contestant(models.Model):
    """Represents a leaderboard contestant."""
    name = models.CharField(max_length=255, unique=True)

class Submission(models.Model):
    """Stores individual scores associated with contestants."""
    contestant = models.ForeignKey(Contestant, on_delete=models.CASCADE)
    submission_name = models.CharField(max_length=255)
    date = models.DateField()
    score = models.IntegerField()
