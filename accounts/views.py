from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from accounts.forms import ProfessorChangeForm


def profile_view(request):
	context_dict = {}

	if request.user.is_authenticated:

		form = ProfessorChangeForm(request.POST, request.FILES, instance=request.user)
		context_dict['form'] = form

		if request.method == 'POST':

			form.save()
			return redirect('index')

		return render(request, 'profile.html', context_dict)

	return HttpResponseRedirect("/auth/login")

