"""
Django Log Ingestor Models

Author: Pramatma Vishwakarma
Date: 2023-11-19

This module defines Django models for log data and metadata, namely Metadata and LogData.

Models:
    - Metadata: Represents additional metadata related to log entries.
      - parentResourceId: CharField with a maximum length of 255 characters, representing the parent resource identifier.

    - LogData: Represents individual log entries with various fields.
      - level: CharField with a maximum length of 255 characters, representing the log level.
      - message: TextField representing the log message.
      - resourceId: CharField with a maximum length of 255 characters, representing the resource identifier.
      - timestamp: DateTimeField representing the timestamp of the log entry.
      - traceId: CharField with a maximum length of 255 characters, representing the trace identifier.
      - spanId: CharField with a maximum length of 255 characters, representing the span identifier.
      - commit: CharField with a maximum length of 255 characters, representing commit information.
      - metadata: OneToOneField relationship with Metadata, allowing for the association of metadata with a log entry.
        (Optional, can be null and blank)

    Methods:
      - __str__: Returns a human-readable string representation of the LogData instance.
        Example: "{self.level}| {self.timestamp}"

Note: Ensure to run migrations after defining or updating these models to apply changes to the database schema.
"""
from django.db import models


class Metadata(models.Model):
    """
    Metadata Model

    Represents additional metadata related to log entries.

    Fields:
        - parentResourceId (CharField): CharField with a maximum length of 255 characters,
          representing the parent resource identifier.

    Methods:
        - __str__: Returns a human-readable string representation of the Metadata instance.
    """

    parentResourceId = models.CharField(max_length=255)

    def __str__(self):
        return self.parentResourceId


class LogData(models.Model):
    """
    LogData Model

    Represents individual log entries with various fields.

    Fields:
        - level (CharField): CharField with a maximum length of 255 characters, representing the log level.
        - message (TextField): TextField representing the log message.
        - resourceId (CharField): CharField with a maximum length of 255 characters, representing the resource identifier.
        - timestamp (DateTimeField): DateTimeField representing the timestamp of the log entry.
        - traceId (CharField): CharField with a maximum length of 255 characters, representing the trace identifier.
        - spanId (CharField): CharField with a maximum length of 255 characters, representing the span identifier.
        - commit (CharField): CharField with a maximum length of 255 characters, representing commit information.
        - metadata (OneToOneField): OneToOneField relationship with Metadata,
          allowing for the association of metadata with a log entry. (Optional, can be null and blank)

    Methods:
        - __str__: Returns a human-readable string representation of the LogData instance.
          Example: "{self.level}| {self.timestamp}"
    """

    level = models.CharField(max_length=255)
    message = models.TextField()
    resourceId = models.CharField(max_length=255)
    timestamp = models.DateTimeField()
    traceId = models.CharField(max_length=255)
    spanId = models.CharField(max_length=255)
    commit = models.CharField(max_length=255)
    metadata = models.OneToOneField(Metadata, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.level}| {self.timestamp}"
