from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from courses.models import Course

from .forms import CourseAdminCreationForm, CourseAdminChangeForm


class CourseAdmin(UserAdmin):

	form = CourseAdminCreationForm
	add_form = CourseAdminChangeForm

	list_display = ('course_name', )
	list_filter = ('prof',)

	fieldsets = (
		(None, {'fields': ('course_name', )}),
	)

	add_fieldsets = (
		(None, {'fields': ('course_name', )}),
	)

	search_fields = ('course_name',)
	ordering = ('course_name',)
	filter_horizontal = ()


admin.site.register(Course)

