import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.utils.encoding import smart_str

from accounts.models import Professor, Student
from courses.models import Quiz, Assignment, Homework, Survey

def index(request):
    context_dict = {}

    quizzes = []
    homeworks = []
    surveys = []

    if request.user.is_authenticated and request.user.role == 1:
        d = datetime.datetime.today()
        prof = Professor.objects.get(id=request.user.id)
        courses = prof.courses.all()

        x = 0
        for course in courses:

            for quiz in course.quizes.all():
                if quiz.due_date.replace(tzinfo=None) > d and x < 5:
                    print(quiz.assignment_name)
                    quizzes.append(quiz)
                    x+=1
            x = 0
            for homework in course.homeworks.all():
                if homework.due_date.replace(tzinfo=None) > d and x < 5:
                    homeworks.append(homework)
                    x+=1
            x = 0
            for survey in course.surveys.all():
                if survey.due_date.replace(tzinfo=None) > d and x < 5:
                    surveys.append(survey)
                    x+=1
        context_dict['courses'] = courses

    elif request.user.is_authenticated and request.user.role == 2:
        d = datetime.datetime.today()
        std = Student.objects.get(id=request.user.id)
        courses = std.courses.all()


        x = 0
        for course in courses:

            for quiz in course.quizes.all():
                #print(quiz.assignment_name)
                if quiz.due_date.replace(tzinfo=None) > d and x < 5:
                    quizzes.append(quiz)
                    x += 1
            x = 0
            for homework in course.homeworks.all():
                if homework.due_date.replace(tzinfo=None) > d and x < 5:
                    homeworks.append(homework)
                    x += 1
            x = 0
            for survey in course.surveys.all():
                if survey.due_date.replace(tzinfo=None) > d and x < 5:
                    surveys.append(survey)
                    x += 1
        context_dict['courses'] = courses

    context_dict['homeworks'] = homeworks
    context_dict['surveys'] = surveys
    context_dict['quizzes'] = quizzes


    return render(request, 'index.html', context_dict)

def download(request, id):
    assignment = Assignment.objects.get(id=id)

    if assignment.type == 0:
        quiz = Quiz.objects.get(id=id)
        fName = quiz.file.name.split('/')[-1]
        response = HttpResponse(quiz.file, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(fName)

    elif assignment.type == 2:
        hw = Homework.objects.get(id=id)
        fName = hw.file.name.split('/')[-1]
        response = HttpResponse(hw.file, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(fName)

    elif assignment.type == 1:
        survey = Survey.objects.get(id=id)
        fName = survey.file.name.split('/')[-1]
        response = HttpResponse(survey.file, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(fName)

    return response
