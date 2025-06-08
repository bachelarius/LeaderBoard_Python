from datetime import datetime
import json
from .models import UploadParseResult

class DataParserService:
    def parse_contestants_json(self, json_data: str) -> UploadParseResult:
        try:
            data = json.loads(json_data)
            results = UploadParseResult()
            for contestant_data in data:
                for submission_data in contestant_data.get('submissions', []):
                    
                    date_object = datetime.strptime(submission_data['date'], '%d/%m/%Y')

                    results.AddSubmission(contestant_name=contestant_data['name'], 
                                          submission_name=submission_data['name'], 
                                          date=date_object.date(),
                                          score=submission_data['score'])
            return results

        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")
        except KeyError as e:
            raise ValueError(f"Missing key in JSON: {e}")
        except ValueError as e:
            raise ValueError(f"Invalid date format: {e}")
        except Exception as e:
            raise ValueError(f"An unexpected error occurred: {e}")
