"""
Django Log Ingestor

This module provides Django views and a model for handling log data. The system allows log data ingestion,
search, and filtering functionalities.

Models:
    - LogData: Represents log entries with various fields.

Views:
    - LogDataView: Handles the creation of log entries through a POST request.
    - SearchLogView: Handles log data retrieval based on specified search parameters.
    - filter_logs: Renders a search form for filtering log entries based on various parameters.

Important Notes:
    - CSRF Exemption: The SearchLogView and filter_logs are marked with @csrf_exempt for exemption from CSRF protection.
    - Date Handling: Date parameters (start_date and end_date) are parsed and used to filter log entries based on the timestamp field.
    - Regex Search: The regex_search parameter enables regex search on the log message field.

Example Usage:
    1. Creating Log Entry: Send a POST request to the endpoint associated with LogDataView with log data in the request payload.
    2. Searching Logs: Send a GET request to the endpoint associated with SearchLogView with query parameters for filtering.
    3. Filtering Logs: Access the filter_logs view through a GET request, providing filter parameters in the URL.
"""

from django.http import HttpResponseBadRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LogDataSerializer
from django.db.models import Q
from django.utils.dateparse import parse_datetime
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import LogData
from django.utils import timezone
from datetime import timedelta


class LogDataView(APIView):
    """
    LogDataView Class

    Handles the creation of log entries through a POST request.
    Expects log data in the request payload.
    Responds with a serialized log entry and HTTP status 201 if successful.
    Returns HTTP status 400 with error details if the data is invalid.
    """

    def post(self, request, *args, **kwargs):
        serializer = LogDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchLogView(APIView):
    """
    SearchLogView Class

    Handles GET requests for log data retrieval.
    Supports various query parameters for filtering log entries.
    Performs case-insensitive substring matching for most fields.
    Supports date range filtering and regex search.
    Responds with serialized log entries that match the specified criteria.
    """

    @csrf_exempt
    def get(self, request, *args, **kwargs):
        regex_search = request.GET.get('regex_search', '')

        # Extracting query parameters
        level = request.GET.get('level', '')
        message = request.GET.get('message', '')
        resourceId = request.GET.get('resource_id', '')
        timestamp = request.GET.get('timestamp', '')
        traceId = request.GET.get('traceId', '')
        spanId = request.GET.get('spanId', '')
        commit = request.GET.get('commit', '')
        parent_resourceId = request.GET.get('metadata.parentResourceId', '')

        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')

        # Convert start_date and end_date to datetime objects
        start_date = parse_datetime(start_date) if start_date else None
        end_date = parse_datetime(end_date) if end_date else None

        # Building the query
        query = Q(level__icontains=level) & Q(message__icontains=message) & \
                Q(resourceId__icontains=resourceId) & Q(traceId__icontains=traceId) & \
                Q(spanId__icontains=spanId) & Q(commit__icontains=commit) & \
                Q(metadata__parentResourceId__icontains=parent_resourceId)

        # Adding date range filter
        if start_date and end_date:
            query &= Q(timestamp__range=(start_date, end_date))

        # Adding regex search
        if regex_search:
            query &= Q(message__iregex=regex_search)

        log_entries = LogData.objects.filter(query)
        serializer = LogDataSerializer(log_entries, many=True)

        return Response(serializer.data)


@csrf_exempt
def filter_logs(request):
    """
    filter_logs Function

    Renders a search form for filtering log entries based on various parameters.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered search form with filtered log entries.
    """
    form_fields = {
        'regex_search': 'Regex Search',
        'level': 'Level contains...',
        'message': 'Message contains...',
        'resourceId': 'Resource Id contains...',
        'timestamp': 'Timestamp contains...',
        'start_date': 'Start Date',
        'end_date': 'End Date',
        'traceId': 'Trace Id contains...',
        'spanId': 'Span Id contains...',
        'commit': 'Commit contains...',
        'metadata': 'Metadata contains...',
    }

    qs = LogData.objects.all()

    filters = {}

    regex_search = request.GET.get('regex_search', '')
    if regex_search:
        filters['message__iregex'] = regex_search

    level = request.GET.get('level', '')
    if level:
        filters['level__icontains'] = level

    message = request.GET.get('message', '')
    if message:
        filters['message__icontains'] = message

    resourceId = request.GET.get('resourceId', '')
    if resourceId:
        filters['resourceId__iexact'] = resourceId

    timestamp = request.GET.get('timestamp', '')
    if timestamp:
        filters['timestamp__icontains'] = timestamp

    traceId = request.GET.get('traceId', '')
    if traceId:
        filters['traceId__icontains'] = traceId

    spanId = request.GET.get('spanId', '')
    if spanId:
        filters['spanId__icontains'] = spanId

    commit = request.GET.get('commit', '')
    if commit:
        filters['commit__icontains'] = commit

    parent_resourceId = request.GET.get('metadata.parentResourceId', '')
    if parent_resourceId:
        filters['metadata__parentResourceId__icontains'] = parent_resourceId

    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    if start_date and end_date:
        start_datetime = parse_datetime(f"{start_date}-01-01T00:00:00Z")
        end_datetime = parse_datetime(f"{end_date}-12-31T23:59:59Z")
        if start_datetime is not None and end_datetime is not None:
            end_datetime += timedelta(days=1)
            filters['timestamp__range'] = (
                start_datetime.replace(tzinfo=timezone.utc), end_datetime.replace(tzinfo=timezone.utc))
        else:
            return HttpResponseBadRequest("Error: Invalid date format")
    elif start_date:
        start_datetime = parse_datetime(f"{start_date}-01-01T00:00:00Z")
        end_datetime = parse_datetime(f"{start_date}-12-31T23:59:59Z")
        if start_datetime is not None and end_datetime is not None:
            end_datetime += timedelta(days=1)
            filters['timestamp__range'] = (
                start_datetime.replace(tzinfo=timezone.utc), end_datetime.replace(tzinfo=timezone.utc))
        else:
            return HttpResponseBadRequest("Error: Invalid date format")
    elif end_date:
        end_datetime = parse_datetime(f"{end_date}-12-31T23:59:59Z")
        if end_datetime is not None:
            end_datetime += timedelta(days=1)
            filters['timestamp__range'] = (
                timezone.datetime.min.replace(tzinfo=timezone.utc), end_datetime.replace(tzinfo=timezone.utc))
        else:
            return HttpResponseBadRequest("Error: Invalid date format")

    qs = qs.select_related('metadata').filter(**filters)
    print(qs.query)

    context = {
        'form_fields': form_fields,
        'log_entries': qs,
        'start_date': start_date,
        'end_date': end_date,
    }

    return render(request, "log_ingestor_app/search_form.html", context)
