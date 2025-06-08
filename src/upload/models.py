from datetime import date
from data.models import SubmissionDto

class UploadParseResult:
    __submissions: set[SubmissionDto] = set()
    __contestants: set[str] = set()
    __competitions: set[str] = set()

    def add_submission(self, contestant_name: str, 
                            competition_name: str, 
                            date: date, 
                            score: int):
        
        new_submission = SubmissionDto(contestant_name=contestant_name, 
                                       competition_name=competition_name, 
                                       date=date, 
                                       score=score)
        
        if new_submission not in self.__submissions:
            self.__submissions.add(new_submission)
        
        if contestant_name not in self.__contestants:
            self.__contestants.add(contestant_name)
        
        if contestant_name not in self.__competitions:
            self.__competitions.add(competition_name)
    
    def submissions(self) -> set[SubmissionDto]:
        return self.__submissions
    
    def contestants(self) -> set[str]:
        return self.__contestants
    
    def competitions(self) -> set[str]:
        return self.__competitions