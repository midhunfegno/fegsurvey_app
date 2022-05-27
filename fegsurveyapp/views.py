from django.db import transaction
from django.forms import formset_factory
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from fegsurveyapp.forms import SurveyForm, QuestionForm, OptionForm
from fegsurveyapp.models import Survey, Question, Answers, SurveyEntry


# def homepage(request):
#     return render(request, 'index.html')


def surveypage(request):
    surveys = Survey.objects.all().order_by("-pub_date")
    if surveys:
        return render(request, "survey.html", {"surveys": surveys})
    else:
        return render(request, "survey.html")


def surveycreatepage(request):
    """can create a new survey"""
    if request.method == "POST":
        form = SurveyForm(request.POST)
        if form.is_valid():
            formdata = form.save(commit=False)
            formdata.save()
            return redirect("survey_edit", pk=formdata.id)
    else:
        form = SurveyForm()
    return render(request, 'createsurvey.html', {"form": form})


def surveyedit(request, pk):
    """can add questions to a draft survey, then acitvate the survey"""
    try:

        print("halo")
        survey = Survey.objects.get(pk=pk, is_active=False)
        print("edit survey:", survey)
    except Survey.DoesNotExist:
        raise Http404()

    if request.method == "POST":
        survey.is_active = True
        survey.save()
        print("survey", survey)
        return redirect("survey_detail", pk=pk)
    else:
        questions = survey.question_set.all()
        return render(request, 'editsurvey.html', {"survey": survey, "questions": questions})


def surveydelete(request, pk):
    """delete an existing survey"""
    survey = get_object_or_404(Survey, pk=pk)
    if request.method == "POST":
        survey.delete()
    return redirect("surveypage")


def surveylist(request):
    """can view all their surveys"""
    surveys = Survey.objects.all().order_by("-pub_date")
    return render(request, "list.html", {"surveys": surveys})


def survey_add_question(request, pk):
    """Ucan add a question to a draft survey"""
    survey = get_object_or_404(Survey, pk=pk)
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.survey = survey
            question.save()
            print(question.pk, pk)
            return redirect("survey_option_create", survey_pk=pk, question_pk=question.pk)
    else:
        form = QuestionForm()
    return render(request, "addquestions.html", {"survey": survey, "form": form})


def survey_option_create(request, survey_pk, question_pk):
    """can add options to a survey question"""
    survey = get_object_or_404(Survey, pk=survey_pk)
    question = Question.objects.get(pk=question_pk)
    print("question", question)
    if request.method == "POST":

        form = OptionForm(request.POST)
        if form.is_valid():
            options = form.save(commit=False)
            options.question_id = question_pk
            options.save()
    else:
        form = OptionForm()
    print(Answers.objects.filter(question=question))
    aoptions = question.answers_set.all()
    print("options", aoptions, form)

    return render(request, "options.html",
                  {"survey": survey, "question": question, "options": aoptions, "form": form})


def survey_details(request, pk):
    try:
        print("inside")
        survey = Survey.objects.prefetch_related("question_set__answers_set").get(pk=pk, is_active=True)
    except Survey.DoesNotExist:
        raise Http404("Sorry No Surveys Activated")
    questions = survey.question_set.all()
    # for question in questions:
    #     option_keys = question.answers_set.values_list("pk", flat=True)
    #     total_answers = Answers.objects.filter(answers_id__in=option_keys).count()
    #     for option in question.answers_set.all():
    #         num_answers = Answers.objects.filter(answers=option).count()
    #         option.percent = 100.0 * num_answers / total_answers if total_answers else 0
    return render(request, "details.html", {"survey": survey, "questions": questions})


"""
Survey Entry part
"""


def attend_survey(request):
    """can view all their surveys"""
    surveys = Survey.objects.all().order_by("-pub_date")
    print(surveys)
    if surveys:
        return render(request, "attendsurveylist.html", {"surveys": surveys})
    else:
        return render(request, "attendsurveylist.html")


def survey_starts(request, pk):
    """can start a survey using this function"""
    survey = get_object_or_404(Survey, pk=pk)
    print("survey list", survey)
    if request.method == "POST":
        ans = SurveyEntry.objects.create(survey=survey)
        print("answer created", ans)
        return redirect("survey_submit", survey_pk=pk, ans_pk=ans.pk)
    return render(request, "surveystart.html", {"survey": survey})


def survey_thanks(request, pk):
    """Survey-taker receives a thank-you message."""
    survey = get_object_or_404(Survey, pk=pk, is_active=True)
    return render(request, "surveythanks.html", {"survey": survey})


def survey_submit(request, survey_pk, ans_pk):
    """Survey-taker submit their completed survey."""
    try:
        survey = Survey.objects.prefetch_related("question_set__answers_set").get(pk=survey_pk, is_active=True)
        print("survey", survey)
    except Survey.DoesNotExist:
        raise Http404("Sorry No Surveys Activated")
    try:
        sub = SurveyEntry.objects.get(pk=ans_pk)
        print(sub)
    except SurveyEntry.DoesNotExist:
        raise Http404()
    questions = survey.question_set.all()
    if request.method == "POST":
        request.POST._mutable = True
        formdata = request.POST
        del formdata['csrfmiddlewaretoken']
        print(formdata)
        for key in formdata:
            for d in formdata[key]:
                print(key,d)

            print(key,formdata[key])
    return render(request, "surveysubmit.html", {"survey": survey, "questions": questions})



