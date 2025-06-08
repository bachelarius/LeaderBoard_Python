from django.contrib import admin
from .models import Contestant, Competition, Submission, Ranking

admin.site.register(Submission)
admin.site.register(Contestant)
admin.site.register(Competition)
admin.site.register(Ranking)