from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from newsleters.views import newsleter_email_list

urlpatterns = [
    # core
    path('admin/', admin.site.urls),

    # 3rd parties
    path('accounts/', include('allauth.urls')),  # allauth
    path('hitcount/', include(('hitcount.urls', 'hitcount'),
                              namespace='hitcount')),  # hitcount
    path('summernote/', include('django_summernote.urls')),  # sumernote

    # local
    path('', include('pages.urls')),
    path('blog/', include('posts.urls')),
    path('blog/', include('comments.urls')),
    path('profile/', include('profiles.urls')),
    path("binblogger-admin/", include('admin_dashboard.urls')),
    path("mydashboard/", include("user_dashboard.urls")),
    path("newsleter/subscribe/", newsleter_email_list, name="newsleter_subscribe"),

]

if settings.DEBUG:
    urlpatterns = urlpatterns + \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
