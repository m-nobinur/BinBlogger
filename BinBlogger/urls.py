from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


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

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
        
    ]+ urlpatterns + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
