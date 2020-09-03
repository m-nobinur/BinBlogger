from django.urls import path

from comments.views import (add_comment,
                            reply_comment,
                            delete_comment,
                            delete_reply)

urlpatterns = [
    path("post/<int:pk>/comment/add", add_comment, name="add_comment"),
    path("post/<int:ppk>/comments/<int:cpk>/reply",
         reply_comment, name="reply_comment"),
    path("post/<int:ppk>/comments/<int:cpk>/delete",
         delete_comment, name="delete_comment"),
    path("post/<int:ppk>/comments/<int:cpk>/replies/<int:rpk>/delete",
         delete_reply, name="delete_reply"),
]
