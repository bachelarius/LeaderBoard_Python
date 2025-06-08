from datetime import date
from data.models import SubmissionDto
import logging

logger = logging.getLogger(__name__)

class UploadParseResult:
    def __init__(self):
        self.__contestants: set[str] = set()
        self.__submissions: set[SubmissionDto] = set()
        self.__competitions: set[str] = set()

    def add_submission(self, contestant_name: str, 
                             competition_name: str, 
                             date: date, 
                             score: int):
        logger.debug(f"Processing a submission: \n\tcontestant: {contestant_name} \n\tcompetition: {competition_name} \n\tdate: {date} \n\tscore: {score}")
        
        new_submission = SubmissionDto(contestant_name=contestant_name, 
                                       competition_name=competition_name, 
                                       date=date, 
                                       score=score)
        
        if contestant_name not in self.__contestants:
            self.__contestants.add(contestant_name)
        
        if competition_name not in self.__competitions:
            self.__competitions.add(competition_name)
        
        if new_submission not in self.__submissions:
            self.__submissions.add(new_submission)
    

    def submissions(self) -> set[SubmissionDto]:
       return self.__submissions
    
    def contestants(self) -> set[str]:
        return self.__contestants
    
    def competitions(self) -> set[str]:
        return self.__competitions