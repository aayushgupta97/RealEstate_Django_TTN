from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('properties/', include('properties.urls')),
    path('', include('pages.urls')),
    path('admin/', admin.site.urls),
]
