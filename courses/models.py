from django.db import models


def quiz_upload_address(instance, filename):
	name, ext = filename.split('.')
	filename = instance.assignment_name
	file_path = '{account_id}/Quizzes/{Assignment}/{filename}.{ext}'.format(
		account_id=instance.course_id.course_name, Assignment=instance.assignment_name, filename=filename+'_key', ext=ext)
	return file_path


def survey_upload_address(instance, filename):
	name, ext = filename.split('.')
	filename = instance.assignment_name
	file_path = '{account_id}/Surveys/{Assignment}/{filename}.{ext}'.format(
		account_id=instance.course_id.course_name, Assignment=instance.assignment_name, filename=filename + '_key', ext=ext)
	return file_path


def homework_upload_address(instance, filename):
	name, ext = filename.split('.')
	filename = instance.assignment_name
	file_path = '{account_id}/Homework/{Assignment}/{filename}.{ext}'.format(
		account_id=instance.course_id.course_name, Assignment=instance.assignment_name, filename=filename + '_key', ext=ext)
	return file_path


def response_upload_address(instance, filename):
	name, ext = filename.split('.')
	filename = instance.assignment.assignment_name
	file_path = '{account_id}/Responses/{filename}.{ext}'.format(
		account_id=instance.assignment.course_id.course_name, filename=filename + '_' + instance.stdnt.email.split('@')[0], ext=ext)
	return file_path


class Assignment(models.Model):

	assignment_name	= models.CharField(max_length=255, blank=True)
	open_date		= models.DateTimeField(blank=True)
	due_date		= models.DateTimeField(blank=True)
	prof			= models.ForeignKey('accounts.Professor', on_delete=models.CASCADE)
	course_id		= models.ForeignKey('courses.Course', on_delete=models.CASCADE)

	TYPE_CHOICES = (
		(2, 'homework'),
		(1, 'survey'),
		(0, 'quiz'),
	)

	type 			= models.SmallIntegerField(choices=TYPE_CHOICES, blank=True)

	def __str__(self):
		return self.assignment_name


class Quiz(Assignment):

	average = models.FloatField(blank=True,default=0, null=True)
	grade_viewable = models.BooleanField()
	file = models.FileField(upload_to=quiz_upload_address, blank=True)

	def __str__(self):
		return self.assignment_name


class Survey(Assignment):
	file = models.FileField(upload_to=survey_upload_address, blank=True)

	def __str__(self):
		return self.assignment_name


class Homework(Assignment):
	file = models.FileField(upload_to=homework_upload_address, blank=True)

	def __str__(self):
		return self.assignment_name


class Grade(models.Model):
	assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, blank=True, default=None)
	grade_value = models.FloatField(blank=True, default=None)
	stdnt = models.ForeignKey('accounts.Student', on_delete=models.CASCADE, blank=True, default=None)
	file = models.FileField(blank=True, default=None)


class Course(models.Model):

	prof			= models.ForeignKey('accounts.Professor', on_delete=models.CASCADE, blank=True, default=None)
	students		= models.ManyToManyField('accounts.Student')
	course_name 	= models.CharField(max_length=255, unique=True)
	description		= models.TextField(blank=True)
	quizes			= models.ManyToManyField(Quiz)
	surveys 		= models.ManyToManyField(Survey)
	homeworks		= models.ManyToManyField(Homework)

	def __str__(self):
		return self.course_name

