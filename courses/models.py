from django.db import models

"""
class Assignment(models.Model):

	assignment_name = models.CharField(max_length=255, blank=True)
	open_date = models.DateTimeField(auto_now_add=True, blank=True)
	due_date = models.DateTimeField(auto_now_add=True, blank=True)

	grade = models.BigIntegerField(blank=True, default=None)

	def __str__(self):
		return self.assignment_name
"""

class Course(models.Model):

	course_name = models.CharField(max_length=255, unique=True)

	def __str__(self):
		return self.course_name


# Create your models here.
