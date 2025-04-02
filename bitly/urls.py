
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('link/create', include('core.urls')),
    path('social/', include('social_auth.urls')),
]
