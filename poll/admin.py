from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Electeur)
admin.site.register(Party)
admin.site.register(Candidate)
admin.site.register(Vote)