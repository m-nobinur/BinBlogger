from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from newsleters.views import newsleter_email_list
urlpatterns = [
       
    path('admin/', admin.site.urls),

    # allauth
    path('accounts/', include('allauth.urls')),

    # hitcount
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
    
    path('summernote/', include('django_summernote.urls')),

    # local
    path('', include('pages.urls')),
    path('blog/', include('posts.urls')),
    path('profile/', include('profiles.urls')),
    path("binblogger-admin/", include('admin_dashboard.urls')),
    path("newsleter/subscribe/", newsleter_email_list, name="newsleter_subscribe")

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
        
    ]+ urlpatterns + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
