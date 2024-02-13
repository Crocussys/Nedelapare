from django.shortcuts import render, redirect


def index(request):
    return redirect('signin')


def sign_in(request):
    return render(request, 'signin.html')


def registration(request):
    return render(request, 'registration.html')


def waiting(request):
    return render(request, 'waiting.html', {"email": request.GET.get("email", "")})


def done_reg(request):
    return render(request, 'donereg.html')


def schedule(request):
    menu = 1
    context = {
        "menu": menu,
        "background_top_height": menu * 60,
        "background_bottom_top": (menu + 1) * 60
    }
    return render(request, 'schedule.html', context)


def add(request):
    return render(request, 'add.html')


def profile(request):
    menu = 0
    context = {
        "menu": menu,
        "background_top_height": menu * 60,
        "background_bottom_top": (menu + 1) * 60
    }
    return render(request, 'profile.html', context)


def group(request):
    menu = 2
    context = {
        "menu": menu,
        "background_top_height": menu * 60,
        "background_bottom_top": (menu + 1) * 60
    }
    return render(request, 'group.html', context)


def group_change(request):
    return render(request, 'group_change.html')


def test(request):
    return render(request, 'test.html')
