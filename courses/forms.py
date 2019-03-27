import csv

from django import forms
from django.core.files.storage import DefaultStorage

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
	_type = ''
	label = ''
	answers = []
	cAnswers = []

	def __init__(self, pType, pLabel, pAnswers, cAns):
		self.label = pLabel
		self.answers = pAnswers
		self.cAnswers = cAns
		self._type = pType


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
				print(qtype[i][qtype[i].index("Correct") - 1])#
				questions.append(
					Question(
							_type='MC',
							pLabel=qtype[i][1],
							pAnswers=qtype[i][2:],
							cAns=qtype[i][qtype[i].index("Correct") - 1]))

			if qtype[i][0] == "SR":  # Short Answer
				print(qtype[i][2])  # The answer for SR will always be in third index
				questions.append(Question(_type='SR', pLabel=qtype[i][1], pAnswers=qtype[i][2], cAns=qtype[i][2]))

			if qtype[i][0] == "MA":  # Multiple Select
				cAns = []
				for k in range(len(qtype[i])):
					if qtype[i][k] == "Correct":
						print(qtype[i][k - 1])  # Print all correct answers
						cAns.append(qtype[i][k - 1])
				questions.append(Question(_type='MA', pLabel=qtype[i][1], pAnswers=[i][2:], cAns=cAns))

			if qtype[i][0] == "FIB":
				cAns = []
				j = 2
				while j < len(qtype[i]):
					print(qtype[i][j]) # Print all answer options
					cAns.append((qtype[i][j]))
					j += 1
				questions.append(Question(_type='FIB', pLabel=qtype[i][1], pAnswers=cAns, cAns=cAns))

			if qtype[i][0] == "TF":  # True or False
				print(qtype[i][2])
				questions.append(Question(_type='TF', pLabel=qtype[i][1], pAnswers=qtype[i][2],cAns=qtype[i][2]))
			if qtype[i][0] == "ESS":  # Esaay Question
				print(qtype[i][2])  # Place holder Text
				questions.append(Question(_type='ESS', pLabel=qtype[i][1], pAnswers=qtype[i][2],cAns=qtype[i][2]))
				i += 1

	return questions


class QuizCreationForm(forms.ModelForm):

	File = forms.FileField(label='Upload')

	class Meta:
		model = Quiz
		fields = ('assignment_name', )


class HomeworkCreationForm(forms.ModelForm):

	class Meta:
		model = Homework
		fields = ('assignment_name', 'file',)

