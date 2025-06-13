from django.contrib import admin
from django.urls import path, include  # Include app URLs

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('predictor.urls')),  # Include URLs from the predictor app
]

# Serve media files during development
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)