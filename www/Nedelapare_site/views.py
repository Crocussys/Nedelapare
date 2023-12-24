from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader


def index(request):
    return redirect('signin')


def sign_in(request):
    return render(request, 'signin.html')


def registration(request):
    return render(request, 'registration.html')


def waiting(request):
    return HttpResponse(loader.get_template("waiting.html").render({"email": request.GET.get("email", "")}, request))


def done_reg(request):
    return render(request, 'donereg.html')


def schedule(request):
    return render(request, 'schedule.html')


def add(request):
    return render(request, 'add.html')
