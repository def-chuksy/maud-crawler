from django.urls import path
from .views import index, crawl

urlpatterns = [
    path("", index, name="index"),
    path("crawl/", crawl, name="crawl")
]