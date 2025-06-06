from django.shortcuts import render
from django.http import HttpResponse
import json

def upload_json(request):
    if request.method == 'POST' and 'json_file' in request.FILES:
        json_file = request.FILES['json_file']
        try:
            data = json.load(json_file)
            element_count = len(data)
            return HttpResponse(f"The JSON file contains {element_count} elements.")
        except json.JSONDecodeError:
            return HttpResponse("Invalid JSON file.")
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}")
    else:
        return render(request, 'upload_form.html')
