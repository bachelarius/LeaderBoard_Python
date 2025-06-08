from django.contrib import admin
from .models import Contestant, Competition, Submission

admin.site.register(Submission)
admin.site.register(Contestant)
admin.site.register(Competition)