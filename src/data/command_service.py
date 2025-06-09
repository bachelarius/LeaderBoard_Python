from datetime import date
from .models import Contestant, Competition, RankingDto, Submission, Ranking, RankingSubmission, SubmissionDto

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

    def upsert_ranking(self, ranking_data:RankingDto):
        existing_contestant = Contestant.objects.get(name=ranking_data.contestant_name)
        
        #Remove existing Rankings, using cascade delete to deal with RankingSubmissions
        Ranking.objects.filter(contestant=existing_contestant).delete()
        
        new_ranking, _ = Ranking.objects.get_or_create(contestant=existing_contestant,
                                                   total_score=ranking_data.total_score,
                                                   latest_submission_date=ranking_data.latest_submission_date,
                                                   num_submissions_included=ranking_data.num_submissions_included)
        new_ranking_submissions: list[RankingSubmission] = []
        for submission in ranking_data.submissions:
            existing_competition, _ = Competition.objects.get_or_create(name=submission.competition_name)
            existing_submission, _ = Submission.objects.get_or_create(contestant = existing_contestant,
                                                                      competition = existing_competition,
                                                                      date = submission.date,
                                                                      score = submission.score)
            new_ranking_submissions.append(RankingSubmission(ranking=new_ranking, 
                                                             submission=existing_submission, 
                                                             submission_date=existing_submission.date))

        RankingSubmission.objects.bulk_create(new_ranking_submissions)
