from django.urls import path

from .views import (BlogPageView, 
                    PostCreateView,
                    PostUpdateView,
                    PostDeleteView,
                    PostDetailView, 
                    Posts_in_CategoryView,
                    TagPostsView,
                    UserPostsView,
                    AddCategoryView,
                    )

urlpatterns = [
    path("", BlogPageView.as_view(), name="blog"),
    path("post/add_new/", PostCreateView.as_view(), name="add_post"),
    path("post/<int:pk>/update", PostUpdateView.as_view(), name="update_post"),
    path("post/<int:pk>/delete", PostDeleteView.as_view(), name="delete_post"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("category/<int:id>/posts", Posts_in_CategoryView, name="posts_in_category"),
    path("tags/<str:tag>/posts", TagPostsView, name="tag_posts"),
    path("<str:username>/posts", UserPostsView , name="user_posts"),
    path("category/add", AddCategoryView.as_view() , name="add_category"),

]
