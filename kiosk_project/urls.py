from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #path('admin/', admin.site.urls),  # Default Django admin panel
    path('app1/', include('app1.urls')),  # Include URLs from app1
    path('api/', include('app1.apiurls')),  # Include your API routes
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])