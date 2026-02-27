from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from analytics.services import (
    age_distribution_stats,
    demographic_summary,
    awareness_stats,
    participation_insights,
    subcity_stats,
    training_preferences
)


def is_analytics_admin(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(is_analytics_admin)
def api_demographics(request):
    return JsonResponse(demographic_summary())


@user_passes_test(is_analytics_admin)
def api_awareness(request):
    return JsonResponse(awareness_stats())


@user_passes_test(is_analytics_admin)
def api_participation(request):
    return JsonResponse(participation_insights())


@user_passes_test(is_analytics_admin)
def api_training(request):
    return JsonResponse(training_preferences())
def api_age_dist(request):
    return JsonResponse({"results": age_distribution_stats()})

def api_subcity(request):
    return JsonResponse({"results": subcity_stats()})