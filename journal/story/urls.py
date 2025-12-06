from . import views
from django.urls import path, include
from rest_framework import routers

urlpatterns = [
    path("", views.home, name='home'),
    path("api/journey/restore", views.restore_db, name='restore_db'),
    path("api/journey/get_story", views.JournalViewSet.as_view(), name="api")
]