from django.db import models

# Create your models here.
CHOICES = ((1, 'BAD'), (2, 'AVERAGE'), (3, 'GOOD'), (4, 'Excellent'))
CHOICE_VALUE = [
    ('text', 'Textbox'),
    ('radio', 'Radio Button'),
    ('checkbox', 'Checkbox'),
    ('date', 'Date'),
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


class Options(models.Model):
    question = models.ForeignKey(Question, blank=True, null=True, on_delete=models.CASCADE)
    text = models.CharField(max_length=128, null=True)


"""
These data holds a set of survey entries 
"""


class SurveyEntry(models.Model):
    """A set of answers a survey's questions."""
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255,null=True)
    email = models.EmailField(max_length=255)
    submit_date = models.DateTimeField(auto_now_add=True)
    is_complete = models.BooleanField(default=False, null=True)
    answers = models.ManyToManyField(Options, null=True)
    answertext = models.CharField(max_length=255, blank=True, null=True)


