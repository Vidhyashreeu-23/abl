from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from campusconnect.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('clubs/', include('clubs.urls')),
    path('events/', include('events.urls')),
    path('posts/', include('posts.urls')),
    path('reviews/', include('reviews.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
