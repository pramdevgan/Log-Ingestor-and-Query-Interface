from django.urls import path
from .views import LogDataView, SearchLogView

urlpatterns = [
    path('logdata/', LogDataView.as_view(), name='logdata'),
    path("query_search", SearchLogView.as_view(), name='search_log')
]