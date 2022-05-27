from django.db import models

# Create your models here.
CHOICES = ((1, 'BAD'), (2, 'AVERAGE'), (3, 'GOOD'), (4, 'Excellent'))
CHOICE_VALUE = [
    ('text', 'Textbox'),
    ('radio', 'Radio Button'),
    ('checkbox', 'Checkbox'),
]


class Survey(models.Model):
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False, null=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    survey = models.ForeignKey(Survey, blank=True, null=True, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    answer_type = models.CharField(max_length=64, blank=True, null=True, choices=CHOICE_VALUE, default="text")

    def __str__(self):
        return self.text


class Answers(models.Model):
    question = models.ForeignKey(Question, blank=True, null=True, on_delete=models.CASCADE)
    text = models.CharField(max_length=128, null=True)

    def __str__(self):
        return self.text


"""
These data holds a set of survey entries 
"""


class SurveyEntry(models.Model):
    """A set of answers a survey's questions."""
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    submit_date = models.DateTimeField(auto_now_add=True)
    is_complete = models.BooleanField(default=False, null=True)
    answers = models.ManyToManyField(Answers, null=True)

    def __str__(self):
        return f'self.name'

#
# class Answer(models.Model):
#     """An answer a survey's questions."""
#     surveyentry = models.ForeignKey(SurveyEntry, on_delete=models.CASCADE, null=True)
#     answers = models.ForeignKey(Answers, on_delete=models.CASCADE, null=True)


