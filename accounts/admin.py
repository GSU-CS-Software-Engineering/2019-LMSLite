from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from .forms import StudentAdminCreationForm, StudentAdminChangeForm, ProfessorAdminChangeForm, ProfessorAdminCreationForm
from .models import User, Student, Professor


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = None
    add_form = None

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'admin')
    list_filter = ('admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'courses')}),
        ('Permissions', {'fields': ('active',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


class StudentAdmin(UserAdmin):
    form = StudentAdminChangeForm
    add_form = StudentAdminCreationForm


class ProfAdmin(UserAdmin):
    form = ProfessorAdminChangeForm
    add_form = ProfessorAdminCreationForm


admin.site.register(Student, StudentAdmin)
admin.site.register(Professor, ProfAdmin)
admin.site.unregister(Group)
# Register your models here.
