from django.contrib.auth.models import User
from django.forms import ModelForm, CharField, TextInput, Select, EmailField

from fegsurveyapp.models import Survey, Question, Options, SurveyEntry

CHOICE_VALUE = [
    ('text', 'Textbox'),
    ('radio', 'Radio Button'),
    ('checkbox', 'Checkbox'),
    ('date', 'Date'),
]


class SurveyForm(ModelForm):
    title = CharField(widget=TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Survey title here'}))

    class Meta:
        model = Survey
        fields = ["title"]


class QuestionForm(ModelForm):
    text = CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your Question here'
    }))
    answer_type = CharField(widget=Select(choices=CHOICE_VALUE, attrs={'class': 'form-control'}))

    class Meta:
        model = Question
        fields = ['text', 'answer_type']


class OptionForm(ModelForm):
    text = CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your answer here'
    }))

    class Meta:
        model = Options
        fields = ["text"]


class AttendSurveyForm(ModelForm):
    name = CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your Name here',
    }))
    email = CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your Email address here',
    }))

    class Meta:
        model = SurveyEntry
        fields = ['name', 'email']


class LoginForms(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
