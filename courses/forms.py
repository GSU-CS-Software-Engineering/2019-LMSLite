from django import forms
from .models import Course


class CourseAdminCreationForm(forms.ModelForm):

	class Meta:
		model = Course
		fields = ('course_name', 'prof', 'students')

	def save(self, commit=True):
		# Save the provided password in hashed format
		course = super(CourseAdminCreationForm, self).save(commit=False)

		if commit:
			course.save()
		return course


class CourseAdminChangeForm(forms.ModelForm):

	class Meta:
		model = Course
		fields = ('course_name', 'prof', 'students')
