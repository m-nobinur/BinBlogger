from django.urls import path

from .views import (
    UserDashboard,
    DeletePostbyAuthor,
    user_dashboard_filter_category_posts_view,
    user_dashboard_filter_tag_posts_view,
)

urlpatterns = [
    path("", UserDashboard.as_view(), name="user_dashboard"),
    path("posts/<int:pk>/delete/confirm",
         DeletePostbyAuthor.as_view(), name="delete_by_author"),
    path("categories/<int:pk>/posts",
         user_dashboard_filter_category_posts_view, name="ud_category_posts"),
    path("tags/<str:tag>/posts",
         user_dashboard_filter_tag_posts_view, name="ud_tag_posts"),
]
