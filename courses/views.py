from django.shortcuts import render
from django import forms

from accounts.models import Professor
from courses.models import Course, Quiz
from courses.forms import QuizFileForm, QuizEditForm, HomeworkCreationForm, create_quiz


def course_view(request, id):

	context_dict = {}
	course = Course.objects.get(id=id)
	quiz = QuizFileForm(request.POST, request.FILES)

	context_dict['course'] = course
	context_dict['quizform'] = quiz
	context_dict['hwForm'] = HomeworkCreationForm
	context_dict['quizes'] = course.quizes.all()

	if 'quizSubmit' in request.POST:
		quiz.save(course=course, prof=Professor.objects.get(id=request.user.id))
		edit = QuizEditForm
		edit.file_address = quiz.quiz_url()
		context_dict['quizform'] = edit

	return render(request, 'course_page.html', context_dict)
# Create your views here.


def quiz_view(request, cid, id):
	context_dict = {}
	quiz = Quiz.objects.get(id=id)
	questions = create_quiz(input='static/Sample_Quiz.txt')
	cid = quiz.course_id
	context_dict['questions'] = questions
	context_dict['quiz'] = quiz
	return render(request, 'quiz_page.html', context_dict)

