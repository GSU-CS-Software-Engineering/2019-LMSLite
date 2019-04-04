from django.shortcuts import render
from django import forms

from accounts.models import Professor
from courses.models import Course
from courses.forms import QuizFileForm, QuizEditForm, HomeworkCreationForm
from django.core.files.storage import default_storage


def course_view(request, id):
	context_dict = {}
	course = Course.objects.get(id=id)

	context_dict['course'] = course
	context_dict['quizform'] = QuizFileForm
	context_dict['hwForm'] = HomeworkCreationForm

	if 'quizSubmit' in request.POST:
		quiz = QuizFileForm(request.POST, request.FILES)
		quiz.save(course=course, prof=Professor.objects.get(id=request.user.id))
		edit = QuizEditForm
		context_dict['quizform'] = edit

	return render(request, 'course_page.html', context_dict)
# Create your views here.
