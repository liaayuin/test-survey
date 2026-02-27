from django.urls import path
from . import views, api_views

urlpatterns = [
    path("", views.dashboard_view, name="dashboard"),

    path("api/demographics/", api_views.api_demographics),
    path("api/age-dist/", api_views.api_age_dist),
    path("api/subcity/", api_views.api_subcity),
    path("api/awareness/", api_views.api_awareness),
    path("api/participation/", api_views.api_participation),
    path("api/training/", api_views.api_training),
]