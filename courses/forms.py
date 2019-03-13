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


"""class QuizCreationForm(forms.ModelForm):

	file 		= forms.FileInput()
	
	class Meta:
		model = Quiz
		fields = ('assignment_name', )

	def create_quiz(self, file):
		pass
"""
