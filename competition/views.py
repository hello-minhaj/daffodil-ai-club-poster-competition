
from django.shortcuts import render

from .models import AbstractSubmission, CompetitionSettings, Team


def home(request):
    return render(request, "competition/home.html")


def rules(request):
    return render(request, "competition/rules.html")


def prizes(request):
    return render(request, "competition/prizes.html")


def developer(request):
    return render(request, "competition/developer.html")



def finalists(request):
    return render(
        request,
        "competition/finalists.html",
        {
            "results_published": False,
            "ranked_teams": [],
            "selected_count": 0,
        },
    )
