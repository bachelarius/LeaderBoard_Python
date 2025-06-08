from http import HTTPStatus
from django.shortcuts import render
from django.http import HttpResponse
import json
from .data_parser_service import DataParserService
from data.command_service import CommandService

def upload_json(request, 
                upload_service: DataParserService = DataParserService(),
                command_service: CommandService = CommandService()):
    if request.method == 'POST' and 'json_file' in request.FILES:
        json_file = request.FILES['json_file']
        try:
            json_data = json_file.read().decode('utf-8')
            
            parsed = upload_service.parse_contestants_json(json_data)

            for contestant_name in parsed.contestants_data:
                command_service.UpsertSubmissions(contestant_name, list(parsed.contestants_data[contestant_name]))

            return HttpResponse(f"Uploaded {len(parsed.contestants_data)} contestants.")
        
        except json.JSONDecodeError:
            response = HttpResponse("Invalid JSON file.")
            response.status_code = HTTPStatus.BAD_REQUEST
            return response
        except Exception as e:
            response = HttpResponse(f"An error occurred: {e}")
            response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
            return response
        
    else:
        return render(request, 'upload_form.html')
