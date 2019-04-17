import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.utils.encoding import smart_str

from accounts.models import Professor
from courses.models import Course, Quiz, Assignment, Homework, Survey
from courses.forms import QuizFileForm, QuizEditForm, HomeworkCreationForm

def index(request):
    context_dict = {}

    if request.user.is_authenticated and request.user.role == 1:
        d = datetime.datetime.today()
        prof = Professor.objects.get(id=request.user.id)
        courses = prof.courses.all()
        quizzes = []

        x = 0
        for course in courses:
            for quiz in course.quizes.all():
                if quiz.due_date.replace(tzinfo=None) > d and x < 5:
                    quizzes.append(quiz)
                    x+=1

        context_dict['quizzes'] = quizzes
        context_dict['courses'] = courses


    return render(request, 'index.html', context_dict)

def download(request, id):
    response = HttpResponse(content_type='application/force-download')
    assignment = Assignment.objects.get(id=id)

    if assignment.type == 0:
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(Quiz.objects.get(id=id).file.name)

    elif assignment.type == 2:
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(Homework.objects.get(id=id).file.name)

    elif assignment.type == 1:
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(Survey.objects.get(id=id).file.name)

    return response
