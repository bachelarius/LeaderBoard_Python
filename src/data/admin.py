from django.contrib import admin
from .models import Contestant, Submission

admin.site.register(Submission)
admin.site.register(Contestant)