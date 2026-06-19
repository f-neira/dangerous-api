from django.urls import path

from .views import show_list

urlpatterns = [
    path("shows/", show_list, name="show-list"),
]
