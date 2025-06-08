from django.http import HttpResponse
from django.shortcuts import render

from data.query_service import QueryService

# Create your views here.
def display_scores(request,
                   query_service: QueryService = QueryService()):
    relevant_contestants = query_service.fetch_contestants()
    return HttpResponse(f"Found {len(relevant_contestants)} users with at least 3 entries")