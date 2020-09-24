from django.http import HttpResponse


def simple_crop(request, width, height, url):
    return HttpResponse('Hello World!')
