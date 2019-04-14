import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.utils.encoding import smart_str

from accounts.models import Professor
from courses.models import Assignment


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
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(Assignment.objects.get(id=id))

    return response
