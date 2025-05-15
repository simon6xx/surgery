from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('surgery/auth/', include('apps.authentication.urls')),
    path('surgery/schedule/', include('apps.schedule.urls')),
]
