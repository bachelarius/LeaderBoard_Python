from unittest.mock import MagicMock
from django.test import TestCase
from upload.ranking_generator_service import RankingGeneratorService
from upload.ranking_generator_config import RankingGeneratorConfig
from data.models import SubmissionDto
from datetime import date

class RankingGeneratorServiceTest(TestCase):
    def test_generate_ranking_enough_submissions(self):
        config = RankingGeneratorConfig()
        query_service_mock = MagicMock()
        submission1 = SubmissionDto(contestant_name="test_contestant", competition_name="test_competition_1", date=date(2023, 1, 1), score=10)
        submission2 = SubmissionDto(contestant_name="test_contestant", competition_name="test_competition_2", date=date(2022, 1, 2), score=20)
        submission3 = SubmissionDto(contestant_name="test_contestant", competition_name="test_competition_3", date=date(2021, 1, 2), score=30)
        query_service_mock.fetch_submissions_for_contestant.return_value = [submission1, submission2, submission3]

        ranking_generator_service = RankingGeneratorService(config=config, query_service=query_service_mock)
        ranking = ranking_generator_service.generate_ranking("test_contestant")

        self.assertIsNotNone(ranking)
        if ranking:
            self.assertEqual(ranking.contestant_name, "test_contestant")
            self.assertEqual(ranking.total_score, 60)
            self.assertEqual(ranking.latest_submission_date, date(2023, 1, 2))
            self.assertEqual(ranking.num_submissions_included, 3)

    def test_not_generate_ranking_not_enough_submissions(self):
        config = RankingGeneratorConfig()
        query_service_mock = MagicMock()
        submission1 = SubmissionDto(contestant_name="test_contestant", competition_name="test_competition", date=date(2023, 1, 1), score=10)
        query_service_mock.fetch_submissions_for_contestant.return_value = [submission1]

        ranking_generator_service = RankingGeneratorService(config=config, query_service=query_service_mock)
        ranking = ranking_generator_service.generate_ranking("test_contestant")

        self.assertIsNone(ranking)

    def test_not_generate_ranking_no_submissions(self):
        config = RankingGeneratorConfig(min_submissions=1, max_submissions=5)
        query_service_mock = MagicMock()
        query_service_mock.fetch_submissions_for_contestant.return_value = []

        ranking_generator_service = RankingGeneratorService(config=config, query_service=query_service_mock)
        ranking = ranking_generator_service.generate_ranking("test_contestant")

        self.assertIsNone(ranking)
