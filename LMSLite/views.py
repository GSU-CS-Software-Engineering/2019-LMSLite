from django.shortcuts import render
from django.http import HttpResponseRedirect


def index(request):

    return render(request, 'index.html')


def profile_view(request):

    if request.user.is_authenticated:
        return render(request, 'profile.html')
    else:
        return HttpResponseRedirect("/auth/login")

