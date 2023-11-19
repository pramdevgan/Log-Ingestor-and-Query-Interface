# Log Ingestor and Query Interface

## Introduction

This project implements a Log Ingestor and Query Interface, designed to efficiently handle large volumes of log data and provide a user-friendly interface for searching and filtering logs. The system includes a log ingestor that receives logs via HTTP on port `3000` and a query interface for interacting with the log data.

## Log Ingestor

### Features:

- Ingest logs in the provided JSON format.
- Ensures scalability to handle high volumes of logs efficiently.
- Mitigates potential bottlenecks such as I/O operations and database write speeds.
- Logs are ingested via an HTTP server running on port `3000` by default.

## Query Interface

### Features:

- User interface for full-text search across logs.
- Filters based on various log attributes:
  - level
  - message
  - resourceId
  - timestamp
  - traceId
  - spanId
  - commit
  - metadata.parentResourceId
- Efficient and quick search results.

### Sample Queries:

- Find all logs with the level set to "error".
- Search for logs with the message containing the term "Failed to connect".
- Retrieve all logs related to resourceId "server-1234".
- Filter logs between the timestamp "2023-09-10T00:00:00Z" and "2023-09-15T23:59:59Z". (Bonus)

## Advanced Features (Bonus):

- Search within specific date ranges.
- Utilize regular expressions for search.
- Allow combining multiple filters.
- Provide real-time log ingestion and searching capabilities.
- Implement role-based access to the query interface.

## System Design

The system is designed with the following components:

1. **Log Ingestor (Python/Django):**

   - Handles log ingestion via HTTP on port `3000`.
   - Efficiently writes logs to a database.
2. **Query Interface (Python/Django):**

   - Provides a user interface for log search and filtering.
   - Communicates with the log database to fetch results.

## Running the Project

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Run the Log Ingestor:

   ```bash
   cd log_ingestor
   python manage.py runserver 3000
   ```

The log ingestor is now running and ready to receive logs.

4. Run the Query Interface:
   ```
   cd query_interface
   python manage.py runserver
   ```

Visit http://127.0.0.1:8000 in your web browser to access the query interface.

## API Endpoints

### Log Ingestor API

#### 1. Log Data Ingestion

* **URL:** `/api/logdata/`
* **Method:** `POST`
* **Description:** Ingests log data in the provided JSON format.
* **Request Body:**
  ```json
  {
  "level": "error",
  "message": "Failed to connect to DB",
  "resourceId": "server-1234",
  "timestamp": "2023-09-15T08:00:00Z",
  "traceId": "abc-xyz-123",
  "spanId": "span-456",
  "commit": "5e5342f",
  "metadata": {
          "parentResourceId": "server-0987"
      }
  }

  ```

**Response:**

* HTTP Status: 201 Created
* Serialized log data


### Query Interface API

#### 1. Log Data Search

* **URL:** `/api/query_search/`
* **Method:** `GET`
* **Description:** Retrieves log entries based on specified search parameters.
* **Query Parameters:**
  * `regex_search` (optional): Regex search on the log message field.
  * `level` (optional): Log level.
  * `message` (optional): Log message.
  * `resourceId` (optional): Resource identifier.
  * `timestamp` (optional): Timestamp of the log entry.
  * `traceId` (optional): Trace identifier.
  * `spanId` (optional): Span identifier.
  * `commit` (optional): Commit information.
  * `metadata.parentResourceId` (optional): Parent resource identifier.
  * `start_date` (optional): Start date for date range filtering (Bonus).
  * `end_date` (optional): End date for date range filtering (Bonus).
* **Response:**
  * HTTP Status: 200 OK
  * Serialized log entries

### Web Interface

* **URL:** `/`
* **Method:** `GET`
* **Description:** Renders a web-based search form for filtering log entries based on various parameters.
* **Query Parameters:**
  * Similar to the parameters used in the Log Data Search API.

## Note

* Ensure that the Log Ingestor is running and configured to handle log ingestion on port`3000`.
* The Log Ingestor and Query Interface should be part of the same Django project for seamless integration.
* Adjust the URL patterns and endpoints according to your Django project structure and requirements.
