from .models import Contestant, Ranking, RankingSubmission, RankingDto, Submission, SubmissionDto

class QueryService:
    def fetch_submissions_for_contestant(self, contestant_name: str,
                                               limit: int) -> list[SubmissionDto]:
        contestant = Contestant.objects.get(name=contestant_name)
        submissions = Submission.objects.filter(contestant=contestant).order_by('date')[:limit]
        return [SubmissionDto(s.contestant.name, s.competition.name, s.date, s.score) for s in submissions]

    def fetch_rankings(self) -> list[RankingDto]:
        ranking_data: list[RankingDto] = []
        rankings = Ranking.objects.all().order_by('-total_score', '-num_submissions_included')
        
        for ranking in rankings:
            submissions = [
                SubmissionDto(s.submission.contestant.name, s.submission.competition.name, s.submission.date, s.submission.score)
                for s in RankingSubmission.objects.filter(ranking=ranking)
            ]
            ranking_data.append(RankingDto(contestant_name=ranking.contestant.name,
                                           total_score=ranking.total_score,
                                           latest_submission_date=ranking.latest_submission_date,
                                           num_submissions_included=ranking.num_submissions_included,
                                           submissions=submissions))
        return ranking_data
