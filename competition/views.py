
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
    settings_obj = CompetitionSettings.objects.order_by("pk").first()

    published = bool(
        settings_obj and settings_obj.phase1_results_published
    )

    ranked_teams = []

    if published:
        teams = (
            Team.objects.filter(
                review_status=Team.ReviewStatus.QUALIFIED,
                phase1_rank__isnull=False,
                phase1_score__isnull=False,
            )
            .select_related("abstract")
            .order_by("phase1_rank", "-phase1_score", "team_name")
        )

        for team in teams:
            try:
                research_title = team.abstract.research_title
            except AbstractSubmission.DoesNotExist:
                research_title = "—"

            ranked_teams.append({
                "rank": team.phase1_rank,
                "team": team,
                "research_title": research_title,
            })

    return render(
        request,
        "competition/finalists.html",
        {
            "results_published": published,
            "ranked_teams": ranked_teams,
            "selected_count": len(ranked_teams),
        },
    )
