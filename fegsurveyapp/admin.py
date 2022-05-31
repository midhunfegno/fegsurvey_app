from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Question)
admin.site.register(Options)
admin.site.register(SurveyEntry)
admin.site.register(Survey)
