from datetime import datetime
import json
import logging

from .models import UploadParseResult

logger = logging.getLogger(__name__)

class DataParserService:
    def parse_contestants_json(self, json_data: str) -> UploadParseResult:
        try:
            data = json.loads(json_data)
            logger.info(f"Parsing JSON data with {len(data)} contestants")
            results = UploadParseResult()
            for contestant_data in data:
                logger.debug(f"Processing contestant: \n{contestant_data}")

                for submission_data in contestant_data.get('submissions', []):
                    logger.debug(f"Processing submission: \n{submission_data}")
                    date_object = datetime.strptime(submission_data['date'], '%d/%m/%Y')
                    
                    results.add_submission(contestant_name=contestant_data['name'], 
                                           competition_name=submission_data['name'], 
                                           date=date_object.date(),
                                           score=submission_data['score'])
                    logger.debug(f"parsed submission: {contestant_data['name']} - {submission_data['name']} - {date_object.date()} - {submission_data['score']}")
            logger.info(f"Parsing complete. Found {len(results.contestants())} contestants and {len(results.submissions())} submissions.")

            return results


        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")
        except KeyError as e:
            raise ValueError(f"Missing key in JSON: {e}")
        except ValueError as e:
            raise ValueError(f"Invalid date format: {e}")
        except Exception as e:
            raise ValueError(f"An unexpected error occurred: {e}")
