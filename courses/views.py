import datetime

from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from tempfile import NamedTemporaryFile

from LMSLite.helpers import grade_quiz, reset_quiz, create_quiz, update_quiz
from accounts.models import Professor, Student
from courses.models import Course, Quiz, Grade, Homework, Survey
from courses.forms import QuizFileForm, QuizEditForm, HomeworkCreationForm, GradeEditForm, SurveyFileForm, SurveyEditForm
from google.cloud import storage


def course_view(request, id):

	context_dict = {}
	course = Course.objects.get(id=id)
	quiz = QuizFileForm(request.POST, request.FILES)
	homework = HomeworkCreationForm(request.POST, request.FILES)
	survey = SurveyFileForm(request.POST, request.FILES)

	context_dict['course'] = course
	context_dict['quizform'] = quiz
	context_dict['hwForm'] = homework
	context_dict['surveyForm'] = survey
	context_dict['quizes'] = course.quizes.all()

	if 'quizFileUpdate' in request.POST:
		print(request.POST)
		post = request.POST.copy()
		update_quiz(Quiz.objects.order_by('id')[len(Quiz.objects.all()) - 1].file.name, post)
		#return redirect('index')

	if 'surveyFileUpdate' in request.POST:
		post = request.POST.copy()
		update_quiz(Survey.objects.order_by('id')[len(Survey.objects.all()) - 1].file.name, post)
		return redirect('index')


	if 'surveySubmit' in request.POST:
		survey.save(course=course, prof=Professor.objects.get(id=request.user.id))

		edit = SurveyEditForm

		client = storage.Client()
		bucket = client.get_bucket('lms-lite-2019')
		blob = bucket.get_blob(course.course_name + '/Surveys/' +request.POST['assignment_name']+'/'+request.POST['assignment_name'].replace(' ', '_') +'_key.txt')
		downloaded_blob = blob.download_as_string()

		quizKey = NamedTemporaryFile(delete=False)
		quizKey.write(bytes(downloaded_blob.decode('utf8'), 'UTF-8'))
		quizKey.seek(0)

		edit.file_address = quizKey.name
		context_dict['surveyForm'] = edit


	if 'quizSubmit' in request.POST:
		quiz.save(course=course, prof=Professor.objects.get(id=request.user.id))

		edit = QuizEditForm

		client = storage.Client()
		bucket = client.get_bucket('lms-lite-2019')
		blob = bucket.get_blob(course.course_name + '/Quizzes/' +request.POST['assignment_name']+'/'+request.POST['assignment_name'].replace(' ', '_') +'_key.txt')
		downloaded_blob = blob.download_as_string()

		quizKey = NamedTemporaryFile(delete=False)
		quizKey.write(bytes(downloaded_blob.decode('utf8'), 'UTF-8'))
		quizKey.seek(0)

		edit.file_address = quizKey.name
		context_dict['quizform'] = edit
		context_dict['fileAddr'] = course.course_name + '/Quizzes/' +request.POST['assignment_name']+'/'+request.POST['assignment_name'].replace(' ', '_') +'_key.txt'

	if 'hmwkSubmit' in request.POST:
		homework.save(course=course, prof=Professor.objects.get(id=request.user.id))
		return redirect('index')

	return render(request,  'course_page.html', context_dict)


def quiz_view(request, cid, id):
	context_dict = {}
	quiz = Quiz.objects.get(id=id)
	cid = quiz.course_id
	student = Student.objects.get(id=request.user.id)
	context_dict['quiz'] = quiz
	context_dict['course'] = cid

	client = storage.Client()
	bucket = client.get_bucket('lms-lite-2019')
	key_blob = bucket.get_blob(quiz.file.name)

	downloaded_blob = key_blob.download_as_string()

	quizKey = NamedTemporaryFile(delete=False)
	quizKey.write(bytes(downloaded_blob.decode('utf8'), 'UTF-8'))
	quizKey.seek(0)

	questions = create_quiz(input=quizKey.name)
	quizKey.seek(0)

	context_dict['questions'] = questions

	if 'btn_done' in request.POST:
		return redirect(course_view(request, cid.id))

	if request.method == "POST":
		stdQuiz = NamedTemporaryFile(delete=False)

		response_loc = '/'.join((cid.course_name, 'Quizzes', quiz.assignment_name, 'Responses', request.user.email.split('@')[0]+'_response.txt'))

		response_file = reset_quiz(quizKey.name, response_loc, request.POST)


		std_quiz_blob = bucket.get_blob(response_loc)

		download = std_quiz_blob.download_as_string()
		stdQuiz.write(bytes(download.decode('utf8'), 'UTF-8'))


		quizKey.seek(0)
		stdQuiz.seek(0)

		score = grade_quiz(stdQuiz.name, quizKey.name)

		context_dict['grade'] = score

		grade = Grade()
		grade.assignment = quiz
		grade.file = response_file.name
		grade.grade_value = score
		grade.stdnt = student
		grade.save()
		student.quizes.remove(quiz)
		student.grades.add(grade)

		return render(request, 'post_quiz_page.html', context_dict)

	return render(request, 'quiz_page.html', context_dict)


def quiz_list_view(request, cid):
	context_dict = {}
	course = Course.objects.get(id=cid)
	quizzes = Student.objects.get(id=request.user.id).quizes.all()
	student = Student.objects.get(id=request.user.id)


	context_dict['quizzes'] = quizzes
	context_dict['course'] = course

	for quiz in quizzes:
		if quiz.restrict_date:
			if quiz.restrict_date.replace(tzinfo=None) <= datetime.datetime.today():
				student.quizes.remove(quiz)

	return render(request, 'quiz_list_page.html', context_dict)


def pre_quiz_view(request,id, cid):
	context_dict = {}
	quiz = Quiz.objects.get(id=id)
	context_dict['quiz'] = quiz
	student = Student.objects.get(id=request.user.id)

	if request.method == 'POST':
		if quiz.quiz_code:
			print("Here")
			if quiz.quiz_code == request.POST['quiz-code']:
				student.quizes.remove(quiz)
				return redirect('quiz_page', quiz.course_id.id, quiz.id)
			else:
				return render(request, 'pre_quiz_page.html', context_dict)

		return redirect('quiz_page', quiz.course_id.id, quiz.id)

	return render(request,'pre_quiz_page.html', context_dict)


def grade_view(request, cid):
	context_dict = {}
	quiz_grades = []
	hw_grades = []


	course = Course.objects.get(id=cid)

	quizzes = course.quizes.all()
	homeworks = course.homeworks.all()
	surveys = course.surveys.all()

	quiz_average = 0
	k = 0
	for quiz in quizzes:
		for student in course.students.all():
			try:
				grade = student.grades.get(assignment=quiz)
				quiz_average += grade.grade_value
				quiz_grades.append(grade)
				k += 1
			except:
				pass
		if k > 0:
			quiz_average /= k
			quiz_average = round(quiz_average, 2)
			quiz.average = quiz_average
			k = 0


	for homework in homeworks:
		for student in course.students.all():
			try:
				grade = student.grades.get(assignment=homework)
				hw_grades.append(grade)
			except:
				pass




	context_dict['quiz_average'] = quiz_average
	context_dict['course'] = course
	context_dict['quizzes'] = quizzes
	context_dict['homeworks'] = homeworks
	context_dict['surveys'] = surveys
	context_dict['quiz_grades'] = quiz_grades
	context_dict['hw_grades'] = hw_grades


	return render(request, 'assignment_list.html', context_dict)


def submission_view(request, cid, id):
	context_dict = {}

	grade = Grade.objects.get(id=id)
	grade_form = GradeEditForm(request.POST, instance=grade)
	context_dict['grade'] = grade
	context_dict['grade_form'] = grade_form

	client = storage.Client()
	bucket = client.get_bucket('lms-lite-2019')
	blob = bucket.get_blob(grade.file.name)

	downloaded_blob = blob.download_as_string()
	response = NamedTemporaryFile(delete=False)
	response.write(bytes(downloaded_blob.decode('utf8'), 'UTF-8'))
	response.seek(0)

	questions = create_quiz(response.name)

	context_dict['questions'] = questions

	if request.method == 'POST':
		grade_form.save()
		grade.stdnt.grades.add(grade)
		return redirect('/courses/'+str(grade.assignment.course_id.id) +'/grades')

	return render(request,'submission_view.html',context_dict)


def homework_view(request,id):
	context_dict = {}

	course = Course.objects.get(id=id)
	homework = Student.objects.get(id=request.user.id).homeworks.all()

	context_dict['homework'] = homework
	context_dict['course'] = course

	return render(request,'homework_list.html',context_dict)


def homework_submit_view(request,id,cid):
	context_dict = {}

	homework = Homework.objects.get(id=id)
	student = Student.objects.get(id=request.user.id)

	if homework.restrict_date.replace(tzinfo=None) <= datetime.datetime.today():
		student.homeworks.remove(homework)

	context_dict['homework'] = homework

	if request.method == 'POST':
		sub_addr = homework.course_id.course_name + '/Homework/' + homework.assignment_name + '/Submissions/' + \
				   Student.objects.get(id=request.user.id).email.split('@')[0] + '/' + request.FILES['upload'].name
		default_storage.save(sub_addr, request.FILES['upload'])
		grade = Grade()
		grade.assignment = homework
		grade.grade_value = 0
		grade.file = sub_addr
		grade.stdnt = student
		grade.save()

		if request.method == 'POST':
			student.homeworks.remove(homework)

		return redirect('index')


	return render(request,'homework_submit_page.html',context_dict)


def survey_list_view(request,cid):
	context_dict = {}

	course = Course.objects.get(id=cid)
	surveys = Student.objects.get(id=request.user.id).surveys.all()
	student = Student.objects.get(id=request.user.id)

	context_dict['course'] = course
	context_dict['survey'] = surveys


	for survey in surveys:
		if survey.restrict_date.replace(tzinfo=None) <= datetime.datetime.today():
			student.surveys.remove(survey)

	return render(request, 'survey_list_view.html', context_dict)

def pre_survey_view(request,id, cid):
	context_dict = {}
	survey = Survey.objects.get(id=id)
	context_dict['survey'] = survey

	student = Student.objects.get(id=request.user.id)

	if request.method == 'POST':
		student.surveys.remove(survey)

	return render(request,'pre_survey_page.html', context_dict)

def take_survey_view(request,id,cid):
	context_dict = {}
	survey = Survey.objects.get(id=id)
	cid = survey.course_id
	student = Student.objects.get(id=request.user.id)
	context_dict['survey'] = survey
	context_dict['course'] = cid

	client = storage.Client()
	bucket = client.get_bucket('lms-lite-2019')
	key_blob = bucket.get_blob(survey.file.name)

	downloaded_blob = key_blob.download_as_string()

	surveyKey = NamedTemporaryFile(delete=False)
	surveyKey.write(bytes(downloaded_blob.decode('utf8'), 'UTF-8'))
	surveyKey.seek(0)

	questions = create_quiz(input=surveyKey.name)
	surveyKey.seek(0)

	context_dict['questions'] = questions
	if request.method=='POST':
		return render(request, 'post_survey_page.html', context_dict)
	return render(request,'survey_page.html',context_dict)
