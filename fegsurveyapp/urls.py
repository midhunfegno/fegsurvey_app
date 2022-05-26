from django.urls import path, include

from fegsurveyapp import views

urlpatterns = [
    # path('home/', views.homepage, name='homepage'),
    path('', views.surveypage, name='surveypage'),
    path('dashboard/survey/', views.surveycreatepage, name='survey_create'),
    path('dashboard/survey/list/', views.surveylist, name='survey_list'),
    # path('survey/edit/', views.surveyedit, name='survey_save'),
    path('dashboard/survey/<int:pk>/edit/', views.surveyedit, name='survey_edit'),
    path('dashboard/survey/<int:pk>/delete/', views.surveydelete, name='survey_delete'),
    path('dashboard/survey/<int:pk>/question/', views.survey_add_question, name='survey_add_question'),
    path('dashboard/survey/<int:survey_pk>/question/<int:question_pk>/options/', views.survey_option_create,
         name='survey_option_create'),
    path('dashboard/survey/<int:pk>/detail', views.survey_details, name='survey_detail'),

    path("survey/start/", views.attend_survey, name="attend_survey"),
    path("survey/start/<int:pk>/", views.survey_starts, name="survey_start"),
    path("survey/<int:survey_pk>/submit/<int:ans_pk>/", views.survey_submit, name="survey_submit"),
    path("survey/<int:pk>/thanks/", views.survey_thanks, name="survey_thanks"),

]
