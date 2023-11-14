from django.shortcuts import render, redirect


def index(request):
    return redirect('signin')

def sign_in(request):
    return render(request, 'signin.html')

def registration(request):
    return render(request, 'registration.html')

def schedule(request):
    if request.user.is_authenticated:  # Не работает!!!!!
        return render(request, 'schedule.html')
    else:
        return redirect('signin')
