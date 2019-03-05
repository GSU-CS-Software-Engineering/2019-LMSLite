from django.db import models


class Assignment(models.Model):
	pass


class Course(models.Model):

	course_name = models.CharField(max_length=255, unique=True)
	prof = models.OneToOneField('accounts.Professor', on_delete=models.CASCADE)
	students = models.ManyToManyField('accounts.Student')

	def __str__(self):
		return self.course_name



# Create your models here.
