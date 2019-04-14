from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from courses.models import Course, Assignment

from .forms import CourseAdminCreationForm, CourseAdminChangeForm


class CourseAdmin(UserAdmin):

	form = CourseAdminCreationForm
	add_form = CourseAdminChangeForm

	list_display = ('course_name', )
	list_filter = ('course_name',)

	fieldsets = (
		(None, {'fields': ('course_name', 'description')}),
	)

	add_fieldsets = (
		(None, {'fields': ('course_name', 'description')}),
	)

	search_fields = ('course_name',)
	ordering = ('course_name',)
	filter_horizontal = ()

admin.site.register(Assignment)
admin.site.register(Course, CourseAdmin)

