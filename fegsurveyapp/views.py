from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
# Create your views here.
from django.views.generic import DeleteView

from fegsurveyapp.forms import SurveyForm, QuestionForm, OptionForm, AttendSurveyForm
from fegsurveyapp.models import Survey, Question, Options, SurveyEntry


class AdminLogin(LoginView):
    template_name = "loginpage.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('surveypage')
        return super(AdminLogin, self).dispatch(request, *args, **kwargs)


def dashboard(request):
    surveys = Survey.objects.all()
    print(surveys)

    for data in surveys:
        question = Question.objects.filter(survey=data)
        print(question.count())
        num_survey = data.surveyentry_set.all().count()
        num_question = question.count()
        data.response = round(num_survey/num_question)

    context = {
        'surveys': surveys,
    }
    return render(request, "dashboard.html", context)


@login_required
def surveypage(request):
    surveys = Survey.objects.all().order_by("-pub_date")
    if surveys:
        return render(request, "survey.html", {"surveys": surveys})
    else:
        return render(request, "survey.html")


@login_required
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


@login_required
def surveyedit(request, pk):
    """can add questions to a draft survey, then acitvate the survey"""
    try:
        survey = Survey.objects.get(pk=pk, is_active=False)
        print("Survey Name:", survey)
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


@login_required
def survey_add_question(request, pk):
    """U can add a question to a draft survey"""
    survey = get_object_or_404(Survey, pk=pk)
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.survey = survey
            question.save()
            if question.answer_type == "text" or question.answer_type == "date":
                return redirect("survey_edit", pk=pk)
            else:
                return redirect("survey_option_create", survey_pk=pk, question_pk=question.pk)
    else:
        form = QuestionForm()
    return render(request, "addquestions.html", {"survey": survey, "form": form})


@login_required
def survey_option_create(request, survey_pk, question_pk):
    """can add options to a survey question"""
    survey = get_object_or_404(Survey, pk=survey_pk)
    question = Question.objects.get(pk=question_pk)
    print("Option Create for question:", question)
    if request.method == "POST":
        form = OptionForm(request.POST)
        if form.is_valid():
            options = form.save(commit=False)
            options.question_id = question_pk
            options.save()
    else:
        form = OptionForm()
    print(Options.objects.filter(question=question))
    aoptions = question.options_set.all()
    print("options", aoptions)

    return render(request, "options.html",
                  {"survey": survey, "question": question, "options": aoptions, "form": form})


@login_required
def survey_details(request, pk):
    try:
        print("inside")
        survey = Survey.objects.prefetch_related("question_set__options_set").get(pk=pk, is_active=True)
    except Survey.DoesNotExist:
        raise Http404("Sorry No Surveys Activated")
    questions = survey.question_set.all()
    """    Here ANALYTICS CODE HAS TO BE WRITTEN     """
    for question in questions:
        option_pks = question.options_set.all().values_list("pk", flat=True)
        total_answers = SurveyEntry.objects.filter(answers__in=option_pks).count()
        for option in question.options_set.all():
            num_answers = SurveyEntry.objects.filter(answers=option).count()
            option.percent = 100.0 * num_answers / total_answers if total_answers else 0
    return render(request, "details.html", {"survey": survey, "questions": questions})


def survey_question_edit(request, pk,question_pk):
    pass


def survey_question_delete(request, question_pk):
    """delete a question from survey"""
    if request.method == "POST":
        question = get_object_or_404(Question, pk=question_pk)
        question.delete()
    return redirect("surveypage")


@login_required
def surveylist(request):
    """can view all their surveys"""
    surveys = Survey.objects.all().order_by("-pub_date")
    return render(request, "list.html", {"surveys": surveys})


@login_required
def surveydelete(request, pk):
    """delete an existing survey"""
    survey = get_object_or_404(Survey, pk=pk)
    if request.method == "POST":
        survey.delete()
    return redirect("surveypage")


"""
*******************************************************************
                        Survey Submission part
*******************************************************************
"""


def attend_survey(request):
    """can view all their surveys"""
    surveys = Survey.objects.all().order_by("-pub_date")
    if surveys:
        return render(request, "attendsurveylist.html", {"surveys": surveys})
    else:
        return render(request, "attendsurveylist.html")


def survey_starts(request, pk):
    """can start a survey using this function"""
    survey = get_object_or_404(Survey, pk=pk)
    # print("survey list", survey)
    if request.method == "POST":
        form = AttendSurveyForm(request.POST)
        if form.is_valid():
            surveyentry = form.save(commit=False)
            print(surveyentry)
            name = surveyentry.name
            email = surveyentry.email
            # surveyentry.survey_id = pk
            # surveyentry.save()
            return redirect("survey_submit", survey_pk=pk, name=name, email=email)
    else:
        form = AttendSurveyForm()

    return render(request, "surveystart.html", {"survey": survey, "form": form})


def survey_submit(request, survey_pk, name, email):
    """Survey-taker submit their completed survey."""
    try:
        survey = Survey.objects.prefetch_related("question_set__options_set").get(pk=survey_pk, is_active=True)
    except Survey.DoesNotExist:
        raise Http404("Sorry No Surveys Activated")
    questions = survey.question_set.all()
    if request.method == "POST":
        request.POST._mutable = True
        formdata = request.POST.copy()
        del formdata['csrfmiddlewaretoken']
        for questionid in formdata:
            questionobj = Question.objects.get(id=questionid)
            surveydata = SurveyEntry.objects.create(survey=survey, question=questionobj, name=name, email=email)
            for answervalue in formdata.getlist(questionid):
                try:
                    ans_obj = Options.objects.get(id=answervalue, question=questionobj)
                    surveydata.answers.add(ans_obj)
                    surveydata.save()
                except Exception as e:
                    if isinstance(answervalue, str):
                        surveydata.answertext = answervalue
                        surveydata.save()
        messages.success(request, "Submitted Successfully")
        return redirect("attend_survey")
        # print(list(SurveyEntry.objects.all().values()))
    return render(request, "surveysubmit.html", {"survey": survey, "questions": questions})


def survey_thanks(request, pk):
    """Survey-taker receives a thank-you message."""
    survey = Survey.objects.filter(pk=pk).all()
    return render(request, "surveythanks.html", {"surveys": survey})
