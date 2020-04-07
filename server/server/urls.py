from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('qsets/', include('qsets.urls')),
    path('', include('qsets.urls')),
    path('admin/', admin.site.urls),
]
