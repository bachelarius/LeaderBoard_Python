from .models import Contestant, Competition, Submission, SubmissionDto

class CommandService():

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
