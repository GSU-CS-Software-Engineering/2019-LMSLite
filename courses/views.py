from django.shortcuts import render
from django import forms

from courses.models import Course
from courses.forms import QuizEditForm, HomeworkCreationForm


def course_view(request, id):
	context_dict = {}
	course = Course.objects.get(id=id)

	context_dict['course'] = course
	context_dict['quizform'] = QuizEditForm
	context_dict['hwForm'] = HomeworkCreationForm
	return render(request, 'course_page.html', context_dict)
# Create your views here.
