from .models import Contestant, Ranking, RankingSubmission, RankingDto, Submission, SubmissionDto

class QueryService:
    def fetch_submissions_for_contestant(self, contestant_name: str,
                                               limit: int) -> list[SubmissionDto]:
        contestant = Contestant.objects.get(name=contestant_name)
        submissions = Submission.objects.filter(contestant=contestant).order_by('date')[:limit]
        return [SubmissionDto(s.contestant.name, s.competition.name, s.date, s.score) for s in submissions]

    def fetch_rankings(self) -> list[RankingDto]:
        ranking_data: list[RankingDto] = []
        rankings = Ranking.objects.all().select_related('contestant')

        for ranking in rankings:
            submissions = [
                SubmissionDto(s.submission.contestant.name, s.submission.competition.name, s.submission.date, s.submission.score)
                for s in RankingSubmission.objects.filter(ranking=ranking).select_related('submission__contestant', 'submission__competition')
            ]
            ranking_data.append(RankingDto(ranking.contestant.name,
                                           ranking.total_score,
                                           ranking.latest_submission_date,
                                           ranking.num_submissions_included,
                                           submissions))
        return ranking_data
