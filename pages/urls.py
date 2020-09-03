from django.urls import path

from .views import (
    HomePageView,
    BlogPageView,
    AuthorPageView,
    ContactView,
    SearchView,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("blog/", BlogPageView.as_view(), name="blog"),
    path("authors/", AuthorPageView.as_view(), name="authors"),
    path("search/", SearchView.as_view(), name="search"),
    path("contact/", ContactView.as_view(), name="contact"),
]
