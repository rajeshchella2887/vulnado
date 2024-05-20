from django.urls import path

from . import views

app_name = "landing"

urlpatterns = [
    path("", views.LandingIndexView.as_view(), name="index"),
]
