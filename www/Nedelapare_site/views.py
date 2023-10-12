from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def sign_in(request):
    return render(request, 'signin.html')

def registration(request):
    return render(request, 'registration.html')

def schedule(request):
    return render(request, 'schedule.html')