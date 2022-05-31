from django.urls import path, include

from fegsurveyapp import views

urlpatterns = [
    path('', views.surveypage, name='surveypage'),
    path('dashboard/survey/', views.surveycreatepage, name='survey_create'),
    path('dashboard/survey/list/', views.surveylist, name='survey_list'),
    path('dashboard/survey/<int:pk>/edit/', views.surveyedit, name='survey_edit'),
    path('dashboard/survey/<int:pk>/delete/', views.surveydelete, name='survey_delete'),
    path('dashboard/survey/<int:pk>/question/', views.survey_add_question, name='survey_add_question'),
    path('dashboard/survey/<int:survey_pk>/question/<int:question_pk>/options/', views.survey_option_create,
         name='survey_option_create'),
    path('dashboard/survey/<int:pk>/detail', views.survey_details, name='survey_detail'),



]
