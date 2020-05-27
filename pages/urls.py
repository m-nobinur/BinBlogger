from django.urls import path,include

from .views import (
                    HomePageView,
                    AboutView, 
                    ContactView, 
                    SearchView,
                    UserDashboard,
                    DeletePostbyAuthor,
                    user_dashboard_filter_category_posts_view,
                    user_dashboard_filter_tag_posts_view,
                    )

urlpatterns = [

    path('', HomePageView.as_view(), name="home"),
    path("search/", SearchView.as_view(), name="search"),
    path("mydashboard/", UserDashboard.as_view(), name="user_dashboard"),
    path("mydashboard/posts/<int:pk>/delete/confirm", DeletePostbyAuthor.as_view(), name="delete_by_author"),
    path("mydashboard/categories/<int:pk>/posts", user_dashboard_filter_category_posts_view, name="ud_category_posts"),
    path("mydashboard/tags/<str:tag>/posts", user_dashboard_filter_tag_posts_view, name="ud_tag_posts"),
    path("about/", AboutView.as_view(), name="about"),
    path("contact/", ContactView.as_view(), name="contact"),
]
