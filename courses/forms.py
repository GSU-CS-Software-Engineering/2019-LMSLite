import csv

from django import forms
from .models import Course, Quiz
from accounts.models import Professor


class CourseAdminCreationForm(forms.ModelForm):

	class Meta:
		model = Course
		fields = ('course_name', )

	def save(self, commit=True):
		# Save the provided password in hashed format
		course = super(CourseAdminCreationForm, self).save(commit=False)
		prof = Professor.objects.get(self.prof.id)
		prof.courses.add(course)

		if commit:
			course.save()
			prof.save()
		return course


class CourseAdminChangeForm(forms.ModelForm):

	class Meta:
		model = Course
		fields = ('course_name', )


class QuizCreationForm(forms.ModelForm):

	file 		= forms.FileInput()
	
	class Meta:
		model = Quiz
		fields = ('assignment_name', )

	def create_quiz(self, file):

		qtype = []

		with open("Sample_Quiz.txt", "r") as file:
			reader = csv.reader(file, delimiter='\t')  # parse by tab
			reader = (line for line in reader if line)  # ignore blank lines
			for questy in reader:
				qtype.append(questy)

			i = 0  # initialize index
			while i < len(qtype):
				if qtype[i][0] == "MC":
					print(qtype[i][qtype[i].index("Correct") - 1])  #
				if qtype[i][0] == "SR":  # Short Answer
					print(qtype[i][2])  # The answer for SR will always be in third index
				if qtype[i][0] == "MA":  # Multiple Select
					for k in range(len(qtype[i])):
						if qtype[i][k] == "Correct":
							print(qtype[i][k - 1])  # Print all correct answers
				if qtype[i][0] == "FIB":
					j = 2
					while j < len(qtype[i]):
						print(qtype[i][j])  # Print all answer options
						j += 1
				if qtype[i][0] == "TF":  # True or False
					print(qtype[i][2])
				if qtype[i][0] == "ESS":  # Esaay Question
					print(qtype[i][2])  # Place holder Text

				i += 1

