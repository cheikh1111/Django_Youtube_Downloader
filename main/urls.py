from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home),
    path("home", views.home),
    path("about", views.about),
    path("contact", views.contact),
    path("video-info", views.video_info),
    path("download-video", views.download_video),
    path("download-audio", views.download_audio),
    path("error/<int:status_code>", views.custom_exception_handler),
]

# Handle errors
