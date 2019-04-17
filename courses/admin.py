from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from courses.models import Course, Assignment, Grade

from .forms import CourseAdminCreationForm, CourseAdminChangeForm


class CourseAdmin(admin.ModelAdmin):

	form = CourseAdminCreationForm
	add_form = CourseAdminChangeForm

	list_display = ('course_name', )
	list_filter = ('course_name',)

	fieldsets = (
		(None, {'fields': ('prof', 'course_name', 'description', 'students')}),
	)

	add_fieldsets = (
		(None, {'fields': ('prof', 'course_name', 'description', 'students')}),
	)

	search_fields = ('course_name',)
	ordering = ('course_name',)
	filter_horizontal = ()

admin.site.register(Assignment)
admin.site.register(Grade)
admin.site.register(Course, CourseAdmin)

