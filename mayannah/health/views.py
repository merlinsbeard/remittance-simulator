from django.http import HttpResponse


def staging(request):
    return HttpResponse(status=200)


def production(request):
    return HttpResponse(status=500)
