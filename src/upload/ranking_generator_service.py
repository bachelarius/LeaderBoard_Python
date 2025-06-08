from typing import Optional
from data.command_service import CommandService
from data.models import RankingDto
from data.query_service import QueryService
from upload.ranking_generator_config import RankingGeneratorConfig

class RankingGeneratorService:
    def __init__(self, config: RankingGeneratorConfig = RankingGeneratorConfig(),
                       command_service: CommandService = CommandService(),
                       query_service: QueryService = QueryService()):
         self.config = config
         self.command_service = command_service
         self.query_service = query_service

    def generate_ranking(self, contestant_name:str) -> Optional[RankingDto]:
        contestant_submissions = self.query_service.fetch_submissions_for_contestant(contestant_name,  self.config.max_submissions)
        if len(contestant_submissions) >= self.config.min_submissions:
            total_score = 0
            for submission in contestant_submissions:
                total_score += submission.score
            
            return RankingDto(contestant_name=contestant_name,
                              total_score=total_score,
                              latest_submission_date=contestant_submissions[0].date,
                              num_submissions_included=len(contestant_submissions),
                              submissions=contestant_submissions)
            