from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test


def is_analytics_admin(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(is_analytics_admin)
def dashboard_view(request):
    return render(request, "analytics/dashboard.html")