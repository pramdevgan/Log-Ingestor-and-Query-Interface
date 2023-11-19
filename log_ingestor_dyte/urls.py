from django.contrib import admin
from django.urls import path, include
from log_ingestor_app.views import filter_logs

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('log_ingestor_app.urls')),
    path('', filter_logs),
]
