from django.urls import path
from . import views

urlpatterns = [
    path("", views.WeekView.as_view(), name="week"),
    path("add/", views.ActivityCreate.as_view(), name="activity-add"),
    path("<int:pk>/edit/", views.ActivityUpdate.as_view(), name="activity-edit"),
    path("<int:pk>/delete/", views.ActivityDelete.as_view(), name="activity-delete"),
    path("api/activities/", views.activities_json, name="api-activities"),
]
