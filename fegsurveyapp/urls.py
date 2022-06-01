from django.urls import path, include
from django.contrib.auth.views import LogoutView
from fegsurveyapp import views
from fegsurveyapp.views import AdminLogin

urlpatterns = [

    path('login/', AdminLogin.as_view(), name='loginpage'),
    path('logout/', LogoutView.as_view(), name='logoutpage'),
    path('home/', views.surveypage, name='surveypage'),
    path('create/', views.surveycreatepage, name='survey_create'),
    path('list/', views.surveylist, name='survey_list'),
    path('edit/<int:pk>', views.surveyedit, name='survey_edit'),
    path('delete/<int:pk>', views.surveydelete, name='survey_delete'),
    path('question/<int:pk>', views.survey_add_question, name='survey_add_question'),
    path('/question/<int:survey_pk>/<int:question_pk>/options/', views.survey_option_create,
         name='survey_option_create'),
    path('detail/<int:pk>', views.survey_details, name='survey_detail'),



]
