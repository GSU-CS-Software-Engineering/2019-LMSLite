from django.shortcuts import render
from tempfile import NamedTemporaryFile

from LMSLite.helpers import grade_quiz, reset_quiz, create_quiz
from accounts.models import Professor
from courses.models import Course, Quiz
from courses.forms import QuizFileForm, QuizEditForm, HomeworkCreationForm
from google.cloud import storage


def course_view(request, id):

	context_dict = {}
	course = Course.objects.get(id=id)
	quiz = QuizFileForm(request.POST, request.FILES)
	homework = HomeworkCreationForm(request.POST, request.FILES)
	context_dict['course'] = course
	context_dict['quizform'] = quiz
	context_dict['hwForm'] = homework
	context_dict['quizes'] = course.quizes.all()

	if 'quizSubmit' in request.POST:
		quiz.save(course=course, prof=Professor.objects.get(id=request.user.id))

		edit = QuizEditForm

		client = storage.Client()
		bucket = client.get_bucket('lms-lite-2019')
		blob = bucket.get_blob('quiz/' + request.FILES['file'].name)

		downloaded_blob = blob.download_as_string()

		quizKey = NamedTemporaryFile(delete=False)
		quizKey.write(bytes(downloaded_blob.decode('utf8'), 'UTF-8'))
		quizKey.seek(0)

		edit.file_address = quizKey.name
		context_dict['quizform'] = edit

	if 'hmwkSubmit' in request.POST:
		homework.save(course=course, prof=Professor.objects.get(id=request.user.id))

	return render(request, 'course_page.html', context_dict)


def quiz_view(request, cid, id):
	context_dict = {}
	quiz = Quiz.objects.get(id=id)
	cid = quiz.course_id
	context_dict['quiz'] = quiz
	context_dict['course'] = cid

	client = storage.Client()
	bucket = client.get_bucket('lms-lite-2019')
	blob = bucket.get_blob(quiz.file.name)

	downloaded_blob = blob.download_as_string()

	quizKey = NamedTemporaryFile(delete=False)
	quizKey.write(bytes(downloaded_blob.decode('utf8'), 'UTF-8'))
	quizKey.seek(0)

	questions = create_quiz(input=quizKey.name)
	quizKey.seek(0)

	context_dict['questions'] = questions

	if request.method == "POST":
		stdQuiz = NamedTemporaryFile(delete=False)
		reset_quiz(quizKey.name, stdQuiz.name, request.POST)

		quizKey.seek(0)
		stdQuiz.seek(0)
		print(grade_quiz(stdQuiz.name, quizKey.name))
		#context_dict['grade'] = grade_quiz(stdQuiz.name, quizKey.name)
		return render(request, 'post_quiz_page.html', context_dict)

	return render(request, 'quiz_page.html', context_dict)


def quiz_list_view(request, cid):
	context_dict = {}
	quizzes = Course.objects.get(id=cid).quizes.all()
	context_dict['quizzes'] = quizzes
	return render(request, 'quiz_list_page.html', context_dict)

def pre_quiz_view(request):
	context_dict = {}

	return render(request, context_dict)

def post_quiz_view(request):
	context_dict = {}


	return render(request,'post_quiz_page.html', context_dict)