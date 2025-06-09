from http import HTTPStatus
from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
import logging

from .data_parser_service import DataParserService
from .ranking_generator_service import RankingGeneratorService
from data.command_service import CommandService

logger = logging.getLogger(__name__)

def upload_json(request, upload_service: DataParserService = DataParserService(),
                         command_service: CommandService = CommandService(),
                         ranking_generator_service: RankingGeneratorService = RankingGeneratorService()):
    if request.method == 'POST' and 'json_file' in request.FILES:
        json_file = request.FILES['json_file']
        try:
            json_data = json_file.read().decode('utf-8')
            logger.info(f"Beginning to parse uploaded JSON file")
            parsed = upload_service.parse_contestants_json(json_data)

            command_service.upsert_contestants(list(parsed.contestants()))
            command_service.upsert_competitions(list(parsed.competitions()))
            command_service.upsert_submissions(list(parsed.submissions()))
            
            for contestant_name in parsed.contestants():
                ranking = ranking_generator_service.generate_ranking(contestant_name)
                if (ranking):
                    command_service.upsert_ranking(ranking)

            return redirect('display_scores')
        
        except json.JSONDecodeError as e:
            logger.error(f"Error during JSON upload: {e}", exc_info=True)
            response = HttpResponse("Invalid JSON file.")
            response.status_code = HTTPStatus.BAD_REQUEST
            return response
        except Exception as e:
            logger.error(f"Error during JSON upload: {e}", exc_info=True)
            response = HttpResponse(f"An error occurred: {e}")
            response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
            return response
        
    else:
        logger.debug(f"Loaded upload page")
        return render(request, 'upload_form.html')
