import csv

from django import forms
from django.core.files.storage import FileSystemStorage
from google.cloud import storage
from .models import Course, Quiz, Homework
from accounts.models import Professor


class CourseAdminCreationForm(forms.ModelForm):

	class Meta:
		model = Course
		fields = ('course_name', 'description')

	def save(self, commit=True):
		# Save the provided password in hashed format
		course = super(CourseAdminCreationForm, self).save(commit=False)

		if commit:
			course.save()
		return course


class CourseAdminChangeForm(forms.ModelForm):

	class Meta:
		model = Course
		fields = ('course_name', 'description')


class Question:
	type = 0
	label = ''
	answers = []
	cAnswers = []

	def __init__(self, pType, pLabel, pAnswers, cAns):
		self.label = pLabel
		self.answers = pAnswers
		self.cAnswers = cAns
		self.type = pType


def create_quiz(input):

	qtype = []
	questions = []

	with open(input, "r") as file:
		reader = csv.reader(file, delimiter='\t')  # parse by tab
		reader = (line for line in reader if line)  # ignore blank lines
		for questy in reader:
			qtype.append(questy)

		i = 0  # initialize index
		while i < len(qtype):

			if qtype[i][0] == "MC":
				questions.append(
					Question(
							pType=1,
							pLabel=qtype[i][1],
							pAnswers=qtype[i][::2],
							cAns=qtype[i][qtype[i].index("Correct") - 1]))
				questions[i].answers = 	questions[i].answers[1:]

			if qtype[i][0] == "SR":  # Short Answer
				questions.append(Question(pType=2, pLabel=qtype[i][1], pAnswers=qtype[i][2:], cAns=qtype[i][2]))

			if qtype[i][0] == "MA":  # Multiple Select
				cAns = []
				for k in range(len(qtype[i])):
					if qtype[i][k] == "Correct":
						cAns.append(qtype[i][k - 1])
				questions.append(Question(pType=3, pLabel=qtype[i][1], pAnswers=qtype[i][2:], cAns=cAns))

			if qtype[i][0] == "FIB":

				cAns = []
				j = 2
				while j < len(qtype[i]):
					cAns.append((qtype[i][j]))
					j += 1
				questions.append(Question(pType=4, pLabel=qtype[i][1], pAnswers=cAns, cAns=cAns))

			if qtype[i][0] == "TF":  # True or False
				questions.append(Question(pType=5, pLabel=qtype[i][1], pAnswers=qtype[i][2:], cAns=qtype[i][2]))
			if qtype[i][0] == "ESS":  # Esaay Question
				questions.append(Question(pType=6, pLabel=qtype[i][1], pAnswers=qtype[i][2:], cAns=qtype[i][2]))
			i += 1

	return questions


class QuizEditForm(forms.ModelForm):

	file_address = ''

	class Meta:
		model = Quiz
		fields = ()

	def generate_quiz_form(self, input):
		questions = create_quiz(input)

		for x, question in enumerate(questions, start=1):

			self.fields['Question' + str(x) + 'type'] = forms.ChoiceField(
				choices={(1, 'MC'), (2, 'SR'), (3, 'MA'), (4, 'FIB'), (5, 'TF'), (6, 'ESS')},
				initial=question.type,
				label='')

			self.fields['Question' + str(x)] = forms.CharField(
				max_length=1000,
				initial=question.label,
				widget=forms.Textarea(attrs={'rows': 1,
											 'cols': 40,
											 'style': 'height: 5rem;'}))

			for y, answer in enumerate(question.answers, start=1):
				self.fields['Question' + str(x) + 'Answer' + str(y)] = forms.CharField(
					label='Answer ' + str(y),
					max_length=1000,
					initial=answer,
					widget=forms.Textarea(attrs={'rows': 1,
												 'cols': 40,
												 'style': 'height: 2rem;'}))

	def __init__(self, *args, **kwargs):
		super(QuizEditForm, self).__init__(*args, **kwargs)
		self.generate_quiz_form(self.file_address)


class QuizFileForm(forms.ModelForm):

	class Meta:
		model = Quiz
		fields = ('assignment_name', 'open_date', 'due_date', 'file', 'grade_viewable')

	def save(self, commit=True, course=None, prof=None):
		quiz = super(QuizFileForm, self).save(commit=False)

		if commit:
			quiz.prof = prof
			quiz.course_id = course
			quiz.type = 0
			quiz.save()
			course.quizes.add(Quiz.objects.get(id=quiz.id))
			course.save()

		return quiz

	def quiz_url(self):
		quiz = super(QuizFileForm, self).save(commit=False)

		return quiz.file.url

class HomeworkCreationForm(forms.ModelForm):

	class Meta:
		model = Homework
		fields = ('assignment_name', 'open_date', 'due_date', 'file',)
		widgets = {
			'open_date': forms.DateInput(),
		}

