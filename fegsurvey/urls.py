"""fegsurvey URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from fegsurveyapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('fegsurveyapp.urls')),
    # path('', include('fegsurveyapp.urls')),
    path("", views.attend_survey, name="attend_survey"),
    path("survey/<int:pk>/", views.survey_starts, name="survey_start"),
    path("survey/<int:survey_pk>/submit/", views.survey_submit, name="survey_submit"),
    # path("survey/<int:survey_pk>/submit/<int:surveyentry_pk>/", views.survey_submit, name="survey_submit"),
    path("survey/<int:pk>/thanks/", views.survey_thanks, name="survey_thanks"),
]
