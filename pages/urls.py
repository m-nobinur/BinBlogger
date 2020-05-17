from django.urls import path,include

from .views import (
                    HomePageView,
                    AboutView, 
                    ContactView, 
                    SearchView,
                    )

urlpatterns = [

    path('', HomePageView.as_view(), name="home"),
    path("search/", SearchView.as_view(), name="search"),
    path("about/", AboutView.as_view(), name="about"),
    path("contact/", ContactView.as_view(), name="contact"),
]
