from django.urls import path

from .views import Profile_Update

urlpatterns = [
    path("update/", Profile_Update, name="profile_update")
]
 