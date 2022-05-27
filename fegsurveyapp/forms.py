from django.forms import ModelForm, CharField, TextInput, Select, BaseFormSet, Form, RadioSelect, ChoiceField, \
    EmailField

from fegsurveyapp.models import Survey, Question, Answers, SurveyEntry

CHOICE_VALUE = [
    ('text', 'Textbox'),
    ('radio', 'Radio Button'),
    ('checkbox', 'Checkbox'),
]


class SurveyForm(ModelForm):
    title = CharField(widget=TextInput(attrs={'class': 'form-control'}))

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
        model = Answers
        fields = ["text"]


# class AnswerForm(Form):
#     def __init__(self, *args, **kwargs):
#         options = kwargs.pop("options")
#         # Options must be a list of Option objects
#         choices = {(opt.pk, opt.text) for opt in options}
#         super().__init__(*args, **kwargs)
#         option_field = ChoiceField(choices=choices, widget=RadioSelect, required=True)
#         self.fields["option"] = option_field
#
#
# class BaseAnswerFormSet(BaseFormSet):
#     """
#     A collection of instances of the same Form class ie,.....(AnswerForm)
#     """
#     def get_form_kwargs(self, index):
#         kwargs = super().get_form_kwargs(index)
#         kwargs["options"] = kwargs["options"][index]
#         return kwargs

