from datetime import date
from .models import Contestant, Competition, Submission, Ranking, RankingSubmission, SubmissionDto

class CommandService:

    def upsert_contestants(self, contestant_names: list[str]):
        contestants: list[Contestant] = []
        for contestant_name in contestant_names:
            contestants.append(Contestant(name=contestant_name))
        Contestant.objects.bulk_create(contestants, ignore_conflicts=True)

    def upsert_competitions(self, competition_names: list[str]):
        competitions: list[Competition] = []
        for competition_name in competition_names:
            competitions.append(Competition(name=competition_name))
        Competition.objects.bulk_create(competitions, ignore_conflicts=True)

    def upsert_submissions(self, submissions: list[SubmissionDto]):
        to_upsert: list[Submission] = []
        for submission in submissions:
            contestant, _ = Contestant.objects.get_or_create(name=submission.contestant_name)
            competition, _ = Competition.objects.get_or_create(name=submission.competition_name)
            to_upsert.append( 
                Submission(contestant = contestant,
                           competition = competition,
                           date = submission.date,
                           score = submission.score
                )
            )
        
        Submission.objects.bulk_create(to_upsert, ignore_conflicts=True)

    def upsert_ranking(self, contestant_name: str,
                             total_score: int,
                             latest_submission_date: date,
                             submissions: list[SubmissionDto]):
        existing_contestant = Contestant.objects.get_or_create(name=contestant_name)
        
        #Remove existing Rankings, using cascade delete to deal with RankingSubmissions
        Ranking.objects.filter(contestant=existing_contestant).delete()
        
        ranking, _ = Ranking.objects.get_or_create(contestant=existing_contestant,
                                                   total_score=total_score,
                                                   latest_submission_date=latest_submission_date,
                                                   num_submissions_included=len(submissions))
        ranking_submissions: list[RankingSubmission] = []
        for submission in submissions:
            existing_competition, _ = Competition.objects.get_or_create(name=submission.competition_name)
            existing_submission, _ = Submission.objects.get_or_create(contestant = existing_contestant,
                                                                      competition = existing_competition,
                                                                      date = submission.date,
                                                                      score = submission.score)
            ranking_submissions.append(RankingSubmission(ranking=ranking,
                                               submission=existing_submission
            ))

        RankingSubmission.objects.bulk_create(ranking_submissions)
