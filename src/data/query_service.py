from .models import Contestant, Submission, SubmissionDto
from django.db.models import Count

class QueryService:
    def fetch_submissions_for_contestant(self, contestant_name: str,
                                               limit: int) -> list[SubmissionDto]:
        contestant = Contestant.objects.get(name=contestant_name)
        submissions = Submission.objects.filter(contestant=contestant).order_by('date')[:limit]
        return [SubmissionDto(s.contestant.name, s.competition.name, s.date, s.score) for s in submissions]

