"""
Django Log Ingestor Serializers

Author: Pramatma Vishwakarma
Date: 2023-11-19

This module defines Django serializers for log data and metadata, namely LogDataSerializer and MetadataSerializer.

Serializers:
    - MetadataSerializer: Serializes Metadata instances, specifically the 'parentResourceId' field.

    - LogDataSerializer: Serializes LogData instances with additional support for creating log entries with associated metadata.

        Fields:
        - level (str): Log level.
        - message (str): Log message.
        - resourceId (str): Resource identifier.
        - timestamp (datetime): Timestamp of the log entry.
        - traceId (str): Trace identifier.
        - spanId (str): Span identifier.
        - commit (str): Commit information.
        - metadata (MetadataSerializer): Nested serializer for Metadata.

        Methods:
        - create(self, validated_data): Overrides the create method to handle the creation of LogData instances with associated metadata.

Note: Ensure to use these serializers in views to handle serialization and deserialization of log data when interacting with the API.
"""
from rest_framework import serializers
from .models import LogData, Metadata


class MetadataSerializer(serializers.ModelSerializer):
    """
    MetadataSerializer

    Serializes Metadata instances, specifically the 'parentResourceId' field.

    Meta:
        model (Metadata): Metadata model.
        fields (list): List of fields to include in the serialized output.

    Example:
        {
            "parentResourceId": "example_parent_resource_id"
        }
    """

    class Meta:
        model = Metadata
        fields = ['parentResourceId']


class LogDataSerializer(serializers.ModelSerializer):
    """
    LogDataSerializer

    Serializes LogData instances with additional support for creating log entries with associated metadata.

    Fields:
        - level (str): Log level.
        - message (str): Log message.
        - resourceId (str): Resource identifier.
        - timestamp (datetime): Timestamp of the log entry.
        - traceId (str): Trace identifier.
        - spanId (str): Span identifier.
        - commit (str): Commit information.
        - metadata (MetadataSerializer): Nested serializer for Metadata.

    Methods:
        - create(self, validated_data): Overrides the create method to handle the creation of LogData instances with associated metadata.

    Example (Serialization):
        {
            "level": "INFO",
            "message": "Log message content",
            "resourceId": "example_resource_id",
            "timestamp": "2023-11-19T12:00:00Z",
            "traceId": "example_trace_id",
            "spanId": "example_span_id",
            "commit": "example_commit_info",
            "metadata": {
                "parentResourceId": "example_parent_resource_id"
            }
        }
    """

    metadata = MetadataSerializer()

    class Meta:
        model = LogData
        fields = ['level', 'message', 'resourceId', 'timestamp', 'traceId', 'spanId', 'commit', 'metadata']

    def create(self, validated_data):
        metadata_data = validated_data.pop('metadata')
        metadata_instance = Metadata.objects.create(**metadata_data)
        log_data = LogData.objects.create(metadata=metadata_instance, **validated_data)
        return log_data
