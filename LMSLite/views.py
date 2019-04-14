from django.http import HttpResponse
from django.shortcuts import render
from django.utils.encoding import smart_str

from courses.models import Homework


def index(request):

    return render(request, 'index.html')


def download(request, id):
    response = HttpResponse(content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(Homework.objects.get(id=id))

    return response
