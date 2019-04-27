import csv

from django import forms

from LMSLite.helpers import create_quiz
from .models import Course, Quiz, Homework, Grade, Survey


class CourseAdminCreationForm(forms.ModelForm):

	class Meta:
		model = Course
		fields = ('course_name', 'description')

	def save(self, commit=True):
		# Save the provided password in hashed format
		course = super(CourseAdminCreationForm, self).save(commit=False)

		for student in course.students.all():
			student.courses.add(course)

		course.prof.courses.add(course)

		if commit:
			course.save()
		return course


class CourseAdminChangeForm(forms.ModelForm):

	class Meta:
		model = Course
		fields = ('course_name', 'description')


class SurveyEditForm(forms.ModelForm):

	file_address = ''

	class Meta:
		model = Survey
		fields = ()

	def generate_survey_form(self, input):
		questions = create_quiz(input)

		for x, question in enumerate(questions, start=1):

			self.fields['Question' + str(x) + 'type'] = forms.ChoiceField(
				choices={(1, 'MC'), (2, 'SR'), (3, 'MA'), (4, 'FIB'), (5, 'TF'), (6, 'ESS')},
				initial=question.type,
				label='')

			self.fields['Question ' + str(x)] = forms.CharField(
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
		super(SurveyEditForm, self).__init__(*args, **kwargs)
		self.generate_survey_form(self.file_address)


class SurveyFileForm(forms.ModelForm):

	class Meta:
		model = Survey
		fields = ('assignment_name', 'open_date', 'due_date', 'file')
		widgets = {
			'open_date': forms.TextInput(attrs={'autocomplete': 'off'}),
			'due_date': forms.TextInput(attrs={'autocomplete': 'off'}),
			'assignment_name': forms.TextInput(attrs={'autocomplete': 'off'}),
		}

	def save(self, commit=True, course=None, prof=None):
		survey = super(SurveyFileForm, self).save(commit=False)

		if commit:
			survey.prof = prof
			survey.course_id = course
			survey.type = 0
			survey.save()
			course.surveys.add(Survey.objects.get(id=survey.id))
			course.save()

		return survey


class QuizEditForm(forms.Form):

	file_address = ''


	def generate_quiz_form(self, input):
		questions = create_quiz(input)

		for x, question in enumerate(questions, start=1):

			self.fields['Question' + str(x) + 'type'] = forms.ChoiceField(
				choices={(1, 'MC'), (2, 'SR'), (3, 'MA'), (4, 'FIB'), (5, 'TF'), (6, 'ESS')},
				initial=question.type,
				label='')

			self.fields['Question ' + str(x)] = forms.CharField(
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
		widgets = {
			'open_date': forms.TextInput(attrs={'autocomplete': 'off'}),
			'due_date': forms.TextInput(attrs={'autocomplete': 'off'}),
			'assignment_name': forms.TextInput(attrs={'autocomplete': 'off'}),
		}

	def save(self, commit=True, course=None, prof=None):
		quiz = super(QuizFileForm, self).save(commit=False)

		if commit:
			quiz.prof = prof
			quiz.course_id = course
			quiz.type = 0
			quiz.save()
			course.quizes.add(Quiz.objects.get(id=quiz.id))

			for student in course.students.all():
				student.quizes.add(Quiz.objects.get(id=quiz.id))
				student.save()

			course.save()

		return quiz


class HomeworkCreationForm(forms.ModelForm):

	class Meta:
		model = Homework
		fields = ('assignment_name', 'open_date', 'due_date', 'file',)


	def save(self, commit=True, course=None, prof=None):
		homework = super(HomeworkCreationForm, self).save(commit=False)

		if commit:
			homework.prof = prof
			homework.course_id = course
			homework.type = 2
			homework.save()
			course.homeworks.add(Homework.objects.get(id=homework.id))
			course.save()

		return homework


class GradeEditForm(forms.ModelForm):

	class Meta:
		model = Grade
		fields = ('grade_value', )
