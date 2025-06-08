from .models import Contestant, Submission, SubmissionDto

class CommandService():

    def UpsertSubmissions(self, contestant_name: str, submissions: list[SubmissionDto]):
        contestant, _ = Contestant.objects.get_or_create(name=contestant_name)
        
        to_upsert: list[Submission] = []
        for submission in submissions:
            to_upsert.append( 
                Submission(contestant = contestant,
                           submission_name = submission.submission_name,
                           date = submission.date,
                           score = submission.score
                )
            )
        
        Submission.objects.bulk_create(to_upsert, ignore_conflicts=True)
