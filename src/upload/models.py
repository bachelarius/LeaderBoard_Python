from datetime import date
from data.models import SubmissionDto

class UploadParseResult:
    contestants_data: dict[str, set[SubmissionDto]] = {}

    def AddSubmission(self, 
                      contestant_name: str, 
                      submission_name: str, 
                      date: date, 
                      score: int):
        
        new_submission = SubmissionDto(contestant_name=contestant_name, 
                                       submission_name=submission_name, 
                                       date=date, 
                                       score=score)
        
        if contestant_name in self.contestants_data:
            existing_submissions = self.contestants_data[contestant_name]
            if new_submission not in existing_submissions:
                self.contestants_data[contestant_name].add(new_submission)
        else:
            self.contestants_data[contestant_name] = {new_submission}

    def Submissions(self) -> set[SubmissionDto]:
        all_submissions: set[SubmissionDto] = set()
        for submissions_set in self.contestants_data.values():
            all_submissions.update(submissions_set)
        return all_submissions
