from django.shortcuts import render


def home(request):
    return render(request, "competition/home.html")


def rules(request):
    return render(request, "competition/rules.html")


def prizes(request):
    return render(request, "competition/prizes.html")


def developer(request):
    return render(request, "competition/developer.html")
