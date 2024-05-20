from django.urls import path

from . import views

app_name = "providers"

urlpatterns = [
    path("add/", views.AddProviderView.as_view(), name="add-provider"),
    path("update/<int:pk>/", views.UpdateProviderView.as_view(), name="update-provider"),
    path("delete/<int:pk>/", views.DeleteProviderView.as_view(), name="delete-provider"),
]
