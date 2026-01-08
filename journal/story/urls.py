from . import views
from django.urls import path, include

urlpatterns = [
    path("", views.home, name='home'),
    path("api/journey/restore", views.restore_db, name='restore_db'),
    path("api/journey/get_story", views.JournalViewSet, name="api")
]
