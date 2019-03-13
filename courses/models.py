from django.db import models


class Assignment(models.Model):

	assignment_name = models.CharField(max_length=255, blank=True)
	open_date		= models.DateTimeField(auto_now_add=True, blank=True)
	due_date		= models.DateTimeField(auto_now_add=True, blank=True)
	prof			= models.ForeignKey('accounts.Professor', on_delete=models.CASCADE)
	course_id		= models.ForeignKey('courses.Course', on_delete=models.CASCADE)
	grade			= models.BigIntegerField(blank=True, default=None)

	TYPE_CHOICES = (
		(2, 'homework'),
		(1, 'survey'),
		(0, 'quiz'),
	)

	type 			= models.SmallIntegerField(choices=TYPE_CHOICES, blank=True)

	def __str__(self):
		return self.assignment_name


class Quiz(Assignment):

	grade_viewable = models.BooleanField()
	type = 0

	def __str__(self):
		return self.assignment_name


class Survey(Assignment):
	type = 1
	grade = None

	def __str__(self):
		return self.assignment_name


class Homework(Assignment):
	type = 2
	link = models.CharField(max_length=255, blank=True)

	def __str__(self):
		return self.assignment_name
# Create your models here.


class Course(models.Model):

	course_name 	= models.CharField(max_length=255, unique=True)
	quizes			= models.ManyToManyField(Quiz)
	surveys 		= models.ManyToManyField(Survey)
	homeworks		= models.ManyToManyField(Homework)

	def __str__(self):
		return self.course_name

