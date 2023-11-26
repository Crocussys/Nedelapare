from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from knox.auth import TokenAuthentication
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework.permissions import IsAuthenticated


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


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def schedule(request):
    return render(request, 'schedule.html')
