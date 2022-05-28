from django.http import HttpResponse
from django.shortcuts import render


def hello(request):
    return HttpResponse("Hello world ! ")


def run(request):
    context = {'name': 'Hello world!'}
    return render(request, 'main.html', context)
