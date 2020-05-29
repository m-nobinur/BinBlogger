from django.urls import path

from comments.views import add_comment, reply_comment, delete_comment, delete_reply
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
    path("post/<int:pk>/comment/add", add_comment, name="add_comment"),
    path("post/<int:ppk>/comments/<int:cpk>/reply", reply_comment, name="reply_comment"),
    path("post/<int:ppk>/comments/<int:cpk>/delete", delete_comment, name="delete_comment"),
    path("post/<int:ppk>/comments/<int:cpk>/replies/<int:rpk>/delete", delete_reply, name="delete_reply"),
]
