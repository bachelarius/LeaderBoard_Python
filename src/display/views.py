from django.http import HttpResponse
from django.shortcuts import render

from data.query_service import QueryService

# Create your views here.
def display_scores(request, query_service: QueryService = QueryService()):
    rankings = query_service.fetch_rankings()
    context = {'rankings': rankings}
    return render(request, 'rankings_table.html', context)
