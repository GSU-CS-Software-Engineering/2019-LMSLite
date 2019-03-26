from django.http import HttpResponseRedirect
from django.shortcuts import render

from accounts.forms import ProfessorChangeForm


def profile_view(request):
	context_dict = {}

	if request.user.is_authenticated:
		form = ProfessorChangeForm()
		context_dict['form'] = form
		return render(request, 'profile.html', context_dict)
	else:
		return HttpResponseRedirect("/auth/login")

